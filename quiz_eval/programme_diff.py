"""New-BO workflow: register edition (append-only), diff skill applicability, review worklist,
preserve old approvals, run regression tests, write an immutable release manifest with hashes."""
import copy, csv, hashlib, json, os, subprocess, sys
from .yamlio import load
from .programme_resolver import ROOT, subject_dir, _year

LINK_FIELDS = ["link_id", "skill_id", "edition_id", "official_ref", "link_status", "verification", "source_url", "page",
               "verbatim_passage", "evidence_origin", "approval", "proposed_action", "reviewer", "approved_on", "note"]

def register_edition(registry, new_programme):
    """Return a NEW registry with the edition appended. Refuses duplicates and overlaps; never edits old entries."""
    if any(p["id"] == new_programme["id"] for p in registry["programmes"]):
        raise ValueError(f"edition {new_programme['id']} already registered (editions are immutable)")
    for a in new_programme["applies"]:
        for p in registry["programmes"]:
            if p["subject"] != new_programme["subject"] or p["track"] != new_programme["track"]: continue
            for b in p["applies"]:
                if b["grade"] == a["grade"] and not (_year(a["through_year"]) < _year(b["from_year"]) or _year(a["from_year"]) > _year(b["through_year"])):
                    raise ValueError(f"overlap with {p['id']} for {a['grade']}: close the old range with a NEW verified bound first")
    reg = copy.deepcopy(registry); reg["programmes"].append(copy.deepcopy(new_programme)); return reg

def diff_applicability(links, old_edition, new_edition):
    old = {l["skill_id"] for l in links if l["edition_id"] == old_edition and not l["link_status"].startswith("EXCLUDED")}
    new = {l["skill_id"] for l in links if l["edition_id"] == new_edition and not l["link_status"].startswith("EXCLUDED")}
    return {"only_old": sorted(old - new), "only_new": sorted(new - old), "both": sorted(old & new)}

def propose_links_for_new_edition(links, old_edition, new_edition):
    """Old links are kept byte-for-byte (approvals preserved). Each old skill gets a NEW link to the new edition
    with status TO_REVIEW: it is not selectable until a teacher checks the new official text."""
    out = [dict(l) for l in links]
    have = {(l["skill_id"], l["edition_id"]) for l in links}
    for l in links:
        if l["edition_id"] == old_edition and (l["skill_id"], new_edition) not in have:
            n = {k: "" for k in LINK_FIELDS}
            n.update(link_id=f"{l['skill_id']}@{new_edition}", skill_id=l["skill_id"], edition_id=new_edition,
                     official_ref=l["official_ref"], link_status="TO_REVIEW", verification="UNVERIFIED", approval="PENDING",
                     evidence_origin="programme_diff (carried over from %s)" % old_edition)
            out.append(n); have.add((l["skill_id"], new_edition))
    return out

def worklist(links, priority=("QUARANTINE", "TO_REVIEW", "PROPOSED_PARTIAL", "PROPOSED")):
    rows = [l for l in links if l["link_status"] in priority]
    return sorted(rows, key=lambda l: (priority.index(l["link_status"]), l["skill_id"], l["edition_id"]))

def write_csv(path, rows, fields=LINK_FIELDS):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

def run_regression(root=ROOT):
    r = subprocess.run([sys.executable, "-I", os.path.join(root, "tests", "test_versioning.py")], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

def write_release_manifest(release_dir, release_id, files, root=ROOT, extra=None):
    """Immutable: refuses to overwrite an existing manifest."""
    os.makedirs(release_dir, exist_ok=True)
    path = os.path.join(release_dir, f"{release_id}.json")
    if os.path.exists(path): raise FileExistsError(f"release manifest {path} exists and is immutable")
    h = {}
    for f in sorted(files):
        with open(f, "rb") as fh: h[os.path.relpath(f, root)] = hashlib.sha256(fh.read()).hexdigest()
    m = {"release_id": release_id, "files_sha256": h, "release_status": {"paper": "HOLD", "digital": "HOLD"}, **(extra or {})}
    with open(path, "w", encoding="utf-8") as fh: fh.write(json.dumps(m, sort_keys=True, indent=1) + "\n")
    return path

def publish_new_edition(subject, new_programme, old_edition, release_id, root=ROOT, run_tests=True):
    """Full new-BO cycle in `root` (use a copy for dry runs). Returns a summary dict."""
    d = subject_dir(subject, root)
    reg_path = os.path.join(d, "programme", "editions.yaml"); links_path = os.path.join(d, "reference", "skill_programme_links.csv")
    reg = register_edition(load(reg_path), new_programme)
    with open(reg_path, "w", encoding="utf-8") as f:
        f.write("# Programme applicability registry (append-only).\n" + json.dumps(reg, ensure_ascii=False, indent=1) + "\n")
    with open(links_path, encoding="utf-8") as f: links = list(csv.DictReader(f))
    new_links = propose_links_for_new_edition(links, old_edition, new_programme["id"])
    write_csv(links_path, new_links)
    wl = os.path.join(d, "reference", f"REVIEW_WORKLIST_{new_programme['id']}.csv")
    write_csv(wl, [l for l in worklist(new_links) if l["edition_id"] == new_programme["id"]])
    code, out = run_regression(root) if run_tests else (0, "skipped")
    if code != 0: raise RuntimeError("regression tests failed; no release manifest written\n" + out)
    man = write_release_manifest(os.path.join(root, "releases", subject), release_id, [reg_path, links_path, wl], root,
                                 {"new_edition": new_programme["id"], "diff": diff_applicability(new_links, old_edition, new_programme["id"])})
    return {"worklist": wl, "manifest": man}
