"""The index file a batch opened keeps (batches r113-r115, b606): a capability of the world's codified spec with no
requirement (`shelved`, its every line retired, named in the index's `## Composition` before the batch is opened) or
with one (`supervision`, which that Composition does not name), and the Thens read off spec/index.md on the batch's
branch after `work batch start`: it conforms to the index form (one `## Composition`, its one table `| area | kind |
capabilities |`, each capability with a requirement named in its area's row), holds a capability (named in a row) or
does not hold it (named nowhere in the index)."""
import re
import sys

import spec_read

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
HEADER = re.compile(r"^\|\s*area\s*\|\s*kind\s*\|\s*capabilities\s*\|$")
SHELVED = ("---\nid: capability/ex.com/prod/ctx/shelved\ntitle: Shelved\nnarrator: the person\ngroup: service\n"
           "language: codified-2\nretired: [g1, r1]\n---\n\n# Shelved\n\n## Purpose\nThings once shelved.\n\n"
           "## Behaviour\n")
COMPOSITION = ("\n\n## Composition\n\nThe capabilities, by area.\n\n| area | kind | capabilities |\n|---|---|---|\n"
               "| work-queue | core | work-queue |\n| shelved | core | shelved |\n\n### Retired\n\n`shelved`.\n")


def first(template, term):
    """`four`, the handler put first in its key's chain."""
    def mark(fn):
        four(template, term, *BOTH)(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


def _spec(step):
    """The world's codified spec, its index given a Composition that names `work-queue` and `shelved`, and the
    capability file of `shelved`, which has no requirement."""
    R = sys.modules["shop_readiness_world"]
    R.codify(step)
    spec = step.repo / "spec"
    if not step.context.get("composed"):
        index = spec / "index.md"
        index.write_text(index.read_text().rstrip("\n") + COMPOSITION)
        (spec / "capabilities" / "shelved.md").write_text(SHELVED)
        step.context["composed"] = True
    return spec


@first("GivenDoes", "has")
def has(step):
    """`the capability c1 has no requirement` (`shelved`), `the capability c1 has the requirement r1` (`supervision`,
    the fixture's, with three)."""
    named = parts(step)
    if [k for k, _ in named][:2] != ["capability", "requirement"]:
        return False
    _spec(step)
    capability = "shelved" if "has no" in step.text else "supervision"
    step.context.setdefault("index_capability", {})[named[0][1]] = capability


def _index(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branch = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()[0]
    return branch, T.git(step, "show", "%s:spec/index.md" % branch)


def rows(text):
    """The cells of each row of the one table under `## Composition` in `text`, or None when it is not there."""
    found = re.search(r"(?ms)^## Composition[ \t]*\n(.*?)(?=^## |\Z)", text)
    lines = [r.strip() for r in found.group(1).splitlines() if r.strip().startswith("|")] if found else []
    if not lines or not HEADER.match(lines[0]):
        return None
    return [[c.strip() for c in r.strip("|").split("|")] for r in lines[2:]]


def named(cells):
    return [n.strip().strip("`") for n in cells[2].split(",") if n.strip()]


def problems(step, branch, text):
    """What keeps the index `text` from the index form: each capability on `branch` with a requirement named in its
    area's row (its `area:`, else its name)."""
    if len(re.findall(r"(?m)^## Composition[ \t]*$", text)) != 1:
        return ["not one ## Composition"]
    table = rows(text)
    if table is None:
        return ["no table | area | kind | capabilities |"]
    found = []
    listed = T.git(step, "ls-tree", "--name-only", "%s:spec/capabilities" % branch).split()
    for name in (n[:-3] for n in listed if n.endswith(".md")):
        body = T.git(step, "show", "%s:spec/capabilities/%s.md" % (branch, name))
        if not any(spec_read.REQ.match(line) for _, line in spec_read.numbered(body, "Behaviour")):
            continue
        area = (re.search(r"(?m)^area: (\S+)", body.split("\n---", 1)[0]) or [None, name])[1]
        if not any(c[0] == area and name in named(c) for c in table):
            found.append("%s not in the row of %s" % (name, area))
    return found


@first("ThenDoes", "conform")
def conforms(step):
    (k1, _), form = parts(step)[0], step.nps[0]
    if (k1, form) != ("index file", "the index form") or "new_capability" in step.context:
        return False
    branch, text = _index(step)
    assert not problems(step, branch, text), (problems(step, branch, text), text)


@first("ThenDoes", "hold")
@first("ThenDoes", "holds")
@first("ThenDoesNot", "hold")
@first("ThenDoesNot", "holds")
def holds(step):
    """`the index file i2 holds the capability c1` (named in a row of its table), `... does not hold ...` (named
    nowhere in the index)."""
    (k1, _), (k2, n2) = parts(step)
    if (k1, k2) != ("index file", "capability"):
        return False
    capability = step.context["index_capability"][n2]
    _, text = _index(step)
    if step.template == "ThenDoes":
        assert any(capability in named(c) for c in rows(text) or []), (capability, text)
    else:
        assert not re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(capability), text), (capability, text)
