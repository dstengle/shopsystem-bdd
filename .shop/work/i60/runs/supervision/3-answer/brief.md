# answer

Agent: delegation-answerer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: none
Worktree: /tmp/work-run-i60-sk55gsmk/supervision-3-answer
Branch: none (a detached checkout)
Question: Are the lines of supervision approved as drafted? Readings: approve supervision as drafted (recommended), or change its lines.
Delegation: The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's.

Read (paths in your worktree):
Run directory: /tmp/work-run-i60-sk55gsmk/supervision-3-answer/.shop/scratch/3-answer
Result file: /tmp/work-run-i60-sk55gsmk/supervision-3-answer/.shop/scratch/3-answer/result.json

You start in your worktree, /tmp/work-run-i60-sk55gsmk/supervision-3-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
