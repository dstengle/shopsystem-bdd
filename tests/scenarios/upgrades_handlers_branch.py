"""upgrades' founding on a branch other than the base branch (r46, b802), each handler a `local` of work_queue_world's
table taken before migration-tools' own: "this branch differs from this base branch" founds on `master`, the branch
`git init` gave in the new-user trial, where the base branch is `main` (`.shop/delivery.toml`'s default, which the
founding writes commented out); the When checks it out (migration_tools_handlers' `runs_migrate`, `main` otherwise);
the Then that the upgrades service names this branch reads `master` in what `migrate init` printed, beside its success."""
import re

from scenarios import migration_tools_handlers as M

local = M.local
OTHER = "master"


@local("GivenDoes")
def differs(step):
    if not M.migration(step) or not re.fullmatch(r"this branch differs from this base branch", step.text):
        return False
    step.context["branch"] = OTHER
    return None


@local("ThenDoes")
def names(step):
    if not M.migration(step) or step.term != "name" or [re.sub(r"^(the|this) ", "", np) for np in step.nps] != ["branch"]:
        return False
    assert step.context["done"].returncode == 0, M.said(step)
    assert re.search(r"\b%s\b" % OTHER, M.said(step)), M.said(step)
    return None
