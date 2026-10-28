# gate of supervision

Capability-proposal: .shop/work/i52/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: supervision#r188, supervision#r189, supervision#r190
Changes: supervision#r171
Removes: none
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i52/runs/supervision/3-integrate/drafts/round-1/
Base: 51bb24048825d03cf1e81728d51046a41b4c2ce0
Worktree: /tmp/work-run-i52-vjpigzqs/supervision-4-gate
Branch: round/supervision-4-gate
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
- .shop/work/i52/runs/supervision/3-integrate
- .shop/work/i52/runs/supervision/3-integrate/drafts/round-1/

Run directory: /tmp/work-run-i52-vjpigzqs/supervision-4-gate/.shop/scratch/4-gate
Result file: /tmp/work-run-i52-vjpigzqs/supervision-4-gate/.shop/scratch/4-gate/result.json

You start in your worktree, /tmp/work-run-i52-vjpigzqs/supervision-4-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
