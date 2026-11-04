# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

French mathematics **diagnostic evaluation** tooling (Alphavalon / Plücken School): a curriculum + error-code reference, an LLM generator prompt, and Python/PowerShell tooling that validates the reference. Every wrong MCQ option and every lost rubric point maps to one named error code, with an evidence state. Chat, docs, script comments and commits are **English**; generated student questionnaires are **French** by default (`{OUTPUT_LANGUAGE}`). English sources are canonical; French twins carry the `_FR` suffix.

**Release posture (v11): everything is `UNVALIDATED — HOLD`.** 594 rows `HOLD`, 6 `FAIL` (`1C-FN-05`…`10`), 0 `PASS`; 152 anchors `PROVISIONAL`, 6 `NOT_SUPPORTED`. A zero-blocking validator run is a structural pass only, not curriculum, maths or pedagogical approval. Never mark an item or package "validated".

## Current authority

- Reference: `Math_Diagnostic_Reference_CLAUDE_v11/French_Math_Diagnostic_Curriculum_Reference_CLAUDE_EN_v11.md`
- Prompt: `Math_Diagnostic_Reference_CLAUDE_v11/PROMPT_Diagnostic_Maths_Brevet_Bac_MPI_v9.md`. **The v10 prompt file is missing**; `GUIDE_Prompt_Usage_v10_EN.md` describes v10 additions that are unverified. Do not call the prompt v10.
- Rules: `AGENT_RULES_v11.md`, `README_v11.md` (same folder). Read before changing rows, IDs or gates.
- v7/v8 and the `ALF_Agents` workspace copies are historical. `00-00_archives/` (here and in the package) is read-only unless ALF asks.

## Commands

Windows, PowerShell 7, Python 3.10+ with SymPy. Use `py -3 -I` (isolated), never the Store `python` stub. Wrappers live in `Math_Diagnostic_Reference_CLAUDE_v11/programs/wrappers/`, Python in `programs/scripts/`, parameters in `programs/config/programs_v11.yaml` (JSON twin for `-I`).

```powershell
$root = '<repo>\Math_Diagnostic_Reference_CLAUDE_v11'
pwsh -NoProfile -File "$root\programs\wrappers\Invoke-ValidateReference.ps1"   # ~30 s; writes eligibility, gaps, report
pwsh -NoProfile -File "$root\programs\wrappers\Invoke-Tests.ps1"              # tests_v11.py, 21 scenarios
pwsh -NoProfile -File "$root\programs\wrappers\Invoke-Build.ps1"              # use --check semantics; never a bare rebuild
pwsh -NoProfile -File "$root\programs\wrappers\Invoke-AllChecks.ps1"          # or RUN_TESTS_V11.cmd
pwsh -NoProfile -File "$root\programs\wrappers\Invoke-MakePrompt.ps1" -ListScenarios
pwsh -NoProfile -File "$root\programs\wrappers\Invoke-MakePrompt.ps1" -Scenario premiere_spe_midyear -Full
```

Single regression scenario: call `programs/scripts/tests_v11.py` directly with `py -3 -I` (see its source for arguments). Test-package format validators are in `test_runs/01_BREVET/`: `validate_test_json.py`, `validate_test_xml.py`, `json_to_xml.py` (schemas in `xml_schemas/`).

## Architecture

```
Math_Diagnostic_Targets_v11.csv (600 rows)  -->  validate_reference_v11.py  -->  Item_Release_Eligibility_v11.csv
Item_Review_Register_v11.csv (human evidence) -^                                  Coverage_Gaps_v11.csv, validation_report_v11.*
                                                                                  
Reference .md + PROMPT v9 --(make_prompt_request_v11.py builds a paste-ready request)--> LLM --> test_runs/0N_*/ (JSON/XML/HTML)
```

- **Targets CSV** is the data core: one row per micro-skill with MCQ and open seeds, keys, `errors_json`, eligibility and anchor status. Levels present: `BREVET`, `BAC_1RE_COMMUN`, `BAC_1RE_SPE`, `BAC_TLE_SPE`, `BAC_TLE_EXPERTES`, `BAC_TLE_COMPLEMENTAIRES`, `MP2I`, `MPI`. **`BAC_2NDE` does not exist**; a `LEARNER_PROFILE` such as "incoming 2nde" is not a catalogue level. Do not invent Seconde rows, IDs or anchors; propose a separately reviewed extension from an official source first.
- **Validator + `chk_*.py`** recompute signatures on each item's own numbers (SymPy). `build_v11.py` regenerates reference files from `build/inputs_v10`; generated files must be deterministic (no runtime info; that goes only in the JSON report).
- **Programs do not generate assessments.** Full questionnaires come from the LLM + prompt workflow; programs only validate, regress, build, dashboard, demo and prepare prompt requests.
- **Test packages** (`test_runs/01_BREVET` … `05_MPI`) hold `SOURCE`, `ANSWER_KEY`, student `TEST*.html`, `PROFESSEUR*.html`, coverage and validation reports; JSON/XML checks are structural only.

## Rules that span files

- **R1, one seed per signature:** compare `sig_mcq` only with the MCQ seed/key and `sig_open` only with the open seed/target; record `mode` and `seed_used`. Never report cross-seed mismatches.
- MCQs only from rows with `allowed_items = MCQ+OPEN`; `OPEN_ONLY` rows give open items only. Never pad options with `LOCAL`/unrelated codes.
- IDs keep their meaning forever; never reuse retired IDs (`BR-AP-01-E3` merged into `-E1`). `SUBDOMAIN-F\d\d` / `-S\d\d` are reserved for CODEX v5. Resolve legacy IDs through `Math_ID_Migration_to_v11.csv`.
- A `PASS` row needs dated (`YYYY-MM-DD`) evidence in `Item_Review_Register_v11.csv`: BO page and passage, teacher reviewer, text-signature review, pilot evidence. Calculation gaps are listed in `Coverage_Gaps_v11.csv`.
- Every signature is a hypothesis; wrong MCQ options are `SUSPECTED` evidence, never `CONFIRMED` without data. No masking or collision between error values unless declared (`ambiguous_with`, `form_distinct`, evidence `UNDETERMINED`).
- Compare floats with a stated tolerance; keep symbolic values exact.
- Do not invent BO citations, DEPP rates, tool features or research; mark `[TO VERIFY]`.
- If `{LEVEL}` is missing or invalid, stop and ask. Default blueprint under 55 min: 12 MCQ + 3 open (Σ time ≤ 90 % of `{DURATION}`). `MPI` requires ≥ 20 % items with `M1-*` prerequisite codes. Player format is `alphavalon.eval/v1`.
- Versioned Markdown (`_v9`, `_v11`, …) is never overwritten: create the next version and update the header. Exceptions only on explicit ALF instruction.
- Do not commit, push, publish or regenerate ZIP/RAR exports unless ALF asks.
