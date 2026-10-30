# answer

Agent: delegation-answerer
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts
Base: none
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-5-answer
Branch: none (a detached checkout)
Question: r212's condition. Line (added): [r212] **If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge. Readings: (a, recommended, as drafted) every failure that would refuse the merge gets one more run; the rerun is how `work run` finds whether it repeats; (b) only failures `work run` can tell in advance are not the work-item's (q41 gives no list): "[r212] **If** a scenario fails in a run that `work run` makes before a merge, for a reason that `work run` takes as not caused by the work-item, **then** `work run` shall run that scenario again once, alone, before it refuses the merge."
Delegation: The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's.

Read (paths in your worktree):
Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-5-answer/.shop/scratch/5-answer
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-5-answer/.shop/scratch/5-answer/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-5-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
