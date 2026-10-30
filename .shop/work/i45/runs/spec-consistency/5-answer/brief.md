# answer

Agent: delegation-answerer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts
Base: none
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-consistency-5-answer
Branch: none (a detached checkout)
Question: r11 "checking-spec-consistency shall start only when the person asks for it, never during an integration or a formulation": Reading 1: integration and formulation never start it themselves; a person who asks mid-integration gets a pass. Reading 2: it does not start while an integration or formulation is under way, even when asked.
Delegation: The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's.

Read (paths in your worktree):
Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-consistency-5-answer/.shop/scratch/5-answer
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-consistency-5-answer/.shop/scratch/5-answer/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/spec-consistency-5-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
