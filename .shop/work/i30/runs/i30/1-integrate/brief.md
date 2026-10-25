# integrate of i30

Initiative: .shop/work/i30/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q7
Accepted lines of the request:
- 1. **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted.
- 2. **When** a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before it ends.
- 3. **When** `work run` starts a researcher, `work run` shall give the researcher a limit of 80 turns.
- 4. **When** `formulating-features` runs an old scenario alone, `formulating-features` shall run it with `python3 -m pytest`.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r99, supervision#r105, supervision#r106, supervision#r107, supervision#r108
Drafts path: /tmp/work-run-i30-o1gqd7vm/i30-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 4fbc25cd32843edb441abb8b04189f38edde1105
Worktree: /tmp/work-run-i30-o1gqd7vm/i30-1-integrate
Branch: round/i30-1-integrate

Read (paths in your worktree):
- .shop/work/i30/initiative.md

Run directory: /tmp/work-run-i30-o1gqd7vm/i30-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i30-o1gqd7vm/i30-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i30-o1gqd7vm/i30-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
