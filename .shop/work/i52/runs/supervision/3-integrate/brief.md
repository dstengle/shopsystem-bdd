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
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3@0.29, supervision#r5@0.29, supervision#r16@0.29, supervision#r71@0.29, supervision#r77@0.29, supervision#r80@0.29, supervision#r92@0.29, supervision#r93@0.29, work-queue#r3@0.29, work-queue#r11@0.29, work-queue#r16@0.29, work-queue#r17@0.29, work-queue#r18@0.29, requests#r1@0.29, requests#r3@0.29, supervision#r99@0.29, supervision#r104@0.29, supervision#r112@0.29, supervision#r113@0.29, supervision#r114@0.29, review#r9@0.29, supervision#r125@0.29, supervision#r126@0.29, supervision#r127@0.29, design-model-check#r120@0.29, design-model-check#r121@0.29, requests#r26@0.29, requests#r27@0.29, requests#r35@0.29, requests#r36@0.29, requests#r37@0.29, requests#r38@0.29, spec-integration#r17@0.29, work-queue#r33@0.29, supervision#r137@0.29, supervision#r138@0.29, supervision#r139@0.29, supervision#r140@0.29, requests#r46@0.29, spec-consistency#r28@0.29, spec-integration#r47@0.29, spec-integration#r48@0.29, spec-integration#r49@0.29, spec-integration#r50@0.29, spec-integration#r51@0.29, spec-integration#r52@0.29, spec-integration#r53@0.29, requests#r47@0.29, requests#r48@0.29, supervision#r177@0.29, supervision#r178@0.29, supervision#r179@0.29, supervision#r174@0.29, supervision#r175@0.29, supervision#r176@0.29, spec-integration#r57@0.29, supervision#r187@0.29, work-queue#r48@0.29, work-queue#r49@0.29, requests#r50@0.29, requests#r51@0.29, requests#r52@0.29, requests#r53@0.29, requests#r54@0.29, requests#r55@0.29, requests#r56@0.29, requests#r57@0.29, requests#r58@0.29, supervision#r184@0.29, supervision#r185@0.29, supervision#r186@0.29, work-queue#r47@0.29, requests#r49@0.29, supervision#r183@0.29, work-queue#r46@0.29, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35@0.29, migration-tools#r36@0.29, spec-integration#r56@0.29, work-queue#r42@0.29, work-queue#r43@0.29, work-queue#r44@0.29, work-queue#r45@0.29
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
