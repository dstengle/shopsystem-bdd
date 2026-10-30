# answer

Agent: delegation-answerer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts
Base: none
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-answer
Branch: none (a detached checkout)
Question: supervision r213 vs r171. r213 (added): "**If** a round of the kind `integrate` ends with a change list that names the glossary and adds, changes and removes no term, **then** `work run` shall write no glossary-proposal." r171 (in spec): "**When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary." They conflict for a change list naming the glossary with no term. Readings: (a, recommended) narrow r171 to "...names the glossary and adds, changes or removes a term...", so r213 stays a plain rule; (b) keep r171 as is and r213 an exception to it.
Delegation: The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's.

Read (paths in your worktree):
Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-answer/.shop/scratch/2-answer
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-answer/.shop/scratch/2-answer/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
