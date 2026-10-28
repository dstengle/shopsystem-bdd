# integrate of supervision

Initiative: .shop/work/i42/supervision.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.1/scripts
Kind: integrate
Request: q22
Accepted lines of the request:
- 1. **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
- 2. **When** a round of the kind `apply` ends, `initiative-round` shall give in its result each answer of the capability-proposal that the drafts it applied do not hold.
- 3. **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r80, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r112, supervision#r113, supervision#r114, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, work-queue#r33, supervision#r137, supervision#r138, supervision#r139
Drafts path: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-integrate/.shop/scratch/3-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Ledger: .shop/work/i42/ledger.md
Earlier drafts path (read only): .shop/work/i42/runs/i42/1-integrate/drafts/round-1/
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: 8f90ad3e6acd9159e1317a8c264050c0e646a842
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-integrate
Branch: round/supervision-3-integrate
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
- .shop/work/i42/runs/supervision/2-apply
- .shop/work/i42/ledger.md
- .shop/work/i42/runs/i42/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-integrate/.shop/scratch/3-integrate
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-integrate/.shop/scratch/3-integrate/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-3-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
