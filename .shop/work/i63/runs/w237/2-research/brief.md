# research of w237

Work-item: .shop/work/i63/w237.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: db2873b73a08e86a12a10f8de97aae3b22914af6
Worktree: /tmp/work-run-i63-83zvvln9/w237-2-research
Branch: none (a detached checkout)
Work-item branch: work/w237
Accepted scenarios:
- features/supervision.feature: what changed in the repository's own checkout while a session of one initiative worked is checked without the paths of another initiative run side by side
- features/supervision.feature: a change to another initiative's path under .shop/work/, made by that initiative's session while a session of one initiative worked, is not put back
- features/supervision.feature: a change to another initiative's path under .shop/work/, made by that initiative's session while a session of one initiative worked, faults no session
Answers the person gave, each with the question it answers:
- Question: the researcher's file set is missing: the researcher's result gave no question and does not give it
  Answer: 2026-10-29: The file set is in the research notes, part 4: scripts/supervise_faults.py and tests/scenarios/supervision_faults_steps.py. Give it as the result's fileset field, and nothing else changes (answered by the coordinator under the person's delegation, 2026-10-29)

Read (paths in your worktree):
- .shop/work/i63/w237.md
- spec/capabilities/supervision.md
- .shop/work/i63/runs/w237/1-research

Run directory: /tmp/work-run-i63-83zvvln9/w237-2-research/.shop/scratch/2-research
Result file: /tmp/work-run-i63-83zvvln9/w237-2-research/.shop/scratch/2-research/result.json

You start in your worktree, /tmp/work-run-i63-83zvvln9/w237-2-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
