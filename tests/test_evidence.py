import sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).parents[1]; sys.path.insert(0, str(ROOT / "src"))
from ir_evidence.bundle import verify_manifest, write_jsonl, write_manifest
from ir_evidence.collectors import load_jsonl
from ir_evidence.redact import redact_record
from ir_evidence.timeline import timeline
from ir_evidence.report import write_html

class EvidenceTests(unittest.TestCase):
    def test_timeline_and_redaction(self):
        records = load_jsonl((ROOT / "fixtures" / "synthetic_events.jsonl").read_text(encoding="utf-8")); ordered = timeline(records)
        self.assertEqual(ordered[0]["record_type"], "service")
        redacted = redact_record(records[0]); self.assertIn("[USER]", redacted["path"]); self.assertEqual(redacted["remote_ip"], "[IP]")
    def test_manifest_detects_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); write_jsonl(root / "evidence.jsonl", [{"safe": True}]); write_manifest(root); self.assertEqual(verify_manifest(root), [])
            (root / "evidence.jsonl").write_text("changed", encoding="utf-8"); self.assertEqual(verify_manifest(root), ["evidence.jsonl"])
    def test_fixtures_are_text_only(self):
        self.assertTrue(all(path.suffix == ".jsonl" for path in (ROOT / "fixtures").iterdir()))
    def test_html_escapes_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "report.html"; write_html(target, [{"record_type":"fixture","data":"<script>"}])
            self.assertNotIn("<script>", target.read_text(encoding="utf-8"))

if __name__ == "__main__": unittest.main()
