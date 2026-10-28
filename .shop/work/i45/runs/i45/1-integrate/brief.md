# integrate of i45

Initiative: .shop/work/i45/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q26
Accepted lines of the request:
- 1. The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines.
- 2. **When** `work request` takes a line that names an implementation detail or a term the glossary does not define, `work request` shall refuse the line, naming the word and why.
- 3. **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers before the gate round starts.
- 4. The glossary shall define each event and each condition that a line's trigger names.
- 5. **When** a gate round finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking.
- 6. **When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading.
- 7. The spec's format rules and the `capability-writer`'s instructions shall say that a changed line is retired and its replacement given a new id.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r80, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140
Drafts path: /tmp/work-run-i45-fukf4k_n/i45-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Base: 10e6a82ef18dc60fb3712e81236e2ea4da33a527
Worktree: /tmp/work-run-i45-fukf4k_n/i45-1-integrate
Branch: round/i45-1-integrate

Read (paths in your worktree):
- .shop/work/i45/initiative.md

Run directory: /tmp/work-run-i45-fukf4k_n/i45-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i45-fukf4k_n/i45-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i45-fukf4k_n/i45-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
