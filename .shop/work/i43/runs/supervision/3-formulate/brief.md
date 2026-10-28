# formulate of supervision

Capability-proposal: .shop/work/i43/supervision.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.1/scripts
Kind: formulate
Base: ebbf1beaaa1fb5e4e3d29ffde673a5999a2cbd22
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-formulate
Branch: round/supervision-3-formulate
Answers the person gave, each with the question it answers:
- Question: supervision#r155: "**When** `work run` starts a branch review, `work run` shall give the branch reviewer each run r154 names with its command, how it exited and its output, naming the commit they ran at." How should a run's exit be worded? Reading A (recommended, drafted): keep "how it exited" and add the Implementation line "r155: how a run exited is given as its exit code." Reading B: put it in the line: "each run r154 names with its command, exit code and output, naming the commit they ran at."
  Answer: 2026-10-28: supervision#r155: Reading A, keep 'how it exited' and add the Implementation line 'r155: how a run exited is given as its exit code.' (answered by the coordinator under the person's delegation of 2026-10-28).

Read (paths in your worktree):
- .shop/work/i43/supervision.md
- .shop/work/i43/runs/supervision/1-gate
- .shop/work/i43/runs/supervision/2-apply

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-formulate/.shop/scratch/3-formulate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-formulate/.shop/scratch/3-formulate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
