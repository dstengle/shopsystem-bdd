# Gate, round 1, i52 (request q38)

## supervision

Added, changed, removed Behaviour lines:

- [r171] CHANGED. Now: **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary and the initiative has no glossary-proposal, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary.
  Was: **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary.
- [r181] ADDED. **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary and the initiative has a glossary-proposal, `work run` shall add the terms the change list adds, changes and removes in the glossary to that glossary-proposal, keeping its status, its questions and its answers. (q38 line 1)
- [r182] ADDED. **While** a question of an initiative is left for the person and has no answer, `work run` shall start no further session under the delegation for that initiative's questions. (q38 line 2)

## work-queue

- [r23] CHANGED. Now: **When** a `work` command other than `work withdraw` makes it true by its change that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
  Was: **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
- [r40] ADDED. **When** `work withdraw` leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now. (q38 line 3)
- [r41] ADDED. **When** `work` sets an initiative's status, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the initiative and its status before and after the transition. (q38 line 4)

(Ids: work-queue already uses r34 to r39, so the added lines are r40 and r41.)

## Glossary

No term added, changed or removed. No decision drafted.

## Questions

1. work-queue r23 and r40: should other `work` commands than `work withdraw` (`work answer`, `work resolve`, a delivering command) also leave `done` to `work run`? (a) Only `work withdraw`, as drafted. (b) Every `work` command: r23 removed (id retired) and r40 reads "**When** a `work` command's change leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now." Writer recommends (b); the request names only `work withdraw`.
2. work-queue r41: should the logged line also hold the time and who set the status, as r5's does? (a) Yes: "...with the time, the initiative, its status before and after, and who set it." (b) Only the initiative and the status before and after, as drafted.
3. work-queue r41: does `work start` writing a `proposed` initiative count as setting its status? (a) Yes, a further line: "**When** `work start` writes an initiative, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the initiative and its status `proposed`." (b) No, as drafted.
4. supervision: should `work run`'s own settings of an initiative's status (r84, r105, r161) also be logged in `log.jsonl`? (a) Yes, a new line r183: "**When** `work run` sets an initiative's status, `work run` shall append a line to `.shop/work/<initiative>/log.jsonl` with the initiative and its status before and after the transition." (b) No, as drafted.
5. work-queue r9: should the `log.jsonl` line r41 writes be committed with the initiative's file? (a) Yes, r9 changed or a new line: "**When** `work` sets an initiative's status, `work` shall commit on the current branch the initiative's file and the `log.jsonl` line it wrote." (b) No line, as drafted.
6. supervision r181: which statuses of the glossary-proposal does it apply to? (a) Any, as drafted (an `approved` proposal would keep its status, so added terms skip the gate). (b) Only `drafted` or `awaiting-answer`: r181 gets "and the initiative has a glossary-proposal that is neither `approved` nor `withdrawn`", plus a line such as "**When** ... the initiative's glossary-proposal is `approved`, `work run` shall add the terms to it and set it `drafted`, keeping its questions and answers." Recommended: (b).
7. supervision r181: a term the proposal already lists, given again by the round: (a) replaces the earlier entry ("...a term the proposal already lists replacing its entry..."), (b) silent, as drafted.
8. supervision r182: "until the person has answered" means (a) that question, as drafted, or (b) every question of the initiative: "**While** a question of the initiative has no answer and one of its questions is left for the person, ...".
9. supervision r182 and r163: once the person has answered, (a) r163 resumes for the remaining questions, no new line, or (b) every later question is left for the person: "**When** a question of an initiative has been left for the person, `work run` shall leave every later question of that initiative for the person."
10. supervision r182: does a question left for the person in an earlier delivery hold back sessions in a later `work run`? (a) Yes, a state on the initiative, as drafted. (b) No, only within one delivery: "**While** a delivery has left a question of an initiative for the person and ...".
