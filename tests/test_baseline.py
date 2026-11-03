"""Frozen MATH_REF_v11 baseline: hashes must not drift; frozen manifests are immutable; freeze != release."""
import os, sys, tempfile, unittest, json, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
from quiz_eval import baselines as B, programme_resolver as P

class FrozenBaseline(unittest.TestCase):
    def setUp(self): self.m = B.load_baseline("MATH_REF_v11")
    def test_no_hash_drift(self):
        self.assertEqual(B.verify_baseline("MATH_REF_v11"), [])
    def test_every_tracked_v11_file_listed(self):
        self.assertEqual(sorted(self.m["files_sha256"]), B.tracked_files("Math_Diagnostic_Reference_CLAUDE_v11"))
        self.assertEqual(self.m["file_count"], len(self.m["files_sha256"]))
    def test_freeze_is_not_release(self):
        self.assertIs(self.m["frozen"], True); self.assertIs(self.m["approved"], False)
        self.assertEqual(self.m["release_status"], {"paper": "HOLD", "digital": "HOLD"})
        self.assertEqual(self.m["kind"], "COMPARISON_BASELINE"); self.assertIn("NOT a pedagogical release", self.m["note"])
        self.assertNotIn("PASS", json.dumps({k: v for k, v in self.m.items() if k != "files_sha256"}))
    def test_prompt_and_engine_recorded(self):
        self.assertEqual(self.m["prompt"]["sha256"], B.sha256_file(os.path.join(ROOT, self.m["prompt"]["file"])))
        self.assertEqual(self.m["engine_version"], "quiz_eval/1.0"); self.assertEqual(len(self.m["source_commit"]), 40)
    def test_refuses_overwrite(self):
        with self.assertRaises(FileExistsError): B.write_baseline(dict(self.m))
    def test_drift_detected_on_copy(self):
        with tempfile.TemporaryDirectory() as t:
            for d in ("Math_Diagnostic_Reference_CLAUDE_v11", "subjects"): shutil.copytree(os.path.join(ROOT, d), os.path.join(t, d))
            shutil.copytree(os.path.join(ROOT, ".git"), os.path.join(t, ".git"))
            f = os.path.join(t, "Math_Diagnostic_Reference_CLAUDE_v11", "README_v11.md")
            with open(f, "a", encoding="utf-8") as fh: fh.write("x")
            self.assertEqual(B.verify_baseline("MATH_REF_v11", t), ["changed Math_Diagnostic_Reference_CLAUDE_v11/README_v11.md"])
    def test_manifest_references_exact_baseline(self):
        m = P.resolve("CURRENT_FOR_COHORT", "mathematics", "5e", "general", school_year="2026-2027")
        self.assertEqual(m["reference_version"], "MATH_REF_v11")
        self.assertEqual(m["reference_baseline"]["sha256"], B.sha256_file(os.path.join(ROOT, B.BASELINE_DIR, "MATH_REF_v11.manifest.json")))
        self.assertEqual(m["curriculum_edition"]["id"], "MATH_C4_2026")
    def test_approval_schema_is_stub(self):
        with open(os.path.join(ROOT, B.BASELINE_DIR, "APPROVAL_MANIFEST_SCHEMA.json"), encoding="utf-8") as f: s = json.load(f)
        self.assertTrue(s["status"].startswith("STUB"))
        self.assertFalse([x for x in os.listdir(os.path.join(ROOT, B.BASELINE_DIR)) if "APPROVAL" in x and x != "APPROVAL_MANIFEST_SCHEMA.json"])

if __name__ == "__main__": unittest.main(verbosity=2)
