"""Handlers of features/decision-tiers.feature's `work decision --supersedes` (b179, r31): the Thens of the status
`work` set on the decision superseded, that decision committed, the decision written and what it supersedes. Each
takes a step only after a When that ran `work decision --supersedes` (decision_tiers_handlers' `superseding`)."""
import subprocess
import sys

D = sys.modules.get("shop_decision_tiers_handlers")
W = sys.modules["shop_work_queue_world"]


def tiers():
    """decision_tiers_handlers.py, loaded once under its shared name."""
    global D
    if D is None:
        import importlib.util
        from pathlib import Path
        spec = importlib.util.spec_from_file_location("shop_decision_tiers_handlers",
                                                      Path(__file__).with_name("decision_tiers_handlers.py"))
        D = sys.modules["shop_decision_tiers_handlers"] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(D)
    return D


def done(step):
    result = step.context["result"]
    assert result.returncode == 0, result.stderr
    return result


def frontmatter(text):
    head = text[4:].split("\n---\n", 1)[0]
    return dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)


def written(step):
    """The decision the run wrote, by the path it printed."""
    return step.repo / done(step).stdout.strip().splitlines()[-1]


def status_set(step):
    """`work sets the status of the design-decision d1 to `superseded``: its file's frontmatter says so."""
    done(step)
    name, value = step.names[0], tiers().bare(step.values[0])
    assert tiers().fields(step, name).get("status") == value, tiers().fields(step, name)


def committed(step):
    """`work commits the design-decision d1`: HEAD holds its file as it is, nothing of it left uncommitted."""
    done(step)
    rel = "spec/decisions/%s.md" % step.names[0]
    head = subprocess.run(["git", "show", "HEAD:%s" % rel], cwd=step.repo, capture_output=True, text=True)
    assert head.returncode == 0, head.stderr
    assert head.stdout == (step.repo / rel).read_text(), head.stdout
    left = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=step.repo, capture_output=True, text=True)
    assert not left.stdout.strip(), left.stdout


def wrote(step):
    """`work writes the design-decision d2`: the file it printed, accepted, is d2."""
    path = written(step)
    assert frontmatter(path.read_text()).get("status") == "accepted", path.read_text()
    step.context.setdefault("decisions", {})[step.names[0]] = path


def supersedes(step):
    """`the design-decision d2 supersedes the design-decision d1`: d2's `supersedes` names d1's id."""
    new, old = step.names
    path = step.context.get("decisions", {}).get(new) or written(step)
    listed = frontmatter(path.read_text()).get("supersedes", "").strip("[]").split(",")
    assert "design-decision/%s/%s" % (tiers().PATH, old) in [x.strip() for x in listed], path.read_text()


THENS = {"set": status_set, "commit": committed, "write": wrote, "supersede": supersedes}


@W.local("ThenDoes")
def superseding(step):
    if "superseding" not in step.context or step.term not in THENS:
        return False
    THENS[step.term](step)
