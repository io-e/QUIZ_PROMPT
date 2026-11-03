"""DNB exam profiles: each session stored independently; historical simulation reproduces the original format."""
import os, sys, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
from quiz_eval import programme_resolver as P
from quiz_eval.yamlio import load

def fmt(s):
    return P.resolve("HISTORICAL_EXAM", "mathematics", "3e", "general", assessment="DNB_MATH", exam_session=s)["exam_session"]["format"]

class ExamProfiles(unittest.TestCase):
    def test_each_session_recorded_independently(self):
        ex = load(os.path.join(ROOT, "subjects/mathematics/programme/exams.yaml"))["exam_profiles"]
        self.assertEqual([e["session"] for e in ex], [2025, 2026, 2027, 2028, 2029])
        self.assertEqual(len({e["id"] for e in ex}), 5)
        for e in ex:
            r = e["rules"]
            self.assertIn(r["source_status"], ("VERIFIED", "USER_REPORTED_PENDING_VERIFICATION"))
            self.assertTrue(r["url"].startswith("https://")); self.assertTrue(r["passage"]); self.assertTrue(r["page"])
            self.assertEqual(e["format_review"], "PENDING_TEACHER_CHECK")
    def test_2025_format(self):
        f = fmt(2025)
        self.assertEqual((f["total_duration_min"], f["scale"], len(f["parts"])), (120, "100 points", 1))
        self.assertTrue(f["parts"][0]["calculator"]); self.assertEqual(f["parts"][0]["points"], 100)
    def test_2026_format(self):
        p1, p2 = fmt(2026)["parts"]
        self.assertEqual((p1["duration_min"], p1["points"], p1["calculator"]), (20, 6, False))
        self.assertEqual((p2["duration_min"], p2["points"], p2["calculator"]), (100, 14, True))
        self.assertIsNot(p2["mcq_allowed"], False)  # no MCQ ban in the 2026 note
    def test_2027_onward_format(self):
        for s in (2027, 2028, 2029):
            p1, p2 = fmt(s)["parts"]
            self.assertEqual((p1["points"], p2["points"], p1["duration_min"], p2["duration_min"]), (6, 14, 20, 100))
            self.assertEqual(p1["answer_format"], "questions à réponses courtes")
            self.assertIs(p2["mcq_allowed"], False); self.assertFalse(p1["calculator"]); self.assertTrue(p2["calculator"])
    def test_formats_differ_by_session(self):
        self.assertNotEqual(fmt(2025), fmt(2026)); self.assertNotEqual(fmt(2026), fmt(2027))
        self.assertEqual(fmt(2027), fmt(2028))  # identical rules, still separate profiles
    def test_2028_2029_flagged_subject_to_amendment(self):
        ex = {e["session"]: e for e in load(os.path.join(ROOT, "subjects/mathematics/programme/exams.yaml"))["exam_profiles"]}
        for s in (2027, 2028, 2029):
            self.assertTrue(ex[s]["rules"]["subject_to_later_amendment"]); self.assertEqual(ex[s]["rules"]["applies_from_session"], 2027)
    def test_historical_2025_not_todays_format(self):
        m = P.resolve("HISTORICAL_EXAM", "mathematics", "3e", "general", assessment="DNB_MATH", exam_session=2025)
        self.assertEqual(m["label"], "HISTORICAL_EXAM"); self.assertEqual(m["curriculum_edition"]["id"], "MATH_C4_2020")
        self.assertNotIn("Automatismes", str(m["exam_session"]["format"]))

if __name__ == "__main__": unittest.main(verbosity=2)
