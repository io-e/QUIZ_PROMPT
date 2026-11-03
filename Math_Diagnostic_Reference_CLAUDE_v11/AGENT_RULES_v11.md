# Agent rules — French math diagnostic reference (v10)

Paste this block into `AGENTS.md` or `CLAUDE.md` at the root of the work folder.

## Math diagnostic reference — rules for every agent (v9)

1. **R1 — one seed per signature.** Each row has an MCQ seed and an open seed. Compare a signature only with its own seed:
   - `mode = mcq`: compare `sig_mcq` with `mcq_seed` / `mcq_key`.
   - `mode = open`: compare `sig_open` with `open_seed` / `open_target`.
   - `mode = mcq+open`: compare each part with its own seed.

   Every finding records the `mode` and the seed used. Never report a cross-seed "mismatch".
2. **MCQ rule.** Generate an MCQ only from a row with `allowed_items = MCQ+OPEN` (three or more distinct MCQ-seed signatures). An `OPEN_ONLY` row gives open items only. Never add a `LOCAL` or unrelated code to reach four options.
3. **IDs.**
   - An ID keeps its meaning forever.
   - A retired or merged ID is never reused. `BR-AP-01-E3` is merged into `BR-AP-01-E1`; log E1.
   - The patterns `SUBDOMAIN-F\d\d` and `SUBDOMAIN-S\d\d` are reserved for the 301-target CODEX v5. Never use them, and never "restore" rows from them without that file.
4. **Anchors.** A row with `anchor_status = PROVISIONAL` (a `COPY` or `TOC` anchor) must be checked in the BO before an item built on it is marked `validated`. Record the check in `Anchor_Verification_Worklist_v11.csv`.
5. **Required form.** A `form_distinct` option has the key's value in another form. Compare it as written. The stem states the required form. Matrix products are compared as written.
6. **Evidence.** Every signature is a hypothesis, because there is no pilot data. A wrong MCQ option is `SUSPECTED` evidence; only `CONFIRMED` evidence supports a misconception.
7. **Validation.** After any edit, run `py -3 -I validate_reference_v11.py` from the package folder (Linux/macOS: `python3 -I`).
   - 0 blocking findings is a **structural pass, not a release**.
   - It does not prove:
     - pedagogical plausibility;
     - BO support of provisional anchors;
     - empirical validity;
     - player-schema compatibility.
8. **Findings format.** Use `Audit_Findings_Template_v8.csv`; the `mode` and `seed_used` columns are mandatory.
9. **(v9) Première common track.** No derivative item in `BAC_1RE_COMMUN`: `1C-FN-05`…`10` are `HOLD` (anchor `NOT_SUPPORTED`).
10. **(v9) Legacy IDs.** Raw logs keep historical IDs (CODEX v5 `-F##`/`-S##`, `EC-*`, `BR-AP-01-E3`); resolve them through `Math_ID_Migration_to_v11.csv`. CODEX v5 proposals are `PROPOSED_UNREVIEWED` until a reviewer sets them.
11. **(v9) Release gates.** `validated` only when STRUCTURE, CALCULATION, CURRICULUM, LEGACY_MIGRATION, PLAYER_SCHEMA (or NOT_APPLICABLE on paper) and TEACHER_REVIEW all pass for the items used.
12. **(v10) Item eligibility.** Use only `PASS` rows of `Item_Release_Eligibility_v11.csv` for a validated quiz; record every review in `Item_Review_Register_v11.csv`, then re-run the validator.
13. **(v10) Numbers.** Compare floating-point values with a stated tolerance, never with exact equality; keep exact symbolic values exact.
14. **(v11) Evidence.** A PASS needs complete, dated evidence (YYYY-MM-DD): BO page and passage; teacher reviewer and date; text-signature reviewer, date and note; pilot evidence ID and date. Run `py -3 -I tests_v11.py` after changing any rule.
15. **(v11) Determinism.** Never write runtime details (Python version, platform, time) into generated reference files; they go to the JSON report only.
