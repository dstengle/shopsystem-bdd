---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-7/review-1
kind: review
batch: batch-7
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/22
head: ed999ad78bddfd1e304c52f02f5854e0936ab65b
range: 78d8243a237d6c69ee86659118a584119b1b6c0d..ed999ad78bddfd1e304c52f02f5854e0936ab65b
result: clean
---

# batch-7 review 1

## Verdict

The batch builds b51's one line, backlog#r18. Every `work` commit now goes through `shop_files.committed`, which pushes it afterwards. When git refuses the push, the commit is kept, `not pushed: <remote>: <reason>` is printed and the command exits 0. The scenario @g18 checks this against a remote whose pre-receive hook refuses every push. All runs exit 0, no test is removed or weakened, and the size (+157 −24) is under the 1000-line limit. Nothing needs fixing before merge; three observations follow.

## Findings

### f1 Minor observation: a slow or unreachable remote now blocks every committing command
- item: b51
- where: scripts/shop_files.py:135
The risk: every `work idea`, `shape`, `rate`, `ready`, `quote`, `record` and `decision` now waits for a network push. `GIT_TERMINAL_PROMPT=0` only stops git's own credential prompt over HTTPS. An SSH remote that asks for a passphrase or host-key confirmation, or a remote that does not answer, can still hang the command until the connection times out. For batch commands, that wait happens while the batch lock is held (`committed` is called from `batch_plan.commit` inside `locked`). What I checked: `push_failure` passes no timeout and does not set `GIT_SSH_COMMAND`, for example with `-o BatchMode=yes`. No line names this case, so it is hardening. A later item could add `BatchMode=yes` and a timeout to the push.

### f2 Minor observation: `git push -u` on every commit resets the upstream of whatever branch is checked out
- item: b51
- where: scripts/shop_files.py:135
`pushed` pushes the branch checked out in `root` with `-u`. Someone who runs a committing `work` command inside a task worktree (`batch-<n>-t<k>`) will push that task branch to `origin` and set its upstream. Before this batch, nothing published a task branch. Every `work` command also rewrites `branch.<b>.remote` and `branch.<b>.merge` of the current branch. To reproduce: in a task worktree with `origin` set, run `work idea "x"`; `git ls-remote origin` then lists the task branch. No line says which branch a command commits on, so this is an observation. Pushing without `-u` when the branch already has an upstream would avoid the config rewrite.

### f3 Minor observation: this release changes two things in the workflow, against decision 0016
- item: b51
- where: skills/building-a-batch/SKILL.md:39
Decision 0016 (an-experiment-is-a-release, judgement) says each version changes one thing, so that `measure compare` can attribute the difference. This batch makes two changes:
- every commit is now pushed;
- the session no longer asks the person: it readies an item and starts the next batch itself (building-a-batch step 7, shaping-items step 6).

The second one changes how the next batch is driven, so the next measured batch cannot tell which change made the difference. Both changes come from the item's notes (quote-5). No requirement line asks for the skill change, but skills are not `work`'s observable behaviour, so this is not code no line asks for. Either release them apart or record in the release note that they are measured together.
