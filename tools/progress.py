#!/usr/bin/env python3
"""Theo dõi 96 lab bằng tệp JSON có thể commit và nhập vào trang học."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILE = ROOT / "tracking" / "workboard-progress.json"


def normalize(data):
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("weeks"), dict):
        raise ValueError("Cần tệp tiến độ WorkBoard version 1 với object weeks.")
    result = {"version": 1, "weeks": {}}
    for n in range(1, 33):
        week = data["weeks"].get(str(n), {})
        if not isinstance(week, dict):
            raise ValueError(f"Tuần {n} không đúng cấu trúc.")
        labs = week.get("labs", [False, False, False])
        accepted = week.get("accepted", False)
        if not isinstance(labs, list) or len(labs) != 3 or any(type(x) is not bool for x in labs):
            raise ValueError(f"Tuần {n} cần ba giá trị true/false cho labs.")
        if type(accepted) is not bool:
            raise ValueError(f"Tuần {n}: accepted phải là true/false.")
        result["weeks"][str(n)] = {"labs": list(labs), "accepted": accepted}
    return result


def empty():
    return normalize({"version": 1, "weeks": {}})


def read(path):
    if not path.exists():
        return empty()
    return normalize(json.loads(path.read_text(encoding="utf-8-sig")))


def write(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=".progress-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(normalize(state), stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def merge(current, incoming):
    result = normalize(current)
    incoming = normalize(incoming)
    for n, week in result["weeks"].items():
        week["labs"] = [a or b for a, b in zip(week["labs"], incoming["weeks"][n]["labs"])]
        week["accepted"] = week["accepted"] or incoming["weeks"][n]["accepted"]
    return result


def lab_id(value):
    match = re.fullmatch(r"W(\d{2})-L([123])", value.upper())
    if not match or not 1 <= int(match[1]) <= 32:
        raise argparse.ArgumentTypeError("Dùng ID từ W01-L1 đến W32-L3.")
    return str(int(match[1])), int(match[2]) - 1


def week_id(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Tuần phải là số 1–32.") from exc
    if not 1 <= number <= 32:
        raise argparse.ArgumentTypeError("Tuần phải là số 1–32.")
    return str(number)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="Tệp tiến độ, mặc định tracking/workboard-progress.json")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status", help="Xem tiến độ")
    for action in ("done", "undo"):
        commands.add_parser(action, help="Đánh dấu hoặc bỏ đánh dấu một lab").add_argument("lab", type=lab_id)
    for action in ("accept", "unaccept"):
        commands.add_parser(action, help="Xác nhận hoặc bỏ xác nhận nghiệm thu tuần").add_argument("week", type=week_id)
    imp = commands.add_parser("import", help="Nhập JSON xuất từ trang học")
    imp.add_argument("source", type=Path)
    imp.add_argument("--replace", action="store_true", help="Lấy chính xác trạng thái tệp, gồm cả các ô đã bỏ chọn")
    commands.add_parser("export", help="Xuất JSON để nhập vào trang học").add_argument("destination", type=Path)
    args = parser.parse_args(argv)
    try:
        state = read(args.file)
        if args.command in ("done", "undo"):
            week, index = args.lab
            state["weeks"][week]["labs"][index] = args.command == "done"
            if args.command == "undo":
                state["weeks"][week]["accepted"] = False
            write(args.file, state)
        elif args.command in ("accept", "unaccept"):
            if args.command == "accept" and not all(state["weeks"][args.week]["labs"]):
                raise ValueError("Cần hoàn thành cả ba lab trước khi xác nhận nghiệm thu.")
            state["weeks"][args.week]["accepted"] = args.command == "accept"
            write(args.file, state)
        elif args.command == "import":
            if not args.source.is_file():
                raise ValueError("Không tìm thấy tệp cần nhập.")
            incoming = read(args.source)
            state = incoming if args.replace else merge(state, incoming)
            write(args.file, state)
        elif args.command == "export":
            write(args.destination, state)
        labs = sum(sum(w["labs"]) for w in state["weeks"].values())
        weeks = sum(w["accepted"] and all(w["labs"]) for w in state["weeks"].values())
        print(f"{labs}/96 lab; {weeks}/32 tuần đạt nghiệm thu.")
        if args.command == "status":
            for n, w in state["weeks"].items():
                if any(w["labs"]) or w["accepted"]:
                    flags = " ".join(f"L{i + 1}:{'x' if done else '-'}" for i, done in enumerate(w["labs"]))
                    print(f"Tuần {int(n):02}: {flags}; nghiệm thu={'đạt' if w['accepted'] and all(w['labs']) else 'chưa'}")
        print(f"Tệp theo dõi: {args.file}")
        return 0
    except (ValueError, OSError) as exc:
        print(f"Lỗi: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
