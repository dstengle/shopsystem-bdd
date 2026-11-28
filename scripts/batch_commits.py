"""The checks of a task's own commits, those on its branch after the commit that keeps its item applied
(batch_tasks' `lines_commit`), which `work batch done` and `work batch review` share: a commit that cites no item
(`uncited`, D10), the paths under `.shop/` one changes (`under_shop`, D4), and a kept change that touches a feature
(`touching_feature`, batches r205, b889): a task's `features/` are written only by the specification service's apply,
at opening and at an amend, and the batch's are rebuilt from the base at submit, so a hand edit of one would be
lost."""
import re

from batch_git import git

SHOP = (".shop/backlog", ".shop/batches")
FEATURES = "features"


def uncited(root, since, branch, names):
    """`<short sha> "<subject>"` of each commit on `branch` after `since` with no `Item: <item>` line for one of the
    item names `names` (D10)."""
    out = git(root, "log", "--format=%h%x00%s%x00%(trailers:key=Item,valueonly,separator=%x2c)%x00%B%x1e",
              "%s..%s" % (since, branch)).stdout
    found = []
    for entry in filter(str.strip, out.split("\x1e")):
        sha, subject, cited, body = entry.strip("\n").split("\x00")
        if not set(names) & {c.strip() for c in cited.split(",")}:
            unread = re.search(r"(?m)^Item: ", body) and not cited.strip()
            found.append('%s "%s"%s' % (sha, subject, " (its Item: line is not in the message's last paragraph, "
                                        "and git reads trailers from the last paragraph only)" if unread else ""))
    return found


def under_shop(root, since, branch):
    """The paths under `.shop/backlog/` or `.shop/batches/` a commit on `branch` after `since` changes (D4)."""
    out = git(root, "log", "--format=", "--name-only", "%s..%s" % (since, branch), "--", *SHOP).stdout
    return sorted(set(filter(None, out.splitlines())))


def touching_feature(root, since, branch, batch):
    """`<short sha> "<subject>"` of each commit on `branch` after `since` that touches a path under `features/`,
    other than an amend's (`<batch>: the requirement lines of ... amended`, batch_amend), whose apply writes them."""
    out = git(root, "log", "--format=%h%x00%s", "%s..%s" % (since, branch), "--", FEATURES).stdout
    amended = "%s: the requirement lines of " % batch
    return ['%s "%s"' % (sha, subject) for sha, _, subject in (line.partition("\0") for line in out.splitlines())
            if not (subject.startswith(amended) and subject.endswith(" amended"))]
