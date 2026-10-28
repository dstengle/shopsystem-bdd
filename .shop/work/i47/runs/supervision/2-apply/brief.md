# apply of supervision

Capability-proposal: .shop/work/i47/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Compare each answer below with the drafts you applied, and give each answer they do not hold in your result's `unheld_answers`, a list of the answers' texts, also when you applied some of the drafts; leave out an answer they hold.
Drafts path: .shop/work/i47/runs/i47/1-integrate/drafts/round-1/
Base: edcfb0c266fb1d7417f5244a620bf7053adf08f7
Worktree: /tmp/work-run-i47-ee1m2t30/supervision-2-apply
Branch: round/supervision-2-apply
Answers the person gave, each with the question it answers:
- Question: supervision, r177 against r4. Lines: added [r177] **While** no work-item accepts a requirement that a scenario names, `work run` shall count a failure of that scenario in the whole-suite run of a work-item's branch as expected. r4 merges a work-item branch only if the whole suite passes "but for the failing scenarios r43 counts as expected"; as drafted, a failure r177 counts as expected still blocks the merge. Reading A (recommended): r177 lets the merge through: change r4 to "[r4] **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r177 count as expected." Reading B: r4 stays.
  Answer: 2026-10-28: Q1, r177 against r4: reading A, r4 changes (retired, new id) so a failure r177 counts as expected does not block the merge (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: supervision, Implementation note for r177. Line: added [r177] (as above). The existing note "r122: the checks are the whole-suite runs of r24 and r43" names the runs; r177 says only "the whole-suite run of a work-item's branch". Reading A (recommended): r177 covers both runs: add the Implementation line "r177: the whole-suite runs are those of r24 and r43; `--whole-suite` marks each such scenario as xfail." Reading B: only r43's run before a merge: "r177: the whole-suite run is r43's, before a merge."
  Answer: 2026-10-28: Q2, the Implementation note for r177: reading A, r177 covers the whole-suite runs of r24 and r43 (answered by the coordinator under the person's delegation, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i47/supervision.md
- .shop/work/i47/runs/supervision/1-gate
- .shop/work/i47/runs/i47/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i47-ee1m2t30/supervision-2-apply/.shop/scratch/2-apply
Result file: /tmp/work-run-i47-ee1m2t30/supervision-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /tmp/work-run-i47-ee1m2t30/supervision-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
