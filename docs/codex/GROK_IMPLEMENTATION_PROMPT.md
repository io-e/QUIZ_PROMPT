# Grok implementation prompt — curriculum change management for all classes

You are maintaining the existing `io-e/QUIZ_PROMPT` GitHub repository. Your task is to make **all subjects, school years, class tracks, historical programmes, and examination sessions selectable and reproducible**, without duplicating Python code between mathematics and physics–chemistry. Work in a draft PR, not in `main`.

## Inputs / source of truth

1. Inspect `main` and **draft PR #2** (`https://github.com/io-e/QUIZ_PROMPT/pull/2`). Do not assume its 600 curriculum anchors are teacher-approved.
2. Read `PROGRAMME_VERSIONING_AND_CHANGE_MANAGEMENT.md` and the sample `programme_registry.yaml` and `selection_cases.yaml`. Treat these as **proposed architecture**, not as completed programme review or official exam-format records.
3. Keep the existing mathematics v11 package, regression checks, review register and historical student error IDs unchanged until golden regression parity is established.
4. Verify every enacted official BO/Éduscol programme and its entry-into-force schedule for each **subject × grade × track × school year**. Distinguish programme edition, reference/dataset version, prompt version and examination format/session. Do not derive all subjects' rules from 2026 mathematics reforms.

## Required architecture

- Shared, subject-agnostic Python modules under `quiz_eval/`: `programme_resolver`, `programme_diff`, `release_gates`, `id_migrations`, `validation`, `manifest`.
- Registry entries and prompt configuration in **YAML**, with JSON Schema validation and explicit Python merge rules. Each subject owns `subjects/<subject>/programme/editions.yaml` and `exams.yaml` and its own `prompts/diagnostic.yaml`.
- Canonical curriculum tables per subject: `skills.csv`, `errors.csv`, `sources.csv`, `anchors.csv`, `skill_programme_links.csv`, `id_migrations.csv` and reviewer registers. Generated `REFERENCE.md` must never be edited by hand.
- Each skill remains identified by its **stable pedagogical ID**, never by replacing that ID when the programme changes. A many-to-many table records whether the skill belongs to an edition; archive previous edition approvals.
- Source URL alone is not a verified official anchor; include official NOR/version, page/section, exact passage, source checksum, reviewer and date. Separate `alignment_status`, `review_status`, `release_status` and `pilot_evidence_status`.
- The selected programme must be recorded inside every test run's immutable `resolved_manifest.yaml`, together with exam profile, subject/grade/track/year, skill dataset, codebook, prompt, engine and source checksums.

## Selection behavior (mandatory)

Implement **three modes**:

1. `CURRENT_FOR_COHORT(subject, grade, track, school_year)`: automatic legally applicable programme for the class that year.
2. `HISTORICAL_EXAM(assessment, exam_session)`: load an archived exam-specific profile (including its historical format and original student school year) before resolving the programme. A 2025 Brevet uses the earlier Cycle 4 edition and 2025 exam rules, not the current DNB rules.
3. `EXPLICIT_EDITION(programme_edition_id, ...)`: allow users to select an older edition to practise, with a conspicuous `HISTORICAL_SIMULATION` label; never falsely claim this is their current applicable programme.

Do not infer examination session from school year with a single universal offset. For instance, the Première anticipatory exam for session 2028 is taken in the school year 2026–2027; the DNB session 2028 is in 2027–2028. Source and version the mapping separately.

Reject zero matches, overlapping active editions, unknown grades/tracks, undefined exam-format profiles, unsupported requested programme editions, and unsupported future years. Offer an explicit draft/research-only mode without release authorization.

## Grok PR #2: convert edition research into governed data

The reported initial partition of **95 Brevet skill rows** is:

- 59 applicable to both `MATH_C4_2020` and `MATH_C4_2026`;
- 16 applicable only to `MATH_C4_2026`;
- 11 applicable only to `MATH_C4_2020`;
- 9 apparently supported by neither version (inspect first; do not delete).

Treat these as **Grok-proposed classifications pending human approval**, not validated truth. `BR-DF-12` is a proposed new-only skill; the earlier `carré`/`carreaux` automatic-match error demonstrates why lexical matching alone is not proof.

Create **per-edition** anchor and review records: one approved 2020 link must not automatically approve the 2026 link. For the nine unsupported rows, propose `REANCHOR`, `PREREQUISITE`, `ENRICHMENT`, or `RETIRED_FROM_EXAM_SELECTION`, with an official passage or explicit absence finding. Do not delete historic IDs or write directly to the existing teacher review register.

## Apply to every class and discipline

Design a registry that can support 5e, 4e, 3e, Seconde, Première (separate speciality, integrated/common, technical tracks), Terminale (speciality, expertes, complémentaires and other tracks), MP2I, MPI, and any subsequently introduced class or option without Python modifications. Mathematics and physics–chemistry maintain **independent effective dates**. CPGE rules are not automatically linked to DNB/Bac reforms. Require an explicit review of any year not yet registered.

## Change-management workflow

On a new BO:

1. Register source and effective date per class/track; never overwrite old edition.
2. Generate the `old ↔ new` per-skill comparison (`ADDED`, `REMOVED`, `REWORDED`, `SCOPE_CHANGED`, `EXAM_FORMAT_CHANGED`, `UNCERTAIN`).
3. Write new candidate edition links to a draft PR; preserve stable IDs and review history.
4. Get teacher approval of source page/passage and all text/numeric keys, separately per edition.
5. Execute structural, curricular, symbolic/numeric, error-code, migration and session-routing regression tests.
6. Collect real pilot evidence for student errors; do not promote authored error hypotheses to confirmed causes automatically.
7. Require independent paper/digital release gates; digital schema compatibility must be demonstrated, not assumed.
8. Freeze approved releases as tagged Git commits and immutable manifests, with rollback and historical replay support.

## Required tests

Use `selection_cases.yaml` and add failure tests. Must cover:

- 5e 2026–2027 → mathematics Cycle 4 2026; 4e 2026–2027 → 2020, then 4e 2027–2028 → 2026; 3e 2027–2028 → 2020 and 3e 2028–2029 → 2026.
- DNB mathematics 2025 → 2020 programme + 2025 exam profile; DNB 2029 → 2026 programme + 2029 exam profile; independently validate historical format rules before actual assessment generation.
- Première speciality mathematics 2026–2027 → 2026 programme; Terminale speciality maths 2026–2027 → 2019, then 2027–2028 → 2026.
- Physics–chemistry Cycle 4 2026–2027 → its own 2020 programme, not maths 2026.
- Distinguish `SUPPORTED/PARTIALLY_SUPPORTED/NOT_SUPPORTED/UNVERIFIED`, teacher approval, error-pattern validity and paper/digital release; no automatic pass from an official link or structural zero.
- Two active editions matching the same scope/year → error; missing known historical profile → error; unsupported future year → fail closed; explicit older-edition override → historical label.
- 59/16/11/9 audit totals 95; every edition link independently reviewed; nine unsupported remain out of normal assessment selection.
- Legacy student logs and CODEX v5 301-ID migrations remain resolvable and immutable.
- v11 build/validation outputs match previous golden results before replacing any old Python script.

## Deliverables and acceptance criteria

Deliver the new repository tree, YAML/CSV schemas, shared CLI, edition-selection engine, historical exam profile registry, migrations, generated Markdown, source-to-skill impact diff, source review worklist, failure-mode tests, GitHub Actions CI and a report identifying all HOLD items. Include an explicit README walkthrough for selecting a 2025 Brevet versus a 2029 Brevet, and a per-class / per-subject example.

**Do not merge PR #2 or release exam content without teacher review. Do not change the meaning of existing IDs, overwrite history, delete unsupported skills, alter `Item_Review_Register_v11.csv`, or claim that 0 structural blockers implies pedagogical release.**

Return all explanations and technical documentation in English. French student-facing assessments only when selected by the user or subject configuration.
