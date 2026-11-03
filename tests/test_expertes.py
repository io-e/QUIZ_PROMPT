"""Maths expertes: MATH_TLE_EXP_2019 stays current; after 2026-27 it is returned WITH a visible warning,
never replaced by the new Terminale spécialité edition, and never usable for a validated test."""
import os, sys, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
from quiz_eval import programme_resolver as P

def R(y): return P.resolve("CURRENT_FOR_COHORT", "mathematics", "Tle", "expertes", school_year=y)

class Expertes(unittest.TestCase):
    def test_verified_years_no_warning(self):
        for y in ("2020-2021", "2024-2025", "2026-2027"):
            m = R(y); self.assertEqual(m["curriculum_edition"]["id"], "MATH_TLE_EXP_2019"); self.assertEqual(m["warnings"], [])
    def test_after_2026_27_same_edition_with_warning(self):
        for y in ("2027-2028", "2028-2029", "2030-2031"):
            m = R(y)
            self.assertEqual(m["curriculum_edition"]["id"], "MATH_TLE_EXP_2019")
            self.assertNotEqual(m["curriculum_edition"]["id"], "MATH_TLE_SPE_2026")
            self.assertEqual(len(m["warnings"]), 1); self.assertIn("REQUIRES_CURRENT_STATUS_VERIFICATION", m["warnings"][0])
            self.assertEqual(m["curriculum_edition"]["verification"], "REQUIRES_CURRENT_STATUS_VERIFICATION")
    def test_not_an_end_date(self):
        self.assertEqual(R("2027-2028")["curriculum_edition"]["applies"]["through_year"], "REQUIRES_CURRENT_STATUS_VERIFICATION")
    def test_validated_test_refused_after_2026_27(self):
        with self.assertRaises(P.ResolutionError) as cm: P.select_skills(R("2027-2028"), validated=True)
        self.assertEqual(cm.exception.code, "UNVERIFIED_EDITION_FOR_VALIDATED_TEST")
    def test_before_rentree_2020_not_inferred(self):
        with self.assertRaises(P.ResolutionError): R("2019-2020")
    def test_specialite_unaffected(self):
        self.assertEqual(P.resolve("CURRENT_FOR_COHORT", "mathematics", "Tle", "specialite", school_year="2027-2028")["curriculum_edition"]["id"], "MATH_TLE_SPE_2026")

if __name__ == "__main__": unittest.main(verbosity=2)
