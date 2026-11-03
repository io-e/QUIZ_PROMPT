"""Grok's PROPOSED review of the 18 QUARANTINE links (9 NEITHER Brevet skills x 2 editions).
Each link is reviewed independently against its own edition. Proposals only: link_status stays QUARANTINE,
approval stays PENDING; reviewer/decision columns are left empty for the teacher.
Passages are checked verbatim against the fetched PDF text (pdftotext -layout) when --verify DIR is given."""
import csv, os, re, sys, unicodedata
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U20 = "https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf"
U26 = "https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf"
URL = {"MATH_C4_2020": U20, "MATH_C4_2026": U26}
TXT = {"MATH_C4_2020": "C4_2020.txt", "MATH_C4_2026": "R15.txt"}
DNB29 = ("DNB 2029+ (MENE2623228N): subjects bear on the programme de la classe de troisième if in force; "
         "this passage sits under the Quatrième heading, so for 3e-only exam selection it would be PREREQUISITE.")
# (skill, edition): (passages [(page, text)], not_found_terms, proposed_decision, confidence, if_unsupported, needs_second, rationale)
P = {
 ("BR-DF-02", "MATH_C4_2020"): ([(133, "- Lire et interpréter des données sous forme de données brutes, de tableau, de diagramme"), (133, "- Calculer des effectifs, des fréquences."), (133, "- Faire le lien entre fréquence et probabilité.")],
    "", "SUPPORTED", "medium", "", "YES", "All three parts (graph/table reading, frequencies, probability) appear in the 2020 attendus; the PR #2 audit had found no 2020 passage, so this is a new finding to confirm."),
 ("BR-DF-02", "MATH_C4_2026"): ([(16, "Lire et interpréter des informations présentées sous forme de tableaux, de diagrammes et de graphiques."), (18, "Observer la stabilisation des fréquences lorsqu’on augmente le nombre de répétitions de l’expérience aléatoire, faire le lien")],
    "", "SUPPORTED", "medium", "", "YES", "Covered across 5e (reading tables/graphs, p.16) and 3e (frequency-probability link, p.18). Composite skill: the teacher should confirm the combination."),
 ("BR-DF-12", "MATH_C4_2020"): ([(133, "- Calculer des probabilités dans des cas simples (par exemple évaluation des chances de")],
    "deux épreuves; arbre", "PARTIALLY_SUPPORTED", "low", "ENRICHMENT", "YES", "The 2020 text only says 'cas simples'; two-stage experiments and trees are not named in the programme text."),
 ("BR-DF-12", "MATH_C4_2026"): ([(17, "Exemples simples d’expériences aléatoires à deux épreuves (par exemple, lancer de deux pièces, d’une pièce et d’un dé, de"), (18, "Simuler des expériences aléatoires indépendantes.")],
    "arbre", "PARTIALLY_SUPPORTED", "medium", "PREREQUISITE", "YES", "Two-stage experiments are explicit (4e) but a tree diagram is not named. " + DNB29),
 ("BR-DF-13", "MATH_C4_2020"): ([(133, "- Probabilité d’événements certains, impossibles, contraires.")],
    "", "SUPPORTED", "high", "", "NO", "Explicit: 'événements ... contraires'."),
 ("BR-DF-13", "MATH_C4_2026"): ([(17, "Calculer la probabilité d’un évènement et de l’évènement contraire.")],
    "", "SUPPORTED", "high", "PREREQUISITE", "YES", "Explicit, but taught in 4e. " + DNB29),
 ("BR-DF-14", "MATH_C4_2020"): ([(133, "- Faire le lien entre fréquence et probabilité.")],
    "stabilisation", "PARTIALLY_SUPPORTED", "medium", "ENRICHMENT", "YES", "The frequency-probability link is explicit; 'stabilisation' is not named in the 2020 text."),
 ("BR-DF-14", "MATH_C4_2026"): ([(18, "Observer la stabilisation des fréquences lorsqu’on augmente le nombre de répétitions de l’expérience aléatoire, faire le lien"), (16, "à la naissance) en s’appuyant sur l’idée de stabilisation des fréquences (loi des grands nombres).")],
    "", "SUPPORTED", "high", "", "NO", "Explicit 3e objective."),
 ("BR-DF-21", "MATH_C4_2020"): ([(132, "- Résoudre algébriquement des équations du premier degré ou s’y ramenant (équations"), (134, "- Passer d’un mode de représentation d’une fonction à un autre."), (134, "- Représenter graphiquement une fonction linéaire, une fonction affine.")],
    "résoudre graphiquement; f(x) = g(x)", "PARTIALLY_SUPPORTED", "low", "ENRICHMENT", "YES", "The algebraic part is explicit; graphical solving of f(x)=g(x) is not named."),
 ("BR-DF-21", "MATH_C4_2026"): ([(10, "Mettre en équation un problème et le résoudre à l’aide d’une équation du premier degré du type a𝑥 + b = c𝑥 + d."), (20, "Résoudre graphiquement des équations et des inéquations linéaires.")],
    "f(x) = g(x) for non-affine f, g", "PARTIALLY_SUPPORTED", "medium", "ENRICHMENT", "YES", "SUPPORTED if f and g are restricted to affine functions (3e p.20 graphical solving, 4e p.10 ax+b=cx+d); not supported for general f, g."),
 ("BR-GM-04", "MATH_C4_2020"): ([(135, "- Notion de grandeur produit et de grandeur quotient."), (135, "- Mener des calculs impliquant des grandeurs mesurables, notamment des grandeurs"), (134, "en fonction de l’intensité, la distance parcourue en fonction du temps à vitesse constante,")],
    "masse volumique; énergie", "PARTIALLY_SUPPORTED", "medium", "ENRICHMENT", "YES", "Compound quantities and speed are explicit; density and energy units are not named in the maths text (they may come from physics)."),
 ("BR-GM-04", "MATH_C4_2026"): ([(19, "Utiliser des grandeurs quotients, avec ou sans unités."), (18, "Utiliser un coefficient de proportionnalité dans des contextes concrets (prix unitaire, vitesse moyenne, échelle, etc.).")],
    "grandeur produit; masse volumique; énergie", "PARTIALLY_SUPPORTED", "low", "ENRICHMENT", "YES", "Only quotient quantities (4e) and average speed (5e) are named; there are no product quantities and no energy. The energy part is a candidate for ENRICHMENT. " + DNB29),
 ("BR-GM-08", "MATH_C4_2020"): ([(135, "- Effectuer des conversions d’unités.")],
    "heure; minute; durée", "PARTIALLY_SUPPORTED", "low", "PREREQUISITE", "YES", "Only a generic unit-conversion objective; time conversion is not named."),
 ("BR-GM-08", "MATH_C4_2026"): ([],
    "heure; minute; durée; conversions de durées (p.13 names only longueur and aires)", "NOT_SUPPORTED", "medium", "PREREQUISITE", "YES", "No passage on durations was found in annexe 2. Proposed as PREREQUISITE (assumed cycle 3 content; the cycle 3 text was NOT checked)."),
 ("BR-GM-09", "MATH_C4_2020"): ([(135, "- Mener des calculs impliquant des grandeurs mesurables, notamment des grandeurs"), (135, "- Notion de grandeur produit et de grandeur quotient.")],
    "débit; masse volumique", "SUPPORTED", "medium", "", "YES", "'grandeurs composées' covers flow rate and density, but neither is named."),
 ("BR-GM-09", "MATH_C4_2026"): ([(19, "Utiliser des grandeurs quotients, avec ou sans unités.")],
    "débit; masse volumique", "PARTIALLY_SUPPORTED", "medium", "PREREQUISITE", "YES", "Flow rate and density are quotient quantities but are not named. " + DNB29),
 ("BR-GM-11", "MATH_C4_2020"): ([(135, "- Effectuer des conversions d’unités."), (135, "- Vérifier la cohérence des résultats du point de vue des unités.")],
    "km/h; m/s", "SUPPORTED", "medium", "", "YES", "Conversions of compound units fall under 'grandeurs composées' + 'conversions d’unités'; the speed units are not named."),
 ("BR-GM-11", "MATH_C4_2026"): ([(19, "Utiliser des grandeurs quotients, avec ou sans unités."), (6, "puissances de dix de nano à giga. On fait le lien avec les conversions.")],
    "km/h; m/s; conversion of compound units", "PARTIALLY_SUPPORTED", "low", "ENRICHMENT", "YES", "No explicit conversion of compound units; p.13 conversions cover length and area only."),
}
def norm(s): return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip()

def verify(bo_dir):
    bad = []
    for (sid, ed), (ps, *_rest) in P.items():
        with open(os.path.join(bo_dir, TXT[ed]), encoding="utf-8") as f: pages = f.read().split("\f")
        for pg, t in ps:
            if norm(t) not in norm(pages[pg - 1]): bad.append((sid, ed, pg, t))
    return bad

FIELDS = ["link_id", "skill_id", "edition_id", "capability", "official_ref", "link_status", "approval", "official_source_url", "page",
          "passages_found", "terms_not_found", "grok_proposed_decision", "grok_confidence", "proposed_classification_if_unsupported",
          "needs_second_review", "grok_rationale", "reviewer_1", "review_1_date", "decision_1", "reviewer_2", "review_2_date", "decision_2"]

def rows():
    with open(os.path.join(R, "subjects/mathematics/reference/skill_programme_links.csv"), encoding="utf-8") as f:
        L = [r for r in csv.DictReader(f) if r["link_status"] == "QUARANTINE"]
    with open(os.path.join(R, "subjects/mathematics/reference/skills.csv"), encoding="utf-8") as f:
        S = {r["skill_id"]: r for r in csv.DictReader(f)}
    out = []
    for l in sorted(L, key=lambda r: r["link_id"]):
        ps, nf, dec, conf, cls, sec, why = P[(l["skill_id"], l["edition_id"])]
        out.append(dict(link_id=l["link_id"], skill_id=l["skill_id"], edition_id=l["edition_id"], capability=S[l["skill_id"]]["capability"],
            official_ref=l["official_ref"], link_status=l["link_status"], approval=l["approval"], official_source_url=URL[l["edition_id"]],
            page="; ".join(f"PDF p.{p}" for p, _ in ps) or "-", passages_found=" || ".join(f"[p.{p}] {t}" for p, t in ps) or "NOT FOUND",
            terms_not_found=nf, grok_proposed_decision=dec, grok_confidence=conf, proposed_classification_if_unsupported=cls,
            needs_second_review=sec, grok_rationale=why, reviewer_1="", review_1_date="", decision_1="", reviewer_2="", review_2_date="", decision_2=""))
    return out

if __name__ == "__main__":
    if "--verify" in sys.argv:
        b = verify(sys.argv[sys.argv.index("--verify") + 1]); print("passage check:", "all verbatim" if not b else b)
        if b: sys.exit(1)
    rs = rows()
    with open(os.path.join(R, "docs/QUARANTINE_REVIEW.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rs)
    md = ["# QUARANTINE review: 18 links (9 Brevet skills x 2 editions), Grok PROPOSALS ONLY", "",
          "Roles: **Grok proposes, Python verifies structure, a qualified teacher approves.** Every link stays `QUARANTINE` / `approval=PENDING` until a teacher fills `decision_1` (and `decision_2` when `needs_second_review=YES`). Every ID is kept. Each link was reviewed against its own edition only; no skill is rejected for both editions.", "",
          f"Sources: 2020 edition = Éduscol cycle 4 PDF ({U20}); 2026 edition = BO n°10 2026, annexe 2 ({U26}). The page is the PDF page. Passages were checked verbatim against `pdftotext -layout` output (`python3 tools/build_quarantine_review.py --verify DIR`). 'Not found' means the terms were searched (case/accent-insensitive) in the whole maths text without a hit.", "",
          "Grade headings in the 2026 text (Cinquième / Quatrième / Troisième) were attributed from the page layout. A reviewer should confirm them.", ""]
    from collections import Counter
    md += ["| Decision | Count |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(Counter(r['grok_proposed_decision'] for r in rs).items())] + [f"| needs_second_review=YES | {sum(r['needs_second_review']=='YES' for r in rs)} |", ""]
    for r in rs:
        md += [f"## {r['link_id']} – {r['capability']} ({r['official_ref']})", "",
               f"- **Grok proposal:** {r['grok_proposed_decision']} (confidence {r['grok_confidence']}); if unsupported: {r['proposed_classification_if_unsupported'] or '-'}; second review: {r['needs_second_review']}",
               f"- **Source:** {r['official_source_url']} – {r['page']}",
               f"- **Passages found:** {r['passages_found']}", f"- **Not found:** {r['terms_not_found'] or '-'}", f"- **Rationale:** {r['grok_rationale']}",
               "- Reviewer 1: ____ Date: ____ Decision: ____ | Reviewer 2: ____ Date: ____ Decision: ____", ""]
    with open(os.path.join(R, "docs/QUARANTINE_REVIEW.md"), "w", encoding="utf-8") as f: f.write("\n".join(md))
    print(len(rs), "quarantine rows written")
