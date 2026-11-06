---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-8/review-1
kind: review
batch: batch-8
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/23
head: cd5c94e7c9262a63d5397dfc503a7d44ea454fdf
range: 6e0ce1b6d99f0f90c5f23b3fa4dafa8f875dacd7..cd5c94e7c9262a63d5397dfc503a7d44ea454fdf
result: fix-now
---

# batch-8 review 1

## Verdict

Both items are built: the push is bounded in time (r19), a branch with an upstream is pushed to that upstream without `-u` (r21), and `work idea` is refused on a task's branch, naming the task, before anything is written (r20). The size and the runs are clean. One finding to fix: the new push environment overrides how the person has told git to reach the remote over ssh.

## Findings

### f1 Important fix now: the push environment overrides `core.sshCommand` and `GIT_SSH`
- item: b56
- where: scripts/shop_files.py:117
`push_env` always sets `GIT_SSH_COMMAND`. When the variable is empty it is set to `ssh -o BatchMode=yes`:

```
ssh = os.environ.get("GIT_SSH_COMMAND", "").strip() or "ssh"
return dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_SSH_COMMAND=ssh + " -o BatchMode=yes")
```

Git gives `$GIT_SSH_COMMAND` precedence over the `core.sshCommand` setting and over `$GIT_SSH`. So the push now ignores a repository that reaches its remote with `core.sshCommand = ssh -i ~/.ssh/deploy_key`, and a setup that uses `GIT_SSH=plink`. Before this change those pushes went through; now they fail as `not pushed: origin: ...`. The commit is kept, but U4 is lost (a command's commit is on the remote) for anyone who configures ssh that way. No line asks for that, and r19 only asks that a silent remote not hang the command.

Fix: start from the command git would use. Take `$GIT_SSH_COMMAND` if it is set, else `git config core.sshCommand`. If neither is set but `$GIT_SSH` is, leave the ssh environment alone. Fall back to `ssh` only after that, and only then add `-o BatchMode=yes`. The timeout already guarantees that the push ends, so it does not depend on BatchMode. Add a test of `push_env` with `core.sshCommand` set.

### f2 Minor observation: a process outside the push's group can still hang the push past its timeout
- item: b56
- where: scripts/shop_files.py:142
When the timeout fires, `bounded` kills the process group and then calls `proc.communicate()` with no timeout. That call waits for end-of-file on the captured pipes. A process that started its own session and kept stderr open is not killed with the group, so the pipes stay open. The case I can name is an ssh ControlPersist master forked by the push. In that case the second `communicate()` blocks forever, and r19's "exit successfully" does not hold. I did not reproduce this; it is from reading the code. Hardening: give the second `communicate()` a short timeout too, and if it runs out, close `proc.stdout` and `proc.stderr` and return None.

### f3 Minor observation: the task-branch refusal covers every committing command, not only `work idea`
- item: b57
- where: scripts/shop_files.py:79
`refuse_task_branch` is called from `committed`. That means `work record`, `work decision`, `work quote`, `work outcome`, `work line` and the rest are all refused on a `batch-<n>-b<j>` branch. r20 only names `work idea`. I checked the batch commands: they commit through `batch_plan.commit`, which `on_base` restricts to the base branch, so none of them is broken by this. The wider refusal matches the existing rule that a task's commits leave `.shop/` alone, so it is consistent. Still, no line states it. Writing a universal line, or one line per command, would put it in the spec.

### f4 Minor observation: the backlog's `ThenExitsErr task` handler never passes a step on to the next handler
- item: b57
- where: tests/scenarios/backlog_handlers_upstream.py:328
`batches_handlers.refused_naming_task` now returns False for a step whose last run was not `work batch`, so that the backlog handler gets it. The backlog handler never returns False, and reads `step.context["task_branches"]` without checking it is there. This only works because of the order in which the two handlers are registered. If that order changes, the batches scenarios fail with a KeyError. Returning False when `task_branches` is missing would make the chain work in either order.

### f5 Minor observation: a 60 s default may time out a slow first push of a large branch
- item: b56
- where: scripts/shop_files.py:124
A large `-u` push over a slow link can legitimately take longer than 60 s. It would then be reported as `timed out after 60 s` and left unpushed. That is recoverable, since the commit is kept and `$SHOPSYSTEM_PUSH_TIMEOUT` raises the limit, but the default is not in any documentation the person reads.
