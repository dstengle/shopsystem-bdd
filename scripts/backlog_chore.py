"""An item's chore (capability readiness r51-r54, batches r41-r43; b316): what an item with no behaviour a scenario
checks names in place of requirement lines, the files its work changes and the command whose exit code 0 shows it
done, kept as the item file's section `## Chore`:

    Files:
    - scripts/foo.py
    - docs/guide/

    Check: `python3 -m pytest -q tests/scripts/test_foo.py`

`work chore` writes it (and, run again, replaces it) and commits the item; a path under spec/, features/ or .shop/ is
refused (lines own spec/ and features/, `work` owns .shop/). A chore and requirement lines exclude each other:
`work chore` refuses an item that holds a requirement, `work line` one that holds a chore (`refuse_line`). `work
batch done` runs the check in the task's worktree and refuses a commit of the task that touches a path the chore does
not name (`run`, `outside`)."""
import posixpath
import subprocess
from typing import NamedTuple

from backlog_items import Refused, commit, find, label, one_line
from backlog_section import SECTION, takes

HEADING = "Chore"
OWNED = ("spec", "features", ".shop")
TAKES = ("idea", "shaped")       # an in-batch item's chore is not changed: `work batch amend` lays only lines (b460)


class Chore(NamedTuple):
    files: tuple
    check: str

    def covers(self, path):
        """Whether `path` is a file the chore names or is under a directory it names."""
        return any(path == f or path.startswith(f.rstrip("/") + "/") for f in self.files)


def name(item, chore):
    """How `work` names an item's chore: `the chore of b3 "Title" (check: `cmd`)`."""
    return "the chore of %s (check: `%s`)" % (label(item), chore.check)


def read(item):
    """The item's chore, or None when it has no `## Chore`; a malformed section is refused, naming the item."""
    text = item.sections.get(HEADING)
    if text is None:
        return None
    files, check = [], None
    for line in text.splitlines():
        if line.startswith("- "):
            files.append(line[2:].strip())
        elif line.startswith("Check: `") and line.endswith("`"):
            check = line[len("Check: `"):-1]
        elif line.strip() and line.strip() != "Files:":
            raise Refused("%s: ## Chore: the line %r is not `Files:`, a `- <path>` bullet or `Check: `<command>``" % (
                label(item), line))
    if not files or not check:
        raise Refused("%s: ## Chore names no %s" % (label(item), "file" if not files else "check"))
    return Chore(tuple(files), check)


def render(chore):
    return "Files:\n%s\n\nCheck: `%s`" % ("\n".join("- %s" % f for f in chore.files), chore.check)


def _path(path):
    """`path` as a repository-relative POSIX path; refused when it leaves the repository or is under spec/, features/
    or .shop/."""
    clean = posixpath.normpath(one_line(path, "file").replace("\\", "/"))
    if clean.startswith(("/", "../")) or clean in (".", ".."):
        raise Refused("work chore: the file %s is not a path inside the repository" % path)
    if clean.split("/")[0] in OWNED:
        raise Refused("work chore: the file %s is under %s/, which %s" % (
            path, clean.split("/")[0], "`work` owns" if clean.startswith(".shop") else "requirement lines own"))
    return clean + ("/" if path.rstrip().endswith("/") else "")


def requirements(item):
    """The item's `## Requirements` text, stripped ("" when it has none)."""
    return (item.sections.get(SECTION) or "").strip()


def write(root, item_name, files, check):
    """`work chore`: the item's `## Chore` written (or replaced) and the item committed; refused while the item holds
    a requirement, naming it."""
    item = find(root, item_name)
    takes(item, "work chore", TAKES)
    held = requirements(item)
    if held:
        import backlog_lines
        ids = backlog_lines.ids(backlog_lines.read(item, "the item")) or [held.splitlines()[0]]
        raise Refused("work chore: %s holds the requirement %s; a chore and requirement lines exclude each other" % (
            label(item), ", ".join(ids)))
    if not files:
        raise Refused("work chore: give the files the work changes, each with --file")
    chore = Chore(tuple(dict.fromkeys(_path(f) for f in files)), one_line(check, "check"))
    item.sections[HEADING] = render(chore)
    commit(root, item, "work chore: %s" % label(item))
    return item, chore


def refuse_line(root, item_name):
    """`work line`'s refusal of an item that holds a chore, naming the chore."""
    item = find(root, item_name)
    chore = read(item)
    if chore is not None:
        raise Refused("work line: %s holds %s; a chore and requirement lines exclude each other" % (
            label(item), name(item, chore)))


def outside(chore, paths):
    """The paths of `paths` the chore does not name, in order."""
    return [p for p in paths if not chore.covers(p)]


def run(chore, tree):
    """The chore's check run in `tree` by the shell: (exit code, its output's last lines)."""
    done = subprocess.run(chore.check, shell=True, cwd=tree, capture_output=True, text=True)
    return done.returncode, "\n".join((done.stdout + done.stderr).splitlines()[-20:])


def cmd_chore(args):
    item, chore = write(args.root, args.name, args.file, args.check)
    print("%s: %s" % (label(item), name(item, chore)))
    return 0


def add_parser(sub):
    p = sub.add_parser("chore", help="write a chore into an item in place of requirement lines: the files its work "
                       "changes and the command whose exit 0 shows it done, and commit it")
    p.add_argument("name")
    p.add_argument("--file", action="append", default=[], help="a file or directory the work changes (repeatable)")
    p.add_argument("--check", required=True, help="the command whose exit code 0 shows the work done")


def unlined(item):
    """The readiness bar's reasons of an item that holds a chore: none, unless it holds requirement lines too."""
    if requirements(item):
        return ["it holds a chore and requirement lines, which exclude each other: take one of them out"]
    return []


def said(item):
    """The chore's lines in a brief, in place of requirement ids: its files and its check; none for an item with no
    chore."""
    chore = read(item)
    if chore is None:
        return []
    return ["Chore: build it until its check passes; `shop work batch done` runs it",
            "Chore files (a commit of the task touches no other path): %s" % ", ".join(chore.files),
            "Chore check: `%s`" % chore.check]


def touched(root, since, branch, item_name):
    """The paths each commit on `branch` after `since` that cites the item `item_name` touches, merges left out."""
    import shop_files
    out = shop_files.git(root, "log", "--no-merges", "--format=%x1e%(trailers:key=Item,valueonly,separator=%x2c)%x00",
                         "--name-only", "%s..%s" % (since, branch))
    paths = []
    for entry in filter(str.strip, out.split("\x1e")):
        cited, _, names = entry.partition("\x00")
        if item_name in {c.strip() for c in cited.split(",")}:
            paths += [p for p in names.splitlines() if p.strip()]
    return list(dict.fromkeys(paths))


def in_scope(root, since, branch, item, said_as):
    """`work batch done`'s refusal of a chore item's commit that touches a path its chore does not name, naming it."""
    chore = read(item)
    if chore is None:
        return
    found = outside(chore, touched(root, since, branch, item.name))
    if found:
        raise Refused("%s: a commit on %s touches %s, which %s does not name" % (
            said_as, branch, ", ".join(found), name(item, chore)))


def passes(item, tree, said_as):
    """`work batch done`'s refusal of a chore item while its check exits non-zero in `tree`, naming the chore."""
    chore = read(item)
    if chore is None:
        return
    code, tail = run(chore, tree)
    if code != 0:
        raise Refused("%s: %s fails in %s (exit %d):\n%s" % (said_as, name(item, chore), tree, code, tail))


COMMANDS = {"chore": cmd_chore}
