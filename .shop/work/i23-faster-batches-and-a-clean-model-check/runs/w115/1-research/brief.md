# research of w115

Work-item: .shop/work/i23-faster-batches-and-a-clean-model-check/w115.md
Agent: code-scout
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.24.0/scripts
Base: 1ad628182e2dd2eb91d1e0ed6e95ecb34f3bcc63
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w115-1-research
Branch: none (a detached checkout)
Work-item branch: work/w115
Accepted scenarios:
- features/batch-measurement.feature: a <file kind> of a shape measure does not know is refused, naming it
- features/batch-measurement.feature: a transcript line with <line break> inside a JSON string is read as one line
- features/batch-measurement.feature: a time ending in Z in <file> is read as a time in UTC
- features/batch-measurement.feature: a stage whose session.json is empty is given without its session's figures, named as such

Read (paths in your worktree):
- .shop/work/i23-faster-batches-and-a-clean-model-check/w115.md
- spec/capabilities/batch-measurement.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w115-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w115-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w115-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
