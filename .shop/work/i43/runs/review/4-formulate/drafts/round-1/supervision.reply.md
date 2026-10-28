## Coverage

| id | line | scenario |
|---|---|---|
| r156 | "**When** `work run` starts a branch review, `work run` shall give the branch reviewer the commits from the initiative branch's base to its head, each with the work-item it belongs to or none, and the change of that range less `.shop/`." | the branch reviewer is given the commits from the initiative branch's base to its head, each with the work-item it belongs to or none, and the change of that range less .shop/ |

## Questions

None. The reading of r156 was settled in the input: a commit belongs to the work-item whose work or status it commits (its implementer's commits, the merge of its branch, `work run`'s transition commits of it), and "none" holds only commits no work-item made.

## Cases no line mentions

- The merge of a work-item branch may be a fast-forward with no merge commit of its own. The neighbouring scenario at features/supervision.feature line 409 shows "no merge commit". If so, "the merge of work/w1" gives no commit to list, and the scenario's step about the merge is only true when the merge leaves a commit. The step definitions need to decide what that step checks.
- `work run` also makes commits that commit no single work-item's work or status. Examples: the commit of a kept branch review's directory (r48), the initiative's own transitions, and a capability-proposal's commits. Under the settled reading these get "none". No line says so, and they are not the "commits no work-item made" the branch reviewer reports.
- One commit might carry transitions of two work-items, for example when workers end at the same time. No line says which work-item that commit belongs to, or whether it can belong to both.
- No line says how a commit that changes only files under `.shop/` shows up: it is still listed as a commit, but it adds nothing to the change.
- No line says whether "the change of that range less `.shop/`" covers `.shop/` at every depth, such as `.shop/scratch/`, which is ignored anyway, and `.shop/delivery.toml`, which is tracked.

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/review-4-formulate/.shop/scratch/4-formulate/drafts/round-1/supervision.feature
- /home/vscode/shopsystem-bdd/.shop/worktrees/review-4-formulate/.shop/scratch/4-formulate/drafts/round-1/supervision.reply.md
