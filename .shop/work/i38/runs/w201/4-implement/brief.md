# implement of w201

Work-item: .shop/work/i38/w201.md
Agent: bdd-implementer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Base: 50a40103b15d1b9455b9d609ddb1a96cf799a11d
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w201
Branch: work/w201
Work-item branch: work/w201
Suite record: Suite: 946 passed, 1 failed at 402fe8f4 in 28 s; failing: tests/scenarios/test_supervision.py::test_a_stages_result_giving_output_is_taken_as_its_stages_output[formulate round-spec/capabilities/steady.md is a guarantees capability, and i1's capability-proposal p1 is awaiting-answer, its adds naming steady#r4, its ## Questions section with "Is a shelf one place or a list?", given by its formulate round, and its Answers section with "One place."-no scenario and no question-`work run i1`-p1's transition to formulated was made once the formulate round had ended]
Answers the person gave, each with the question it answers:
- Question: Please have a feature-formulator add a row to the r132 outline (or an @r83 scenario): proposal p1 awaiting-answer with answered formulate questions, its adds naming a requirement of a capability with `group: guarantees`; the formulate round gives no scenario and no question; Then p1's transition to formulated was made once the round ended. Evidence: grep guarantees features/supervision.feature shows only r56/r64/r65 scenarios; plan section 1 says nothing is red today.
  Answer: 2026-10-26: Done: features/supervision.feature's r132 outline has a formulate round row for capability-proposal p1 whose adds name steady#r4 of a guarantees capability (spec/capabilities/steady.md), the round giving no scenario and no question, p1 formulated once the round ended (design-decision/workflow-capabilities-are-guarantees). main is merged into work/w201 at 402fe8f4. Make the row green red-green (q16's delegation).

Read (paths in your worktree):
- .shop/work/i38/w201.md
- spec/capabilities/supervision.md
- .shop/work/i38/runs/w201/1-research
- .shop/work/i38/runs/w201/2-plan
- .shop/work/i38/runs/w201/3-implement

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w201/.shop/scratch/4-implement
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w201/.shop/scratch/4-implement/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w201: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
