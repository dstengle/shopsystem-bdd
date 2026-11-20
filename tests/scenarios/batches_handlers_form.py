"""A capability new on an item laid in 0.38's form (b391, batches r76): the Thens read off the batch's branch after
`work batch start`, the capability file conforming to the capability form (frontmatter `area:` and `specifies:`, no
empty section) and spec/index.md to the index form (one `## Composition`, its table `| area | kind | capabilities |`,
the capability named in its area's row), and that the request kept both."""
import re
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
HEADER = re.compile(r"^\|\s*area\s*\|\s*kind\s*\|\s*capabilities\s*\|$")


def _branch(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    return T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()[0]


def _capability(step, name):
    new = step.context["new_capability"][name]
    return new, T.git(step, "show", "%s:spec/capabilities/%s.md" % (_branch(step), new))


def empty_sections(text):
    """The `## ` headings of `text` with nothing but blank lines under them."""
    found = re.finditer(r"(?ms)^## (.+?)[ \t]*\n(.*?)(?=^## |\Z)", text)
    return [m.group(1) for m in found if not m.group(2).strip()]


def capability_form(text):
    """What keeps `text` from conforming to the capability form, or []."""
    head = text.split("\n---", 1)[0] if text.startswith("---\n") else ""
    problems = ["no %s:" % f for f in ("area", "specifies") if not re.search(r"(?m)^%s: \S" % f, head)]
    return problems + ["the empty section ## %s" % s for s in empty_sections(text)]


def index_form(text, capability, area):
    """What keeps spec/index.md `text` from conforming to the index form, with `capability` in `area`'s row, or []."""
    sections = re.findall(r"(?m)^## Composition[ \t]*$", text)
    if len(sections) != 1:
        return ["%d ## Composition sections" % len(sections)]
    body = re.search(r"(?ms)^## Composition[ \t]*\n(.*?)(?=^## |\Z)", text).group(1)
    rows = [r.strip() for r in body.splitlines() if r.strip().startswith("|")]
    if not rows or not HEADER.match(rows[0]):
        return ["no table | area | kind | capabilities |: %s" % rows[:1]]
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows[2:]]
    mine = [c for c in cells if c[0] == area]
    if len(mine) != 1 or capability not in [n.strip().strip("`") for n in mine[0][2].split(",")]:
        return ["no row of the area %s naming %s: %s" % (area, capability, cells)]
    return []


@four("ThenDoes", "conform", *BOTH)
def conforms(step):
    (k1, n1), form = parts(step)[0], step.nps[0]
    if (k1, form) == ("capability", "the capability form"):
        _, text = _capability(step, n1)
        assert not capability_form(text), (capability_form(text), text)
    elif (k1, form) == ("index file", "the index form"):
        name = next(iter(step.context["new_capability"]))
        new, text = _capability(step, name)
        area = re.search(r"(?m)^area: (\S+)", text).group(1)
        index = T.git(step, "show", "%s:spec/index.md" % _branch(step))
        assert not index_form(index, new, area), (index_form(index, new, area), index)
    else:
        return False


@four("ThenDoes", "keep", *BOTH)
def keeps(step):
    """`the batches service keeps the capability c1` (its file on the batch's branch), `keeps the index file i2`."""
    k, name = parts(step)[1]
    if k == "capability":
        _capability(step, name)
    elif k == "index file":
        T.git(step, "show", "%s:spec/index.md" % _branch(step))
    else:
        return False
