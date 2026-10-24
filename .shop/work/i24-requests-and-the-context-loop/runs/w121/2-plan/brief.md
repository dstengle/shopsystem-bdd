# plan of w121

Work-item: .shop/work/i24-requests-and-the-context-loop/w121.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w121-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w121
Questions the researcher gave with its DONE, for you to settle or ask:
- F2: a probe test kept (r55) next to an unaccepted scenario of a non-guarantees capability: r56 literally refuses the run; r55 says keep the probe. Plan should choose: refuse (today) or run the probe and deselect.
- I: a work-item accepting a requirement whose capability file is missing: treat as not guarantees (refuse) or unknown (refuse too). Both refuse today; the plan should state which the tests pin.

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w121.md
- spec/capabilities/supervision.md
- .shop/work/i24-requests-and-the-context-loop/runs/w121/1-research

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w121-2-plan/.shop/scratch/2-plan
Result file: /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w121-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-4_2sh8kq/w121-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
