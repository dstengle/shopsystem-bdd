"""Requirements moved to new capability files with new ids (the domain contract design, §9.2), and the old ids resolved.

`apply(root, table, capabilities)` writes the move a session's table says: `table` a TSV of rows `old id, new
capability, new group title, new text` (a new capability `-` drops the line, its text the reason), `capabilities` a
TSV of the new capability files (`name, area, specifies, narrator, group, title, purpose`). Each new capability file
gets its frontmatter (`area:`, `specifies:`, `narrator`, `group`, `language: codified-2`, `retired: []`, `unbuilt:
[]`), `## Purpose` and `## Behaviour`, one group a row (rows of one new capability and one title in a row are one
group), its ids from r1/g1, or past the highest id an old file of the same name held (`batches`, `trials`: renamed
`<name>-0.37.md` with `git mv` before, so that an old id stays one id); a moved group keeps its `Restates:` line,
qualified by its old capability, and its given block. Each old capability's groups leave `## Behaviour`, every id
goes into `retired:`, a `## Moved` table names each old id's new one, and a dropped line's `Restates:` ids go under
`## Dropped`. `spec/moves.json` holds the whole map, `<cap>#r<n>` and `<cap>#g<n>` to the new id or null.

`resolve(root, old_id)` gives an old id's new one (null when it was dropped, the id itself when moves.json names it
not), read by `model check`'s retired-id facts, by the `Restates:` and `request_lines` readers. `problems(root)` gives
a moves.json that misses a retired id of a moved capability or names one new id twice.
"""
import csv
import json
import re
import textwrap
from collections import OrderedDict
from pathlib import Path

from shop_refused import Refused

MOVES = "spec/moves.json"
CONTEXT = "capability/missingmass.io/shopsystem/shopsystem-bdd/"
GROUP = re.compile(r"^### \[g(\d+)\] (.*)$")
REQ = re.compile(r"^- \[r(\d+)\] ")
_CACHE = {}


def _rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [r for r in csv.reader(f, delimiter="\t") if r and not r[0].startswith("#")]


def _sections(text):
    """(head, [(heading, lines)]) of a markdown file split at its `## ` headings."""
    head, out = [], []
    for line in text.splitlines():
        if line.startswith("## "):
            out.append((line, []))
        elif out:
            out[-1][1].append(line)
        else:
            head.append(line)
    return head, out


def _groups(lines):
    """{g<n>: {"title", "restates", "given", "ids"}} of a `## Behaviour` section's lines."""
    out, cur, fence = OrderedDict(), None, False
    for line in lines:
        m = GROUP.match(line)
        if m and not fence:
            cur = out.setdefault("g" + m.group(1), {"title": m.group(2), "restates": [], "given": [], "ids": []})
        elif cur is None:
            continue
        elif fence:
            cur["given"].append(line)
            fence = line.strip() != "```"
        elif line.strip() == "```given":
            cur["given"].append(line)
            fence = True
        elif line.startswith("Restates:"):
            cur["restates"] += [t.strip() for t in line[9:].strip().rstrip(".").split(",") if t.strip()]
        elif REQ.match(line):
            cur["ids"].append("r" + REQ.match(line).group(1))
    return out


def _qualified(token, cap):
    return token if "#" in token else "%s#%s" % (cap, token)


def _frontmatter_list(head, key, ids):
    out = []
    for line in head:
        if line.startswith(key + ":"):
            old = [t.strip() for t in line.split(":", 1)[1].strip().strip("[]").split(",") if t.strip()]
            line = "%s: [%s]" % (key, ", ".join(dict.fromkeys(old + ids)))
        out.append(line)
    return out


def _highest(text):
    """The highest r<n> or g<n> a capability file's groups, requirements and `retired:` hold."""
    ids = re.findall(r"^### \[g(\d+)\]|^- \[r(\d+)\]", text, re.M)
    retired = re.search(r"^retired: \[(.*)\]", text, re.M)
    found = [int(a or b) for a, b in ids] + [int(t) for t in re.findall(r"[rg](\d+)", retired.group(1) if retired else "")]
    return max(found or [0])


def _wrap(prefix, text):
    return textwrap.wrap(prefix + text, 120, subsequent_indent="  ", break_long_words=False, break_on_hyphens=False)


def apply(root, table, capabilities):
    """Write the move of `table` with the new capabilities of `capabilities`; the map written to moves.json."""
    root = Path(root)
    caps = {r[0]: dict(zip(("name", "area", "specifies", "narrator", "group", "title", "purpose"), r))
            for r in _rows(capabilities)}
    rows = _rows(table)
    seen = [r[0] for r in rows]
    if len(seen) != len(set(seen)):
        raise Refused("the move names %s twice" % sorted({s for s in seen if seen.count(s) > 1})[0])
    old = {}
    for old_id in seen:
        cap = old_id.split("#")[0]
        if cap not in old:
            path = root / "spec" / "capabilities" / ("%s.md" % cap)
            if not path.is_file():
                path = root / "spec" / "capabilities" / ("%s-0.37.md" % cap)
            head, secs = _sections(path.read_text(encoding="utf-8"))
            behaviour = next((ls for h, ls in secs if h.strip() == "## Behaviour"), [])
            old[cap] = {"path": path, "head": head, "secs": secs, "groups": _groups(behaviour)}
    for cap, o in old.items():
        live = {"%s#%s" % (cap, r) for g in o["groups"].values() for r in g["ids"]}
        missing = sorted(live - set(seen))
        if missing:
            raise Refused("the move misses %s" % missing[0])
    group_of = {"%s#%s" % (cap, r): g for cap, o in old.items() for g, d in o["groups"].items() for r in d["ids"]}
    moves, new_files, dropped = OrderedDict(), OrderedDict(), {}
    for old_id, new_cap, title, text in rows:
        cap = old_id.split("#")[0]
        g = group_of[old_id]
        gd = old[cap]["groups"][g]
        if new_cap == "-":
            moves[old_id] = None
            moves.setdefault("%s#%s" % (cap, g), None)
            dropped.setdefault(cap, []).extend((_qualified(t, cap), text) for t in gd["restates"])
            continue
        if new_cap not in caps:
            raise Refused("the move names the capability %s, which the capabilities table does not" % new_cap)
        f = new_files.setdefault(new_cap, {"groups": [], "n": None})
        if f["n"] is None:
            reused = root / "spec" / "capabilities" / ("%s-0.37.md" % new_cap)
            f["n"] = _highest(reused.read_text(encoding="utf-8")) if reused.is_file() else 0
            f["g"] = f["n"]
        last = f["groups"][-1] if f["groups"] else None
        if last is None or last["title"] != title:
            f["g"] += 1
            last = {"id": "g%d" % f["g"], "title": title, "restates": [], "given": [], "reqs": []}
            f["groups"].append(last)
        f["n"] += 1
        rid = "r%d" % f["n"]
        last["reqs"].append((rid, text))
        moves[old_id] = "%s#%s" % (new_cap, rid)
        key = "%s#%s" % (cap, g)
        if key not in moves:
            moves[key] = "%s#%s" % (new_cap, last["id"])
            last["restates"] += [_qualified(t, cap) for t in gd["restates"]]
            last["given"] += gd["given"]
    for name, f in new_files.items():
        _write_new(root, caps[name], f)
    for cap, o in old.items():
        _retire(cap, o, moves, dropped.get(cap, []))
    path = root / MOVES
    current = json.loads(path.read_text()) if path.is_file() else {}
    current.update(moves)
    path.write_text(json.dumps(current, indent=1) + "\n", encoding="utf-8")
    _CACHE.clear()
    return moves


def _write_new(root, c, f):
    path = root / "spec" / "capabilities" / ("%s.md" % c["name"])
    lines = ["---", "id: %s%s" % (CONTEXT, c["name"]), "title: %s" % c["title"], "narrator: %s" % c["narrator"],
             "group: %s" % c["group"], "area: %s" % c["area"], "specifies: %s" % c["specifies"],
             "language: codified-2", "retired: []", "unbuilt: []", "---", "", "# %s" % c["title"], "", "## Purpose"]
    lines += textwrap.wrap(c["purpose"], 120) + ["", "## Behaviour"]
    for g in f["groups"]:
        lines += ["", "### [%s] %s" % (g["id"], g["title"])]
        if g["restates"]:
            lines.append("Restates: %s." % ", ".join(g["restates"]))
        for rid, text in g["reqs"]:
            lines += _wrap("- [%s] " % rid, text)
        lines += g["given"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _retire(cap, o, moves, dropped):
    ids = [i for g, d in o["groups"].items() for i in [g] + d["ids"]]
    head = _frontmatter_list(o["head"], "retired", ids)
    out = list(head)
    secs = [(h, ls) for h, ls in o["secs"] if h.strip() not in ("## Moved",)]
    for h, ls in secs:
        name = h.strip()
        if name == "## Behaviour":
            ls = [""]
        elif name in ("## Terms", "## Relations"):
            ls = ["", "Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).", ""]
        elif name == "## Dropped" and dropped:
            ls = [x for x in ls if x.strip()] + ["- %s@0.29: %s" % (t.replace("@0.29", ""), why) for t, why in dropped]
            ls = [""] + ls + [""]
        out += [h] + ls
    if dropped and not any(h.strip() == "## Dropped" for h, _ in secs):
        out += ["## Dropped", ""] + ["- %s@0.29: %s" % (t.replace("@0.29", ""), why) for t, why in dropped] + [""]
    out += ["## Moved", "", "Every line moved to a new capability with a new id (the domain contract, 0.38.0).", "",
            "| old | new |", "|---|---|"]
    for i in ids:
        new = moves.get("%s#%s" % (cap, i))
        out.append("| %s | %s |" % (i, new or "dropped"))
    o["path"].write_text("\n".join(out).rstrip("\n") + "\n", encoding="utf-8")


def load(root):
    """{old id: new id or None} of `spec/moves.json`, read once per state of the file."""
    path = Path(root) / MOVES
    if not path.is_file():
        return {}
    key = (str(path), path.stat().st_mtime_ns)
    if key not in _CACHE:
        _CACHE.clear()
        _CACHE[key] = json.loads(path.read_text(encoding="utf-8"))
    return _CACHE[key]


def resolve(root, old_id):
    """The id `old_id` names now: its move's new id, None when it was dropped, else `old_id` itself."""
    moves = load(root)
    seen = set()
    while old_id in moves and old_id not in seen:
        seen.add(old_id)
        old_id = moves[old_id]
        if old_id is None:
            return None
    return old_id


def problems(root):
    """Each new id moves.json names twice, as a message."""
    news = [v for v in load(root).values() if v]
    return ["spec/moves.json names %s twice" % v for v in sorted({v for v in news if news.count(v) > 1})]
