"""Regression tests for quiz_eval (run: python3 -I tests/test_versioning.py)."""
import csv, os, shutil, sys, tempfile, unittest, json, copy
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quiz_eval import programme_resolver as PR, programme_diff as PD, release_gates as RG
from quiz_eval.migrations import Migrations
from quiz_eval.yamlio import load
from codex_cases import load_cases

def R(**k): return PR.resolve(**k)
def ed(m): return m["curriculum_edition"]["id"]

class CodexSelectionCases(unittest.TestCase):
    """The 12 golden cases of docs/codex/examples/selection_cases.yaml, read verbatim."""
    def test_codex_cases(self):
        cases = load_cases(os.path.join(ROOT, "docs", "codex", "examples", "selection_cases.yaml"))
        self.assertEqual(len(cases), 12)
        for i, c in enumerate(cases, 1):
            inp = dict(c["input"]); policy = inp.pop("policy")
            with self.subTest(case=i, input=c["input"]):
                if "expect_error" in c:
                    with self.assertRaises(PR.ResolutionError) as cm: R(policy=policy, **inp)
                    self.assertEqual(cm.exception.code, c["expect_error"])
                else:
                    m = R(policy=policy, **inp)
                    self.assertEqual(ed(m), c["expect_programme"])
                    if "expect_exam_profile" in c: self.assertEqual(m["exam_session"]["id"], c["expect_exam_profile"])

class HistoricalBrevet(unittest.TestCase):
    def test_sessions(self):
        for s, e in ((2025, "MATH_C4_2020"), (2026, "MATH_C4_2020"), (2027, "MATH_C4_2020"), (2028, "MATH_C4_2020"), (2029, "MATH_C4_2026")):
            m = R(policy="HISTORICAL_EXAM", subject="mathematics", grade="3e", track="general", assessment="DNB_MATH", exam_session=s)
            self.assertEqual(ed(m), e, s); self.assertEqual(m["exam_session"]["id"], f"DNB_MATH_{s}")
            self.assertEqual(m["exam_session"]["rules_status"], "UNVERIFIED")  # rules stored separately, not yet verified
            self.assertEqual(m["label"], "HISTORICAL_EXAM")
    def test_unknown_session(self):
        with self.assertRaises(PR.ResolutionError) as cm:
            R(policy="HISTORICAL_EXAM", subject="mathematics", grade="3e", track="general", assessment="DNB_MATH", exam_session=2019)
        self.assertEqual(cm.exception.code, "UNKNOWN_EXAM_SESSION")

class StaggeredImplementation(unittest.TestCase):
    CASES = [  # (grade, track, year, expected)
        ("5e", "general", "2025-2026", "MATH_C4_2020"), ("5e", "general", "2026-2027", "MATH_C4_2026"),
        ("4e", "general", "2026-2027", "MATH_C4_2020"), ("4e", "general", "2027-2028", "MATH_C4_2026"),
        ("3e", "general", "2027-2028", "MATH_C4_2020"), ("3e", "general", "2028-2029", "MATH_C4_2026"),
        ("2nde", "general", "2025-2026", "MATH_2NDE_2019"), ("2nde", "general", "2026-2027", "MATH_2NDE_2026"),
        ("1re", "specialite", "2025-2026", "MATH_1RE_SPE_2019"), ("1re", "specialite", "2026-2027", "MATH_1RE_SPE_2026"),
        ("1re", "tronc_commun", "2025-2026", "MATH_1RE_ES_2022"), ("1re", "tronc_commun", "2026-2027", "MATH_1RE_ES_2026"),
        ("Tle", "specialite", "2026-2027", "MATH_TLE_SPE_2019"), ("Tle", "specialite", "2027-2028", "MATH_TLE_SPE_2026"),
        ("Tle", "complementaires", "2026-2027", "MATH_TLE_COMP_2019"), ("Tle", "complementaires", "2027-2028", "MATH_TLE_COMP_2026"),
        ("Tle", "expertes", "2026-2027", "MATH_TLE_EXP_2019"),
        ("MP2I", "cpge", "2021-2022", "MATH_MP2I_2021"), ("MPI", "cpge", "2022-2023", "MATH_MPI_2021")]
    def test_every_class(self):
        for g, t, y, e in self.CASES:
            with self.subTest(g=g, t=t, y=y): self.assertEqual(ed(R(policy="CURRENT_FOR_COHORT", subject="mathematics", grade=g, track=t, school_year=y)), e)
    def test_bounded_never_inferred(self):
        for g, t, y in (("Tle", "specialite", "2019-2020"), ("Tle", "expertes", "2027-2028"), ("MPI", "cpge", "2021-2022"), ("MP2I", "cpge", "2020-2021")):
            with self.subTest(g=g, y=y):
                with self.assertRaises(PR.ResolutionError) as cm: R(policy="CURRENT_FOR_COHORT", subject="mathematics", grade=g, track=t, school_year=y)
                self.assertEqual(cm.exception.code, "UNVERIFIED_EDITION")
    def test_no_overlaps(self):
        reg, _ = PR.load_registry("mathematics")
        for p in reg["programmes"]:
            for a in p["applies"]:
                for y in range(PR._year(a["from_year"]), PR._year(a["through_year"]) + 1):
                    PR.find_edition(reg, "mathematics", a["grade"], p["track"], f"{y}-{y+1}")  # raises on ambiguity
    def test_every_date_has_evidence(self):
        reg, _ = PR.load_registry("mathematics")
        for p in reg["programmes"]:
            for a in p["applies"]:
                for k in ("from_evidence", "through_evidence"):
                    self.assertIn(a[k]["status"], ("VERIFIED", "UNVERIFIED"))
                    if a[k]["status"] == "VERIFIED" and a[k]["quote"]: self.assertTrue(a[k]["url"].startswith("https://"))

class SubjectSpecificReform(unittest.TestCase):
    def test_physics_not_switched(self):
        m = R(policy="CURRENT_FOR_COHORT", subject="physics_chemistry", grade="5e", track="general", school_year="2026-2027")
        self.assertEqual(ed(m), "PHYS_C4_2020")  # maths 5e switched that year, physics did not
        self.assertEqual(ed(R(policy="CURRENT_FOR_COHORT", subject="mathematics", grade="5e", track="general", school_year="2026-2027")), "MATH_C4_2026")
    def test_physics_future_unverified(self):
        with self.assertRaises(PR.ResolutionError) as cm:
            R(policy="CURRENT_FOR_COHORT", subject="physics_chemistry", grade="3e", track="general", school_year="2028-2029")
        self.assertEqual(cm.exception.code, "UNVERIFIED_EDITION")
    def test_no_math_edition_in_physics_registry(self):
        reg, _ = PR.load_registry("physics_chemistry")
        self.assertTrue(all(p["subject"] == "physics_chemistry" and not p["id"].startswith("MATH_") for p in reg["programmes"]))

class ExplicitEdition(unittest.TestCase):
    def test_label(self):
        m = R(policy="EXPLICIT_EDITION", subject="mathematics", grade="3e", track="general", edition="MATH_C4_2020")
        self.assertEqual(m["label"], "HISTORICAL_SIMULATION"); self.assertEqual(ed(m), "MATH_C4_2020")
    def test_wrong_subject(self):
        with self.assertRaises(PR.ResolutionError):
            R(policy="EXPLICIT_EDITION", subject="physics_chemistry", grade="3e", track="general", edition="MATH_C4_2020")

class Reproducibility(unittest.TestCase):
    def test_byte_identical_manifest(self):
        k = dict(policy="HISTORICAL_EXAM", subject="mathematics", grade="3e", track="general", assessment="DNB_MATH", exam_session=2027)
        self.assertEqual(PR.manifest_bytes(R(**k)), PR.manifest_bytes(R(**k)))
        m = R(**k)
        for key in ("software_version", "reference_version", "curriculum_edition", "exam_session"): self.assertIn(key, m)
        self.assertEqual(m["software_version"], "quiz_eval/1.0"); self.assertEqual(m["reference_version"], "MATH_REF_v11")
        self.assertEqual(m["release_status"], {"paper": "HOLD", "digital": "HOLD"})

class SkillSelection(unittest.TestCase):
    def setUp(self):
        self.links = PR.load_links("mathematics")
        A = {r["target_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "subjects/mathematics/reference/sources/Official_Programme_Audit_600_GROK.csv"), encoding="utf-8"))}
        self.flag = {k: v["edition_flag"] for k, v in A.items() if v["level"] == "BREVET"}
    def dnb(self, s): return R(policy="HISTORICAL_EXAM", subject="mathematics", grade="3e", track="general", assessment="DNB_MATH", exam_session=s)
    def test_2026_only_excluded_from_dnb_2027(self):
        sel = set(PR.select_skills(self.dnb(2027), validated=False))
        only26 = {k for k, v in self.flag.items() if v == "2026_ONLY"}
        self.assertEqual(len(only26), 16); self.assertFalse(sel & only26)
        self.assertTrue(only26 <= set(PR.select_skills(self.dnb(2029), validated=False)))
    def test_2020_only_kept_for_history(self):
        only20 = {k for k, v in self.flag.items() if v == "2020_ONLY"}
        self.assertEqual(len(only20), 11)
        self.assertTrue(only20 <= set(PR.select_skills(self.dnb(2025), validated=False)))
        self.assertFalse(only20 & set(PR.select_skills(self.dnb(2029), validated=False)))
    def test_classification_counts(self):
        from collections import Counter
        self.assertEqual(Counter(self.flag.values()), Counter({"BOTH": 59, "2026_ONLY": 16, "2020_ONLY": 11, "NEITHER": 9}))
    def test_quarantine_never_selectable(self):
        q = {l["skill_id"] for l in self.links if l["link_status"] == "QUARANTINE"}
        self.assertEqual(len(q), 9)
        for s in (2025, 2027, 2029):
            self.assertFalse(q & set(PR.select_skills(self.dnb(s), validated=False)))
            self.assertEqual(PR.select_skills(self.dnb(s), validated=True), [])  # nothing APPROVED yet
    def test_quarantine_rows_have_action_and_pending(self):
        q = [l for l in self.links if l["link_status"] == "QUARANTINE"]
        self.assertEqual(len(q), 18)  # 9 NEITHER skills x 2 editions
        self.assertTrue(all(l["approval"] == "PENDING" and l["proposed_action"].startswith("TO_DECIDE") for l in q))
        self.assertTrue(all(l["approval"] == "PENDING" for l in self.links))
    def test_worklist_neither_first(self):
        wl = list(csv.DictReader(open(os.path.join(ROOT, "docs/REVIEW_WORKLIST.csv"), encoding="utf-8")))
        self.assertTrue(all(r["link_status"] == "QUARANTINE" for r in wl[:18]))
        self.assertEqual(len({r["skill_id"] for r in wl[:18]}), 9)
    def test_validated_requires_verified_edition(self):
        m = R(policy="CURRENT_FOR_COHORT", subject="mathematics", grade="1re", track="specialite", school_year="2025-2026")
        with self.assertRaises(PR.ResolutionError): PR.select_skills(m, validated=True)
    def test_ids_preserved(self):
        sk = list(csv.DictReader(open(os.path.join(ROOT, "subjects/mathematics/reference/skills.csv"), encoding="utf-8")))
        T = list(csv.DictReader(open(os.path.join(ROOT, "Math_Diagnostic_Reference_CLAUDE_v11/Math_Diagnostic_Targets_v11.csv"), encoding="utf-8")))
        self.assertEqual([s["skill_id"] for s in sk], [t["id"] for t in T])
        e1 = sorted(e["id"] for t in T for e in json.loads(t["errors_json"])); e2 = sorted(e for s in sk for e in s["error_ids"].split())
        self.assertEqual(e1, e2)

class Migration(unittest.TestCase):
    M = Migrations()
    def test_same(self): self.assertEqual(self.M.resolve("BR-NC-01")["current_id"], "BR-NC-01")
    def test_merged(self): self.assertEqual(self.M.resolve("BR-AP-01-E3"), {"current_id": "BR-AP-01-E1", "relation": "MERGED", "review_status": "BUILD"})
    def test_retired(self): self.assertEqual(self.M.resolve("M1-F2-02-E4")["relation"], "RETIRED"); self.assertIsNone(self.M.resolve("M1-F2-02-E4")["current_id"])
    def test_unmapped_and_unknown(self):
        self.assertEqual(self.M.resolve("BR-NC-F19")["relation"], "UNMAPPED"); self.assertEqual(self.M.resolve("NOPE-1")["relation"], "UNKNOWN")
    def test_partial_is_proposal(self): self.assertEqual(self.M.resolve("BR-NC-F01")["review_status"], "PROPOSED_UNREVIEWED")
    def test_reserved_pattern(self): self.assertTrue(self.M.is_reserved_pattern("BR-NC-F07"))

class NewBOWorkflow(unittest.TestCase):
    def test_register_diff_preserve_release(self):
        tmp = tempfile.mkdtemp()
        try:
            for d in ("subjects", "tests", "quiz_eval", "docs", "Math_Diagnostic_Reference_CLAUDE_v11"):
                (shutil.copytree if os.path.isdir(os.path.join(ROOT, d)) else shutil.copy)(os.path.join(ROOT, d), os.path.join(tmp, d))
            links_before = PR.load_links("mathematics", tmp)
            # approve one old link in the copy, then publish a fictitious future edition: approval must survive untouched
            p = os.path.join(tmp, "subjects/mathematics/reference/skill_programme_links.csv")
            links_before[-1]["link_status"] = "APPROVED"; links_before[-1]["reviewer"] = "test"; PD.write_csv(p, links_before)
            old = [l for l in links_before if l["edition_id"] == links_before[-1]["edition_id"]]
            reg = load(os.path.join(tmp, "subjects/mathematics/programme/editions.yaml"))
            with self.assertRaises(ValueError): PD.register_edition(reg, copy.deepcopy(reg["programmes"][0]))  # immutable ids
            newp = {"id": "MATH_MPI_2099_TEST", "subject": "mathematics", "track": "cpge", "title": "test", "sources": [],
                    "applies": [{"grade": "MPI", "from_year": "2099-2100", "through_year": "2099-2100",
                                 "from_evidence": {"status": "UNVERIFIED", "url": "", "quote": "", "note": "test"},
                                 "through_evidence": {"status": "UNVERIFIED", "url": "", "quote": "", "note": "test"}}]}
            out = PD.publish_new_edition("mathematics", newp, links_before[-1]["edition_id"], "TEST_R1", root=tmp, run_tests=False)
            after = PR.load_links("mathematics", tmp)
            self.assertEqual(after[:len(links_before)], links_before)  # old links (and the approval) preserved
            new = [l for l in after if l["edition_id"] == "MATH_MPI_2099_TEST"]
            self.assertEqual(len(new), len(old)); self.assertTrue(all(l["link_status"] == "TO_REVIEW" for l in new))
            self.assertTrue(os.path.exists(out["worklist"]) and os.path.exists(out["manifest"]))
            with self.assertRaises(FileExistsError): PD.write_release_manifest(os.path.dirname(out["manifest"]), "TEST_R1", [p], tmp)
            m = R(policy="CURRENT_FOR_COHORT", subject="mathematics", grade="MPI", track="cpge", school_year="2099-2100", root=tmp)
            self.assertEqual(ed(m), "MATH_MPI_2099_TEST"); self.assertEqual(PR.select_skills(m, validated=False, root=tmp), [])
        finally: shutil.rmtree(tmp)

class Gates(unittest.TestCase):
    def test_read_only(self):
        g, s = RG.read_gates(); self.assertEqual(s["paper"], "HOLD"); self.assertFalse(RG.release_allowed())
        with self.assertRaises(PermissionError): RG.set_gate("STRUCTURE_PASS", "PASS")

if __name__ == "__main__":
    unittest.main(verbosity=2)
