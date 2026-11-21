"""Handlers of batches' `work settings set` scenarios (r84-r86, b462), each a `work_queue_world.local` that takes only
a step of a scenario of one of its groups (`mine`). The setting s1 is `review.size` and the setting value s2 `500`,
unless a Given says one does not conform to the delivery settings form: then `review.batch_size` (a key the plugin
reads only at the top level) or `many`. At the When the repository is given a settings file (`BEFORE`: `batch_size`
at the top level and a `[batch]` table, no `[review]`) committed, and `work settings set` run on it. The Thens read
the settings file back: kept in one commit, the setting in its own table, conforming to the form (delivery_settings'
`problems`)."""
import subprocess
import sys
import tomllib
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
GROUPS = {"g84", "g85", "g86"}
REL = ".shop/delivery.toml"
BEFORE = "# How this repository's batches are delivered.\nbatch_size = 4\n\n[batch]\npush = \"\"\n"
GOOD = {"setting": "review.size", "setting value": "500"}
BAD = {"setting": "review.batch_size", "setting value": "many"}


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "batches" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("settings", {"kinds": {}, "bad": set()})


def given_instance(step):
    if not mine(step) or step.kind not in GOOD:
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_unconforming(step):
    """`the setting s1 does not conform to the delivery settings form`."""
    if not mine(step) or step.term != "conform":
        return False
    world(step)["bad"].add(step.names[0])


def said(w, name):
    kind = w["kinds"][name]
    return (BAD if name in w["bad"] else GOOD)[kind]


def runs(step):
    if not mine(step) or step.term != "`work settings set`":
        return False
    w, repo = world(step), step.repo
    path = repo / REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(BEFORE)
    for name in w["kinds"]:
        step.context.setdefault("says", {})[name] = said(w, name)
    step.context["head"] = W.init(repo)
    words = [said(w, n) for n in step.names if n in w["kinds"]]
    step.context["result"] = step.run("work", "settings", "set", *words)


def scripts(name):
    import importlib
    if str(ROOT / "scripts") not in sys.path:
        sys.path.insert(0, str(ROOT / "scripts"))
    return importlib.import_module(name)


def kept(step):
    """The settings file changed and committed alone by HEAD, as it now is."""
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr
    git = lambda *a: subprocess.run(["git", *a], cwd=step.repo, capture_output=True, text=True).stdout  # noqa: E731
    assert git("show", "HEAD:%s" % REL) == (step.repo / REL).read_text() != BEFORE
    assert git("show", "--name-only", "--format=", "HEAD").split() == [REL]


def then(step):
    if not mine(step) or "settings" not in step.context or step.term not in ("keep", "write", "holds", "conform"):
        return False
    text = (step.repo / REL).read_text()
    if step.term in ("keep", "write"):
        return kept(step)
    if step.term == "holds":           # the setting in its own table, the top level's key still the top level's
        table, _, key = said(world(step), step.names[1]).partition(".")
        data = tomllib.loads(text)
        assert data[table][key] == 500 and data["batch_size"] == 4, text
        return None
    assert scripts("delivery_settings").problems(text) == [], text
    return None


W.local("GivenK")(given_instance)
W.local("GivenDoesNot")(given_unconforming)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then)
