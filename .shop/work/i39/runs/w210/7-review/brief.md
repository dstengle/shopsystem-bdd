# review of w210

Work-item: .shop/work/i39/w210.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w210-7-review
Branch: none (a detached checkout)
Work-item branch: work/w210
Answers the person gave, each with the question it answers:
- Question: supervision#r135: what does `work run` do when the raise of an integrate round's lines fails? It fails when `work request` refuses or errors: no repository that keeps requests at the Upstreams path, a line not in strict form, a blank delegation. Reading A: exit with an error naming the round, the upstream and work's reason. The round's proposals are kept and committed, with no record line. The narrator sees an error exit, the drafted proposals, no request in the upstream, and later the proposal's work-items drafted unheld, because nothing retries the raise. Reading B: write a question naming the failed raise under the initiative's ledger (or the proposals' ## Questions), keep the proposals and go on. The narrator sees the question and an exit awaiting an answer. Reading C: write no proposal and commit nothing from the round, then exit with an error, as r10 does. The narrator sees an error exit, the initiative still started with no proposal, and the round run again next time.; supervision#r136: when work run checks whether a raised request is delivered and the upstream's request cannot be read (no checkout at the Upstreams path, or the request missing there), is the proposal held? Reading A: held, so no work-item is drafted until the request reads as delivered. The narrator sees the proposal formulated with no work-items. Reading B: not held, because only a request read as not delivered holds it. The narrator sees its work-items drafted. Reading C: fall back to the last status in this context's raised.jsonl, which nothing updates. In practice the narrator sees it held.
  Answer: 2026-10-27: r135: Reading C, write no proposal and commit nothing from the round, then exit with an error naming the round, the upstream and work's reason, as r10 does; the round runs again next time (A leaves work-items drafted unheld with no retry, B leaves the proposals half-processed). r136: Reading A, held: no work-item is drafted until the upstream's request reads as delivered (drafting against an unconfirmed delivery is the riskier error) (answered by the coordinator under the person's delegation of 2026-10-27; no reading was recommended).
- Question: Important, scripts/supervise_rounds.py:161-162: a failed raise undoes the round's merge with git reset --hard on the checkout the initiatives share, after the lock was let go; other initiatives' merged commits and every run's uncommitted log.jsonl lines can be lost. Run the raise before the merge instead.; Important, scripts/supervise_rounds.py:163: a failed raise commits the round's stage directory (keep_round, 'work: <name> integrate round <label> faulted'), against the r135 ruling (reading C: commit nothing from the round) and plan decision 9.
  Answer: 2026-10-27: Fix both as the reviewer says: run the raise before the merge, so a failed raise needs no git reset on the shared checkout; and on a failed raise commit nothing from the round, per the r135 ruling (reading C) (answered by the coordinator under the person's delegation of 2026-10-27).

Read (paths in your worktree):
- .shop/work/i39/w210.md
- spec/capabilities/supervision.md
- .shop/work/i39/runs/w210/1-research
- .shop/work/i39/runs/w210/2-plan
- .shop/work/i39/runs/w210/3-plan
- .shop/work/i39/runs/w210/4-implement
- .shop/work/i39/runs/w210/5-review
- .shop/work/i39/runs/w210/6-implement

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w210-7-review/.shop/scratch/7-review
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w210-7-review/.shop/scratch/7-review/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w210-7-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
