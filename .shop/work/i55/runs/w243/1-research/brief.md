# research of w243

Work-item: .shop/work/i55/w243.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: c53a7c25e23bac68cae83b147c9dd66a2e6c6227
Worktree: /tmp/work-run-i55-bbqcq18a/w243-1-research
Branch: none (a detached checkout)
Work-item branch: work/w243
Accepted scenarios:
- features/supervision.feature: a researcher's result that gives an empty file set is taken as the researcher's file set
- features/supervision.feature: a formulate round that formulates nothing because the proposal's answers change lines not in spec/ is followed by a new integrate round for the proposal
- features/supervision.feature: when `work run` ends with <node> awaiting-answer, it exits with an error, printing <node> with its open questions

Read (paths in your worktree):
- .shop/work/i55/w243.md
- spec/capabilities/supervision.md

Run directory: /tmp/work-run-i55-bbqcq18a/w243-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i55-bbqcq18a/w243-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i55-bbqcq18a/w243-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
