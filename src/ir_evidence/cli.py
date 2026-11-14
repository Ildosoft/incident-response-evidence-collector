from __future__ import annotations
import argparse, json
from pathlib import Path
from .bundle import verify_manifest, write_jsonl, write_manifest
from .collectors import collect_windows, load_jsonl
from .redact import redact_record
from .timeline import timeline
from .report import write_html

def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only IR evidence collector"); sub = parser.add_subparsers(dest="command", required=True)
    live = sub.add_parser("collect"); live.add_argument("--output", type=Path, required=True); live.add_argument("--redact", action="store_true"); live.add_argument("--html", action="store_true")
    offline = sub.add_parser("offline"); offline.add_argument("input", type=Path); offline.add_argument("--output", type=Path, required=True); offline.add_argument("--redact", action="store_true"); offline.add_argument("--html", action="store_true")
    verify = sub.add_parser("verify"); verify.add_argument("bundle", type=Path)
    args = parser.parse_args(argv)
    if args.command == "verify":
        errors = verify_manifest(args.bundle); print(json.dumps({"valid": not errors, "errors": errors}, indent=2)); return int(bool(errors))
    records = collect_windows() if args.command == "collect" else load_jsonl(args.input.read_text(encoding="utf-8"))
    if args.redact: records = [redact_record(item) for item in records]
    args.output.mkdir(parents=True, exist_ok=True); write_jsonl(args.output / "evidence.jsonl", records); write_jsonl(args.output / "timeline.jsonl", timeline(records))
    if args.html: write_html(args.output / "report.html", records)
    write_manifest(args.output)
    print(json.dumps({"output": str(args.output.resolve()), "records": len(records), "redacted": args.redact}, indent=2)); return 0

if __name__ == "__main__": raise SystemExit(main())
