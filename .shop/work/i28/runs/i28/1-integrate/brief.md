# integrate of i28

Initiative: .shop/work/i28/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q6
Accepted lines of the request:
- 1. **When** `work answer <initiative>/<name> <answer>` is run, `work` shall answer the work-item or capability-proposal `<name>` of that initiative.
- 2. **When** `work run` starts a round of the kind `integrate`, `work run` shall give the round every requirement id that the kept drafts of another initiative, not yet applied, add.
- 3. **When** a request of which this context is the upstream is `accepted` and no initiative fulfils it, `work run` shall start its initiative with `work start`.
- 4. **When** `work run` starts a round of the kind `gate` for a capability-proposal, `work run` shall ask the round only for the questions on the lines and terms the proposal adds, changes or removes.
Drafts path: /tmp/work-run-i28-7r_j31qx/i28-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 4b7dca6c200ffc64be3fe1887f1d08a62b311332
Worktree: /tmp/work-run-i28-7r_j31qx/i28-1-integrate
Branch: round/i28-1-integrate

Read (paths in your worktree):
- .shop/work/i28/initiative.md

Run directory: /tmp/work-run-i28-7r_j31qx/i28-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i28-7r_j31qx/i28-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i28-7r_j31qx/i28-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
