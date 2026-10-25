## Coverage

| id | line | scenario |
|---|---|---|
| r117 | "**When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted." | when the gate round `work run` started for a capability-proposal gives no question, one question asking for the approval of the proposal's lines as drafted is written under its ## Questions |
| r110 | "**When** a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before `work run` exits." | when the work-item drafted for a kept branch review's findings turns green, the next branch review of the initiative is started before `work run` exits |
| r19 | "**When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 80 turns." | a researcher is given the work-item's file set and accepted scenarios, and a limit of 80 turns (replaces the existing @r19 scenario; only the title and the last Then change, 40 to 80) |

## Questions

None.

## Cases no line mentions

- r110 when another work-item of the initiative is not yet `green` or `withdrawn` as the findings' work-item turns `green`: r110 says to start the next branch review then, but r27 starts one only once every work-item is `green` or `withdrawn`. No line says which wins. The r110 scenario has every other work-item green or withdrawn, so it does not depend on the answer.
- r110 when the findings' work-item stops at `awaiting-answer` or `failed` and never turns `green`: no line says whether `work run` reviews before it exits.
- r110 when the next branch review also lists findings to fix now: no line bounds how many review and fix cycles one delivery runs.
- r117 when the gate round ends at its turn limit or in an error with no question: r86 to r88 cover that case, and r117 does not say which applies.
- r117 when the gate round's questions all concern lines the proposal does not add, change or remove (r104): no line says whether those count as "no question".

## Drafts

- /tmp/work-run-i30-chbawhjx/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/supervision.feature
