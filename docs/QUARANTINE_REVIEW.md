# QUARANTINE review: 18 links (9 Brevet skills x 2 editions), Grok PROPOSALS ONLY

Roles: **Grok proposes, Python verifies structure, a qualified teacher approves.** Every link stays `QUARANTINE` / `approval=PENDING` until a teacher fills `decision_1` (and `decision_2` when `needs_second_review=YES`). Every ID is kept. Each link was reviewed against its own edition only; no skill is rejected for both editions.

Sources: 2020 edition = Éduscol cycle 4 PDF (https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf); 2026 edition = BO n°10 2026, annexe 2 (https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf). The page is the PDF page. Passages were checked verbatim against `pdftotext -layout` output (`python3 tools/build_quarantine_review.py --verify DIR`). 'Not found' means the terms were searched (case/accent-insensitive) in the whole maths text without a hit.

Grade headings in the 2026 text (Cinquième / Quatrième / Troisième) were attributed from the page layout. A reviewer should confirm them.

| Decision | Count |
|---|---|
| NOT_SUPPORTED | 1 |
| PARTIALLY_SUPPORTED | 10 |
| SUPPORTED | 7 |
| needs_second_review=YES | 16 |

## BR-DF-02@MATH_C4_2020 – interpret a graph, frequency table and probability (BR.DF.4)

- **Grok proposal:** SUPPORTED (confidence medium); if unsupported: -; second review: YES
- **Source:** https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf – PDF p.133; PDF p.133; PDF p.133
- **Passages found:** [p.133] - Lire et interpréter des données sous forme de données brutes, de tableau, de diagramme || [p.133] - Calculer des effectifs, des fréquences. || [p.133] - Faire le lien entre fréquence et probabilité.
- **Not found:** -
- **Rationale:** All three parts (graph/table reading, frequencies, probability) appear in the 2020 attendus; the PR #2 audit had found no 2020 passage, so this is a new finding to confirm.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-DF-02@MATH_C4_2026 – interpret a graph, frequency table and probability (BR.DF.4)

- **Grok proposal:** SUPPORTED (confidence medium); if unsupported: -; second review: YES
- **Source:** https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf – PDF p.16; PDF p.18
- **Passages found:** [p.16] Lire et interpréter des informations présentées sous forme de tableaux, de diagrammes et de graphiques. || [p.18] Observer la stabilisation des fréquences lorsqu’on augmente le nombre de répétitions de l’expérience aléatoire, faire le lien
- **Not found:** -
- **Rationale:** Covered across 5e (reading tables/graphs, p.16) and 3e (frequency-probability link, p.18). Composite skill: the teacher should confirm the combination.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-DF-12@MATH_C4_2020 – compute a probability for a two-stage experiment with a tree (BR.DF.4)

- **Grok proposal:** PARTIALLY_SUPPORTED (confidence low); if unsupported: ENRICHMENT; second review: YES
- **Source:** https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf – PDF p.133
- **Passages found:** [p.133] - Calculer des probabilités dans des cas simples (par exemple évaluation des chances de
- **Not found:** deux épreuves; arbre
- **Rationale:** The 2020 text only says 'cas simples'; two-stage experiments and trees are not named in the programme text.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-DF-12@MATH_C4_2026 – compute a probability for a two-stage experiment with a tree (BR.DF.4)

- **Grok proposal:** PARTIALLY_SUPPORTED (confidence medium); if unsupported: PREREQUISITE; second review: YES
- **Source:** https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf – PDF p.17; PDF p.18
- **Passages found:** [p.17] Exemples simples d’expériences aléatoires à deux épreuves (par exemple, lancer de deux pièces, d’une pièce et d’un dé, de || [p.18] Simuler des expériences aléatoires indépendantes.
- **Not found:** arbre
- **Rationale:** Two-stage experiments are explicit (4e) but a tree diagram is not named. DNB 2029+ (MENE2623228N): subjects bear on the programme de la classe de troisième if in force; this passage sits under the Quatrième heading, so for 3e-only exam selection it would be PREREQUISITE.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-DF-13@MATH_C4_2020 – use the complementary event (BR.DF.4)

- **Grok proposal:** SUPPORTED (confidence high); if unsupported: -; second review: NO
- **Source:** https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf – PDF p.133
- **Passages found:** [p.133] - Probabilité d’événements certains, impossibles, contraires.
- **Not found:** -
- **Rationale:** Explicit: 'événements ... contraires'.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-DF-13@MATH_C4_2026 – use the complementary event (BR.DF.4)

- **Grok proposal:** SUPPORTED (confidence high); if unsupported: PREREQUISITE; second review: YES
- **Source:** https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf – PDF p.17
- **Passages found:** [p.17] Calculer la probabilité d’un évènement et de l’évènement contraire.
- **Not found:** -
- **Rationale:** Explicit, but taught in 4e. DNB 2029+ (MENE2623228N): subjects bear on the programme de la classe de troisième if in force; this passage sits under the Quatrième heading, so for 3e-only exam selection it would be PREREQUISITE.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-DF-14@MATH_C4_2020 – relate the stabilisation of frequencies to a probability (BR.DF.5)

- **Grok proposal:** PARTIALLY_SUPPORTED (confidence medium); if unsupported: ENRICHMENT; second review: YES
- **Source:** https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf – PDF p.133
- **Passages found:** [p.133] - Faire le lien entre fréquence et probabilité.
- **Not found:** stabilisation
- **Rationale:** The frequency-probability link is explicit; 'stabilisation' is not named in the 2020 text.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-DF-14@MATH_C4_2026 – relate the stabilisation of frequencies to a probability (BR.DF.5)

- **Grok proposal:** SUPPORTED (confidence high); if unsupported: -; second review: NO
- **Source:** https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf – PDF p.18; PDF p.16
- **Passages found:** [p.18] Observer la stabilisation des fréquences lorsqu’on augmente le nombre de répétitions de l’expérience aléatoire, faire le lien || [p.16] à la naissance) en s’appuyant sur l’idée de stabilisation des fréquences (loi des grands nombres).
- **Not found:** -
- **Rationale:** Explicit 3e objective.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-DF-21@MATH_C4_2020 – solve f(x) = g(x) by calculation and on a graph (BR.DF.9;BR.DF.12)

- **Grok proposal:** PARTIALLY_SUPPORTED (confidence low); if unsupported: ENRICHMENT; second review: YES
- **Source:** https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf – PDF p.132; PDF p.134; PDF p.134
- **Passages found:** [p.132] - Résoudre algébriquement des équations du premier degré ou s’y ramenant (équations || [p.134] - Passer d’un mode de représentation d’une fonction à un autre. || [p.134] - Représenter graphiquement une fonction linéaire, une fonction affine.
- **Not found:** résoudre graphiquement; f(x) = g(x)
- **Rationale:** The algebraic part is explicit; graphical solving of f(x)=g(x) is not named.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-DF-21@MATH_C4_2026 – solve f(x) = g(x) by calculation and on a graph (BR.DF.9;BR.DF.12)

- **Grok proposal:** PARTIALLY_SUPPORTED (confidence medium); if unsupported: ENRICHMENT; second review: YES
- **Source:** https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf – PDF p.10; PDF p.20
- **Passages found:** [p.10] Mettre en équation un problème et le résoudre à l’aide d’une équation du premier degré du type a𝑥 + b = c𝑥 + d. || [p.20] Résoudre graphiquement des équations et des inéquations linéaires.
- **Not found:** f(x) = g(x) for non-affine f, g
- **Rationale:** SUPPORTED if f and g are restricted to affine functions (3e p.20 graphical solving, 4e p.10 ax+b=cx+d); not supported for general f, g.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-GM-04@MATH_C4_2020 – model speed, density and energy units (BR.GM.2)

- **Grok proposal:** PARTIALLY_SUPPORTED (confidence medium); if unsupported: ENRICHMENT; second review: YES
- **Source:** https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf – PDF p.135; PDF p.135; PDF p.134
- **Passages found:** [p.135] - Notion de grandeur produit et de grandeur quotient. || [p.135] - Mener des calculs impliquant des grandeurs mesurables, notamment des grandeurs || [p.134] en fonction de l’intensité, la distance parcourue en fonction du temps à vitesse constante,
- **Not found:** masse volumique; énergie
- **Rationale:** Compound quantities and speed are explicit; density and energy units are not named in the maths text (they may come from physics).
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-GM-04@MATH_C4_2026 – model speed, density and energy units (BR.GM.2)

- **Grok proposal:** PARTIALLY_SUPPORTED (confidence low); if unsupported: ENRICHMENT; second review: YES
- **Source:** https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf – PDF p.19; PDF p.18
- **Passages found:** [p.19] Utiliser des grandeurs quotients, avec ou sans unités. || [p.18] Utiliser un coefficient de proportionnalité dans des contextes concrets (prix unitaire, vitesse moyenne, échelle, etc.).
- **Not found:** grandeur produit; masse volumique; énergie
- **Rationale:** Only quotient quantities (4e) and average speed (5e) are named; there are no product quantities and no energy. The energy part is a candidate for ENRICHMENT. DNB 2029+ (MENE2623228N): subjects bear on the programme de la classe de troisième if in force; this passage sits under the Quatrième heading, so for 3e-only exam selection it would be PREREQUISITE.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-GM-08@MATH_C4_2020 – convert between decimal hours and hours–minutes (BR.GM.2)

- **Grok proposal:** PARTIALLY_SUPPORTED (confidence low); if unsupported: PREREQUISITE; second review: YES
- **Source:** https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf – PDF p.135
- **Passages found:** [p.135] - Effectuer des conversions d’unités.
- **Not found:** heure; minute; durée
- **Rationale:** Only a generic unit-conversion objective; time conversion is not named.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-GM-08@MATH_C4_2026 – convert between decimal hours and hours–minutes (BR.GM.2)

- **Grok proposal:** NOT_SUPPORTED (confidence medium); if unsupported: PREREQUISITE; second review: YES
- **Source:** https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf – -
- **Passages found:** NOT FOUND
- **Not found:** heure; minute; durée; conversions de durées (p.13 names only longueur and aires)
- **Rationale:** No passage on durations was found in annexe 2. Proposed as PREREQUISITE (assumed cycle 3 content; the cycle 3 text was NOT checked).
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-GM-09@MATH_C4_2020 – use a compound quantity (flow rate or density) (BR.GM.2)

- **Grok proposal:** SUPPORTED (confidence medium); if unsupported: -; second review: YES
- **Source:** https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf – PDF p.135; PDF p.135
- **Passages found:** [p.135] - Mener des calculs impliquant des grandeurs mesurables, notamment des grandeurs || [p.135] - Notion de grandeur produit et de grandeur quotient.
- **Not found:** débit; masse volumique
- **Rationale:** 'grandeurs composées' covers flow rate and density, but neither is named.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-GM-09@MATH_C4_2026 – use a compound quantity (flow rate or density) (BR.GM.2)

- **Grok proposal:** PARTIALLY_SUPPORTED (confidence medium); if unsupported: PREREQUISITE; second review: YES
- **Source:** https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf – PDF p.19
- **Passages found:** [p.19] Utiliser des grandeurs quotients, avec ou sans unités.
- **Not found:** débit; masse volumique
- **Rationale:** Flow rate and density are quotient quantities but are not named. DNB 2029+ (MENE2623228N): subjects bear on the programme de la classe de troisième if in force; this passage sits under the Quatrième heading, so for 3e-only exam selection it would be PREREQUISITE.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-GM-11@MATH_C4_2020 – convert speeds between km/h and m/s (BR.GM.2)

- **Grok proposal:** SUPPORTED (confidence medium); if unsupported: -; second review: YES
- **Source:** https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf – PDF p.135; PDF p.135
- **Passages found:** [p.135] - Effectuer des conversions d’unités. || [p.135] - Vérifier la cohérence des résultats du point de vue des unités.
- **Not found:** km/h; m/s
- **Rationale:** Conversions of compound units fall under 'grandeurs composées' + 'conversions d’unités'; the speed units are not named.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____

## BR-GM-11@MATH_C4_2026 – convert speeds between km/h and m/s (BR.GM.2)

- **Grok proposal:** PARTIALLY_SUPPORTED (confidence low); if unsupported: ENRICHMENT; second review: YES
- **Source:** https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf – PDF p.19; PDF p.6
- **Passages found:** [p.19] Utiliser des grandeurs quotients, avec ou sans unités. || [p.6] puissances de dix de nano à giga. On fait le lien avec les conversions.
- **Not found:** km/h; m/s; conversion of compound units
- **Rationale:** No explicit conversion of compound units; p.13 conversions cover length and area only.
- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____
