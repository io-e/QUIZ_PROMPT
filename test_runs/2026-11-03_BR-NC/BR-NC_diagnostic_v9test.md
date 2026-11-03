# Diagnostic de mathématiques — Brevet · Nombres et calculs (BR-NC)

> **STATUT : NON VALIDÉ — HOLD (papier et numérique).** Version de test du prompt v9 / référence v11. Ne pas utiliser pour évaluer des élèves.

## Version élève

Niveau : 3e (Brevet) · Durée : 30 min · **Calculatrice non autorisée**

Si tu ne sais pas, coche "Je ne sais pas" : ça ne te retire rien et ça aide ton professeur.
Après chaque réponse, coche "Sûr" ou "Pas sûr".

### Partie A — QCM (une seule bonne réponse)

**1.** Calculer : −3/4 + 1/2. Donner le résultat sous forme de fraction irréductible.

- A. −1/3
- B. −1/4
- C. 5/4
- D. −5/4
- E. Je ne sais pas

☐ Sûr ☐ Pas sûr

**2.** Calculer : −7 + 3 − (−5)

- A. −5
- B. −9
- C. 9
- D. 1
- E. Je ne sais pas

☐ Sûr ☐ Pas sûr

**3.** Calculer : 2/3 − 1/4. Donner le résultat sous forme de fraction irréductible.

- A. 5/12
- B. −1
- C. 1/12
- D. 1/6
- E. Je ne sais pas

☐ Sûr ☐ Pas sûr

**4.** Développer et réduire : 5 − 3(2x − 4)

- A. −7 − 6x
- B. 1 − 6x
- C. 17 − 6x
- D. 4x − 8
- E. Je ne sais pas

☐ Sûr ☐ Pas sûr

**5.** Résoudre l’équation : 5x − 7 = 2x + 8

- A. x = 1/3
- B. x = 5
- C. x = 12
- D. x = 15/7
- E. Je ne sais pas

☐ Sûr ☐ Pas sûr

### Partie B — Questions ouvertes

**6.** On considère l’équation 9x² − 25 = 0.
- a) Factoriser 9x² − 25.
- b) En déduire les solutions de l’équation. Énoncer la règle utilisée.
- c) Léa a écrit : « 9x² − 25 = (3x − 5)², donc la seule solution est x = 5/3. » Trouve son ou ses erreurs et explique-les.

*(Espace de réponse : 10 lignes)*

**7.** On cherche les nombres x tels que 2x + 3 ≤ 11.
- a) Résoudre cette inéquation.
- b) Écrire l’ensemble des solutions sous forme d’intervalle.
- c) Vérifier avec x = 4.

*(Espace de réponse : 8 lignes)*

---

## Version enseignant

> ⚠️ **HOLD — aucun item n’est validé.** Les 7 lignes utilisées sont `eligibility_paper = HOLD`, `eligibility_digital = HOLD` dans `Item_Release_Eligibility_v11.csv` (curriculum non revu, relecture enseignant PENDING, pas de données pilotes, schéma player non vérifié). Tous les codes d’erreur sont des **hypothèses** (preuve `SUSPECTED` au mieux).

Paramètres : LEVEL = BREVET · SUBJECT = BR-NC · PURPOSE = Entry diagnostic · MODE = DIAGNOSTIC · NB_MCQ/NB_OPEN = 5/2 (version courte) · DURATION = 30 min · CALCULATOR = non · DELIVERY = Paper · OPTIONS = NSP, CONFIDENCE · OUTPUT = MARKDOWN.

### T1 — Sources
| Source | Version | Consultation |
|---|---|---|
| French_Math_Diagnostic_Curriculum_Reference_CLAUDE_EN_v11.md + Math_Diagnostic_Targets_v11.csv + Item_Release_Eligibility_v11.csv | v11 (kit local) | 2026-11-03 |
| Programme de cycle 4 (BO) | [TO VERIFY] — non consulté dans ce test | — |

### T2 — Benchmark d’outils
Non réalisé dans ce test court (aucun outil documenté consulté) — [TO VERIFY].

### T3 — Carte des compétences
| Code | Micro-compétence | Ancre officielle | Statut d’ancre | Difficulté | Items autorisés | Éligibilité papier/num. |
|---|---|---|---|---|---|---|
| BR-NC-01 | calculate with signed fractions and decimals | BR.NC.2 | SOURCE_LINKED | D1 | MCQ+OPEN | HOLD/HOLD |
| BR-NC-06 | add and subtract signed numbers | BR.NC.2 | SOURCE_LINKED | D1 | MCQ+OPEN | HOLD/HOLD |
| BR-NC-10 | add and subtract fractions with different denominators | BR.NC.1 | SOURCE_LINKED | D1 | MCQ+OPEN | HOLD/HOLD |
| BR-NC-22 | expand with a single distribution and reduce | BR.NC.7 | SOURCE_LINKED | D1 | MCQ+OPEN | HOLD/HOLD |
| BR-NC-26 | solve a first-degree equation with x on both sides | BR.NC.9 | SOURCE_LINKED | D1 | MCQ+OPEN | HOLD/HOLD |
| BR-NC-04 | expand and factor elementary expressions | BR.NC.8 | SOURCE_LINKED | D2 | MCQ+OPEN | HOLD/HOLD |
| BR-NC-05 | solve first-degree equations, inequalities and zero products | BR.NC.9;BR.NC.10 | SOURCE_LINKED | D3 | MCQ+OPEN | HOLD/HOLD |

### T4/T6 — Clés des QCM et banque d’erreurs (graine MCQ, règle R1)
| Item | Ligne | Clé | Option → code → pourquoi | Tags transversaux |
|---|---|---|---|---|
| 1 | BR-NC-01 | **B** (−1/4) | A. −1/3 → `BR-NC-01-E1` → A additionné numérateurs et dénominateurs : (−3+1)/(4+2).<br>C. 5/4 → `BR-NC-01-E2` → A ignoré le signe moins de −3/4.<br>D. −5/4 → `BR-NC-01-E3` → A additionné les valeurs absolues en gardant le signe moins. | CB-FRA-01; CB-SGN-07; CB-SGN-07 |
| 2 | BR-NC-06 | **D** (1) | A. −5 → `BR-NC-06-E1` → A additionné les valeurs absolues de −7 et 3 en gardant le signe moins.<br>B. −9 → `BR-NC-06-E2` → A traité « − (−5) » comme « − 5 ».<br>C. 9 → `BR-NC-06-E3` → A perdu le signe de −7 + 3. | CB-SGN-07; CB-SGN-02; CB-SGN-07 |
| 3 | BR-NC-10 | **A** (5/12) | B. −1 → `BR-NC-10-E1` → A soustrait numérateurs et dénominateurs.<br>C. 1/12 → `BR-NC-10-E2` → A pris 12 comme dénominateur commun sans convertir les numérateurs.<br>D. 1/6 → `BR-NC-10-E3` → A appliqué la règle du produit à la différence. | CB-FRA-01; CB-FRA-12; CB-FRA-13 |
| 4 | BR-NC-22 | **C** (17 − 6x) | A. −7 − 6x → `BR-NC-22-E1` → N’a pas appliqué le signe moins au second terme de la parenthèse.<br>B. 1 − 6x → `BR-NC-22-E2` → A multiplié seulement le premier terme par 3.<br>D. 4x − 8 → `BR-NC-22-E3` → A calculé 5 − 3 d’abord. | CB-SGN-03; CB-PAR-02; CB-PAR-01 |
| 5 | BR-NC-26 | **B** (x = 5) | A. x = 1/3 → `BR-NC-26-E1` → A déplacé −7 sans changer son signe.<br>C. x = 12 → `BR-NC-26-E2` → A confondu opposé et inverse (3x = 15 ⇒ x = 12).<br>D. x = 15/7 → `BR-NC-26-E3` → A déplacé 2x sans changer son signe. | CB-SGN-05; CB-EQ-01; CB-SGN-05 |

Positions des clés : B, D, A, C, B → B = 40 % (≤ 40 %). Temps QCM : 5 min.

### T7 — Solutions des questions ouvertes
**6 (BR-NC-04, D2, 8 min, ancre BR.NC.8, SOURCE_LINKED)** — FIND_ERROR inclus.
- a) 9x² − 25 = (3x)² − 5² = (3x − 5)(3x + 5).
- b) Un produit est nul si et seulement si l’un de ses facteurs est nul : 3x − 5 = 0 ou 3x + 5 = 0, donc x = 5/3 ou x = −5/3.
- c) Erreur 1 : a² − b² écrit (a − b)² ; erreur 2 : une seule solution retenue.

| Critère | Points | Code si perdu |
|---|---|---|
| Factorisation correcte | 1 | BR-NC-04-E4 (signature recalculée sur les nombres ouverts : (3x − 5)²) / BR-NC-04-E1 |
| Règle du produit nul énoncée | 1 | BR-NC-04-E3 |
| Deux solutions ±5/3 | 1 | BR-NC-04-E3 (graine ouverte : « x = 5/3 only ») |
| Erreurs de Léa identifiées | 1 | BR-NC-04-E4 |
Total : 4 points. Re-test : résoudre 4x² − 49 = 0 (x = ±7/2).

**7 (BR-NC-05, D3, 12 min, ancres BR.NC.9 ; BR.NC.10, SOURCE_LINKED)**
- a) 2x ≤ 8, donc x ≤ 4. b) S = ]−∞ ; 4]. c) x = 4 : 2×4 + 3 = 11 ≤ 11 ✓.

| Critère | Points | Code si perdu |
|---|---|---|
| 2x ≤ 8 puis x ≤ 4 | 2 | BR-NC-05-E1 (x ≥ 4) |
| Ensemble de solutions (pas une valeur unique) | 1 | BR-NC-05-E3 (« x = 4 ») |
| Vérification avec x = 4 | 1 | BR-NC-05-E1 |
Total : 4 points. Re-test : 3x − 2 ≤ 10 (S = ]−∞ ; 4]).

### T8 — Grille de diagnostic
| Compétence | Items | Seuil | Statut |
|---|---|---|---|
| Fractions et nombres relatifs (01, 06, 10) | Q1, Q2, Q3 | 3/3 acquis · 2/3 fragile · ≤ 1 à retravailler | indicatif |
| Calcul littéral (22, 04) | Q4, Q6 | ≥ 5/5 pts acquis | indicatif |
| Équations / inéquations (26, 05) | Q5, Q7 | ≥ 4/5 pts acquis | indicatif |
Chaque code observé = `SUSPECTED` ; aucun statut à partir d’un seul item ; aucune conception erronée affirmée sans preuve `CONFIRMED`.

### T9 — Couverture
5 QCM + 2 ouverts sur 7 lignes BR-NC (01, 06, 10, 22, 26, 04, 05) ; difficultés D1–D3 présentes. Temps total 25 min ≤ 0,9 × 30 = 27 min. Lignes BR-NC hors sélection (02, 03, 07–09, 11–21, 23–25, 27–29) : hors de ce blueprint court, non comptées comme lacunes. Chaque code n’est planté qu’une fois (version courte : la règle « ≥ 2 fois » de T5 n’est pas satisfaite).

### T10 — Suivi
Pour chaque code observé : sonde d’1 minute avec de nouveaux nombres (ex. −5/6 + 1/3 = −1/2 ; −4 + 2 − (−6) = 4 ; 3/4 − 1/6 = 7/12 ; 7 − 2(3x − 1) = 9 − 6x ; 4x − 3 = x + 9 ⇒ x = 4).

En-tête du journal d’erreurs : `student_id,date,item,code,option,confidence,evidence` (evidence ∈ SUSPECTED · CONFIRMED · UNDETERMINED).
