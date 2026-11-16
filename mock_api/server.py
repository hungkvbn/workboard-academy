#!/usr/bin/env python3
"""WorkBoard local teaching API. Deliberately NOT a production auth service."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import secrets
import sqlite3
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

MAX_BODY = 1024 * 1024
USERS = {
    'learner1@example.test': {'id': 'user-1', 'email': 'learner1@example.test'},
    'learner2@example.test': {'id': 'user-2', 'email': 'learner2@example.test'},
}
PASSWORD = 'learn1234'
TASK_ID = re.compile(r'^[A-Za-z0-9_-]{1,100}$')


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def title_length(value: str) -> int:
    # Dart String.length counts UTF-16 code units (an emoji commonly counts as 2).
    return len(value.encode('utf-16-le')) // 2


def validate_fields(data: dict) -> dict:
    title = data.get('title')
    if not isinstance(title, str):
        raise ApiError(400, 'validation', 'title must be a string.')
    title = title.strip()
    if not 1 <= title_length(title) <= 120:
        raise ApiError(400, 'validation', 'Trimmed title must have 1–120 UTF-16 code units.')
    description = data.get('description', '')
    status = data.get('status', 'todo')
    if not isinstance(description, str) or len(description) > 10000:
        raise ApiError(400, 'validation', 'description must be a string of at most 10000 characters.')
    if status not in ('todo', 'doing', 'done'):
        raise ApiError(400, 'validation', 'status must be todo, doing, or done.')
    due_at = data.get('dueAt')
    if due_at is not None:
        if not isinstance(due_at, str):
            raise ApiError(400, 'validation', 'dueAt must be null or an ISO 8601 UTC string.')
        try:
            dt = datetime.fromisoformat(due_at.replace('Z', '+00:00'))
            if dt.tzinfo is None or dt.utcoffset().total_seconds() != 0:
                raise ValueError('UTC required')
            due_at = dt.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        except ValueError:
            raise ApiError(400, 'validation', 'dueAt must include UTC Z or +00:00.')
    return {'title': title, 'description': description, 'status': status, 'dueAt': due_at}


def require_version(value) -> int:
    if type(value) is not int or value < 1:
        raise ApiError(400, 'validation', 'version must be a positive integer.')
    return value


class App:
    def __init__(self, db_path: str, token_ttl: float = 300):
        self.db_path, self.token_ttl = db_path, token_ttl
        self.token_lock = threading.Lock()
        self.access: dict[str, tuple[str, float]] = {}
        self.refresh: dict[str, tuple[str, str]] = {}
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS tasks (
                    owner_id TEXT NOT NULL, id TEXT NOT NULL, title TEXT NOT NULL,
                    description TEXT NOT NULL, status TEXT NOT NULL,
                    due_at TEXT, updated_at TEXT NOT NULL, version INTEGER NOT NULL,
                    PRIMARY KEY (owner_id, id)
                );
                CREATE TABLE IF NOT EXISTS idempotency (
                    owner_id TEXT NOT NULL, key TEXT NOT NULL, request_hash TEXT NOT NULL,
                    response TEXT NOT NULL, PRIMARY KEY (owner_id, key)
                );
            ''')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.db_path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def issue_tokens_locked(self, user_id: str) -> dict:
        access, refresh = secrets.token_urlsafe(24), secrets.token_urlsafe(32)
        self.access[access] = (user_id, time.monotonic() + self.token_ttl)
        self.refresh[refresh] = (user_id, access)
        user = next(user for user in USERS.values() if user['id'] == user_id)
        return {'accessToken': access, 'refreshToken': refresh, 'expiresIn': self.token_ttl, 'user': user}

    def login(self, data: dict) -> dict:
        email, password = data.get('email'), data.get('password')
        if not isinstance(email, str) or email not in USERS or password != PASSWORD:
            raise ApiError(401, 'invalid_credentials', 'Incorrect demo email or password.')
        with self.token_lock:
            return self.issue_tokens_locked(USERS[email]['id'])

    def refresh_tokens(self, data: dict) -> dict:
        token = data.get('refreshToken')
        if not isinstance(token, str):
            raise ApiError(401, 'invalid_refresh', 'Invalid or already used refresh token.')
        with self.token_lock:
            pair = self.refresh.pop(token, None)
            if pair is None:
                raise ApiError(401, 'invalid_refresh', 'Invalid or already used refresh token.')
            user_id, old_access = pair
            self.access.pop(old_access, None)
            return self.issue_tokens_locked(user_id)

    def authenticate(self, authorization: str | None) -> str:
        if not authorization or not authorization.startswith('Bearer '):
            raise ApiError(401, 'unauthorized', 'A valid Bearer token is required.')
        token = authorization[7:]
        with self.token_lock:
            pair = self.access.get(token)
            if not pair or pair[1] <= time.monotonic():
                self.access.pop(token, None)
                raise ApiError(401, 'unauthorized', 'Access token is invalid or expired.')
            return pair[0]

    @staticmethod
    def task(row) -> dict:
        return {'id': row['id'], 'title': row['title'], 'description': row['description'],
                'status': row['status'], 'dueAt': row['due_at'], 'updatedAt': row['updated_at'],
                'version': row['version'], 'ownerId': row['owner_id']}

    def get_task(self, owner: str, task_id: str) -> dict:
        with self.connect() as db:
            row = db.execute('SELECT * FROM tasks WHERE owner_id=? AND id=?', (owner, task_id)).fetchone()
        if row is None:
            raise ApiError(404, 'not_found', 'Task not found.')
        return self.task(row)

    def list_tasks(self, owner: str, query: dict) -> dict:
        try:
            limit = int(query.get('limit', ['20'])[0])
        except (ValueError, IndexError):
            raise ApiError(400, 'validation', 'limit must be an integer from 1 to 100.')
        if not 1 <= limit <= 100:
            raise ApiError(400, 'validation', 'limit must be an integer from 1 to 100.')
        q = query.get('q', [''])[0].strip()
        status = query.get('status', [''])[0]
        if status and status not in ('todo', 'doing', 'done'):
            raise ApiError(400, 'validation', 'Invalid status filter.')
        clauses, args = ['owner_id=?'], [owner]
        if q:
            # instr means % and _ are literal text, not SQL LIKE wildcards.
            clauses.append('instr(lower(title), lower(?)) > 0')
            args.append(q)
        if status:
            clauses.append('status=?')
            args.append(status)
        cursor = query.get('cursor', [''])[0]
        if cursor:
            try:
                decoded = json.loads(base64.urlsafe_b64decode(cursor + '=' * (-len(cursor) % 4)))
                if not isinstance(decoded, dict) or decoded.get('q') != q or decoded.get('status') != status:
                    raise ValueError('Filter mismatch')
                after = decoded['after']
                if not isinstance(after, str) or not TASK_ID.fullmatch(after):
                    raise ValueError('Bad id')
            except (ValueError, KeyError, TypeError, UnicodeDecodeError):
                raise ApiError(400, 'validation', 'Invalid cursor or cursor belongs to different filters.')
            clauses.append('id > ?')
            args.append(after)
        with self.connect() as db:
            rows = db.execute('SELECT * FROM tasks WHERE ' + ' AND '.join(clauses) + ' ORDER BY id ASC LIMIT ?',
                              (*args, limit + 1)).fetchall()
        items = [self.task(row) for row in rows[:limit]]
        next_cursor = None
        if len(rows) > limit:
            payload = canonical({'after': items[-1]['id'], 'q': q, 'status': status}).encode()
            next_cursor = base64.urlsafe_b64encode(payload).decode().rstrip('=')
        return {'items': items, 'nextCursor': next_cursor}

    def create_task(self, owner: str, data: dict, key: str | None) -> dict:
        if not key or not 1 <= len(key) <= 128 or not key.isascii():
            raise ApiError(400, 'validation', 'Idempotency-Key is required (1–128 ASCII characters).')
        task_id = data.get('id')
        if not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
            raise ApiError(400, 'validation', 'id must have 1–100 ASCII letters, digits, hyphens or underscores.')
        fields = validate_fields(data)
        request_hash = hashlib.sha256(canonical(data).encode()).hexdigest()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            replay = db.execute('SELECT * FROM idempotency WHERE owner_id=? AND key=?', (owner, key)).fetchone()
            if replay:
                if replay['request_hash'] != request_hash:
                    raise ApiError(409, 'idempotency_conflict', 'This key was already used for a different request body.')
                return json.loads(replay['response'])
            try:
                db.execute('INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?)',
                           (owner, task_id, fields['title'], fields['description'], fields['status'], fields['dueAt'], utc_now(), 1))
            except sqlite3.IntegrityError:
                raise ApiError(409, 'duplicate_id', 'A task with this id already exists for this user.')
            row = db.execute('SELECT * FROM tasks WHERE owner_id=? AND id=?', (owner, task_id)).fetchone()
            task = self.task(row)
            db.execute('INSERT INTO idempotency VALUES (?,?,?,?)', (owner, key, request_hash, canonical(task)))
            return task

    def update_task(self, owner: str, task_id: str, data: dict) -> dict:
        for field in ('title', 'description', 'status', 'dueAt', 'version'):
            if field not in data:
                raise ApiError(400, 'validation', f'PUT requires {field}.')
        fields, version = validate_fields(data), require_version(data['version'])
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            existing = db.execute('SELECT version FROM tasks WHERE owner_id=? AND id=?', (owner, task_id)).fetchone()
            if existing is None:
                raise ApiError(404, 'not_found', 'Task not found.')
            if existing['version'] != version:
                raise ApiError(409, 'version_conflict', 'Task changed. Fetch the latest version before resolving this conflict.')
            db.execute('''UPDATE tasks SET title=?,description=?,status=?,due_at=?,updated_at=?,version=version+1
                          WHERE owner_id=? AND id=? AND version=?''',
                       (fields['title'], fields['description'], fields['status'], fields['dueAt'], utc_now(), owner, task_id, version))
            return self.task(db.execute('SELECT * FROM tasks WHERE owner_id=? AND id=?', (owner, task_id)).fetchone())

    def delete_task(self, owner: str, task_id: str, match: str | None):
        if not match or not re.fullmatch(r'[1-9][0-9]*', match):
            raise ApiError(400, 'validation', 'If-Match must contain the positive integer version, without quotes.')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT version FROM tasks WHERE owner_id=? AND id=?', (owner, task_id)).fetchone()
            if row is None:
                raise ApiError(404, 'not_found', 'Task not found.')
            if row['version'] != int(match):
                raise ApiError(409, 'version_conflict', 'Task changed. Fetch its latest version before deleting.')
            db.execute('DELETE FROM tasks WHERE owner_id=? AND id=? AND version=?', (owner, task_id, int(match)))


class Handler(BaseHTTPRequestHandler):
    server_version = 'WorkBoardMock/1'

    def setup(self):
        super().setup()
        self.connection.settimeout(10)

    def log_message(self, fmt, *args):
        # Avoid logging Authorization headers or request bodies.
        if not getattr(self.server, 'quiet', False):
            super().log_message(fmt, *args)

    def send_json(self, status: int, data=None):
        body = b'' if data is None else canonical(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        origin = self.headers.get('Origin', '')
        try:
            parsed = urlsplit(origin)
            local_origin = parsed.scheme in ('http', 'https') and parsed.hostname in ('localhost', '127.0.0.1', '::1')
        except ValueError:
            local_origin = False
        if local_origin:
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Vary', 'Origin')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type, Idempotency-Key, If-Match, X-Debug-Delay-Ms, X-Debug-Fail')
        self.end_headers()
        if body:
            self.wfile.write(body)

    def body(self) -> dict:
        try:
            length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            raise ApiError(400, 'validation', 'Invalid Content-Length.')
        if length < 0 or length > MAX_BODY:
            raise ApiError(413, 'body_too_large', 'Maximum request body size is 1 MiB.')
        if not self.headers.get('Content-Type', '').lower().startswith('application/json'):
            raise ApiError(400, 'validation', 'Use Content-Type: application/json.')
        try:
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise ValueError('Incomplete request')
            data = json.loads(raw, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Invalid JSON constant')))
            if not isinstance(data, dict):
                raise ValueError('Object required')
            # Reject lone surrogate escapes, which are not interoperable UTF-8 strings.
            canonical(data).encode('utf-8')
            return data
        except (ValueError, UnicodeError):
            raise ApiError(400, 'validation', 'Body must be a valid JSON object with valid Unicode.')

    def debug(self):
        delay = self.headers.get('X-Debug-Delay-Ms')
        if delay is not None:
            try:
                ms = int(delay)
            except ValueError:
                raise ApiError(400, 'validation', 'X-Debug-Delay-Ms must be an integer from 0 to 3000.')
            if not 0 <= ms <= 3000:
                raise ApiError(400, 'validation', 'X-Debug-Delay-Ms must be an integer from 0 to 3000.')
            time.sleep(ms / 1000)
        failure = self.headers.get('X-Debug-Fail')
        if failure is not None:
            if failure != '503':
                raise ApiError(400, 'validation', 'Only X-Debug-Fail: 503 is supported.')
            raise ApiError(503, 'debug_failure', 'Simulated transient failure; remove the header to recover.')

    def route(self):
        app = self.server.app
        path = urlsplit(self.path)
        self.debug()
        if self.command == 'GET' and path.path == '/health':
            return 200, {'status': 'ok', 'mode': 'local-learning-only'}
        if self.command == 'POST' and path.path == '/auth/login':
            return 200, app.login(self.body())
        if self.command == 'POST' and path.path == '/auth/refresh':
            return 200, app.refresh_tokens(self.body())
        if path.path != '/tasks' and not path.path.startswith('/tasks/'):
            raise ApiError(404, 'not_found', 'Endpoint not found.')
        owner = app.authenticate(self.headers.get('Authorization'))
        if path.path == '/tasks':
            if self.command == 'GET':
                return 200, app.list_tasks(owner, parse_qs(path.query, keep_blank_values=True))
            if self.command == 'POST':
                return 201, app.create_task(owner, self.body(), self.headers.get('Idempotency-Key'))
        else:
            task_id = unquote(path.path[len('/tasks/'):])
            if not TASK_ID.fullmatch(task_id):
                raise ApiError(400, 'validation', 'Invalid task id.')
            if self.command == 'GET':
                return 200, app.get_task(owner, task_id)
            if self.command == 'PUT':
                return 200, app.update_task(owner, task_id, self.body())
            if self.command == 'DELETE':
                app.delete_task(owner, task_id, self.headers.get('If-Match'))
                return 204, None
        raise ApiError(405, 'method_not_allowed', 'Method not supported for this endpoint.')

    def dispatch(self):
        try:
            status, data = self.route()
            self.send_json(status, data)
        except ApiError as error:
            self.send_json(error.status, {'error': {'code': error.code, 'message': error.message}})
        except (BrokenPipeError, ConnectionResetError, TimeoutError):
            pass  # Client canceled or timed out; this is expected in the race-condition lab.
        except sqlite3.Error:
            self.send_json(500, {'error': {'code': 'storage_error', 'message': 'Local database operation failed.'}})

    do_GET = do_POST = do_PUT = do_DELETE = dispatch

    def do_OPTIONS(self):
        self.send_json(204)


def make_server(db_path: str, host='127.0.0.1', port=8765, token_ttl=300, quiet=False):
    server = ThreadingHTTPServer((host, port), Handler)
    server.daemon_threads = True
    server.app = App(db_path, token_ttl=token_ttl)
    server.quiet = quiet
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--db', default=str(Path(__file__).with_name('workboard.sqlite3')))
    parser.add_argument('--token-ttl', type=float, default=300, help='Access token lifetime in seconds (default: 300).')
    args = parser.parse_args()
    if args.token_ttl <= 0:
        parser.error('--token-ttl must be positive')
    server = make_server(args.db, args.host, args.port, args.token_ttl)
    print(f'WorkBoard mock: http://{args.host}:{server.server_port}; local learning ONLY. Ctrl+C to stop.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
