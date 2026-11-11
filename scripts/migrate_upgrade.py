"""`migrate status` and `migrate upgrade` (migration-tools g14-g29): the repository's plugin version, the plugin's,
the upgrade steps between them, what a session is told at its start, and the upgrade, all of it in one commit or none
of it, with what a step leaves for a session to write printed and in the commit message."""
import json
import re
import subprocess
import sys
import types
from pathlib import Path

import migrate_upgrade_answers
import migrate_upgrade_cnl4
import migrate_upgrade_codified
import migrate_upgrade_frames
import migrate_upgrade_ids
import migrate_upgrade_simplified
import migrate_upgrade_values
import shop_files
from migrate_write import check_moves, git, top_level, uncommitted

SCRIPTS = Path(__file__).resolve().parent
VERSION_FILE = ".shop/plugin-version"
UNRECORDED = "0.23.1"
BATCH = 500  # paths a `git add` stages at once: one process per batch, not one per file
STEPS = [("0.24.0", "work-items named by ids", "give every work-item the id w<n>", migrate_upgrade_ids),
         ("0.25.0", "answers, not rulings",
          "rename awaiting-ruling to awaiting-answer and `## Rulings` to `## Answers`", migrate_upgrade_answers),
         ("0.30.0", "codified requirements",
          ("write spec/restated.json, scaffold each uncodified capability's Behaviour as groups, delete @deprecated "
          "scenarios and write old references <cap>#r<n>@0.29"), migrate_upgrade_codified),
         ("0.31.0", "the workflow simplified",
          "freeze .shop/work/, move the live requests to .shop/requests/ and write the decisions index",
          migrate_upgrade_simplified),
         ("0.32.0", "verb frames",
          ("write each glossary entry's category as its part of speech and name each verb with no Frame:, each "
           "relational condition and each requirement that no longer parses"), migrate_upgrade_frames),
         ("0.33.0", "the controlled language 4",
          ("write each file's marker codified-2, import the CLI pack and give each verb its aspect where its lines "
           "decide it, and name by file and id each line that no longer parses and what else a session rewords"),
          migrate_upgrade_cnl4),
         ("0.34.0", "value kinds",
          ("name each attribute whose values are declared neither adjectives nor nouns and each line that says one of "
           "its values in the short form, by file and id"), migrate_upgrade_values)]


def number(version):
    return tuple(int(part) for part in version.split("."))


def plugin_version():
    return json.loads((SCRIPTS.parent / ".claude-plugin/plugin.json").read_text())["version"]


def repository_version(root):
    path = root / VERSION_FILE
    return path.read_text().strip() if path.is_file() else UNRECORDED


def no_version(root):
    """What `.shop/plugin-version` holds when that is no version (dotted numbers), else None."""
    path = root / VERSION_FILE
    if not path.is_file():
        return None
    held = path.read_text().strip()
    return None if re.fullmatch(r"\d+(\.\d+)*", held) else ('it holds "%s"' % held if held else "it is empty")


def refusal(held):
    return "%s holds no version, and that %s" % (VERSION_FILE, held)


def pending(root):
    """The steps above the repository's version and not above the plugin's, oldest first (r20)."""
    here, there = number(repository_version(root)), number(plugin_version())
    return [step for step in sorted(STEPS, key=lambda s: number(s[0])) if here < number(step[0]) <= there]


def step_line(step):
    return '%s "%s": %s' % (step[0], step[1], step[2])


def status(root):
    held = no_version(root)
    if held:
        print(refusal(held), file=sys.stderr)
        return 1
    print("the repository's plugin version: %s" % repository_version(root))
    print("the plugin's version: %s" % plugin_version())
    for step in pending(root):
        print("pending upgrade step " + step_line(step))
    return 0


def session_text(root):
    """What a session is told at its start (r22-r24, r28): nothing unless the repository has .shop/ and is behind or ahead."""
    if not (root / ".shop").is_dir():
        return ""
    held = no_version(root)
    if held:
        return "Tell the person that %s.\n" % refusal(held)
    here, there = repository_version(root), plugin_version()
    if number(here) > number(there):
        return ("This repository is on plugin version %s, above the plugin's %s: tell the person to update the plugin.\n"
                % (here, there))
    steps = pending(root)
    if not steps:
        return ""
    return ("This repository is on plugin version %s and the plugin is on %s. Offer the person the upgrade from %s to %s, "
            "which applies:\n%s\nRun `migrate upgrade` (python3 %s upgrade) only on the person's yes.\n"
            % (here, there, here, there, "\n".join("  " + step_line(s) for s in steps), SCRIPTS / "migrate"))


def apply(root, changes):
    """Make a step's changes: renames through a temporary name, so that a name another rename frees is no collision."""
    held = []
    for index, (old, new) in enumerate(changes.moves):
        temporary = "%s.upgrading-%d" % (old, index)
        git(root, "mv", old, temporary)
        held.append((temporary, new))
    for temporary, new in held:
        (root / new).parent.mkdir(parents=True, exist_ok=True)     # a request moved to .shop/requests/ (0.31.0)
        git(root, "mv", temporary, new)
    for rel, text in changes.texts.items():
        with open(root / rel, "w", newline="") as handle:
            handle.write(text)
    paths = list(changes.texts)
    for start in range(0, len(paths), BATCH):
        git(root, "add", "-f", "--", *paths[start:start + BATCH])


def move_failures(root, changes):
    """What migrate run's check of moves names for a step's changes: a rename onto a file, two onto one."""
    checked = types.SimpleNamespace(root=root, moves=dict(changes.moves), texts=changes.texts, created={}, failures=[])
    # two sources to one destination cannot sit in a dict: count them first
    seen = {}
    for old, new in changes.moves:
        seen.setdefault(new, []).append(old)
    checked.failures += ["could not move both %s to %s" % (" and ".join(s), n) for n, s in seen.items() if len(s) > 1]
    check_moves(checked)
    return list(dict.fromkeys(checked.failures))


def identity(root):
    """Whether git has an author and a committer to commit the upgrade with (plan-9 review M1)."""
    return all(subprocess.run(["git", "var", var], cwd=root, capture_output=True).returncode == 0
               for var in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT"))


def upgrade(root):
    held = no_version(root)
    if held:
        print("migrate changed nothing; " + refusal(held), file=sys.stderr)
        return 1
    changed = uncommitted(root)
    if changed:
        print("migrate changed nothing; it could not start from a tree with an uncommitted change: " + ", ".join(changed),
              file=sys.stderr)
        return 1
    steps = pending(root)
    if not steps:
        print("no upgrade step is pending")
        return 0
    if not identity(root):
        print('migrate changed nothing; git has no identity to commit with: set one with git config user.name "…" '
              'and git config user.email "…"', file=sys.stderr)
        return 1
    before = repository_version(root)
    refused, notes = [], []
    try:
        for step in steps:  # oldest first, each planned from the tree the steps before it left (r20)
            changes = step[3].plan(root)
            refused = list(dict.fromkeys(changes.failures + move_failures(root, changes)))
            if refused:
                break
            apply(root, changes)
            notes += getattr(changes, "notes", [])
        if refused:
            subprocess.run(["git", "reset", "-q", "--hard", "HEAD"], cwd=root, capture_output=True)
            subprocess.run(["git", "clean", "-fdq"], cwd=root, capture_output=True)
            print("migrate changed nothing; it could not make every change:\n" + "\n".join(refused), file=sys.stderr)
            return 1
        if any(step[3] is migrate_upgrade_simplified for step in steps):
            notes = [note for note in notes if not migrate_upgrade_simplified.superseded(note)]
        (root / VERSION_FILE).write_text(plugin_version() + "\n")
        git(root, "add", "-f", "--", VERSION_FILE)
        message = "migrate upgrade: %s to %s\n\n%s" % (
            before, plugin_version(), "\n".join(["upgrade step " + step_line(s) for s in steps] + notes))
        # on stdin: the notes of a large spec are over Linux's 128 KB limit for one argument
        subprocess.run(["git", "commit", "-q", "-F", "-"], cwd=root, input=message, capture_output=True, text=True,
                       check=True)
    except Exception as error:  # noqa: BLE001 -- any failure of a step puts every change back (r15, r20)
        subprocess.run(["git", "reset", "-q", "--hard", "HEAD"], cwd=root, capture_output=True)
        subprocess.run(["git", "clean", "-fdq"], cwd=root, capture_output=True)
        print("migrate put the repository back as it was; it could not make every change: %s"
              % (getattr(error, "stderr", None) or error), file=sys.stderr)
        return 1
    shop_files.pushed(root)   # U4: after the try, so a push git refuses keeps the upgrade's commit
    print("upgraded to %s: %s" % (plugin_version(), ", ".join(s[1] for s in steps)))
    for note in notes:
        print(note)
    return 0


def run(command, hook=False):
    """`migrate status` (with `hook`, the session's text, always exit 0) or `migrate upgrade`."""
    root = top_level(Path.cwd())
    if root is None:
        if hook:
            return 0
        print("migrate could not find a git repository at %s" % Path.cwd(), file=sys.stderr)
        return 1
    if hook:
        sys.stdout.write(session_text(root))
        return 0
    return {"status": status, "upgrade": upgrade}[command](root)
