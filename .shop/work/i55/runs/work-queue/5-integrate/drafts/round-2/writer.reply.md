/tmp/work-run-i55-mwcb2_hn/work-queue-5-integrate/.shop/scratch/5-integrate/drafts/round-2/spec/capabilities/work-queue.md
/tmp/work-run-i55-mwcb2_hn/work-queue-5-integrate/.shop/scratch/5-integrate/drafts/round-2/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| removed | work-queue | r23 | [r23] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`. | "(1) Reading (a): retire work-queue r23 for this line" (answer of 2026-10-29, under the delegation of 2026-10-27) |
| added | work-queue | r59 | [r59] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`. | "(1) Reading (a): retire work-queue r23 for this line: \"[r48] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.\"" (numbered r59: ids up to work-queue#r58 are drafted elsewhere) |
| removed | supervision | r105 | [r105] **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`. | "AND retire supervision r105 for the same condition" (answer of 2026-10-29) |
| added | supervision | r213 | [r213] **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose every capability-proposal is `formulated` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`. | "AND retire supervision r105 for the same condition (the same line as r105 with \"whose every capability-proposal is `formulated` or `withdrawn`\" added after \"whose every work-item is `green` or `withdrawn`\")." (numbered r213: ids up to supervision#r212 are drafted elsewhere) |

Unchanged by decision: work-queue r47 stays word for word ("(2) Reading (a): work-queue r47 (already in spec/) stays word for word; do not touch it.").

Other changes in the drafts: the work-queue Implementation line "r23: a request names the initiative in its `part_of` or its `source`." now names r59. Both frontmatters drafted whole, with r23 (work-queue) and r105 (supervision) added to `retired`. No glossary change, no decision file.

## Questions

None.

## Cut sentences

None.
