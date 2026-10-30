# answer

Agent: delegation-answerer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts
Base: none
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-consistency-4-answer
Branch: none (a detached checkout)
Question: r9 "...when a step is complete, tell the person what model check finds before the next step": Reading 1: a step is each single fix (each term's gate pass, reworded scenario, question, drift finding). Reading 2: a step is each stage of fix mode (terms, rewording, questions, other drift).
Delegation: The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's.

Read (paths in your worktree):
Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-consistency-4-answer/.shop/scratch/4-answer
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-consistency-4-answer/.shop/scratch/4-answer/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/spec-consistency-4-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
