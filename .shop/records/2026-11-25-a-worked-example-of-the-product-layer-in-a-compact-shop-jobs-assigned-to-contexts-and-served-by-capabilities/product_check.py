#!/usr/bin/env python3
"""The checks a product layer enables, run read-only over a repository and a product layer sketch.

usage: product_check.py <repo root> <product dir> [--serves <overlay>] [--shop <shop.toml>]
The overlay stands in for `serves:` frontmatter that no capability carries yet: lines `<capability> j<n>`.
"""
import re
import subprocess
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

ROOT, PRODUCT = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
OPT = dict(zip(sys.argv[3::2], sys.argv[4::2]))
HERE = Path(__file__).resolve().parent


def front(path):
    text = path.read_text()
    head = text.split("---", 2)[1] if text.startswith("---") else ""
    return {k.strip(): v.strip() for k, _, v in (ln.partition(":") for ln in head.splitlines()) if v}, text


def rows(text, first):
    for ln in text.splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) > 1 and re.match(first, cells[0]):
            yield cells


jobs = {}
for m in re.finditer(r"## \[(j\d+)\] (.*)\n- actor: (.*)", (PRODUCT / "jobs.md").read_text()):
    jobs[m.group(1)] = {"title": m.group(2), "actor": m.group(3).strip()}
domain = (PRODUCT / "domain.md").read_text()
subdomains = {c[0].split()[0]: {"type": c[1], "jobs": re.findall(r"j\d+", c[3])} for c in rows(domain, r"s\d+ ")}
contexts = {c[0].rsplit("/", 1)[1]: {"addresses": re.findall(r"s\d+", c[1]), "shop": c[2],
                                     "today": re.findall(r"(area|cap):([a-z-]+)", c[3]), "id": c[0]}
            for c in rows(domain, r"bounded-context/")}
assigned = defaultdict(list)
for c in rows(domain, r"j\d+$"):
    assigned[c[0]].append(c[1].rsplit("/", 1)[1])

caps = {}
for p in sorted((ROOT / "spec/capabilities").glob("*.md")):
    fm, text = front(p)
    live = len(re.findall(r"^- \[r\d+\]", text, re.M))
    if fm.get("area") and live:              # a live capability of 0.38's form
        caps[p.stem] = {"narrator": fm.get("narrator", ""), "area": fm["area"], "serves": fm.get("serves"),
                        "live": live}
source = "frontmatter `serves:`"
if "--serves" in OPT:
    source = "the overlay " + Path(OPT["--serves"]).name
    for ln in Path(OPT["--serves"]).read_text().splitlines():
        if ln.strip() and not ln.startswith("#"):
            cap, job = ln.split()
            caps[cap]["serves"] = job


def ctx(cap):
    for name, c in contexts.items():
        if ("cap", cap) in c["today"]:
            return name
    for name, c in contexts.items():
        if ("area", caps[cap]["area"]) in c["today"]:
            return name
    return None


served = defaultdict(list)
for cap, c in caps.items():
    if c["serves"]:
        served[c["serves"].rsplit("/", 1)[-1]].append(cap)
out = []


def finding(code, text):
    out.append(f"{code}  {text}")


for j in jobs:
    if len(assigned[j]) != 1:
        finding("p1 job assigned not once", f"{j} assigned to {assigned[j] or 'no context'}")
    if len(served[j]) != 1:
        finding("p2 job served not once", f"{j} served by {served[j] or 'no capability'} ({source})")
    for cap in served[j]:
        if assigned[j] and ctx(cap) != assigned[j][0]:
            finding("p3 served outside its context", f"{j} assigned to {assigned[j][0]}, served by {cap} in {ctx(cap)}")
        if caps[cap]["narrator"] != jobs[j]["actor"]:
            finding("p4 narrator is not the actor", f"{j} actor '{jobs[j]['actor']}', {cap} narrator "
                    f"'{caps[cap]['narrator']}'")
for name, c in contexts.items():
    if not c["today"] or not any(ctx(cap) == name for cap in caps):
        finding("p6 context holds no capability", name)
shop = OPT.get("--shop")
if shop:
    hosted = {h["context"] for h in tomllib.loads(Path(shop).read_text()).get("hosts", [])}
    for name, c in contexts.items():
        if c["id"] not in hosted:
            finding("p7 context hosted by no shop's hosts", f"{c['id']} (map says {c['shop']})")
for s, d in subdomains.items():
    if not any(s in c["addresses"] for c in contexts.values()):
        finding("p8 subdomain no context addresses", s)
    if not d["jobs"]:
        finding("w2 subdomain serves no job", f"{s} ({d['type']})")
traced = {}
for j, cs in served.items():
    if len(cs) != 1 or j not in jobs:
        continue
    run = subprocess.run([sys.executable, str(HERE / "job_trace.py"), str(ROOT), cs[0], "--depth", "3",
                          "--domain", str(PRODUCT / "domain.md")], capture_output=True, text=True)
    m = re.search(r"capabilities in the trace: (.*)", run.stdout)
    traced[j] = set(m.group(1).split(", ")) if m else set()
    ctxs = {ctx(c) for c in traced[j]}
    reach = {s for x in ctxs if x for s in contexts[x]["addresses"]}
    mapped = {s for s, d in subdomains.items() if j in d["jobs"]}
    if mapped - reach:
        finding("p9 trace misses a mapped subdomain", f"{j}: mapped to {sorted(mapped)}, trace reaches "
                f"{sorted(ctxs)} addressing {sorted(reach & mapped)}; missing {sorted(mapped - reach)}")
in_trace = set().union(*traced.values()) if traced else set()
for cap, c in sorted(caps.items()):
    if not c["serves"]:
        finding("w1 capability serves no job" + ("" if cap not in in_trace else " (in a trace)"),
                f"{cap} ({ctx(cap)}, narrator '{c['narrator']}', {c['live']} lines)")
print(f"{len(jobs)} jobs, {len(subdomains)} subdomains, {len(contexts)} contexts, {len(caps)} live capabilities; "
      f"serving from {source}")
print("\n".join(out) or "no findings")
