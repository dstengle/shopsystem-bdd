#!/usr/bin/env python3
"""A job's derived trace, read-only: the serving capability's live lines, the operations they request (in a trigger,
in a response with parameters, and a response's act whose verb names an operation with none), the capabilities those
operations' governing lines are in, followed to a depth, and what each line reads or sets of another area's objects.

usage: job_trace.py <repo root> <capability> [--depth N] [--domain product/domain.md] [--service]
Writes nothing; imports the plugin's own modules from <root>/scripts.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "scripts"))
import domain_model      # noqa: E402
import spec_grammar4     # noqa: E402
import spec_language     # noqa: E402
import spec_lf           # noqa: E402
import spec_vocabulary   # noqa: E402
from spec_lf_core import Atom, Box, Ref  # noqa: E402

CAP = sys.argv[2]
DEPTH = int(sys.argv[sys.argv.index("--depth") + 1]) if "--depth" in sys.argv else 2
DOMAIN = Path(sys.argv[sys.argv.index("--domain") + 1]) if "--domain" in sys.argv else None


def front(path):
    text = path.read_text()
    head = text.split("---", 2)[1] if text.startswith("---") else ""
    return {k.strip(): v.strip() for k, _, v in (ln.partition(":") for ln in head.splitlines()) if v}, text


def lines(text):
    """Live requirement lines of a capability file's ## Behaviour: id -> text (continuation lines joined)."""
    out, cur = {}, None
    body = text.split("## Behaviour", 1)[-1].split("\n## ", 1)[0]
    for ln in body.splitlines():
        m = re.match(r"- \[(r\d+)\] (.*)", ln)
        if m:
            cur = m.group(1)
            out[cur] = m.group(2)
        elif cur and ln.startswith("  ") and ln.strip():
            out[cur] += " " + ln.strip()
        else:
            cur = None
    return out


CAPS = {}
for p in sorted((ROOT / "spec/capabilities").glob("*.md")):
    fm, text = front(p)
    CAPS[p.stem] = (fm, lines(text))
MODEL = domain_model.load(ROOT)
ENTRIES = list(spec_vocabulary.entries(ROOT))
KIND_AREA = {e.term: e.element.area for e in ENTRIES  # the area whose model declares the object
             if e.element is not None and e.element.kind == "object"}
VERB_OPS = defaultdict(list)            # verb -> [(operation, object kind of its frame)]
for e in ENTRIES:
    if e.ref.startswith("operation "):
        m = re.search(r"Frame: <[^>]+> \S+ (?:\w+ )?<([^>]+)>", e.text)
        VERB_OPS[e.term].append((e.ref.split(" ", 1)[1], m.group(1) if m else None))
AREA_CTX, CAP_CTX = {}, {}
if DOMAIN and DOMAIN.exists():          # | context | addresses | shop | today: area:x cap:y |
    for ln in DOMAIN.read_text().splitlines():
        cells = [c.strip(" `") for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0].startswith("bounded-context/"):
            name = cells[0].rsplit("/", 1)[1]
            for kind, what in re.findall(r"(area|cap):([a-z-]+)", cells[3]):
                (AREA_CTX if kind == "area" else CAP_CTX)[what] = name


def ctx(cap):
    """The context a capability is in: a `cap:` of the domain map, else its area's, else its area."""
    if cap is None:
        return "?"
    a = CAPS[cap][0].get("area", "")
    return CAP_CTX.get(cap) or AREA_CTX.get(a, a or "?")


def owner_of_op(op):
    """The capability that specifies an operation's service (frontmatter specifies:), else the one whose lines
    govern it most."""
    service, _, name = op.rpartition(".")
    for cap, (fm, _) in CAPS.items():
        for part in fm.get("specifies", "").split(";"):
            for piece in part.split(","):
                piece = piece.strip()
                if piece.startswith("service " + service):
                    rest = piece[len("service " + service):].strip(": ")
                    if not rest or name in [r.strip() for r in rest.split(",")] or name == rest:
                        return cap
            m = re.match(r"\s*service ([\w -]+): (.*)", part)
            if m and m.group(1).strip() == service and name in [x.strip() for x in m.group(2).split(",")]:
                return cap
    return None


VOCAB = spec_grammar4.load(ROOT)[0]
FORMS = {}


def form_of(cap, rid):
    key = (cap, rid)
    if key not in FORMS:
        parsed = spec_language.parse(ROOT, CAPS[cap][1][rid])
        FORMS[key] = spec_lf.form(VOCAB, parsed.tree) if parsed.tree is not None else None
    return FORMS[key]


def walk(items, neg=False):
    for x in items:
        if isinstance(x, Atom):
            yield x, neg
        elif isinstance(x, Box):
            inner = neg ^ (x.op in ("not", "no"))
            yield from walk(x.body, inner)
            if x.scope:
                yield from walk(x.scope.body, inner)


def refs(atom):
    def flat(v):
        if isinstance(v, Ref):
            yield v
        elif isinstance(v, tuple):
            for w in v:
                yield from flat(w)
    return list(flat(atom.args))


def read(cap, rid):
    """(trigger ops, response ops [(op, how, negated)], sets [(kind, attr, value, negated)], kinds read)."""
    f = form_of(cap, rid)
    if f is None:
        return None
    trig, resp, sets, kinds = [], [], [], set()
    for part in f.parts:
        for a, neg in walk(part.body):
            for r in refs(a):
                if r.origin != "constant":
                    kinds.add(r.kind)
            if part.op in ("when", "if") and a.pred == "request":
                trig.append(a.args[1])
            if part.op != "response":
                continue
            if a.pred == "request":
                resp.append((a.args[1], "request atom", neg))
            elif a.pred == "event" and a.args[1] in VERB_OPS:
                obj = next((r.kind for role, r in a.args[3] if role == "object" and isinstance(r, Ref)), None)
                cands = [o for o, k in VERB_OPS[a.args[1]] if k == obj] or [o for o, _ in VERB_OPS[a.args[1]]]
                for o in cands[:1]:
                    resp.append((o, "event of an operation's verb, no parameters", neg))
            elif a.pred == "initiates":
                sets.append((a.args[2].kind, a.args[3], a.args[4].strip("`"), neg))
    return trig, resp, sets, kinds


def governing(op):
    """Lines (cap, rid) whose trigger requests op."""
    out = []
    cap = owner_of_op(op)
    for c in ([cap] if cap else []) + [k for k in CAPS if k != cap and CAPS[k][0].get("area")]:
        for rid in CAPS[c][1]:
            r = read(c, rid)
            if r and op in r[0]:
                out.append((c, rid))
        if out:
            break
    return out


def area(cap):
    return CAPS[cap][0].get("area", "")


def report():
    home = area(CAP)
    print(f"# trace of {CAP} (area {home}, context {ctx(CAP)}, narrator {CAPS[CAP][0].get('narrator')})")
    seen, frontier, unread = {CAP}, [(CAP, rid) for rid in CAPS[CAP][1]], []
    if "--service" in sys.argv:         # also every line governing an operation of a service CAP specifies
        services = re.findall(r"service ([a-z][\w -]*?)(?:[:,;]|$)", CAPS[CAP][0].get("specifies", ""))
        for c in CAPS:
            if c == CAP or not CAPS[c][0].get("area"):
                continue
            for rid in CAPS[c][1]:
                r = read(c, rid)
                if r and any(op.rpartition(".")[0] in services for op in r[0]):
                    frontier.append((c, rid))
                    seen.add(c)
    reached = defaultdict(set)          # op -> lines that request it
    visited = set(frontier)
    for depth in range(DEPTH + 1):
        nxt = []
        for cap, rid in frontier:
            r = read(cap, rid)
            if r is None:
                unread.append(f"{cap}#{rid}")
                continue
            trig, resp, sets, kinds = r
            outside = sorted(k for k in kinds if KIND_AREA.get(k) and KIND_AREA[k] != area(cap))
            print(f"{'  ' * depth}{cap}#{rid}  trigger={','.join(trig) or '-'}")
            for op, how, neg in resp:
                o = owner_of_op(op)
                tag = "NOT " if neg else ""
                print(f"{'  ' * depth}  -> {tag}{op} [{how}] owner={o} area={area(o) if o else '?'}"
                      f" ctx={ctx(o)}")
                if not neg:
                    reached[op].add(f"{cap}#{rid}")
            for k, t, v, neg in sets:
                if KIND_AREA.get(k) and KIND_AREA[k] != area(cap):
                    print(f"{'  ' * depth}  sets {'NOT ' if neg else ''}{t}({k})={v}  <- {k} is {KIND_AREA[k]}'s")
            if outside:
                print(f"{'  ' * depth}  reads {', '.join(f'{k}({KIND_AREA[k]})' for k in outside)}")
        if depth == DEPTH:
            break
        for op in sorted(reached):
            for c, rid in governing(op):
                if (c, rid) not in visited and (c, rid) not in nxt:
                    nxt.append((c, rid))
        visited |= set(nxt)
        seen |= {c for c, _ in nxt}
        frontier = nxt
        if frontier:
            print(f"--- depth {depth + 1}: lines governing the operations reached")
    print("\n## summary")
    print("capabilities in the trace:", ", ".join(sorted(seen)))
    print("contexts in the trace:", ", ".join(sorted({ctx(c) for c in seen})))
    print("operations reached:", ", ".join(f"{op} ({len(v)})" for op, v in sorted(reached.items())))
    print("lines with no reading:", ", ".join(unread) or "none")


report()
