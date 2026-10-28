# gate of supervision

Capability-proposal: .shop/work/i47/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: supervision#r188, supervision#r189, supervision#r190
Changes: none
Removes: supervision#r4
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i47/runs/supervision/3-integrate/drafts/round-1/
Base: edcfb0c266fb1d7417f5244a620bf7053adf08f7
Worktree: /tmp/work-run-i47-ee1m2t30/supervision-4-gate
Branch: round/supervision-4-gate
Answers the person gave, each with the question it answers:
- Question: supervision, r177 against r4. Lines: added [r177] **While** no work-item accepts a requirement that a scenario names, `work run` shall count a failure of that scenario in the whole-suite run of a work-item's branch as expected. r4 merges a work-item branch only if the whole suite passes "but for the failing scenarios r43 counts as expected"; as drafted, a failure r177 counts as expected still blocks the merge. Reading A (recommended): r177 lets the merge through: change r4 to "[r4] **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r177 count as expected." Reading B: r4 stays.
  Answer: 2026-10-28: Q1, r177 against r4: reading A, r4 changes (retired, new id) so a failure r177 counts as expected does not block the merge (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: supervision, Implementation note for r177. Line: added [r177] (as above). The existing note "r122: the checks are the whole-suite runs of r24 and r43" names the runs; r177 says only "the whole-suite run of a work-item's branch". Reading A (recommended): r177 covers both runs: add the Implementation line "r177: the whole-suite runs are those of r24 and r43; `--whole-suite` marks each such scenario as xfail." Reading B: only r43's run before a merge: "r177: the whole-suite run is r43's, before a merge."
  Answer: 2026-10-28: Q2, the Implementation note for r177: reading A, r177 covers the whole-suite runs of r24 and r43 (answered by the coordinator under the person's delegation, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i47/supervision.md
- .shop/work/i47/runs/supervision/1-gate
- .shop/work/i47/runs/supervision/2-apply
- .shop/work/i47/runs/supervision/3-integrate
- .shop/work/i47/runs/supervision/3-integrate/drafts/round-1/

Run directory: /tmp/work-run-i47-ee1m2t30/supervision-4-gate/.shop/scratch/4-gate
Result file: /tmp/work-run-i47-ee1m2t30/supervision-4-gate/.shop/scratch/4-gate/result.json

You start in your worktree, /tmp/work-run-i47-ee1m2t30/supervision-4-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
