# integrate of supervision

Initiative: .shop/work/i52/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q38
Accepted lines of the request:
- 1. **When** a round of the kind `integrate` gives terms for an initiative that already has a glossary-proposal, `work run` shall add them to that glossary-proposal, keeping its status, questions and answers.
- 2. **When** a question of an initiative is left for the person, `work run` shall start no further session under the delegation for that initiative's questions until the person has answered.
- 3. **When** `work withdraw` leaves every work-item of an initiative green or withdrawn, `work` shall leave the initiative's status for `work run` to set once its kept branch review lists nothing to fix now.
- 4. **When** `work` sets an initiative's status, `work` shall log the move in the initiative's log.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-consistency#r28, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r177, supervision#r178, supervision#r179, supervision#r174, supervision#r175, supervision#r176, spec-integration#r57, supervision#r187, work-queue#r48, work-queue#r49, requests#r50, requests#r51, requests#r52, requests#r53, requests#r54, requests#r55, requests#r56, requests#r57, requests#r58, supervision#r184, supervision#r185, supervision#r186, work-queue#r47, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45
Drafts path: /tmp/work-run-i52-vjpigzqs/supervision-3-integrate/.shop/scratch/3-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Ledger: .shop/work/i52/ledger.md
Earlier drafts path (read only): .shop/work/i52/runs/i52/1-integrate/drafts/round-1/
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: 51bb24048825d03cf1e81728d51046a41b4c2ce0
Worktree: /tmp/work-run-i52-vjpigzqs/supervision-3-integrate
Branch: round/supervision-3-integrate
Answers the person gave, each with the question it answers:
- Question: supervision r181 (added): **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary and the initiative has a glossary-proposal, `work run` shall add the terms the change list adds, changes and removes in the glossary to that glossary-proposal, keeping its status, its questions and its answers. Which statuses of the glossary-proposal does it apply to? (a) Any, as drafted: an `approved` proposal keeps its status, so added terms skip the gate. (b) Only one that is neither `approved` nor `withdrawn`: r181 gets 'and the initiative has a glossary-proposal that is neither `approved` nor `withdrawn`', plus a line such as '**When** ... the initiative's glossary-proposal is `approved`, `work run` shall add the terms to it and set it `drafted`, keeping its questions and answers.' Recommended: (b).
  Answer: 2026-10-28: Q3, r182 'until the person has answered': reading (a), that question only, as drafted (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: supervision r181 (added), same line: when the round gives a term the glossary-proposal already lists, what happens? (a) The new entry replaces the earlier one: the line gets '...a term the proposal already lists replacing its entry...'. (b) The line is silent, as drafted. Recommended: (a), so the proposal holds the round's latest wording.
  Answer: 2026-10-28: Q4, r182 with r163 after the answer: reading (a), r163 resumes for the remaining questions (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: supervision r182 (added): **While** a question of an initiative is left for the person and has no answer, `work run` shall start no further session under the delegation for that initiative's questions. What does 'until the person has answered' mean? (a) That question only, as drafted. (b) Every question of the initiative: '**While** a question of the initiative has no answer and one of its questions is left for the person, ...'. Recommended: (a), the request names that question.
  Answer: 2026-10-28: Q5, r182 across runs: reading (a), yes, it is a state on the initiative (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: supervision r182 (added) with r163: once the person has answered the question left for them, what happens to the later questions? (a) r163 resumes for the remaining questions, no new line, as drafted. (b) Every later question is left for the person: new line '**When** a question of an initiative has been left for the person, `work run` shall leave every later question of that initiative for the person.' Recommended: (a).
  Answer: 2026-10-28: Q1, r181's statuses: reading (b), only a glossary-proposal neither approved nor withdrawn; an approved one gets the terms and is set drafted, keeping its questions and answers (answered by the person, 2026-10-28)
- Question: supervision r182 (added): does a question left for the person in an earlier delivery hold back sessions in a later `work run`? (a) Yes, it is a state on the initiative, as drafted. (b) No, only within one delivery: '**While** a delivery has left a question of an initiative for the person and ...'. Recommended: (a), since the question stays unanswered across runs.
  Answer: 2026-10-28: Q2, r181 and a term already listed: reading (a), the new entry replaces the earlier one (answered by the person, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i52/supervision.md
- .shop/work/i52/runs/supervision/1-gate
- .shop/work/i52/runs/supervision/2-apply
- .shop/work/i52/ledger.md
- .shop/work/i52/runs/i52/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i52-vjpigzqs/supervision-3-integrate/.shop/scratch/3-integrate
Result file: /tmp/work-run-i52-vjpigzqs/supervision-3-integrate/.shop/scratch/3-integrate/result.json

You start in your worktree, /tmp/work-run-i52-vjpigzqs/supervision-3-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
