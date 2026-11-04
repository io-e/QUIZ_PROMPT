# referentiel/

This folder is the **local documentation anchor** for the curriculum data root.

By default, `programs/config/programs_v11.yaml` sets:

```yaml
paths:
  referentiel: ".."
```

so the live data files stay in the parent package:

- `French_Math_Diagnostic_Curriculum_Reference_CLAUDE_EN_v11.md`
- `Math_Diagnostic_Targets_v11.csv`
- `Item_Release_Eligibility_v11.csv`
- `PROMPT_Diagnostic_Maths_Brevet_Bac_MPI_v9.md`
- `build/`, registers, indexes, …

To point the tools at another tree (for example a copied snapshot), set `paths.referentiel` to that folder, or set the environment variable `EA_EVAL_REFERENTIEL` before running a wrapper.

Do not delete the parent package files while `referentiel: ".."` is in force.