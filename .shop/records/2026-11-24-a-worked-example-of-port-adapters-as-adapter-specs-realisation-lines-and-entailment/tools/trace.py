"""Read an adapter spec's trace off `spec parse --form` of its realisation lines: each line's trigger (a port operation
requested, or a provider act) and the acts of its response whose verb names an operation, by the vocabulary."""
import re, subprocess, sys
from pathlib import Path

root = Path(sys.argv[1])
ops = {}
for f in (root / "spec" / "vocabulary").glob("*.md"):
    for m in re.finditer(r"^- \*\*(.+?)\*\* \(verb, action\) → operation (\S+)\.", f.read_text(), re.M):
        ops[m.group(1)] = m.group(2)
out = subprocess.run([sys.executable, "/home/vscode/shopsystem-bdd/scripts/spec", "--root", str(root), "parse",
                      "--form", "--file", str(root / "spec/capabilities/realisation.md")],
                     capture_output=True, text=True).stdout
for block in re.split(r"\n(?=\d+: )", out):
    trig = re.search(r"request\(e1, (\S+?),", block) or re.search(r"^\s+(\w+)\(e1,", block, re.M)
    acts = [ops[v] for v in re.findall(r"^\s+(\w+)\(e[2-9],", block, re.M) if v in ops]
    first = trig.group(1) if trig else "?"
    print(f"{block.split(':')[0]:>4}  {ops.get(first, first):<22} -> {', '.join(acts) or '-'}")
