"""A base merge (b492, reviews r9, r10, review-guarantees r10): a merge commit on a batch's branch, made after the
batch's last review, one of whose later parents is on the batch's base, as a driver makes it when the pull request
conflicts with the base after a clean review.

`work batch review` takes a batch `awaiting-merge` whose branch holds one (`resubmit`): the tests run in the batch's
worktree, the branch is pushed, and the batch is `in-review` again with the pull request it has, committed on the base;
one whose branch holds none is refused, naming the batch. `work batch brief` then reads the re-review's range, from
the last review's head, as only the base merges (`section`)."""
import shutil
import subprocess
from pathlib import Path

import batch_findings
import batch_plan
import batch_timings
from batch_git import git, push, remote, remove_tree, tree_for, trees_dir, trees_path
from plumbing.shop_files import Refused


def since(root, batch):
    """The head of the batch's last review, else the commit it forked from."""
    done = batch_findings.reviews(root, batch.name)
    return done[-1].head if done else batch.forked_from


def _on_base(root, sha, base):
    return subprocess.run(["git", "merge-base", "--is-ancestor", sha, base], cwd=root,
                          capture_output=True).returncode == 0


def merges(root, batch, head=None):
    """The base merges on the batch's branch since its last review, oldest first: (sha, subject)."""
    rows = git(root, "rev-list", "--reverse", "--merges", "--parents", "--format=%s",
               "%s..%s" % (since(root, batch), head or batch.branch)).stdout.splitlines()
    out = []
    for row, subject in zip(rows[::2], rows[1::2]):
        shas = row.split()[1:]
        if any(_on_base(root, p, batch.base) for p in shas[2:]):
            out.append((shas[0], subject))
    return out


def resubmit(root, batch, command, tests_pass):
    """The pull request's URL: the batch `awaiting-merge` whose branch holds a base merge tested, pushed and
    `in-review` (r9); refused naming the batch when its branch holds none (r10). Run under the lock, the tests by
    `tests_pass` (batch_tasks', which reaches batch_brief, which reads this module)."""
    batch_plan.on_base(root, batch)
    if not merges(root, batch):
        raise Refused("%s: %s is awaiting-merge and its branch %s holds no merge of %s since its last review; %s "
                      "takes an awaiting-merge batch once its branch merged its base" % (
                          command, batch.name, batch.branch, batch.base, command))
    fresh = not trees_path(root).is_dir()
    tree = trees_dir(root) / batch.name
    made = False
    try:
        made = tree_for(root, tree, batch.branch, command)
        with batch_timings.timed(root, batch.name, "review"):       # the test run's duration (b73)
            tests_pass(root, tree, "%s: %s" % (command, batch.name))
        push(root, remote(root, batch.base), batch.branch, command)
    except BaseException:
        if made:
            remove_tree(root, tree)
        if fresh:
            shutil.rmtree(trees_path(root), ignore_errors=True)
        raise
    batch.status = "in-review"
    batch_plan.commit(root, batch, [], "%s: %s -> in-review %s (a base merge)" % (command, batch.name,
                                                                                   batch.pull_request))
    return batch.pull_request


def section(root, tree, batch, head, where):
    """The brief's `## Base merges` of a re-review whose range holds a base merge and no open finding, else None:
    each merge with its resolution's patch (`git show --remerge-diff`: what it changed beyond merging the two sides,
    empty when it settled no conflict) written to `<where>/commits/<short sha>.merge.patch`, which with the range's
    `change.diff` is all `pr-reviewer` reviews (review-guarantees r10)."""
    found = merges(root, batch, head)
    if not found or batch_findings.open_findings(root, batch.name):
        return None
    folder = Path(where) / "commits"
    folder.mkdir(parents=True, exist_ok=True)
    lines = []
    for sha, subject in found:
        path = folder / ("%s.merge.patch" % sha[:12])
        path.write_text(git(tree, "show", "--remerge-diff", "--format=commit %H%n%n%B", sha, "--", ".",
                            ":(exclude).shop").stdout, encoding="utf-8")
        lines.append("- %s %s; resolution: %s" % (sha[:12], batch_findings.quoted(subject), path))
    return ("Review only these merges of %s into %s, made after the last clean review: `change.diff` is what they "
            "brought from the base, each resolution patch how it settled a conflict. Nothing else of the batch "
            "changed since that review.\n\n%s" % (batch.base, batch.branch, "\n".join(lines)))
