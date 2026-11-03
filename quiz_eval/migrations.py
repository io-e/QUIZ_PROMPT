"""Legacy ID resolution through Math_ID_Migration_to_v11.csv (read-only)."""
import csv, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = os.path.join(ROOT, "Math_Diagnostic_Reference_CLAUDE_v11", "Math_ID_Migration_to_v11.csv")

class Migrations:
    def __init__(self, path=DEFAULT):
        with open(path, encoding="utf-8") as f: self.rows = list(csv.DictReader(f))
        self.reserved = [re.compile("^" + r["legacy_id"] + "$") for r in self.rows if r["relation"] == "RESERVED"]
        self.by_legacy = {}
        for r in self.rows:
            if r["legacy_id"] and r["relation"] != "RESERVED": self.by_legacy.setdefault(r["legacy_id"], []).append(r)
        self.current = {r["current_id"] for r in self.rows if r["current_id"]}

    def resolve(self, legacy_id):
        """Return dict(current_id, relation, review_status). Never invents a mapping."""
        rows = self.by_legacy.get(legacy_id)
        if not rows:
            if legacy_id in self.current: return {"current_id": legacy_id, "relation": "CURRENT", "review_status": "BUILD"}
            return {"current_id": None, "relation": "UNKNOWN", "review_status": None}
        r = rows[0]
        return {"current_id": r["current_id"] or None, "relation": r["relation"], "review_status": r["review_status"]}

    def is_reserved_pattern(self, candidate):
        return any(p.match(candidate) for p in self.reserved)
