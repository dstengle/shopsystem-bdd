"""`migrate init --id <bounded context id>` (b318): a new bounded context founded in the repository it is run in, its
context scaffold written and committed in one commit: `spec/index.md` (the id, its last part the title,
`language: codified-2`, `imports: [request]`), `spec/universal.md` (no condition), `spec/model/`, `spec/vocabulary/`,
`spec/capabilities/`, `.shop/backlog/`, `.shop/records/README.md` (an empty records index), `.shop/plugin-version`
(the plugin's release), `.shop/delivery.toml` (every key commented out at its default), `features/` and
`tests/scenarios/conftest.py`, each empty directory with a `.gitkeep`, and the ignore file `.gitignore` naming the
interpreter and the caches (b454; an existing one given the names it lacks, a name matched as git matches a line, its
leading or trailing slash no other entry, and left out of the commit when it lacks none, b470). A repository with an index file or a shop
directory is refused, never merged into; an existing `features/` or conftest is left as it is."""
import re
from pathlib import Path

import shop_files
from migrate_upgrade import identity, plugin_version
from migrate_write import top_level
from record_write import README_HEAD
from shop_refused import Refused

FORM = re.compile(r"bounded-context/[a-z0-9-]+(\.[a-z0-9-]+)+(/[A-Za-z0-9][A-Za-z0-9._-]*)+")
KEEP = ("spec/model/.gitkeep", "spec/vocabulary/.gitkeep", "spec/capabilities/.gitkeep", ".shop/backlog/.gitkeep")
CONFTEST = "tests/scenarios/conftest.py"
IGNORE = ".gitignore"
IGNORED = (".venv/", "__pycache__/", ".pytest_cache/", ".ruff_cache/")

INDEX = """---
id: {id}
title: {title}
language: codified-2
imports: [request]
---

# {title}

## Purpose

## Composition
"""

UNIVERSAL = """---
id: capability/{path}/universal
title: Universal conditions
narrator: every trace of every delivery and every tool
group: guarantees
language: codified-2
retired: []
---

# Universal conditions

## Purpose

The statements that are true in every state of every trace, each written once here and never restated in a
requirement.

## Behaviour
"""

DELIVERY = """# How this repository's batches are delivered (`work batch`), every key at its default: uncomment one to change it.

# The base branch `tools check` with no paths checks the branch's change against.
# base = "main"

# How many ready items a batch picks.
# batch_size = 4

# [batch]
# The prefix every push and gh call takes, such as a command that gives them credentials.
# push = ""
# The command a task's tests run with.
# tests = "python3 -m pytest -q -p work_items"
# Where a batch's worktrees go.
# worktrees = ".shop/worktrees"

# [review]
# The changed lines a pull request review reads before it says the batch is too big.
# size = 1000
# The checks a pull request review runs.
# checks = [
#   "python3 {scripts}/tools size --limit 300",
#   "python3 {scripts}/tools check --base {forked_from}",
#   "python3 {scripts}/features generate --check",
#   "python3 {scripts}/features bindings --unbound",
#   "python3 {scripts}/spec decisions --check",
# ]

# [prices]
# A model's price per million tokens, over the plugin's dated table: "<model>" = { input = 0.0, output = 0.0 }
"""

CONFTEST_TEXT = '''"""The generated features' scenarios: one `test_<capability>.py` a capability binds its feature's steps.

The plugin's pytest plugin `work_items` is loaded here, so that a plain `python -m pytest` registers each @g<n> and
@r<n> tag as a mark and runs a scenario of an `unbuilt:` requirement as a strict expected failure. Its scripts are
found on the path (PYTHONPATH), else in `$CLAUDE_PLUGIN_ROOT`, else in the plugin cache's folder of the release
`.shop/plugin-version` names."""
import importlib.util
import os
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _scripts():
    """The plugin's scripts directory, or None when `work_items` is importable already."""
    if importlib.util.find_spec("work_items") is not None:
        return None
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    places = [pathlib.Path(root) / "scripts"] if root else []
    release = ROOT / ".shop" / "plugin-version"
    if release.is_file():
        home = pathlib.Path(os.environ.get("CLAUDE_CONFIG_DIR") or pathlib.Path.home() / ".claude")
        version = release.read_text().strip()
        places += sorted((home / "plugins" / "cache").glob("*/shopsystem-bdd/%s/scripts" % version))
    for place in places:
        if (place / "work_items.py").is_file():
            return place
    raise pytest.UsageError("the plugin's pytest plugin work_items is not found: put the plugin's scripts on "
                            "PYTHONPATH or name the plugin in $CLAUDE_PLUGIN_ROOT")


def pytest_configure(config):
    if config.pluginmanager.has_plugin("work_items"):     # loaded already, as by -p work_items
        return
    scripts = _scripts()
    if scripts is not None:
        sys.path.append(str(scripts))
    config.pluginmanager.import_plugin("work_items")
'''


def scaffold(ident):
    """{path: text} of the context scaffold of the bounded context `ident`."""
    path = ident.split("/", 1)[1]
    return {"spec/index.md": INDEX.format(id=ident, title=ident.rsplit("/", 1)[1]),
            "spec/universal.md": UNIVERSAL.format(path=path),
            **{rel: "" for rel in KEEP},
            ".shop/records/README.md": README_HEAD,
            ".shop/plugin-version": plugin_version() + "\n",
            ".shop/delivery.toml": DELIVERY}


def ignore_text(root):
    """The ignore file's text: the repository's own, if any, with each name of IGNORED it lacks added at its end; a
    name it holds with or without a leading or a trailing slash is not lacked (b470)."""
    path = root / IGNORE
    text = path.read_text() if path.is_file() else ""
    held = {line.strip().strip("/") for line in text.splitlines()}
    missing = [name for name in IGNORED if name.strip("/") not in held]
    if text and not text.endswith("\n"):
        text += "\n"
    return text + "".join(name + "\n" for name in missing)


def check(root, ident):
    """Refused unless `ident` is a bounded context id and the repository at `root` holds no context yet."""
    if ident is None:
        raise Refused("the bounded context at %s is founded with no context id: give {names} "
                      "bounded-context/<domain>/<path>" % root, reason="bounded context with no context id",
                      names=["parameter:context id"])
    if not FORM.fullmatch(ident):
        raise Refused("the context id %s is not a bounded context id: bounded-context/<domain>/<path>, "
                      "its <domain> a domain name with a dot (example.org)" % ident,
                      reason="context id not a bounded context id", names=["parameter:context id"])
    if (root / "spec/index.md").exists():
        raise Refused("this bounded context has an index file already: spec/index.md; nothing written",
                      reason="index file present", names=["file:spec/index.md"])
    if (root / ".shop").exists():
        raise Refused("this repository has a shop directory already: .shop; nothing written",
                      reason="shop directory present", names=["file:.shop"])


def run(args):
    root = top_level(Path.cwd())
    if root is None:
        raise Refused("could not find a git repository at %s" % Path.cwd())
    check(root, args.id)
    if not identity(root):      # the person's name and email, asked for, never made up (b415)
        raise Refused('git has no identity to commit the context with: ask the person for theirs and set it with git '
                      'config user.name "…" and git config user.email "…"; nothing written')
    files = scaffold(args.id)
    if not (root / "features").exists():
        files["features/.gitkeep"] = ""
    if not (root / CONFTEST).exists():
        files[CONFTEST] = CONFTEST_TEXT
    ignore = ignore_text(root)
    if not (root / IGNORE).is_file() or (root / IGNORE).read_text() != ignore:     # one that lacks nothing left alone
        files[IGNORE] = ignore

    made = sorted({p for rel in files for p in (root / rel).parents if root in p.parents and not p.exists()},
                  key=lambda p: -len(p.parts))

    def write():
        for rel, text in files.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text)
    try:
        shop_files.committed(root, sorted(files), "migrate init: %s" % args.id, write)
    except Refused:
        for folder in made:      # the files are put back by `committed`; the folders it made go too
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()
        raise
    for rel in sorted(files):
        print("wrote %s" % rel)
    return 0
