"""Handlers of features/decision-tiers.feature (workflow simplification plan 6, D16): decision files written under
spec/decisions/ with their tier, status and `enforced_by`, and `model` run on them through design-model-check's
handlers. The steps whose key another capability holds (a design-decision's condition, design-model-check's
`headless`) reach these through work_queue_world's `local` table, so test_decision_tiers.py binds with `bind_all`;
each returns False for a step that is not its own."""
import importlib.util
import re
import sys
from pathlib import Path

from vocab import handler

PATH = "ex.com/prod/ctx"
TIERS = ("check", "requirement", "judgement")


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
local = W.local


def bare(word):
    return word.strip("`")


def says(step, name, value):
    step.context.setdefault("says", {})[name] = value


def decision(step, name, tier=None, status="accepted"):
    """spec/decisions/<name>.md with its id, a summary, the tier and a `## Decision` section; the output names it by
    its path."""
    rel = "spec/decisions/%s.md" % name
    path = step.repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: design-decision/%s/%s\nsummary: s\nstatus: %s\n%s---\n# %s\n\n## Decision\nSo.\n"
                    % (PATH, name, status, "tier: %s\n" % tier if tier else "", name))
    says(step, name, rel)
    return path


def field(step, name, key, value):
    """Set or replace one frontmatter line `key: value` of the decision's file."""
    path = step.repo / "spec" / "decisions" / ("%s.md" % name)
    text = path.read_text()
    head, rest = text[4:].split("\n---\n", 1)
    lines = [line for line in head.splitlines() if not line.startswith(key + ":")] + ["%s: %s" % (key, value)]
    path.write_text("---\n%s\n---\n%s" % ("\n".join(lines), rest))


def fields(step, name):
    path = step.repo / "spec" / "decisions" / ("%s.md" % name)
    head = path.read_text()[4:].split("\n---\n", 1)[0]
    return dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)


@handler("GivenK_A", "design-decision")
def given_decision_is(step):
    """A value among the tiers is the decision's tier (it is accepted); any other is its status."""
    name, value = bare(step.names[0]), bare(step.values[0])
    if (step.repo / "spec" / "decisions" / ("%s.md" % name)).is_file():
        field(step, name, "tier" if value in TIERS else "status", value)
        says(step, name, "spec/decisions/%s.md" % name)
    elif value in TIERS:
        decision(step, name, tier=value)
    else:
        decision(step, name, status=value)


@local("GivenK_C", "design-decision")
def given_unenforced(step):
    """untiered, untested and unrequired: the decision as written gives no tier, no test, no requirement. Any other
    condition (design-model-check's headless) goes on to the registry."""
    if step.text.rsplit(" is ", 1)[1] not in ("untiered", "untested", "unrequired"):
        return False


@handler("GivenR", "supersedes")
def given_supersedes(step):
    new, old = (bare(n) for n in step.names)
    have = re.findall(r"[\w./-]+", fields(step, new).get("supersedes", "").strip("[]"))
    field(step, new, "supersedes", "[%s]" % ", ".join(have + ["design-decision/%s" % old]))
