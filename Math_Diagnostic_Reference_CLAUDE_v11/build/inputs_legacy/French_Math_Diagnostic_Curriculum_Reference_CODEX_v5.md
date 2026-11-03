# French Mathematics Diagnostic Curriculum Reference — Error Tracking, Proofs and CPGE Bridge (CODEX v5)

**Version:** CODEX v5.0 · **Prepared:** 2026-10-19 · **Output format:** Markdown · **Reference language:** English

**Purpose:** Skills-based content specification for generating diagnostic **four-option, one-key MCQs**, **open questions**, corrections, misconceptions, and remediations using *PROMPT Diagnostic Maths Brevet Bac MPI_v3.md*. This file is a curriculum-to-item design reference, **not** a collection of ministerially approved exam questions.

**Coverage:** 8 level groups · **60 original subdomain codes** · **247 baseline atomic diagnostic targets**, plus **24 foundational calculation diagnostics**, **12 Brevet proof diagnostics**, **14 Terminale analysis extension targets** and **4 Terminale logic extension targets**. No original code is renamed or removed. The foundational layer is cross-level diagnostic support, not an additional official programme.

**Version lineage / limitation:** A file actually named `French_Math_Diagnostic_Curriculum_Reference_CODEX_v4.md` was not available with this request. This is a **v5 work product built from the most recent accessible expanded v3** and the two uploaded original source documents; it does **not** certify that every unpublished v4 change has been retained. If that v4 contains unique edits, compare/merge them before deployment.

**v5 change log:** persistent root-cause tracking; granular arithmetic pitfalls (signs, negative parentheses, order of operations, fractions, powers, algebraic equivalences); grade-3 proof writing and proof-error diagnosis; Terminale epsilon notation, elementary quantitative convergence, differentials and first-order approximation, all gated as enrichment where beyond official examinable content.

## 1. Reading this reference correctly

The original source is *French_Math_Curriculum_Reference_EN_CLAUDE_v2.docx* (19 October 2026). It supplies the original subdomain, content summary, expected learning outcome, exclusions and example. Every detailed assessment target and misconception in this Markdown is **new editorial elaboration**, not quoted official text. The official documents below supply program/version gating; a heading match **does not automatically certify each proposed question as examinable**.

### Evidence and approval labels

| Label | Meaning | Item-generation rule |
|---|---|---|
| `OFFICIAL-HEADINGS` | Official annex checked for programme structure and effective date; not full audit of each micro-skill | Validate the precise skill against the applicable annex before generating a summative item |
| `SOURCE-BASED` | Present in the supplied reference document, not necessarily officially verified | Drafting candidate only; confirm eligibility before using in a scored assessment |
| `PROVISIONAL` | Ambiguous/possibly out-of-scope subskill | Do not issue as a scored question until verified |
| `EXCLUDED` | Outside official or explicitly inherited source boundaries | Never generate as an ordinary on-programme item |
| `MISCONCEPTION-CANDIDATE` | A hypothesised wrong-answer mechanism, not a documented prevalence claim | Use to devise three separate distractors; confirm with subject review or actual learner responses |

### Stable identifiers

- Subdomain: original code, for example `M2-SF`.
- Diagnostic micro-skill: `<subdomain>-S01`, for example `M2-SF-S01`.
- Distinct misconception candidates: `<micro-skill>-E1` through `-E3`.
- Planned MCQ or open item: `Q-M2-SF-S01-01`, `O-M2-SF-S01-01`.
- Every item must name **one primary micro-skill**, its parent subdomain, programme edition and exam session (teacher version only).
- Numerical answers following `→` are **candidate correct targets**, not ready-to-print full question stems. For MCQs, generate three plausible, mutually different incorrect options based on E1/E2/E3; shuffle the position of the unique correct answer; recalculate all four options.
- The open-question probe includes the expected result after `→`. The teacher edition must additionally give **Data → Method → Steps → Result → Check**, explicit scoring steps, and equivalently valid methods.

### Test-design defaults (diagnostic, NOT exam-format claims)

| Difficulty | MCQ estimate | Open estimate | Model rubric for an open item |
|---|---:|---:|---|
| D1 automatic | 1 min | 4 min | 1 pt setup, 2 pts correct operation, 1 pt answer/check |
| D2 application | 2 min | 8 min | 1 pt conditions, 2 pts method, 3 pts steps, 1 pt result, 1 pt check |
| D3 reasoning | 3 min | 12 min | 2 pts hypotheses and structure, 5 pts reasoning, 3 pts execution, 1 pt conclusion, 1 pt validation |

The per-skill suggested difficulty below is an **authorial design choice**, not an official weighting. An item may change difficulty if its numbers, proof obligations or context change.

### MCQ safety checks

1. Fully solve the question before writing the distractors, then solve it independently again.
2. Construct a distractor from **each of E1, E2 and E3**. If two errors give the same wrong numerical value, change the numerical parameters or find an independent error mechanism; never knowingly include duplicate options.
3. Exactly four options (A–D), exactly one mathematically correct. Check domains, quantifier scope, rounding, endpoints, unit conversions and all edge cases.
4. For `Not/Except` stems, avoid ambiguity. Avoid clues such as disproportionate length of the right option.
5. Distinguish *wrong concept*, *algebraic slip*, and *unjustified inference* in teacher marking.
6. Preserve the calculator rule and the actual version of the exam. A diagnostic MCQ does not imply that the official exam uses MCQs.

### Open-response safety checks

1. Make the learner's reasoning visible: a proof, a justified computation, a model selection, a parameter condition, or an error diagnosis.
2. Use a criterion-referenced rubric with partial credit. Reward a valid method even if arithmetic contains a later isolated slip.
3. For every proof: verify hypotheses, quantifier order, target conclusion and any prohibited theorem.
4. For code-related tasks: distinguish predicting output, modifying an algorithm, and proving a property. Do not pretend that an implementation is required when only a reading task is in scope.
5. Record the misconception responsible for a failure, not merely the final numerical error.

## 1A. V5 — Longitudinal learner-error tracking and evidence model

### 1A.1 What constitutes evidence of an error?

**An incorrect final answer does not identify the cause.** A distractor choice is a **candidate hypothesis**; open-response steps, a brief follow-up probe or a student explanation are needed to verify it. Keep the observed action separate from the teacher's interpretation. In particular, do not infer dyscalculia, DYS status, attention, motivation or a health condition from a score or arithmetic error.

**Root cause versus propagated errors.** In `-3(2-5)`, a pupil might first compute `2-5=3`, then multiply `-3×3=-9`. The wrong inner subtraction is the **primary root error**; the product is procedurally correct given that erroneous intermediate value. Do not record two independent deficits. If the multiplication is also wrong, record a second error only when there is independent evidence (another step or transfer item).

| Field | Type / allowed values | Diagnostic purpose |
|---|---|---|
| `learner_id` | Pseudonymous identifier, not a full name | Longitudinal joins without unnecessary personal data |
| `attempt_id`, `item_id`, `timestamp` | Stable IDs; ISO date-time | Distinguish independent attempts and sessions |
| `level`, `school_year`, `programme_version` | Existing track code; applicable version | Separate prerequisite probes from the official assessed programme |
| `primary_skill`, `prerequisite_skill` | One assessable skill; optional root skill | Track a Terminale derivative question separately from a Brevet-level sign error |
| `format`, `calculator`, `adaptation` | `MCQ_4_ONE`, `OPEN`, `SHORT_RESPONSE`, `PROOF`, `ERROR_FIND`; calculator state; permitted accommodation | Interpretation context; accommodations must not automatically lower mastery |
| `response_raw`, `steps_observed` | Original student answer / ordered reasoning steps | Auditable evidence; never overwrite with a corrected solution |
| `step_index`, `expected_step`, `observed_step` | Localised divergence | First wrong transformation and whether later steps propagate it |
| `error_code` | Controlled v5 taxonomy, e.g. `EC-PAR-NEG` | Comparable tracking across chapters and sessions |
| `error_role` | `ROOT`, `PROPAGATED`, `INDEPENDENT`, `UNDETERMINED` | Prevent double counting |
| `evidence_level` | `OBSERVED`, `SUPPORTED`, `HYPOTHESIS`, `UNDETERMINED` | Do not overinterpret an MCQ distractor |
| `teacher_confirmed` / `confidence` | Boolean + optional 0–1 estimate | Human review and uncertain classifications |
| `rubric_dimension` | `KNOWLEDGE`, `METHOD`, `EXECUTION`, `JUSTIFICATION`, `NOTATION`, `CHECK` | Distinguish computation from reasoning |
| `points_earned`, `points_possible`, `assistance_used` | Numeric; independent / hint / correction | Preserve partial credit and context |
| `remediation_id`, `practice_item_ids`, `retest_item_ids` | Stable foreign keys | Tie a gap to an intervention and new evidence |
| `status_before`, `status_after`, `next_review_date` | `NOT_TESTED`, `INSUFFICIENT_EVIDENCE`, `NOT_ACQUIRED`, `FRAGILE`, `PARTIAL`, `ACQUIRED` | Progress without falsely marking untested skills as failures |

### 1A.2 Error taxonomy (cross-level tags; not official programme topics)

| Error code | Observable mechanism | Confirm with | Targeted remediation |
|---|---|---|---|
| `EC-SGN-ADD` | Integer addition/subtraction sign inversion | Pair positive/negative sums and number-line explanation | Sign-line comparison, five varied additions |
| `EC-SGN-MUL` | Product or quotient sign rule incorrect | Four signed multiplication/division cases | Sign table, verbalised parity of negative factors |
| `EC-SGN-UNARY` | Unary minus treated as a term separator or ignored | Compare `-x`, `(-x)`, `-(-x)` | Opposite-number transformation |
| `EC-PAR-NEG` | Minus before a bracket not distributed to all terms | Compare `-(a-b)` with `-a+b` | Opposite of a sum; literal and numeric transfer |
| `EC-PAR-DIS` | Distribution / double distribution loses a term or sign | Expand and verify by substitution | One arrow per product, then collect like terms |
| `EC-PAR-NEST` | Nested grouping order or closing bracket misread | Request numbered simplification stages | Innermost-first colour-free grouping |
| `EC-PRE-ORDER` | Addition before multiplication / improper precedence | Compare `3+2×5` with `(3+2)×5` | Operation tree and mixed exercises |
| `EC-PRE-POW` | Negative-base powers or precedence misinterpreted | Compare `-3²` with `(-3)²` | Explicit base identification |
| `EC-FRA-ADD` | Numerators and denominators added separately | Same-denominator and unequal-denominator tasks | Equivalent fractions then common denominator |
| `EC-FRA-DIV` | Incorrect fraction quotient / wrong reciprocal | `2/3 ÷ 4/5` and reverse-direction check | Reciprocal of divisor only |
| `EC-FRA-SIGN` | Sign inside/outside fraction mishandled | Compare `-a/b`, `a/-b`, `-a/-b` | Standard sign placement |
| `EC-FRA-CANCEL` | Illegal cancellation across addition | Ask why `(x+2)/x ≠ 2` for `x=1` | Cancel factors, never addends |
| `EC-POW-LAWS` | Power/product/quotient exponent rules mixed | `2³×2⁴` vs `(2³)⁴` | Power rule mapping with valid base assumptions |
| `EC-DEC-PLACE` | Decimal place, powers of ten or scientific exponent error | Multiply/divide by 10 and estimate magnitude | Estimation, unit and exponent checks |
| `EC-EQU-BAL` | Operation applied to only one equation side | Write each equivalent equation explicitly | Balance model and line-by-line equivalences |
| `EC-EQU-DIV0` | Division by expression potentially zero | Solve with parameter/domain restriction | Explicit nonzero-domain gate |
| `EC-ALG-ID` | `(a+b)² = a²+b²`, or square-difference identity confusion | Expand using distribution | Three-term square diagram and substitution |
| `EC-DOMAIN` | Square-root/logarithm/denominator domain ignored | Ask for domain before solution | Domain-first checklist |
| `EC-GEO-HYP` | Assumed fact comes only from drawing | Ask which statements were given | Data vs visible conjecture |
| `EC-GEO-THM` | Inappropriate theorem or missing hypotheses | Force theorem + hypothesis pairing | Given → theorem → conclusion cards |
| `EC-GEO-CONV` | Theorem/converse/contrapositive mixed | Parallelism vs ratio equality situations | Logical arrows and counterexamples |
| `EC-GEO-CONCL` | Correct calculation but conclusion unjustified or unstated | Request complete proof sentence | Proof closing sentence rubric |
| `EC-EPS-QUANT` | `∀ε∃N∀n` order reversed / N depends on n | Restate using words then symbols | Choose ε, construct N, handle all n≥N |
| `EC-EPS-STRICT` | `<` versus `≤` / threshold rounding | Show N for ε=0.1 with strict bound | Integer cutoff: floor and +1 |
| `EC-EPS-DELTA` | Choice of δ invalid or missing neighbourhood constraint | Check affine/quadratic examples | Bound variable factors then select δ |
| `EC-INF-ZERO` | Nonzero small real increment treated as exactly zero | Compare numerical Δ and limiting Δ/h | `h≠0` before limit; approximations marked `≈` |
| `EC-INF-REST` | Higher-order remainder omitted as exact identity | Expand `(a+h)²` | `Δf = f'(a)h + remainder`, distinguish equality/approximation |

### 1A.3 Mastery state machine (assessment vs remediation)

1. `NOT_TESTED` means no relevant observation; never convert it into failure.
2. `INSUFFICIENT_EVIDENCE` means a single guess-prone MCQ, an ambiguous student explanation or insufficient independent data. A wrong MCQ **cannot confirm** its mapped error code by itself.
3. For adequate evidence, retain the original prompt's score bands: `ACQUIRED` ≥80%, `PARTIAL` 50–79%, `FRAGILE` 30–49%, `NOT_ACQUIRED` <30%. These are **pedagogical decisions**, not official diagnoses. A stable specific error can warrant `PARTIAL` with a named target as the prompt requires.
4. For error **persistence**, require at least **two distinct item instances**, ideally across two sittings; otherwise `HYPOTHESIS`. Register `first_seen`, `last_seen`, `episodes`, and `distinct_sittings` per learner × root-error code.
5. For **remediation**, teach one root rule, assign two new practice variations (without giving the identical answer), then administer two independent transfer probes, preferably after a delay. A teacher may close an error as `RESOLVED` if both probes pass without assistance and explanation is coherent; record recurrence separately.
6. Never use simple percentage changes across substantially different tests as proof of improvement. Use `skill_id`, matched difficulty, independent attempt, and whether hints/calculators/accommodations were used.
7. One item can have one primary *programme skill* and one primary *root misconception*. If the student gets an advanced item wrong solely from `EC-SGN-MUL`, do not infer a missing advanced concept.

**Worked observation:** Terminale pupil computes `f'(x)= -2x` correctly but gets `f'(-3)=-6` instead of `6`. Primary programme skill `TS-AN-S03`; observed arithmetic mechanism `EC-SGN-MUL`; derivative-rule mastery remains supported, evaluation of a negative argument needs retest. Record the observed substitution as primary evidence, not a diagnostic label from the final number alone.

**Example append-only event (teacher/backend; no identifying details):**

```yaml
schema_version: diagnostic-error-v5
learner_id: anonymous-003
attempt_id: attempt-2026-10-19-01
item_id: Q-BR-NC-F03-01
primary_skill: BR-NC-F03
error_code: EC-SGN-MUL
observed_step: '(-4) * (-3) = -12'
expected_step: '(-4) * (-3) = 12'
error_role: ROOT
evidence_level: OBSERVED
teacher_confirmed: true
status_after: INSUFFICIENT_EVIDENCE  # one observed event, no retest yet
remediation_id: REM-EC-SGN-MUL-001
next_review_date: 2026-10-26
```

**Privacy principle:** store only what the diagnostic requires; retain actual scripts according to the school's documented retention and access policies. Do not store a medical diagnosis in an error-log field.

## 2. Session-sensitive official rules

| Topic | Applicable rule / transition | Consequence for this catalogue |
|---|---|---|
| DNB mathematics | Official 2026 definition: 2h, 20 min automatisms (6/20, no calculator), 1h40 reasoning (14/20; calculator permitted). Cycle-4 mathematics reform takes effect for 5e in 2026–2027, 4e in 2027–2028, 3e in 2028–2029. | Choose the grade-level programme applying to the candidate; do not automatically assume 2026 reform content is already examinable in 3e. |
| Première specialty | New 2026 programme applies from **2026–2027**. | For Première students in 2026–2027, use the 2026 annex, not the earlier curriculum by default. |
| Première common mathematics | New 2026 programme applies from **2026–2027**. Emphasises analysis of data, conditional probability, evolution via arithmetic/geometric sequences and quadratic/exponential models; no derivative chapter in this annex. | Do not test derivatives through `1C-FN`. Quadratic roots from factorised form; general discriminant procedure not in this common-track annex. |
| Première anticipated exam | **Session 2027:** 2025 exam note applies to candidates sitting in 2025–2026. **Session 2028, sat in 2026–2027:** Sept 2026 note replaces 2025 note; 2 h, 6 pt short-answer automatisms, 14 pt two/three independent exercises, no calculator, 2/20 marks dedicated to written-language mastery. | Keep diagnostic MCQ mode separate from an exam-faithful simulated paper. `{EXAM_SESSION}` must be interpreted together with actual year of sitting. |
| Terminale specialty | Replacement programme starts at the beginning of **2027–2028** school year; terminal written exam is 4h under Sept 2026 note. | Select the correct version by school year and avoid mixing the two. |
| MP2I | 2021 maths programme. | Probability year 1 on finite universes; `Z/nZ` rings are not year-1 requirements. Some source details remain pending granular review. |
| MPI | 2021 maths programme, CPGE 2nd year. | Full mathematics proofs and error diagnosis; respect source exclusions; no Hermitian product or measure-theory problems. |

### Direct official documents (effective-date checks as of 2026-10-19)

- 2026 cycle-4 changes: https://www.education.gouv.fr/bo/2026/Hebdo10/MENE2602912A
- 2026 Première specialty programme: https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602917A
- 2026 Première integrated common mathematics programme: https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602916A
- 2026 Terminale specialty programme (effective 2027–2028): https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602919A
- 2025 anticipated maths exam note: https://www.education.gouv.fr/bo/2025/Hebdo24/MENE2515469N
- 2026 replacement maths anticipated exam note: https://www.education.gouv.fr/bo/2026/Special4/MENE2622640N
- 2026 Terminale specialty exam note: https://www.education.gouv.fr/bo/2026/Hebdo4/MENE2622642N
- 2026 DNB maths definition: https://www.education.gouv.fr/bo/2025/Hebdo33/MENE2515977N
- 2021 MP2I official programme: https://www.education.gouv.fr/bo/21/Special1/ESRS2035779A.htm (full maths annex, first 36 pages: https://cache.media.education.gouv.fr/file/SPE1-MEN-MESRI-4-2-2021/64/8/spe779_annexe_1373648.pdf)
- 2021 MPI mathematics annex (as referenced by uploaded document): https://cache.media.education.gouv.fr/file/31/21/2/ensecsup756_annexes_1417212.pdf

## 3. Atomic subdomain-to-item specifications

For every row: the **MCQ probe** is a diagnostic stem seed with a target correct result, the **open probe** is a teacher-facing open-question seed with its expected evidence, and the `E1/E2/E3` column supplies three distinct candidate error diagnoses. Student-facing copies must omit answers, codes, rubrics, and traps.

## 3A. Cross-level foundation: basic calculations and error localisation

**Status:** `PEDAGOGICAL_DIAGNOSTIC` (Cycle 3/Cycle 4 prerequisites and numeracy fluency); not an extra national examination domain. Use these codes for **all levels** when an advanced answer may conceal a basic-calculation gap. Parent `BR-NC` is preserved for content provenance. For lycée/MPI, mark the item as a declared **cross-level prerequisite probe** rather than claiming it belongs to a Terminale/MPI chapter. New stable codes are `BR-NC-F01`–`BR-NC-F24`; they do **not** replace `BR-NC-S01`–`S05`.

**Item specification:** Each MCQ probe gives the **correct target**, but is not a full 4-option question. Generate *three different* distractors: (1) the named error-code mechanism, (2) a separate arithmetic misconception, (3) a transcription or execution misconception. Validate unique answers. For the OPEN probe, request all steps and annotate the **first non-equivalent line**, not just the last response. Do not classify a root misconception from one selected distractor.

| Skill ID | Atomic assessment target | MCQ seed → unique correct target | Open task → expected result or reasoning | Principal root-error tag | D |
|---|---|---|---|---|---|
| `BR-NC-F01` | Identify signs in addition | (-7)+(+3) → -4 | Explain on a number line why -7+3=-4 | `EC-SGN-ADD` | D1 |
| `BR-NC-F02` | Subtract a negative number | 5-(-8) → 13 | Rewrite -4-(-6) as addition and compute → 2 | `EC-SGN-ADD` | D1 |
| `BR-NC-F03` | Determine signs of products | (-4)×(-3) → 12 | Compute -2×(-3)×(-5) and justify parity → -30 | `EC-SGN-MUL` | D1 |
| `BR-NC-F04` | Determine signs of quotients | (-24)÷(+6) → -4 | Compute (-42)÷(-7) and justify sign → 6 | `EC-SGN-MUL` | D1 |
| `BR-NC-F05` | Use unary minus and double negation | -(-5) → 5 | Explain why -(x-2)=-x+2 for all x | `EC-SGN-UNARY` | D1 |
| `BR-NC-F06` | Remove a negative parenthesis | -(3x-4) → -3x+4 | Simplify 8-(2x-5) → 13-2x | `EC-PAR-NEG` | D2 |
| `BR-NC-F07` | Distribute a signed factor | -3(2x-5) → -6x+15 | Expand -2(3x+4) and verify for x=1 → -6x-8 | `EC-PAR-DIS` | D2 |
| `BR-NC-F08` | Multiply binomials without losing terms | (x+2)(x-3) → x²-x-6 | Expand (2x-1)(x+4) → 2x²+7x-4 | `EC-PAR-DIS` | D2 |
| `BR-NC-F09` | Simplify nested parentheses | 3-[2-(5-1)] → 5 | Compute 4-{2-[3-(-1)]} → 6 | `EC-PAR-NEST` | D2 |
| `BR-NC-F10` | Respect arithmetic priority | 3+2×5 → 13 | Compute 18÷3+2×4 with precedence → 14 | `EC-PRE-ORDER` | D1 |
| `BR-NC-F11` | Distinguish negative power bases | -3² → -9; (-3)² → 9 | Explain why -(2²) differs from (-2)² | `EC-PRE-POW` | D2 |
| `BR-NC-F12` | Combine unlike-denominator fractions | 1/2+1/3 → 5/6 | Show all steps for -3/4+1/2 → -1/4 | `EC-FRA-ADD` | D2 |
| `BR-NC-F13` | Divide fractions correctly | (2/3)÷(4/5) → 5/6 | Calculate (-3/5)÷(9/10) and simplify → -2/3 | `EC-FRA-DIV` | D2 |
| `BR-NC-F14` | Normalise fraction signs | (-3)/(-5) → 3/5 | Give three equivalent forms of -2/7, with correct denominator signs | `EC-FRA-SIGN` | D1 |
| `BR-NC-F15` | Cancel factors only, not addends | (2x+4)/(2x) → (x+2)/x, x≠0 | Explain by x=1 why (x+2)/x ≠2 in general | `EC-FRA-CANCEL` | D3 |
| `BR-NC-F16` | Use exponent laws | 2³×2⁴ → 2⁷=128 | Simplify a⁵/a² for a≠0 and explain → a³ | `EC-POW-LAWS` | D2 |
| `BR-NC-F17` | Handle powers of 10 and decimal places | 0.003 = 3×10^-3 | Order 2×10^-3 and 9×10^-4 by magnitude → first greater | `EC-DEC-PLACE` | D1 |
| `BR-NC-F18` | Balance both sides of equations | x-7=5 → x=12 | Solve 3(x-2)=12 line by line → x=6 | `EC-EQU-BAL` | D2 |
| `BR-NC-F19` | Track division restrictions | x/x=1 iff → x≠0 | Solve x(x-3)=0 without dividing by x → {0,3} | `EC-EQU-DIV0` | D3 |
| `BR-NC-F20` | Expand remarkable identities | (x+3)² → x²+6x+9 | Correct (a-b)²=a²-b² with full derivation | `EC-ALG-ID` | D2 |
| `BR-NC-F21` | Apply difference of squares correctly | 9x²-25 → (3x-5)(3x+5) | Factor x²-16 and verify by re-expansion | `EC-ALG-ID` | D2 |
| `BR-NC-F22` | Check denominators and admissible values | (x+1)/(x-2) defined iff → x≠2 | Solve (x²-1)/(x-1)=0 with domain → x=-1 only | `EC-DOMAIN` | D3 |
| `BR-NC-F23` | Distinguish equality from approximate equality | 1/3 = 0.333… exactly, 0.33 approximately | Compare 7/3 to 2.3 and explain rounding | `EC-DEC-PLACE` | D2 |
| `BR-NC-F24` | Separate root sign from arithmetic root | √25 → 5; x²=25 → x=±5 | Explain why √((-4)²)=4 not -4 | `EC-PRE-POW` | D2 |


### 3A.1 Two complementary probe types for every calculation skill

- **Isolated rule** (e.g., `(-4)(-3)`) distinguishes recall of the sign rule; **embedded rule** (e.g., `f'(-3)` after differentiating `f(x)=x²`) checks transfer under cognitive load. A pupil may pass the first and miss the second; record the difference rather than marking the underlying rule definitively mastered.
- **Wrong-solution repair**: show a student's first erroneous line; ask the pupil to circle it, name the violated rule, correct only that line and finish the computation. Evaluate error identification separately from numerical completion.
- **Ambiguity probe**: compare `-3²` vs `(-3)²`, `3+2×5` vs `(3+2)×5`, or `-(a-b)` vs `-a-b`. Request oral or written explanation to validate root cause.
- **Regression probes**: repeat sign, bracket and fractions checks after remediation at D1 and in a different chapter at D2; retain original error ID when it reappears.

### 3A.2 Worked example — isolate sign versus bracket error

**Student-facing MCQ candidate:** `-3(2-5)+(-4)^2 = ?` **Correct: 25.** The calculation is `2-5=-3`, `(-3)(-3)=9`, `(-4)^2=16`, total `25`.

**Open task:** Calculate the same expression without a calculator; on every line, say which rule was applied. The teacher should check: inner subtraction; multiplication of negatives; negative base in parentheses; addition. If several early stages are skipped, give a separate single-operation probe before assigning `EC-SGN-ADD` / `EC-SGN-MUL` / `EC-PRE-POW`.

**8-point diagnostic rubric:** expression read correctly 1; `2-5=-3` 2; `(-3)(-3)=9` 2; `(-4)^2=16` 2; final answer 25 with check 1. Award method points even when a single arithmetic slip propagates; annotate which step failed.

### 3A.3 Example of a learner-error trajectory

| Sitting | Independent evidence | Error classification | Action / status |
|---|---|---|---|
| Day 1 | `(-4)(-3)=-12` in open working | `EC-SGN-MUL`, `OBSERVED` | Provisional root-error candidate; avoid persistent-deficit label |
| Day 1, different item | `(-2)(-5)=-10` | `EC-SGN-MUL`, second independent observation | Target confirmed for remediation; `FRAGILE` only if scoring evidence meets thresholds |
| Day 2 | Two graded new drills: one rule, one mixed expression | Practice evidence; hint-use logged | No automatic status upgrade |
| Day 9 | Two fresh tasks correct with explanations | Transfer pass without help | `RESOLVED` may be recorded by teacher; schedule later recurrence check |

---

## BREVET — Brevet — cycle 4 / DNB

**Version gate:** New cycle-4 program rolls out by grade: Year 5 (2026), Year 4 (2027), Year 3 (2028). Use the program applicable to the pupil and exam session.  
**Status:** `REVIEW EXAM-SESSION GRADE PROGRAM`.

### `BR-NC` — Numbers & calculation

- **Source content:** Signed decimals, fractions, powers (powers of 10, scientific notation), square roots, multiples/divisors, prime factorisation; literal calculation: expand, factorise (incl. a²−b²), 1st-degree equations and inequations, zero-product equations.
- **Expected learner outcome:** Calculate fluently with and without a calculator; choose a suitable form of a number; use literal calculation to prove a general property; set up and solve an equation from a problem.
- **Limit / exclusions:** No general 2nd-degree solving (only x² = a and zero-product); no algebraic rules on square roots required; no formal number sets.
- **Prerequisite codes / competencies (inferred crosswalk):** Cycle 3 arithmetic.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `BR-NC-S01` | Calculate with signed fractions and decimals | Compute -3/4 + 1/2 → -1/4 | Show a common-denominator method for -3/4 + 1/2 → -1/4; sign, denominator, simplification | `BR-NC-S01-E1` add denominators; `BR-NC-S01-E2` discard negative sign; `BR-NC-S01-E3` add absolute values | D1 |
| `BR-NC-S02` | Use powers, scientific notation and roots | Convert 0.00042 to scientific notation → 4.2×10^-4 | Compare 4.2×10^-4 and 3.8×10^-3; justify using powers of ten | `BR-NC-S02-E1` wrong exponent sign; `BR-NC-S02-E2` coefficient outside [1,10); `BR-NC-S02-E3` confuse order of magnitude | D2 |
| `BR-NC-S03` | Identify divisibility, factors and prime decomposition | Factor 84 into primes → 2²×3×7 | Find GCD(84,36) using prime factors; explain the shared factors → 12 | `BR-NC-S03-E1` take LCM instead of GCD; `BR-NC-S03-E2` omit repeated factor; `BR-NC-S03-E3` treat 1 as prime | D2 |
| `BR-NC-S04` | Expand and factor elementary expressions | Factor 9x²−25 → (3x−5)(3x+5) | Solve 9x²−25=0 using factorisation; explain zero-product rule → ±5/3 | `BR-NC-S04-E1` forget square of 3; `BR-NC-S04-E2` replace difference by sum; `BR-NC-S04-E3` solve only one factor | D2 |
| `BR-NC-S05` | Solve first-degree equations, inequalities and zero products | Solve 3(2x−1)=9 → x=2 | Formulate and solve 2x+3≤11; give solution set → x≤4 | `BR-NC-S05-E1` reverse inequality without sign change; `BR-NC-S05-E2` distribute incorrectly; `BR-NC-S05-E3` confuse equation and inequation | D3 |

> **Original source example (retained for provenance):** « Factoriser 9x² − 25. » → (3x − 5)(3x + 5)

### `BR-DF` — Data, statistics, probability & functions

- **Source content:** Mean, median, range; frequency and equiprobable probability; proportionality, percentages; functions: image, antecedent, f(x) notation, linear and affine functions, graph/table reading.
- **Expected learner outcome:** Read and interpret tables and graphs; compute a probability in a simple random experiment; model a situation with a linear or affine function.
- **Limit / exclusions:** No conditional probability, no variance/standard deviation; formal study limited to linear and affine functions (others only through graphs or tables).
- **Prerequisite codes / competencies (inferred crosswalk):** BR-NC.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `BR-DF-S01` | Compute mean, median and range | Median of 2,3,3,8,9 → 3 | Compare mean and median of 1,2,2,3,12; comment on outlier → mean 4, median 2 | `BR-DF-S01-E1` use unsorted median; `BR-DF-S01-E2` divide sum by wrong count; `BR-DF-S01-E3` confuse median and mode | D1 |
| `BR-DF-S02` | Interpret a graph, frequency table and probability | P(red) for 3 red of 8 equally likely → 3/8 | Construct outcomes and compute P(not red) → 5/8; justify complement | `BR-DF-S02-E1` count all outcomes wrongly; `BR-DF-S02-E2` conflate probability and percentage; `BR-DF-S02-E3` assume equiprobability without grounds | D2 |
| `BR-DF-S03` | Work with proportionality and successive percentage changes | Increase 80 by 25% → 100 | Calculate final price after +10% then −10% on 100 → 99, net −1% | `BR-DF-S03-E1` add successive percentages; `BR-DF-S03-E2` treat 10% as 10 points universally; `BR-DF-S03-E3` use wrong reference base | D2 |
| `BR-DF-S04` | Evaluate images and antecedents of affine functions | For f(x)=3x−2 solve f(x)=7 → x=3 | Model taxi fare 4+2x; find x when fare=18 → 7 km | `BR-DF-S04-E1` interchange image/antecedent; `BR-DF-S04-E2` use reciprocal gradient; `BR-DF-S04-E3` omit constant term | D2 |
| `BR-DF-S05` | Connect a function formula, table and graph | Slope through (0,2),(3,8) → 2 | Find affine equation from two points; check on graph → f(x)=2x+2 | `BR-DF-S05-E1` read y-intercept as slope; `BR-DF-S05-E2` ignore axis scale; `BR-DF-S05-E3` mix x and f(x) | D3 |

> **Original source example (retained for provenance):** « f(x) = 3x − 2. Antécédent de 7 ? » → 3

### `BR-GM` — Quantities & measures

- **Source content:** Lengths, areas, volumes (prism, cylinder, pyramid, cone, sphere); unit conversions; compound quantities (speed, density, kWh); scale factors k, k², k³.
- **Expected learner outcome:** Compute and convert quantities; use area/volume formulas; reason on the effect of an enlargement or reduction.
- **Limit / exclusions:** No calculus-based measure; formulas outside the usual solids are given in the subject.
- **Prerequisite codes / competencies (inferred crosswalk):** BR-NC.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `BR-GM-S01` | Convert lengths, areas, volumes and compound units | 1.5 m² in cm² → 15000 cm² | Convert 0.25 m³ into litres → 250 L; show cube conversion | `BR-GM-S01-E1` apply linear factor to area; `BR-GM-S01-E2` confuse litre and cubic metre; `BR-GM-S01-E3` omit powers of ten | D1 |
| `BR-GM-S02` | Apply area and volume formulas for usual solids | Cylinder radius 2 height 3 volume → 12π | Calculate volume of a cone with r=3 h=4 → 12π; explain one-third | `BR-GM-S02-E1` forget 1/3; `BR-GM-S02-E2` use diameter as radius; `BR-GM-S02-E3` confuse area with volume | D2 |
| `BR-GM-S03` | Use enlargement scale factors | Volume factor for scale 2 → 8 | A solid scales by 3/2; determine new area/volume multipliers → 9/4,27/8 | `BR-GM-S03-E1` apply k to volume; `BR-GM-S03-E2` apply k² to length; `BR-GM-S03-E3` confuse enlargement with addition | D2 |
| `BR-GM-S04` | Model speed, density and energy units | At 60 km/h for 1.5h distance → 90 km | Estimate electricity cost for 2 kW over 3 h at €0.20/kWh → €1.20 | `BR-GM-S04-E1` multiply rate by wrong unit; `BR-GM-S04-E2` confuse kW with kWh; `BR-GM-S04-E3` skip currency rate | D3 |

> **Original source example (retained for provenance):** « Un agrandissement de rapport 2 multiplie le volume par ? » → 8

### `BR-EG` — Space & geometry

- **Source content:** Pythagoras and converse, Thales and converse, right-triangle trigonometry (cos, sin, tan); transformations (axial/central symmetry, translation, rotation, homothety); 3D sections; latitude/longitude.
- **Expected learner outcome:** Write a short deductive proof; compute lengths and angles; recognise and use a transformation.
- **Limit / exclusions:** Trigonometry only in the right triangle; no vectors, no coordinate equations of lines.
- **Prerequisite codes / competencies (inferred crosswalk):** BR-NC; BR-GM.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `BR-EG-S01` | Apply Pythagoras and its converse | Hypotenuse of legs 6,8 → 10 | Determine if sides 5,12,13 form right triangle; justify by squares | `BR-EG-S01-E1` add lengths instead of squares; `BR-EG-S01-E2` treat any longest side as hypotenuse without check; `BR-EG-S01-E3` omit converse | D1 |
| `BR-EG-S02` | Apply Thales and distinguish its converse | If parallel triangles scale by 2/3, segment 9 becomes → 6 | Determine unknown length with parallel lines using equal ratios and justify correspondences | `BR-EG-S02-E1` invert only one ratio; `BR-EG-S02-E2` assume parallelism without evidence; `BR-EG-S02-E3` mismatch corresponding segments | D2 |
| `BR-EG-S03` | Calculate right-triangle sine, cosine, tangent | Right triangle opposite=3 hypotenuse=5: sin θ → 3/5 | Given opposite=6 adjacent=8 compute tan θ and angle estimate; justify ratio → 3/4 | `BR-EG-S03-E1` use reciprocal trig ratio; `BR-EG-S03-E2` use non-right triangle; `BR-EG-S03-E3` swap opposite and adjacent | D2 |
| `BR-EG-S04` | Describe plane transformations and homotheties | A rotation by 180° about O equals → central symmetry | Construct image of a point by translation and homothety factor -2; explain orientation | `BR-EG-S04-E1` treat homothety as translation; `BR-EG-S04-E2` ignore negative ratio; `BR-EG-S04-E3` confuse centre and vector | D2 |
| `BR-EG-S05` | Interpret 3D sections and geographical coordinates | Plane parallel to base cuts cylinder in → circle | Explain why horizontal section of vertical prism retains base shape; sketch and label | `BR-EG-S05-E1` confuse net and section; `BR-EG-S05-E2` treat perspective lengths as true; `BR-EG-S05-E3` swap latitude and longitude | D3 |

> **Original source example (retained for provenance):** « Triangle rectangle de côtés de l'angle droit 6 et 8 : hypoténuse ? » → 10

**v5 extension — mandatory proof-writing probes (particularly for Part 2 diagnostic practice).** The standard is not merely a numeric response. A complete proof names **given hypotheses → applicable theorem/property → symbolic application → justified conclusion**. Do not infer equal lengths, right angles or parallel lines from appearance.

| Atomic skill | Demonstration outcome | MCQ / quick probe → correct target | Open proof / correction task | Root-error candidate | D |
|---|---|---|---|---|---|
| `BR-EG-S06` | Distinguish facts from diagram appearance | A sketch appears right angled with no mark: may one invoke Pythagoras? → No | Write the minimum hypotheses needed before Pythagoras direct theorem | `EC-GEO-HYP` | D1 |
| `BR-EG-S07` | Write a direct Pythagoras proof | Right triangle legs 6 and 8: hypotenuse → 10 | Given triangle ABC right-angled at A with AB=6, AC=8, prove BC=10; cite hypotheses, theorem, computation, conclusion | `EC-GEO-THM` | D2 |
| `BR-EG-S08` | Prove right angle by Pythagoras converse | Sides 5,12,13: right triangle? → Yes | Given AB=5, AC=12, BC=13, justify ABC is right at A; identify longest side and equality of squares | `EC-GEO-CONV` | D2 |
| `BR-EG-S09` | Disprove a right-angle conjecture using squares | Sides 4,5,6: right triangle? → No | For triangle sides 4,5,6, compare 4²+5² with 6² and conclude via contrapositive / inequality criterion | `EC-GEO-CONV` | D2 |
| `BR-EG-S10` | Apply Thales with all incidence hypotheses | D on AB,E on AC and DE∥BC, AB=10 AD=4 AC=15: AE → 6 | Write complete Thales proof: alignment / corresponding segments / parallelism / ratios / unknown length | `EC-GEO-THM` | D2 |
| `BR-EG-S11` | Use converse Thales for parallelism | D∈[AB],E∈[AC], AD/AB=AE/AC: DE∥BC? → Yes if same configuration | AB=10, AD=4, AC=15, AE=6: prove DE∥BC with position assumptions and converse | `EC-GEO-CONV` | D3 |
| `BR-EG-S12` | Prove parallelism from common perpendicular | Distinct lines d⊥ℓ and e⊥ℓ in plane: d∥e → True | Given distinct lines d and e each perpendicular to ℓ, state property and conclude d∥e | `EC-GEO-THM` | D2 |
| `BR-EG-S13` | Prove a midpoint or segment ratio | Midpoint M of [AB], AB=10: AM → 5 | In triangle ABC with D midpoint AB and E midpoint AC, justify DE∥BC and DE=BC/2 using midpoint theorem if applicable | `EC-GEO-HYP` | D3 |
| `BR-EG-S14` | Prove angle relation with parallel lines | Corresponding angles if lines parallel → equal | From d∥e and a transversal, write a short argument for equality of alternate-interior angles | `EC-GEO-THM` | D2 |
| `BR-EG-S15` | Give a deductive triangle angle proof | Triangle angles 50° and 60°: third → 70° | Explain why third angle is 70° using angle sum, with named hypotheses and conclusion | `EC-GEO-CONCL` | D1 |
| `BR-EG-S16` | Prove parallelogram using diagonal midpoints | If diagonals bisect each other, quadrilateral → parallelogram | Given quadrilateral ABCD diagonals AC and BD meet at O with AO=OC and BO=OD, prove ABCD parallelogram | `EC-GEO-CONV` | D3 |
| `BR-EG-S17` | Detect circular reasoning or misuse of converse | If lines are parallel ⇒ equal ratios; can equality be asserted without positions? → No | Correct this proof: "the picture shows parallel lines, so Thales; hence they are parallel"; give missing data and valid converse logic | `EC-GEO-HYP` | D3 |


**Brevet proof rubric (10 pts, reusable):**

| Proof component | Maximum | Observable marker | Candidate error |
|---|---:|---|---|
| Diagram data versus proved facts | 2 | Precisely names given incidences, right angle, position, parallels | `EC-GEO-HYP` |
| Choice of property and direction | 2 | Correctly distinguishes Pythagoras from converse; Thales from converse | `EC-GEO-THM`, `EC-GEO-CONV` |
| Formal mathematical chain | 3 | Appropriate equations/ratios, valid equivalences, correct correspondences | `EC-GEO-THM` plus any underlying calculation code |
| Numerical execution | 2 | Arithmetic correct; unit consistent where relevant | `EC-SGN-MUL`, `EC-FRA-ADD`, etc. when actually observed |
| Final justified sentence | 1 | Concludes exactly what is proven, with appropriate geometric vocabulary | `EC-GEO-CONCL` |

**Fully worked model (Pythagoras converse):** In triangle ABC, `AB=5`, `AC=12`, `BC=13`. Since `AB²+AC²=25+144=169=BC²` and `BC` is the longest side, *by the converse of Pythagoras's theorem*, ABC is right-angled at A. The plain equality of squares is not, by itself, a complete written demonstration unless the converse and conclusion are named.

**Fully worked model (Thales converse):** A, D, B are aligned in that order, A, E, C are aligned in that order, `AB=10`, `AD=4`, `AC=15`, `AE=6`. `AD/AB=4/10=2/5` and `AE/AC=6/15=2/5`. With D and E on the respective segments/rays in the required configuration, **by the converse of Thales's theorem**, `(DE)∥(BC)`. If the positional hypotheses are missing, the proof is not complete.

**Proof-specific MCQ design:** ask which theorem is valid *given the written hypotheses*, identify the first invalid proof line, select the missing hypothesis, or distinguish a theorem from its converse. Three distractors should correspond separately to missing given, wrong theorem direction, and unjustified conclusion; a correct numerical value must not disguise an invalid proof.


### `BR-AP` — Algorithms & programming

- **Source content:** Block programming (Scratch): sequences, loops, conditions, variables, events; calculation programs.
- **Expected learner outcome:** Read, complete or correct a short program; predict its output.
- **Limit / exclusions:** Block language only; no Python required.
- **Prerequisite codes / competencies (inferred crosswalk):** BR-NC.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `BR-AP-S01` | Trace sequential block operations | Start n=-2; ×3 then +4 → -2 | Give algebraic formula for a block program with ×3, +4; test two values | `BR-AP-S01-E1` reverse operation order; `BR-AP-S01-E2` treat n as fixed; `BR-AP-S01-E3` apply addition before multiplication | D1 |
| `BR-AP-S02` | Execute conditionals and comparisons | If x>0 and x=0, which branch? → else | Trace a sign-based branching algorithm at x=-1,0,1; explain boundary case | `BR-AP-S02-E1` confuse strict and non-strict; `BR-AP-S02-E2` execute both branches; `BR-AP-S02-E3` ignore boundary equality | D2 |
| `BR-AP-S03` | Analyse loops and variable updates | Repeat increment x←x+2 three times from 1 → 7 | Trace a repeat-until program; tabulate states and stop condition | `BR-AP-S03-E1` off-by-one repetitions; `BR-AP-S03-E2` check condition at wrong point; `BR-AP-S03-E3` confuse assignment with equality | D2 |
| `BR-AP-S04` | Correct a short Scratch algorithm | Loop adding 1 to total 4 times from 0 → 4 | Identify incorrect variable initialization and fix block diagram with validation test | `BR-AP-S04-E1` reuse stale value; `BR-AP-S04-E2` reset accumulator inside loop; `BR-AP-S04-E3` misread variable scope | D3 |

> **Original source example (retained for provenance):** « Choisir n, ×3, +4. Résultat pour n = −2 ? » → −2

## BAC_1RE_SPE — Première — spécialité mathematics

**Version gate:** New Première speciality program applies from school year 2026–2027; short-answer automatisms exam rule from Bac session 2028.  
**Status:** `REVIEW 2026 REVISED ANNEX`.

### `1S-AU` — Automatisms

- **Source content:** Fractions, powers, percentages and evolutions (multiplier coefficient), literal calculation, graph reading, line equations, proportions.
- **Expected learner outcome:** Answer quickly and reliably without a calculator.
- **Limit / exclusions:** Limited to the yearly official automatisms list.
- **Prerequisite codes / competencies (inferred crosswalk):** BR-NC; BR-DF.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1S-AU-S01` | Calculate fractions, signs and powers without calculator | (3/4)×(8/9) → 2/3 | Simplify and explain 2^-3×2^5 → 4 | `1S-AU-S01-E1` add exponents when dividing incorrectly; `1S-AU-S01-E2` mistake negative exponent as negative value; `1S-AU-S01-E3` cross-multiply without division | D1 |
| `1S-AU-S02` | Handle evolution coefficients and reverse percentages | +20% then -20% overall → -4% | Find initial value when final 126 after +5% → 120 | `1S-AU-S02-E1` add instead of multiply coefficients; `1S-AU-S02-E2` divide by rate not coefficient; `1S-AU-S02-E3` use final as original base | D2 |
| `1S-AU-S03` | Manipulate routine algebra and proportionality | Factor 6x+9 → 3(2x+3) | Solve proportional situation with 3 objects for 12 euros and 5 objects → 20 | `1S-AU-S03-E1` misfactor coefficients; `1S-AU-S03-E2` confuse multiplication/division; `1S-AU-S03-E3` assume additive rather than multiplicative | D2 |
| `1S-AU-S04` | Read functions, graphs and straight-line equations | Slope of y=−2x+3 → −2 | Find antecedent of 1 under f(x)=−2x+3 → 1 | `1S-AU-S04-E1` read intercept as slope; `1S-AU-S04-E2` confuse antecedent with image; `1S-AU-S04-E3` lose negative sign | D3 |

> **Original source example (retained for provenance):** « +20 % puis −20 % : évolution globale ? » → −4 %

### `1S-AL` — Algebra

- **Source content:** 2nd degree: canonical form, discriminant, factorisation, sign. Sequences: explicit/recursive, arithmetic, geometric, sums 1+…+n and 1+q+…+qⁿ, monotonicity.
- **Expected learner outcome:** Solve, factorise and study the sign of a quadratic; model a situation with a sequence.
- **Limit / exclusions:** No formal limit of a sequence (intuitive approach only).
- **Prerequisite codes / competencies (inferred crosswalk):** 1S-AU.
- **Special gate:** OFFICIAL 2026: simple square completion expected; general canonical form symbolic derivation not required.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1S-AL-S01` | Solve quadratic equations with discriminant | Roots of x²−5x+6 → 2,3 | Solve 2x²−3x−2=0 showing discriminant and roots → 2,−1/2 | `1S-AL-S01-E1` forget 2a denominator; `1S-AL-S01-E2` confuse ± in formula; `1S-AL-S01-E3` assume real roots for negative discriminant | D1 |
| `1S-AL-S02` | Use factorised/canonical quadratic forms | Vertex of (x−2)²+3 → (2,3) | Rewrite x²−4x+1 in canonical form → (x−2)²−3 | `1S-AL-S02-E1` take vertex x=-2; `1S-AL-S02-E2` omit square correction; `1S-AL-S02-E3` equate canonical and factor form | D2 |
| `1S-AL-S03` | Study signs and inequalities for quadratics | Sign x²−1 on (−1,1) → negative | Solve x²−4>0 with sign chart → x<-2 or x>2 | `1S-AL-S03-E1` reverse sign outside roots; `1S-AL-S03-E2` forget endpoint strictness; `1S-AL-S03-E3` use interval intersection instead of union | D2 |
| `1S-AL-S04` | Compute explicit/recursive arithmetic/geometric sequences | u0=3, u(n+1)=u(n)+2; u3 → 9 | Find u_n and sum from u0 to u4 for u0=3,r=2 → u_n=3+2n, sum 35 | `1S-AL-S04-E1` shift index n by one; `1S-AL-S04-E2` mistake geometric for arithmetic; `1S-AL-S04-E3` confuse term and sum | D2 |
| `1S-AL-S05` | Model monotonicity and finite sums | 1+2+...+10 → 55 | Derive 1+q+...+q^n for q≠1 and check q=2,n=3 → 15 | `1S-AL-S05-E1` off-by-one exponent; `1S-AL-S05-E2` misuse denominator 1-q; `1S-AL-S05-E3` apply formula when q=1 without exception | D3 |

> **Original source example (retained for provenance):** « Résoudre x² − 5x + 6 = 0. » → {2 ; 3}

### `1S-AN` — Analysis

- **Source content:** Derivative as limit of the difference quotient, tangent line, derivative rules (product, quotient, x ↦ g(ax+b)), variations and extrema; exponential (y′ = y, y(0) = 1); unit circle, sine and cosine.
- **Expected learner outcome:** Compute derivatives; study variations; use properties of exp; solve simple trigonometric equations.
- **Limit / exclusions:** Limits not formalised; no logarithm (Terminale); no general composite derivative.
- **Prerequisite codes / competencies (inferred crosswalk):** 1S-AL; 1S-AU.
- **Special gate:** OFFICIAL 2026: derivative presented through intuitive variation limit, not a formal epsilon-delta limit definition.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1S-AN-S01` | Compute derivatives via sum/product/quotient rules | Derivative of x e^x → (x+1)e^x | Differentiate (x²+1)e^x; factor result → e^x(x²+2x+1) | `1S-AN-S01-E1` omit product term; `1S-AN-S01-E2` change exp derivative sign; `1S-AN-S01-E3` forget chain factor | D1 |
| `1S-AN-S02` | Interpret tangent slope and local derivative | For f(x)=x² at x=2 slope → 4 | Write tangent equation to x² at x=1 → y=2x−1 | `1S-AN-S02-E1` use f(a) as slope; `1S-AN-S02-E2` tangent through origin assumption; `1S-AN-S02-E3` swap coordinates | D2 |
| `1S-AN-S03` | Derive variation table and extrema | For f(x)=−x²+4x maximum x → 2 | Derive and study x²−4x+1 on R; locate min → at x=2 value -3 | `1S-AN-S03-E1` sign of derivative reversed; `1S-AN-S03-E2` critical point treated as max always; `1S-AN-S03-E3` forget end behaviour | D2 |
| `1S-AN-S04` | Use exponential law and simple equation | e^(x+1)/e^x → e | Solve e^(2x)=e^4 and justify injectivity → x=2 | `1S-AN-S04-E1` add exponents under quotient; `1S-AN-S04-E2` take logs when not required incorrectly; `1S-AN-S04-E3` forget coefficient 2 | D2 |
| `1S-AN-S05` | Read sine and cosine on unit circle | cos(π/3) → 1/2 | Solve cos x=0 on [0,2π] → π/2,3π/2 | `1S-AN-S05-E1` mix degrees and radians; `1S-AN-S05-E2` omit second solution; `1S-AN-S05-E3` interchange sine and cosine | D3 |

> **Original source example (retained for provenance):** « Dériver f(x) = x eˣ. » → (x + 1)eˣ

### `1S-GE` — Geometry

- **Source content:** Vectors, scalar product (projection, norms, coordinates, Al-Kashi); normal vector, Cartesian line equation, circle equation.
- **Expected learner outcome:** Use the scalar product for orthogonality, angles and lengths; find line and circle equations.
- **Limit / exclusions:** Plane geometry only (space in Terminale).
- **Prerequisite codes / competencies (inferred crosswalk):** BR-EG; 1S-AU.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1S-GE-S01` | Compute scalar product from coordinates | (2,-1)·(1,2) → 0 | Determine angle status of vectors (2,1),(1,-2); justify orthogonality | `1S-GE-S01-E1` multiply cross-coordinates; `1S-GE-S01-E2` confuse dot product with determinant; `1S-GE-S01-E3` infer perpendicularity from equal length | D1 |
| `1S-GE-S02` | Use scalar product for distances and cosines | For orthogonal vectors u,v, u·v → 0 | Find cos θ for u=(1,0),v=(1,1) → 1/√2 | `1S-GE-S02-E1` omit vector norms; `1S-GE-S02-E2` use sine; `1S-GE-S02-E3` confuse scalar product with length product | D2 |
| `1S-GE-S03` | Find line equations via normal vectors | Line normal (2,3) through (1,0) → 2x+3y−2=0 | Derive normal and Cartesian equation of line through given point and direction | `1S-GE-S03-E1` take direction as normal; `1S-GE-S03-E2` wrong constant sign; `1S-GE-S03-E3` treat all line equations y=mx+b | D2 |
| `1S-GE-S04` | Use circle equation in Cartesian coordinates | (x−1)²+(y+2)²=9 centre → (1,-2) | Find equation of circle centre (2,-1),radius 3 → (x−2)²+(y+1)²=9 | `1S-GE-S04-E1` change radius to radius² incorrectly; `1S-GE-S04-E2` sign of centre reversed; `1S-GE-S04-E3` confuse circle and disc | D3 |

> **Original source example (retained for provenance):** « u(2 ; −1), v(1 ; 2) : u·v ? » → 0, vecteurs orthogonaux

### `1S-PS` — Probability & statistics

- **Source content:** Conditional probability, trees, total probability formula, independence; discrete random variable, expectation, variance, standard deviation.
- **Expected learner outcome:** Model a situation with a tree; compute and interpret E(X).
- **Limit / exclusions:** Finite universes; no binomial law (Terminale).
- **Prerequisite codes / competencies (inferred crosswalk):** BR-DF.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1S-PS-S01` | Compute probabilities with weighted trees | P(A)=.4 and P(B\|A)=.5: P(A∩B) → .2 | Complete tree and compute P(B) from two branches by total probability | `1S-PS-S01-E1` confuse conditional with intersection; `1S-PS-S01-E2` add instead of multiply branch; `1S-PS-S01-E3` forget second branch | D1 |
| `1S-PS-S02` | Test independence and inverted conditioning | P(A∩B)=P(A)P(B) means → independence | Given prevalence 0.1,sensitivity 0.8,false positive rate 0.2 find P(A\|positive) → 4/13 | `1S-PS-S02-E1` reverse conditioning; `1S-PS-S02-E2` neglect base rate; `1S-PS-S02-E3` wrong denominator P(positive) | D2 |
| `1S-PS-S03` | Compute discrete random variable expectation | X=0 or 2 equally likely: E(X) → 1 | Build law and compute E for winnings −1 with p=.75 and +3 with p=.25 → 0 | `1S-PS-S03-E1` take most likely outcome as expectation; `1S-PS-S03-E2` sum without probability weights; `1S-PS-S03-E3` forget negative winnings | D2 |
| `1S-PS-S04` | Compute variance and standard deviation | X=−1,1 equiprobable: V(X) → 1 | Using same X, show E(X²)−E(X)² and σ(X) → 1 | `1S-PS-S04-E1` forget squared expectation; `1S-PS-S04-E2` report variance as σ; `1S-PS-S04-E3` use unweighted squared differences | D3 |

> **Original source example (retained for provenance):** « P(A) = 0,4 ; P_A(B) = 0,5. P(A ∩ B) ? » → 0,2

### `1S-AP` — Algorithms & programming

- **Source content:** Python: variables, functions, loops, conditions, lists; threshold algorithms, scanning/dichotomy.
- **Expected learner outcome:** Write or complete a short Python function.
- **Limit / exclusions:** No advanced data structures.
- **Prerequisite codes / competencies (inferred crosswalk):** BR-AP; 1S-AL.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1S-AP-S01` | Trace Python variables, loops and lists | After x=2; x=x+3, x → 5 | Trace for loop building squares of 0,1,2; show list → [0,1,4] | `1S-AP-S01-E1` confuse assignment with equality; `1S-AP-S01-E2` loop endpoint included; `1S-AP-S01-E3` overwrite list rather than append | D1 |
| `1S-AP-S02` | Write threshold loops | First n with 2^n>1000 → 10 | Write while-loop for 1.1^n>2; state invariant and stopping check | `1S-AP-S02-E1` wrong inequality boundary; `1S-AP-S02-E2` initialise n=1 incorrectly; `1S-AP-S02-E3` increment outside loop | D2 |
| `1S-AP-S03` | Implement numerical scanning/dichotomy | Bisect [1,2] for x²−2, first midpoint → 1.5 | Complete iteration table for two bisections and keep root bracket | `1S-AP-S03-E1` discard wrong interval; `1S-AP-S03-E2` test sign against wrong endpoint; `1S-AP-S03-E3` use midpoint as exact root | D2 |
| `1S-AP-S04` | Diagnose conditional or indexing bug | Python range(3) yields → 0,1,2 | Correct a list index error in short code and explain with boundary tests | `1S-AP-S04-E1` off-by-one list index; `1S-AP-S04-E2` confuse length with last index; `1S-AP-S04-E3` wrong branch indentation | D3 |

> **Original source example (retained for provenance):** « Compléter une boucle qui renvoie le 1er n tel que 2ⁿ > 1000. » → 10

### `1S-LO` — Set vocabulary & logic

- **Source content:** Set notation, implication, equivalence, quantifiers, negation, counterexample, contrapositive, proof by contradiction.
- **Expected learner outcome:** Negate a quantified statement; choose an appropriate proof method.
- **Limit / exclusions:** Logic is taught through the content, not as a separate chapter.
- **Prerequisite codes / competencies (inferred crosswalk):** BR-NC.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1S-LO-S01` | Recognise implication and converse | From x=2 follows x²=4; converse? → false | Give counterexample to x²=4 ⇒ x=2 → x=-2 | `1S-LO-S01-E1` treat converse automatically valid; `1S-LO-S01-E2` counterexample violates hypothesis; `1S-LO-S01-E3` confuse necessary and sufficient | D1 |
| `1S-LO-S02` | Negate universal and existential statements | Negation ∀x∈R,x²>0 → ∃x∈R,x²≤0 | Negate ∃x∈R,x>2 and justify → ∀x∈R,x≤2 | `1S-LO-S02-E1` keep same quantifier; `1S-LO-S02-E2` negate number not relation; `1S-LO-S02-E3` confuse ≤ with < | D2 |
| `1S-LO-S03` | Use contrapositive and contradiction | Contrapositive P⇒Q → ¬Q⇒¬P | Prove n² even ⇒ n even by contrapositive | `1S-LO-S03-E1` prove converse instead; `1S-LO-S03-E2` assume required conclusion; `1S-LO-S03-E3` omit integer parity argument | D2 |
| `1S-LO-S04` | Distinguish equality, equivalence and counterexample | x²=1 equivalent to → x=±1 | Analyse each step of solving square-root equation and reject extraneous roots | `1S-LO-S04-E1` drop domain restriction; `1S-LO-S04-E2` square and assume equivalence; `1S-LO-S04-E3` fail verification | D3 |

> **Original source example (retained for provenance):** « Négation de : ∀x ∈ ℝ, x² > 0. » → ∃x ∈ ℝ, x² ≤ 0

## BAC_1RE_COMMUN — Première — mathématiques spécifiques within enseignement scientifique

**Version gate:** New 2026–2027 common general-track mathematics program; mathematical derivative not listed; quadratic roots through factorized expression only; not general discriminant.  
**Status:** `SCREENED AGAINST 2026 THEMES — ITEM REVIEW REQUIRED`.

### `1C-AU` — Automatisms

- **Source content:** Simple fractions, powers of 10, decimal/fraction/percentage conversions, mental calculation, orders of magnitude, graph reading (image, antecedent, line equation).
- **Expected learner outcome:** Calculate and read graphs without a calculator; check consistency of a result.
- **Limit / exclusions:** Yearly official automatisms list. [TO VERIFY]
- **Prerequisite codes / competencies (inferred crosswalk):** BR-NC; BR-DF.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1C-AU-S01` | Convert fractions, decimals and percentages | 3/4 as percentage → 75% | Explain how 0.125 equals 1/8 and 12.5% | `1C-AU-S01-E1` move decimal one place; `1C-AU-S01-E2` confuse percent with fraction; `1C-AU-S01-E3` invert numerator and denominator | D1 |
| `1C-AU-S02` | Compute numerical order of magnitude | Approximate 49×201 → near 10000 | Estimate consumption 1.9×10³ over 5 units and check plausible magnitude | `1C-AU-S02-E1` wrong power of ten; `1C-AU-S02-E2` excessive false precision; `1C-AU-S02-E3` ignore units | D2 |
| `1C-AU-S03` | Read a graph or basic function value | If chart gives f(2)=5, image of 2 → 5 | Extract image and antecedent from supplied graph and distinguish them | `1C-AU-S03-E1` swap axes; `1C-AU-S03-E2` confuse image/antecedent; `1C-AU-S03-E3` ignore graph scale | D2 |
| `1C-AU-S04` | Use cumulative proportional changes | Price 80 with +25% → 100 | Compute final amount after a 10% rebate on 50 → 45 with multiplier | `1C-AU-S04-E1` subtract 10 instead of 10%; `1C-AU-S04-E2` confuse 0.1 and 10; `1C-AU-S04-E3` use incorrect starting base | D3 |

> **Original source example (retained for provenance):** « 3/4 en pourcentage ? » → 75 %

### `1C-FN` — Functions

- **Source content:** Functions as models: 2nd-degree polynomials, exponential; graphical and local view of the derivative to analyse variations.
- **Expected learner outcome:** Use a function to describe a phenomenon; interpret variations.
- **Limit / exclusions:** No formal limits; light formalism. [TO VERIFY]
- **Prerequisite codes / competencies (inferred crosswalk):** 1C-AU; BR-DF.
- **Special gate:** GATED derivative: official 2026 program does NOT list derivatives; only quadratic/affine/exponential modelling in the 2026 profile.
- **Explicit correction to the source:** Its reference-document derivative/local-variation wording must **not** be used as an examinable 2026 `BAC_1RE_COMMUN` skill. The four micro-skills below exclude differentiation.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1C-FN-S01` | Read and compare linear/affine evolution graphs | For f(x)=2x+1, f(3) → 7 | Model a 2€/unit fee plus 5€ fixed cost; identify slope/intercept → 2,5 | `1C-FN-S01-E1` forget fixed fee; `1C-FN-S01-E2` confuse slope with intercept; `1C-FN-S01-E3` reverse axes | D1 |
| `1C-FN-S02` | Interpret quadratic parabolas graphically | Parabola (x−2)²+1 vertex → (2,1) | From supplied parabola, locate axis and vertex and discuss minimum | `1C-FN-S02-E1` misread vertex sign; `1C-FN-S02-E2` assume all parabolas open upward; `1C-FN-S02-E3` confuse zeros and extrema | D2 |
| `1C-FN-S03` | Find roots/sign for factorised quadratics in model | Roots (x−1)(x−3) → 1,3 | Determine positive/negative intervals for (x−1)(x−3) from a sign chart | `1C-FN-S03-E1` try unsupported discriminant requirement; `1C-FN-S03-E2` reverse sign between roots; `1C-FN-S03-E3` overlook endpoints | D2 |
| `1C-FN-S04` | Interpret exponential-style positive-base growth [x≥0] | With f(x)=2^x, f(3) → 8 | Compare discrete doubling and graph of f(x)=2^x for x≥0 using model quantities | `1C-FN-S04-E1` linearise multiplication; `1C-FN-S04-E2` allow negative-base fractional powers; `1C-FN-S04-E3` confuse exponential and quadratic | D3 |

> **Original source example (retained for provenance):** « Lire sur le graphique l'intervalle où f est croissante. »

### `1C-SE` — Sequences / evolutions

- **Source content:** Discrete evolution models (e.g., radioactive decay, half-life) using tables and graphs.
- **Expected learner outcome:** Model an evolution step by step; estimate durations or remaining proportions.
- **Limit / exclusions:** No formal sequence theory required. [TO VERIFY]
- **Prerequisite codes / competencies (inferred crosswalk):** 1C-AU.
- **Special gate:** OFFICIAL 2026: arithmetic and geometric sequences in contexts; avoid a purely theoretical sequence exercise.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1C-SE-S01` | Identify discrete additive vs multiplicative changes | Sequence 4,7,10,13 → arithmetic step 3 | Choose model for fixed annual increase and write u(n)=u0+nr | `1C-SE-S01-E1` treat increase as multiplier; `1C-SE-S01-E2` confuse n and n+1; `1C-SE-S01-E3` use wrong initial term | D1 |
| `1C-SE-S02` | Compute terms of arithmetic sequences | u0=5, r=2; u4 → 13 | Given recurrence u(n+1)=u(n)+3, u0=7 compute 5th update → 22 | `1C-SE-S02-E1` apply n−1 formula with u0; `1C-SE-S02-E2` miscount changes; `1C-SE-S02-E3` subtract common difference | D2 |
| `1C-SE-S03` | Compute terms of geometric sequences | u0=100, ratio 1/2; u3 → 12.5 | Model radioactive half-life 5y; amount after 15y as fraction → 1/8 | `1C-SE-S03-E1` add rather than multiply ratios; `1C-SE-S03-E2` confuse half-life and elapsed periods; `1C-SE-S03-E3` neglect exponent | D2 |
| `1C-SE-S04` | Locate threshold using table or recursion | Growth by 20% each year from 100; after 2y → 144 | Find first n with 100×1.2^n≥150 by table → n=3 | `1C-SE-S04-E1` wrong comparison strictness; `1C-SE-S04-E2` miscount initial year; `1C-SE-S04-E3` solve using linear growth | D3 |

> **Original source example (retained for provenance):** « Une quantité diminue de moitié tous les 5 ans. Reste-t-il après 15 ans ? » → 1/8

### `1C-SD` — Statistics

- **Source content:** Two-variable data, scatter plots, linear and non-linear trends.
- **Expected learner outcome:** Read a scatter plot; criticise an extrapolation.
- **Limit / exclusions:** No least-squares formalism required. [TO VERIFY]
- **Prerequisite codes / competencies (inferred crosswalk):** BR-DF.
- **Special gate:** OFFICIAL 2026: analyse bivariée; no generic mandatory regression-coefficient calculus without official support.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1C-SD-S01` | Read a bivariate data table | If (hours,score) = (1,8),(2,10) association → increasing | Explain tendency seen in supplied scatter plot and note an outlier | `1C-SD-S01-E1` assume correlation implies causation; `1C-SD-S01-E2` swap variables; `1C-SD-S01-E3` ignore outlier | D1 |
| `1C-SD-S02` | Describe positive, negative and absent trend | Scatter falling left to right → negative association | Sketch plausible data with negative association and justify qualitative description | `1C-SD-S02-E1` confuse negative values with negative association; `1C-SD-S02-E2` assume perfect alignment; `1C-SD-S02-E3` mistake visual axis orientation | D2 |
| `1C-SD-S03` | Interpolate versus extrapolate responsibly | Prediction between observed x-values is → interpolation | Evaluate prediction far beyond observed range and list validity concerns | `1C-SD-S03-E1` extrapolation considered guaranteed; `1C-SD-S03-E2` overinterpret two points; `1C-SD-S03-E3` ignore context/units | D2 |
| `1C-SD-S04` | Assess information quality in statistics | Single outlier proves causal link? → no | Contrast two candidate interpretations of noisy bivariate plot using evidence | `1C-SD-S04-E1` select extreme observation alone; `1C-SD-S04-E2` imply causal mechanism from association; `1C-SD-S04-E3` treat mean as a point on all plots | D3 |

> **Original source example (retained for provenance):** « Le nuage suggère-t-il une tendance linéaire ? Justifier. »

### `1C-PR` — Probability

- **Source content:** Introductory conditional probability: two-way tables, trees (sensitivity, specificity).
- **Expected learner outcome:** Read a two-way table; compute a conditional probability.
- **Limit / exclusions:** No random variables formalism. [TO VERIFY]
- **Prerequisite codes / competencies (inferred crosswalk):** BR-DF; 1C-AU.
- **Special gate:** OFFICIAL 2026: conditional probabilities with two-way tables or trees; independent Bernoulli repetition up to n=4.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `1C-PR-S01` | Read a two-way table conditionally | Of 200 positive tests, 150 sick; P(sick\|positive) → 3/4 | Fill conditional denominator from a confusion matrix; compute both P(sick\|+) and P(+\|sick) | `1C-PR-S01-E1` reverse conditioning; `1C-PR-S01-E2` divide by total population; `1C-PR-S01-E3` ignore true negatives | D1 |
| `1C-PR-S02` | Multiply along weighted tree branches | P(A)=.4 and P(B\|A)=.5; intersection → .2 | Draw a two-stage tree, multiply branch and add disjoint paths | `1C-PR-S02-E1` add branch probabilities instead of multiply; `1C-PR-S02-E2` omit complement branch; `1C-PR-S02-E3` misuse non-independent assumption | D2 |
| `1C-PR-S03` | Use total probability and complement | If P(A∩B)=.1 and P(not A∩B)=.2, P(B) → .3 | Calculate P(B) by partition A/not A and show both contributions | `1C-PR-S03-E1` drop one tree arm; `1C-PR-S03-E2` complement wrong event; `1C-PR-S03-E3` confuse union/intersection | D2 |
| `1C-PR-S04` | Compare independence and repeated Bernoulli trials (n≤4) | Two independent p=.5 trials; P(two successes) → .25 | Enumerate outcomes for 3 repeated trials and P(exactly 2 successes) at p=.5 → 3/8 | `1C-PR-S04-E1` assume all success counts equiprobable; `1C-PR-S04-E2` omit binomial multiplicities; `1C-PR-S04-E3` confuse independence and disjointness | D3 |

> **Original source example (retained for provenance):** « Sur 200 tests positifs, 150 malades : P(malade | positif) ? » → 0,75

## BAC_TLE_SPE — Terminale — spécialité mathematics

**Version gate:** 2019-era program remains applicable for 2026–2027; replacement comes into force in school year 2027–2028.  
**Status:** `REVIEW 2027–2028 REVISED ANNEX`.

### `TS-AG` — Algebra & geometry

- **Source content:** Counting: k-tuples, arrangements, permutations, combinations, Pascal's relation. Space: vectors, lines and planes, orthogonality, distances, parametric representations, Cartesian plane equations.
- **Expected learner outcome:** Count with an appropriate model; prove orthogonality; find intersections in space.
- **Limit / exclusions:** No cross product; complex numbers belong to Maths expertes.
- **Prerequisite codes / competencies (inferred crosswalk):** 1S-GE; 1S-AL.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TS-AG-S01` | Count permutations, arrangements and combinations | Number of ordered triples distinct chosen from 5 → 60 | Explain selection of 3 committee members from 5 without order → C(5,3)=10 | `TS-AG-S01-E1` confuse arrangement with combination; `TS-AG-S01-E2` omit factorial division; `TS-AG-S01-E3` miscount replacement | D1 |
| `TS-AG-S02` | Use binomial coefficients and Pascal identity | C(5,2) → 10 | Prove C(n,k)+C(n,k+1)=C(n+1,k+1) combinatorially | `TS-AG-S02-E1` shift Pascal index; `TS-AG-S02-E2` count ordered choices; `TS-AG-S02-E3` assert identity without interpretation | D2 |
| `TS-AG-S03` | Represent vectors and lines in three-dimensional space | Line through (1,0,0) along (1,2,3) → (1+t,2t,3t) | Find intersection of parameterised line with plane z=3; check coordinates | `TS-AG-S03-E1` swap normal and direction; `TS-AG-S03-E2` forget parameter consistency; `TS-AG-S03-E3` solve only one coordinate | D2 |
| `TS-AG-S04` | Determine plane equation, orthogonality and distances | Plane normal (1,0,0) through (2,0,0) → x=2 | Find Cartesian plane equation from point and normal; verify a test point | `TS-AG-S04-E1` use point as normal; `TS-AG-S04-E2` wrong plane constant; `TS-AG-S04-E3` infer parallelism from intersecting lines | D3 |

> **Original source example (retained for provenance):** « Mots de 3 lettres distinctes avec 5 lettres ? » → 60

### `TS-AN` — Analysis

- **Source content:** Sequences (induction, limits, comparison, monotone convergence), limits of functions, composition, convexity, continuity and IVT, logarithm, sine/cosine, primitives, differential equations y′ = ay + b and y′ = ay + f, integrals (linearity, integration by parts).
- **Expected learner outcome:** Prove by induction; compute limits; study a function fully; compute an integral.
- **Limit / exclusions:** Integrals on a segment only (no improper integrals); **formal ε-manipulation is not required for standard Terminale examination items**. The v5 ε and infinitesimal sections are clearly marked as optional preparation for CPGE.
- **Prerequisite codes / competencies (inferred crosswalk):** 1S-AN; 1S-AL.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TS-AN-S01` | Prove sequence property by induction | u_n=n(n+1)/2; base at n=0 → 0 | Show Σ(k=1..n)k=n(n+1)/2 by induction with clear induction step | `TS-AN-S01-E1` omit base case; `TS-AN-S01-E2` apply hypothesis at n+1 directly; `TS-AN-S01-E3` algebraic step wrong | D1 |
| `TS-AN-S02` | Evaluate sequence and function limits | lim n→∞ (2n²+1)/(n²−3) → 2 | Compute limit of (3x²−x)/(x²+1) at +∞ with degree argument → 3 | `TS-AN-S02-E1` substitute infinity as number; `TS-AN-S02-E2` neglect leading degrees; `TS-AN-S02-E3` cancel unmatched terms | D2 |
| `TS-AN-S03` | Study derivative, continuity, convexity and logarithm | d/dx ln x → 1/x for x>0 | Study extrema of f(x)=x−ln x on x>0; show f'(x)=1−1/x, min at 1 | `TS-AN-S03-E1` ignore log domain; `TS-AN-S03-E2` sign-chart inversion; `TS-AN-S03-E3` stationary point assumed max | D2 |
| `TS-AN-S04` | Compute primitives and integration by parts | Integral_0^1 x e^x dx → 1 | Show IPP on ∫_0^1 x e^x dx; boundary evaluation → 1 | `TS-AN-S04-E1` IPP sign error; `TS-AN-S04-E2` omit endpoint terms; `TS-AN-S04-E3` confuse derivative and primitive | D2 |
| `TS-AN-S05` | Solve scalar linear differential equations | Solution y'=2y, y(0)=3 → 3e^(2x) | Solve y'+y=2, y(0)=0 → y=2−2e^(−x) | `TS-AN-S05-E1` particular solution ignored; `TS-AN-S05-E2` exponent coefficient sign wrong; `TS-AN-S05-E3` initial condition ignored | D3 |

> **Original source example (retained for provenance):** « ∫₀¹ x eˣ dx ? » → 1 (IPP)

**v5 extension: quantitative limits (ε), infinitesimal reasoning, first-order differential calculus.** The **official Terminale speciality scope** includes convergence/limits, derivative and tangent, and numerical approximation; the **2026 replacement programme applicable from 2027–2028** describes convergence by eventual membership in every open interval and generally teaches limits intuitively. It **does not make symbolic ε–N/ε–δ proofs, little-o expansions or formal differential notation standard examinable requirements**. Accordingly: `OFFICIAL-CONCEPT` = the underlying concept is included but this particular formal presentation may be enrichment; `CPGE-BRIDGE` and `PEDAGOGICAL-BRIDGE` = **optional preparation only**. Unless `{PURPOSE}` explicitly requests enrichment, omit these optional items from an official-exam simulation and distinguish them in the teacher score report.

| Atomic skill | Observable assessment target | MCQ seed → key | Open task → observable evidence | Scope gate | Root-error tag | D |
|---|---|---|---|---|---|---|
| `TS-AN-S06` | Explain convergence using neighbourhood intervals | For u_n→2, eventual membership of (2-ε,2+ε) for every ε>0 → True | Translate "every open interval containing 2 eventually contains all u_n" into words and discuss dependence of threshold | `OFFICIAL-CONCEPT / notation enrichment` | `EC-EPS-QUANT` | D2 |
| `TS-AN-S07` | Construct an N(ε) for 1/n→0 | For ε=0.1, n≥11 guarantees 1/n<ε → Yes | Given ε>0 choose N=floor(1/ε)+1 and show ∀n≥N, abs(1/n)<ε | `CPGE-BRIDGE / formal ε proof` | `EC-EPS-STRICT` | D3 |
| `TS-AN-S08` | Respect the order of ε and N quantifiers | Definition of sequence limit: ∀ε>0 ∃N ∀n≥N → Correct | Explain why ∃N ∀ε>0 ∀n≥N is much stronger and generally false for 1/n | `CPGE-BRIDGE / symbolic quantifiers` | `EC-EPS-QUANT` | D3 |
| `TS-AN-S09` | Give an ε–δ proof for an affine function | For f(x)=3x+1 at a=2, δ=ε/3 → works | Given ε>0, set δ=ε/3 and prove abs(x-2)<δ implies abs(f(x)-7)<ε | `CPGE-BRIDGE / ε–δ` | `EC-EPS-DELTA` | D3 |
| `TS-AN-S10` | Use a controlled ε–δ bound for a quadratic | For abs(x-2)<1, abs(x+2)<5 → True | For f(x)=x² at 2, choose δ=min(1,ε/5) and prove abs(x²-4)<ε | `CPGE-BRIDGE / ε–δ` | `EC-EPS-DELTA` | D3 |
| `TS-AN-S11` | Interpret small nonzero increments h | For h≠0, [(3+h)²-9]/h → 6+h | Compute the difference quotient and take limit as h→0; say where h≠0 matters | `ON-TRACK calculus bridge via increment` | `EC-INF-ZERO` | D2 |
| `TS-AN-S12` | Separate exact increment and first-order approximation | For f(x)=x², Δf at x=3: 6h+h² (exact) → True | Derive Δf=6h+h² and explain Δf≈6h for small h with a numerical check | `PEDAGOGICAL-BRIDGE / differential intuition` | `EC-INF-REST` | D2 |
| `TS-AN-S13` | Introduce differential notation as linearisation | For f(x)=x² at a=3, df=6 dx (first-order linear map) → True | Contrast exact Δf=6h+h² with df=6h; explain why they differ if h≠0 | `CPGE-BRIDGE / formal differential notation` | `EC-INF-REST` | D3 |
| `TS-AN-S14` | Distinguish ≈ and = for infinitesimal calculations | Is (1+h)²=1+2h for every nonzero h? → No | Find missing term h² and bound approximation error for abs(h)≤0.01 | `PEDAGOGICAL-BRIDGE / approximation` | `EC-INF-REST` | D2 |
| `TS-AN-S15` | Compare first- and second-order small terms | For 0<abs(h)<0.01, abs(h²)<0.01abs(h) → True | Show h²/h→0 as h→0, h≠0, and state why h² is negligible versus h | `CPGE-BRIDGE / order notation` | `EC-INF-ZERO` | D3 |
| `TS-AN-S16` | Write a first-order remainder o(h) | f(a+h)=f(a)+f'(a)h+o(h) if differentiable → True | Explain r(h)=o(h) means r(h)/h→0 (h≠0) and prove it for f(x)=x² | `CPGE-BRIDGE / little-o` | `EC-INF-REST` | D3 |
| `TS-AN-S17` | Differentiate composite expressions via increments | For g(x)=(2x+1)², g'(x)=4(2x+1) → True | At x=1, expand g(1+h)-g(1) and recover g'(1)=12 | `ON-TRACK chain-rule with optional first-order link` | `EC-PAR-DIS` | D2 |
| `TS-AN-S18` | Link threshold algorithms to convergence | If u_n=1/n, threshold u_n<0.02 first holds at n → 51 | Write a loop/search method for smallest n with 1/n<ε (ε>0); justify termination | `OFFICIAL-CONCEPT / quantitative extension` | `EC-EPS-STRICT` | D2 |
| `TS-AN-S19` | Interpret infinitesimal language without nonstandard-number assumptions | In real analysis a small nonzero h is still a real number → True | Explain why "h is infinitesimal, therefore h=0" is false; give role of h→0 limit | `CPGE-BRIDGE / foundations` | `EC-INF-ZERO` | D2 |


#### Formalism and accepted mathematical language

- **Sequence limit** (`CPGE-BRIDGE` formal expression): `∀ε>0 ∃N∈ℕ ∀n≥N: |u_n−ℓ|<ε`. In the official Terminale presentation, the equivalent statement is eventual inclusion in **every open interval containing** `ℓ`; do not require `∀` and `∃` symbolic forms in routine baccalaureate questions.
- **Function continuity at a** (`CPGE-BRIDGE`): `∀ε>0 ∃δ>0 ∀x∈D_f: |x−a|<δ ⇒ |f(x)−f(a)|<ε`. If testing the **limit on a punctured domain**, require `0<|x−a|<δ` instead and handle `f(a)` separately. Conditions and quantifier scope are part of assessment.
- **Small increments:** for `h≠0`, `Δf=f(a+h)−f(a)`; if differentiable, `Δf=f'(a)h+r(h)` where `r(h)/h→0` as `h→0`. Thus `Δf≈f'(a)h` for small `h`, **not necessarily equality**. The differential `df_a(h)=f'(a)h` is a linear approximation; notation `dy=f'(x)dx` is a bridge convention, not a new number system.
- **Orders:** `h²=o(h)` as `h→0` through nonzero real values. Do not state that `h²=0` for merely small `h` or cancel `h` at `h=0`.
- **Scope exclusions:** no formal non-standard-analysis hyperreals, no unproved series expansions, no general multivariable differential calculus, no proof obligation beyond the official Terminale programme unless explicitly in bridge mode.

#### Worked example — ε/N proof (`TS-AN-S07`, 10 pts, **bridge only**)

**Open question:** Let `u_n=1/n` for `n≥1`. Prove using ε that `u_n→0`.

1. Fix arbitrary `ε>0` (2 pts).
2. Choose `N=max(1,⌊1/ε⌋+1)` so that `N>1/ε` (3 pts).
3. For every `n≥N`, `0<|u_n−0|=1/n≤1/N<ε` (3 pts).
4. Conclude using the correct order `∀ε>0 ∃N ∀n≥N` (2 pts).

**Error patterns:** one fixed N for all ε (`EC-EPS-QUANT`), choosing `N=1/ε` without integer/strictness check (`EC-EPS-STRICT`), substituting n=∞ as a number (`EC-INF-ZERO`).

#### Worked example — infinitesimal increment (`TS-AN-S12/S13`, 8 pts, bridge)

**Open question:** For `f(x)=x²`, `a=3` and nonzero real `h`, compare `Δf` with the tangent approximation.

- Exact expansion (3 pts): `Δf=(3+h)²−9=6h+h²`.
- Difference quotient (2 pts): `Δf/h=6+h`, so `f'(3)=6` after taking a limit.
- Differential/linear approximation (2 pts): `df_3(h)=6h`, `Δf−df_3(h)=h²`; exact equality holds only if `h=0`, outside the initial nonzero quotient computation.
- Interpretation (1 pt): `Δf≈6h` for small `h`; relative to `h`, the neglected term `h²` is of smaller order.

**Diagnostic discrimination:** dropping `h²` as an **exact** identity is `EC-INF-REST`; treating `h=0` during division is `EC-INF-ZERO`; a mistake in `(3+h)²` is `EC-PAR-DIS` or `EC-ALG-ID`, **not** automatically an ε misconception.


### `TS-PR` — Probability

- **Source content:** Bernoulli scheme, binomial law; sums of random variables, linearity of expectation, variance of a sum of independent variables; Bienaymé-Tchebychev, concentration, weak law of large numbers.
- **Expected learner outcome:** Recognise a binomial law; compute E and V; use concentration inequalities.
- **Limit / exclusions:** No continuous (density) laws in spécialité.
- **Prerequisite codes / competencies (inferred crosswalk):** 1S-PS.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TS-PR-S01` | Identify Bernoulli and binomial distributions | X~B(10,.5), E(X) → 5 | Model 3 independent trials p=.2; calculate P(X=1) → 3(.2)(.8)² | `TS-PR-S01-E1` ignore independence; `TS-PR-S01-E2` omit binomial coefficient; `TS-PR-S01-E3` confuse success count with sequence | D1 |
| `TS-PR-S02` | Calculate mean, variance and standard deviation | Var B(10,.5) → 2.5 | Derive E and V of Bin(10,.3) → 3 and 2.1 | `TS-PR-S02-E1` use np²; `TS-PR-S02-E2` forget 1−p; `TS-PR-S02-E3` confuse V with σ | D2 |
| `TS-PR-S03` | Compute variance of independent sums | If independent X,Y with variances 2,3, V(X+Y) → 5 | Explain why covariance term vanishes under independence and calculate V(2X+Y) → 11 | `TS-PR-S03-E1` sum standard deviations; `TS-PR-S03-E2` ignore square of coefficient; `TS-PR-S03-E3` assume any variables independent | D2 |
| `TS-PR-S04` | Apply Markov/Chebyshev and LLN at stated scope | For V(X)=4, P(\|X−E X\|≥4) ≤ → 1/4 | Bound deviation of sample mean from mean for independent identically distributed variables using Chebyshev | `TS-PR-S04-E1` wrong inequality direction; `TS-PR-S04-E2` forget variance divided by n; `TS-PR-S04-E3` claim certainty from probabilistic bound | D3 |

> **Original source example (retained for provenance):** « X ~ B(10 ; 0,5) : E(X), V(X) ? » → 5 ; 2,5

### `TS-AP` — Algorithms & programming

- **Source content:** Python: lists, simulations, sequence thresholds, approximation algorithms (rectangles, dichotomy).
- **Expected learner outcome:** Write or interpret a short algorithm linked to the content.
- **Limit / exclusions:** No advanced complexity analysis.
- **Prerequisite codes / competencies (inferred crosswalk):** 1S-AP; TS-AN.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TS-AP-S01` | Trace and implement Python sequence simulation | For s=0; for k in range(3): s+=k; s → 3 | Write algorithm summing first n squares and explain loop invariant | `TS-AP-S01-E1` include wrong range endpoint; `TS-AP-S01-E2` reset accumulator; `TS-AP-S01-E3` confuse update and return | D1 |
| `TS-AP-S02` | Implement dichotomy on a continuous scalar function | First midpoint of [1,2] → 1.5 | Trace two bisection steps for f(x)=x²−2 with sign justifications | `TS-AP-S02-E1` retain endpoint with wrong sign; `TS-AP-S02-E2` stop too early; `TS-AP-S02-E3` assume midpoint exact root | D2 |
| `TS-AP-S03` | Use rectangle approximation of integrals | Left rectangles n=2 for f(x)=x on [0,1] → .25 | Compute left and right Riemann sums for f(x)=x, n=4 → 3/8 and 5/8 | `TS-AP-S03-E1` width h omitted; `TS-AP-S03-E2` use wrong sample points; `TS-AP-S03-E3` confuse sum with integral | D2 |
| `TS-AP-S04` | Read stochastic simulation output with caution | Empirical 52/100 heads gives frequency → 0.52 | Outline independent simulation and explain why frequency need not equal p exactly | `TS-AP-S04-E1` mistake observation for exact probability; `TS-AP-S04-E2` reseed each trial unintentionally; `TS-AP-S04-E3` ignore sample variability | D3 |

> **Original source example (retained for provenance):** « Que renvoie un algorithme de dichotomie sur x² − 2 sur [1 ; 2] ? » → une approximation de √2

### `TS-LO` — Set vocabulary & logic

- **Source content:** Induction, implication, quantifiers, contrapositive, contradiction.
- **Expected learner outcome:** Write a rigorous induction proof.
- **Limit / exclusions:** Taught through the content.
- **Prerequisite codes / competencies (inferred crosswalk):** 1S-LO.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TS-LO-S01` | Translate logical implication and quantifiers | Negate ∀x∈R f(x)>0 → ∃x f(x)≤0 | Formulate quantified definition of increasing function on an interval and negate it | `TS-LO-S01-E1` reverse quantifiers wrongly; `TS-LO-S01-E2` confuse ≥ and >; `TS-LO-S01-E3` leave variables unquantified | D1 |
| `TS-LO-S02` | Write complete induction proofs | To prove P(n) for n≥1 first show → P(1) | Prove 2^n≥n+1 for n≥0, with proper hereditary step | `TS-LO-S02-E1` assume P(n+1); `TS-LO-S02-E2` omit base; `TS-LO-S02-E3` prove inequality for one case only | D2 |
| `TS-LO-S03` | Use contradiction and contrapositive | Contrapositive of P⇒Q → ¬Q⇒¬P | Prove √2 irrational by contradiction with coprime integers | `TS-LO-S03-E1` assume desired conclusion; `TS-LO-S03-E2` misuse parity; `TS-LO-S03-E3` forget coprimality contradiction | D2 |
| `TS-LO-S04` | Differentiate necessity, sufficiency and equivalence | x=2 sufficient for x²=4 → yes | Show x²=4 is equivalent to x=2 or x=−2 and discuss single direction | `TS-LO-S04-E1` confuse converse; `TS-LO-S04-E2` lose alternate root; `TS-LO-S04-E3` mistake example for general proof | D3 |

> **Original source example (retained for provenance):** « Montrer par récurrence que 2ⁿ ≥ n + 1. »

**v5 bridge-only logic probes:** All four rows below formalise limit reasoning for CPGE preparation. They are **not compulsory Terminale symbolic-quantifier exam items**; the official 2026 Terminale annex explicitly says `∀` and `∃` are not required symbols.

| Atomic skill | Target | MCQ seed → correct target | Open task | Root-error tag | D |
|---|---|---|---|---|---|
| `TS-LO-S05` | Read sequence-limit quantifiers in ordinary French | ∀ε>0 ∃N ∀n≥N means for every tolerance eventual closeness → True | Rewrite quantifiers in ordinary French without swapping their scopes | `EC-EPS-QUANT` | D2 |
| `TS-LO-S06` | Negate a quantified convergence statement | Negation of ∀ε>0 ∃N ∀n≥N P(n,ε): ∃ε>0 ∀N ∃n≥N ¬P → True | Negate the ε/N convergence claim and explain witness tolerance | `EC-EPS-QUANT` | D3 |
| `TS-LO-S07` | Separate uniform N from depending on n | Can N depend on chosen ε? → Yes | Contrast allowed N(ε) with invalid N(ε,n) in sequence-limit proof | `EC-EPS-QUANT` | D3 |
| `TS-LO-S08` | Explain implication in an ε–δ proof | Given abs(x-a)<δ and δ=ε/3 for f(x)=3x+1, conclude abs(f(x)-f(a))<ε → Yes | Check logical direction and the domain assumptions step by step | `EC-EPS-DELTA` | D3 |


## BAC_TLE_EXPERTES — Terminale — option mathématiques expertes

**Version gate:** Optional curriculum, with Terminale spécialité as prerequisite. Check the applicable official option and assessment session.  
**Status:** `SOURCE-BASED — OFFICIAL ITEM CHECK REQUIRED`.

### `TE-CX` — Complex numbers

- **Source content:** Algebraic, trigonometric and exponential forms; conjugate, modulus, argument; Euler and Moivre formulas; nth roots of unity; polynomial equations with real coefficients; geometric applications.
- **Expected learner outcome:** Switch between forms; solve equations in ℂ; prove alignment/orthogonality with complex numbers.
- **Limit / exclusions:** No complex analysis; polynomial equations limited to real coefficients.
- **Prerequisite codes / competencies (inferred crosswalk):** 1S-AN; 1S-GE.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TE-CX-S01` | Convert complex numbers across forms | Modulus of 1+i → √2 | Write 1+i in trigonometric/exponential form → √2e^(iπ/4) | `TE-CX-S01-E1` argument quadrant error; `TE-CX-S01-E2` confuse modulus with modulus squared; `TE-CX-S01-E3` omit periodicity | D1 |
| `TE-CX-S02` | Apply conjugate, Euler and de Moivre | (cos θ+i sin θ)^2 → cos2θ+i sin2θ | Compute (1+i)^4 by exponential form → −4 | `TE-CX-S02-E1` square modulus wrongly; `TE-CX-S02-E2` multiply argument incorrectly; `TE-CX-S02-E3` mix power and angle | D2 |
| `TE-CX-S03` | Find roots of unity and polynomial roots | Solutions z³=1 → 1,e^(2πi/3),e^(4πi/3) | Solve z⁴=−1 with full set and modulus/arguments | `TE-CX-S03-E1` forget distinct roots; `TE-CX-S03-E2` use real-only solutions; `TE-CX-S03-E3` divide angle by wrong n | D2 |
| `TE-CX-S04` | Apply complex numbers to geometry | For affix z_B−z_A, its modulus is → AB | Show alignment of three distinct points via real ratio of complex differences | `TE-CX-S04-E1` take modulus for oriented angle; `TE-CX-S04-E2` ignore zero denominator; `TE-CX-S04-E3` confuse alignment and perpendicularity | D3 |

> **Original source example (retained for provenance):** « Module et argument de 1 + i ? » → √2 ; π/4

### `TE-AR` — Arithmetic

- **Source content:** Divisibility, Euclidean division, congruences, GCD, Bézout, Gauss, primes, Fermat's little theorem; applications (cryptography, check digits).
- **Expected learner outcome:** Solve congruences; use Bézout/Gauss in proofs.
- **Limit / exclusions:** No ℤ/nℤ ring structure.
- **Prerequisite codes / competencies (inferred crosswalk):** BR-NC; 1S-LO.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TE-AR-S01` | Execute Euclidean division and gcd | gcd(84,36) → 12 | Use Euclidean algorithm and back-substitution to express 12=84u+36v | `TE-AR-S01-E1` incorrect quotient; `TE-AR-S01-E2` stop before final nonzero remainder; `TE-AR-S01-E3` forget Bezout coefficients | D1 |
| `TE-AR-S02` | Solve linear congruences using gcd | Solve 3x≡1 (mod 7) → x≡5 | Find all x with 4x≡2 (mod 6) → x≡2 or 5 (mod 6) | `TE-AR-S02-E1` divide modulo non-invertible coefficient; `TE-AR-S02-E2` omit solutions; `TE-AR-S02-E3` confuse equality and congruence | D2 |
| `TE-AR-S03` | Use prime divisibility, Gauss and Fermat | 2^10 mod 11 → 1 | Prove that if prime p divides ab and not a then p divides b, and apply to numbers | `TE-AR-S03-E1` apply Fermat without coprimality; `TE-AR-S03-E2` misstate Gauss lemma; `TE-AR-S03-E3` assume primality of composite | D2 |
| `TE-AR-S04` | Interpret elementary modular coding/check digits | Last decimal digit of 7^4 → 1 | Design a mod 11 check digit for short identifier; verify error detection with example | `TE-AR-S04-E1` work in base 10 instead of congruence; `TE-AR-S04-E2` mishandle zero residue; `TE-AR-S04-E3` assume any checksum catches all errors | D3 |

> **Original source example (retained for provenance):** « 2¹⁰ mod 11 ? » → 1 (Fermat)

### `TE-GM` — Graphs & matrices

- **Source content:** Matrix operations, inverse (order 2–3); graphs, adjacency matrix, paths; Markov chains, stable state.
- **Expected learner outcome:** Use matrix powers to count paths or compute states.
- **Limit / exclusions:** No eigenvalue theory.
- **Prerequisite codes / competencies (inferred crosswalk):** 1S-AL; TS-PR.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TE-GM-S01` | Multiply simple matrices and find inverses | [[1,1],[0,1]] squared → [[1,2],[0,1]] | Compute inverse of [[1,1],[0,1]] and verify AB=I | `TE-GM-S01-E1` entry-wise multiplication; `TE-GM-S01-E2` invert entries separately; `TE-GM-S01-E3` wrong matrix order | D1 |
| `TE-GM-S02` | Build and interpret adjacency matrices | (A²)ij counts → length-2 walks from i to j | Construct graph of three vertices and find number of length-2 walks using A² | `TE-GM-S02-E1` swap vertices; `TE-GM-S02-E2` count edges instead of walks; `TE-GM-S02-E3` forget orientation | D2 |
| `TE-GM-S03` | Compute transition probabilities via matrices | For row-stochastic P, row sums → 1 | Compute distribution after two steps from row vector v0 and P; check nonnegativity and total 1 | `TE-GM-S03-E1` multiply on wrong side; `TE-GM-S03-E2` assume column-stochastic convention; `TE-GM-S03-E3` sum state entries incorrectly | D2 |
| `TE-GM-S04` | Find stationary distribution in a small Markov chain | Stationary row π satisfies → πP=π | Solve 2-state chain with P=[[.8,.2],[.3,.7]] → π=(.6,.4) | `TE-GM-S04-E1` solve Pπ=π for wrong convention; `TE-GM-S04-E2` forget normalization; `TE-GM-S04-E3` assume limiting state without conditions | D3 |

> **Original source example (retained for provenance):** « Nombre de chemins de longueur 2 de i à j ? » → coefficient (i, j) de A²

## BAC_TLE_COMPLEMENTAIRES — Terminale — option mathématiques complémentaires

**Version gate:** Applied track without concurrent Terminale maths speciality. Revised programme scheduled from school year 2027–2028: review before use then.  
**Status:** `REVIEW 2027–2028 REVISED ANNEX`.

### `TC-SE` — Sequences & evolution models

- **Source content:** Arithmetic and geometric sequences, limits, population and finance models (loans, amortisation).
- **Expected learner outcome:** Model a real evolution with a sequence; interpret its limit.
- **Limit / exclusions:** Applied approach; no formal proofs of convergence.
- **Prerequisite codes / competencies (inferred crosswalk):** 1C-SE.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TC-SE-S01` | Recognize arithmetic/geometric model in context | 1000 growing 3% annually after n → 1000×1.03^n | Compare 1000€ +30€/year versus +3%/year after 3 years | `TC-SE-S01-E1` mix fixed increase and percentage; `TC-SE-S01-E2` use n−1 incorrectly; `TC-SE-S01-E3` omit initial value | D1 |
| `TC-SE-S02` | Calculate and interpret a sequence limit | For u_n=10+1/n, limit → 10 | Interpret long-run capacity in model u_n=100−50(0.8)^n → 100 | `TC-SE-S02-E1` read first term as limit; `TC-SE-S02-E2` ignore absolute ratio; `TC-SE-S02-E3` treat asymptote as attained at finite n | D2 |
| `TC-SE-S03` | Model amortization or scheduled repayments | Balance after interest r and payment a obeys → u(n+1)=(1+r)u_n−a | Compute first two months of loan recurrence with given rates and payments | `TC-SE-S03-E1` subtract before interest; `TC-SE-S03-E2` change rate units; `TC-SE-S03-E3` confuse cash flow direction | D2 |
| `TC-SE-S04` | Compare a model with real constraints | Fixed annual growth may become unrealistic because → resources limited | Explain domain of validity and plausible stop condition of exponential population model | `TC-SE-S04-E1` extrapolate indefinitely; `TC-SE-S04-E2` ignore negative amounts; `TC-SE-S04-E3` treat parameters as universal constants | D3 |

> **Original source example (retained for provenance):** « Capital de 1 000 € à 3 %/an : valeur après n ans ? » → 1 000 × 1,03ⁿ

### `TC-FN` — Functions

- **Source content:** Derivatives, convexity, exponential and logarithm as models (marginal cost, thresholds).
- **Expected learner outcome:** Study variations and convexity in context.
- **Limit / exclusions:** Context-based; no theoretical analysis.
- **Prerequisite codes / competencies (inferred crosswalk):** 1C-FN; 1C-AU.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TC-FN-S01` | Compute derivatives in applied models | For C(q)=q²+5, marginal cost C'(q) → 2q | Determine when revenue R(q)=20q−q² increases and locate optimal q → 10 | `TC-FN-S01-E1` interpret derivative as total cost; `TC-FN-S01-E2` sign chart inverted; `TC-FN-S01-E3` ignore domain q≥0 | D1 |
| `TC-FN-S02` | Read convexity and economic significance | If C''(q)>0, marginal cost → increasing | Discuss convexity of C(q)=q²+2q+1 and its effect on marginal cost | `TC-FN-S02-E1` confuse convexity with increasing; `TC-FN-S02-E2` assume slope positive; `TC-FN-S02-E3` disregard units | D2 |
| `TC-FN-S03` | Use exponential/logarithmic model for thresholds | Solve e^x=4 → x=ln 4 | Estimate time for 200e^(−0.2t) to drop below 100 → t>5ln2 | `TC-FN-S03-E1` reverse inequality after negative division; `TC-FN-S03-E2` omit logarithm; `TC-FN-S03-E3` confuse decimal and percentage | D2 |
| `TC-FN-S04` | Evaluate model and constraints | For x≥0, f(x)=−x²+6x max at → x=3 | Find realistic optimum of quadratic benefit model under 0≤x≤5 | `TC-FN-S04-E1` optimise outside domain; `TC-FN-S04-E2` ignore meaning of x; `TC-FN-S04-E3` choose minimum instead of maximum | D3 |

> **Original source example (retained for provenance):** « Coût C(q). Interpréter C′(q). » → coût marginal

### `TC-IN` — Integration & area

- **Source content:** Integral as area, approximation methods, mean value; Lorenz curve and Gini coefficient.
- **Expected learner outcome:** Compute and interpret an area in context.
- **Limit / exclusions:** Segment integrals only.
- **Prerequisite codes / competencies (inferred crosswalk):** TC-FN.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TC-IN-S01` | Interpret integral as signed area / accumulation | ∫_0^2 x dx → 2 | Estimate cumulative cost from variable rate f(t)=2t over [0,3] → 9 units | `TC-IN-S01-E1` confuse integrand with derivative; `TC-IN-S01-E2` omit interval width; `TC-IN-S01-E3` interpret signed area as always positive | D1 |
| `TC-IN-S02` | Approximate integrals with rectangles/trapezoids | For f(x)=x, midpoint estimate on [0,2] with 1 rectangle → 2 | Compute left and right sums for f(x)=x² on [0,2] with n=2 → 1 and 5 | `TC-IN-S02-E1` omit width h; `TC-IN-S02-E2` use incorrect endpoints; `TC-IN-S02-E3` assume all estimates equal exact integral | D2 |
| `TC-IN-S03` | Find mean value of continuous function | Mean of f(x)=x on [0,2] → 1 | Derive mean value of f(x)=x² on [0,3] → 3 | `TC-IN-S03-E1` forget divide by b−a; `TC-IN-S03-E2` confuse mean with endpoint average; `TC-IN-S03-E3` use derivative instead of integral | D2 |
| `TC-IN-S04` | Use Lorenz curve and Gini coefficient in model | For Lorenz L(x)=x², Gini → 1/3 | Compute G=1−2∫_0^1L(x)dx for L(x)=x²; explain 0≤G≤1 | `TC-IN-S04-E1` use integral as G directly; `TC-IN-S04-E2` wrong normalisation factor; `TC-IN-S04-E3` confuse equality line and Lorenz curve | D3 |

> **Original source example (retained for provenance):** « Gini pour L(x) = x² ? » → 1/3

### `TC-PR` — Probability laws & sampling

- **Source content:** Repeated independent trials, binomial, geometric, uniform and exponential laws; sampling.
- **Expected learner outcome:** Choose a suitable law; estimate from a sample.
- **Limit / exclusions:** No formal measure theory.
- **Prerequisite codes / competencies (inferred crosswalk):** 1C-PR.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TC-PR-S01` | Identify binomial versus geometric trial models | X~B(3,.5), P(X=0) → 1/8 | Model number of attempts to first success with geometric law; compute P(X=3) when p=.2 → .8²×.2 | `TC-PR-S01-E1` misuse binomial count; `TC-PR-S01-E2` off-by-one first success; `TC-PR-S01-E3` assume non-independent trials | D1 |
| `TC-PR-S02` | Work with uniform or exponential continuous laws | For Exp(λ), P(X>t) → e^(−λt) | Compute conditional survival P(X>5\|X>2) for Exp(.5) → e^(−1.5) | `TC-PR-S02-E1` confuse tail and CDF; `TC-PR-S02-E2` omit density integral/domain; `TC-PR-S02-E3` misuse memorylessness | D2 |
| `TC-PR-S03` | Calculate expectation in a discrete context | X~B(4,.25), E(X) → 1 | Estimate expected defect count in batch of 200 at defect probability .02 → 4 | `TC-PR-S03-E1` multiply by 1−p; `TC-PR-S03-E2` mistake expected value as certainty; `TC-PR-S03-E3` confuse mean and variance | D2 |
| `TC-PR-S04` | Read a sampling interval with context | If sample proportion 0.4, sample count 100, successes → 40 | Discuss why sample estimate differs from population parameter and identify effect of sample size | `TC-PR-S04-E1` assume sample equals population; `TC-PR-S04-E2` generalise biased sample; `TC-PR-S04-E3` confuse sample size with effect size | D3 |

> **Original source example (retained for provenance):** « X ~ Exp(λ). P(X > t) ? » → e^(−λt)

### `TC-ST` — Two-variable statistics

- **Source content:** Linear fit, regression line, correlation vs causation.
- **Expected learner outcome:** Fit and interpret a model; distinguish correlation and causation.
- **Limit / exclusions:** Least squares used, not derived.
- **Prerequisite codes / competencies (inferred crosswalk):** 1C-SD.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TC-ST-S01` | Interpret scatterplot and fit quality | Positive correlation coefficient indicates → rising linear tendency | Discuss outlier effect on fitted trend with before/after sketches | `TC-ST-S01-E1` infer causality from correlation; `TC-ST-S01-E2` ignore influential point; `TC-ST-S01-E3` treat r as regression slope | D1 |
| `TC-ST-S02` | Find approximate least-squares prediction (given line) | Line y=2x+1 at x=3 → 7 | With fitted line y=1.5x+2, interpret slope and predict for x=4 → 8 | `TC-ST-S02-E1` interchange dependent and independent; `TC-ST-S02-E2` treat intercept as slope; `TC-ST-S02-E3` ignore units | D2 |
| `TC-ST-S03` | Distinguish interpolation and extrapolation | Prediction x inside sample range → interpolation | Assess model reliability when predicting ten years beyond observed data | `TC-ST-S03-E1` assume linear trend indefinitely; `TC-ST-S03-E2` no residual check; `TC-ST-S03-E3` ignore domain shift | D2 |
| `TC-ST-S04` | Analyse residual signs | Observed y=8 and predicted yhat=6 residual y−yhat → 2 | Calculate residuals for 3 points; explain positive/negative meaning | `TC-ST-S04-E1` compute yhat−y; `TC-ST-S04-E2` equate residual to correlation; `TC-ST-S04-E3` ignore non-linear pattern | D3 |

> **Original source example (retained for provenance):** « Corrélation forte ⇒ causalité ? » → Non

### `TC-BA` — Bayesian inference

- **Source content:** Bayes' formula, sensitivity, specificity, positive predictive value.
- **Expected learner outcome:** Invert a conditioning and interpret a screening test.
- **Limit / exclusions:** Two-event Bayes in context.
- **Prerequisite codes / competencies (inferred crosswalk):** 1C-PR.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `TC-BA-S01` | Reverse conditional probability using Bayes | P(disease)=.01, Se=Sp=.99, PPV → .5 | Compute P(disease\|positive) from test characteristics and explain denominator | `TC-BA-S01-E1` confuse sensitivity with PPV; `TC-BA-S01-E2` ignore false positives; `TC-BA-S01-E3` reverse events | D1 |
| `TC-BA-S02` | Represent prevalence with frequency counts | In 10000 people, 1% disease → 100 | Build a 10,000-person contingency table at 1% prevalence, 99% Se/Sp | `TC-BA-S02-E1` apply specificity to diseased; `TC-BA-S02-E2` mix relative/absolute counts; `TC-BA-S02-E3` discard rounding basis | D2 |
| `TC-BA-S03` | Assess sensitivity/specificity and false positives | Specificity=90%, false-positive rate → 10% | Explain tradeoff between false-positive rate and prevalence in PPV | `TC-BA-S03-E1` equate sensitivity with specificity; `TC-BA-S03-E2` treat PPV independent of prevalence; `TC-BA-S03-E3` wrong complement | D2 |
| `TC-BA-S04` | Communicate Bayesian result ethically and accurately | Low prevalence can make PPV lower than Se → true | Explain to patient why 99%-accurate test may yield PPV near 50% at 1% prevalence | `TC-BA-S04-E1` claim test is unreliable overall; `TC-BA-S04-E2` ignore base rates; `TC-BA-S04-E3` assert definitive diagnosis from screening | D3 |

> **Original source example (retained for provenance):** « Prévalence 1 %, sensibilité et spécificité 99 % : VPP ? » → 50 %

## MP2I — MP2I — CPGE year 1

**Version gate:** Use 2021 official MP2I programme; some source specifics require verification. Do not introduce quotient rings Z/nZ or countable-universe probability as year-1 items.  
**Status:** `2021 M1-F2 AND CORE CHAPTERS CONFIRMED; OTHER SOURCE DETAILS NEED VERIFICATION`.

### `M1-LO` — Reasoning & set vocabulary

- **Source content:** Logic, quantifiers, sets, maps (injection, surjection, bijection), relations (equivalence, order).
- **Expected learner outcome:** Write and negate quantified statements; structure a proof.
- **Limit / exclusions:** Formal logic and set theory beyond the basics are out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** TS-LO; 1S-LO.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-LO-S01` | Negate nested quantified statements correctly | Negate ∀x∈R ∃y∈R, y>x → ∃x ∀y, y≤x | Negate ε-N convergence statement including variable ranges and order | `M1-LO-S01-E1` preserve quantifiers; `M1-LO-S01-E2` negate only final inequality; `M1-LO-S01-E3` swap ∀ and ∃ order | D1 |
| `M1-LO-S02` | Analyse injectivity, surjectivity and bijectivity | x↦x² on R is injective? → no | Prove f:R→R,x↦2x+3 is bijective and find inverse → (y−3)/2 | `M1-LO-S02-E1` ignore codomain; `M1-LO-S02-E2` conflate injective/surjective; `M1-LO-S02-E3` assume monotone globally without check | D2 |
| `M1-LO-S03` | Use equivalence/order relations | Congruence mod 3 is → equivalence relation | Show a given relation is reflexive, symmetric, transitive, or give counterexample | `M1-LO-S03-E1` confuse symmetric and antisymmetric; `M1-LO-S03-E2` forget reflexivity; `M1-LO-S03-E3` generalise from examples | D2 |
| `M1-LO-S04` | Structure proof using implication or contradiction | To refute ∀x P(x) need → one counterexample | Prove a simple uniqueness claim by assuming two solutions and comparing them | `M1-LO-S04-E1` circular argument; `M1-LO-S04-E2` show only existence; `M1-LO-S04-E3` confuse example with proof | D3 |

> **Original source example (retained for provenance):** « Nier : ∀ε > 0, ∃N, ∀n ≥ N, |uₙ − ℓ| ≤ ε. »

### `M1-CA` — Algebraic calculation & trigonometry

- **Source content:** Sums and products, binomial formula, double sums, small linear systems, inequalities, trigonometric formulas.
- **Expected learner outcome:** Manipulate sums and indices fluently.
- **Limit / exclusions:** —
- **Prerequisite codes / competencies (inferred crosswalk):** TS-AG; 1S-AU.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-CA-S01` | Manipulate indexed sums and products | Σ(k=1..n)k → n(n+1)/2 | Reindex Σ(k=1..n)(k+1) and simplify → n(n+3)/2 | `M1-CA-S01-E1` index bounds unchanged after reindex; `M1-CA-S01-E2` confuse sum with product; `M1-CA-S01-E3` omit last term | D1 |
| `M1-CA-S02` | Apply binomial identity and combinatorial coefficients | Coefficient x² in (1+x)^4 → 6 | Prove Σ C(n,k)=2^n using binomial theorem | `M1-CA-S02-E1` misplace powers; `M1-CA-S02-E2` treat binomial coefficient as permutation; `M1-CA-S02-E3` forget endpoints | D2 |
| `M1-CA-S03` | Handle double sums and order of summation | Σ(i=1..2)Σ(j=1..3)1 → 6 | Evaluate Σ(i=1..n)Σ(j=1..i)1 → n(n+1)/2 | `M1-CA-S03-E1` assume rectangular domain; `M1-CA-S03-E2` reverse limits incorrectly; `M1-CA-S03-E3` collapse independent indices | D2 |
| `M1-CA-S04` | Prove inequalities and trig transformations | sin²x+cos²x → 1 | Derive cos(2x)=1−2sin²x and use in solving elementary trig equation | `M1-CA-S04-E1` confuse sin(x+y) with sin x+sin y; `M1-CA-S04-E2` ignore periodicity; `M1-CA-S04-E3` lose solution branches | D3 |

> **Original source example (retained for provenance):** « Σₖ₌₀ⁿ C(n,k) ? » → 2ⁿ

### `M1-CX` — Complex numbers

- **Source content:** Modulus, argument, complex exponential, nth roots, 2nd-degree equations in ℂ, geometry.
- **Expected learner outcome:** Compute roots and solve equations in ℂ.
- **Limit / exclusions:** Construction of ℂ is out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** TE-CX (recommended bridging).

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-CX-S01` | Determine modulus and argument with quadrants | Arg(−1+i) principal → 3π/4 | Write −1+i in exponential form and verify by components | `M1-CX-S01-E1` use arctan without quadrant; `M1-CX-S01-E2` take modulus squared; `M1-CX-S01-E3` omit 2π equivalence | D1 |
| `M1-CX-S02` | Calculate roots of unity and nth roots | Roots of z³=1 count → 3 | Solve z⁴=16 in C in exponential form, list four roots | `M1-CX-S02-E1` list real roots only; `M1-CX-S02-E2` wrong argument division; `M1-CX-S02-E3` count multiplicities incorrectly | D2 |
| `M1-CX-S03` | Solve quadratic equations over C | Roots of z²+1=0 → ±i | Solve z²−2z+2=0 → 1±i | `M1-CX-S03-E1` discard negative discriminant; `M1-CX-S03-E2` use real sqrt for complex roots; `M1-CX-S03-E3` sign error in formula | D2 |
| `M1-CX-S04` | Use complex affixes for plane geometry | z_B−z_A represents → displacement A→B | Show perpendicularity via (z_C−z_A)/(z_B−z_A) purely imaginary, with nonzero denominator | `M1-CX-S04-E1` mistake imaginary criterion for alignment; `M1-CX-S04-E2` forget division condition; `M1-CX-S04-E3` ignore orientation | D3 |

> **Original source example (retained for provenance):** « Racines 3ᵉ de l'unité ? » → 1, j, j²

### `M1-TA` — Calculus techniques

- **Source content:** Usual functions, derivation, primitives; linear differential equations of order 1 and 2 (constant coefficients).
- **Expected learner outcome:** Solve standard ODEs; compute primitives.
- **Limit / exclusions:** Proof of the order-2 existence result is out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** TS-AN.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-TA-S01` | Differentiate and integrate usual elementary functions | Primitive of 1/x for x>0 → ln x+C | Find primitive of 2x e^(x²) → e^(x²)+C | `M1-TA-S01-E1` forget additive constant; `M1-TA-S01-E2` omit chain derivative; `M1-TA-S01-E3` use absolute log domain incorrectly | D1 |
| `M1-TA-S02` | Solve first-order linear ODE | y'=2y,y(0)=1 → e^(2x) | Solve y'+2y=4 with y(0)=0 → y=2−2e^(−2x) | `M1-TA-S02-E1` homogeneous-only solution; `M1-TA-S02-E2` wrong characteristic exponent; `M1-TA-S02-E3` initial condition omitted | D2 |
| `M1-TA-S03` | Solve constant-coefficient second-order ODE | y''+y=0 → A cos x+B sin x | Solve y''−3y'+2y=0 with initial conditions y(0)=1,y'(0)=0 → 2e^x−e^(2x) | `M1-TA-S03-E1` wrong characteristic roots; `M1-TA-S03-E2` count one free constant; `M1-TA-S03-E3` mismatch derivative initial value | D2 |
| `M1-TA-S04` | Use elementary differentiation rules with parameters | d/dx e^(3x) → 3e^(3x) | Differentiate ln(2x+1) on x>−1/2 and state domain | `M1-TA-S04-E1` omit chain multiplier; `M1-TA-S04-E2` neglect logarithm domain; `M1-TA-S04-E3` confuse derivative with inverse | D3 |

> **Original source example (retained for provenance):** « Résoudre y″ + y = 0. » → y = A cos x + B sin x

### `M1-SU` — Real numbers & sequences

- **Source content:** Supremum property, sequences, limits (ε-N), subsequences, Bolzano-Weierstrass, adjacent and recursive sequences.
- **Expected learner outcome:** Prove convergence rigorously with quantifiers.
- **Limit / exclusions:** Constructions of ℝ are out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** TS-AN; TS-LO.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-SU-S01` | Use supremum/infimum correctly | sup(0,1) → 1, not attained | Prove sup{1−1/n:n≥1}=1 and explain no maximum | `M1-SU-S01-E1` confuse sup with max; `M1-SU-S01-E2` do not establish upper bound; `M1-SU-S01-E3` ignore sequence indexing | D1 |
| `M1-SU-S02` | Write rigorous ε-N limit proof | For u_n=1/n, limit → 0 | Prove ∀ε>0 ∃N ∀n≥N: \|1/n\|<ε and choose N>1/ε | `M1-SU-S02-E1` choose N depending on n; `M1-SU-S02-E2` wrong quantifier order; `M1-SU-S02-E3` infer convergence only numerically | D2 |
| `M1-SU-S03` | Analyse monotone bounded or adjacent sequences | Increasing and upper-bounded sequence → convergent | Show monotone convergence of recurrence u(n+1)=sqrt(2+u_n) for suitable initial u0 | `M1-SU-S03-E1` assert boundedness without proof; `M1-SU-S03-E2` confuse fixed point with convergence proof; `M1-SU-S03-E3` check only first few terms | D2 |
| `M1-SU-S04` | Use subsequences and Bolzano-Weierstrass | Every bounded real sequence has → convergent subsequence | Find two subsequences of (-1)^n and show whole sequence diverges | `M1-SU-S04-E1` mistake bounded implies convergent; `M1-SU-S04-E2` choose subsequences with same limit incorrectly; `M1-SU-S04-E3` ignore parity | D3 |

> **Original source example (retained for provenance):** « Montrer que uₙ = 1/n tend vers 0 (ε-N). »

### `M1-LC` — Limits, continuity, differentiability, convexity

- **Source content:** IVT, extreme value theorem, Rolle, mean value theorem, Cᵏ functions, convexity and Jensen.
- **Expected learner outcome:** Apply the big theorems with checked hypotheses.
- **Limit / exclusions:** —
- **Prerequisite codes / competencies (inferred crosswalk):** TS-AN; M1-LO.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-LC-S01` | Apply IVT with hypotheses | Continuous f on [a,b], opposite signs → root exists | Show x³+x−1 has a root in (0,1), then uniqueness by monotonicity | `M1-LC-S01-E1` apply IVT without continuity; `M1-LC-S01-E2` confuse existence with uniqueness; `M1-LC-S01-E3` omit endpoint signs | D1 |
| `M1-LC-S02` | Use Rolle or mean value theorem | If f(a)=f(b) and differentiable, ∃c with f'(c)=0 → Rolle | Prove \|sin b−sin a\|≤\|b−a\| using MVT on suitable interval | `M1-LC-S02-E1` forget differentiability interval; `M1-LC-S02-E2` use endpoint derivative; `M1-LC-S02-E3` inequality reversed | D2 |
| `M1-LC-S03` | Establish continuity, differentiability and convexity | Differentiable at a implies → continuous at a | Study convexity of x² and tangent supporting property via derivative | `M1-LC-S03-E1` assume converse; `M1-LC-S03-E2` confuse second derivative sign; `M1-LC-S03-E3` omit interval | D2 |
| `M1-LC-S04` | Use extreme value theorem on compact intervals | Continuous on [0,1] achieves max → yes | State hypotheses for Weierstrass and give counterexample on open interval | `M1-LC-S04-E1` replace closed interval by open; `M1-LC-S04-E2` assume mere boundedness implies attained; `M1-LC-S04-E3` ignore continuity | D3 |

> **Original source example (retained for provenance):** « f continue sur [a ; b] ⇒ f bornée et atteint ses bornes. »

### `M1-AA` — Asymptotic analysis

- **Source content:** o, O, ~; Taylor-Young, limited expansions; asymptotics of sequences; Stirling (admitted).
- **Expected learner outcome:** Compute expansions and equivalents.
- **Limit / exclusions:** Proof of Stirling not required.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-LC.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-AA-S01` | Identify o, O and asymptotic equivalence | sin x ~ x as x→0 → true | Prove ln(1+x)~x as x→0 by standard expansion | `M1-AA-S01-E1` conflate O and o; `M1-AA-S01-E2` change equivalence under subtraction; `M1-AA-S01-E3` forget limiting regime | D1 |
| `M1-AA-S02` | Calculate Taylor expansions | e^x to order 2 at 0 → 1+x+x²/2+o(x²) | Obtain order-3 expansion of sin x and estimate small-angle error | `M1-AA-S02-E1` omit remainder; `M1-AA-S02-E2` mistake factorial; `M1-AA-S02-E3` use wrong parity terms | D2 |
| `M1-AA-S03` | Apply equivalents to limits | (1−cos x)/x² → 1/2 as x→0 | Evaluate (e^x−1−x)/x² at 0 using order-2 expansion → 1/2 | `M1-AA-S03-E1` substitute leading equivalent after cancellation; `M1-AA-S03-E2` drop needed order; `M1-AA-S03-E3` confuse variable direction | D2 |
| `M1-AA-S04` | Use Stirling only as admitted approximation | n! ~ sqrt(2πn)(n/e)^n → yes | Compute asymptotic n!/(n^n) with stated admitted Stirling formula | `M1-AA-S04-E1` claim proof of Stirling required; `M1-AA-S04-E2` forget sqrt factor; `M1-AA-S04-E3` invert e^n | D3 |

> **Original source example (retained for provenance):** « DL₂(0) de eˣ. » → 1 + x + x²/2 + o(x²)

### `M1-AR` — Arithmetic in ℤ

- **Source content:** Divisibility, GCD, Bézout, primes, p-adic valuation, congruences.
- **Expected learner outcome:** Solve arithmetic problems with congruences.
- **Limit / exclusions:** ℤ/nℤ rings are OUT of program (2nd year).
- **Prerequisite codes / competencies (inferred crosswalk):** TE-AR (recommended bridging).

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-AR-S01` | Apply Euclid and Bézout in Z | gcd(84,36) → 12 | Derive Bézout combination of 84 and 36 via Euclid → 12=84−2·36 | `M1-AR-S01-E1` wrong quotient; `M1-AR-S01-E2` stop before last nonzero remainder; `M1-AR-S01-E3` confuse gcd/lcm | D1 |
| `M1-AR-S02` | Manipulate congruences without quotient-ring theory | 7² mod 5 → 4 | Prove if a≡b (mod m), then a²≡b² (mod m) | `M1-AR-S02-E1` treat congruence as equality; `M1-AR-S02-E2` divide by nonunit unconditionally; `M1-AR-S02-E3` change modulus inadvertently | D2 |
| `M1-AR-S03` | Study prime factors and valuations | v₂(40) → 3 | Find v₃(72) and v₂(72) → 2 and 3 | `M1-AR-S03-E1` count all factors instead of powers; `M1-AR-S03-E2` confuse valuations for different primes; `M1-AR-S03-E3` neglect factorization | D2 |
| `M1-AR-S04` | Solve Diophantine first-degree equation | 6x+9y=3 solvable? → yes | Find integer solution of 6x+9y=3 then describe all solutions | `M1-AR-S04-E1` ignore gcd divisibility; `M1-AR-S04-E2` give real solutions only; `M1-AR-S04-E3` omit family parameter | D3 |

> **Original source example (retained for provenance):** « PGCD(84, 36) ? » → 12

### `M1-ST` — Usual algebraic structures

- **Source content:** Groups, morphisms, rings, fields.
- **Expected learner outcome:** Check a structure; use morphisms.
- **Limit / exclusions:** Artificial laws to be avoided.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-LO; M1-AR.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-ST-S01` | Check group axioms and subgroup criterion | Kernel of group homomorphism is → subgroup | Prove set 2Z is subgroup of (Z,+) using closure/inverses | `M1-ST-S01-E1` forget identity; `M1-ST-S01-E2` confuse subgroup with subset; `M1-ST-S01-E3` assume commutativity mandatory | D1 |
| `M1-ST-S02` | Identify morphisms and kernels/images | For f:Z→Z/3Z, n↦class n, kernel → 3Z | Compute image and kernel for a given explicit group morphism and justify subgroup status | `M1-ST-S02-E1` confuse image/kernel; `M1-ST-S02-E2` mis-handle neutral element; `M1-ST-S02-E3` assume all maps morphisms | D2 |
| `M1-ST-S03` | Recognise elementary ring/field operations | Z is field? → no | Explain why Z is integral domain but not field using 2 not invertible | `M1-ST-S03-E1` confuse units with nonzero elements; `M1-ST-S03-E2` treat ring as field; `M1-ST-S03-E3` disregard associativity | D2 |
| `M1-ST-S04` | Use algebraic structure for proof | Intersection of two subgroups is → subgroup | Show intersection is a subgroup by subgroup criterion, with nonempty condition | `M1-ST-S04-E1` assume union always subgroup; `M1-ST-S04-E2` forget closure under inverses; `M1-ST-S04-E3` replace proof with examples | D3 |

> **Original source example (retained for provenance):** « Le noyau d'un morphisme de groupes est-il un sous-groupe ? » → Oui

### `M1-PO` — Polynomials & rational fractions

- **Source content:** K[X], division, roots and multiplicity, factorisation over ℂ and ℝ, Lagrange interpolation, partial fractions.
- **Expected learner outcome:** Factorise; decompose rational fractions.
- **Limit / exclusions:** Proof of d'Alembert-Gauss out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** 1S-AL; M1-CX.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-PO-S01` | Execute polynomial Euclidean division | Remainder P(X) mod (X−a) → P(a) | Divide X³−1 by X−1; obtain X²+X+1 and remainder 0 | `M1-PO-S01-E1` misalign coefficients; `M1-PO-S01-E2` ignore remainder degree; `M1-PO-S01-E3` confuse polynomial and numeric quotient | D1 |
| `M1-PO-S02` | Apply roots and multiplicity | If P(a)=P'(a)=0 then multiplicity ≥ → 2 | Determine multiplicity of 1 in (X−1)³(X+2)² → 3 | `M1-PO-S02-E1` count distinct roots instead of multiplicity; `M1-PO-S02-E2` assume repeated root always simple; `M1-PO-S02-E3` ignore derivative test | D2 |
| `M1-PO-S03` | Factor polynomials over R and C | X⁴−1 over R → (X−1)(X+1)(X²+1) | Factor X⁴+1 over C using roots e^{i(π/4+kπ/2)} | `M1-PO-S03-E1` assume irreducible over C; `M1-PO-S03-E2` omit complex-conjugate roots; `M1-PO-S03-E3` misread exponents | D2 |
| `M1-PO-S04` | Decompose rational functions into simple elements | (2X+3)/((X+1)(X+2)) coefficients → A=1,B=1? compute: A=1,B=1 gives (2X+3) yes | Find A,B in (2X+3)/((X+1)(X+2)) and verify → 1,1 | `M1-PO-S04-E1` combine fractions incorrectly; `M1-PO-S04-E2` overlook denominator poles; `M1-PO-S04-E3` equate coefficients with wrong signs | D3 |

> **Original source example (retained for provenance):** « Factoriser X⁴ − 1 dans ℝ[X]. » → (X−1)(X+1)(X²+1)

### `M1-AL` — Linear algebra & matrices

- **Source content:** Matrix calculus, systems, GL_n; vector spaces, bases, dimension, linear maps, rank theorem, hyperplanes, affine subspaces; matrices of linear maps, change of basis, similarity, trace.
- **Expected learner outcome:** Use the rank theorem; change bases.
- **Limit / exclusions:** Infinite-dimensional theory out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** TS-AG; M1-CA.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-AL-S01` | Find basis, dimension and linear independence | If rank f=2 in R³, dim ker f → 1 | Use rank-nullity theorem to compute kernel dimension and justify assumptions | `M1-AL-S01-E1` add rank and dimension of image; `M1-AL-S01-E2` confuse columns/rows; `M1-AL-S01-E3` assume injective due square matrix | D1 |
| `M1-AL-S02` | Solve linear systems and matrix products | For [[1,0],[0,2]], determinant → 2 | Solve 2×2 linear system by Gaussian elimination; verify solution | `M1-AL-S02-E1` row operation applied to one side only; `M1-AL-S02-E2` confuse product with entrywise; `M1-AL-S02-E3` ignore inconsistent rows | D2 |
| `M1-AL-S03` | Change bases and compute representing matrices | If vectors of basis B form columns of P, P maps B-coordinates → standard coordinates | Find transition matrix between two explicit R² bases; check by reconstructing vector | `M1-AL-S03-E1` invert P wrong way; `M1-AL-S03-E2` put basis vectors as rows; `M1-AL-S03-E3` ignore change-of-basis conjugation | D2 |
| `M1-AL-S04` | Interpret trace, similarity and invariant quantities | Similar matrices have same → trace and determinant | Prove tr(P⁻¹AP)=tr(A) using cyclic trace identity | `M1-AL-S04-E1` assume similar matrices equal; `M1-AL-S04-E2` commute arbitrary matrices; `M1-AL-S04-E3` mismatch sizes | D3 |

> **Original source example (retained for provenance):** « u ∈ L(ℝ³), rg u = 2 : dim Ker u ? » → 1

### `M1-DT` — Symmetric group & determinants

- **Source content:** Permutations, cycles, signature; alternating n-linear forms; determinants.
- **Expected learner outcome:** Compute determinants; use signature.
- **Limit / exclusions:** —
- **Prerequisite codes / competencies (inferred crosswalk):** M1-AL; M1-CA.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-DT-S01` | Compute signatures and cycle types of permutations | Signature of one transposition → −1 | Write (1 2 3) as transpositions and compute its sign → +1 | `M1-DT-S01-E1` confuse cycle length with sign; `M1-DT-S01-E2` ignore permutation composition order; `M1-DT-S01-E3` mistake parity | D1 |
| `M1-DT-S02` | Compute determinants by row operations | Swapping two rows changes determinant sign → yes | Evaluate determinant 3×3 using permitted row operations and track sign/scales | `M1-DT-S02-E1` row addition treated as scaling; `M1-DT-S02-E2` forget swap sign; `M1-DT-S02-E3` expand with wrong cofactor sign | D2 |
| `M1-DT-S03` | Use alternation and multilinearity | Determinant with two equal rows → 0 | Explain determinant vanishing for linearly dependent rows via alternating multilinearity | `M1-DT-S03-E1` treat determinant as product of diagonal always; `M1-DT-S03-E2` forget linearity in each row; `M1-DT-S03-E3` confuse row/column conventions | D2 |
| `M1-DT-S04` | Apply determinants to invertibility | det A≠0 implies → invertible | For parametric 2×2 matrix find parameter values for non-invertibility and justify | `M1-DT-S04-E1` assume det=0 means zero matrix; `M1-DT-S04-E2` arithmetic sign error; `M1-DT-S04-E3` confuse eigenvalue with determinant | D3 |

> **Original source example (retained for provenance):** « Signature d'une transposition ? » → −1

### `M1-IN` — Integration

- **Source content:** Integration on a segment, Riemann sums, fundamental theorem, Taylor with integral remainder.
- **Expected learner outcome:** Compute and bound integrals. [TO VERIFY details]
- **Limit / exclusions:** Construction method [TO VERIFY]; Laplace transform NOT in program.
- **Prerequisite codes / competencies (inferred crosswalk):** TS-AN; M1-LC.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-IN-S01` | Compute segment integrals and primitive relation | Integral_0^1 x dx → 1/2 | Bound ∫_0^1 x² dx between Riemann sums and compute exact value → 1/3 | `M1-IN-S01-E1` forget integration bounds; `M1-IN-S01-E2` wrong primitive constant; `M1-IN-S01-E3` neglect interval orientation | D1 |
| `M1-IN-S02` | Identify Riemann sums | (1/n)Σ(k=1..n) (k/n) as n→∞ → 1/2 | Convert an equidistant sum to ∫_0^1 f(x)dx with explicit mesh justification | `M1-IN-S02-E1` omit factor 1/n; `M1-IN-S02-E2` use k outside interval; `M1-IN-S02-E3` confuse right/left endpoints | D2 |
| `M1-IN-S03` | Use FTC and integral as function | d/dx ∫_0^x t²dt → x² | Differentiate F(x)=∫_1^x (1+t²)dt and find F(1) | `M1-IN-S03-E1` differentiate integrand with respect to wrong variable; `M1-IN-S03-E2` forget upper limit dependence; `M1-IN-S03-E3` ignore base condition | D2 |
| `M1-IN-S04` | Apply Taylor formula with integral remainder where specified | Taylor order 1 remainder includes integral of f'' → yes | Use integral remainder to bound error of exp approximation on [0,1] | `M1-IN-S04-E1` omit derivative order; `M1-IN-S04-E2` assume remainder zero; `M1-IN-S04-E3` bound with wrong interval maximum | D3 |

> **Original source example (retained for provenance):** « lim (1/n) Σ f(k/n) ? » → ∫₀¹ f

### `M1-PR` — Counting & probability

- **Source content:** Counting; probability on FINITE universes, random variables, laws, expectation, variance.
- **Expected learner outcome:** Model and compute on finite universes.
- **Limit / exclusions:** Countable universes are 2nd year.
- **Prerequisite codes / competencies (inferred crosswalk):** TS-PR; M1-CA.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-PR-S01` | Count finite outcomes with combinations | Number 2-card hands from 5 distinct cards → 10 | Compare ordered and unordered selection of k objects and justify factorial division | `M1-PR-S01-E1` confuse replacement and no replacement; `M1-PR-S01-E2` conflate permutation and combination; `M1-PR-S01-E3` count impossible draws | D1 |
| `M1-PR-S02` | Calculate event probabilities in finite spaces | Two fair dice sum 7 probability → 6/36 | Enumerate suitable events on finite equiprobable universe and justify each outcome count | `M1-PR-S02-E1` treat sums equiprobable; `M1-PR-S02-E2` use denominator 11 instead of 36; `M1-PR-S02-E3` forget order of dice | D2 |
| `M1-PR-S03` | Calculate conditional probabilities on finite universe | Two successive draws without replacement; P(second red\|first red) from 3 red 2 blue → 2/4 | Compute P(both red) in two draws from 3 red 2 blue without replacement → 3/5×2/4=3/10 | `M1-PR-S03-E1` assume independence without replacement; `M1-PR-S03-E2` use unconditional for second draw; `M1-PR-S03-E3` confuse conditional/intersection | D2 |
| `M1-PR-S04` | Compute expectation and variance of finite discrete variables | Fair die E(X) → 3.5 | Find E(X),V(X) for Bernoulli(p) → p, p(1−p) | `M1-PR-S04-E1` sum values without weights; `M1-PR-S04-E2` omit squared mean; `M1-PR-S04-E3` confuse variance with std deviation | D3 |

> **Original source example (retained for provenance):** « E(X) pour X ~ B(n, p) ? » → np

### `M1-EU` — Real inner product spaces

- **Source content:** Inner product, Cauchy-Schwarz, orthonormal bases, orthogonal projection. [TO VERIFY details]
- **Expected learner outcome:** Compute projections and distances.
- **Limit / exclusions:** Hermitian case out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-AL.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-EU-S01` | Recognise inner product and orthogonality | (1,1)·(1,−1) → 0 | Prove Cauchy-Schwarz in R² for two vectors using quadratic nonnegativity | `M1-EU-S01-E1` omit norm factors; `M1-EU-S01-E2` use signed norm; `M1-EU-S01-E3` assume orthogonal if lengths equal | D1 |
| `M1-EU-S02` | Construct orthonormal bases (first-year scope) | Normalise (3,4) → (3/5,4/5) | Apply Gram-Schmidt to (1,0),(1,1) in R² and check orthonormality | `M1-EU-S02-E1` forget normalization; `M1-EU-S02-E2` subtract wrong projection; `M1-EU-S02-E3` ignore linear dependence | D2 |
| `M1-EU-S03` | Compute orthogonal projections | Projection of (1,1) onto x-axis → (1,0) | Project (2,1) onto line span(1,1) → (3/2,3/2), justify formula | `M1-EU-S03-E1` omit denominator \|\|v\|\|²; `M1-EU-S03-E2` confuse orthogonal complement and projection; `M1-EU-S03-E3` use sign error | D2 |
| `M1-EU-S04` | Find distances to subspaces | Distance from (1,1) to x-axis → 1 | Minimise \|\|x−p\|\| to a line using orthogonal projection and prove residual orthogonal | `M1-EU-S04-E1` take projection length as distance; `M1-EU-S04-E2` omit perpendicular component; `M1-EU-S04-E3` assume any point on line nearest | D3 |

> **Original source example (retained for provenance):** « Projeté de (1,1) sur la droite dirigée par (1,0) ? » → (1,0)

### `M1-SN` — Discrete summation (series)

- **Source content:** Numerical series: convergence, comparison, absolute convergence, Riemann series. [TO VERIFY details]
- **Expected learner outcome:** Decide convergence by comparison.
- **Limit / exclusions:** d'Alembert's rule is listed in the 2nd-year program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-SU; M1-LC.
- **Special gate:** VERIFY source detail: first-year series scope should be checked against 2021 annex.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-SN-S01` | Distinguish sequence term and series | Σ(n≥1)1/n² → convergent | Use comparison with p-series to classify Σ1/n³; state conditions | `M1-SN-S01-E1` assume terms→0 ensures sum converges; `M1-SN-S01-E2` compare in wrong direction; `M1-SN-S01-E3` ignore positivity conditions | D1 |
| `M1-SN-S02` | Apply absolute convergence and comparisons | Σ(-1)^n/n² absolutely convergent → yes | Classify Σ(n≥1)1/(n(n+1)) by telescoping → convergent | `M1-SN-S02-E1` overlook telescoping; `M1-SN-S02-E2` wrong partial fraction; `M1-SN-S02-E3` confuse conditional and absolute | D2 |
| `M1-SN-S03` | Evaluate geometric series | Σ(n≥0)(1/2)^n → 2 | Prove finite geometric sum then passage to limit for \|q\|<1 | `M1-SN-S03-E1` forget q=1 case; `M1-SN-S03-E2` apply if \|q\|≥1; `M1-SN-S03-E3` off-by-one exponent | D2 |
| `M1-SN-S04` | Use asymptotic comparisons where first-year confirmed | For n→∞ 1/(n²+1)~1/n² → true | Conclude convergence of Σ1/(n²+1) by limit comparison | `M1-SN-S04-E1` use equivalence under cancellation incorrectly; `M1-SN-S04-E2` compare to divergent harmonic; `M1-SN-S04-E3` omit positive terms condition | D3 |

> **Original source example (retained for provenance):** « Σ 1/n² converge-t-elle ? » → Oui

### `M1-F2` — Functions of two variables

- **Source content:** Partial derivatives, gradient, critical points (end of 2nd semester). [TO VERIFY details]
- **Expected learner outcome:** Compute partial derivatives.
- **Limit / exclusions:** [TO VERIFY]
- **Prerequisite codes / competencies (inferred crosswalk):** M1-LC; M1-TA.
- **Special gate:** OFFICIAL 2021 ANNEX VERIFIED: practical two-variable derivatives, gradient, chain rule, first-order approximation and critical points; do not test abstract differentiability theory or proof of first-order formula.
- **Official 2021 programme scope:** the final MP2I chapter explicitly includes partial derivatives, `C¹` functions, gradient, directional derivatives, chain rule, tangent-plane approximation and critical points. Abstract theory of differentiability and proof of first-order expansion remain out of scope.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M1-F2-S01` | Compute partial derivatives of C1 functions | For f(x,y)=x²y, ∂_x f → 2xy | Compute ∂_x and ∂_y of x²y+xy², treating the other variable as constant | `M1-F2-S01-E1` differentiate both variables simultaneously; `M1-F2-S01-E2` omit product contributions; `M1-F2-S01-E3` mistake evaluation point | D1 |
| `M1-F2-S02` | Use gradient and directional derivatives | Gradient of x+y at origin → (1,1) | For f=x²+y² identify gradient at (1,2) and directional derivative along (1,0) → 2 | `M1-F2-S02-E1` interchange components; `M1-F2-S02-E2` use gradient norm for a directional derivative; `M1-F2-S02-E3` forget evaluation point | D2 |
| `M1-F2-S03` | Apply multivariable chain rule in first-year practical setting | For f=x²+y² and γ(t)=(t,t²), (f∘γ)'(t) → 2t+4t³ | Calculate by partial-derivative chain rule and independently by substitution, showing equality | `M1-F2-S03-E1` omit derivative of one component; `M1-F2-S03-E2` confuse ∂f/∂x and ∂f/∂y; `M1-F2-S03-E3` forget chain coefficient | D2 |
| `M1-F2-S04` | Use first-order approximation and tangent plane for C1 functions | For f=x²+y at (1,2), tangent plane → z=3+2(x−1)+(y−2) | Write local first-order expansion for f=x²+y at (1,2) and identify tangent-plane equation; no proof of general formula required | `M1-F2-S04-E1` omit base value f(a,b); `M1-F2-S04-E2` use wrong partials; `M1-F2-S04-E3` confuse surface and tangent-plane coordinates | D2 |
| `M1-F2-S05` | Locate and assess critical points by elementary methods | For f=x²+y²−2x, only critical point → (1,0) | Find critical point and prove global minimum by completing square, without Hessian theory | `M1-F2-S05-E1` solve only one gradient equation; `M1-F2-S05-E2` assume all critical points extrema; `M1-F2-S05-E3` infer globality without comparison | D3 |

> **Original source example (retained for provenance):** « ∂f/∂x pour f(x, y) = x²y. » → 2xy

## MPI — MPI — CPGE year 2

**Version gate:** 2021 MPI programme, with at least 20% assessment items tagging an explicit year-1 M1 prerequisite in the parent prompt.  
**Status:** `2021 CHAPTERS CONFIRMED — VERIFY EXIGIBILITY OF EVERY ITEM`.

### `M2-ST` — Usual algebraic structures

- **Source content:** Groups (order, cyclic groups), ideals of ℤ and K[X], ℤ/nℤ, Chinese remainder theorem, Euler's φ, algebras.
- **Expected learner outcome:** Use ℤ/nℤ and ideals in proofs.
- **Limit / exclusions:** Proof of d'Alembert-Gauss out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-ST; M1-AR.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-ST-S01` | Use congruence classes and units in Z/nZ | In Z/7Z, inverse of 3 → 5 | Find the invertible elements of Z/8Z, give inverses, justify by gcd | `M2-ST-S01-E1` confuse representatives/classes; `M2-ST-S01-E2` cancel non-units; `M2-ST-S01-E3` assume every nonzero class invertible | D1 |
| `M2-ST-S02` | Apply Chinese remainder theorem in coprime moduli | x≡1(mod 3), x≡2(mod 5) gives x≡ → 7(mod 15) | Solve x≡2(mod 3), x≡3(mod 5) with full residue class | `M2-ST-S02-E1` forget coprimality for uniqueness; `M2-ST-S02-E2` add residues directly; `M2-ST-S02-E3` incorrect modulus product | D2 |
| `M2-ST-S03` | Use Euler totient and cyclic-group order | phi(12) → 4 | Compute phi(15) and verify Euler congruence for a coprime to 15 | `M2-ST-S03-E1` count non-units as units; `M2-ST-S03-E2` use Fermat for composite modulus; `M2-ST-S03-E3` confuse group order and element order | D2 |
| `M2-ST-S04` | Recognise ideals of Z and K[X] | Ideal generated by 6 and 10 in Z → 2Z | Prove every ideal of Z is nZ, identifying the least positive generator | `M2-ST-S04-E1` confuse ideal/subgroup closure; `M2-ST-S04-E2` choose lcm not gcd; `M2-ST-S04-E3` neglect zero ideal | D3 |

> **Original source example (retained for provenance):** « φ(12) ? » → 4

### `M2-RED` — Reduction

- **Source content:** Stable subspaces, eigen-elements, characteristic and minimal polynomials, diagonalisation, trigonalisation, nilpotence, kernel lemma, Cayley-Hamilton.
- **Expected learner outcome:** Decide diagonalisability; use annihilating polynomials.
- **Limit / exclusions:** « Valeur spectrale » out of program; trigonalisation practice not an objective.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-AL; M1-PO.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-RED-S01` | Find characteristic polynomial and eigenvalues | Diagonal diag(2,3) has characteristic polynomial → (X−2)(X−3) | Compute characteristic polynomial of [[2,1],[0,3]]; identify eigenvalues | `M2-RED-S01-E1` use det(A+XI); `M2-RED-S01-E2` sign of characteristic polynomial; `M2-RED-S01-E3` confuse eigenvectors with eigenvalues | D1 |
| `M2-RED-S02` | Distinguish diagonalisation criteria and eigenspace dimensions | A with 2 distinct eigenvalues in M2(C) → diagonalizable | Determine whether [[1,1],[0,1]] is diagonalizable by computing eigenspaces | `M2-RED-S02-E1` assume characteristic roots suffice; `M2-RED-S02-E2` wrong kernel; `M2-RED-S02-E3` confuse trigonalisation with diagonalisation | D2 |
| `M2-RED-S03` | Apply annihilating and minimal polynomials | If A²=0 then eigenvalues belong to → {0} | Use A²−3A+2I=0 to restrict spectrum to {1,2} and discuss diagonalizability | `M2-RED-S03-E1` assume every annihilator minimal; `M2-RED-S03-E2` reverse spectral implication; `M2-RED-S03-E3` ignore square-free criterion | D2 |
| `M2-RED-S04` | Analyse nilpotent matrices and kernel lemma | Nilpotent matrix has determinant → 0 (n≥1) | Prove a nilpotent endomorphism has no nonzero eigenvalue | `M2-RED-S04-E1` nilpotent means zero; `M2-RED-S04-E2` conflate nilpotent and invertible; `M2-RED-S04-E3` overclaim diagonalizability | D3 |

> **Original source example (retained for provenance):** « A nilpotente ⇒ Sp(A) ? » → ⊂ {0}

### `M2-EU` — Endomorphisms of a Euclidean space

- **Source content:** Adjoint, orthogonal matrices, isometries, spectral theorem, positive self-adjoint endomorphisms.
- **Expected learner outcome:** Diagonalise a real symmetric matrix in an orthonormal basis.
- **Limit / exclusions:** Hermitian products out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-EU; M1-AL.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-EU-S01` | Compute adjoint in orthonormal basis | Adjoint of real matrix A in orthonormal basis → A transpose | Find adjoint of [[1,2],[0,3]], justify scalar-product identity | `M2-EU-S01-E1` transpose inverse instead of transpose; `M2-EU-S01-E2` ignore orthonormal-basis hypothesis; `M2-EU-S01-E3` conflate symmetry/orthogonality | D1 |
| `M2-EU-S02` | Use orthogonal matrices and isometries | If Q orthogonal then Q^TQ → I | Prove norm preservation under orthogonal transformation, then find determinant possibilities | `M2-EU-S02-E1` forget Q transpose; `M2-EU-S02-E2` require det=1 only; `M2-EU-S02-E3` conclude all isometries are identity | D2 |
| `M2-EU-S03` | Apply real symmetric spectral theorem | Real symmetric matrices admit → orthonormal eigenbasis | Diagonalise [[2,1],[1,2]] orthogonally and give its eigenvalues 3,1 | `M2-EU-S03-E1` eigenvectors not orthogonalised; `M2-EU-S03-E2` confuse congruence and similarity; `M2-EU-S03-E3` claim complex-only theorem | D2 |
| `M2-EU-S04` | Classify positive semidefinite self-adjoint maps | For symmetric diag(1,0), positive semidefinite? → yes | Use spectrum to determine sign of quadratic form of [[2,0],[0,−1]] | `M2-EU-S04-E1` assume all symmetric maps positive; `M2-EU-S04-E2` omit eigenvalue signs; `M2-EU-S04-E3` confuse positive definite/semidefinite | D3 |

> **Original source example (retained for provenance):** « Une matrice symétrique réelle est-elle diagonalisable ? » → Oui (base orthonormée)

### `M2-EVN` — Topology of normed spaces

- **Source content:** Norms, sequences, equivalent norms, open/closed sets, continuity, operator norm, compactness, path-connectedness, finite dimension.
- **Expected learner outcome:** Prove continuity; use compactness for extrema.
- **Limit / exclusions:** Metric/topological spaces, Cauchy sequences, Banach, Borel-Lebesgue out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-AL; M1-LC.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-EVN-S01` | Work with norms and operator norm | \|\| (3,4) \|\|₂ → 5 | Show a linear operator on finite-dimensional normed spaces is continuous and bound it in an example | `M2-EVN-S01-E1` use coordinatewise bound without norm; `M2-EVN-S01-E2` assume infinite-dimensional equivalence; `M2-EVN-S01-E3` ignore finite dimensionality | D1 |
| `M2-EVN-S02` | Recognise open and closed sets | [0,1] in R is → closed and bounded | Prove closed unit ball is closed and bounded; discuss compactness in finite dimension | `M2-EVN-S02-E1` confuse open/closed with bounded; `M2-EVN-S02-E2` assume bounded implies compact generally; `M2-EVN-S02-E3` ignore topology induced by norm | D2 |
| `M2-EVN-S03` | Apply compactness to extrema | Continuous f on nonempty compact K attains → min and max | Find extrema of f(x)=x² on [-2,1] and justify Weierstrass hypotheses | `M2-EVN-S03-E1` use open interval; `M2-EVN-S03-E2` forget continuity; `M2-EVN-S03-E3` assume unbounded domain compact | D2 |
| `M2-EVN-S04` | Use equivalent norms and convergence | All norms on R^n are equivalent → true | Prove convergence of (1/n,(-1)^n/n) in R² and justify norm independence | `M2-EVN-S04-E1` conflate coordinatewise and uniform convergence; `M2-EVN-S04-E2` invoke Banach theorem; `M2-EVN-S04-E3` claim norm equivalence in all dimensions | D3 |

> **Original source example (retained for provenance):** « En dimension finie, les normes sont-elles équivalentes ? » → Oui

### `M2-SE` — Numerical & vector series

- **Source content:** Absolute convergence, series-integral comparison, d'Alembert's rule, comparison relations.
- **Expected learner outcome:** Determine nature and asymptotics of series.
- **Limit / exclusions:** Cauchy criterion and semi-convergent series study out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-SN; M1-AA.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-SE-S01` | Classify positive numerical series with comparison | sum 1/n² converges → yes | Prove convergence of sum 1/(n²+1) using appropriate positive comparison | `M2-SE-S01-E1` reverse comparison direction; `M2-SE-S01-E2` omit positivity; `M2-SE-S01-E3` infer from term→0 | D1 |
| `M2-SE-S02` | Use d'Alembert ratio test where eligible | For sum n!/n^n, ratio limit → 1/e | Classify sum n!/n^n by ratio test, writing a_{n+1}/a_n | `M2-SE-S02-E1` apply ratio test to sign-changing terms blindly; `M2-SE-S02-E2` miscompute ratio; `M2-SE-S02-E3` infer from limit equal 1 | D2 |
| `M2-SE-S03` | Analyse vector series via absolute convergence | If sum \|\|u_n\|\| finite in R², sum u_n → converges | Study sum (1/n²,(-1)^n/n²) in R² and prove convergence by norm bound | `M2-SE-S03-E1` infer convergence only coordinatewise without proof; `M2-SE-S03-E2` confuse norm and components; `M2-SE-S03-E3` ignore completeness of finite-dimensional space | D2 |
| `M2-SE-S04` | Use asymptotic term comparison for series | For positive u_n~1/n², series sum u_n → converges | Compare sum 1/(n²+n) to reference series and justify equivalent | `M2-SE-S04-E1` compare asymptotic sums instead of terms; `M2-SE-S04-E2` use cancellation incorrectly; `M2-SE-S04-E3` omit eventual positivity | D3 |

> **Original source example (retained for provenance):** « Nature de Σ n!/nⁿ ? » → convergente (d'Alembert)

### `M2-SF` — Sequences & series of functions

- **Source content:** Simple, uniform, normal convergence; double limit, term-by-term integration/derivation; Weierstrass.
- **Expected learner outcome:** Justify interchange of limits.
- **Limit / exclusions:** Proof of double-limit theorem out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-LC; M1-SN.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-SF-S01` | Distinguish pointwise and uniform convergence | f_n(x)=x^n on [0,1] converges uniformly? → no | Prove pointwise limit of x^n on [0,1] is discontinuous; explain why not uniform | `M2-SF-S01-E1` interchange quantifiers; `M2-SF-S01-E2` infer uniform from continuity of each f_n; `M2-SF-S01-E3` omit endpoint x=1 | D1 |
| `M2-SF-S02` | Apply uniform-convergence continuity theorem | Uniform limit of continuous f_n is → continuous | Prove uniform convergence of f_n(x)=x/n on [0,1] using supremum bound then conclude continuity | `M2-SF-S02-E1` pointwise bound dependent on x; `M2-SF-S02-E2` assume unbounded-domain sup finite; `M2-SF-S02-E3` omit hypotheses | D2 |
| `M2-SF-S03` | Test normal convergence of series of functions | sum \|\|f_n\|\|∞<∞ implies → uniform convergence | Show sum x^n/n² converges normally on [0,1] by M-test | `M2-SF-S03-E1` sum sup vs sup sum confusion; `M2-SF-S03-E2` use M-test with divergent majorant; `M2-SF-S03-E3` confuse uniform and normal | D2 |
| `M2-SF-S04` | Justify termwise integration or differentiation with correct hypotheses | Uniform convergence on a segment permits termwise → integration | For sum x^n/2^n on [0,1] integrate termwise and justify uniform convergence | `M2-SF-S04-E1` swap integral/sum without theorem; `M2-SF-S04-E2` confuse derivative conditions; `M2-SF-S04-E3` apply on noncompact domain without check | D3 |

> **Original source example (retained for provenance):** « fₙ(x) = xⁿ sur [0 ; 1] : convergence uniforme ? » → Non

### `M2-SEN` — Power series

- **Source content:** Radius, Abel's lemma, continuity and regularity of the sum, usual expansions.
- **Expected learner outcome:** Compute radii; expand usual functions.
- **Limit / exclusions:** Proof of radial Abel theorem out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-SN; M1-AA.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-SEN-S01` | Find radius of convergence using ratio test on coefficients | sum x^n/n has radius → 1 | Determine radius of sum n x^n and discuss convergence at endpoints | `M2-SEN-S01-E1` confuse term series with power series; `M2-SEN-S01-E2` include endpoint automatically; `M2-SEN-S01-E3` misuse radius inequality | D1 |
| `M2-SEN-S02` | Expand familiar functions into power series | sum x^n for \|x\|<1 → 1/(1−x) | Differentiate geometric series within \|x\|<1 to derive sum n x^(n−1) | `M2-SEN-S02-E1` differentiate on boundary; `M2-SEN-S02-E2` omit derivative coefficient; `M2-SEN-S02-E3` wrong radius | D2 |
| `M2-SEN-S03` | Work with Abel lemma and power-series regularity | For \|x\|<R, power series sum a_n x^n is → infinitely differentiable | Justify term-by-term derivation of sum x^n/n on (-1,1), obtain 1/(1−x) | `M2-SEN-S03-E1` apply theorem at endpoint; `M2-SEN-S03-E2` confuse continuity of sum and uniformity globally; `M2-SEN-S03-E3` miscompute coefficients | D2 |
| `M2-SEN-S04` | Distinguish radius and endpoint convergence | sum x^n/n at x=−1 converges? → yes | Check convergence at x=−1 and x=1 separately for sum x^n/n, with appropriate tests | `M2-SEN-S04-E1` apply radius test at boundary; `M2-SEN-S04-E2` treat alternating harmonic absolutely convergent; `M2-SEN-S04-E3` ignore endpoint divergence | D3 |

> **Original source example (retained for provenance):** « Rayon de Σ xⁿ/n ? » → 1

### `M2-FV` — Vector-valued functions

- **Source content:** Derivation, integral on a segment, integral as function of upper bound, Taylor formulas.
- **Expected learner outcome:** Apply Taylor formulas to vector functions.
- **Limit / exclusions:** —
- **Prerequisite codes / competencies (inferred crosswalk):** M1-LC; M1-IN.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-FV-S01` | Derive vector-valued functions coordinatewise | F(t)=(t²,e^t); F'(t) → (2t,e^t) | Determine tangent vector to curve F(t)=(cos t,sin t) at t=0 and discuss orthogonality to radius | `M2-FV-S01-E1` differentiate norm instead of components; `M2-FV-S01-E2` confuse vector/coordinate; `M2-FV-S01-E3` treat derivative as scalar | D1 |
| `M2-FV-S02` | Use fundamental theorem for vector integrals | Integral_0^1 (t,t²)dt → (1/2,1/3) | Compute vector primitive and definite integral of (2t,e^t) on [0,1] | `M2-FV-S02-E1` mix integral and norm; `M2-FV-S02-E2` omit integration constant for primitive; `M2-FV-S02-E3` swap endpoint signs | D2 |
| `M2-FV-S03` | Apply Taylor formula to vector functions | First-order Taylor of F(t)= (cos t,sin t) at 0 → (1,t)+o(t) | Write order-two expansion of F(t)=(e^t,cos t) at 0 with vector remainder | `M2-FV-S03-E1` wrong remainder norm; `M2-FV-S03-E2` omit second derivative; `M2-FV-S03-E3` treat components at differing orders | D2 |
| `M2-FV-S04` | Bound vector increments with derivative | If \|\|F'(t)\|\|≤M on [a,b], then \|\|F(b)-F(a)\|\|≤ → M(b−a) | Prove norm inequality using integral of F' and triangle inequality | `M2-FV-S04-E1` use scalar mean-value equality for vectors; `M2-FV-S04-E2` bound derivative coordinate only; `M2-FV-S04-E3` lose absolute interval length | D3 |

> **Original source example (retained for provenance):** « Inégalité des accroissements finis pour f vectorielle. »

### `M2-IN` — Integration on any interval

- **Source content:** Integrability, comparison, IPP and change of variable, dominated convergence, term-by-term integration, parameter integrals.
- **Expected learner outcome:** Justify integrability and apply dominated convergence.
- **Limit / exclusions:** Semi-convergent integrals not an objective; proofs of dominated convergence out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-IN; M1-SN.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-IN-S01` | Test integrability on unbounded interval | Integral_0^infty e^(−t)dt → 1 | Discuss convergence of integral_1^infty 1/t² dt and compute value | `M2-IN-S01-E1` treat all unbounded integrals divergent; `M2-IN-S01-E2` compute primitive endpoints incorrectly; `M2-IN-S01-E3` use upper endpoint infinity algebraically | D1 |
| `M2-IN-S02` | Use comparison for improper integrals | For p>1, integral_1^infty t^(−p) converges → true | Classify integral_1^infty 1/sqrt(t) dt using p-integral test | `M2-IN-S02-E1` reverse p criterion; `M2-IN-S02-E2` ignore positivity; `M2-IN-S02-E3` conflate near zero/infinity | D2 |
| `M2-IN-S03` | Apply dominated convergence with stated bound | If \|f_n\|≤g integrable and f_n→0 pointwise, integral f_n → 0 (under hypotheses) | For f_n(t)=e^(−nt) on [0,1] apply dominated convergence, determine integral limit | `M2-IN-S03-E1` omit uniform domination; `M2-IN-S03-E2` assume pointwise convergence at every endpoint; `M2-IN-S03-E3` confuse theorem statement with proof requirement | D2 |
| `M2-IN-S04` | Change variable / integrate by parts on improper integrals | Integral_0^infty t e^(−t)dt → 1 | Compute integral_0^infty t e^(−t)dt via integration by parts with boundary justification | `M2-IN-S04-E1` omit boundary at infinity; `M2-IN-S04-E2` apply IPP without convergence check; `M2-IN-S04-E3` wrong sign | D3 |

> **Original source example (retained for provenance):** « ∫₀^{+∞} e^(−t) dt ? » → 1

### `M2-PR` — Discrete random variables

- **Source content:** Countable sets, probability spaces, conditioning, usual laws (geometric, Poisson), expectation, variance, covariance, Markov, Bienaymé-Tchebychev, weak LLN, generating functions.
- **Expected learner outcome:** Model with discrete laws; use generating functions.
- **Limit / exclusions:** σ-algebra manipulation, densities, conditional expectation, a.s./in-law convergence out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-PR; M1-SN.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-PR-S01` | Model a countable discrete distribution | For Poisson(lambda), P(X=0) → e^(−lambda) | Verify sum_{k≥0} e^(−lambda)lambda^k/k!=1 from exponential series | `M2-PR-S01-E1` assume finite universe; `M2-PR-S01-E2` confuse mass and density; `M2-PR-S01-E3` incorrect normalization | D1 |
| `M2-PR-S02` | Calculate expectation and variance of standard laws | For geometric(p) on {1,2,...}, E(X) → 1/p | Compute E and Var of Poisson(lambda), state assumed parametrization and support | `M2-PR-S02-E1` confuse geometric conventions; `M2-PR-S02-E2` use E² for variance; `M2-PR-S02-E3` conflate Poisson and binomial | D2 |
| `M2-PR-S03` | Use generating functions for sums of independent variables | Poisson(lambda) generating function → exp(lambda(t−1)) | Find generating function of X+Y for independent Poisson(lambda),Poisson(mu) and deduce law | `M2-PR-S03-E1` add rather than multiply generating functions; `M2-PR-S03-E2` omit independence; `M2-PR-S03-E3` differentiate at wrong t | D2 |
| `M2-PR-S04` | Apply concentration bound for discrete variables | If Var(X)=4, P(\|X−E(X)\|≥4)≤ → 1/4 | Use Chebyshev to bound P(\|sample mean−mu\|≥epsilon) in an iid finite-variance model | `M2-PR-S04-E1` use Markov on signed variable; `M2-PR-S04-E2` forget n variance factor; `M2-PR-S04-E3` interpret upper bound as exact value | D3 |

> **Original source example (retained for provenance):** « G_X(t) pour X ~ P(λ) ? » → e^(λ(t−1))

### `M2-ED` — Linear differential equations

- **Source content:** Cauchy linear theorem, solution structure, matrix exponential, constant-coefficient systems, variation of constants.
- **Expected learner outcome:** Solve linear systems via reduction and exp(A).
- **Limit / exclusions:** Explicit solving of constant-coefficient systems not an objective.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-TA; M1-AL.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-ED-S01` | Solve scalar linear homogeneous ODE | Solve y'=3y with y(0)=2 → 2e^(3t) | Solve y'−2y=0 with boundary condition and justify uniqueness | `M2-ED-S01-E1` wrong exponential sign; `M2-ED-S01-E2` omit arbitrary constant; `M2-ED-S01-E3` apply boundary at wrong t | D1 |
| `M2-ED-S02` | Use matrix exponential for constant-coefficient systems | For X'=AX, X(0)=X0 solution → e^(tA)X0 | Verify X(t)=e^(tA)X0 for a diagonal A by differentiation and initial-value check; explicit system solving is not a mandatory objective | `M2-ED-S02-E1` apply exponential entrywise to arbitrary matrix; `M2-ED-S02-E2` confuse left/right multiplication; `M2-ED-S02-E3` omit initial state | D2 |
| `M2-ED-S03` | Use diagonalisation for matrix exponentials | If A=PDP^-1 then e^(tA)= → P e^(tD) P^-1 | Derive e^(tA)=P e^(tD) P^-1 for an explicitly diagonalizable A; state the method without requiring an explicit IVP solution | `M2-ED-S03-E1` reverse basis matrices; `M2-ED-S03-E2` take exp eigenvalues without t; `M2-ED-S03-E3` assume all matrices diagonalizable | D2 |
| `M2-ED-S04` | Apply variation of constants | For y'+y=1, y(0)=0 → 1−e^(−t) | Derive variation-of-constants solution to y'=ay+f(t) in simple case | `M2-ED-S04-E1` forget integrating factor; `M2-ED-S04-E2` wrong integration bounds; `M2-ED-S04-E3` count particular solution as unique without homogeneous term | D3 |

> **Original source example (retained for provenance):** « Solution de X′ = AX, X(0) = X₀ ? » → X(t) = e^(tA)X₀

### `M2-CD` — Differential calculus & optimisation

- **Source content:** Directional/partial derivatives, differential, gradient, chain rule, C¹/Cᵏ, tangent vectors, critical points, constrained extrema, Hessian.
- **Expected learner outcome:** Find and classify extrema.
- **Limit / exclusions:** Implicit function theorem and second differential out of program.
- **Prerequisite codes / competencies (inferred crosswalk):** M1-F2; M1-AL; M1-LC.
- **Special gate:** OFFICIAL MPI exclusion: second differential and implicit-function theorem.

| Atomic skill | Observable target | MCQ probe → correct result | Open probe → expected outcome | Misconceptions E1 / E2 / E3 | Suggested D |
|---|---|---|---|---|---|
| `M2-CD-S01` | Compute partial derivatives and gradient | For f(x,y)=x²+y²−2x, grad f → (2x−2,2y) | Find critical point of x²+y²−2x and evaluate function there | `M2-CD-S01-E1` differentiate wrong coordinate; `M2-CD-S01-E2` only solve one equation; `M2-CD-S01-E3` confuse point and value | D1 |
| `M2-CD-S02` | Use chain rule in several variables | For f(x,y)=x²+y², path (t,t²), derivative at t=1 → 6 | Compute derivative of f(cos t,sin t) with multivariable chain rule; state vector form | `M2-CD-S02-E1` forget inner derivative; `M2-CD-S02-E2` confuse partial and directional; `M2-CD-S02-E3` evaluate at wrong point | D2 |
| `M2-CD-S03` | Apply differentiability/Taylor formula to optimise | For f=x²+y² at 0, Hessian → 2I | Use positive-definite Hessian at a critical point to conclude strict local min; explain hypotheses | `M2-CD-S03-E1` infer min from stationary alone; `M2-CD-S03-E2` confuse determinant condition; `M2-CD-S03-E3` attempt proof of second differential | D2 |
| `M2-CD-S04` | Analyse constrained extrema with permitted techniques | For x²+y²=1, max x → 1 | Find extrema of x+y over unit disk and justify using Cauchy-Schwarz, state attainment | `M2-CD-S04-E1` apply interior derivative condition only; `M2-CD-S04-E2` ignore boundary; `M2-CD-S04-E3` invoke implicit function theorem | D3 |

> **Original source example (retained for provenance):** « Points critiques de f(x, y) = x² + y² − 2x ? » → (1 ; 0)

## 4. Exclusion and boundary registry (question-writing blockers)

| Track | Do not test as ordinary on-programme items |
|---|---|
| Brevet | General quadratic discriminant-solving; analytic geometry with vectors; general unrestricted trig; advanced statistical inference; Python-specific coding if the task assumes Scratch only. |
| Première speciality | Formal full limit definitions for sequences; Terminale logarithm or binomial distribution as Première-specific topics; generic derivative of arbitrary composite functions. Check the **2026** annex for detailed progression. |
| Première common, 2026 programme | Derivative and tangent calculus; discriminant method for quadratics; unconstrained abstract proof-heavy sequence theory; general continuous density laws. |
| Terminale speciality | General complex number curriculum (belongs to maths expertes); density laws unless explicit programme update says otherwise; improper integrals. |
| Maths expertes | Complex analysis; quotient-ring structures as a required abstract chapter; general spectral theory. |
| MP2I | `Z/nZ` ring theory; countable probability universes as the standard year-1 probability syllabus; Laplace transforms; proof of Stirling. |
| MPI | Proof of d'Alembert–Gauss, proof of double-limit/radial-Abel/dominated-convergence theorems; Hermitian inner products; general metric/Banach theory; sigma-algebra manipulation; probability densities; conditional expectation; almost-sure or distributional convergence; second differential and implicit-function theorem. |

## 5. Fully formed examples — MCQs (teacher demonstration only)

### Example A — Brevet `BR-NC-S04`, D1

**Student prompt (French, appropriate when `{OUTPUT_LANGUAGE}=French`):**  *Factoriser* `9x² − 25`.

A. `(3x − 5)(3x + 5)`  
B. `(9x − 5)(x + 5)`  
C. `(3x − 5)²`  
D. `(9x − 25)(x + 1)`

**Key:** A. Explanation: difference of squares `(3x)²−5²`. **Error evidence:** B mishandles first square; C mistakes conjugate product for square; D treats original as factor with an unjustified extra factor. **Review:** Option B expands to `9x²+40x−25`, option C to `9x²−30x+25`, option D is non-equivalent. Each distractor has a distinct fault mechanism.

### Example B — Première speciality `1S-PS-S01`, D2

If `P(A)=0.4` and `P(B|A)=0.5`, what is `P(A∩B)`?

A. `0.9` · B. `0.2` · C. `0.5` · D. `0.1`

**Key:** B. Product formula `P(A∩B)=P(A)P(B|A)`. A adds instead of multiplying; C reports conditional probability; D is an unsupported product or mistaken scaling. Context must specify that `P(A)>0`.

### Example C — MPI `M2-SF-S01`, D2

Let `f_n(x)=x^n` on `[0,1]`. Which statement is correct?

A. `f_n` converges uniformly to `0` on `[0,1]`.  
B. `f_n` converges pointwise to a continuous function on `[0,1]`.  
C. `f_n` converges pointwise, but **not uniformly**, on `[0,1]`.  
D. `f_n` does not converge pointwise at `x=1`.

**Key:** C. Pointwise limit is `0` for `0≤x<1` and `1` for `x=1`, so discontinuous and cannot be uniform limit of continuous functions. B confuses pointwise and uniform; A ignores endpoint `1`; D mistakes constant sequence `1^n=1`. All options assessed for the entire specified interval.

## 6. Fully formed examples — open response (teacher demonstration only)

### Example D — Brevet `BR-EG-S01` (4 pts, D2)

*Un triangle possède des côtés de longueurs 5 cm, 12 cm et 13 cm. Démontrer qu'il est rectangle.*

| Observable step | Pts |
|---|---:|
| Identify 13 cm as longest side and state converse of Pythagoras | 1 |
| Calculate `5²+12²=25+144=169` | 1 |
| Calculate `13²=169` and compare both expressions | 1 |
| State the triangle is right-angled opposite the side of 13 cm | 1 |

**Diagnoses:** assumption of right angle without converse; numerical-square mistakes; omitted conclusion.

### Example E — Terminale speciality `TS-AN-S04` (8 pts, D2)

*Calculer l'intégrale* `I = ∫₀¹ x e^x dx` *par intégration par parties.*

| Observable step | Pts |
|---|---:|
| Specify integration-by-parts decomposition: `u=x`, `dv=e^x dx` | 2 |
| Derive `I=[xe^x]₀¹−∫₀¹e^x dx` | 2 |
| Evaluate boundary term `e` and exponential integral `e−1` | 2 |
| Conclude `I=1` and check positivity | 2 |

**SCoT:** Data: integral on `[0,1]` → Method: IPP → Steps shown → Result 1 → Check: integrand nonnegative; value consistent with bounds. **Session gate:** integrals are from applicable Terminale programme, not Première.

### Example F — MPI `M2-SF-S01` (12 pts, D3 proof)

*Soit `(f_n)` une suite de fonctions continues sur un intervalle `I`, convergeant uniformément vers `f` sur `I`. Démontrer que `f` est continue en un point arbitraire `x₀∈I`.*

| Observable proof obligation | Pts |
|---|---:|
| State uniform convergence using `∀ε>0 ∃N ∀n≥N ∀x∈I` | 2 |
| Fix `x₀` and select `n≥N`, using continuity of this `f_n` | 2 |
| Bound `|f(x)−f(x₀)|` by the standard three-term decomposition | 4 |
| Make each of the three terms `<ε/3` with valid parameter choices | 2 |
| Conclude continuity for arbitrary `x₀` with correct quantifiers | 2 |

**Common errors:** `N` depends on `x`; uniform convergence used only at `x₀`; δ chosen without controlling `f_n`. A coherent alternative proof receives equal credit.

### Example G — MPI `M2-SF-S01` (8 pts, find-the-error)

*A student writes: « Les fonctions `f_n(x)=x^n` sont continues sur `[0,1]`. Leur limite est donc continue. » Trouver précisément l'erreur et corriger le raisonnement.*

| Observable step | Pts |
|---|---:|
| Determine pointwise limit for `x∈[0,1[` and at `x=1` | 2 |
| State discontinuity of the limit at 1 | 2 |
| Identify missing **uniform** convergence hypothesis | 2 |
| Explain contradiction with uniform-limit continuity theorem, or give direct sup-norm argument | 2 |

## 7. Gap diagnosis, misconception IDs and coverage

### Required teacher-record fields per generated question

| Field | Allowed content | Example |
|---|---|---|
| `item_id` | Unique `Q-` or `O-` key | `Q-M2-SF-S01-02` |
| `parent_code` | One of the 60 original codes | `M2-SF` |
| `primary_skill` | Exactly one `<code>-S##` | `M2-SF-S01` |
| `session` / `programme_version` | Exact school year and official version | `2026–2027`, `2026-04-02 Première` |
| `format` | `MCQ_4_ONE` / `OPEN` / `SHORT_RESPONSE` | `MCQ_4_ONE` |
| `difficulty`, `minutes` | D1/2/3; respectively 1/2/3 for MCQ or 4/8/12 for open (overridable with justification) | `D2`, `2` |
| `misconception_ids` | One to three IDs from relevant micro-skill | `M2-SF-S01-E2` |
| `correct_answer` | Validated exact answer or admissible equivalence class | `not uniform` |
| `rubric` | Named observable steps, total point count, valid alternatives | Four steps, 8 points |
| `prerequisite_code` | Additional code if intentionally testing a prerequisite | `M1-LC` |
| `eligibility` | `VERIFIED_FOR_SESSION`, `DRAFT`, `PROVISIONAL`, `EXCLUDED` | `DRAFT` |
| `evidence` | Official source URL and pinpoint/extract used for eligibility | `...` |

**Avoid overclaiming documentation:** E1–E3 are candidate misconceptions for design; the supplied files do not empirically document all such misconceptions. Tag them `MISCONCEPTION-CANDIDATE` until linked to student scripts, DEPP analyses or a documented didactic source.

**Diagnostic status thresholds (from supplied prompt):** acquired ≥80%; partially acquired 50–79%, or a well-established specific error; fragile 30–49% with scattered errors; not acquired <30%. **Do not assign** a mastery status for an **untested** micro-skill. If fewer than two independent items assess a skill, report **insufficient evidence** unless evidence from a rubric clearly differentiates the target. Even then, qualify the inference.

**Remediation chain:** `primary_skill → one confirmed misconception → brief concept reminder → two progressively harder exercises → fresh re-test on the same skill`. Never reuse an identical numeric MCQ as proof of remediation.

### Time feasibility worked example — 55-minute diagnostic

A default of 16 MCQs plus 3 open questions **can exceed** the prompt's 90% working-time ceiling (49.5 min). A balanced feasible example:

- MCQs: 5×D1 at 1 minute, 7×D2 at 2 minutes, 2×D3 at 3 minutes = **25 minutes**.
- Open questions: 1×D1 at 4 minutes, 1×D2 at 8 minutes, 1×D3 at 12 minutes = **24 minutes**.
- Total: **14 MCQs + 3 open = 49 minutes**, under 49.5 minutes; if DYS extra time applies, compute allowable time using the actual authorised duration, not double-counting the accommodation.
- MPI with this 17-item blueprint requires **at least 4 M1-labelled prerequisite items**, because 20% of 17 = 3.4 and counts must round up.

### Two unresolved logic conflicts in the original diagnostic prompt

1. **Full micro-skill coverage vs time constraint:** with this expanded catalogue, `ALL` means potentially hundreds of micro-skills. Requiring ≥1 item for *every* selected micro-skill in 55 minutes is impossible. **Proposed rule:** assess a declared subset of micro-skills per sitting; display all excluded micro-skills as `NOT_TESTED`, not as unmastered; cover the remaining ones across successive assessments.
2. **Programme-first verification vs automatic draft:** the prompt excludes all `[TO VERIFY]` content from final keys but many of its legacy curriculum catalogue lines are `[TO VERIFY]`. **Proposed rule:** build an official-source eligibility map before writing items; if verification is unavailable, deliver **draft-only** questions with no claim of exam conformity.

### Copy-ready supplement for the existing PROMPTEZ prompt

```text
CURRICULUM-REFERENCE INTEGRATION — ADDITIONAL RULES

Use "Math_Curriculum_Diagnostic_Expanded_EN_v3.md" as the structured
candidate skill bank. Preserve all original parent codes and the new
-S01/-S02/... micro-skill codes. For each generated question:
  1. Validate school year, exam session, subject track, and current BO annex.
  2. Select exactly one primary micro-skill and optional tested prerequisite.
  3. In the Teacher version only, record program source, admissible methods,
     misconception IDs, reasoning rubric, difficulty, and time.
  4. For a MCQ, construct exactly four distinct choices (one correct),
     each distractor linked to a different misconception candidate.
  5. For OPEN, write a complete independent marking rubric and check.
  6. Never use any PROVISIONAL or EXCLUDED skill in the scored Student version.
  7. Distinguish OFFICIAL_EXAM_SIMULATION from DIAGNOSTIC_MCQ.
  8. Bac 2028 Première automatisms use short answers in exam simulations;
     diagnostic MCQs remain permitted if the user requests a diagnostic.
  9. Coverage is assessed against DECLARED_SELECTED_SKILLS, not all
     micro-skills in the reference. Untested is not "not acquired".
 10. If 16 MCQs + 3 OPEN cannot meet 90% of DURATION, propose a reduced
     balanced blueprint and ask for approval as required by the main prompt.
 11. For MPI, verify that ≥20% of all selected items test M1 prerequisites;
     do not count mere secondary mentions as tested prerequisites.
 12. Include both M1-DT and M1-F2 in MP2I catalogue; both appear in
     the 2021 official mathematics annex. Keep M1-F2 practical-scope limits.
 13. For any new school year or revised programme, revalidate the curriculum
     before using a previously released item bank.
```

## 7A. V5 — Automatic skill attribution, remediation planning and quality gates

### Compatible additions to the original diagnostic PROMPTEZ prompt

- Preserve the supplied **one primary programme skill per item** policy. A wrong answer may additionally carry **one root-error code**, one `prerequisite_skill`, and further observation annotations. A primary skill need not be recorded as failed merely because a basic-calculation step failed.
- Allow the **24 v5 `BR-NC-F##` foundation codes** when `ASSESSMENT_MODE=FOUNDATION_DIAGNOSTIC` or as declared prerequisite checks at any level. They are **not** new official `BREVET` examination strands. In a Terminale or MPI report, separate prerequisite accuracy from on-track curriculum accuracy.
- Add item-format `PROOF` (or treat it as `OPEN` with `task_type=PROOF`) for `BR-EG-S06`–`BR-EG-S17`; require hypotheses, theorem, application, conclusion. For MCQs about proofs, ask one precisely defined logical step.
- `TS-AN-S06`–`S19` and `TS-LO-S05`–`S08` have a **scope gate per row**. Any `CPGE-BRIDGE`/`PEDAGOGICAL-BRIDGE` item needs `{ENRICHMENT}=true` or `{PURPOSE}=PRE_CPGE`; it is not part of a strict Terminale official exam simulation. The underlying standard limit/derivative concepts may be tested separately in regular on-programme form.
- Require `root_error_id`, `evidence_level`, `step_index`, `error_role`, `teacher_confirmed`, `remediation_id`, and `retest_id` in the teacher/export version where there is sufficient evidence. In the **student version** omit diagnostic labels, answer keys, misconception hints, and sensitive annotations.
- Every **foundation or geometry proof** error must trigger a targeted **same-skill** remediation and **different-number/different-figure** retest. In particular, never infer correct geometry reasoning just because the numeric result is right.
- A distractor maps to a **hypothesis**, not to a confirmed psychological or didactic cause; confirm with a new independent task or visible method.
- If an MCQ requires identifying **which line** fails, all candidate line choices must be independently checkable and exactly one marked as the **first error**.
- Maintain two coverage matrices: **programme skills** and **root-error mechanisms**. The first asks *what was assessed?*; the second asks *what repeatedly went wrong?* Do not inflate programme coverage by counting cross-cutting root tags as separate curricular chapters.
- Preserve the prompt's hard constraints: calculator eligibility, school-year programme selection, ≤90% timing, MPI ≥20% verified `M1-*` prerequisite items, and student/teacher separation. Foundation `BR-NC-F##` items **do not** count as `M1-*` items for the MPI quota.

### Required longitudinal aggregate per learner × error code

| Metric | Exact meaning | Decision use |
|---|---|---|
| `exposures` | Independent items where this mechanism could be detected | Denominator; cannot infer lack of error from non-exposure |
| `observed_root_occurrences` | Times the mechanism was verified as a **root** (not propagated) | Error frequency |
| `hypothesis_only_occurrences` | MCQ-based or ambiguous mapping | Provisional targeting, not confirmed prevalence |
| `last_3_independent_accuracy` | Three recent comparable same-skill probes, if available | Short-term progress signal |
| `first_seen`, `last_seen`, `distinct_sittings` | Date range and recurrence | Persistence / recurrence |
| `retest_passed_independent` | Both fresh probes passed without hint | Possible teacher-approved resolution |
| `teacher_override_reason` | Explain exceptions and manual classification | Auditability / human oversight |

### Student progress dashboard (teacher-facing)

| Column | Example | Rule |
|---|---|---|
| Curriculum area | `TS-AN-S03` | One primary programme target |
| Prerequisite mechanism | `EC-SGN-MUL` | Root error confirmed separately |
| Observations | 3 independent, 2 verified wrong | State sample size |
| Inference | `FRAGILE / provisional` | Combine points with evidence; no medical inference |
| Intervention | `REM-EC-SGN-MUL-001` | Rule + two graded practice items |
| Re-test | `RT-EC-SGN-MUL-2026-10` | Fresh problems; teacher review |
| Next scheduled review | ISO date | Prevent a gap from being lost |

### Integrity checks added in v5

- [ ] Each `BR-NC-F##`, `BR-EG-S06`–`S17`, `TS-AN-S06`–`S19`, `TS-LO-S05`–`S08` code is unique and has a candidate MCQ, open prompt, error tag, and difficulty.
- [ ] Every geometry proof includes valid hypotheses and an explicit theorem direction (direct / converse / contrapositive); avoid circular arguments.
- [ ] Every ε proof has strictly correct integer thresholds, domains, and quantified dependencies; check `N(ε)` and δ choices.
- [ ] Approximation uses `≈` or a stated remainder, not an invalid exact equality; `h` is nonzero wherever division by `h` occurs.
- [ ] Every candidate root error is linked to **a specific wrong line** or follow-up evidence; a single MCQ does not automatically confirm it.
- [ ] In official exam simulation no `CPGE-BRIDGE` skill appears and the real exam format is used; diagnostic MCQs are still allowed outside simulation.
- [ ] Longitudinal metrics do not merge retries of the **same item** into independent exposures.
- [ ] Existing 247 micro-skills, 60 original subdomains, original example annotations, and MPI 20% rule are unchanged.

### V5 copy-ready override block

```text
DIAGNOSTIC REFERENCE = French_Math_Diagnostic_Curriculum_Reference_CODEX_v5.md

For each assessment:
- Select an applicable official curriculum version and distinguish DIAGNOSTIC
  from EXAM_SIMULATION and optional PRE_CPGE/ENRICHMENT scopes.
- Preserve a single primary curriculum skill. Add a separate root-error tag only
  when the student's visible reasoning or independent probes support it.
- Test arithmetic prerequisites where sign, parentheses, fractions, powers,
  equalities or domains might mask an advanced skill; use BR-NC-F01..F24.
- For Brevet geometry, include open DEMONSTRATION and ERROR_FIND tasks with
  hypothesis → theorem/converse → application → conclusion rubrics.
- For Terminale, enable formal ε / infinitesimal / differential items only in
  explicit enrichment or CPGE-transition mode; exclude them from standard exam
  simulations unless session-specific official authority makes them examinable.
- Export append-only attempt and step-level evidence, error_role, confidence,
  remediation action and independent retest; distinguish observed errors from
  hypotheses and root causes from propagated mistakes.
- Continue all original prompt timing, MPI prerequisite, calculator,
  source-verification and student/teacher separation constraints.
```

## 8. Quality assurance and known issues before production use

- **Content source vs official scope:** source descriptions and editorial decomposition are not enough for an official conformity guarantee. Check every item against the precise official programme version and its *capacités attendues*.
- **`M1-DT` catalogue omission:** the diagnostic prompt's MP2I list merges determinant topics into `M1-AL` but the reference file has separate `M1-DT`. Preserve both codes; amend the prompt catalogue accordingly.
- **`M1-F2` catalogue omission:** the 2021 official MP2I annex confirms this chapter and its practical scope. The prompt must add `M1-F2`; do not test abstract differentiability theory or a proof of the first-order expansion.
- **`BAC_1RE_COMMUN` change:** reference's derivative claim does not match the new 2026 integrated-maths programme. Do not issue the derivative material as standard `1C-FN` from 2026 onward.
- **`BAC_1RE_SPE` programme shift:** the 2026 specialty annex retains some topics under revised descriptions; its derivative concept is introduced intuitively, not via general formal limit proofs.
- **`BAC_TLE_SPE` programme shift:** consult both existing and replacement programme according to the school year; the original source alone cannot determine what is examinable in 2028+.
- **`BAC_TLE_COMPLEMENTAIRES` syllabus:** keep the supplied six parent codes for compatibility but check content and boundaries against the relevant option programme edition; the grouping is an editorial diagnostic taxonomy, not necessarily chapter titles.
- **Possible overlaps:** `TS-AN`/`TS-LO` induction; `TC-PR`/`TC-BA` Bayes; `M1-AL`/`M1-DT` determinants; `M2-CD`/`M1-F2` derivatives. Assign only **one** primary micro-skill to each item and record the other strictly as a supporting prerequisite if relevant.
- **MCQ keys & distractors:** seeds with an arrow are not full validated MCQs. A final student question is not publishable until all options, domain restrictions and scoring have been checked.
- **Misconception evidence:** wrong-answer archetypes are proposed, not empirical prevalence statistics.

## 9. Sources and provenance

**Uploaded project sources:**

1. *French_Math_Curriculum_Reference_EN_CLAUDE_v2.docx* (60 subdomain rows and original status notes; supplied 2026-10-19).
2. *PROMPT Diagnostic Maths Brevet Bac MPI_v3.md* (actual header calls itself `v2`; the filename and internal version do not match). Its 8 level families, prerequisites, MPI 20% rule, 16/3 default and 90% time ceiling governed the catalogue structure.

**Additional official checks for v5:**

- Cycle-4 mathematical proof and new programme rollout: https://www.education.gouv.fr/bo/2026/Hebdo10/MENE2602912A and https://www.education.gouv.fr/les-programmes-du-college-470408 (official guidance: demonstration is an essential goal).
- Terminale specialty 2026 annex (applies from school year 2027–2028): https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602919A (official annex: limits are treated via intuitive examples and eventual containment in intervals; the historical note refers to infinitesimal calculus; symbolic ∀/∃ are not required).

**Official programme/version references:** URLs in §2. **Editorial additions:** skills, worked candidates, misconception-candidate labels, prerequisite links, and remediation rules. **Not independently established:** individual item exigibility in every official programme, correctness of every source example and didactic prevalence of any listed misconception. These require validation before summative deployment.
