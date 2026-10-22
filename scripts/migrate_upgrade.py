"""`migrate status` and `migrate upgrade` (migration-tools r15, r18-r20, r22-r24, r27, r28): the repository's plugin
version, the plugin's, the upgrade steps between them, what a session is told at its start, and the upgrade, all of it
in one commit or none of it."""
import json
import subprocess
import sys
import types
from pathlib import Path

import migrate_upgrade_ids
from migrate_write import check_moves, git, top_level, uncommitted

SCRIPTS = Path(__file__).resolve().parent
VERSION_FILE = ".shop/plugin-version"
UNRECORDED = "0.23.1"
STEPS = [("0.24.0", "work-items named by ids", "give every work-item the id w<n>", migrate_upgrade_ids)]


def number(version):
    return tuple(int(part) for part in version.split("."))


def plugin_version():
    return json.loads((SCRIPTS.parent / ".claude-plugin/plugin.json").read_text())["version"]


def repository_version(root):
    path = root / VERSION_FILE
    return path.read_text().strip() if path.is_file() else UNRECORDED


def pending(root):
    """The steps above the repository's version and not above the plugin's, oldest first (r20)."""
    here, there = number(repository_version(root)), number(plugin_version())
    return [step for step in sorted(STEPS, key=lambda s: number(s[0])) if here < number(step[0]) <= there]


def step_line(step):
    return '%s "%s": %s' % (step[0], step[1], step[2])


def status(root):
    print("the repository's plugin version: %s" % repository_version(root))
    print("the plugin's version: %s" % plugin_version())
    for step in pending(root):
        print("pending upgrade step " + step_line(step))
    return 0


def session_text(root):
    """What a session is told at its start (r22-r24, r28): nothing unless the repository has .shop/ and is behind or ahead."""
    if not (root / ".shop").is_dir():
        return ""
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
        git(root, "mv", temporary, new)
    for rel, text in changes.texts.items():
        with open(root / rel, "w", newline="") as handle:
            handle.write(text)
        git(root, "add", "-f", "--", rel)


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


def upgrade(root):
    changed = uncommitted(root)
    if changed:
        print("migrate changed nothing; it could not start from a tree with an uncommitted change: " + ", ".join(changed),
              file=sys.stderr)
        return 1
    steps = pending(root)
    if not steps:
        print("no upgrade step is pending")
        return 0
    before = repository_version(root)
    plans = [step[3].plan(root) for step in steps]
    refused = [failure for changes in plans for failure in changes.failures + move_failures(root, changes)]
    if refused:
        print("migrate changed nothing; it could not make every change:\n" + "\n".join(refused), file=sys.stderr)
        return 1
    try:
        for changes in plans:
            apply(root, changes)
        (root / VERSION_FILE).write_text(plugin_version() + "\n")
        git(root, "add", "-f", "--", VERSION_FILE)
        git(root, "commit", "-q", "-m", "migrate upgrade: %s to %s\n\n%s" % (
            before, plugin_version(), "\n".join("upgrade step " + step_line(s) for s in steps)))
    except (subprocess.CalledProcessError, OSError) as error:
        subprocess.run(["git", "reset", "-q", "--hard", "HEAD"], cwd=root, capture_output=True)
        subprocess.run(["git", "clean", "-fdq"], cwd=root, capture_output=True)
        print("migrate put the repository back as it was; it could not make every change: %s"
              % (getattr(error, "stderr", None) or error), file=sys.stderr)
        return 1
    print("upgraded to %s: %s" % (plugin_version(), ", ".join(s[1] for s in steps)))
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
