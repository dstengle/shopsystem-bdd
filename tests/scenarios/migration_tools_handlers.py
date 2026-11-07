"""migration-tools' handlers (design §14.3): the Givens hold the files of the repository `migrate` runs in, tracked
(committed before the command runs) or not; every `migrate ...` command of the generated feature runs the real
script, and the hooks' commands run as hooks/hooks.json has them, both from the plugin migration_old.plugin gives (a
copy at its TARGET while this one is below it); the Thens read what it printed and the files it left.

What a `relocate`, `rewrite` or `rename` Then looks for in a file is in this module (EXPECTED and the checks under
it), from the files the scenario's given block holds. A `migrate run` that exits successfully also leaves a
repository in which `model check` finds no unresolved reference and no file problem (r19)."""
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from vocab import handler, runner

from scenarios.migration_old import CONTEXT, Old, plugin

PLUGIN = HERE.parents[1]
FEATURE = PLUGIN / "features" / "migration-tools.feature"
WHO = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
HOOKS = {"`migrate status --hook`": "SessionStart"}
RELOCATED = {"decisions/": "spec/decisions/", "work/": ".shop/work/", "records/": ".shop/records/",
             "docs/superpowers/plans/": ".shop/records/archive/plans/",
             "docs/superpowers/specs/": ".shop/records/archive/design-notes/",
             "docs/superpowers/requests/": ".shop/records/archive/requests/",
             "adrs/": ".shop/records/decision-arguments/", "spec/decisions.md": "spec/decisions/0007-a.md"}


def bare(word):
    return word.strip("`")


def held(step):
    return step.context.setdefault("tracked", {})


@handler("GivenCode", "tracked file")
@handler("GivenCodeText", "tracked file")
def given_tracked(step):
    text = step.docstring if step.docstring is not None else step.quoted[0][1:-1]
    held(step)[bare(step.names[0])] = text + "\n"


def hook(step, name):
    root = plugin()[0]
    command = json.loads((root / "hooks/hooks.json").read_text())["hooks"][name][0]["hooks"][0]["command"]
    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(root), PYTHON=sys.executable, **WHO)
    return subprocess.run(command, shell=True, cwd=step.repo, env=env, capture_output=True, text=True)


def runs_migrate(step):
    old = step.context["old"] = Old(step.repo)
    for rel, text in held(step).items():
        old.write(rel, text)
    old.git("add", "-A")
    old.git("commit", "-q", "--allow-empty", "-m", "the repository")
    for rel, text in step.context.get("untracked", {}).items():
        old.write(rel, text)
    old.keep()
    step.context["commits"] = len(old.git("log", "--oneline").stdout.splitlines())
    if step.command in HOOKS:
        step.context["done"] = hook(step, HOOKS[step.command])
    else:
        run = runner(step.repo, step.request, scripts=plugin()[0] / "scripts")
        step.context["done"] = run("migrate", *shlex.split(bare(step.command))[1:], env=dict(os.environ, **WHO))


for _command in sorted(set(re.findall(r"When .* runs (`migrate[^`]*`)", FEATURE.read_text()))):
    handler("WhenRuns", _command)(runs_migrate)


def said(step):
    done = step.context["done"]
    return done.stdout + done.stderr


def read(step, rel):
    return (step.repo / rel).read_text()


@handler("ThenExitsOk", "`migrate`")
def exits_ok(step):
    done = step.context["done"]
    assert done.returncode == 0, said(step)
    if isinstance(done.args, list) and done.args[2:3] == ["run"]:
        checked = subprocess.run([sys.executable, str(PLUGIN / "scripts" / "model"), "--root", str(step.repo),
                                  "check", "--json"], capture_output=True, text=True)
        report = json.loads(checked.stdout)
        assert (report["unresolved"], report["problems"]) == ([], []), checked.stdout


@handler("ThenExitsErr", "`migrate`")
def exits_err(step):
    assert step.context["done"].returncode != 0, said(step)
    for np in step.nps:
        want = np.strip('"') if np.startswith('"') else bare(np.split()[-1])
        want = step.context.get("says", {}).get(want, want)
        assert want in said(step), (want, said(step))


@handler("ThenPrints", "`migrate`")
def prints(step):
    for np in step.nps:
        assert np.strip('"') in said(step), (np, said(step))


@handler("ThenPrintsNot", "`migrate`")
def prints_not(step):
    for np in step.nps:
        assert np.strip('"') not in step.context["done"].stdout, (np, step.context["done"].stdout)


@handler("ThenDoes", "relocate")
def relocates(step):
    source = bare(step.nps[0])
    target = RELOCATED[source]
    assert not (step.repo / source).exists() and (step.repo / target).exists(), said(step)
    tracked = step.context["old"].git("ls-files", "--", target).stdout
    added = step.context["old"].git("diff", "--cached", "--name-only", "--", target).stdout
    assert tracked or added, (target, step.context["old"].git("status", "--porcelain").stdout)
    if source == "docs/superpowers/plans/":
        assert "about: bounded-context/%s" % CONTEXT in read(step, ".shop/records/archive/plans/2025-01-01-cart.md")


def decision(step, rel):
    text, ledger = read(step, rel), held(step).get("spec/decisions.md", "")
    name = re.sub(r"^\d+-", "", pathlib.PurePosixPath(rel).stem)
    assert "id: design-decision/%s/%s\n" % (CONTEXT, name) in text, text
    if rel.endswith("0007-a.md") and "supersedes" in ledger:
        assert "status: superseded" in text, text
    if rel.endswith("0008-b.md") and "(in part)" in ledger:
        assert "(in part)" not in re.search(r"^supersedes:.*$", text, re.MULTILINE).group(0), text
        assert re.search(r'^by: "?bob; supersedes .*\(in part\)', text, re.MULTILINE), text
    if rel.endswith("0008-b.md") and "revisit_when" in ledger:
        assert re.search(r'^revisit_when: "?the cart grows', text, re.MULTILINE) and "design-decision/%s/a" % CONTEXT in text, text


def upgraded(step, rel):
    old = step.context["old"]
    assert read(step, rel).strip() == plugin()[1]
    assert len(old.git("log", "--oneline").stdout.splitlines()) == step.context["commits"] + 1
    assert old.git("status", "--porcelain").stdout == ""


def relabelled(step, rel):
    """`spec/index.md` as `migrate run` writes it, or, when the scenario upgrades a repository (it holds a plugin
    version) whose glossary is in plugin 2.x's categories, as "verb frames" rewrites it: each category its part of
    speech, nothing else changed."""
    text = read(step, rel)
    if rel not in held(step) or ".shop/plugin-version" not in held(step):
        return "id: bounded-context/%s\n" % CONTEXT in text
    return text == held(step)[rel].replace("(kind)", "(noun)").replace("(event)", "(verb)") != held(step)[rel]


EXPECTED = {
    "spec/decisions/index.md": lambda step, rel: ("0007-a" in read(step, rel) if "spec/decisions.md" in held(step)
                                                  else "| tier |" in read(step, rel) and "0001-one.md" in read(step, rel)),
    "spec/index.md": relabelled,
    "README.md": lambda step, rel: ("(.shop/records/notes/one.md)" in read(step, rel)
                                    and ".shop/work/i1-cart/initiative.md" in read(step, rel)),
    "spec/capabilities/thing.md": lambda step, rel: (
        "id: capability/%s/thing\n" % CONTEXT in read(step, rel)
        and ("[r4]" not in held(step)[rel] or "- [r5] **When** b" in read(step, rel))),
    ".shop/work/i1/log.jsonl": lambda step, rel: json.loads(read(step, rel))["work-item"] == "w1",
    ".shop/work/i1/w1.md": lambda step, rel: ("status: awaiting-answer" in read(step, rel)
                                              and "## Answers" in read(step, rel)),
    "spec/capabilities/cart.md": lambda step, rel: ("### [g1] r1@0.29\nRestates: r1@0.29.\n" in read(step, rel)
                                                    and "- [r1]" not in read(step, rel)
                                                    and json.loads(read(step, "spec/restated.json"))["cart#r1"]),
    "features/cart.feature": lambda step, rel: ("@deprecated" not in read(step, rel)
                                                and read(step, rel).startswith("Feature: Cart")),
    ".shop/work/i1/w2.md": lambda step, rel: "accepts: [cart#r1@0.29]" in read(step, rel),
}


@handler("ThenDoes", "rewrite")
def rewrites(step):
    rel = bare(step.nps[0])
    assert step.context["done"].returncode == 0, said(step)
    if rel.startswith("spec/decisions/") and rel != "spec/decisions/index.md":
        decision(step, rel)
    elif rel == ".shop/plugin-version":
        upgraded(step, rel)
    else:
        assert EXPECTED[rel](step, rel), read(step, rel)


@handler("ThenDoes", "rename")
def renames(step):
    rel = bare(step.nps[0]).rstrip("/")
    assert step.context["done"].returncode == 0, said(step)
    assert not (step.repo / rel).exists()
    if rel.startswith(".shop/work/requests/"):      # moved, byte for byte, to the live requests
        assert read(step, ".shop/requests/" + rel.rsplit("/", 1)[1]) == held(step)[rel]
    elif rel.endswith(".md"):
        text = read(step, ".shop/work/i1/w1.md")
        assert "id: work-item/%s/w1\n" % CONTEXT in text and "\n# size-check\n" in text, text
    else:
        assert (step.repo / ".shop/work/i1/runs/w1/1-research/notes.md").is_file()
