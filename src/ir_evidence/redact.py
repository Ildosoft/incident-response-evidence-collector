import re

USER_PATH = re.compile(r"(?i)([A-Z]:\\Users\\)[^\\\s]+")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

def redact_text(value: str) -> str:
    value = USER_PATH.sub(r"\1[USER]", value)
    return IPV4.sub("[IP]", value)

def redact_record(record: dict) -> dict:
    return {key: redact_text(value) if isinstance(value, str) else value for key, value in record.items()}
