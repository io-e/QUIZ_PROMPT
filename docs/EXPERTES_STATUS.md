# Mathématiques expertes: current-status handling

- **Edition kept:** `MATH_TLE_EXP_2019` (MENE1921264A, BO spécial n°8 of 25 July 2019). Article 2: "Les dispositions du présent arrêté entrent en vigueur à la rentrée scolaire 2020". So it applies **from 2020-2021** (VERIFIED).
- **After 2026-2027:** `through_year = REQUIRES_CURRENT_STATUS_VERIFICATION`. This is **not an end date and not a replacement**. The last verified year is `verified_through_year = 2026-2027`.
- **Why:** BO n°14 (April 2026) published new Terminale programmes for mathématiques de spécialité and mathématiques complémentaires (from 2027-2028), with **no replacement for mathématiques expertes**. That is what I found, and the user's check on 2026-11-03 confirms it.
- **Resolver behaviour:**
  - For `Tle / expertes` from 2027-2028 onward, the resolver returns `MATH_TLE_EXP_2019`, with `verification = REQUIRES_CURRENT_STATUS_VERIFICATION` and a visible entry in `warnings`.
  - It never returns `MATH_TLE_SPE_2026`.
  - Validated tests are refused (`UNVERIFIED_EDITION_FOR_VALIDATED_TEST`).
  - Draft tests stay possible, and the warning is printed in their manifest.
- **Tests:** `tests/test_expertes.py`.
- **To close:** find an official text confirming the status of the expertes programme for 2027-2028. It could be a repeal, a new programme, or an explicit confirmation. Then register it with `programme_diff.register_edition` or set a verified bound.
