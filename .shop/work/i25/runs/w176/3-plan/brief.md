# plan of w176

Work-item: .shop/work/i25/w176.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i25-inmctmii/w176-3-plan
Branch: none (a detached checkout)
Work-item branch: work/w176
Questions the researcher gave with its DONE, for you to settle or ask:
- Q1: both --change and --accept given: refuse with an error (a), or the spec is silent (b)? No scenario covers it.
- Q2: a delegated reviewer question (scripts/supervise_answers.py:79): the answer session must give the verdict and the path refuses otherwise (a), or keep asked_from so it lands done with no verdict (b)?
- Q3: the accepted deprecated outline's reviewer row (feature 285-298) expects done for a verdict-less answer, which r28 refuses. Retire it with a Retires section in w176.md (a), or change its expectation to a refusal (b)?
- Q4: --accept sends the item to done, which work run starts a review on again (supervise.py:35,37). Implement r27 as written (a), or the supervision capability gives accepted items another status (b)?

Read (paths in your worktree):
- .shop/work/i25/w176.md
- spec/capabilities/work-queue.md
- .shop/work/i25/runs/w176/1-research
- .shop/work/i25/runs/w176/2-research

Run directory: /tmp/work-run-i25-inmctmii/w176-3-plan/.shop/scratch/3-plan
Result file: /tmp/work-run-i25-inmctmii/w176-3-plan/.shop/scratch/3-plan/result.json

You start in your worktree, /tmp/work-run-i25-inmctmii/w176-3-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
