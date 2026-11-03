"""Version-aware curriculum resolver.

Four independent versions travel in every manifest:
  curriculum edition (e.g. MATH_C4_2020), reference version (e.g. MATH_REF_v11),
  exam session (e.g. DNB_MATH_2027) and software version (quiz_eval/1.0).
Selection modes (Codex kit calls them `policy`):
  CURRENT_FOR_COHORT  legally applicable programme for subject + grade + track + school year
  HISTORICAL_EXAM     a past/future session: its original programme + separately stored exam rules
  EXPLICIT_EDITION    a deliberately chosen edition; output labelled HISTORICAL_SIMULATION
"""
import csv, hashlib, json, os
from . import SOFTWARE_VERSION
from .yamlio import load

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODES = ("CURRENT_FOR_COHORT", "HISTORICAL_EXAM", "EXPLICIT_EDITION")
REFERENCE_VERSIONS = {"mathematics": "MATH_REF_v11", "physics_chemistry": "PHYS_REF_NONE"}
# link statuses allowed in a test; QUARANTINE / EXCLUDED_* are never selectable
SELECTABLE = {"validated": {"APPROVED"}, "draft": {"APPROVED", "PROPOSED", "PROPOSED_PARTIAL"}}

class ResolutionError(Exception):
    def __init__(self, code, msg):
        super().__init__(f"{code}: {msg}"); self.code = code

def subject_dir(subject, root=ROOT): return os.path.join(root, "subjects", subject)
def _year(y): return int(str(y).split("-")[0])

def load_registry(subject, root=ROOT):
    d = subject_dir(subject, root)
    return load(os.path.join(d, "programme", "editions.yaml")), load(os.path.join(d, "programme", "exams.yaml"))

def _sha(path):
    with open(path, "rb") as f: return hashlib.sha256(f.read()).hexdigest()

def find_edition(reg, subject, grade, track, school_year):
    """Bounded lookup. Returns (programme, applies-entry) or raises UNVERIFIED_EDITION. Never infers."""
    hits = []
    for p in reg["programmes"]:
        if p["subject"] != subject or p["track"] != track: continue
        for a in p["applies"]:
            if a["grade"] == grade and _year(a["from_year"]) <= _year(school_year) <= _year(a["through_year"]):
                hits.append((p, a))
    if not hits:
        raise ResolutionError("UNVERIFIED_EDITION", f"no verified edition for {subject}/{grade}/{track}/{school_year}")
    if len(hits) > 1:
        raise ResolutionError("AMBIGUOUS_EDITION", f"{[h[0]['id'] for h in hits]} overlap for {grade} {school_year}")
    return hits[0]

def _verification(a):
    return "VERIFIED" if a["from_evidence"]["status"] == a["through_evidence"]["status"] == "VERIFIED" else "UNVERIFIED"

def resolve(policy, subject, grade, track, school_year=None, assessment=None, exam_session=None, edition=None, root=ROOT):
    """Return a deterministic version manifest (dict). Same inputs -> identical manifest."""
    if policy not in MODES: raise ResolutionError("BAD_MODE", policy)
    reg, exams = load_registry(subject, root)
    exam = None
    if policy == "HISTORICAL_EXAM":
        cands = [e for e in exams["exam_profiles"] if e["assessment"] == assessment and int(e["session"]) == int(exam_session)
                 and e["grade"] == grade and e["track"] == track]
        if not cands: raise ResolutionError("UNKNOWN_EXAM_SESSION", f"{assessment} {exam_session}")
        exam = cands[0]; school_year = exam["school_year"]
    if policy == "EXPLICIT_EDITION":
        p = next((x for x in reg["programmes"] if x["id"] == edition), None)
        if not p or p["subject"] != subject: raise ResolutionError("UNKNOWN_EDITION", str(edition))
        a = next((x for x in p["applies"] if x["grade"] == grade), None)
        if not a or p["track"] != track: raise ResolutionError("EDITION_GRADE_MISMATCH", f"{edition} has no {grade}/{track}")
        label = "HISTORICAL_SIMULATION"
    else:
        if school_year is None: raise ResolutionError("MISSING_SCHOOL_YEAR", "school_year required")
        p, a = find_edition(reg, subject, grade, track, school_year)
        label = "HISTORICAL_EXAM" if policy == "HISTORICAL_EXAM" else "CURRENT_FOR_COHORT"
    d = subject_dir(subject, root)
    files = [os.path.join(d, "programme", "editions.yaml"), os.path.join(d, "programme", "exams.yaml"),
             os.path.join(d, "reference", "skill_programme_links.csv")]
    rv = REFERENCE_VERSIONS.get(subject, "UNKNOWN")
    bl = os.path.join(root, "subjects", subject, "reference", "baselines", rv + ".manifest.json")
    baseline = {"manifest": os.path.relpath(bl, root), "sha256": _sha(bl)} if os.path.exists(bl) else None
    return {
        "manifest_schema": "quiz_eval.version_manifest/1",
        "software_version": SOFTWARE_VERSION,
        "reference_version": rv,
        "reference_baseline": baseline,
        "mode": policy, "label": label,
        "cohort": {"subject": subject, "grade": grade, "track": track, "school_year": school_year},
        "curriculum_edition": {"id": p["id"], "title": p["title"], "applies": {"from_year": a["from_year"], "through_year": a["through_year"]},
                               "verification": _verification(a)},
        "exam_session": None if not exam else {"id": exam["id"], "session": exam["session"], "rules_id": exam["rules"]["id"],
                                               "rules_status": exam["rules"]["status"], "format_review": exam["format_review"]},
        "inputs_sha256": {os.path.relpath(f, root): _sha(f) for f in files if os.path.exists(f)},
        "release_status": {"paper": "HOLD", "digital": "HOLD"},
    }

def manifest_bytes(m):
    """Canonical serialisation: byte-identical for identical inputs (no timestamps)."""
    return (json.dumps(m, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")

def load_links(subject, root=ROOT):
    with open(os.path.join(subject_dir(subject, root), "reference", "skill_programme_links.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))

def select_skills(manifest, validated, root=ROOT):
    """Skills linked to the manifest's edition with a selectable link status.
    validated=True only accepts APPROVED links (none exist until the teacher approves) and a VERIFIED edition."""
    allowed = SELECTABLE["validated" if validated else "draft"]
    if validated and manifest["curriculum_edition"]["verification"] != "VERIFIED":
        raise ResolutionError("UNVERIFIED_EDITION_FOR_VALIDATED_TEST", manifest["curriculum_edition"]["id"])
    ed = manifest["curriculum_edition"]["id"]
    return sorted({l["skill_id"] for l in load_links(manifest["cohort"]["subject"], root)
                   if l["edition_id"] == ed and l["link_status"] in allowed})
