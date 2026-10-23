# research of w112

Work-item: .shop/work/i23-faster-batches-and-a-clean-model-check/w112.md
Agent: code-scout
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.24.0/scripts
Base: 1ad628182e2dd2eb91d1e0ed6e95ecb34f3bcc63
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w112-1-research
Branch: none (a detached checkout)
Work-item branch: work/w112
Accepted scenarios:
- features/design-model-check.feature: a bounded context with no job gets no unserved-capability warning
- features/design-model-check.feature: a malformed work directory or work file is a file problem
- features/design-model-check.feature: a work-item accepting a requirement no scenario names is a file problem
- features/design-model-check.feature: a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem
- features/design-model-check.feature: a green work-item accepting a retired id is no file problem
- features/design-model-check.feature: a work-item with no accepts and no check is v_w4, unless it is withdrawn
- features/design-model-check.feature: a work-item accepting a requirement no scenario names yet, with no check, is not v_w4

Read (paths in your worktree):
- .shop/work/i23-faster-batches-and-a-clean-model-check/w112.md
- spec/capabilities/design-model-check.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w112-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w112-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w112-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
