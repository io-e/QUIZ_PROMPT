# Validation results – programme-versioning-v1 (2026-11-03, Python 3.13.5)

## v11 package (unchanged; `git diff origin/main -- Math_Diagnostic_Reference_CLAUDE_v11` is empty)
```
scenarios: 21, failed: 0
rebuild check: 8 files, 0 differ []
STRUCTURE_PASS PASS
release_status: paper HOLD, digital HOLD
```

## New engine: `python3 -I tests/test_versioning.py`
```
test_codex_cases (__main__.CodexSelectionCases.test_codex_cases) ... /workspace/QUIZ_PROMPT/tests/codex_cases.py:13: ResourceWarning: unclosed file <_io.TextIOWrapper name='/workspace/QUIZ_PROMPT/docs/codex/examples/selection_cases.yaml' mode='r' encoding='utf-8'>
  for line in open(path, encoding="utf-8"):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_label (__main__.ExplicitEdition.test_label) ... ok
test_wrong_subject (__main__.ExplicitEdition.test_wrong_subject) ... ok
test_read_only (__main__.Gates.test_read_only) ... ok
test_sessions (__main__.HistoricalBrevet.test_sessions) ... ok
test_unknown_session (__main__.HistoricalBrevet.test_unknown_session) ... ok
test_merged (__main__.Migration.test_merged) ... ok
test_partial_is_proposal (__main__.Migration.test_partial_is_proposal) ... ok
test_reserved_pattern (__main__.Migration.test_reserved_pattern) ... ok
test_retired (__main__.Migration.test_retired) ... ok
test_same (__main__.Migration.test_same) ... ok
test_unmapped_and_unknown (__main__.Migration.test_unmapped_and_unknown) ... ok
test_register_diff_preserve_release (__main__.NewBOWorkflow.test_register_diff_preserve_release) ... ok
test_byte_identical_manifest (__main__.Reproducibility.test_byte_identical_manifest) ... ok
test_2020_only_kept_for_history (__main__.SkillSelection.test_2020_only_kept_for_history) ... /workspace/QUIZ_PROMPT/tests/test_versioning.py:108: ResourceWarning: unclosed file <_io.TextIOWrapper name='/workspace/QUIZ_PROMPT/subjects/mathematics/reference/sources/Official_Programme_Audit_600_GROK.csv' mode='r' encoding='utf-8'>
  A = {r["target_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "subjects/mathematics/reference/sources/Official_Programme_Audit_600_GROK.csv"), encoding="utf-8"))}
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_2026_only_excluded_from_dnb_2027 (__main__.SkillSelection.test_2026_only_excluded_from_dnb_2027) ... ok
test_classification_counts (__main__.SkillSelection.test_classification_counts) ... ok
test_ids_preserved (__main__.SkillSelection.test_ids_preserved) ... /workspace/QUIZ_PROMPT/tests/test_versioning.py:143: ResourceWarning: unclosed file <_io.TextIOWrapper name='/workspace/QUIZ_PROMPT/subjects/mathematics/reference/skills.csv' mode='r' encoding='utf-8'>
  sk = list(csv.DictReader(open(os.path.join(ROOT, "subjects/mathematics/reference/skills.csv"), encoding="utf-8")))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
/workspace/QUIZ_PROMPT/tests/test_versioning.py:144: ResourceWarning: unclosed file <_io.TextIOWrapper name='/workspace/QUIZ_PROMPT/Math_Diagnostic_Reference_CLAUDE_v11/Math_Diagnostic_Targets_v11.csv' mode='r' encoding='utf-8'>
  T = list(csv.DictReader(open(os.path.join(ROOT, "Math_Diagnostic_Reference_CLAUDE_v11/Math_Diagnostic_Targets_v11.csv"), encoding="utf-8")))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_quarantine_never_selectable (__main__.SkillSelection.test_quarantine_never_selectable) ... ok
test_quarantine_rows_have_action_and_pending (__main__.SkillSelection.test_quarantine_rows_have_action_and_pending) ... ok
test_validated_requires_verified_edition (__main__.SkillSelection.test_validated_requires_verified_edition) ... ok
test_worklist_neither_first (__main__.SkillSelection.test_worklist_neither_first) ... /workspace/QUIZ_PROMPT/tests/test_versioning.py:136: ResourceWarning: unclosed file <_io.TextIOWrapper name='/workspace/QUIZ_PROMPT/docs/REVIEW_WORKLIST.csv' mode='r' encoding='utf-8'>
  wl = list(csv.DictReader(open(os.path.join(ROOT, "docs/REVIEW_WORKLIST.csv"), encoding="utf-8")))
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_bounded_never_inferred (__main__.StaggeredImplementation.test_bounded_never_inferred) ... ok
test_every_class (__main__.StaggeredImplementation.test_every_class) ... ok
test_every_date_has_evidence (__main__.StaggeredImplementation.test_every_date_has_evidence) ... ok
test_no_overlaps (__main__.StaggeredImplementation.test_no_overlaps) ... ok
test_no_math_edition_in_physics_registry (__main__.SubjectSpecificReform.test_no_math_edition_in_physics_registry) ... ok
test_physics_future_unverified (__main__.SubjectSpecificReform.test_physics_future_unverified) ... ok
test_physics_not_switched (__main__.SubjectSpecificReform.test_physics_not_switched) ... ok

----------------------------------------------------------------------
Ran 29 tests in 0.190s

OK
```
The suite covers:
- the 12 Codex golden cases, read from `docs/codex/examples/selection_cases.yaml` and run as one subTest each;
- 19 per-class staggered scenarios;
- 5 DNB sessions;
- 4 bounded "never infer" cases;
- physics-chemistry isolation;
- EXPLICIT_EDITION labelling;
- byte-identical manifests;
- 2026_ONLY exclusion from DNB 2027;
- 2020_ONLY preservation;
- QUARANTINE never selectable;
- ID migrations;
- the new-BO workflow on a temporary copy;
- read-only gates.

## Applicability dates
VERIFIED means the date is quoted from a fetched official text. The quotes and URLs are in `subjects/*/programme/editions.yaml`.

| Edition | Grade/track | From | Through | Status |
|---|---|---|---|---|
| MATH_C4_2020 | 5e/4e/3e | 2020-2021 (Éduscol cycle 4 "En vigueur à la rentrée 2020") | 2025-26 / 2026-27 / 2027-28 (MENE2602912A art. 3) | VERIFIED |
| MATH_C4_2026 | 5e/4e/3e | 2026-27 / 2027-28 / 2028-29 (MENE2602912A art. 3) | 2028-29 horizon | VERIFIED |
| MATH_2NDE_2019 | 2nde | 2019-2020 | 2025-2026 (MENE2602914A art. 2) | from UNVERIFIED |
| MATH_2NDE_2026 | 2nde | 2026-2027 (MENE2602914A) | horizon | VERIFIED |
| MATH_1RE_SPE_2019 | 1re spé | 2019-2020 (Codex value) | 2025-2026 (MENE2602917A) | from UNVERIFIED |
| MATH_1RE_SPE_2026 | 1re spé | 2026-2027 (MENE2602917A) | horizon | VERIFIED |
| MATH_1RE_ES_2022 | 1re tronc commun | 2022-2023 | 2025-2026 (MENE2602916A) | from UNVERIFIED |
| MATH_1RE_ES_2026 | 1re tronc commun | 2026-2027 (MENE2602916A) | horizon | VERIFIED |
| MATH_TLE_SPE_2019 | Tle spé | 2020-2021 (MENE1921246A art. 2, BO spécial n°8 2019) | 2026-2027 (MENE2602919A: 2027-2028) | VERIFIED |
| MATH_TLE_SPE_2026 | Tle spé | 2027-2028 (MENE2602919A) | horizon | VERIFIED |
| MATH_TLE_COMP_2019 | Tle complémentaires | 2020-2021 (MENE1921265A art. 2) | 2026-2027 | VERIFIED |
| MATH_TLE_COMP_2026 | Tle complémentaires | 2027-2028 (BO n°14) | horizon | VERIFIED |
| MATH_TLE_EXP_2019 | Tle expertes | 2020-2021 (MENE1921264A art. 2) | 2026-2027 (bounded; no successor found) | through UNVERIFIED |
| MATH_MP2I_2021 | MP2I | 2021-2022 (ESRS2035779A) | 2026-2027 current-year bound | VERIFIED (search extract of the ESR BO page) |
| MATH_MPI_2021 | MPI | 2022-2023 (ESRS2111756A art. 2) | 2026-2027 current-year bound | VERIFIED (search extract) |
| PHYS_C4_2020 | 5e/4e/3e | 2020-2021 | 2026-2027 (Éduscol "Enseigner au cycle 4" table) | VERIFIED for 2026-27 only |

Exam rules: every DNB_MATH_2025–2029 rules entry is UNVERIFIED (DNB 2027+ rules page MENE2623228N was blocked, 403).

## Conflicts with the Codex kit (followed the verified source)
1. **MATH_TLE_SPE_2019 from_year.** The kit says 2019-2020. The BO spécial n°8 of 25 July 2019 (MENE1921246A, art. 2) says "entrent en vigueur à la rentrée scolaire 2020", so the registry uses **2020-2021**. Tle spé 2019-2020 therefore resolves to UNVERIFIED_EDITION.
2. **BO_C4_2020 source.** The kit cites https://www.education.gouv.fr/bo/20/Hebdo31/MENE2018714A.htm, which I could not fetch or check. The registry cites the Éduscol consolidated cycle 4 PDF, which I did fetch.
3. **MATH_1RE_SPE_2019 from_year 2019-2020.** I kept the kit's value but marked it UNVERIFIED, because the 2019 BO was not read.
4. **File format.** The kit's examples are block YAML and need PyYAML. The registries here are JSON-compatible YAML, because `python3 -I` has no PyYAML. The kit's selection_cases.yaml is read verbatim by a minimal reader (`tests/codex_cases.py`).
5. **Out of scope for v1.** These kit items are not implemented: the CLI (`py -3 -m quiz_eval ...`), the GitHub Actions CI, the errors.csv, sources.csv and id_migrations.csv per subject (error IDs are listed in skills.csv; migrations are read from v11), and resolved_manifest.yaml (the manifest is canonical JSON from `manifest_bytes`).
