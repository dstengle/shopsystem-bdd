"""migration-tools' Thens in grammar 4 (b240, phase 19): each a `local` of work_queue_world's table, which returns
False outside migration-tools. A noun phrase names a thing by its kind ("the work-item file w1"); the files of that
kind are read off the given block (`FILES`), and a design-decision off the ledger entry the scenario gave it
(`the ledger entry l2 has the design-decision d1`, kept under `decisions`). A `migrate run` that exits successfully
also leaves a repository in which `model check` finds no unresolved reference and no file problem."""
import json
import re
import subprocess
import sys

from scenarios import migration_tools_handlers as M
from scenarios.migration_old import CONTEXT, plugin

local = M.local
RELOCATED = {"decisions/": "spec/decisions/", "work/": ".shop/work/", "records/": ".shop/records/",
             "docs/superpowers/plans/": ".shop/records/archive/plans/",
             "docs/superpowers/specs/": ".shop/records/archive/design-notes/",
             "docs/superpowers/requests/": ".shop/records/archive/requests/",
             "adrs/": ".shop/records/decision-arguments/"}


def kind(np):
    """The kind a noun phrase names: "the work-item file w1" -> "work-item file"."""
    return re.sub(r"^(the|a|an|this) ", "", np).rsplit(" ", 1)[0] if re.search(r" [a-z]\d+$", np) else \
        re.sub(r"^(the|a|an|this) ", "", np)


def ok(step):
    assert step.context["done"].returncode == 0, M.said(step)


def decision(step, name):
    """The design-decision file of the scenario's design-decision `name`."""
    entry = step.context.setdefault("decisions", {}).get(name)
    if entry is None:    # the one the scenario gave no entry: the ledger entry that supersedes
        entry = M.entries(step)["l1"]
    return M.decision_file(entry)


def relocated(step, what):
    ok(step)
    if what == "old-layout directory":
        moved = [s for s in RELOCATED if any(rel.startswith(s) for rel in M.held(step))]
        assert moved, M.held(step)
        for source in moved:
            assert not (step.repo / source).exists() and (step.repo / RELOCATED[source]).exists(), source
        if "docs/superpowers/plans/" in moved:
            assert "about: bounded-context/%s" % CONTEXT in M.read(step, ".shop/records/archive/plans/2025-01-01-cart.md")
    else:    # a frozen request another context asked, not closed: moved byte for byte; the internal one kept
        for rel, text in M.held(step).items():
            if rel.startswith(".shop/work/requests/"):
                peer = "asker: internal" not in text
                assert (step.repo / rel).exists() != peer, rel
                if peer:
                    assert M.read(step, ".shop/requests/" + rel.rsplit("/", 1)[1]) == text


def rewritten(step, what):
    ok(step)
    if what == "plugin version file":
        assert M.read(step, ".shop/plugin-version").strip() == plugin()[1]
        old = step.context["old"]
        assert len(old.git("log", "--oneline").stdout.splitlines()) == step.context["commits"] + 1
        assert old.git("status", "--porcelain").stdout == ""
    elif what == "file":
        assert "(.shop/records/notes/one.md)" in M.read(step, "README.md")
        assert ".shop/work/i1-cart/initiative.md" in M.read(step, "README.md")
        assert "id: capability/%s/thing\n" % CONTEXT in M.read(step, "spec/capabilities/thing.md")
    elif what == "decisions index":
        text = M.read(step, "spec/decisions/index.md")
        assert ("0007-a" in text) if "spec/decisions.md" in M.held(step) else ("| tier |" in text and "0001-one.md" in text)
    elif what == "initiative log":
        assert json.loads(M.read(step, ".shop/work/i1/log.jsonl"))["work-item"] == "w1"
    elif what == "work-item file" and ".shop/work/i1/w1.md" in M.held(step):
        text = M.read(step, ".shop/work/i1/w1.md")
        assert "status: awaiting-answer" in text and "## Answers" in text, text
    elif what == "work-item file":
        assert "accepts: [cart#r1@0.29]" in M.read(step, ".shop/work/i1/w2.md")
    elif what == "capability" and "language: codified-1" in M.held(step).get("spec/capabilities/cart.md", ""):
        before = M.held(step)["spec/capabilities/cart.md"]      # 4.0.0: the marker alone, no line reworded
        assert M.read(step, "spec/capabilities/cart.md") == before.replace("codified-1", "codified-2")
    elif what == "capability":
        text = M.read(step, "spec/capabilities/cart.md")
        assert "### [g1] r1@0.29\nRestates: r1@0.29.\n" in text and "- [r1]" not in text, text
    elif what == "feature":
        text = M.read(step, "features/cart.feature")
        assert "@deprecated" not in text and text.startswith("Feature: Cart"), text
    elif what == "index file":
        before = M.held(step)["spec/index.md"]      # 3.0.0's parts of speech, then 4.0.0's marker and aspect (no line uses a CLI word)
        after = (before.replace("(kind)", "(noun)").replace("(event)", "(verb)").replace("(verb)", "(verb, action)")
                 .replace("language: codified-1\n", "language: codified-2\n"))
        assert M.read(step, "spec/index.md") == after != before
    else:
        raise AssertionError("no reading of a rewritten %s" % what)


def wrote(step, what, name):
    ok(step)
    if what == "design-decision":
        rel = decision(step, name)
        assert "id: design-decision/%s/%s\n" % (CONTEXT, re.sub(r"^\d+-", "", rel.rsplit("/", 1)[1][:-3])) in M.read(step, rel)
    else:
        rel = {"restated file": "spec/restated.json", "frozen notice": ".shop/work/FROZEN.md"}[what]
        assert (step.repo / rel).is_file(), rel


def has(step):
    one, other = kind(step.subject), kind(step.nps[0])
    if one == "ledger entry":
        step.context.setdefault("decisions", {})[step.names[1]] = M.entries(step)[step.names[0]]
    elif other == "content":
        return
    else:
        rel = {"decisions index": "spec/decisions/index.md", "plugin version file": ".shop/plugin-version",
               "index file": "spec/index.md"}[other]
        assert (step.repo / rel).is_file(), rel


@local("ThenDoes")
def then_does(step):
    if not M.migration(step):
        return False
    what = kind(step.nps[0]) if step.nps else None
    if step.term == "relocate":
        relocated(step, what)
    elif step.term == "rewrite":
        rewritten(step, what)
    elif step.term == "write":
        wrote(step, what, step.names[0])
    elif step.term == "has":
        has(step)
    elif step.term == "remove":
        ok(step)
        assert not (step.repo / "spec/decisions.md").exists()
    elif step.term == "rename":
        ok(step)
        if what == "work-item file":
            assert not (step.repo / ".shop/work/i1/size-check.md").exists()
            text = M.read(step, ".shop/work/i1/w1.md")
            assert "id: work-item/%s/w1\n" % CONTEXT in text and "\n# size-check\n" in text, text
        else:
            assert (step.repo / ".shop/work/i1/runs/w1/1-research/notes.md").is_file()
    elif step.term == "supersede":
        text = M.read(step, decision(step, step.names[0]))
        target = re.sub(r"^\d+-", "", decision(step, step.names[1]).rsplit("/", 1)[1][:-3])
        assert re.search(r"^supersedes: design-decision/%s/%s$" % (re.escape(CONTEXT), target), text, re.MULTILINE), text
    elif step.term == "holds":     # the qualifier, in the design-decision's `by`, its supersedes the id alone
        text = M.read(step, decision(step, step.names[0]))
        assert "(in part)" not in re.search(r"^supersedes:.*$", text, re.MULTILINE).group(0), text
        assert re.search(r'^by: "?bob; supersedes .*\(in part\)', text, re.MULTILINE), text
    elif step.term == "give" and what == "ledger number":
        ok(step)
        assert (step.repo / "spec/decisions/0008-b.md").is_file()
    elif step.term == "give":
        ok(step)
        assert "- [r5] **When** b" in M.read(step, "spec/capabilities/thing.md")
    elif step.term in ("refuse", "name"):
        refused(step, what)
    else:
        return False
    return None


def refused(step, what):
    assert step.context["done"].returncode != 0, M.said(step)
    if what == "uncommitted change":
        assert "u1.md" in M.said(step), M.said(step)
    elif what == "tracked file":
        assert "decisions/0007-a.md" in M.said(step), M.said(step)
    elif what == "content":
        assert "banana" in M.said(step), M.said(step)


@local("ThenK_A", "design-decision")
def decision_is(step):
    if not M.migration(step):
        return False
    assert "status: %s\n" % M.bare(step.values[0]) in M.read(step, decision(step, step.names[0]))
    return None


def printed(step, np):
    """The words `migrate` prints for the thing a noun phrase names."""
    what = kind(np)
    if np.startswith("`"):
        return [M.bare(np)]
    return {"release of this repository": [M.held(step).get(".shop/plugin-version", "").strip()],
            "upgrade step": M.pending(step), "restated file": ["spec/restated.json"],
            "capability": ["spec/capabilities/cart.md"], "initiative": ["i1"], "frozen request": ["q1"],
            "term": ["v_t11"], "content": ["banana"]}[what]


@local("ThenPrints")
def prints(step):
    if not M.migration(step):
        return False
    for np in step.nps:
        for word in printed(step, np):
            assert word in M.said(step), (np, word, M.said(step))
    return None


@local("ThenPrintsNot")
def prints_not(step):
    """`migrate` prints no upgrade step (no step's title, nor `migrate upgrade`) and no initiative."""
    if not M.migration(step):
        return False
    out = step.context["done"].stdout
    for np in step.nps:
        words = ["migrate upgrade"] + M.pending(step) if "upgrade step" in np else ["i1"]
        assert not any(w in out for w in words), (np, out)
    return None


@local("ThenDoesNot")
def changes_nothing(step):
    if not M.migration(step) or step.term != "change":
        return False
    old = step.context["old"]
    assert old.git("status", "--porcelain").stdout == "", old.git("status", "--porcelain").stdout
    assert len(old.git("log", "--oneline").stdout.splitlines()) == step.context["commits"]
    return None


@local("ThenExitsOk")
def exits_ok(step):
    if not M.migration(step):
        return False
    ok(step)
    done = step.context["done"]
    if isinstance(done.args, list) and done.args[2:3] == ["run"]:
        checked = subprocess.run([sys.executable, str(M.PLUGIN / "scripts" / "model"), "--root", str(step.repo),
                                  "check", "--json"], capture_output=True, text=True)
        report = json.loads(checked.stdout)
        assert (report["unresolved"], report["problems"]) == ([], []), checked.stdout
    return None
