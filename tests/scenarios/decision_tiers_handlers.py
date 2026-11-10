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
    condition = step.text.rsplit(" is ", 1)[1]
    if condition not in ("untiered", "untested", "unrequired"):
        return False
    step.context.setdefault(condition, set()).add(bare(step.names[0]))


@handler("GivenR", "supersedes")
def given_supersedes(step):
    new, old = (bare(n) for n in step.names)
    have = re.findall(r"[\w./-]+", fields(step, new).get("supersedes", "").strip("[]"))
    field(step, new, "supersedes", "[%s]" % ", ".join(have + ["design-decision/%s" % old]))


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


@local("GivenK_C", "test")
def given_failing_test(step):
    """failing: the test also asserts False. Any other condition goes on to the registry."""
    name = bare(step.names[0])
    if not step.text.endswith(" is failing") or name not in step.context.get("says", {}):
        return False
    write(step, "tests/test_%s.py" % name, source(step, name, failing=True))


@handler("GivenR", "enforced by")
def given_enforced_by(step):
    name, by = (bare(n) for n in step.names)
    have = [x.strip() for x in fields(step, name).get("enforced_by", "").strip("[]").split(",") if x.strip()]
    field(step, name, "enforced_by", "[%s]" % ", ".join(have + [step.context["says"][by]]))


@handler("WhenRuns", "`model decisions --check`")
def model_decisions_check(step):
    H.run_model(step, "decisions")
    H.run_model(step, "decisions", "--check")
    step.context["decisions_run"] = True


@local("ThenDoes", "test")
def uses_test(step):
    """`model` uses the test: its id is on a `holds` or `failing` line, and the test ran. Only after `model decisions
    --check`: the registry's `use` is the batches' (a batch's plan)."""
    if step.term != "use" or not step.context.get("decisions_run"):
        return False
    done, name = step.context["result"], bare(step.names[0])
    said = step.context["says"][name]
    assert any(line.startswith(("holds ", "failing ")) and said in line for line in done.stdout.splitlines()), \
        (said, done.stdout)
    assert name in (outside(step) / "ran").read_text().split(), done.stdout


ARGUMENTS = (("--summary", "One sentence."), ("--decision", "So it is."), ("--tier", "judgement"))


@handler("GivenK", "argument")
def given_argument(step):
    """The arguments `work decision` requires, in order of mention: --summary, --decision, --tier."""
    have = step.context.setdefault("arguments", {})
    have[bare(step.names[0])] = ARGUMENTS[len(have)][0]
    says(step, bare(step.names[0]), have[bare(step.names[0])])


@handler("GivenK_C", "argument")
def given_absent(step):
    """absent: the command is run without it; not absent, with it. An argument no Given named is its option."""
    gone = step.context.setdefault("absent", set())
    option = step.context.get("arguments", {}).get(bare(step.names[0]), bare(step.names[0]))
    if " is not " in step.text:
        gone.discard(option)
    else:
        gone.add(option)


@handler("WhenRuns", "`work decision`")
def work_decision(step, extra=()):
    """`work decision` in the repository, committed first, with a title, a summary, the decision's text and the tier
    `judgement`: no `--tier` where the step names a decision a Given made untiered, and none of the arguments a Given
    made absent."""
    H.base(step.repo, step.context)
    step.context["head"] = W.init(step.repo)
    named = [bare(n) for n in step.names]
    gone = set(step.context.get("absent", ()))
    if set(named) & step.context.get("untiered", set()):
        gone.add("--tier")
    title = named[0] if named and named[0] not in step.context.get("arguments", {}) else "Decided once"
    given = [word for option, value in ARGUMENTS if option not in gone for word in (option, value)]
    step.context["work_decision"] = True
    step.context["result"] = step.run("work", "decision", title, *given, *extra)


@handler("WhenRuns", "`work decision --verified-by`")
def work_decision_routed(step):
    """`work decision` as above with `--verified-by check`: the decision it writes must hold the route."""
    work_decision(step, ("--verified-by", "check"))
    done = step.context["result"]
    if done.returncode == 0:
        step.context.setdefault("holds", {})[done.stdout.strip()] = re.compile(r"^verified_by: \[check\]$", re.M)


@local("ThenExitsErr")
def decision_refused(step):
    """After `work decision`: an error naming each code the step names (`--tier`) and each argument it names."""
    if not step.context.get("work_decision"):
        return False
    done = step.context["result"]
    assert done.returncode != 0, done.stdout
    for np in step.nps:
        for word in (w.strip("`") for w in np.split() if w.startswith("`")):
            assert word in done.stderr, (word, done.stderr)
    for name in step.names:
        assert step.context["says"][bare(name)] in done.stderr, (name, done.stderr)
