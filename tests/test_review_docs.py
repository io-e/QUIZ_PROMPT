"""Structure checks for teacher review documents (Python verifies structure; it never approves)."""
import csv, os, sys, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)

def rd(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f: return list(csv.DictReader(f))

class QuarantineReview(unittest.TestCase):
    def setUp(self): self.q = rd("docs/QUARANTINE_REVIEW.csv"); self.links = {r["link_id"]: r for r in rd("subjects/mathematics/reference/skill_programme_links.csv")}
    def test_18_links_9_skills_2_editions(self):
        self.assertEqual(len(self.q), 18); self.assertEqual(len({r["skill_id"] for r in self.q}), 9)
        self.assertEqual({r["edition_id"] for r in self.q}, {"MATH_C4_2020", "MATH_C4_2026"})
        self.assertEqual({r["link_id"] for r in self.q}, {k for k, v in self.links.items() if v["link_status"] == "QUARANTINE"})
    def test_statuses_unchanged_and_reviewer_columns_empty(self):
        for r in self.q:
            self.assertEqual((r["link_status"], r["approval"]), ("QUARANTINE", "PENDING"))
            self.assertEqual((self.links[r["link_id"]]["link_status"], self.links[r["link_id"]]["approval"]), ("QUARANTINE", "PENDING"))
            for c in ("reviewer_1", "review_1_date", "decision_1", "reviewer_2", "review_2_date", "decision_2"): self.assertEqual(r[c], "")
    def test_proposal_fields(self):
        for r in self.q:
            self.assertIn(r["grok_proposed_decision"], ("SUPPORTED", "PARTIALLY_SUPPORTED", "NOT_SUPPORTED"))
            self.assertTrue(r["official_source_url"].startswith("https://")); self.assertTrue(r["page"]); self.assertTrue(r["passages_found"])
            if r["grok_proposed_decision"] != "SUPPORTED" or r["proposed_classification_if_unsupported"]:
                self.assertIn(r["proposed_classification_if_unsupported"], ("PREREQUISITE", "ENRICHMENT", "EXCLUDED_FROM_EXAM_SELECTION"))
            if r["grok_confidence"] != "high" or r["grok_proposed_decision"] != "SUPPORTED": self.assertEqual(r["needs_second_review"], "YES")
    def test_never_both_editions_rejected(self):
        by = {}
        for r in self.q: by.setdefault(r["skill_id"], []).append(r["grok_proposed_decision"])
        for s, d in by.items(): self.assertNotEqual(d, ["NOT_SUPPORTED"] * 2, s)

class LinkApprovalWorklist(unittest.TestCase):
    def test_all_668_links_quarantine_first_blank(self):
        w = rd("docs/LINK_APPROVAL_WORKLIST.csv"); links = rd("subjects/mathematics/reference/skill_programme_links.csv")
        self.assertEqual(len(w), 668); self.assertEqual({r["link_id"] for r in w}, {r["link_id"] for r in links})
        self.assertTrue(all(r["link_status"] == "QUARANTINE" for r in w[:18])); self.assertTrue(all(r["link_status"] != "QUARANTINE" for r in w[18:]))
        for r in w:
            for c in ("teacher_source_url", "teacher_passage", "teacher_page", "reviewer", "review_date", "decision"): self.assertEqual(r[c], "")
            self.assertEqual(r["approval"], "PENDING")

if __name__ == "__main__": unittest.main(verbosity=2)
