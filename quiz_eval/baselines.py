"""Frozen comparison baselines. A FREEZE is not a RELEASE: frozen=true, approved=false, release HOLD.
Frozen manifests are immutable: write_baseline refuses to overwrite, verify_baseline detects drift."""
import hashlib, json, os, subprocess
from . import SOFTWARE_VERSION
from .programme_resolver import ROOT

BASELINE_DIR = os.path.join("subjects", "mathematics", "reference", "baselines")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""): h.update(chunk)
    return h.hexdigest()

def tracked_files(package_dir, root=ROOT):
    out = subprocess.run(["git", "ls-files", "-z", package_dir], cwd=root, capture_output=True, check=True).stdout
    return sorted(p for p in out.decode().split("\0") if p)

def build_baseline(reference_version, package_dir, prompt_file, source_commit, root=ROOT):
    files = {p: sha256_file(os.path.join(root, p)) for p in tracked_files(package_dir, root)}
    return {
        "schema": "quiz_eval.baseline/1",
        "reference_version": reference_version,
        "kind": "COMPARISON_BASELINE",
        "frozen": True, "approved": False,
        "release_status": {"paper": "HOLD", "digital": "HOLD"},
        "note": "Frozen comparison baseline, NOT a pedagogical release. No target has passed teacher review because of this freeze. A validated release requires a separate approval manifest (schema quiz_eval.approval/1).",
        "engine_version": SOFTWARE_VERSION,
        "source_commit": source_commit,
        "package_dir": package_dir,
        "prompt": {"version": "PROMPT_v9", "file": prompt_file, "sha256": files[prompt_file]},
        "file_count": len(files), "files_sha256": files,
    }

def write_baseline(manifest, root=ROOT):
    path = os.path.join(root, BASELINE_DIR, manifest["reference_version"] + ".manifest.json")
    if os.path.exists(path): raise FileExistsError(f"{path} is frozen and immutable")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "x", encoding="utf-8") as f: f.write(json.dumps(manifest, sort_keys=True, indent=1) + "\n")
    return path

def load_baseline(reference_version, root=ROOT):
    with open(os.path.join(root, BASELINE_DIR, reference_version + ".manifest.json"), encoding="utf-8") as f: return json.load(f)

def verify_baseline(reference_version, root=ROOT):
    """Return list of drift messages (empty = intact)."""
    m = load_baseline(reference_version, root); drift = []
    for p, h in m["files_sha256"].items():
        fp = os.path.join(root, p)
        if not os.path.exists(fp): drift.append(f"missing {p}")
        elif sha256_file(fp) != h: drift.append(f"changed {p}")
    extra = set(tracked_files(m["package_dir"], root)) - set(m["files_sha256"])
    drift += [f"added {p}" for p in sorted(extra)]
    return drift
