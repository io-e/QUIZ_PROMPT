# Validation results: programme-versioning-v1

Regenerated on 2026-11-03 with Python 3.13.5. Every suite was run as `python3 -I -X tracemalloc=5 -W error::ResourceWarning tests/<file>.py`, with all exits 0. `grep -c ResourceWarning` on every output gives **0**.

## v11 package (byte-identical)
- `git diff origin/main -- Math_Diagnostic_Reference_CLAUDE_v11` is empty.
- `quiz_eval.baselines.verify_baseline('MATH_REF_v11')` returns `[]` (no drift).
- The frozen manifest is `subjects/mathematics/reference/baselines/MATH_REF_v11.manifest.json`, sha256 `046eeb507049ee6e3a0a75b0761cb5d292cef278d56d0ef8caeebb34f77a2459`.

```
scenarios: 21, failed: 0
rebuild check: 8 files, 0 differ []
STRUCTURE_PASS PASS
release_status: paper HOLD, digital HOLD
```

## `tests/test_versioning.py`
```
test_codex_cases (__main__.CodexSelectionCases.test_codex_cases) ... ok
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
test_2020_only_kept_for_history (__main__.SkillSelection.test_2020_only_kept_for_history) ... ok
test_2026_only_excluded_from_dnb_2027 (__main__.SkillSelection.test_2026_only_excluded_from_dnb_2027) ... ok
test_classification_counts (__main__.SkillSelection.test_classification_counts) ... ok
test_ids_preserved (__main__.SkillSelection.test_ids_preserved) ... ok
test_quarantine_never_selectable (__main__.SkillSelection.test_quarantine_never_selectable) ... ok
test_quarantine_rows_have_action_and_pending (__main__.SkillSelection.test_quarantine_rows_have_action_and_pending) ... ok
test_validated_requires_verified_edition (__main__.SkillSelection.test_validated_requires_verified_edition) ... ok
test_worklist_neither_first (__main__.SkillSelection.test_worklist_neither_first) ... ok
test_bounded_never_inferred (__main__.StaggeredImplementation.test_bounded_never_inferred) ... ok
test_every_class (__main__.StaggeredImplementation.test_every_class) ... ok
test_every_date_has_evidence (__main__.StaggeredImplementation.test_every_date_has_evidence) ... ok
test_no_overlaps (__main__.StaggeredImplementation.test_no_overlaps) ... ok
test_no_math_edition_in_physics_registry (__main__.SubjectSpecificReform.test_no_math_edition_in_physics_registry) ... ok
test_physics_future_unverified (__main__.SubjectSpecificReform.test_physics_future_unverified) ... ok
test_physics_not_switched (__main__.SubjectSpecificReform.test_physics_not_switched) ... ok

----------------------------------------------------------------------
Ran 29 tests in 1.125s

OK
```

## `tests/test_baseline.py`
```
test_approval_schema_is_stub (__main__.FrozenBaseline.test_approval_schema_is_stub) ... ok
test_drift_detected_on_copy (__main__.FrozenBaseline.test_drift_detected_on_copy) ... ok
test_every_tracked_v11_file_listed (__main__.FrozenBaseline.test_every_tracked_v11_file_listed) ... ok
test_freeze_is_not_release (__main__.FrozenBaseline.test_freeze_is_not_release) ... ok
test_manifest_references_exact_baseline (__main__.FrozenBaseline.test_manifest_references_exact_baseline) ... ok
test_no_hash_drift (__main__.FrozenBaseline.test_no_hash_drift) ... ok
test_prompt_and_engine_recorded (__main__.FrozenBaseline.test_prompt_and_engine_recorded) ... ok
test_refuses_overwrite (__main__.FrozenBaseline.test_refuses_overwrite) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.214s

OK
```

## `tests/test_exam_profiles.py`
```
test_2025_format (__main__.ExamProfiles.test_2025_format) ... ok
test_2026_format (__main__.ExamProfiles.test_2026_format) ... ok
test_2027_onward_format (__main__.ExamProfiles.test_2027_onward_format) ... ok
test_2028_2029_flagged_subject_to_amendment (__main__.ExamProfiles.test_2028_2029_flagged_subject_to_amendment) ... ok
test_each_session_recorded_independently (__main__.ExamProfiles.test_each_session_recorded_independently) ... ok
test_formats_differ_by_session (__main__.ExamProfiles.test_formats_differ_by_session) ... ok
test_historical_2025_not_todays_format (__main__.ExamProfiles.test_historical_2025_not_todays_format) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.038s

OK
```

## `tests/test_expertes.py`
```
test_after_2026_27_same_edition_with_warning (__main__.Expertes.test_after_2026_27_same_edition_with_warning) ... ok
test_before_rentree_2020_not_inferred (__main__.Expertes.test_before_rentree_2020_not_inferred) ... ok
test_not_an_end_date (__main__.Expertes.test_not_an_end_date) ... ok
test_specialite_unaffected (__main__.Expertes.test_specialite_unaffected) ... ok
test_validated_test_refused_after_2026_27 (__main__.Expertes.test_validated_test_refused_after_2026_27) ... ok
test_verified_years_no_warning (__main__.Expertes.test_verified_years_no_warning) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.031s

OK
```

## `tests/test_review_docs.py`
```
test_all_668_links_quarantine_first_blank (__main__.LinkApprovalWorklist.test_all_668_links_quarantine_first_blank) ... ok
test_18_links_9_skills_2_editions (__main__.QuarantineReview.test_18_links_9_skills_2_editions) ... ok
test_never_both_editions_rejected (__main__.QuarantineReview.test_never_both_editions_rejected) ... ok
test_proposal_fields (__main__.QuarantineReview.test_proposal_fields) ... ok
test_statuses_unchanged_and_reviewer_columns_empty (__main__.QuarantineReview.test_statuses_unchanged_and_reviewer_columns_empty) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.154s

OK
```

## DNB exam profiles (subjects/mathematics/programme/exams.yaml)
Each session is stored separately; 2027, 2028 and 2029 share the same rules but are still separate profiles.

| Session | Format | Status | Source and passage |
|---|---|---|---|
| 2025 | 2 h, 100 points, calculator allowed (5 exercises; ex. 3 is an MCQ) | VERIFIED | Official paper https://www.education.gouv.fr/sites/default/files/2025-06/dipl-me-national-du-brevet-2025-math-matiques-441366.pdf p.1/8: "Durée de l’épreuve : 2 h 00 100 points … L'utilisation de la calculatrice avec mode examen actif est autorisée." |
| 2026 | P1 automatismes 20 min, no calculator, 6 pts; P2 problem solving 100 min, calculator, 14 pts; /20 | VERIFIED | MENE2515977N (note of 2-9-2025) https://www.education.gouv.fr/bo/2025/Hebdo33/MENE2515977N, read via https://web.archive.org/web/20260205090837/https://www.education.gouv.fr/bo/2025/Hebdo33/MENE2515977N §3.1.2: "Partie 1 – Automatismes : 6 points – 20 minutes Les élèves réalisent cette partie sans calculatrice … Partie 2 – Raisonnement et résolution de problèmes :14 points – 1 heure et 40 minutes"; "entre en vigueur à compter de la session 2026" |
| 2027, 2028, 2029 | Same 6/14 split; P1 short-answer questions; P2 with calculator, MCQ excluded | VERIFIED (from session 2027, subject to later amendments) | MENE2623228N, BO spécial n°4 of 17-9-2026, https://www.education.gouv.fr/sites/default/files/document/20260917boenjsspe4pdf-520753.pdf, PDF p.12: "Elle entre en vigueur à compter de la session 2027 du DNB"; pp.19-20: "questions à réponses courtes … toutes les modalités possibles hormis celle du questionnaire à choix multiple" |

The education.gouv.fr HTML pages returned 403. The official PDFs downloaded directly, and the 2026 note was read from its web.archive.org snapshot. No value is `USER_REPORTED_PENDING_VERIFICATION`: every user-supplied value matched the official text.

## Quarantine review and link approval
- `docs/QUARANTINE_REVIEW.{md,csv}` holds Grok's proposals for the 18 links: 7 SUPPORTED (3 at high confidence), 10 PARTIALLY_SUPPORTED, 1 NOT_SUPPORTED. 16 links need a second review.
- All 18 links stay QUARANTINE / PENDING.
- `docs/LINK_APPROVAL_WORKLIST.csv` lists all 668 links, the 18 quarantine links first, with every teacher column empty.

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
| MATH_TLE_EXP_2019 | Tle expertes | 2020-2021 (MENE1921264A art. 2) | REQUIRES_CURRENT_STATUS_VERIFICATION after 2026-2027 (no end date; no replacement in BO n°14 2026) | from VERIFIED; current status to verify |
| MATH_MP2I_2021 | MP2I | 2021-2022 (ESRS2035779A) | 2026-2027 current-year bound | VERIFIED (search extract of the ESR BO page) |
| MATH_MPI_2021 | MPI | 2022-2023 (ESRS2111756A art. 2) | 2026-2027 current-year bound | VERIFIED (search extract) |
| PHYS_C4_2020 | 5e/4e/3e | 2020-2021 | 2026-2027 (Éduscol "Enseigner au cycle 4" table) | VERIFIED for 2026-27 only |



See also docs/EXPERTES_STATUS.md.

## Conflicts with the Codex kit (followed the verified source)
1. **MATH_TLE_SPE_2019 from_year.** The kit says 2019-2020. The BO spécial n°8 of 25 July 2019 (MENE1921246A, art. 2) says "entrent en vigueur à la rentrée scolaire 2020", so the registry uses **2020-2021**. Tle spé 2019-2020 therefore resolves to UNVERIFIED_EDITION.
2. **BO_C4_2020 source.** The kit cites https://www.education.gouv.fr/bo/20/Hebdo31/MENE2018714A.htm, which I could not fetch or check. The registry cites the Éduscol consolidated cycle 4 PDF, which I did fetch.
3. **MATH_1RE_SPE_2019 from_year 2019-2020.** I kept the kit's value but marked it UNVERIFIED, because the 2019 BO was not read.
4. **File format.** The kit's examples are block YAML and need PyYAML. The registries here are JSON-compatible YAML, because `python3 -I` has no PyYAML. The kit's selection_cases.yaml is read verbatim by a minimal reader (`tests/codex_cases.py`).
5. **Out of scope for v1.** These kit items are not implemented: the CLI (`py -3 -m quiz_eval ...`), the GitHub Actions CI, the errors.csv, sources.csv and id_migrations.csv per subject (error IDs are listed in skills.csv; migrations are read from v11), and resolved_manifest.yaml (the manifest is canonical JSON from `manifest_bytes`).
