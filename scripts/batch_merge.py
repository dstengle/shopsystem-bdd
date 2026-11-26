"""The merge of an item's branch into its batch's branch (capability batches; workflow simplification plan 4, D5,
D6; reviews r7, r8, b491), in the batch's worktree, with `--no-ff` and a message citing the item, each task's branch
after the ones before it. git's rerere is on for the merge and its commit, so a resolution recorded before (a driver
settling a conflict by hand) is used again and one settled now is recorded.

Every item's ids are in its capability's `unbuilt:` on the batch branch, and each task takes its own out. Two items
of one capability so change the same line of the same file, which git cannot merge; that conflict alone is settled
here: when a conflicted file merges cleanly with its `unbuilt:` line set aside, the line is written with the base's
ids still unbuilt on both sides, then each id either side added (plan 4 review, M6). Any other conflict aborts the merge and is refused, naming each file left unsettled, the item merged and every other item whose
branch conflicts with its branch in that file (`clashing`).

An id of the item that its branch holds as a line and has taken out of `unbuilt:` is built: once merged it is out of
the batch branch's `unbuilt:` too (`built`, reviews r13, b600). An amend lays a line on the batch branch and on the
task's branch in two commits, neither an ancestor of the other, so git keeps the batch branch's `unbuilt:` entry of
a line the task then built."""
import re
import subprocess
import tempfile
from pathlib import Path

import spec_unbuilt
from batch_git import git
from shop_files import Refused

RERERE = ("-c", "rerere.enabled=true", "-c", "rerere.autoUpdate=true")

UNBUILT = re.compile(r"(?m)^unbuilt:[ \t]*\[(.*)\][ \t]*$")
MARK = "unbuilt: [<set aside by work batch review>]"


def _stage(tree, n, path):
    done = subprocess.run(["git", "show", ":%d:%s" % (n, path)], cwd=tree, capture_output=True, text=True)
    return done.stdout if done.returncode == 0 else None


def _ids(text):
    found = UNBUILT.search(text)
    return [one.strip() for one in found.group(1).split(",") if one.strip()] if found else None


def settled(tree, path):
    """The text of the conflicted `path` with its `unbuilt:` lines reconciled, or None when it has another
    conflict."""
    return reconciled(*(_stage(tree, n, path) for n in (1, 2, 3)))


def reconciled(base, ours, theirs):
    """The merge of three texts of a file with its `unbuilt:` lines reconciled, or None when it has another
    conflict."""
    if None in (base, ours, theirs) or None in map(_ids, (base, ours, theirs)):
        return None
    with tempfile.TemporaryDirectory(prefix="batch-merge-") as tmp:
        files = []
        for name, text in (("ours", ours), ("base", base), ("theirs", theirs)):
            files.append(Path(tmp) / name)
            files[-1].write_text(UNBUILT.sub(MARK, text, count=1))
        done = subprocess.run(["git", "merge-file", "-p", *map(str, files)], capture_output=True, text=True)
    if done.returncode != 0:
        return None
    was, mine, other = _ids(base), _ids(ours), _ids(theirs)
    left = [one for one in was if one in mine and one in other]
    left += [one for one in mine + other if one not in was and one not in left]
    return done.stdout.replace(MARK, "unbuilt: [%s]" % ", ".join(left), 1)


def _blob(tree, oid):
    return subprocess.run(["git", "cat-file", "blob", oid], cwd=tree, capture_output=True, text=True).stdout


def clashes(tree, branch, other):
    """The paths in which `branch` and `other` conflict, other than in their `unbuilt:` lines (git merge-tree)."""
    done = subprocess.run(["git", "merge-tree", "--write-tree", "--no-messages", branch, other], cwd=tree,
                          capture_output=True, text=True)
    if done.returncode != 1:
        return []
    stages = {}
    for line in done.stdout.splitlines()[1:]:
        info, _, name = line.partition("\t")
        if name and len(info.split()) == 3:
            stages.setdefault(name, {})[int(info.split()[2])] = _blob(tree, info.split()[1])
    return [name for name, found in stages.items() if reconciled(*(found.get(n) for n in (1, 2, 3))) is None]


def clashing(tree, branch, other, path):
    """Whether `branch` and `other` conflict in `path`, other than in its `unbuilt:` line (git merge-tree)."""
    return path in clashes(tree, branch, other)


def _merging(tree):
    return subprocess.run(["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"], cwd=tree,
                          capture_output=True).returncode == 0


def merge(tree, branch, message, item=None, others=()):
    """`branch` (of `item`, a label) merged into the worktree's branch; refused, when a conflict is left, naming each
    file, the item and each of `others` ((label, branch) of the batch's other items) whose branch conflicts with
    `branch` there."""
    done = subprocess.run(["git", *RERERE, "merge", "-q", "--no-ff", "-m", message, branch], cwd=tree,
                          capture_output=True, text=True)
    if done.returncode == 0:
        return
    conflicted = git(tree, "diff", "--name-only", "--diff-filter=U").stdout.split()
    texts = {path: settled(tree, path) for path in conflicted}
    if _merging(tree) and None not in texts.values():
        for path, text in texts.items():
            (Path(tree) / path).write_text(text)
        if conflicted:
            git(tree, "add", "--", *conflicted)
        git(tree, *RERERE, "commit", "-q", "--no-edit")
        return
    subprocess.run(["git", "merge", "--abort"], cwd=tree, capture_output=True)
    left = [path for path, text in texts.items() if text is None]
    if not left:
        said = [line for line in (done.stdout + done.stderr).splitlines() if line.strip()]
        raise Refused("%s does not merge: %s" % (branch, said[0] if said else "exit %d" % done.returncode))
    raise Refused("%s does not merge: %s" % (branch, "; ".join(
        "%s conflicts between %s and %s" % (path, item or branch, ", ".join(
            [label for label, other in others if clashing(tree, branch, other, path)]) or "the batch's branch")
        for path in left)))


def built(tree, branch, ids):
    """Each of `ids` (`<capability>#r<n>`, the merged item's) that `branch` holds as a line and lists no more as
    unbuilt taken out of the worktree's `unbuilt:`, in the merge commit just made; the paths changed."""
    second = subprocess.run(["git", "rev-parse", "-q", "--verify", "HEAD^2"], cwd=tree, capture_output=True, text=True)
    if second.stdout.strip() != git(tree, "rev-parse", branch).stdout.strip():
        return []           # no merge commit of the branch made: it was merged before
    caps = {}
    for ident in ids:
        cap, _, rid = ident.partition("#")
        caps.setdefault(cap, []).append(rid)
    changed = []
    for cap, rids in caps.items():
        rel = "spec/capabilities/%s.md" % cap
        path = Path(tree) / rel
        done = subprocess.run(["git", "show", "%s:%s" % (branch, rel)], cwd=tree, capture_output=True, text=True)
        if not path.is_file() or done.returncode != 0:
            continue
        text, theirs = path.read_text(), done.stdout
        gone = [r for r in rids if r in (_ids(text) or []) and r not in (_ids(theirs) or []) and "[%s]" % r in theirs]
        if gone:
            path.write_text(spec_unbuilt.without_unbuilt(text, gone))
            changed.append(rel)
    if changed:
        git(tree, "add", "--", *changed)
        git(tree, "commit", "-q", "--amend", "--no-edit")
    return changed
