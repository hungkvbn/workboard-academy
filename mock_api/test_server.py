"""Black-box HTTP tests: python3 -m unittest discover -s mock_api -v"""
import json
from http.client import HTTPConnection
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import threading
import time
import unittest
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from server import make_server


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.temp.name) / 'test.sqlite3')
        self.server = make_server(self.db, port=0, quiet=True)
        self.thread = threading.Thread(target=lambda: self.server.serve_forever(poll_interval=0.01), daemon=True)
        self.thread.start()
        self.base = f'http://127.0.0.1:{self.server.server_port}'
        self.session = self.login()
        self.token = self.session['accessToken']

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def request(self, method, path, body=None, token=None, headers=None, raw=None):
        request_headers = dict(headers or {})
        if body is not None:
            raw = json.dumps(body, ensure_ascii=False).encode('utf-8')
            request_headers['Content-Type'] = 'application/json'
        if token:
            request_headers['Authorization'] = f'Bearer {token}'
        req = Request(self.base + path, data=raw, headers=request_headers, method=method)
        try:
            response = urlopen(req, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            data = response.read()
            return response.status, json.loads(data) if data else None, dict(response.headers)

    def login(self, email='learner1@example.test'):
        status, data, _ = self.request('POST', '/auth/login', {'email': email, 'password': 'learn1234'})
        self.assertEqual(status, 200)
        return data

    def create(self, task_id='task-001', title='  Học Dart  ', key=None, token=None, **fields):
        body = {'id': task_id, 'title': title, 'description': '', 'status': 'todo', 'dueAt': None, **fields}
        return self.request('POST', '/tasks', body, token or self.token,
                            {'Idempotency-Key': key or f'create-{task_id}'})

    def update(self, task, **changes):
        body = {k: task[k] for k in ('title', 'description', 'status', 'dueAt', 'version')}
        body.update(changes)
        return self.request('PUT', f'/tasks/{task["id"]}', body, self.token)

    def test_health_and_empty_database(self):
        self.assertEqual(self.request('GET', '/health')[1]['mode'], 'local-learning-only')
        self.assertEqual(self.request('GET', '/tasks', token=self.token)[1], {'items': [], 'nextCursor': None})

    def test_invalid_login_and_required_auth(self):
        self.assertEqual(self.request('POST', '/auth/login', {'email': 'learner1@example.test', 'password': 'bad'})[0], 401)
        self.assertEqual(self.request('GET', '/tasks')[0], 401)
        self.assertEqual(self.request('GET', '/tasks', token='invalid')[0], 401)

    def test_create_canonical_task_and_persistence(self):
        status, task, _ = self.create(ownerId='user-2', version=999)
        self.assertEqual(status, 201)
        self.assertEqual((task['title'], task['ownerId'], task['version']), ('Học Dart', 'user-1', 1))
        self.assertTrue(task['updatedAt'].endswith('Z'))
        self.assertEqual(self.request('GET', '/tasks/task-001', token=self.token)[1], task)
        # A second server instance reads the same disk state; auth is intentionally independent.
        second = make_server(self.db, port=0, quiet=True)
        try:
            self.assertEqual(second.app.get_task('user-1', 'task-001'), task)
        finally:
            second.server_close()

    def test_same_key_retry_does_not_duplicate(self):
        first = self.create()
        second = self.create()
        self.assertEqual(first[:2], second[:2])
        self.assertEqual(len(self.request('GET', '/tasks', token=self.token)[1]['items']), 1)

    def test_same_key_new_payload_rejected(self):
        self.create(key='same')
        status, data, _ = self.create(title='Changed', key='same')
        self.assertEqual((status, data['error']['code']), (409, 'idempotency_conflict'))
        self.assertEqual(self.create(key='different')[0], 409)

    def test_parallel_same_key_creates_one_row(self):
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: self.create(), range(4)))
        self.assertTrue(all(item[0] == 201 for item in results))
        self.assertTrue(all(item[1] == results[0][1] for item in results))
        self.assertEqual(len(self.request('GET', '/tasks', token=self.token)[1]['items']), 1)

    def test_owner_boundary_list_get_update_delete(self):
        _, task, _ = self.create()
        other = self.login('learner2@example.test')['accessToken']
        self.assertEqual(self.request('GET', '/tasks', token=other)[1]['items'], [])
        self.assertEqual(self.request('GET', '/tasks/task-001', token=other)[0], 404)
        body = {k: task[k] for k in ('title', 'description', 'status', 'dueAt', 'version')}
        self.assertEqual(self.request('PUT', '/tasks/task-001', body, other)[0], 404)
        self.assertEqual(self.request('DELETE', '/tasks/task-001', token=other, headers={'If-Match': '1'})[0], 404)
        # Each owner may independently use the same client ID and idempotency key.
        self.assertEqual(self.create(token=other)[0], 201)

    def test_update_version_conflict_preserves_latest(self):
        _, task, _ = self.create()
        status, updated, _ = self.update(task, status='doing')
        self.assertEqual((status, updated['version']), (200, 2))
        stale = self.update(task, title='Old client')
        self.assertEqual((stale[0], stale[1]['error']['code']), (409, 'version_conflict'))
        self.assertEqual(self.request('GET', '/tasks/task-001', token=self.token)[1], updated)

    def test_parallel_updates_have_exactly_one_winner(self):
        _, task, _ = self.create()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda title: self.update(task, title=title), ['A', 'B']))
        self.assertEqual(sorted(result[0] for result in results), [200, 409])
        self.assertEqual(self.request('GET', '/tasks/task-001', token=self.token)[1]['version'], 2)

    def test_delete_requires_version_and_handles_stale(self):
        _, task, _ = self.create()
        self.update(task, status='done')
        self.assertEqual(self.request('DELETE', '/tasks/task-001', token=self.token)[0], 400)
        self.assertEqual(self.request('DELETE', '/tasks/task-001', token=self.token, headers={'If-Match': '1'})[0], 409)
        self.assertEqual(self.request('DELETE', '/tasks/task-001', token=self.token, headers={'If-Match': '2'})[:2], (204, None))
        self.assertEqual(self.request('GET', '/tasks/task-001', token=self.token)[0], 404)

    def test_pagination_filters_and_invalid_cursor(self):
        for task_id, title, status in [('c', 'Dart three', 'todo'), ('a', 'Dart one', 'todo'), ('b', 'Flutter two', 'done')]:
            self.create(task_id, title, status=status)
        first = self.request('GET', '/tasks?limit=1&q=Dart&status=todo', token=self.token)[1]
        self.assertEqual(first['items'][0]['id'], 'a')
        second = self.request('GET', '/tasks?limit=1&q=Dart&status=todo&cursor=' + quote(first['nextCursor']), token=self.token)[1]
        self.assertEqual(second['items'][0]['id'], 'c')
        self.assertIsNone(second['nextCursor'])
        self.assertEqual(self.request('GET', '/tasks?cursor=bad', token=self.token)[0], 400)
        self.assertEqual(self.request('GET', '/tasks?cursor=' + quote(first['nextCursor']), token=self.token)[0], 400)
        for query in ['limit=0', 'limit=101', 'limit=no', 'status=bogus']:
            self.assertEqual(self.request('GET', '/tasks?' + query, token=self.token)[0], 400)

    def test_search_treats_percent_and_underscore_literally(self):
        self.create('one', '100% done')
        self.create('two', 'Normal')
        data = self.request('GET', '/tasks?q=%25', token=self.token)[1]
        self.assertEqual([task['id'] for task in data['items']], ['one'])

    def test_title_and_status_validation(self):
        self.assertEqual(self.create(title='   ')[0], 400)
        self.assertEqual(self.create(title='😀' * 61)[0], 400)
        self.assertEqual(self.create(title='😀' * 60)[0], 201)
        self.assertEqual(self.create(task_id='other', status='invalid')[0], 400)
        self.assertEqual(self.create(task_id='with/slash')[0], 400)
        self.assertEqual(self.request('POST', '/tasks', {'id': 'withoutkey', 'title': 'Missing key'}, self.token)[0], 400)

    def test_due_date_must_be_utc(self):
        for index, due in enumerate(['2026-01-01', '2026-01-01T00:00:00', '2026-01-01T00:00:00+07:00', 123]):
            self.assertEqual(self.create(task_id=str(index), dueAt=due)[0], 400)
        status, task, _ = self.create(dueAt='2026-01-01T00:00:00+00:00')
        self.assertEqual(status, 201)
        self.assertEqual(task['dueAt'], '2026-01-01T00:00:00.000Z')

    def test_put_requires_all_fields_and_integer_version(self):
        _, task, _ = self.create()
        self.assertEqual(self.request('PUT', '/tasks/task-001', {'title': 'x', 'version': 1}, self.token)[0], 400)
        self.assertEqual(self.update(task, version=True)[0], 400)
        self.assertEqual(self.update(task, version='1')[0], 400)

    def test_refresh_rotation_and_expired_access(self):
        # Deterministic expiry without waiting for wall-clock time.
        with self.server.app.token_lock:
            self.server.app.access[self.token] = ('user-1', time.monotonic() - 1)
        self.assertEqual(self.request('GET', '/tasks', token=self.token)[0], 401)
        payload = {'refreshToken': self.session['refreshToken']}
        status, renewed, _ = self.request('POST', '/auth/refresh', payload)
        self.assertEqual(status, 200)
        self.assertEqual(self.request('GET', '/tasks', token=renewed['accessToken'])[0], 200)
        self.assertEqual(self.request('POST', '/auth/refresh', payload)[0], 401)
        self.assertEqual(self.request('GET', '/tasks', token=self.token)[0], 401)

    def test_injected_failure_delay_and_limits(self):
        result = self.request('GET', '/tasks', token=self.token, headers={'X-Debug-Fail': '503'})
        self.assertEqual((result[0], result[1]['error']['code']), (503, 'debug_failure'))
        before = time.monotonic()
        self.assertEqual(self.request('GET', '/tasks', token=self.token, headers={'X-Debug-Delay-Ms': '80'})[0], 200)
        self.assertGreaterEqual(time.monotonic() - before, 0.075)
        for headers in [{'X-Debug-Delay-Ms': '-1'}, {'X-Debug-Delay-Ms': '3001'}, {'X-Debug-Fail': '401'}]:
            self.assertEqual(self.request('GET', '/tasks', token=self.token, headers=headers)[0], 400)

    def test_cors_only_local_browser_origins(self):
        headers = {'Origin': 'http://localhost:54321', 'Access-Control-Request-Method': 'POST'}
        status, _, response_headers = self.request('OPTIONS', '/tasks', headers=headers)
        self.assertEqual(status, 204)
        self.assertEqual(response_headers['Access-Control-Allow-Origin'], headers['Origin'])
        remote = self.request('OPTIONS', '/tasks', headers={'Origin': 'https://example.org'})[2]
        self.assertNotIn('Access-Control-Allow-Origin', remote)

    def test_malformed_json_and_body_limit(self):
        for raw in [b'[]', b'{', b'{"title":NaN}', b'{"title":"\\ud800"}']:
            self.assertEqual(self.request('POST', '/tasks', raw=raw, token=self.token, headers={'Content-Type': 'application/json'})[0], 400)
        # Oversized declarations are rejected before receiving/allocating the body.
        connection = HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        try:
            connection.putrequest('POST', '/tasks')
            connection.putheader('Authorization', f'Bearer {self.token}')
            connection.putheader('Content-Type', 'application/json')
            connection.putheader('Content-Length', str(1024 * 1024 + 1))
            connection.endheaders()
            response = connection.getresponse()
            self.assertEqual(response.status, 413)
            response.read()
        finally:
            connection.close()


if __name__ == '__main__':
    unittest.main()
