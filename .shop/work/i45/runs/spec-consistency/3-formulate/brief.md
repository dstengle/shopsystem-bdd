# formulate of spec-consistency

Capability-proposal: .shop/work/i45/spec-consistency.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: formulate
Where the answers below change lines that are not in spec/, so that you formulate nothing, give in your result `nothing_formulated`, a sentence saying so, and no `questions`: `work run` then starts an integrate round for the proposal.
Base: 10e6a82ef18dc60fb3712e81236e2ea4da33a527
Worktree: /tmp/work-run-i45-7xftq6tl/spec-consistency-3-formulate
Branch: round/spec-consistency-3-formulate
Answers the person gave, each with the question it answers:
- Question: Decision on spec-consistency r5 and r28 (request q26, line 7: a changed line is retired and its replacement given a new id). r5 says: "**Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, ids kept, through one gate pass for the term." It says the opposite of line 7 (ids kept). Readings: A (recommended, drafted): retire r5 (it goes to `retired`) and add r28: "**Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, each changed line retired and its replacement given a new id, through one gate pass for the term." B: leave r5 as it is and add no r28; the spec then contradicts itself, since line 7's rule would hold for every line but the fix mode's. The answer with A also holds for the same decision on spec-integration r13 (retired) and r53 (added), which that proposal's gate asks.
  Answer: 2026-10-28: Decision on r5 and r28: reading A, retire r5 and add r28 (answered by the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i45/spec-consistency.md
- .shop/work/i45/runs/spec-consistency/1-gate
- .shop/work/i45/runs/spec-consistency/2-apply

Run directory: /tmp/work-run-i45-7xftq6tl/spec-consistency-3-formulate/.shop/scratch/3-formulate
Result file: /tmp/work-run-i45-7xftq6tl/spec-consistency-3-formulate/.shop/scratch/3-formulate/result.json

You start in your worktree, /tmp/work-run-i45-7xftq6tl/spec-consistency-3-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
