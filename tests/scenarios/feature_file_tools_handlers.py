"""feature-file-tools' handlers in the step grammar 4 (b240 phase 21): a Given records an instance or a fact in
feature_file_tools_world, the When writes the files they describe (`build`, or for `features generate` and `features
vocab` feature_file_tools_capability) and runs `features` with the command's options and their
arguments, each argument an instance's value; the Thens read what it printed and how it exited, an instance named by
its value (a scenario by its title, a feature file by its path, a tag as written).

Example data of a capability and of its feature file (g106, g107, g110) is written as the given block holds it, and an
instance the Givens bind to it takes what it holds (`a capability c1`, the scenario of its feature file)."""
import importlib.util
import re
import shlex
import sys
from pathlib import Path


def shared(name, file):
    """A world module loaded once by path, the one the other modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_feature_file_tools_world", "feature_file_tools_world.py")
GEN = shared("shop_feature_file_tools_capability", "feature_file_tools_capability.py")

INDEX = "---\nid: bounded-context/ex.com/prod/ctx\n---\n# ctx\n\n## Glossary\n\n"
KINDS = ("feature file", "scenario", "scenario title", "tag", "requirement tag", "docstring", "scenario line",
         "scenario outline", "examples row", "rule block", "subdirectory", "replacement", "search text", "binding",
         "scenarios call", "test module", "step", "feature", "requirement", "requirement group", "universal condition",
         "capability", "handler")
FILES = ("`features count`", "`features list`", "`features deprecated`", "`features bindings`")


def write(step, rel, text):
    path = step.repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


# --- the Givens ---------------------------------------------------------------------------------------------------
@W.own("GivenCodeText", "feature file", "capability")
def given_data(step):
    """Example data: the file the given block holds (a capability under spec/capabilities/, with an index)."""
    name = step.names[0].strip("`")
    if step.term == "capability":
        if not (step.repo / "spec" / "index.md").is_file():
            write(step, "spec/index.md", INDEX)
        name = "spec/capabilities/%s.md" % name
    write(step, name, step.docstring + "\n")


@W.own("GivenK", *KINDS)
def given_k(step):
    w, name = W.world(step), step.names[0]
    w["kinds"][name] = step.kind
    caps = sorted((step.repo / "spec" / "capabilities").glob("*.md"))
    if step.kind == "capability" and caps:      # the example data's capability
        w["values"][name] = caps[0].stem


@W.own("GivenDoes", "has", "contain", "bind", "use", "conform", "entail", "holds")
def given_does(step):
    W.record(step)
    w = W.world(step)
    a, b = w["facts"][-1][1:3]
    if W.kind(w, a) == "capability" and W.kind(w, b) == "feature":
        w["values"][b] = "features/%s.feature" % W.value(w, a)
    if W.kind(w, a) == "feature" and W.kind(w, b) in ("scenario", "step"):     # what the example's feature holds
        w["values"].setdefault(a, GEN.feature(w, a))
        text = (step.repo / w["values"][a]).read_text()
        pattern = r"^\s*Scenario: (.*)$" if W.kind(w, b) == "scenario" else r"^\s*(?:Given|When|Then) (.*)$"
        w["values"][b] = re.findall(pattern, text, re.MULTILINE)[0]


@W.own("GivenDoesNot", "has")
def given_does_not(step):
    W.record(step, False)


@W.own("GivenK_A", "capability")
def given_attribute(step):
    """`the capability c1 is `codified-2``: the attribute's value written into the example's capability, or kept for
    the capability the When writes."""
    w = W.world(step)
    w.setdefault("attrs", {})[step.attribute] = step.values[0].strip("`")
    name = w["values"].get(step.names[0])
    if name:
        path = step.repo / "spec" / "capabilities" / ("%s.md" % name)
        field = {"group": "group", "language": "language"}[step.attribute]
        path.write_text(re.sub(r"^%s: .*$" % field, "%s: %s" % (field, step.values[0].strip("`")), path.read_text(),
                               count=1, flags=re.MULTILINE))


# --- the When -----------------------------------------------------------------------------------------------------
def argument(w, text):
    return text.strip("`") if text.startswith("`") else W.value(w, W.ref(text))


@W.own("WhenRuns", *FILES, "`features generate`", "`features vocab`")
def runs(step):
    w = W.world(step)
    names = GEN.prepare(step) if step.command not in FILES else W.build(step) or []
    args = shlex.split(step.command.strip("`"))[1:]
    for code, text in step.options:
        args += [code.strip("`")] + ([argument(w, text)] if text else [])
    step.context["result"] = step.run("features", *args, *names)


# --- the Thens ----------------------------------------------------------------------------------------------------
def result(step):
    done = step.context["result"]
    assert "Traceback" not in done.stderr, done.stderr
    return done


def said(step, np):
    """What output shows of a noun phrase: a number as `total <n>`, a code as it is, an instance by its value."""
    w = W.world(step)
    if np.startswith("the number of scenarios of "):
        f = W.ref(np)
        return "total %d" % sum(W.owner(w, s) == f for s in W.free(w))
    if np.startswith("the number of examples rows of "):
        o = W.ref(np)
        return "total %d" % len([e for o2, e in W.facts(w, "has", ("scenario outline",)) if o2 == o])
    return argument(w, np)


@W.own("ThenPrints", "`features`")
def prints(step):
    out = result(step).stdout
    for np in step.nps:
        assert said(step, np) in out, (said(step, np), out)


@W.own("ThenPrintsNot", "`features`")
def prints_not(step):
    done = result(step)
    for np in step.nps:
        assert said(step, np) not in done.stdout, (said(step, np), done.stdout)


@W.own("ThenExitsErr", "`features`")
def exits_err(step):
    done = result(step)
    assert done.returncode != 0, done.stdout
    for np in step.nps:
        assert said(step, np) in done.stdout + done.stderr, (said(step, np), done.stdout, done.stderr)


@W.own("ThenDoes", "write", registry=False)
@W.own("ThenDoes", "refuse", "name", "has")
def then_does(step):
    done, w = result(step), W.world(step)
    if step.term == "refuse":
        assert done.returncode != 0, done.stdout
    elif step.term == "name":
        assert said(step, step.nps[0]) in done.stdout + done.stderr, (step.nps[0], done.stdout, done.stderr)
    elif step.term == "has":
        GEN.has(step, w)
    else:
        GEN.writes(step, w)


@W.own("ThenDoesNot", "write", registry=False)
def then_does_not(step):
    GEN.writes_not(step, W.world(step))


def unoverstated(step):
    """`features does not write the file f1` (requests' handler of ThenDoesNot write, when a capability condition of
    the codified-2 world kept what its feature must hold and must not under `generated`): `features generate` wrote
    the capability's feature, which holds the one and not the other."""
    result(step)
    assert step.context["result"].returncode == 0, step.context["result"].stderr
    kept, entailed = step.context["generated"]
    texts = [p.read_text() for p in sorted((step.repo / "features").glob("*.feature"))]
    assert texts, "features generate wrote no feature file"
    assert any(kept.search(t) for t in texts), (kept.pattern, texts)
    assert not any(entailed.search(t) for t in texts), (entailed.pattern, texts)
