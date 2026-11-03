"""docs/LINK_APPROVAL_WORKLIST.csv: all links, QUARANTINE first, with Grok's evidence as context and
EMPTY teacher columns (source, passage, page, reviewer, date, decision). Never fills approvals."""
import csv, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = {"QUARANTINE": 0, "TO_REVIEW": 1, "PROPOSED_PARTIAL": 2, "PROPOSED": 3, "EXCLUDED_NOT_SUPPORTED": 4}
F = ["priority", "link_id", "skill_id", "edition_id", "official_ref", "link_status", "approval", "grok_source_url", "grok_page", "grok_passage",
     "quarantine_review_ref", "teacher_source_url", "teacher_passage", "teacher_page", "reviewer", "review_date", "decision", "second_reviewer", "second_review_date", "second_decision"]
with open(os.path.join(R, "subjects/mathematics/reference/skill_programme_links.csv"), encoding="utf-8") as f: L = list(csv.DictReader(f))
L.sort(key=lambda r: (ORDER.get(r["link_status"], 9), r["link_id"]))
rows = [dict(priority=i + 1, link_id=l["link_id"], skill_id=l["skill_id"], edition_id=l["edition_id"], official_ref=l["official_ref"],
             link_status=l["link_status"], approval=l["approval"], grok_source_url=l["source_url"], grok_page=l["page"], grok_passage=l["verbatim_passage"],
             quarantine_review_ref="docs/QUARANTINE_REVIEW.csv" if l["link_status"] == "QUARANTINE" else "",
             **{k: "" for k in F[11:]}) for i, l in enumerate(L)]
with open(os.path.join(R, "docs/LINK_APPROVAL_WORKLIST.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, F); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), "links;", dict(Counter(r["link_status"] for r in rows)))
