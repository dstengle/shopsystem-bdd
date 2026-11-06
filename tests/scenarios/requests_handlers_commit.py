"""Handlers of features/requests.feature's uncommittable repository (b36, requests r45-r47): a repository whose git
refuses every commit, by a pre-commit hook that fails, installed once the repository is in git, before the run
(requests_handlers.run_work's `before_run`); and what `work` did not post or close, read back from the stand-in gh's
calls."""
import sys

from vocab import handler

W = sys.modules["shop_work_queue_world"]
local = W.local
HOOK = "#!/bin/sh\necho 'the pre-commit hook refuses the commit' >&2\nexit 1\n"


def uncommittable(step):
    hook = step.repo / ".git" / "hooks" / "pre-commit"
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text(HOOK)
    hook.chmod(0o755)
    W.git(step.repo, "config", "core.hooksPath", str(hook.parent))


@local("GivenK_C", "repository")
def repository_is(step):
    if step.text.rsplit(" is ", 1)[1] != "uncommittable":
        return False
    step.context.setdefault("before_run", []).append(uncommittable)


def calls(step, *words):
    Q = sys.modules["shop_requests_world"]
    return [argv for argv in Q.gh_calls(step) if argv[:len(words)] == list(words)]


@handler("ThenDoesNot", "post")
def posts_not(step):
    """An issue: no `gh issue create`; a comment: no `gh issue comment`."""
    words = ("issue", "create") if step.nps[-1].startswith("the issue") else ("issue", "comment")
    assert not calls(step, *words), (step.text, calls(step, *words))


@handler("ThenDoesNot", "close")
def closes_not(step):
    assert not calls(step, "issue", "close"), (step.text, calls(step, "issue", "close"))
