# BR-NC short diagnostic — verification (prompt v9 / reference v11)

Handoff repo `io-e/QUIZ_PROMPT`: **not reachable** (public API 404; GitHub connector: repo not granted to Cursor's GitHub App). Test rebuilt from the prompt v9 §O/§T checklist, the guide, and the BR-NC rows.

## Sympy recomputation (sympy 1.14.0, exact rationals, each signature on its own seed, R1)
| Row | Seed (mode) | Key | Distractors (code → sig_mcq → recomputed) | Result |
|---|---|---|---|---|
| BR-NC-01 | mcq: −3/4 + 1/2 | −1/4 ✓ | E1 −1/3 ✓ · E2 5/4 ✓ · E3 −5/4 ✓ | PASS |
| BR-NC-06 | mcq: −7 + 3 − (−5) | 1 ✓ | E1 −5 ✓ · E2 −9 ✓ · E3 9 ✓ | PASS |
| BR-NC-10 | mcq: 2/3 − 1/4 | 5/12 ✓ | E1 −1 ✓ · E2 1/12 ✓ · E3 1/6 ✓ | PASS |
| BR-NC-22 | mcq: 5 − 3(2x − 4) | 17 − 6x ✓ | E1 −7 − 6x ✓ · E2 1 − 6x ✓ · E3 4x − 8 ✓ | PASS |
| BR-NC-26 | mcq: 5x − 7 = 2x + 8 | x = 5 ✓ | E1 1/3 ✓ · E2 12 ✓ · E3 15/7 ✓ | PASS |
| BR-NC-04 | open: 9x² − 25 = 0 | (3x−5)(3x+5), {−5/3 ; 5/3} ✓ | E3 (open seed) "x = 5/3 only"; E4 recomputed on open numbers (3x−5)² | PASS |
| BR-NC-05 | open: 2x + 3 ≤ 11 | x ≤ 4, ]−∞ ; 4] ✓ | E1 x ≥ 4, E3 "x = 4" (open seed) | PASS |
Discrepancies: **none**. All distractors distinct from the key and from each other.

## Checklist (prompt v9 §T)
| Check | Result |
|---|---|
| R1: MCQ distractors only from that row's sig_mcq; open errors from sig_open or recomputed on open numbers | PASS |
| R2: MCQ only from MCQ+OPEN rows; 3 own signatures each; no LOCAL padding | PASS |
| R3: IDs exist, no -F##/-S##, no merged IDs, no micro-skill ID used as code | PASS |
| Anchors: all 7 rows SOURCE_LINKED (none PROVISIONAL), so no [ANCHOR TO VERIFY] needed; none marked validated | PASS |
| No HOLD/NOT_SUPPORTED row in catalogue status | **FLAG**: every row is HOLD in Item_Release_Eligibility (no PASS row exists), so the output is UNVALIDATED/HOLD by design |
| ≥ 1 FIND_ERROR item (DIAGNOSTIC) | PASS (Q6c) |
| Open items: staged parts, intermediate results, code per rubric criterion, re-test | PASS |
| Key positions ≤ 40 % per letter | PASS (B 40 %) |
| Time ≤ 0.9 × duration | PASS (25 min ≤ 27) |
| Student version: no key, rubric or code | PASS (checked in HTML: no -E codes, no keys) |
| Gap grid: no status from a single item; "indicatif" | PASS |
| Each target code planted ≥ 2 times (T5) | **FAIL** (short version: each code once) |
| T1 CoVe sources / T2 tool benchmark | **PARTIAL**: BO not consulted → [TO VERIFY]; T2 not done |
| French notation (virgule, ]a ; b]) | PASS (no decimals used) |
| Calculator rule (none) | PASS |
| YAML / player schema | N/A (Markdown only; schema unavailable) |

## Notes on the prompt itself
- The prompt's defaults (12/3 items, 55 min, T5 "each code ≥ 2 times", T1–T10 full) conflict with a "short" diagnostic; it has no explicit short mode.
- §T says "no HOLD row", but v11 has 0 PASS rows, so any compliant output is impossible unless HOLD is read as the catalogue `status` column; the prompt should say outputs are allowed as UNVALIDATED drafts.
- Open-item errors whose signature exists only as sig_mcq (e.g. BR-NC-04-E4) must be "recomputed on the open numbers"; the prompt allows this but the CSV has no sig_open for them, so the reviewer must accept the recomputation.
