"""The relations of a context (design-r2 §4.2, §8): the `## Relations` tables, `Kind of:` expanded, v_t8 and v_t10.

A row of a `## Relations` table, in `spec/index.md` or in a capability for its own local relations, is
`| from kind | word | to kind |`, with an optional fourth cell for cardinality; the table's header and its rule are
not rows. A relation entry (`- **fulfils** (relation initiative → request): ...`) is no row: it is v_t8. A row
whose kind is a supertype (a kind entry's `Kind of:`) expands to each of its subkinds, at any depth, and keeps its
own: (stage, for, node) gives (stage, for, node), (stage, for, work-item), ..., all with the one relation id of the
row. spec_lexicon calls `read` and gives `expand` as `Lexicon.relations()` and
`problems` among its own.
"""
import re
from collections import defaultdict, namedtuple
from pathlib import Path

Row = namedtuple("Row", "k1 word k2 cardinality where")


def _cells(line):
    return [c.strip().strip("`").strip() for c in line.strip().strip("|").split("|")]


def rows(text, where):
    """The rows of the `## Relations` tables of one file's text."""
    out, inside, table = [], False, []

    def close():
        body = table[2:] if len(table) > 1 and all(set(c) <= set("-: ") for c in table[1]) else table
        out.extend(Row(c[0], c[1], c[2], c[3] if len(c) > 3 else "", where) for c in body if len(c) >= 3)
        table.clear()
    for line in text.splitlines():
        if line.startswith("## "):
            close()
            inside = line[3:].strip() == "Relations"
        elif inside and line.strip().startswith("|"):
            table.append(_cells(line))
        elif table:
            close()
    close()
    return out


def read(root):
    """The rows of `spec/index.md` and of every capability file, in that order."""
    root = Path(root)
    paths = [root / "spec" / "index.md"] + sorted((root / "spec" / "capabilities").glob("*.md"))
    return [r for p in paths if p.is_file() for r in rows(p.read_text(), p.relative_to(root).as_posix())]


def slug(word):
    return re.sub(r"[^a-z0-9]+", "_", word.lower()).strip("_") or "x"


def subkinds(lexicon):
    """{kind: every kind under it, at any depth}."""
    direct = defaultdict(set)
    for t in lexicon.of("kind"):
        if t.supertype:
            direct[t.supertype].add(t.term)
    out = {}
    for k in {t.term for t in lexicon.of("kind")} | set(direct):
        seen, todo = set(), [k]
        while todo:
            for s in direct.get(todo.pop(), ()):
                if s not in seen and s != k:
                    seen.add(s)
                    todo.append(s)
        out[k] = seen
    return out


def rid(row):
    return "r_%s_%s_%s" % (slug(row.k1), slug(row.word), slug(row.k2))


def expansion(lexicon):
    """(k1, word, k2, rid, source row) for every row expanded to its subkinds, the supertype's own kept."""
    subs = subkinds(lexicon)
    out = []
    for row in lexicon.rows:
        for a in sorted({row.k1} | subs.get(row.k1, set())):
            for b in sorted({row.k2} | subs.get(row.k2, set())):
                out.append((a, row.word, b, rid(row), row))
    return out


def expand(lexicon):
    """The relations as sorted, distinct (k1, word, k2, rid)."""
    return sorted({e[:4] for e in expansion(lexicon)})


def problems(lexicon):
    """v_t4 (a row or a `Kind of:` naming no kind), v_t8 (a relation entry: a relation is a row) and v_t10
    (two rows giving one (from, word, to)), as (code, term, message)."""
    kinds = lexicon.kind_names()
    out = [("v_t4", t.term, "%s: Kind of: %s is not a kind" % (t.where, t.supertype))
           for t in lexicon.of("kind") if t.supertype and t.supertype not in kinds]
    for row in lexicon.rows:
        out += [("v_t4", row.word, "%s: the relation row %s %s %s names %s, which is not a kind"
                 % (row.where, row.k1, row.word, row.k2, k)) for k in (row.k1, row.k2) if k not in kinds]
    out += [("v_t8", t.term, "%s: the relation %s (%s) is an entry; write it as a row of ## Relations"
             % (t.where, t.term, " → ".join(t.kinds))) for t in lexicon.of("relation")]
    given = defaultdict(set)
    for a, word, b, _, row in expansion(lexicon):
        given[(a, word, b)].add(row)
    for (a, word, b), found in sorted(given.items()):
        if len(found) > 1:
            out.append(("v_t10", word, "the relation %s %s %s is given by %d rows (%s)" % (
                a, word, b, len(found), "; ".join(sorted("%s %s %s in %s" % (r.k1, r.word, r.k2, r.where)
                                                         for r in found)))))
    return out
