from datetime import datetime

def timeline(records: list[dict]) -> list[dict]:
    def key(record):
        raw = record.get("timestamp", "")
        try: return datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except (TypeError, ValueError): return datetime.min
    return sorted(records, key=key)
