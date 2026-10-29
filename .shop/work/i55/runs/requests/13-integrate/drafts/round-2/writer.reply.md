/tmp/work-run-i55-mwcb2_hn/requests-13-integrate/.shop/scratch/13-integrate/drafts/round-2/spec/capabilities/requests.md
/tmp/work-run-i55-mwcb2_hn/requests-13-integrate/.shop/scratch/13-integrate/drafts/round-2/spec/capabilities/supervision.md
/tmp/work-run-i55-mwcb2_hn/requests-13-integrate/.shop/scratch/13-integrate/drafts/round-2/spec/capabilities/work-queue.md

## Change list

| change | capability | id | line | from |
|---|---|---|---|---|
| removed | requests | r14 | **When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names. | answer 1: "Retire r14 and add r59 as worded" |
| added | requests | r64 | **When** `work list` is run, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names. | answer 1: "Retire r14 and add r59 as worded" |
| removed | supervision | r149 | **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. | answer 2: r149 retired; its duplicate r186 stays |
| removed | supervision | r9 | **When** no work-item can make a transition, every work-item is `green` or `withdrawn` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status. | answer 3: "retire r32 and r9 and add r187 as worded" |
| removed | supervision | r32 | **When** no work-item can make a transition and a work-item is `awaiting-answer`, `work run` shall exit with an error, printing each work-item's status and each open question. | answer 3: "retire r32 and r9 and add r187 as worded" |
| added | supervision | r212 | **When** no node of the initiative can make a transition, every work-item is `green` or `withdrawn`, no capability-proposal is `awaiting-answer` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status. | answer 3: "retire r32 and r9 and add r187 as worded" |
| removed | supervision | r105 | **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`. | answer 5: r105 retired |
| added | supervision | r213 | **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose every capability-proposal is `formulated` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`. | answer 5: "the same condition as in r105 with one more condition, after \"whose every work-item is `green` or `withdrawn`\": \"whose every capability-proposal is `formulated` or `withdrawn`,\"" |
| removed | work-queue | r23 | **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`. | answer 4: work-queue r23 is retired |
| added | work-queue | r59 | **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`. | answer 4: "Add under work-queue: \"**When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and ...\"" |

Placement: each added line stands where the line it replaces stood (requests r64 at the end of Behaviour; supervision r212 where r9 was, r213 where r105 was; work-queue r59 where r23 was).

Implementation lines changed (no Behaviour change): work-queue "r23: a request names the initiative in its `part_of` or its `source`." becomes "r59: a request names the initiative in its `part_of` or its `source`." No Implementation line of requests cites r14, and none of supervision cites r149, r9, r32 or r105.

New `retired:` lists:
- requests: [r6, r1, r3, r13, r34, r39, r41, r43, r14]
- supervision: [r3, r5, r16, r112, r113, r80, r114, r71, r140, r92, r77, r104, r158, r160, r93, r162, r163, r149, r32, r9, r105]
- work-queue: [r2, r3, r11, r16, r17, r18, r33, r23]

Glossary: no change. Decisions: none.

## Questions
None.

## Cut sentences
None.
