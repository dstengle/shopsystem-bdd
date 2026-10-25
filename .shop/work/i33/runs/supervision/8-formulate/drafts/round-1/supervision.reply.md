## Coverage

| id | line | scenario |
|---|---|---|
| r121 | "**When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever its status." | Scenario Outline: a kept branch review whose result gives <outcome> and no question is taken as listing nothing to fix now (DONE, PARTIAL, BLOCKED, NEEDS_CONTEXT) |
| r75 (changed) | "**When** every work-item of an initiative is `green` or `withdrawn` and at least one of them is `green` and its kept branch review lists nothing to fix now, `work run` shall run `measure initiative` on the initiative." | Scenario Outline: an initiative whose work-items are <work-items> and whose kept branch review lists nothing to fix now <measured> |
| r105 (changed) | "**When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`." | Scenario Outline: an initiative whose work-items are <work-items>, its delivery otherwise closed, <set> |
| r120 | "**Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item, the session shall give in its result whether its answer asks for a change or accepts the work-item as it is." | none: returned as a question |

## Questions

- r120: "**Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item, the session shall give in its result whether its answer asks for a change or accepts the work-item as it is."
  - Reading 1: the line binds `work run`. The brief it writes for the answering session asks the session to say in its result whether its answer asks for a change or accepts the work-item as it is. The scenario checks that brief.
  - Reading 2: the line binds the answering session's agent. Only a real session's result shows it. Under the stand-in claude the scenario would be true by its own setup, so it would not belong in this feature.

## Cases no line mentions

- The existing @r75 scenario "a kept branch review that ended PARTIAL, with no question and no finding, does not list nothing to fix now, and no `measure initiative` is run" contradicts r121, which takes such a review as listing nothing to fix now. That scenario needs retiring. The other existing @r75 scenario and the existing @r105 scenario show the old lines and are replaced by the drafts.
- A kept branch review whose result gives no question but whose findings file has findings triaged fix now. r121 takes that review as listing nothing to fix now, and r74 says nothing about it.
- An initiative whose every work-item is withdrawn, after r75 and r105. No line says what `work run` does with it: whether it ends successfully, whether it is ever done, or whether a branch review of it is still started under r27.
- Under a delegation, a session's result that answers a reviewer's question but gives neither "asks for a change" nor "accepts as it is". r118 and r119 make no transition for it, and no line says what follows.

## Drafts

- /tmp/work-run-i33-9vstbbh_/supervision-8-formulate/.shop/scratch/8-formulate/drafts/round-1/supervision/supervision.feature
