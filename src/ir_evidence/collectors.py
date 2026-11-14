from __future__ import annotations
import csv, io, json, platform, subprocess
from datetime import datetime, timezone

def run_read_only(command: list[str], source: str) -> list[dict]:
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    return [{"timestamp": datetime.now(timezone.utc).isoformat(), "source": source, "record_type": "command_output", "exit_code": completed.returncode, "data": completed.stdout, "error": completed.stderr}]

def parse_tasklist(text: str) -> list[dict]:
    rows = []
    for row in csv.DictReader(io.StringIO(text)):
        rows.append({"record_type": "process", "image_name": row.get("Image Name"), "pid": row.get("PID"), "session": row.get("Session Name"), "memory": row.get("Mem Usage")})
    return rows

def collect_windows() -> list[dict]:
    if platform.system() != "Windows": raise RuntimeError("live collection is supported only on Windows")
    records = []
    commands = [(["tasklist", "/FO", "CSV", "/NH"], "tasklist"), (["netstat", "-ano"], "netstat"), (["sc.exe", "query", "type=", "service", "state=", "all"], "services")]
    for command, source in commands: records.extend(run_read_only(command, source))
    return records

def load_jsonl(text: str) -> list[dict]:
    return [json.loads(line) for line in text.splitlines() if line.strip()]
