from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("".join(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")

def build_manifest(directory: Path) -> dict:
    files = []
    for path in sorted(p for p in directory.rglob("*") if p.is_file() and p.name != "manifest.json"):
        files.append({"path": path.relative_to(directory).as_posix(), "size": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return {"created_utc": datetime.now(timezone.utc).isoformat(), "algorithm": "SHA-256", "files": files, "read_only_collection": True}

def write_manifest(directory: Path) -> Path:
    target = directory / "manifest.json"; target.write_text(json.dumps(build_manifest(directory), indent=2), encoding="utf-8"); return target

def verify_manifest(directory: Path) -> list[str]:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8")); errors = []
    for entry in manifest["files"]:
        path = directory / entry["path"]
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]: errors.append(entry["path"])
    return errors
