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
H = shared("shop_design_model_check_handlers", "design_model_check_handlers.py")   # design-model-check's run_model
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
    """Set or replace one frontmatter line `key: value` of the decision's file; with None, take it away."""
    path = step.repo / "spec" / "decisions" / ("%s.md" % name)
    text = path.read_text()
    head, rest = text[4:].split("\n---\n", 1)
    lines = [line for line in head.splitlines() if not line.startswith(key + ":")]
    lines += ["%s: %s" % (key, value)] if value is not None else []
    path.write_text("---\n%s\n---\n%s" % ("\n".join(lines), rest))


def fields(step, name):
    path = step.repo / "spec" / "decisions" / ("%s.md" % name)
    head = path.read_text()[4:].split("\n---\n", 1)[0]
    return dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)


@handler("GivenK_A", "design-decision")
def given_decision_is(step):
    """A value among the tiers is the decision's tier (it is accepted); any other is its status. "is not v" leaves the
    decision as it is unless it is v (its status `accepted`, no tier); "has no tier" takes its tier away."""
    name = bare(step.names[0])
    path = step.repo / "spec" / "decisions" / ("%s.md" % name)
    if not path.is_file():
        decision(step, name)
    says(step, name, "spec/decisions/%s.md" % name)
    if not step.values:
        return field(step, name, step.attribute, None)
    value = bare(step.values[0])
    key = "tier" if value in TIERS else "status"
    if " is not " in step.text:
        if fields(step, name).get(key) == value:
            field(step, name, key, "accepted" if key == "status" else None)
    else:
        field(step, name, key, value)


UNIVERSAL = ("---\nid: capability/%s/universal\ntitle: Universal conditions\nnarrator: every trace\ngroup: guarantees\n"
             "language: codified-2\nretired: []\n---\n\n# Universal conditions\n\n## Behaviour\n\n%s")


@handler("GivenK", "universal condition")
def given_universal(step):
    """spec/universal.md with the condition [U<n>], a statement that parses; output names it by its id."""
    have = step.context.setdefault("universal", [])
    have.append(int(re.sub(r"\D", "", bare(step.names[0])) or 1))
    write(step, "spec/universal.md", UNIVERSAL % (PATH, "".join(
        "- [U%d] `work` shall commit every transition.\n" % n for n in have)))
    says(step, bare(step.names[0]), "universal-condition/%s/u%d" % (PATH, have[-1]))


def write(step, rel, text):
    path = step.repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def outside(step):
    """A directory outside the repository, where a test leaves the mark that it ran."""
    if "outside" not in step.context:
        step.context["outside"] = step.fixtures("tmp_path_factory").mktemp("outside")
    return step.context["outside"]


def source(step, name, failing=False):
    mark = str(outside(step) / "ran")
    return "def test_%s():\n    open(%r, 'a').write(%r)\n%s" % (name, mark, name + "\n",
                                                                "    assert False\n" if failing else "")


@local("GivenK", "test")
def given_test(step):
    """tests/test_<t>.py, whose test marks that it ran outside the repository and passes. analysis-tools' test (it
    imports `cart`) is the registry's, and its feature does not bind with `bind_all`."""
    name = bare(step.names[0])
    write(step, "tests/test_%s.py" % name, source(step, name))
    says(step, name, "tests/test_%s.py::test_%s" % (name, name))


@handler("WhenRuns", "`model decisions --check`")
def model_decisions_check(step):
    H.run_model(step, "decisions")
    H.run_model(step, "decisions", "--check")
    step.context["decisions_run"] = True


ARGUMENTS = (("--summary", "One sentence."), ("--decision", "So it is."), ("--tier", "judgement"))


@handler("WhenRuns", "`work decision`")
def work_decision(step):
    """`work decision` in the repository, committed first, with a title, a summary, the decision's text and the tier
    `judgement`, but each option the step runs it without; with `--verified-by`, the route `check`."""
    H.base(step.repo, step.context)
    step.context["head"] = W.init(step.repo)
    gone = {bare(o) for o in getattr(step, "without", None) or ()}
    given = [word for option, value in ARGUMENTS if option not in gone for word in (option, value)]
    if "--verified-by" in {bare(o) for o, _ in getattr(step, "options", None) or ()}:
        given += ["--verified-by", "check"]
    step.context["result"] = step.run("work", "decision", "Decided once", *given)
