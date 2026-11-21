"""Handlers of features/decisions.feature's `work decision --amend` (b458, r21-r23): the When that amends a
design-decision with an enforcer or a foundation, and the Thens of the decision amended in place (the scenario's d2,
the decision d1 as it now reads: the one id under `enforced_by` or `rests_on` added, nothing else of it changed),
committed with the decisions index. Each takes a step only after a When that ran `work decision --amend`
(`amending`)."""
import subprocess
import sys

W = sys.modules["shop_work_queue_world"]
D = sys.modules.get("shop_decision_tiers_handlers")
H = sys.modules.get("shop_design_model_check_handlers")
# what the scenario's enforcer and foundation are: a test that holds a decision, the universal condition it rests on
GIVEN = {"enforcer": ("--enforced-by", "enforced_by", "tests/test_e.py::test_e"),
         "foundation": ("--rests-on", "rests_on", "universal-condition/ex.com/prod/ctx/u9")}
INDEX = "spec/decisions/index.md"


def tiers():
    """decision_tiers_handlers.py, loaded once under its shared name."""
    global D, H
    if D is None:
        import importlib.util
        from pathlib import Path
        spec = importlib.util.spec_from_file_location("shop_decision_tiers_handlers",
                                                      Path(__file__).with_name("decision_tiers_handlers.py"))
        D = sys.modules["shop_decision_tiers_handlers"] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(D)
    H = sys.modules["shop_design_model_check_handlers"]
    return D


@W.local("WhenRuns")
def amends(step):
    """`work decision --amend <d1's id>` with `--enforced-by` or `--rests-on` set to the one the step names, in the
    repository committed first; the decision's text before it kept to compare."""
    options = {o.strip("`"): v for o, v in getattr(step, "options", None) or ()}
    if not str(step.term).startswith("`work decision") or "--amend" not in options:
        return False
    tiers()
    H.base(step.repo, step.context)
    name = options["--amend"].split()[-1]
    path = step.repo / "spec" / "decisions" / ("%s.md" % name)
    words = ["--amend", "design-decision/%s/%s" % (D.PATH, name)]
    added = {}
    for option, key, value in GIVEN.values():
        if option in options:
            words += [option, value]
            added[key] = value
    step.context["head"] = W.init(step.repo)
    step.context["amending"] = {"path": path, "before": path.read_text(), "added": added}
    step.context["result"] = step.run("work", "decision", *words)


def done(step):
    result = step.context["result"]
    assert result.returncode == 0, result.stderr
    return step.context["amending"]


def committed(step, rel):
    """HEAD is a commit that changed `rel`, which it holds as the file now is."""
    head = subprocess.run(["git", "show", "HEAD:%s" % rel], cwd=step.repo, capture_output=True, text=True)
    assert head.returncode == 0, head.stderr
    assert head.stdout == (step.repo / rel).read_text(), head.stdout
    changed = subprocess.run(["git", "show", "--name-only", "--format=", "HEAD"], cwd=step.repo, capture_output=True,
                             text=True).stdout.split()
    assert rel in changed, changed


def kept(step):
    """`the decisions service keeps the design-decision d2` (the decision amended) or `... this decisions index`."""
    amending = done(step)
    rel = INDEX if "decisions index" in step.text else amending["path"].relative_to(step.repo).as_posix()
    committed(step, rel)


def has(step):
    """`the design-decision d2 has the enforcer e2` (the foundation f2): the decision amended names the id under its
    list, and reads as it did with only that list's line changed."""
    amending = done(step)
    key = "enforced_by" if " enforcer " in step.text else "rests_on"
    text = amending["path"].read_text()
    head = text[4:].split("\n---\n", 1)[0].splitlines()
    line = next((x for x in head if x.startswith(key + ":")), "")
    assert amending["added"][key] in line, text
    before = [x for x in amending["before"].splitlines() if not x.startswith(key + ":")]
    assert [x for x in text.splitlines() if not x.startswith(key + ":")] == before, text


@W.local("ThenDoes")
def amended(step):
    if "amending" not in step.context:
        return False
    if step.term == "has" and (" enforcer " in step.text or " foundation " in step.text):
        return has(step)
    if step.term in ("keep", "write", "commit") and ("design-decision" in step.text or "decisions index" in step.text):
        return kept(step)
    return False
