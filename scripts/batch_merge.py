"""The merge of an item's branch into its batch's branch (capability batches; workflow simplification plan 4, D5,
D6; reviews r7, r8, b491, b874), in the batch's worktree, with `--no-ff` and a message citing the item, each task's
branch after the ones before it. git's rerere is on for the merge and its commit, so a resolution recorded before (a
driver settling a conflict by hand) is used again and one settled now is recorded.

The paths the specification service's apply writes (`OWNED`: `spec/`, `features/`, the spec corpus and the
catalogues, and any other path the batch's rebuild changed) are the batch branch's own: `work batch review` rebuilt
them from the base with every in-batch item applied (batch_rebuild), so a merge keeps the batch branch's side of each
(`merge`'s `owned`), and only the ids a task built leave `unbuilt:` (`built`, reviews r15, b600). Any other conflict
aborts the merge and is refused, naming each file left unsettled, the item merged and every other item whose branch
conflicts with its branch in that file (`clashing`, of code paths only)."""
import re
import subprocess
from pathlib import Path

import spec_unbuilt
from batch_git import git
from plumbing.shop_files import Refused

RERERE = ("-c", "rerere.enabled=true", "-c", "rerere.autoUpdate=true")

UNBUILT = re.compile(r"(?m)^unbuilt:[ \t]*\[(.*)\][ \t]*$")
OWNED = ("spec/", "features/", "grammar/corpus/spec/", "grammar/rules.md", "grammar/constructs.md")


def _ids(text):
    found = UNBUILT.search(text)
    return [one.strip() for one in found.group(1).split(",") if one.strip()] if found else None


def is_owned(path, owned=()):
    """Whether the path is one the specification service's apply writes (`OWNED`, or one of `owned`)."""
    return path in owned or any(path == o.rstrip("/") or path.startswith(o) for o in OWNED if o.endswith("/")) or \
        path in OWNED


def clashes(tree, branch, other):
    """The paths in which `branch` and `other` conflict, other than those the apply writes (git merge-tree)."""
    done = subprocess.run(["git", "merge-tree", "--write-tree", "--no-messages", branch, other], cwd=tree,
                          capture_output=True, text=True)
    if done.returncode != 1:
        return []
    names = []
    for line in done.stdout.splitlines()[1:]:
        info, _, name = line.partition("\t")
        if name and len(info.split()) == 3 and not is_owned(name) and name not in names:
            names.append(name)
    return names


def clashing(tree, branch, other, path):
    """Whether `branch` and `other` conflict in `path`, a path the apply does not write (git merge-tree)."""
    return path in clashes(tree, branch, other)


def _merging(tree):
    return subprocess.run(["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"], cwd=tree,
                          capture_output=True).returncode == 0


def _ours(tree, owned):
    """Each path the apply writes taken as the worktree's branch holds it, a file only the merged branch added there
    taken out."""
    held = set(git(tree, "ls-tree", "-r", "--name-only", "HEAD").stdout.splitlines())
    staged = set(git(tree, "ls-files").stdout.splitlines()) | set(
        git(tree, "diff", "--name-only", "--diff-filter=U").stdout.splitlines())
    mine = sorted(p for p in held if is_owned(p, owned))
    for k in range(0, len(mine), 200):
        git(tree, "checkout", "HEAD", "--", *mine[k:k + 200])
    added = sorted(p for p in staged - held if is_owned(p, owned))
    if added:
        git(tree, "rm", "-q", "-f", "--", *added)


def merge(tree, branch, message, item=None, others=(), owned=()):
    """`branch` (of `item`, a label) merged into the worktree's branch, the paths the apply writes kept as the
    worktree's branch holds them; refused, when another conflict is left, naming each file, the item and each of
    `others` ((label, branch) of the batch's other items) whose branch conflicts with `branch` there."""
    done = subprocess.run(["git", *RERERE, "merge", "-q", "--no-ff", "--no-commit", branch], cwd=tree,
                          capture_output=True, text=True)
    if not _merging(tree):
        if done.returncode == 0:
            return              # merged before: nothing to merge
        said = [line for line in (done.stdout + done.stderr).splitlines() if line.strip()]
        raise Refused("%s does not merge: %s" % (branch, said[0] if said else "exit %d" % done.returncode))
    _ours(tree, owned)
    left = git(tree, "diff", "--name-only", "--diff-filter=U").stdout.split()
    if not left:
        git(tree, *RERERE, "commit", "-q", "-m", message)
        return
    subprocess.run(["git", "merge", "--abort"], cwd=tree, capture_output=True)
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
    changed = built_on(tree, branch, ids)
    if changed:
        git(tree, "commit", "-q", "--amend", "--no-edit")
    return changed


def built_on(tree, branch, ids):
    """Each of `ids` that `branch` holds as a line and lists no more as unbuilt taken out of the worktree's
    `unbuilt:`, staged; the paths changed."""
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
    return changed
