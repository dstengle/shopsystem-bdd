"""feature-file-tools' scenario world in the step grammar 4 (b240 phase 21): its Givens are recorded as instances
(`a feature file f1`) and facts (`the feature file f1 has the scenario s2`, `no binding binds the scenario s1`), and
the files they describe are written when the command runs (`build`): a feature file for each feature file instance
(`features/<f>.feature`, under its subdirectory's name when one holds it), each scenario in its feature file (else in
`features/f0.feature`) with its tags, its docstring and its `Deprecated for:` line, an outline with its examples rows, a
rule block, and a test module for each (`tests/test_<t>.py`) with a `scenario(...)` or `scenarios(...)` call for each
binding. `value` gives what an instance is in a command's arguments and output: a scenario's title (`find s2` when its
title contains a search text, which is `find`), a feature file's or a test module's path, a tag (`@t1`, a requirement
tag `@r901`).

`OWN` holds this feature's handlers by (template, term): test_feature_file_tools.py's step definitions take each step
of the feature to them first (`dispatch`), so a key another feature's handler holds in the registry stays its own;
`own` also registers a handler where the registry has none for its key, so that `features vocab --check` finds one."""
import sys
from pathlib import Path

OWN = {}
SEARCH = "find"


def own(template, *terms, registry=True):
    """With `registry=False`, OWN's only: a key another feature's handler claims in the registry, loaded later."""
    vocab = sys.modules["vocab"]

    def mark(fn):
        for term in terms or (None,):
            OWN[(template, term)] = fn
            if registry and vocab.lookup(template, term) is None:
                vocab.handler(template, term)(fn)
        return fn
    return mark


def dispatch(root, keyword):
    """The step function of one keyword: a step of this feature to its OWN handler, else to the registry's."""
    import pytest
    vocab = sys.modules["vocab"]
    fallback = vocab._step_function(root, keyword)

    def step_function(text, request, docstring=None, datatable=None):
        call = vocab.vocab4.step(root, keyword, text, request)
        if call is None:
            return fallback(text, request, docstring, datatable)
        call.docstring, call.datatable, call.fixtures = docstring, datatable, request.getfixturevalue
        found = OWN.get((call.template, call.term)) or vocab.lookup(call.template, call.term)
        if found is None:
            pytest.fail("no handler for %s %s: %s" % (call.template, call.term, text), pytrace=False)
        return found(call)
    return step_function


def bind(namespace, root):
    """One step definition for each keyword in a test module's namespace, ahead of the conftest's."""
    import pytest
    from pytest_bdd.steps import StepFunctionContext
    vocab = sys.modules["vocab"]
    for keyword in ("given", "when", "then"):
        context = StepFunctionContext(type=keyword, step_func=dispatch(str(root), keyword),
                                      parser=vocab.vocab4.Parser(root, keyword))
        name = "pytestbdd_stepdef_%s_feature_file_tools" % keyword
        namespace[name] = pytest.fixture(name=name)(vocab._marker(context))


# --- the record ---------------------------------------------------------------------------------------------------
def world(step):
    return step.context.setdefault("ff", {"kinds": {}, "facts": [], "values": {}})


def ref(text):
    """What a noun phrase names: an instance's name ("the scenario s2"), ("no", K) of "no K", or a code as it is."""
    if text.startswith("no "):
        return ("no", text[3:])
    return text if text.startswith("`") else text.split()[-1]


def record(step, polarity=True):
    """A Given's fact: (verb, subject, object, polarity), each side a name, ("no", K) or a code."""
    subject = ref(step.subject)
    obj = ref(step.nps[0]) if step.nps else None
    world(step)["facts"].append((step.term, subject, obj, polarity))


def kind(w, name):
    return w["kinds"].get(name) if isinstance(name, str) else None


def facts(w, verb, k1=None, k2=None):
    """The positive facts of `verb` whose subject is of kind k1 and object of kind k2 (None: any)."""
    return [(a, b) for v, a, b, pos in w["facts"] if v == verb and pos and (k1 is None or kind(w, a) in k1)
            and (k2 is None or kind(w, b) in k2)]


# --- the files ----------------------------------------------------------------------------------------------------
SCENARIOS, TAGS = ("scenario", "replacement"), ("tag", "requirement tag")


def title(w, s):
    """A scenario's title: its name, after the search text when its scenario title contains one."""
    searched = {t for t, _ in facts(w, "contain", ("scenario title",), ("search text",))}
    if any(s2 == s and t in searched for s2, t in facts(w, "has", SCENARIOS, ("scenario title",))):
        return "%s %s" % (SEARCH, s)
    return s


def tag(w, t):
    if isinstance(t, str) and t.startswith("`"):
        return t.strip("`")
    names = [n for n, k in w["kinds"].items() if k in TAGS]
    return "@r%d" % (901 + names.index(t)) if kind(w, t) == "requirement tag" else "@" + t


def files(w):
    """{feature file name: its relative path}, with the default `f0` when a scenario has no feature file."""
    under = {f: d for d, f in facts(w, "holds", ("subdirectory",), ("feature file",))}
    out = {n: "features/%s%s.feature" % (under[n] + "/" if n in under else "", n)
           for n, k in w["kinds"].items() if k == "feature file"}
    return out


def free(w):
    """The scenarios a feature file is written with: each but those found in a file of the example data."""
    return [s for s, k in w["kinds"].items() if k in SCENARIOS and s not in w["values"]]


def owner(w, s):
    for f, s2 in facts(w, "has", ("feature file",), SCENARIOS):
        if s2 == s:
            return f
    for s1, r in facts(w, "has", ("scenario",), ("replacement",)):
        if r == s:
            return owner(w, s1)
    return "f0"


def value(w, name):
    """What an instance is in arguments and output."""
    k = kind(w, name)
    if name in w["values"]:
        return w["values"][name]
    if k in SCENARIOS:
        return title(w, name)
    if k == "scenario title":
        return next(title(w, s) for s, t in facts(w, "has", SCENARIOS, ("scenario title",)) if t == name)
    if k in TAGS:
        return tag(w, name)
    if k == "search text":
        return SEARCH
    if k == "feature file":
        return files(w).get(name, "features/%s.feature" % name)
    if k == "test module":
        return "tests/test_%s.py" % name
    return name.strip("`")


def feature_text(w, f):
    """The text of the feature file f: its tags, its rule block, its scenarios and outlines."""
    tags = [tag(w, t) for f2, t in facts(w, "has", ("feature file",), TAGS) if f2 == f]
    rule = [r for f2, r in facts(w, "has", ("feature file",), ("rule block",)) if f2 == f]
    pad = "    " if rule else "  "
    out = (" ".join(tags) + "\n" if tags else "") + "Feature: %s\n" % f + ("  Rule: %s\n" % rule[0] if rule else "")
    docs = [d for f2, d in facts(w, "has", ("feature file",), ("docstring",)) if f2 == f]
    scenarios = [s for s in free(w) if owner(w, s) == f]
    if rule and not scenarios:
        scenarios = ["under"]
    for n, s in enumerate(scenarios):
        own_tags = [tag(w, t) for s2, t in facts(w, "has", SCENARIOS) if s2 == s and (kind(w, t) in TAGS or
                                                                                      str(t).startswith("`@"))]
        out += (pad + " ".join(own_tags) + "\n" if own_tags else "") + pad + "Scenario: %s\n" % value(w, s)
        out += "".join(pad + "  Deprecated for: %s\n" % value(w, r) for s1, r in facts(w, "has", ("scenario",),
                                                                                        ("replacement",)) if s1 == s)
        out += pad + "  Given a step\n"
        if n == 0 and docs:
            inside = [tag(w, t) if kind(w, t) in TAGS else "Scenario: %s" % t
                      for d, t in facts(w, "contain", ("docstring",)) if d in docs]
            out += "".join(pad + "    %s\n" % line for line in ['"""'] + inside + ['"""'])
    for f2, o in facts(w, "has", ("feature file",), ("scenario outline",)):
        if f2 == f:
            rows = [e for o2, e in facts(w, "has", ("scenario outline",), ("examples row",)) if o2 == o]
            out += pad + "Scenario Outline: %s\n%s  Given a <n> step\n%s  Examples:\n%s    | n |\n" % (o, pad, pad, pad)
            out += "".join(pad + "    | %s |\n" % e for e in rows)
    return out


def module_text(w, m, paths):
    """The text of the test module m: a call for each of its bindings."""
    out = "from pytest_bdd import scenario, scenarios\n"
    held = [b for m2, b in facts(w, "has", ("test module",), ("binding", "scenarios call")) if m2 == m]
    for b in held:
        target = [s for b2, s in facts(w, "bind") if b2 == b]
        s = target[0] if target else None
        feature = Path(paths.get(owner(w, s), "features/f0.feature")).name if isinstance(s, str) else "f0.feature"
        if kind(w, b) == "scenarios call":
            out += 'scenarios("%s")\n' % feature
        else:
            out += '\n\n@scenario("%s", "%s")\ndef test_%s():\n    pass\n' % (
                feature, value(w, s) if isinstance(s, str) else "no such title", b)
    return out


def build(step):
    """Write the files the Givens describe into the scenario's repository."""
    w, repo = world(step), step.repo
    paths = files(w)
    if any(owner(w, s) == "f0" for s in free(w)) or not paths:
        paths["f0"] = "features/f0.feature"
    for f, rel in paths.items():
        _write(repo / rel, feature_text(w, f))
    modules = [n for n, k in w["kinds"].items() if k == "test module"]
    loose = [b for b, k in w["kinds"].items() if k in ("binding", "scenarios call")
             and not any(b2 == b for _, b2 in facts(w, "has", ("test module",)))]
    if loose:
        modules.append("bindings")
        w["facts"] += [("has", "bindings", b, True) for b in loose]
        w["kinds"]["bindings"] = "test module"
    (repo / "tests").mkdir(exist_ok=True)
    for m in modules:
        _write(repo / value(w, m), module_text(w, m, paths))


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
