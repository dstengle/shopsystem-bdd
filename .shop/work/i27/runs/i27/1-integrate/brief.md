# integrate of i27

Initiative: .shop/work/i27/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q4
Accepted lines of the request:
- 1. **When** a round of the kind `integrate` that `work run` started ends, `work run` shall keep the round's drafts on the initiative branch.
- 2. **When** a round of the kind `integrate` that `work run` started ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names, with the requirement ids and terms it adds, changes and removes on that capability.
- 3. **When** an initiative is `started` and has neither a capability-proposal nor a work-item, `work run` shall start a round of the kind `integrate` given the accepted lines of the request it fulfils.
- 4. **When** an initiative has no work-item, `work run` shall start no branch review of it.
- 5. `work run` shall start the rounds of the kind `integrate`, `apply` and `formulate` of different initiatives one at a time.
- 6. **When** `work start` writes an initiative, `work` shall commit the initiative on the current branch.
- 7. **Where** `--delegation <text>` is given to `work request`, `work` shall write the delegation in the request.
Base: 3cbd0c528b0bd62d10ca4b2453f47921f76c1c6e
Worktree: /tmp/work-run-i27-15a81p5x/i27-1-integrate
Branch: round/i27-1-integrate

Read (paths in your worktree):
- .shop/work/i27/initiative.md

Run directory: /tmp/work-run-i27-15a81p5x/i27-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i27-15a81p5x/i27-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i27-15a81p5x/i27-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
