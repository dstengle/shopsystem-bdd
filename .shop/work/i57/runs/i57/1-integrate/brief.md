# integrate of i57

Initiative: .shop/work/i57/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q31
Accepted lines of the request:
- 1. The bounded context shall have a backlog of ideas and observations, kept in the repository.
- 2. **When** the person gives a session an idea or an observation outside an initiative, the session shall add it to the backlog in the same turn, with its date and the person's words.
- 3. The session-start hook's text shall give no item of the backlog.
- 4. **While** an item of the backlog has had no discovery discussion with the person, the plugin shall draft no request and no proposal from it.
- 5. **When** the person and a session have held a discovery discussion on an item of the backlog, the session shall raise a request from it, naming the item as its source.
- 6. The bounded context shall have a log of temporary rules that the person gives its sessions, kept in the repository.
- 7. **When** the person gives a session a rule outside an initiative, the session shall add it to the log of temporary rules in the same turn, with its date and the person's words.
- 8. The session-start hook's text shall give each rule of the log of temporary rules.
- 9. **When** the person rules that a rule of the log of temporary rules moves to the backlog, the session shall move it from the log to the backlog.
- 10. The session shall keep each rule, idea and observation of the bounded context in the repository.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-consistency#r28, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r177, supervision#r178, supervision#r179, supervision#r180, supervision#r173, supervision#r174, supervision#r175, supervision#r176, supervision#r181, supervision#r182, work-queue#r40, work-queue#r41, spec-integration#r57, requests#r49, supervision#r183, work-queue#r46, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45
Drafts path: /tmp/work-run-i57-z7zn1_jh/i57-1-integrate/.shop/scratch/1-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Base: ba786220582dd893205e255a321e988ef0c26fa7
Worktree: /tmp/work-run-i57-z7zn1_jh/i57-1-integrate
Branch: round/i57-1-integrate

Read (paths in your worktree):
- .shop/work/i57/initiative.md

Run directory: /tmp/work-run-i57-z7zn1_jh/i57-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i57-z7zn1_jh/i57-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i57-z7zn1_jh/i57-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
