# plan of w194

Work-item: .shop/work/i33/w194.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 1caef88132eda3084c4ef5d18d7c8deeeccaf483
Worktree: /tmp/work-run-i33-9u0pon3p/w194-3-plan
Branch: none (a detached checkout)
Work-item branch: work/w194
Answers the person gave, each with the question it answers:
- Question: w194 turns green the r121 Outline that replaces the deprecated scenario 'a kept branch review that ended PARTIAL, with no question and no finding, does not list nothing to fix now, and no `measure initiative` is run (deprecated)' (features/supervision.feature:1050). That scenario passes today and fails once r121 is in. w194 does not list it under ## Retires, because r73 matches only @r120/@r121 and it is tagged @r75, so under red-green#r2 the implementer may not retire it. Reading (a): it is added to w194's ## Retires (as decision 0011, held-scenarios, implies), and the implementer removes it and its step with `features retire`. The narrator then sees it gone from features/supervision.feature and w194's whole-suite gate can pass. Reading (b): w194 stays without Retires. The scenario is left in place and fails, and the narrator sees w194's whole-suite gate fail on it, with w194 sent awaiting-answer until another work-item retires it.
  Answer: 2026-10-25: Reading (a): it is under w194's ## Retires now; remove it and its step with features retire (the coordinator under the person's delegation 2026-10-25)

Read (paths in your worktree):
- .shop/work/i33/w194.md
- spec/capabilities/supervision.md
- .shop/work/i33/runs/w194/1-research
- .shop/work/i33/runs/w194/2-plan

Run directory: /tmp/work-run-i33-9u0pon3p/w194-3-plan/.shop/scratch/3-plan
Result file: /tmp/work-run-i33-9u0pon3p/w194-3-plan/.shop/scratch/3-plan/result.json

You start in your worktree, /tmp/work-run-i33-9u0pon3p/w194-3-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
