"""Minimal reader for the Codex kit's selection_cases.yaml (block list of flow mappings). Stdlib only."""
import re
def _val(v):
    v = v.strip()
    if v[:1] in "'\"": return v[1:-1]
    return int(v) if re.fullmatch(r"-?\d+", v) else v
def _flow(s):
    s = s.strip()[1:-1]; out = {}
    for part in re.findall(r"(\w+):\s*('[^']*'|\"[^\"]*\"|[^,]+)", s): out[part[0]] = _val(part[1])
    return out
def load_cases(path):
    cases = []
    with open(path, encoding="utf-8") as f: lines = f.readlines()
    for line in lines:
        if line.lstrip().startswith("#") or not line.strip() or line.strip() == "cases:": continue
        m = re.match(r"\s*-\s*input:\s*(\{.*\})\s*$", line)
        if m: cases.append({"input": _flow(m.group(1))}); continue
        m = re.match(r"\s*(expect_\w+):\s*(.+?)\s*$", line)
        if m: cases[-1][m.group(1)] = _val(m.group(2)); continue
        raise ValueError("unparsed line: " + line)
    return cases
