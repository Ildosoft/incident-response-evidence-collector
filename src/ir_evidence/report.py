from __future__ import annotations
import html, json
from collections import Counter
from pathlib import Path

def write_html(path: Path, records: list[dict]) -> None:
    counts = Counter(str(record.get("record_type", "unknown")) for record in records)
    rows = "".join(f"<tr><td>{html.escape(kind)}</td><td>{count}</td></tr>" for kind, count in sorted(counts.items()))
    preview = html.escape(json.dumps(records[:10], indent=2, ensure_ascii=False))
    body = f"""<!doctype html><meta charset='utf-8'><title>IR Evidence Report</title><style>body{{font:15px system-ui;margin:2rem;background:#0d1117;color:#e6edf3}}h1{{color:#58a6ff}}table{{border-collapse:collapse;background:#161b22}}th,td{{border:1px solid #30363d;padding:.6rem;text-align:left}}pre{{white-space:pre-wrap;background:#161b22;padding:1rem}}</style><h1>Incident Response Evidence Report</h1><p>Read-only collection. Review and redact before sharing.</p><table><tr><th>Record type</th><th>Count</th></tr>{rows}</table><h2>Redacted preview</h2><pre>{preview}</pre>"""
    path.write_text(body, encoding="utf-8")
