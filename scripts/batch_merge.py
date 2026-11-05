"""The merge of an item's branch into its batch's branch (capability batches; workflow simplification plan 4, D5,
D6), in the batch's worktree, with `--no-ff` and a message citing the item.

Every item's ids are in its capability's `unbuilt:` on the batch branch, and each task takes its own out. Two items
of one capability so change the same line of the same file, which git cannot merge; that conflict alone is settled
here: when a conflicted file merges cleanly with its `unbuilt:` line set aside, the line is written with the base's
ids still unbuilt on both sides, then each id either side added (plan 4 review, M6). Any other conflict aborts the merge and is refused."""
import re
import subprocess
import tempfile
from pathlib import Path

from batch_git import git
from workqueue import Refused

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
    base, ours, theirs = (_stage(tree, n, path) for n in (1, 2, 3))
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


def merge(tree, branch, message):
    """`branch` merged into the worktree's branch; refused with git's first line when it does not merge."""
    done = subprocess.run(["git", "merge", "-q", "--no-ff", "-m", message, branch], cwd=tree, capture_output=True,
                          text=True)
    if done.returncode == 0:
        return
    conflicted = git(tree, "diff", "--name-only", "--diff-filter=U").stdout.split()
    texts = {path: settled(tree, path) for path in conflicted}
    if conflicted and None not in texts.values():
        for path, text in texts.items():
            (Path(tree) / path).write_text(text)
        git(tree, "add", "--", *conflicted)
        git(tree, "commit", "-q", "--no-edit")
        return
    subprocess.run(["git", "merge", "--abort"], cwd=tree, capture_output=True)
    said = [line for line in (done.stdout + done.stderr).splitlines() if line.startswith("CONFLICT")]
    raise Refused("%s does not merge: %s" % (branch, said[0] if said else (done.stderr.strip() or "exit %d" %
                                                                            done.returncode).splitlines()[0]))
