# apply of supervision

Capability-proposal: .shop/work/i42/supervision.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.1/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Drafts path: .shop/work/i42/runs/i42/1-integrate/drafts/round-1/
Base: 8f90ad3e6acd9159e1317a8c264050c0e646a842
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply
Branch: round/supervision-2-apply
Answers the person gave, each with the question it answers:
- Question: r150 against r140: an apply that applies nothing also gives the answers its drafts do not hold, so r150 covers r140's case. Line concerned (added): [supervision#r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) retire r140 and keep r150, r140's scenario deprecated for r150 (recommended); (b) keep both.
  Answer: 2026-10-28: r150 against r140: reading (a), retire r140 and keep r150, r140's scenario deprecated for r150 (the person, 2026-10-28: take recommendations).
- Question: r150 against r144-r146: a partial apply still fires 'having applied its drafts' (proposal `approved`, formulate starts beside the new integrate). Line concerned (added): [supervision#r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) meant, no further line; (b) add r151 '**When** an apply round gives an answer its drafts do not hold, `work run` shall start no `formulate` round for the proposal until the new `integrate` round has been applied.' (recommended); (c) (b) plus r152, keeping the proposal's status.
  Answer: 2026-10-28: r150 against r144-r146: reading (b), add r151 'When an apply round gives an answer its drafts do not hold, work run shall start no formulate round for the proposal until the new integrate round has been applied.' (the person, 2026-10-28: take recommendations).
- Question: r149 against r83: a formulate that formulates nothing and gives no question would be set `formulated`. Line concerned (added): [supervision#r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) add r151 '**When** a formulate round formulates nothing because answers change lines not in `spec/`, `work run` shall keep the proposal's status.' (recommended); (b) let r83 apply.
  Answer: 2026-10-28: r149 against r83: reading (a), add a line 'When a formulate round formulates nothing because answers change lines not in spec/, work run shall keep the proposal's status.' (the person, 2026-10-28: take recommendations).
- Question: r149 against r131/r132: a formulate that formulates nothing lacks its output. Line concerned (added): [supervision#r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) add a line that `work run` shall take that case as the round's output, as r147 does for apply (recommended); (b) no line.
  Answer: 2026-10-28: r149 against r131/r132: reading (a), add a line that work run shall take that case as the round's output, as r147 does for apply (the person, 2026-10-28: take recommendations).

Read (paths in your worktree):
- .shop/work/i42/supervision.md
- .shop/work/i42/runs/supervision/1-gate
- .shop/work/i42/runs/i42/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply/.shop/scratch/2-apply
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
