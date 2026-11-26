"""Handlers of checking's scenarios of a term that redefines a verb of the request pack (r162, r163, b847), each a
`work_queue_world.local` that takes only a step of a scenario of their groups (`mine`). The world is
design_model_check_worlds_redefines' fixture, written at the When: the verb return of the notes layer naming the
operation `notes.return`, which notebook's r10 requests, `Redefines: request`, its frame `the person returns <note>` (g162: its senses told apart
from the pack's `service returns thing`) or `<actor> returns <note>` (g163: a term that violates `v_t15`, an agent's
frame overlapping the pack's); the term t1 the verb return, and g162's t2 too, the term the grammar would spell itself
(`v_t6`) were the pack's sense not kept beside it. `spec check` run, and the Thens read its exit and output: no row
of `v_t6` names return (g162), a row of `v_t15` names return and the pack `request` (g163)."""
import importlib.util
import re
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


W = _sibling("work_queue_world.py", "shop_work_queue_world")
R = _sibling("design_model_check_worlds_redefines.py", "shop_design_model_check_worlds_redefines")
GROUPS = {"g162", "g163"}
WORD = "return"
LINE = "\n### [g10] A note returned is kept\n- [r10] %s\n" % R.REDEFINED     # the line that requests notes.return


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("redefines", {"terms": [], "violates": set(), "keeps": set()})


def given_instance(step):
    """a term t1 (t2)."""
    if not mine(step) or step.kind != "term":
        return False
    world(step)["terms"].append(step.names[0])


def given_state(step):
    """the term t1 redefines `request`; the term t1 violates (does not violate) `v_t15`; the term t2 violates
    `v_t6`."""
    if not mine(step) or step.term not in ("redefine", "violate"):
        return False
    if step.term == "violate":
        code = step.nps[-1].strip("`")
        (world(step)["violates"] if not step.template.endswith("Not") else world(step)["keeps"]).add(code)


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    R.fixture(step.repo, overlapping="v_t15" in world(step)["violates"])
    notebook = step.repo / "spec" / "capabilities" / "notebook.md"
    notebook.write_text(notebook.read_text() + LINE)
    for args in (("features", "generate"), ("spec", "annotate")):
        done = step.run(*args)
        assert done.returncode == 0, done.stdout + done.stderr
    step.context["result"] = step.run("spec", "check")


def rows(done, code):
    """The rows `spec check` printed under the rule `code`'s heading."""
    found, inside = [], False
    for line in done.stdout.splitlines():
        if re.match(r"^\S", line):
            inside = line.split()[0] == code
        elif inside:
            found.append(line.strip())
    return found


def then_ok(step):
    """the specification service completes this request: `spec check` exits 0."""
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


def then_not_returned(step):
    """the specification service does not return the term t2: no row of `v_t6` names return."""
    if not mine(step) or "result" not in step.context or not step.names:
        return False
    done = step.context["result"]
    assert not [r for r in rows(done, "v_t6") if re.search(r"\b%s\b" % WORD, r)], done.stdout


def then_failed(step):
    """the specification service fails this check: `spec check` exits 1."""
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr


def then_does(step):
    """the specification service names the term t1, names `request`: a row of `v_t15` names return, and the pack;
    `spec check` exits 1."""
    if not mine(step) or "result" not in step.context or step.term not in ("fail", "name"):
        return False
    done = step.context["result"]
    assert done.returncode == 1, done.stdout + done.stderr
    if step.term == "name":
        said = " ".join(rows(done, "v_t15"))
        word = WORD if step.names else step.nps[-1].strip("`")
        assert re.search(r"\b%s\b" % re.escape(word), said), done.stdout


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("GivenDoesNot")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(then_ok)
W.local("ThenPrintsNot")(then_not_returned)
W.local("ThenDoes")(then_does)
W.local("ThenExitsErr")(then_failed)
