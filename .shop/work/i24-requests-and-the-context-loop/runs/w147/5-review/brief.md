# review of w147

Work-item: .shop/work/i24-requests-and-the-context-loop/w147.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w147-5-review
Branch: none (a detached checkout)
Work-item branch: work/w147
Answers the person gave, each with the question it answers:
- Question: Important, scripts/supervise.py:193 / scripts/supervise_answers.py:59: the answer pass runs once at the start of run(), so questions raised in the same run (gate round r69/r85, worker r5) go to the person with exit 3 instead of a session (r77; plan D6 not done); Important, scripts/supervise_answers.py:85-96: a faulted answer session raises Refused leaving its stage dir, log.jsonl lines and written answers uncommitted, so the next work run is refused (r46) and the work-item is not moved to failed (r45)
  Answer: 2026-10-25: Accept the work-item as it stands (the coordinator, under the person's delegation): a faulted answer session gets a supervision line first (integrate round 8) and its own fix work-item; questions raised during a run going to the person rather than to a session in the same run are accepted for now and recorded as an observation.

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w147.md
- spec/capabilities/supervision.md
- .shop/work/i24-requests-and-the-context-loop/runs/w147/1-research
- .shop/work/i24-requests-and-the-context-loop/runs/w147/2-plan
- .shop/work/i24-requests-and-the-context-loop/runs/w147/3-implement
- .shop/work/i24-requests-and-the-context-loop/runs/w147/4-review

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w147-5-review/.shop/scratch/5-review
Result file: /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w147-5-review/.shop/scratch/5-review/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w147-5-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
