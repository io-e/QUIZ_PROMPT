"""Configuration files are YAML written in the JSON-compatible subset (YAML 1.2 is a superset of JSON),
with full-line '#' comments allowed. This keeps the engine stdlib-only and runnable with `python3 -I`
(PyYAML is not installed in that mode). Any YAML 1.2 parser reads these files identically."""
import json
def load(path):
    with open(path, encoding="utf-8") as f:
        txt = "\n".join(l for l in f.read().split("\n") if not l.lstrip().startswith("#"))
    return json.loads(txt)
