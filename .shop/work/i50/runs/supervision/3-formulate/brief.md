# formulate of supervision

Capability-proposal: .shop/work/i50/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: formulate
Where the answers below change lines that are not in spec/, so that you formulate nothing, give in your result `nothing_formulated`, a sentence saying so, and no `questions`: `work run` then starts an integrate round for the proposal.
Base: 2c461ed7dd4de768f3bb16ce4a54e866773b4d2d
Worktree: /tmp/work-run-i50-dmmrs8mf/supervision-3-formulate
Branch: round/supervision-3-formulate
Answers the person gave, each with the question it answers:
- Question: supervision r173 (added): "**When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write one question asking the person to approve the terms the proposal adds, changes and removes." (from q36 line 1). The request does not say where the question is written. r117 (the capability-proposal counterpart) writes it under the proposal's `## Questions`; no line says where a glossary-proposal gate's questions go (r85 covers capability-proposals only; r129 covers a result that gives questions). Reading a (recommended): r173 as drafted. Reading b: r173 reads "**When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write under the proposal's `## Questions` one question asking the person to approve the terms the proposal adds, changes and removes."
  Answer: 2026-10-28: Q1, r173's question: reading (a), r173 as drafted (answered by the person, 2026-10-28)
- Question: supervision r173 against r131/r132: r132 takes "a gate round's questions" as a gate round's output, so a gate round with no question gives neither question nor output, and r131 would write a question naming the missing output as well as r173 (r117 has the same tension). Reading a (recommended): no change; r131 and r173 both apply. Reading b: r132's last item becomes "a gate round's questions, or none" (a changed line with a new id; r132 retired).
  Answer: 2026-10-28: Q2, r173 against r131/r132: reading (a), no change; r131 and r173 both apply (answered by the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i50/supervision.md
- .shop/work/i50/runs/supervision/1-gate
- .shop/work/i50/runs/supervision/2-apply

Run directory: /tmp/work-run-i50-dmmrs8mf/supervision-3-formulate/.shop/scratch/3-formulate
Result file: /tmp/work-run-i50-dmmrs8mf/supervision-3-formulate/.shop/scratch/3-formulate/result.json

You start in your worktree, /tmp/work-run-i50-dmmrs8mf/supervision-3-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
