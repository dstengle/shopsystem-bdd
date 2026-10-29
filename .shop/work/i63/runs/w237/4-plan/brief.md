# plan of w237

Work-item: .shop/work/i63/w237.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: db2873b73a08e86a12a10f8de97aae3b22914af6
Worktree: /tmp/work-run-i63-mt1u2rt6/w237-4-plan
Branch: none (a detached checkout)
Work-item branch: work/w237
Answers the person gave, each with the question it answers:
- Question: the researcher's file set is missing: the researcher's result gave no question and does not give it
  Answer: 2026-10-29: The file set is in the research notes, part 4: scripts/supervise_faults.py and tests/scenarios/supervision_faults_steps.py. Give it as the result's fileset field, and nothing else changes (answered by the coordinator under the person's delegation, 2026-10-29)
- Question: When a session of initiative i2 changes .shop/work/i2/initiative.md in the main checkout while a session of i1 works, and a later session of i2 (its gate, apply or formulate round) ends with that change still uncommitted, which requirement governs i2's own check: r218 (its own part is checked) or r215/r216 (no put-back, no fault for that change)? Reading A (r218 governs i2's own sessions; code as it is): i2's ending round puts the file back to its last commit and is taken as a fault, recorded under p2's ## Faults, with p2 keeping its status. Whether the person sees this depends on timing, so the r215 and r216 scenarios hold only when every i2 session ends before the write. Reading B (r215/r216 govern every session, i2's own included): no session of i1 or i2 is faulted and the file stays as i2's session left it. work run must then tell, in i2's check, a change made by an i2 session while an i1 session worked from one it must put back under r218. That needs a record of the change's writer, which the code does not keep, and a change in Faults.checkout_changes.
  Answer: 2026-10-29: Reading A: r218 governs i2's own sessions, as gate question 2 took (a, recommended): r215 and r216 cover a change made by another initiative's session, and r6, r34 and r218 still apply to a session's own initiative. Keep the code as it is, and make the r215 and r216 scenarios independent of timing: the i2 change is made by the i2 session that is working while i1's session works, and that i2 session's own end takes it in as work run does, so no later i2 round finds it uncommitted; the scenarios pass on every run, alone and under -n auto (answered by the coordinator under the person's delegation, 2026-10-29)

Read (paths in your worktree):
- .shop/work/i63/w237.md
- spec/capabilities/supervision.md
- .shop/work/i63/runs/w237/1-research
- .shop/work/i63/runs/w237/2-research
- .shop/work/i63/runs/w237/3-plan

Run directory: /tmp/work-run-i63-mt1u2rt6/w237-4-plan/.shop/scratch/4-plan
Result file: /tmp/work-run-i63-mt1u2rt6/w237-4-plan/.shop/scratch/4-plan/result.json

You start in your worktree, /tmp/work-run-i63-mt1u2rt6/w237-4-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
