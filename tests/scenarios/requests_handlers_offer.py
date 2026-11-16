"""features/requests.feature's offer of a capability (b40, r112-r115): the capability a `work offer --capability`
names written before the run, its group's lines the requirements the Givens say it has (each its own line), its given
block, and its `## Terms` the term its lines mention; a requirement it does not have the line of another capability.
A term no Given wrote is that mentioned term. The Thens read the comment `work offer` posted off the stand-in gh's
calls. Each is a local of work_queue_world's table, taken only in a scenario of features/requests.feature."""
import importlib.util
import sys
from pathlib import Path


def shared(name, file):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
Q = shared("shop_requests_world", "requests_world.py")
local = W.local
TERM = "widget"
GIVEN = "the widget `w-given` holds \"a given line\""
HEAD = ("---\nid: capability/ex.com/prod/ctx/%s\ntitle: %s\nnarrator: a client\ngroup: service\n"
        "language: codified-2\nrests_on: []\nretired: []\n---\n\n# %s\n\n## Purpose\nSomething.\n\n")


def ours(step):
    return Q.feature(step) == "requests"


def line(name, mentions=()):
    """The requirement `name`'s line: it mentions the term of the capability's `## Terms` and each of `mentions`."""
    more = "".join(" It mentions %s." % t for t in mentions)
    return "When the person runs `work start-%s` on a %s, `work` shall print the %s.%s" % (name, TERM, TERM, more)


def capability(name, lines, given=False):
    """A codified-2 capability file of one group holding `lines`, with `## Terms` the term they mention."""
    reqs = "".join("- [r%d] %s\n" % (k, text) for k, text in enumerate(lines, 1))
    block = "\n```given\n%s\n```\n" % GIVEN if given else ""
    return (HEAD % (name, name, name) + "## Terms\n- **%s** (noun): a thing the client keeps. Kind of: thing.\n\n"
            "## Behaviour\n\n### [g1] A %s is printed\n%s%s\n## Dropped\n" % (TERM, TERM, reqs, block))


@local("GivenK", "given block")
def given_block(step):
    """A given block: the one the capability the When names is written with (`GIVEN`)."""
    return None if ours(step) else False


@local("GivenDoes")
@local("GivenDoesNot")
def given_has(step):
    """`the capability c1 has the requirement r2`, or `does not have`: the requirement's line in it, or elsewhere;
    `this bounded context holds the term t1`: the term an entry of the glossary, written at the When;
    `the requirement r1 mentions the term t1`: the term in the glossary and in the requirement's line."""
    if not ours(step):
        return False
    if step.event == "holds" and step.subject == "this bounded context" and step.nps[-1].startswith("the term "):
        step.context.setdefault("glossed", []).append(step.names[-1])
        return None
    if step.event == "mention" and step.subject.startswith("the requirement ") and step.template == "GivenDoes":
        step.context.setdefault("glossed", []).append(step.names[-1])
        step.context.setdefault("mentions", {}).setdefault(step.names[0], []).append(step.names[-1])
        return None
    if step.event != "has" or not step.subject.startswith("the capability "):
        return False
    side = "elsewhere" if step.template == "GivenDoesNot" else step.names[0]
    step.context.setdefault("offer_lines", {})[step.names[1]] = side


def glossary(step):
    """spec/index.md as `work` will read it, each term the Givens put in this bounded context an entry of its
    glossary; a term no Given wrote is the term the capability's lines mention."""
    handlers = next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith(
        "requests_handlers.py"))
    index = step.repo / "spec" / "index.md"
    text = index.read_text() if index.is_file() else ""
    if not text.startswith(handlers.HEAD):
        text = handlers.INDEX + text.partition("## Glossary\n")[2]
    entries = "".join("- **%s** (noun): a thing the context names. Kind of: thing.\n" % t
                      for t in dict.fromkeys(step.context.get("glossed", [])) if "- **%s** (" % t not in text)
    index.write_text(text.replace("## Glossary\n", "## Glossary\n\n" + entries, 1))
    says = step.context.setdefault("says", {})
    for name in step.context.get("glossed", []):
        says[name] = name
    says.setdefault("t1", TERM)


def args(step, given):
    """The arguments of `work offer` for the options the When gives: each capability written first."""
    if "--capability" not in given:
        return []
    name = next(n for n in step.names if (step.repo / "spec" / "capabilities" / ("%s.md" % n)).is_file())
    held = step.context.get("offer_lines", {})
    said = step.context.get("mentions", {})
    mine = [line(r, said.get(r, ())) for r, where in held.items() if where == name] or [line("default")]
    (step.repo / "spec" / "capabilities" / ("%s.md" % name)).write_text(capability(name, mine, given=True))
    others = [line(r) for r, where in held.items() if where == "elsewhere"]
    if others:
        (step.repo / "spec" / "capabilities" / "elsewhere.md").write_text(capability("elsewhere", others))
    glossary(step)
    return ["--capability", name]


def posted(step):
    """The body of the last comment `work` posted."""
    bodies = [argv[argv.index("--body") + 1] for argv in Q.gh_calls(step) if argv[:2] == ["issue", "comment"]]
    assert bodies, ("no comment posted", Q.gh_calls(step))
    return bodies[-1]


def wanted(step):
    """What the comment holds for the step's last noun phrase: a requirement's line, a term's entry, a given block."""
    np, name = step.nps[-1], step.names[-1]
    if np.startswith("the requirement "):
        return line(name)
    if np.startswith("the term "):
        return "**%s**" % step.context.get("says", {}).get(name, name)
    if np.startswith("the given block "):
        return GIVEN
    return None


@local("ThenDoes")
@local("ThenDoesNot")
def then_holds(step):
    if not ours(step) or step.event != "holds" or not step.subject.startswith("the comment "):
        return False
    want = wanted(step)
    if want is None:
        return False
    body = posted(step)
    assert (want not in body) if " not " in step.text else (want in body), (step.text, want, body)
