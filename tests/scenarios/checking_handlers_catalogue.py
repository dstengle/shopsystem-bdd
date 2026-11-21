"""Handlers of checking's `spec catalogue entry` scenarios (r59-r62, b462), each a `work_queue_world.local` that takes
only a step of a scenario of one of its groups (`mine`). The Givens keep what they say (`world`): the catalogue
entry c1 is `rules#v_c2`, an entry of a rule, unless a Given says no rule (or no construct) has it, then an entry
`v_zz` (or `zz-none`) the copied catalogue is given a heading of; the purpose p1 and the item i1 are `PURPOSE` and
`ITEM`. At the When the repository is given the plugin's `grammar/catalogue-entries.toml`, `rules.md` and
`constructs.md` and `spec catalogue entry` is run with the options the step names. The Thens read the entry's table
and its catalogue's lines back."""
import re
import shutil
import sys
import tomllib
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
GROUPS = {"g59", "g60", "g61", "g62"}
FILES = ("catalogue-entries.toml", "rules.md", "constructs.md")
PURPOSE, ITEM = "Says what the scenario's purpose is.", "b7"
UNHAD = {"rule": ("rules", "v_zz", "rules.md"), "construct": ("constructs", "zz-none", "constructs.md")}


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def world(step):
    return step.context.setdefault("catalogue", {"catalogue": "rules", "unhad": None, "kinds": {}})


def given_instance(step):
    if not mine(step) or step.kind not in ("catalogue entry", "purpose", "item"):
        return False
    world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """`this rule catalogue holds the catalogue entry c1`, `no construct has the catalogue entry c1`."""
    if not mine(step) or step.term not in ("holds", "has"):
        return False
    w = world(step)
    if step.term == "holds":
        w["catalogue"] = "constructs" if "construct catalogue" in step.text else "rules"
    else:
        w["unhad"] = "construct" if step.text.startswith("no construct") else "rule"


def entry(w):
    return "%s#%s" % UNHAD[w["unhad"]][:2] if w["unhad"] else "rules#v_c2"


def runs(step):
    if not mine(step) or step.term != "`spec catalogue entry`":
        return False
    w, repo = world(step), step.repo
    (repo / "grammar").mkdir(exist_ok=True)
    for name in FILES:
        shutil.copy(ROOT / "grammar" / name, repo / "grammar" / name)
    if w["unhad"]:
        _, code, name = UNHAD[w["unhad"]]
        path = repo / "grammar" / name
        path.write_text(path.read_text() + "\n## %s\n\nan entry of nothing\n\n- Purpose: None.\n" % code)
    w["before"] = (repo / "grammar" / FILES[0]).read_text()
    for name, kind in w["kinds"].items():       # what the output names each instance by
        step.context.setdefault("says", {})[name] = {"catalogue entry": entry(w), "purpose": PURPOSE,
                                                     "item": ITEM}[kind]
    words = ["catalogue", "entry", entry(w)]
    for option, _ in getattr(step, "options", None) or ():
        words += {"`--purpose`": ["--purpose", PURPOSE], "`--item`": ["--item", ITEM]}[option]
    step.context["result"] = step.run("spec", *words)


def table(step):
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr
    catalogue, _, code = entry(world(step)).partition("#")
    data = tomllib.loads((step.repo / "grammar" / FILES[0]).read_text())
    md = (step.repo / "grammar" / ("%s.md" % catalogue)).read_text()
    body = re.search(r"^## %s\n(.*?)(?=^## |\Z)" % re.escape(code), md, re.DOTALL | re.MULTILINE).group(1)
    return data[catalogue][code], body


def then(step):
    if not mine(step) or "catalogue" not in step.context or step.term not in ("keep", "write", "has", "mention"):
        return False
    found, body = table(step)
    if step.term in ("keep", "write"):          # the entry's table written
        assert (step.repo / "grammar" / FILES[0]).read_text() != world(step)["before"]
        return None
    if step.term == "has" and "purpose" in step.text:
        assert found["purpose"] == PURPOSE, found
        assert "- Purpose: %s\n" % PURPOSE in body, body
        return None
    if step.term == "mention" and "item" in step.text:
        assert ITEM == found.get("since") or ITEM in found.get("changed", []), found
        assert re.search(r"^- (Since|Changed): .*\b%s\b" % ITEM, body, re.MULTILINE), body
        return None
    return False


W.local("GivenK")(given_instance)
W.local("GivenDoes")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then)
