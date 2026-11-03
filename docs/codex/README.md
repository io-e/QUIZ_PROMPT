# Curriculum versioning / change management — for QUIZ_PROMPT

Proposal package; no GitHub PR is created, no registry or production release status has been modified.

- `PROGRAMME_VERSIONING_AND_CHANGE_MANAGEMENT.md`: versioning model, rollout by grade, historical Brevet selection, per-edition skill links, review gates, Git workflows, tests and CLI contract.
- `GROK_IMPLEMENTATION_PROMPT.md`: complete copy-and-send implementation prompt for Grok.
- `examples/programme_registry.yaml`: **illustrative bounded** curriculum edition and historical exam registry. Entries and format profiles are not teacher approved; no indefinite future applicability implied.
- `examples/selection_cases.yaml`: golden-test request/expected-edition matrix for the future generic Python resolver.

**Key selection:** Brevet session 2025 resolves `MATH_C4_2020`; session 2029 resolves `MATH_C4_2026` in the proposal, while separate exam format profiles require actual official verification.

Validation of the proposal: `python -c "import yaml; yaml.safe_load(open('examples/programme_registry.yaml')); yaml.safe_load(open('examples/selection_cases.yaml'))"` (PyYAML required). A proposed shared engine CLI appears in the specification, but it is **not implemented here**.
