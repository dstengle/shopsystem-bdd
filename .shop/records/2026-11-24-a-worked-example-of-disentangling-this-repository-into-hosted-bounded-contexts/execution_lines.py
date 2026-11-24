#!/usr/bin/env python3
"""Each live line of execution's capabilities classified by what it needs of tracking and specification (read-only).

python3 execution_lines.py /home/vscode/shopsystem-bdd > execution-lines.md
Classes, the first that fits: W writes a tracking object's state (sets the status of an item or a context request,
keeps a question on an item); R reads tracking state in its condition (an item's status, the readiness bar, a
dependency, the review limit, a chore, a request line); S needs the specification laid or checked (a requirement,
scenario, corpus, catalogue, construct, rule, operation table, adapter contract, universal, domain model); E only
execution's own words. Text patterns, not the logical form: a first cut for the walk-through.
"""
import re, sys
from pathlib import Path
ROOT = Path(sys.argv[1]); sys.path.insert(0, str(ROOT / "scripts"))
import spec_read
W = re.compile(r"set the status of (the|every) (item|context request)|keep a question on the item|set the side of the context request")
R = re.compile(r"item (in a batch )?is `|item is not `|readiness bar|dependency|review limit|chore|request line|item whose status|an item is|the item (holds|has)")
S = re.compile(r"requirement|scenario|corpus|catalogue|construct|rule|operation table|adapter contract|`universal`|domain model|model line|capability|feature|term")
rows, n = [], {"W": 0, "R": 0, "S": 0, "E": 0}
for cap in ("batches", "reviews", "review-guarantees"):
    c = spec_read.capability(ROOT / ("spec/capabilities/%s.md" % cap))
    for g in c.groups:
        for r in g.requirements:
            t = r.text
            k = "W" if W.search(t) else "R" if R.search(t) else "S" if S.search(t) else "E"
            also = "".join(x for x, rx in (("R", R), ("S", S)) if x != k and rx.search(t))
            n[k] += 1
            rows.append("| %s#%s | %s | %s | %s |" % (cap, r.id, k, also or "-", t.replace("|", "/")[:200] + ("..." if len(t) > 200 else "")))
print("Totals: %s of %d lines\n" % (", ".join("%s %d" % kv for kv in n.items()), len(rows)))
print("| line | class | also | text |\n|---|---|---|---|")
print("\n".join(rows))
