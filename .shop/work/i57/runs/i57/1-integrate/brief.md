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
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3@0.29, supervision#r5@0.29, supervision#r16@0.29, supervision#r71@0.29, supervision#r77@0.29, supervision#r80@0.29, supervision#r92@0.29, work-queue#r3@0.29, work-queue#r11@0.29, work-queue#r16@0.29, work-queue#r17@0.29, work-queue#r18@0.29, requests#r1@0.29, requests#r3@0.29, supervision#r99@0.29, supervision#r104@0.29, supervision#r112@0.29, supervision#r113@0.29, supervision#r114@0.29, review#r9@0.29, supervision#r125@0.29, supervision#r126@0.29, supervision#r127@0.29, design-model-check#r120@0.29, design-model-check#r121@0.29, requests#r26@0.29, requests#r27@0.29, requests#r35@0.29, requests#r36@0.29, requests#r37@0.29, requests#r38@0.29, spec-integration#r17@0.29, work-queue#r33@0.29, supervision#r137@0.29, supervision#r138@0.29, supervision#r139@0.29, supervision#r140@0.29, requests#r46@0.29, spec-consistency#r28@0.29, spec-integration#r47@0.29, spec-integration#r48@0.29, spec-integration#r49@0.29, spec-integration#r50@0.29, spec-integration#r51@0.29, spec-integration#r52@0.29, spec-integration#r53@0.29, requests#r47@0.29, requests#r48@0.29, supervision#r177@0.29, supervision#r178@0.29, supervision#r179@0.29, supervision#r180@0.29, supervision#r173@0.29, supervision#r174@0.29, supervision#r175@0.29, supervision#r176@0.29, supervision#r181@0.29, supervision#r182@0.29, work-queue#r40@0.29, work-queue#r41@0.29, spec-integration#r57@0.29, requests#r49@0.29, supervision#r183@0.29, work-queue#r46@0.29, spec-integration#r56@0.29, work-queue#r42@0.29, work-queue#r43@0.29, work-queue#r44@0.29, work-queue#r45@0.29
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
