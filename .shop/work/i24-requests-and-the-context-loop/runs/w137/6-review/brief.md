# review of w137

Work-item: .shop/work/i24-requests-and-the-context-loop/w137.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-hei00uh6/w137-6-review
Branch: none (a detached checkout)
Work-item branch: work/w137
Answers the person gave, each with the question it answers:
- Question: Where do the commits of an apply or formulate round go? The round commits spec/ (apply) or features/ (formulate) in the worktree work run gives it, and no supervision line says what becomes of them. Reading A: work run merges the round's branch into the initiative branch when the round ends, before the proposal's transition; the person sees spec/ and features/ changed on the initiative branch, with p1 approved and then formulated. Reading B: the round's branch is kept unmerged, as r26 keeps a work-item branch; the person sees p1 approved and then formulated, spec/ and features/ unchanged on the initiative branch, and the round's commits on a kept branch.; Does r70 start an apply round for an awaiting-answer capability-proposal that has no question at all? This happens when a gate's result gives none. Reading A: yes, 'every question has an answer' holds, so apply starts given no answers; the person sees p1 approved and then formulated in the same run. Reading B: no, no round starts; the person sees p1 stay awaiting-answer, and work run exits as it does on an awaiting-answer node.; What happens to a capability-proposal whose apply or formulate round's session ends in an error, at its turn limit, or without a readable result? Reading A: work run moves the proposal to failed and writes the fault under its ## Faults, as r45 does for a work-item; the person sees p1 failed, and work run exits with an error naming p1 and its fault. Reading B: the proposal keeps its status and work run exits with an error naming p1's round and its fault; the person sees p1 still awaiting-answer (or approved), and the next work run starts the round again.
  Answer: 2026-10-25: (the coordinator, under the person's delegation) Q1 reading A: work run merges the round's branch into the initiative branch when the round ends, before the proposal's transition. Q2 reading A: a proposal whose gate gave no question has every question answered, so its apply round starts. Q3 reading B: the proposal keeps its status and work run exits with an error naming the round and its fault; the next work run starts the round again.

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w137.md
- spec/capabilities/supervision.md
- .shop/work/i24-requests-and-the-context-loop/runs/w137/1-research
- .shop/work/i24-requests-and-the-context-loop/runs/w137/2-research
- .shop/work/i24-requests-and-the-context-loop/runs/w137/3-plan
- .shop/work/i24-requests-and-the-context-loop/runs/w137/4-plan
- .shop/work/i24-requests-and-the-context-loop/runs/w137/5-implement

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-hei00uh6/w137-6-review/.shop/scratch/6-review
Result file: /tmp/work-run-i24-requests-and-the-context-loop-hei00uh6/w137-6-review/.shop/scratch/6-review/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-hei00uh6/w137-6-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
