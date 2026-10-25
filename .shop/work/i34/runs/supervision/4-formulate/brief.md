# formulate of supervision

Capability-proposal: .shop/work/i34/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: formulate
Base: c7f6d2f71b0d2438e60d21651997f4e47262a3a7
Worktree: /tmp/work-run-i34-m7mb7b1k/supervision-4-formulate
Branch: round/supervision-4-formulate
Answers the person gave, each with the question it answers:
- Question: Scope of supervision#r122. The line reads: "[r122] **When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes." Readings: (a) the check is only the whole-suite run before a merge (r43, which r4 uses), so the line would say "runs the whole suite before a merge"; (b) the check is every whole-suite run for a work-item, the run before an implementer starts (r24) as well as the one before a merge (r43), as the line reads now. Recommended: (b), the line as drafted.
  Answer: 2026-10-25: (b) every whole-suite run for a work-item, both the run before an implementer starts (r24) and the one before a merge (r43), keeping supervision#r122 as drafted; answered under the person's delegation of 2026-10-25 (recommended reading). by: work run, under the delegation "The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading; where no reading is recommended, choose the one a test can check."

Read (paths in your worktree):
- .shop/work/i34/supervision.md
- .shop/work/i34/runs/supervision/1-gate
- .shop/work/i34/runs/supervision/2-answer
- .shop/work/i34/runs/supervision/3-apply

Run directory: /tmp/work-run-i34-m7mb7b1k/supervision-4-formulate/.shop/scratch/4-formulate
Result file: /tmp/work-run-i34-m7mb7b1k/supervision-4-formulate/.shop/scratch/4-formulate/result.json

You start in your worktree, /tmp/work-run-i34-m7mb7b1k/supervision-4-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
