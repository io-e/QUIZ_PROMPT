# Migration plan: v11 → subjects/mathematics/reference (after approval)

`Math_Diagnostic_Reference_CLAUDE_v11/` stays **untouched** in this PR. The `subjects/mathematics/reference/` CSVs are generated from it read-only (`tools/build_math_reference.py`). They are a derived view, not a replacement.

## Phases
1. **Now (this PR, draft).** The shared engine and registries are added, and the links are generated as proposals (approval=PENDING). The v11 checks must still pass: tests 21/21, build --check 8/8, STRUCTURE_PASS / HOLD.
2. **Teacher review.** Work through `docs/REVIEW_WORKLIST.csv` in priority order: the 18 QUARANTINE links (the 9 NEITHER Brevet skills) first, then the other Brevet links, then the other levels. Each decision is written to a link row (`approval`, `reviewer`, `approved_on`, `proposed_action`) by the teacher. The bot never writes those fields, and the v11 `Item_Review_Register_v11.csv` is not touched.
3. **Missing verifications.** Close the UNVERIFIED applicability dates in `editions.yaml` and the UNVERIFIED exam rules in `exams.yaml` (DNB rules per session).
4. **Freeze MATH_REF_v11.** Once 2–3 are done and the engine tests pass, copy (not move) the v11 files under `subjects/mathematics/reference/v11/` with their SHA256SUMS. Then write an immutable release manifest with `programme_diff.write_release_manifest`.
5. **Switch the readers.** The prompt binding (`subjects/mathematics/prompts/diagnostic.yaml`) and the build scripts point to the copy. The original folder is kept as an archive and is never rewritten.
6. **Next reference version (MATH_REF_v12).** It is added next to v11. Old student records keep their manifest (edition, reference version, exam session, software version), and nothing is re-labelled.

## Rollback
Every phase is a separate PR. Reverting one removes only derived files; v11 and the old editions are never modified.

## New BO published
Use `programme_diff.publish_new_edition(...)`. It runs these steps in order:
1. Register the edition (append-only; overlaps are refused).
2. Carry the links over as TO_REVIEW.
3. Write a worklist.
4. Run the regression tests.
5. Write an immutable release manifest with hashes.

Old approvals are preserved byte-for-byte.
