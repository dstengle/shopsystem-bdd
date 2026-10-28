# gate of supervision

Capability-proposal: .shop/work/i46/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: supervision#r171, supervision#r172
Changes: none
Removes: supervision#r158, supervision#r160
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i46/runs/supervision/3-integrate/drafts/round-3/
Base: 134745663cfa0a109b8564370c2464ef9ee9a7d5
Worktree: /tmp/work-run-i46-rhbgokrg/supervision-4-gate
Branch: round/supervision-4-gate
Answers the person gave, each with the question it answers:
- Question: r158: "When a change list that `work run` reads names the glossary, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary." Reading A: only an integrate round's change list gives a glossary-proposal, as in r159. Reading B: every change list work run reads gives one, an apply round's included (r145); then an apply round applying a glossary-proposal's drafts would give a new drafted glossary-proposal, against r166.
  Answer: 2026-10-28: r158: reading A, only an integrate round's change list gives a glossary-proposal, as in r159 (the person, 2026-10-28)
- Question: r160: "While a glossary-proposal is `awaiting-answer`, `work run` shall start no round of the kind `apply` for it." Reading A: no apply round while it is awaiting-answer and some question has no answer; once all are answered r165 starts the apply round. Reading B: no apply round while the status is awaiting-answer whatever the answers; but r169 sets that status at gate end and an answered proposal still has it, so r165 could never hold.
  Answer: 2026-10-28: r160: reading A, no apply round while the glossary-proposal is awaiting-answer and some question has no answer; once all are answered r165 starts the apply round (the person, 2026-10-28) The drafts of this proposal are in .shop/work/i46/runs/supervision/3-integrate/drafts/round-3/.

Read (paths in your worktree):
- .shop/work/i46/supervision.md
- .shop/work/i46/runs/supervision/1-formulate
- .shop/work/i46/runs/supervision/2-formulate
- .shop/work/i46/runs/supervision/3-integrate
- .shop/work/i46/runs/supervision/3-integrate/drafts/round-3/

Run directory: /tmp/work-run-i46-rhbgokrg/supervision-4-gate/.shop/scratch/4-gate
Result file: /tmp/work-run-i46-rhbgokrg/supervision-4-gate/.shop/scratch/4-gate/result.json

You start in your worktree, /tmp/work-run-i46-rhbgokrg/supervision-4-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
