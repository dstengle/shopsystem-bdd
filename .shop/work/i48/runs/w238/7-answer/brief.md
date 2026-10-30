# answer

Agent: delegation-answerer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts
Base: none
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w238-7-answer
Branch: none (a detached checkout)
Question: Add [r190] to spec/capabilities/supervision.md (via formulating-features) and a scenario/work-item for the glossary-proposal apply-to-integrate route; then r189 can go green. Evidence: assertion len(rounds(repo,'integrate','g1')) == 1 fails; only the apply round for g1 started.
Delegation: The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's.

Read (paths in your worktree):
- spec/capabilities/supervision.md
Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w238-7-answer/.shop/scratch/7-answer
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w238-7-answer/.shop/scratch/7-answer/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w238-7-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
