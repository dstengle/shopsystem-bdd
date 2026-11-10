"""The capabilities of feature-file-tools' `features generate` and `features vocab` scenarios (b240 phase 21), written
before the command (`prepare`) and read by its Thens:

- a capability every requirement of which conforms to the language reference and uses the `shall` construct (r108):
  one group for each "shall" example of the construct catalogue `grammar/constructs.md`, but those of the constructs
  `grammar/language.md` says `model logic` and `features generate` do not read yet (`EXCLUDED`), in the catalogue's
  context `grammar/corpus/constructs/`, three of its groups with a given block of example data (a docstring, a table
  and one value);
- a capability one of whose steps a universal condition entails (r109): codified2_world's declining lines and U1;
- else the capability of the example data, run on by no name.

`has` (`the requirement group r3 has the scenario s1`: every group of the capability has its scenario in the feature;
`the capability c1 has the feature f1`), `writes` and `writes_not` are the Thens."""
import importlib.util
import re
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[2]
CONTEXT = PLUGIN / "grammar" / "corpus" / "constructs" / "spec" / "index.md"
NAME, PATH = "c1", "ex.com/prod/ctx"
GIVEN = [["the file `a.txt` holds:", "  one line", "  another line"],
         ["the file `b.txt` holds:", "  | step | count |", "  | Given | 2 |"],
         ['the file `c.txt` holds "3.0.0"']]


def shared(name, file):
    """A world module loaded once by path, the one the other modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_feature_file_tools_world", "feature_file_tools_world.py")


def _codified2():
    return shared("shop_codified2_world", "codified2_world.py")


def excluded():
    """The construct codes language.md's section #16 names: the lines `model logic` does not read yet."""
    text = (PLUGIN / "grammar" / "language.md").read_text()
    part = text.split("\n### #16: history, moments", 1)[1].split("\n#", 1)[0]
    return set(re.findall(r"`([a-z][a-z-]+)`", part)) - {"model", "features"}


def examples():
    """(code, line) of each "shall" example of the catalogue whose construct `model logic` reads."""
    text = (PLUGIN / "grammar" / "constructs.md").read_text()
    found = re.findall(r"^## (\S+)\n.*?```construct\n(.*?)\n(.*?)\n", text, re.DOTALL | re.MULTILINE)
    out = excluded()
    return [(code, line) for code, line, form in found if form.startswith("shall") and code not in out]


def constructs(repo):
    groups = []
    for k, (code, line) in enumerate(examples(), 1):
        block = "\n```given\n%s\n```\n" % "\n".join(GIVEN[k - 1]) if k <= len(GIVEN) else ""
        groups.append("### [g%d] %s\n- [r%d] %s\n%s" % (k, code, k, line, block))
    cap = ("---\nid: capability/%s/%s\ntitle: %s\nnarrator: a client\ngroup: service\nlanguage: codified-2\n"
           "rests_on: []\nretired: []\n---\n\n# %s\n\n## Purpose\nSomething.\n\n## Behaviour\n\n%s\n## Not yet\n"
           % (PATH, NAME, NAME, NAME, "\n".join(groups)))
    W._write(repo / "spec" / "index.md", CONTEXT.read_text())
    W._write(repo / "spec" / "capabilities" / ("%s.md" % NAME), cap)
    return len(groups)


def prepare(step):
    """The capability the Givens describe, written; the names the command runs on."""
    w = W.world(step)
    verbs = {v for v, *_ in w["facts"]}
    if "entail" in verbs:
        C2 = _codified2()
        C2.context(step.repo, PATH, C2.CAPABILITIES["declining"], NAME, C2.UNIVERSAL["declining"])
        w["entailed"] = tuple(re.compile(p, re.MULTILINE) for p in C2.GENERATED["declining"])
    elif "conform" in verbs:
        w["groups"] = constructs(step.repo)
    else:
        return []
    for c in [n for n, k in w["kinds"].items() if k == "capability"]:
        w["values"][c] = NAME
    return [NAME]


def feature(w, f):
    """The path of the feature f: its capability's feature, or the one feature of the example data."""
    caps = [c for c, f2 in W.facts(w, "has", ("capability",)) if f2 == f]
    if caps:
        return "features/%s.feature" % W.value(w, caps[0])
    return w["values"].get(f, "features/shelf.feature")


def has(step, w):
    a, b = step.names[:2]
    if W.kind(w, a) == "capability" or step.subject.startswith("the capability"):
        w["values"][b] = "features/%s.feature" % W.value(w, a)
        assert (step.repo / w["values"][b]).is_file(), w["values"][b]
    elif step.subject.startswith("the requirement group"):
        text = (step.repo / "features" / ("%s.feature" % NAME)).read_text()
        missing = [g for g in range(1, w["groups"] + 1) if not re.search(r"^  @g%d @" % g, text, re.MULTILINE)]
        assert not missing, "no scenario of the groups %s" % missing
    else:       # `the scenario s1 has the scenario title s2`: the title it was written with
        w["values"][b] = W.value(w, a)


def writes(step, w):
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    name = step.names[0]
    if name in w["values"] and str(w["values"][name]).startswith("features/"):
        assert (step.repo / w["values"][name]).is_file(), w["values"][name]


def writes_not(step, w):
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    kept, entailed = w["entailed"]
    text = (step.repo / "features" / ("%s.feature" % NAME)).read_text()
    assert kept.search(text) and not entailed.search(text), text
