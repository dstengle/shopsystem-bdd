# review of w127

Work-item: .shop/work/i24-requests-and-the-context-loop/w127.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-4iuaa3m5/w127-5-review
Branch: none (a detached checkout)
Work-item branch: work/w127
Answers the person gave, each with the question it answers:
- Question: features/requests.feature, the requests#r17 scenario 'turn passing a request to its asker with a line that has <line 2> sets the request's status to awaiting-asker', is a Scenario Outline with no Examples table, so its Given reaches the step as the literal text '<line 2>'. The implementer may not change features/, and the plan cannot pick the cases. Which line-2 cases does it pin? Reading A: the formulation adds an Examples table with two rows, line 2 with no line outcome and line 2 with the line outcome question. The narrator runs `work turn q1` twice and sees status awaiting-asker both times. Reading B: the formulation makes it a plain Scenario naming one case (e.g. line 2 with the line outcome question). The narrator sees awaiting-asker for that one case only. Reading C: no spec change. The step reads the literal '<line 2>' as a line with no line outcome. The narrator sees awaiting-asker, but the scenario's title and step stay literal, and the case of an outcome other than accepted, refused or withdrawn is never pinned.
  Answer: 2026-10-24: Reading A (the coordinator, under the person's delegation): the formulation gave the r17 outline its Examples table in 5d4cc75, two rows: line 2 with no line outcome, and line 2 with the line outcome question. Rebase on the initiative branch and pin both.

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w127.md
- spec/capabilities/requests.md
- .shop/work/i24-requests-and-the-context-loop/runs/w127/1-research
- .shop/work/i24-requests-and-the-context-loop/runs/w127/2-plan
- .shop/work/i24-requests-and-the-context-loop/runs/w127/3-plan
- .shop/work/i24-requests-and-the-context-loop/runs/w127/4-implement

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-4iuaa3m5/w127-5-review/.shop/scratch/5-review
Result file: /tmp/work-run-i24-requests-and-the-context-loop-4iuaa3m5/w127-5-review/.shop/scratch/5-review/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-4iuaa3m5/w127-5-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
