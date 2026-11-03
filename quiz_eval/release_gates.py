"""Read-only view of release gates. This module never sets PASS (or anything) itself."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = os.path.join(ROOT, "Math_Diagnostic_Reference_CLAUDE_v11", "validation_report_v11.json")

def read_gates(path=DEFAULT):
    with open(path, encoding="utf-8") as f: d = json.load(f)
    return dict(d["gates"]), dict(d["release_status"])

def release_allowed(path=DEFAULT):
    gates, status = read_gates(path)
    return all(v == "PASS" for v in gates.values()) and status.get("paper") != "HOLD"

def set_gate(*_a, **_k):
    raise PermissionError("release_gates never sets a gate: gates change only through the validator and teacher review.")
