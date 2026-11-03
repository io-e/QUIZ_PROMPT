import json,csv,html,re
K='/workspace/quiz2/Math_Diagnostic_Reference_CLAUDE_v11/'
rows={r['id']:r for r in csv.DictReader(open(K+'Math_Diagnostic_Targets_v11.csv',encoding='utf-8'))}
d=json.load(open('BR-NC_items.json'))
T={1:(1,4),2:(2,8),3:(3,12)}
mcq_t=sum(T[int(rows[i['id']]['difficulty'])][0] for i in d['items']); open_t=T[2][1]+T[3][1]
total=mcq_t+open_t; dur=30
def tags(rid,code):
    for e in json.loads(rows[rid]['errors_json']):
        if e['id']==code: return ', '.join(e['tags'])
S=[f"""# Diagnostic de mathématiques — Brevet · Nombres et calculs (BR-NC)

> **STATUT : NON VALIDÉ — HOLD (papier et numérique).** Version de test du prompt v9 / référence v11. Ne pas utiliser pour évaluer des élèves.

## Version élève

Niveau : 3e (Brevet) · Durée : {dur} min · **Calculatrice non autorisée**

Si tu ne sais pas, coche "Je ne sais pas" : ça ne te retire rien et ça aide ton professeur.
Après chaque réponse, coche "Sûr" ou "Pas sûr".

### Partie A — QCM (une seule bonne réponse)
"""]
for n,it in enumerate(d['items'],1):
    S.append(f"**{n}.** {it['stem']}\n")
    for L,o in zip('ABCD',it['options']): S.append(f"- {L}. {o['text']}")
    S.append("- E. Je ne sais pas\n\n☐ Sûr ☐ Pas sûr\n")
S.append("""### Partie B — Questions ouvertes

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
""")
student='\n'.join(S)
Tt=[f"""## Version enseignant

> ⚠️ **HOLD — aucun item n’est validé.** Les 7 lignes utilisées sont `eligibility_paper = HOLD`, `eligibility_digital = HOLD` dans `Item_Release_Eligibility_v11.csv` (curriculum non revu, relecture enseignant PENDING, pas de données pilotes, schéma player non vérifié). Tous les codes d’erreur sont des **hypothèses** (preuve `SUSPECTED` au mieux).

Paramètres : LEVEL = BREVET · SUBJECT = BR-NC · PURPOSE = Entry diagnostic · MODE = DIAGNOSTIC · NB_MCQ/NB_OPEN = 5/2 (version courte) · DURATION = {dur} min · CALCULATOR = non · DELIVERY = Paper · OPTIONS = NSP, CONFIDENCE · OUTPUT = MARKDOWN.

### T1 — Sources
| Source | Version | Consultation |
|---|---|---|
| French_Math_Diagnostic_Curriculum_Reference_CLAUDE_EN_v11.md + Math_Diagnostic_Targets_v11.csv + Item_Release_Eligibility_v11.csv | v11 (kit local) | 2026-11-03 |
| Programme de cycle 4 (BO) | [TO VERIFY] — non consulté dans ce test | — |

### T2 — Benchmark d’outils
Non réalisé dans ce test court (aucun outil documenté consulté) — [TO VERIFY].

### T3 — Carte des compétences
| Code | Micro-compétence | Ancre officielle | Statut d’ancre | Difficulté | Items autorisés | Éligibilité papier/num. |
|---|---|---|---|---|---|---|"""]
for rid in [i['id'] for i in d['items']]+['BR-NC-04','BR-NC-05']:
    r=rows[rid]; Tt.append(f"| {rid} | {r['capability']} | {r['official_ref']} | {r['anchor_status']} | D{r['difficulty']} | {r['allowed_items']} | HOLD/HOLD |")
Tt.append("\n### T4/T6 — Clés des QCM et banque d’erreurs (graine MCQ, règle R1)\n| Item | Ligne | Clé | Option → code → pourquoi | Tags transversaux |\n|---|---|---|---|---|")
for n,it in enumerate(d['items'],1):
    ds='<br>'.join(f"{L}. {o['text']} → `{o['error_code']}` → {o['why']}" for L,o in zip('ABCD',it['options']) if not o['correct'])
    tg='; '.join(tags(it['id'],o['error_code']) for o in it['options'] if not o['correct'])
    Tt.append(f"| {n} | {it['id']} | **{it['key']}** ({[o for o in it['options'] if o['correct']][0]['text']}) | {ds} | {tg} |")
Tt.append(f"""
Positions des clés : B, D, A, C, B → B = 40 % (≤ 40 %). Temps QCM : {mcq_t} min.

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
5 QCM + 2 ouverts sur 7 lignes BR-NC (01, 06, 10, 22, 26, 04, 05) ; difficultés D1–D3 présentes. Temps total {total} min ≤ 0,9 × {dur} = {0.9*dur:.0f} min. Lignes BR-NC hors sélection (02, 03, 07–09, 11–21, 23–25, 27–29) : hors de ce blueprint court, non comptées comme lacunes. Chaque code n’est planté qu’une fois (version courte : la règle « ≥ 2 fois » de T5 n’est pas satisfaite).

### T10 — Suivi
Pour chaque code observé : sonde d’1 minute avec de nouveaux nombres (ex. −5/6 + 1/3 = −1/2 ; −4 + 2 − (−6) = 4 ; 3/4 − 1/6 = 7/12 ; 7 − 2(3x − 1) = 9 − 6x ; 4x − 3 = x + 9 ⇒ x = 4).

En-tête du journal d’erreurs : `student_id,date,item,code,option,confidence,evidence` (evidence ∈ SUSPECTED · CONFIRMED · UNDETERMINED).
""")
teacher='\n'.join(Tt)
open('BR-NC_diagnostic_v9test.md','w').write(student+'\n---\n\n'+teacher)
# minimal MD->HTML
def inline(s):
    s=html.escape(s); s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s); s=re.sub(r'\*(.+?)\*',r'<em>\1</em>',s)
    s=re.sub(r'`(.+?)`',r'<code>\1</code>',s); return s.replace('&lt;br&gt;','<br>')
def md2html(md):
    out=[];ls=md.split('\n');i=0
    while i<len(ls):
        l=ls[i]
        if l.startswith('|'):
            t=[];
            while i<len(ls) and ls[i].startswith('|'): t.append(ls[i]);i+=1
            cells=lambda r:[c.strip() for c in r.strip('|').split('|')]
            out.append('<table><tr>'+''.join(f'<th>{inline(c)}</th>' for c in cells(t[0]))+'</tr>'+''.join('<tr>'+''.join(f'<td>{inline(c)}</td>' for c in cells(r))+'</tr>' for r in t[2:])+'</table>');continue
        if l.startswith('- '):
            out.append('<ul>')
            while i<len(ls) and ls[i].startswith('- '): out.append(f'<li>{inline(ls[i][2:])}</li>');i+=1
            out.append('</ul>');continue
        m=re.match(r'(#+) (.*)',l)
        if m: out.append(f'<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>')
        elif l.startswith('> '): out.append(f'<div class="warn">{inline(l[2:])}</div>')
        elif l.strip()=='---': out.append('<hr>')
        elif l.strip(): out.append(f'<p>{inline(l)}</p>')
        i+=1
    return '\n'.join(out)
CSS="body{font-family:Arial,Verdana,sans-serif;max-width:900px;margin:auto;padding:20px;line-height:1.5;color:#162338}table{border-collapse:collapse;width:100%;margin:10px 0}td,th{border:1px solid #ccd;padding:6px;vertical-align:top;text-align:left}th{background:#eef}.warn{background:#fff5df;border-left:4px solid #a46b17;padding:10px;margin:10px 0}code{background:#eef;padding:1px 3px}ul{list-style:none}@media print{.warn{border:1px solid #a46b17}}"
for name,title,md in [('BR-NC_eleve.html','Diagnostic BR-NC — élève',student),('BR-NC_enseignant.html','Diagnostic BR-NC — enseignant',student+'\n---\n'+teacher)]:
    open(name,'w').write(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style></head><body>{md2html(md)}</body></html>')
print(mcq_t,open_t,total)
