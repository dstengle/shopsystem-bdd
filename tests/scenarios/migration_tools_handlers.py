"""migration-tools' handlers in grammar 4 (b240, phase 19): the Givens hold the files of the repository `migrate`
runs in, tracked (committed before the command runs) or not (`an uncommitted change u1`, the file `u1.md`); every
`migrate ...` command of the generated feature runs the real script, and the hooks' commands run as hooks/hooks.json
has them, both from the plugin migration_old.plugin gives; the Thens (migration_tools_handlers_thens.py) read what it
printed and the files it left.

The scenario's instances are its lines' things; their example data is the given block. So a Given of an instance or
a link records nothing (a `local` of work_queue_world's table, which keeps the other worlds' Givens out of this
repository), "this repository is `v`" checks the release the given block's `.shop/plugin-version` holds, and the
Thens find the files a noun phrase names by its kind (`FILES`, `ledger`)."""
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


def _queue_world():
    """work_queue_world as the other handler modules load it (its `local` table is that copy's)."""
    import importlib.util
    if "shop_work_queue_world" not in sys.modules:
        spec = importlib.util.spec_from_file_location("shop_work_queue_world", HERE / "work_queue_world.py")
        sys.modules["shop_work_queue_world"] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules["shop_work_queue_world"]


local = _queue_world().local


def bare(word):
    return word.strip("`")


def held(step):
    return step.context.setdefault("tracked", {})


def migration(step):
    """True in a scenario of features/migration-tools.feature."""
    scenario = getattr(getattr(step.request.node, "obj", None), "__scenario__", None)
    return scenario is not None and pathlib.Path(scenario.feature.filename).name == "migration-tools.feature"


# --- Givens ---


@handler("GivenCode", "tracked file")
@handler("GivenCodeText", "tracked file")
def given_tracked(step):
    text = step.docstring if step.docstring is not None else step.quoted[0][1:-1]
    held(step)[bare(step.names[0])] = text + "\n"


def recorded(step):
    """An instance, a value or a link of the scenario's lines: the given block holds it."""
    if not migration(step):
        return False
    if step.kind == "uncommitted change":
        rel = "%s.md" % step.names[0]
        step.context.setdefault("untracked", {})[rel] = "not committed\n"
    for code in re.findall(r" violates `([vw]_\w+)`", step.text):   # the rule a term violates, which migrate names
        step.context.setdefault("violates", []).append(code)
    if step.kind == "repository":
        version = held(step).get(".shop/plugin-version", "").strip()
        assert step.values and bare(step.values[0]) == version, (step.text, version)
    return None


for _template in ("GivenK", "GivenK_A", "GivenDoes", "GivenDoesNot"):
    local(_template)(recorded)
for _kind in ("capability", "feature", "requirement", "scenario", "term", "initiative"):
    local("GivenK", _kind)(recorded)
    local("GivenK_A", _kind)(recorded)


# --- the When ---


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
        return
    args = shlex.split(bare(step.command))[1:]
    if args == ["run"]:
        args += ["--context", CONTEXT]
    run = runner(step.repo, step.request, scripts=plugin()[0] / "scripts")
    step.context["done"] = run("migrate", *args, env=dict(os.environ, **WHO))


for _command in sorted(set(re.findall(r"When .* runs (`migrate[^`]*`)", FEATURE.read_text()))):
    handler("WhenRuns", _command)(runs_migrate)


# --- what the Thens read ---


def said(step):
    done = step.context["done"]
    return done.stdout + done.stderr


def read(step, rel):
    return (step.repo / rel).read_text()


def ledger(step):
    """[(entry name, {field: value})] of the given block's decision ledger, in its order."""
    text, out = held(step).get("spec/decisions.md", ""), []
    for name, body in re.findall(r"^## decision/(\S+)\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL):
        out.append((name, dict(re.findall(r"^(\w+): (.*)$", body, re.MULTILINE))))
    return out


def decision_file(name):
    """The design-decision `migrate run` writes of the ledger entry `name` (an entry with no number is the eighth)."""
    return "spec/decisions/%s.md" % (name if re.match(r"\d", name) else "0008-" + name)


def entries(step):
    """{the scenario's ledger entry name: the given ledger's entry}: the one that supersedes first."""
    found = ledger(step)
    ordered = sorted(found, key=lambda e: "supersedes" not in e[1])
    return {"l%d" % k: name for k, (name, _) in enumerate(ordered, 1)}


def pending(step):
    """The titles of the upgrade steps after the repository's release, up to the plugin's."""
    sys.path.insert(0, str(plugin()[0] / "scripts"))
    import migrate_upgrade
    version = held(step).get(".shop/plugin-version", "0.23.1").strip()
    key = tuple(int(p) for p in version.split(".")) if re.fullmatch(r"[\d.]+", version) else (0, 23, 1)
    return [title for release, title, *_ in migrate_upgrade.STEPS
            if key < tuple(int(p) for p in release.split(".")) <= tuple(int(p) for p in plugin()[1].split("."))]
