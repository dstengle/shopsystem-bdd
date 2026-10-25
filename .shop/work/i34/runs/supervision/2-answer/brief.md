# answer

Agent: delegation-answerer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: none
Worktree: /tmp/work-run-i34-m7mb7b1k/supervision-2-answer
Branch: none (a detached checkout)
Question: Scope of supervision#r122. The line reads: "[r122] **When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes." Readings: (a) the check is only the whole-suite run before a merge (r43, which r4 uses), so the line would say "runs the whole suite before a merge"; (b) the check is every whole-suite run for a work-item, the run before an implementer starts (r24) as well as the one before a merge (r43), as the line reads now. Recommended: (b), the line as drafted.
Delegation: The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading; where no reading is recommended, choose the one a test can check.

Read (paths in your worktree):
Run directory: /tmp/work-run-i34-m7mb7b1k/supervision-2-answer/.shop/scratch/2-answer
Result file: /tmp/work-run-i34-m7mb7b1k/supervision-2-answer/.shop/scratch/2-answer/result.json

You start in your worktree, /tmp/work-run-i34-m7mb7b1k/supervision-2-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
