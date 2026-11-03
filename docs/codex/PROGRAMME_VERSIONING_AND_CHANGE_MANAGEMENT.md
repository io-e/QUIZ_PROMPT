# QUIZ_PROMPT — Curriculum edition selection and change management (proposal v1)

**Status:** architecture proposal, not a curriculum approval or a change to `io-e/QUIZ_PROMPT`.
**Scope:** every subject, year group, academic track and examination session; first concrete examples are French mathematics, physics–chemistry, Cycle 4 and lycée.
**Principle:** the shared Python engine resolves editions; YAML declares applicability and prompt rules; per-subject CSV is the canonical reference; Markdown is generated. The mathematics v11 package and Grok PR #2 remain unchanged until migration is reviewed.

## 1. Four independent version dimensions

Do **not** use the reference release number (e.g. v11) as a curriculum edition.

| Dimension | Example | Purpose |
|---|---|---|
| `engine_version` | `quiz_eval/1.0.0` | Python behavior and validators |
| `dataset_version` | `math-reference/v11`, later `math-reference/v12` | Stable IDs, skill/error content, signatures and data migrations |
| `programme_edition_id` | `MATH_C4_2020` versus `MATH_C4_2026` | Legally applicable subject syllabus by class and school year |
| `assessment_profile_id` | `DNB_MATH_2025` versus `DNB_MATH_2029` | Specific exam-session format, duration, allowed tools and grading |

Also record `prompt_version`, `codebook_version`, `source_revision` and source SHA-256. Examination **session** and **school year** are not interchangeable: an anticipated Première mathematics exam for baccalauréat session 2028 takes place in the 2026–2027 school year, whereas DNB session 2028 corresponds to a 3e pupil in 2027–2028. Verify dates in an independently versioned exam profile.

## 2. Model academic applicability per class, not per cycle alone

The 2026 mathematics Cycle 4 programme starts in **5e in 2026–2027**, **4e in 2027–2028** and **3e in 2028–2029** (BO 5 March 2026, article 3). Thus two editions coexist in different classes:

| Student's class | 2026–2027 | 2027–2028 | 2028–2029 |
|---|---|---|---|
| 5e | `MATH_C4_2026` | `MATH_C4_2026` | `MATH_C4_2026` |
| 4e | `MATH_C4_2020` | `MATH_C4_2026` | `MATH_C4_2026` |
| 3e (DNB) | `MATH_C4_2020` | `MATH_C4_2020` | `MATH_C4_2026` |

Verified source: https://www.education.gouv.fr/bo/2026/Hebdo10/MENE2602912A . The label `MATH_C4_2020` is the repository's stable identifier for the previous Cycle 4 programme version, not a claim that the full programme originally began in 2020.

Another example: Première speciality mathematics uses the 2026 edition beginning 2026–2027; Terminale speciality mathematics uses the 2026 edition beginning 2027–2028. They are different rollout dates and cannot be inferred from the education level alone. Sources: https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602917A and https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602919A . Physics–chemistry is independently versioned: Éduscol identifies the 2020 Cycle 4 programme as in force as of March 2026; do **not** automatically apply the 2026 mathematics rollout to physics–chemistry (https://eduscol.education.gouv.fr/5739/ressources-d-accompagnement-du-programme-de-physique-chimie-au-cycle-4).

For Seconde, Première intégré, Première spécialité, Terminale spécialité, Expertes, Complémentaires, MP2I, MPI, and any additional grade or speciality, create their **own** versioned applicability records from official texts. Unknown future validity must stay `UNVERIFIED`; never assume an open-ended period establishes indefinite legal applicability.

## 3. User selection: recent versus older exam

Support three explicit selection policies:

1. `CURRENT_FOR_COHORT`: input `subject + grade + track + school_year`; resolve the **one** edition applicable to that cohort. Reject zero or ambiguous matches.
2. `HISTORICAL_EXAM`: input `assessment + exam_session`; use a **versioned session-to-school-year exam profile**, then resolve the applicable programme and historical exam rules. Never apply today's exam rules to old papers.
3. `EXPLICIT_EDITION`: input `programme_edition_id`, school year, grade, track and reason. Allow a deliberate older-edition simulation even if that edition is not the cohort's current legal programme; label `HISTORICAL_SIMULATION`, never `CURRENT_PROGRAMME`. Default to no overrides in actual exam simulation or released assessment.

Examples:

| Request | Resolved syllabus | Exam profile |
|---|---|---|
| 3e in 2026–2027 | `MATH_C4_2020` | Selected separately |
| DNB mathematics session 2025 | `MATH_C4_2020` | `DNB_MATH_2025` (historical) |
| DNB mathematics session 2028 | `MATH_C4_2020` | `DNB_MATH_2028` (historical) |
| DNB mathematics session 2029 | `MATH_C4_2026` | `DNB_MATH_2029` |
| 5e in 2026–2027 | `MATH_C4_2026` | Not applicable |
| Première speciality maths in 2026–2027 | `MATH_1RE_SPE_2026` | First-year assessment profile separately |
| Terminale speciality maths in 2026–2027 | `MATH_TLE_SPE_2019` | Bac profile separately |

The attached example YAML gives only sample exam-profile dates, **not** authoritative historical exam rules. Official exam formats must be sourced separately before simulation. A user selecting 2020 when currently in 3e in 2028–2029 receives an explicit historical-simulation warning.

## 4. Replace binary BOTH/OLD/NEW with a many-to-many eligibility table

A single skill ID survives programme changes. Its *applicability* varies by edition. Create `reference/skill_programme_links.csv` per subject with one record per `skill_id × programme_edition_id × grade/track` and evidence state:

```csv
skill_id,programme_edition_id,grade,track,alignment_status,anchor_id,review_status,reviewer,review_date,change_reason
BR-DF-12,MATH_C4_2020,3e,general,NOT_SUPPORTED,ANCH-OLD-EXAMPLE,PENDING,,,
BR-DF-12,MATH_C4_2026,3e,general,SUPPORTED,ANCH-NEW-EXAMPLE,PENDING,,,
```

**These are illustrative records only**, reflecting the user's report that `BR-DF-12` is new-edition-specific; do not treat either fake `ANCH-...` identifier as a real citation. Real links need correct BO pages, passages and teacher approval. Use four curriculum alignment states: `SUPPORTED`, `PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, `UNVERIFIED`; keep separate reviewer approval (`PENDING`/`APPROVED`/`REJECTED`) and release eligibility (`PASS`/`HOLD`/`FAIL`). A Grok model's medium-confidence match stays `PENDING`.

For Grok's reported **95 Brevet rows**, capture independent per-edition links: 59 both, 16 new-only, 11 old-only, 9 unsupported in both (59+16+11+9=95). The 9 are reviewed first; they must not be deleted or silently forced into an edition. Possible actions after human review: `REANCHOR`, `PREREQUISITE`, `ENRICHMENT`, or `RETIRED_FROM_EXAM_SELECTION`. The 59 both-edition rows need **two distinct source reviews**, not a blanket BOTH approval. The string search mismatch `carré` versus `carreaux` shows why semantic/manual review is required.

## 5. Proposed repository layout

```text
QUIZ_PROMPT/
├── quiz_eval/                            # generic Python code ONLY
│   ├── programme_resolver.py              # resolves subject/class/year/edition/session
│   ├── reference_validator.py             # general structural and source checks
│   ├── release_gates.py                   # separate paper/digital gates
│   ├── migrations.py                      # stable-ID migration and history
│   └── adapters/                          # algebra, dimensions, chemistry, etc.
├── shared/
│   ├── config/programme_selection.schema.json
│   ├── prompts/diagnostic_base.yaml
│   └── tests/test_programme_selection.py
├── subjects/
│   ├── mathematics/
│   │   ├── programme/editions.yaml         # source facts + rollout by grade
│   │   ├── programme/exams.yaml            # separate examination sessions
│   │   ├── prompts/diagnostic.yaml
│   │   ├── reference/skills.csv
│   │   ├── reference/errors.csv
│   │   ├── reference/skill_programme_links.csv
│   │   ├── reference/anchors.csv
│   │   ├── reference/sources.csv
│   │   ├── reference/id_migrations.csv
│   │   └── reference/REFERENCE.md         # GENERATED: never edit manually
│   └── physics_chemistry/                 # same folders and schemas; own editions
├── test_runs/{subject}/{run_id}/
│   ├── request.yaml
│   ├── resolved_manifest.yaml             # immutable reproducibility record
│   ├── questions.yaml
│   ├── validation_report.json
│   └── source_review_report.csv
├── legacy/Math_Diagnostic_Reference_CLAUDE_v11/  # immutable until migration
└── .github/workflows/validate.yml
```

Use Python to load common YAML and subject YAML with explicit precedence; YAML never executes arbitrary expressions. Ensure deterministic generation: sort inputs, normalize float handling, pin adapter versions, and keep runtime/Python metadata OUTSIDE canonical generated Markdown.

## 6. Source / content / review / release lifecycle

**Every official change** follows this append-only procedure:

1. **Detect:** register new BO source, NOR, document revision, URL, effective date *per class/track*, original document checksum and consultation date. Do not overwrite a former edition or link.
2. **Diff:** report `ADDED`, `REMOVED`, `REWORDED`, `SCOPE_CHANGED`, `EXAM_FORMAT_CHANGED`, `UNCHANGED`, or `UNCERTAIN` at skill × edition level. Match on stable ID, not wording alone.
3. **Propose:** Grok produces source excerpts and `skill_programme_links` proposals in an independent PR branch; no writes to approved teacher registers.
4. **Review:** a teacher checks the **exact** BO passage/page, its applicability for that grade/session, and the lesson objective. Reviewer identity/date/source checksum required. Approvals for an older edition stay frozen; they DO NOT confer approval for the new edition.
5. **Validate:** shared structural, numeric/symbolic, science dimension and source checks; golden tests for v11; exam session resolver tests; stable-ID migration tests. Report unverified coverage explicitly.
6. **Pilot:** separate student-error hypothesis validation. An automatically generated distractor does not establish a misconception or a CONFIRMED evidence state.
7. **Release:** distinguish curriculum-supported, human-reviewed and overall paper/digital eligible statuses. Never upgrade all rows because a build passes. Digital requires real player-schema compatibility evidence.
8. **Freeze and archive:** versioned Git tag and immutable `resolved_manifest.yaml` containing selected programme and exam profile IDs, exact source/review SHA-256, dataset and prompt versions, codebook version and run ID. Historical exams keep resolving to their archived source set even when `main` changes.

Recommended release labels: `engine-vX.Y.Z`, `math-reference-vN`, `physics-reference-vN`, `programme-math-c4-2026-r1`, `exam-dnb-2025-r1`. Assign independent revisions; changing a prompt must not automatically relabel the programme.

## 7. Stable identifiers and migrations

- Preserve existing `BR-*`, `TS-*`, `1C-*`, `M1-*`, `M2-*` skill IDs and `-E*` error IDs. **Programme years are not part of skill identifiers.**
- Store aliases for old IDs; mark deletions as tombstones; never reuse retired or reserved IDs.
- A skill may split, merge or change meaning: add rows to `id_migrations.csv` with `from_id`, `to_id`, `operation`, `scope`, `valid_from_dataset`, `human_review`, `notes`; a split may require a **one-to-many** mapping and manual resolution of legacy student events.
- Keep student logs with `skill_id`, `programme_edition_id`, `assessment_profile_id`, `dataset_version`, `question_id`, `answer`, evidence, `date` and provenance. Old logs must not be rewritten to new editions.
- Reclassifying a skill from 2020-only to 2026-supported changes a link row, not the skill ID or its historical record.

## 8. Required shared regression tests

| Test | Expected result |
|---|---|
| Select 3e 2026–2027 | `MATH_C4_2020` |
| Select 3e 2028–2029 | `MATH_C4_2026` |
| Select 5e 2026–2027 | `MATH_C4_2026` |
| Select 4e 2026–2027 versus 2027–2028 | 2020 then 2026 |
| Select historical DNB 2025 versus DNB 2029 | 2020 then 2026 with distinct exam profiles |
| Select Première speciality 2026–2027 | 2026 edition |
| Select Terminale speciality 2026–2027 versus 2027–2028 | 2019 then 2026 |
| Select Physics–Chemistry 3e 2026–2027 | Independently resolved to 2020 edition, NOT maths 2026 |
| Give unsupported future year | `UNVERIFIED`, never silently use latest |
| Add a second applicable edition with same scope/period | `AMBIGUOUS_EDITION` and refuse assessment |
| Force older edition with no historical-mode declaration | Reject; require explicit historical labeling |
| Target supported only in 2026 requested for DNB 2025 | Exclude, or offer separately as an explicitly labeled enrichment item |
| Target among Grok's nine unsupported in both editions | Exclude from normal DNB selection, preserve for review |
| Review old edition only | New edition review stays PENDING |
| Changed BO passage checksum | New review required, historical approvals preserved |
| Rebuild older run from manifest | Same canonical questions, keys and codes; environment info only in report |

Also maintain the existing v11 regression and release gates (HOLD until reviews). **Do not merge draft PR #2 simply because all 95 Brevet rows have proposed edition labels.**

## 9. User-facing configuration and CLI contract

Sample learner request in `request.yaml`:

```yaml
subject: mathematics
grade: 3e
track: general
selection:
  policy: HISTORICAL_EXAM
  assessment: DNB_MATH
  exam_session: 2025
output:
  language: fr
  mode: EXAM_SIMULATION
```

The resolver emits immutable `resolved_manifest.yaml` with `school_year: 2024-2025`, `programme_edition_id: MATH_C4_2020`, `assessment_profile_id: DNB_MATH_2025`, and **separately verified** exam-format details. To choose the old programme for a student currently in 3e in 2028–2029, use `EXPLICIT_EDITION` and visibly label the assessment `HISTORICAL_SIMULATION`.

Proposed shared CLI (to be implemented by Grok; **not yet available in the current starter**):

```powershell
py -3 -m quiz_eval programme list --subject mathematics --grade 3e
py -3 -m quiz_eval programme resolve --request request.yaml
py -3 -m quiz_eval programme diff --subject mathematics --old MATH_C4_2020 --new MATH_C4_2026
py -3 -m quiz_eval validate --subject mathematics --edition MATH_C4_2020
py -3 -m quiz_eval release --subject mathematics --session 2025 --mode paper
```

## 10. PR policy and deliverables

- **PR A** shared resolver and version registry + tests; no change to mathematics v11 content.
- **PR B** migrate Brevet edition proposals from Grok's draft PR #2 into the canonical many-to-many link table, including a full 95-row, two-edition coverage audit and independent review worklist. Preserve the 59/16/11/9 partition as a **Grok-reported preliminary count**, not a certified fact.
- **PR C** extend registry to every class/track, mathematics and physics–chemistry; obtain source-verified effective dates per subject; compare per-edition links and plan the 301-ID history migration.
- **PR D** migrate the old math v11 runtime to shared Python **only after** golden-output parity, while retaining historical exports.

Each PR must include a complete changelog, impact matrix, reversible migration or rollback, CI evidence, unresolved rows and a declaration that structural PASS does not imply any assessment is release-ready.
