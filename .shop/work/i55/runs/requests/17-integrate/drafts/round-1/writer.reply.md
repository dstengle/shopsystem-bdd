/tmp/work-run-i55-kf283p9t/requests-17-integrate/.shop/scratch/17-integrate/drafts/round-1/spec/capabilities/work-queue.md

## Change list

| change | capability | id | line | from |
|---|---|---|---|---|
| removed | work-queue | r23 | **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`. | answer (2026-10-29, under the delegation of 2026-10-27): "retire work-queue r23 and add, in its place, a line worded: ..." |
| added | work-queue | r62 | **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`. | answer (2026-10-29, under the delegation of 2026-10-27): "retire work-queue r23 and add, in its place, a line worded: \"**When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.\"" |

Id: r62 is one above the highest id work-queue uses (lines up to r61, `retired` up to r35) and above r58, which other drafts add.

Placement: r62 stands where r23 stood, after r25.

Implementation line changed (no Behaviour change): "r23: a request names the initiative in its `part_of` or its `source`." now reads "r62: a request names the initiative in its `part_of` or its `source`."

New `retired:` list: [r2, r3, r11, r16, r17, r18, r33, r34, r35, r23]

Glossary: no change. Decisions: none.

## Questions
None.

## Cut sentences
None.
