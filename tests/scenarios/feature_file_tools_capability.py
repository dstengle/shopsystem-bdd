"""The capabilities of feature-file-tools' `features generate` and `features vocab` scenarios (b240 phase 21), written
before the command (`prepare`) and read by its Thens:

- a capability every requirement of which conforms to the language reference and uses the `shall` construct (r108):
  one group for each "shall" example of the construct catalogue `grammar/constructs.md`, but those of the constructs
  `grammar/language.md` says `spec logic` and `features generate` do not read yet (`EXCLUDED`) and those read in
  another context (a request's, `- Context:`), in the catalogue's
  context `grammar/corpus/constructs/`, three of its groups with a given block of example data (a docstring, a table
  and one value);
- a capability one of whose steps a universal condition entails (r109): codified2_world's declining lines and U1;
- a capability whose requirement uses `holds-relation` and `only` or `count` (r113, r112, b272): codified2_constructs'
  holding or capping line, and the Then its feature must hold (`uses`);
- a capability whose requirement uses `param-of` or governs an operation that makes a referent (b418):
  feature_file_tools_request's;
- a capability whose requirement uses `no-noun`, `rc-object` and `named` and a step that has an ambiguous text:
  feature_file_tools_ambiguous's (b733);
- a capability whose requirement uses a construct (b274): its catalogue example (feature_file_tools_uses), of
  `no-noun`, `of-relation` and a code a no box of two atoms (b716);
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
USES = shared("shop_feature_file_tools_uses", "feature_file_tools_uses.py")
COL = shared("shop_feature_file_tools_collections", "feature_file_tools_collections.py")
REQ = shared("shop_feature_file_tools_request", "feature_file_tools_request.py")     # b418
AMB = shared("shop_feature_file_tools_ambiguous", "feature_file_tools_ambiguous.py")     # b733


def _codified2():
    return shared("shop_codified2_world", "codified2_world.py")


def excluded():
    """The construct codes language.md's section #16 names: the lines `spec logic` does not read yet."""
    text = (PLUGIN / "grammar" / "language.md").read_text()
    part = text.split("\n### #16: history, moments", 1)[1].split("\n#", 1)[0]
    return set(re.findall(r"`([a-z][a-z-]+)`", part)) - {"model", "spec", "features"}


def examples():
    """(code, line) of each "shall" example of the catalogue whose construct `spec logic` reads."""
    text = (PLUGIN / "grammar" / "constructs.md").read_text()
    found = re.findall(r"^## (\S+)\n(.*?)```construct\n(.*?)\n(.*?)\n", text, re.DOTALL | re.MULTILINE)
    out = excluded()     # and an example read in another context than the catalogue's (a request's)
    return [(code, line) for code, head, line, form in found if form.startswith("shall") and code not in out
            and "- Context:" not in head]


def capability(repo, groups):
    """The capability c1 of the groups' text, in the construct catalogue's context."""
    cap = ("---\nid: capability/%s/%s\ntitle: %s\nnarrator: a client\ngroup: service\nlanguage: codified-2\n"
           "rests_on: []\nretired: []\n---\n\n# %s\n\n## Purpose\nSomething.\n\n## Behaviour\n\n%s\n## Not yet\n"
           % (PATH, NAME, NAME, NAME, groups))
    W._write(repo / "spec" / "index.md", CONTEXT.read_text())
    W._write(repo / "spec" / "capabilities" / ("%s.md" % NAME), cap)


def constructs(repo):
    groups = []
    for k, (code, line) in enumerate(examples(), 1):
        block = "\n```given\n%s\n```\n" % "\n".join(GIVEN[k - 1]) if k <= len(GIVEN) else ""
        groups.append("### [g%d] %s\n- [r%d] %s\n%s" % (k, code, k, line, block))
    capability(repo, "\n".join(groups))
    return len(groups)


# (the constructs a requirement uses) -> codified2_constructs' world of them
HELD = {frozenset({"`holds-relation`", "`only`"}): "holding", frozenset({"`holds-relation`", "`count`"}): "capping"}


def prepare(step):
    """The capability the Givens describe, written; the names the command runs on."""
    w = W.world(step)
    verbs = {v for v, *_ in w["facts"]}
    used = frozenset(b for v, a, b, pos in w["facts"] if v == "use" and pos and W.kind(w, a) == "requirement")
    if used in HELD and COL.kind(w, W.kind) != "capped":     # with an upper bound, its counter-example (b296)
        held = shared("shop_codified2_constructs", "codified2_constructs.py")
        held.capability(step, PATH, HELD[used])
        w["uses"] = step.context["holds"]["features/%s.feature" % held.NAME]
        for c in [n for n, k in w["kinds"].items() if k == "capability"]:
            w["values"][c] = held.NAME
        return [held.NAME]
    if "entail" in verbs:
        C2 = _codified2()
        C2.context(step.repo, PATH, C2.CAPABILITIES["declining"], NAME, C2.UNIVERSAL["declining"])
        w["entailed"] = tuple(re.compile(p, re.MULTILINE) for p in C2.GENERATED["declining"])
    elif "conform" in verbs:
        w["groups"] = constructs(step.repo)
    elif USES.unlinked(step, w, NAME, PATH):     # a no box of two atoms (b716)
        w["groups"] = 1
    elif AMB.mine(w, W.kind):     # a code that reads two ways bare (b733)
        AMB.prepare(step, w, capability, step.repo / "spec" / "index.md")
        w["groups"] = 1
    elif COL.kind(w, W.kind):     # every, only, counts and two (b273)
        w["lines"] = COL.kind(w, W.kind)
        COL.bind(w, W.kind)     # b732
        capability(step.repo, COL.groups(w["lines"]))
        w["groups"] = len(COL.LINES[w["lines"]])
    elif REQ.prepare(step, w, W.kind, NAME, PATH):     # a request's parameters, an operation that makes (b418)
        w["groups"] = 1
    elif not USES.prepare(step, w, W._write, NAME, PATH):     # a capability of one construct (b274)
        return []
    else:
        w["groups"] = 1     # its one group, the construct's (b288)
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
    elif step.nps[0].startswith("the order counter-example"):      # b275
        USES.counter(step, NAME)
    elif step.nps[0].startswith(("the counter-example", "the boundary")):    # b273
        if step.subject.startswith("the scenario"):
            collections(step, w, step.nps[0].split()[1])
    elif b in w["values"]:      # a title printed before: the scenario's own
        assert w["values"][b] == W.value(w, a), (step.text, w["values"][b], W.value(w, a))
    else:       # `the scenario s1 has the scenario title s2`: the title it was written with
        w["values"][b] = W.value(w, a)


def writes(step, w):
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    name = step.names[0]
    if name in w["values"] and str(w["values"][name]).startswith("features/"):
        assert (step.repo / w["values"][name]).is_file(), w["values"][name]


def collections(step, w, what):
    """The feature of the lines of every, only, counts and two read back for `what` (feature_file_tools_collections'
    `check`)."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    COL.check(w["lines"], (step.repo / "features" / ("%s.feature" % NAME)).read_text(), what)


def unused(step, w):
    """`the counter-example c3 does not use the code c2`: no step of the counter-example's member holds the code
    (b732)."""
    assert result_ok(step) and w.get("lines"), step.text
    COL.unused((step.repo / "features" / ("%s.feature" % NAME)).read_text(), W.value(w, step.names[-1]))


def valueless(step, w):
    """`the counter-example c2 uses `has-no-value``: the scenario holds the lines' patterns and each counter-example's
    member has no value of the attribute (b743)."""
    assert result_ok(step) and w.get("lines"), step.text
    text = (step.repo / "features" / ("%s.feature" % NAME)).read_text()
    COL.check(w["lines"], text, "counter-example")
    COL.valueless(text, step.nps[-1])


def uses(step, w):
    """`the scenario s1 uses `only``: the feature written holds the Then of the construct's world."""
    assert result_ok(step)
    text = (step.repo / "features" / "shelf.feature").read_text()
    assert w["uses"].search(text), (w["uses"].pattern, text)


def result_ok(step):
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    return True


def writes_not(step, w):
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    if w.get("ambiguous"):      # every step of one parse (b733)
        return AMB.check(step.repo, NAME)
    if w.get("lines"):      # a step that asserts what only allows (r118), one that names an unbrought instance (r116)
        return collections(step, w, "assert" if w["lines"] == "only" else "introduce")
    kept, entailed = w["entailed"]
    text = (step.repo / "features" / ("%s.feature" % NAME)).read_text()
    assert kept.search(text) and not entailed.search(text), text
