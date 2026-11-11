"""`model restates`: the coverage of the 0.29 ids (the GF conversion's design §8.3, §15).

Every id of `spec/restated.json` (keyed `<cap>#r<n>`) is restated by a group of a codified capability, listed under
its own capability's `## Dropped` with a reason, or listed there as `moved to <cap>`; a moved id must be restated by a
group of `<cap>` once `<cap>` is codified, and is pending until then. An uncodified capability has nothing dropped, so
its ids are missing until it is converted. An id that another capability's `## Dropped` lists qualified
(`<cap>#r<n>@0.29: <reason>`, a reason that is not a move) is dropped with that reason, as a capability retired in
0.31.0 records the ids moved into it (workflow simplification plan 9, D11); restated by a group still wins."""

import json
import re
from pathlib import Path

import spec_read
from model_parse import frontmatter

MOVED = re.compile(r"^moved to ([a-z0-9]+(?:-[a-z0-9]+)*)\b")


def _key(old):
    cap, _, n = old.partition("#r")
    return cap, int(n)


def coverage(root, capability=None):
    """One row per 0.29 id (of `capability`, or of every capability): {"id", "state", "by", "reason"}, the state
    restated, dropped, pending or missing."""
    root = Path(root)
    files = {p.stem: p for p in sorted((root / "spec" / "capabilities").glob("*.md"))}
    docs = {name: spec_read.capability(p) for name, p in files.items() if spec_read.codified(p)}
    by, gone, elsewhere = {}, {}, {}
    for name, doc in docs.items():
        ident = frontmatter(files[name].read_text())[0].get("id") or name
        for g in doc.groups:
            for cap, n in g.restates:
                by.setdefault((cap, n), []).append(f"{ident}#{g.id}")
        for cap, n, why in doc.dropped:
            if cap == name:
                gone[(cap, n)] = why
            elif not MOVED.match(why):
                elsewhere.setdefault((cap, n), why)
    rows = []
    for old in sorted(spec_read.restated(root), key=_key):
        cap, n = _key(old)
        if capability and cap != capability:
            continue
        row = {"id": old, "state": "missing", "by": by.get((cap, n), []), "reason": gone.get((cap, n))}
        moved = MOVED.match(row["reason"] or "")
        if moved:
            target = moved.group(1)
            if target not in docs:
                row["state"] = "pending"
            elif any(g.split("/")[-1].startswith(f"{target}#") for g in row["by"]):
                row["state"] = "restated"
            if row["state"] != "restated" and (cap, n) in elsewhere:
                row["state"], row["reason"] = "dropped", elsewhere[(cap, n)]
        elif row["by"]:
            row["state"] = "restated"
        elif row["reason"]:
            row["state"] = "dropped"
        elif (cap, n) in elsewhere:
            row["state"], row["reason"] = "dropped", elsewhere[(cap, n)]
        rows.append(row)
    return rows


def text(row):
    moved = MOVED.match(row["reason"] or "")
    if row["state"] == "pending":
        return f"{row['id']}: pending, {row['reason']}, which is not codified yet"
    if moved:
        return f"{row['id']}: {row['reason']}, which does not restate it"
    return f"{row['id']}: neither restated by a group nor dropped nor moved"


def cmd_restates(args):
    rows = coverage(args.root, args.capability)
    if args.capability and not rows:
        print(f"spec/restated.json has no id of {args.capability}")
        return 2
    missing = [r for r in rows if r["state"] == "missing"]
    if args.json:
        print(json.dumps({"ids": rows, "missing": len(missing)}, indent=1))
    else:
        for row in rows:
            if row["state"] in ("missing", "pending"):
                print(text(row))
        counts = {s: len([r for r in rows if r["state"] == s]) for s in ("restated", "dropped", "pending", "missing")}
        print(f"{len(rows)} ids: " + ", ".join(f"{n} {s}" for s, n in counts.items()))
    return 1 if missing else 0
