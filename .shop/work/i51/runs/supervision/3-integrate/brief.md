# integrate of supervision

Initiative: .shop/work/i51/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q37
Accepted lines of the request:
- 1. **When** a question of an initiative mentions the glossary, `work run` shall leave the question for the person, giving it to no session under a delegation.
- 2. **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that does not mention the glossary to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise.
- 3. **When** a round or a worker writes a question on the definition of a term or on a proposed term, the round or the worker shall name the glossary in the question.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-consistency#r28, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r177, supervision#r178, supervision#r179, supervision#r181, supervision#r182, work-queue#r40, work-queue#r41, spec-integration#r57, supervision#r187, work-queue#r48, work-queue#r49, requests#r50, requests#r51, requests#r52, requests#r53, requests#r54, requests#r55, requests#r56, requests#r57, requests#r58, supervision#r184, supervision#r185, supervision#r186, work-queue#r47, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45
Drafts path: /tmp/work-run-i51-wv8x5s99/supervision-3-integrate/.shop/scratch/3-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Ledger: .shop/work/i51/ledger.md
Earlier drafts path (read only): .shop/work/i51/runs/i51/1-integrate/drafts/round-1/
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: 3c43389a5a12ce6f84d8556d2d86945c5fd901aa
Worktree: /tmp/work-run-i51-wv8x5s99/supervision-3-integrate
Branch: round/supervision-3-integrate
Answers the person gave, each with the question it answers:
- Question: Question 1 (r174, r175; replace retired r162, r163): what does "mentions the glossary" mean? r174 (added, replaces r162): **When** a question of an initiative mentions the glossary, `work run` shall leave the question for the person, giving it to no session under a delegation. r175 (added, replaces r163): **Where** the request an initiative fulfils gives a delegation, `work run` shall give each question of the initiative that does not mention the glossary to a session of its own, given the delegation, the files that one question names and nothing else, which answers the question if the delegation covers it and leaves it for the person otherwise. Retired: r162 (names a term of the glossary or a glossary-proposal), r163 (names neither). Readings: (a) [recommended] The question's text names the glossary itself, which r176 makes every question about a term do; lines stand as drafted. (b) The question is about the glossary: it names the glossary, a term of it or a glossary-proposal. r174 would read: "**When** a question of an initiative names the glossary, a term of the glossary or a glossary-proposal, `work run` shall leave the question for the person, giving it to no session under a delegation." and r175 "... that names neither the glossary, a term of the glossary nor a glossary-proposal ..."
  Answer: 2026-10-28: Question 1, mentions the glossary: reading (a), the question's text names the glossary itself; lines as drafted (answered by the person, 2026-10-28)
- Question: Question 2 (r176): who does "a round or a worker" cover? r176 (added): **When** a round or a worker writes a question on the definition of a term or on a proposed term, the round or the worker shall name the glossary in the question. Readings: (a) [recommended] Only rounds and workers `work run` starts (the glossary's worker is a session for one stage of one work-item); as drafted. (b) Also the branch reviewer and answering sessions. r176 would read: "**When** a session that `work run` started writes a question on the definition of a term or on a proposed term, the session shall name the glossary in the question."
  Answer: 2026-10-28: Question 2, r176's sessions: reading (b), every session work run starts, the branch reviewer and answering sessions included (answered by the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i51/supervision.md
- .shop/work/i51/runs/supervision/1-gate
- .shop/work/i51/runs/supervision/2-apply
- .shop/work/i51/ledger.md
- .shop/work/i51/runs/i51/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i51-wv8x5s99/supervision-3-integrate/.shop/scratch/3-integrate
Result file: /tmp/work-run-i51-wv8x5s99/supervision-3-integrate/.shop/scratch/3-integrate/result.json

You start in your worktree, /tmp/work-run-i51-wv8x5s99/supervision-3-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
