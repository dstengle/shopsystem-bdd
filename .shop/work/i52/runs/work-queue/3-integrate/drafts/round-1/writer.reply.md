/tmp/work-run-i52-vjpigzqs/work-queue-3-integrate/.shop/scratch/3-integrate/drafts/round-1/spec/capabilities/work-queue.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| removed | work-queue | r23 | **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`. (id added to `retired`) | answer to Q1, reading (b), 2026-10-28; q38 line 3: "When `work withdraw` leaves every work-item of an initiative green or withdrawn, `work` shall leave the initiative's status for `work run` to set once its kept branch review lists nothing to fix now." |
| added | work-queue | r50 | **When** a `work` command's change leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now. | answer to Q1, reading (b); q38 line 3 (quoted above) |
| added | work-queue | r51 | **When** `work` sets an initiative's status, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the time, the initiative, its status before and after, and who set it. | answer to Q2, reading (a); q38 line 4 |

Not added: Q3 (`work start` writing `proposed` is not a transition) and Q4 (no commit line for r51's log line), as answered.

No glossary term added, changed or removed. No decision drafted.

## Questions

Lines and sections the removal of r23 touches; reported, not edited:

1. work-queue Purpose: "it ... makes it `done` when its work and the requests it raised are" contradicts the removal of r23 and r50. With no answer, Purpose stays as it is. If the person agrees, it would read "...it starts an initiative from an `accepted` request and leaves its `done` to `work run`; ...".
2. work-queue Implementation, may change: "r23: a request names the initiative in its `part_of` or its `source`." now points at a retired id. If the person agrees, the line is removed (or moved to supervision's line that sets `done`, if that line uses the same condition).
3. work-queue r31 ("If every work-item of an initiative is `withdrawn`, then `work` shall leave the initiative's status as it is") is now a case r50 already covers. It does not conflict. Should it be (a) kept as it stands, or (b) removed, with r31 added to `retired`?
4. work-queue r51: once r23 is gone, no work-queue line has `work` set an initiative's status (r22 writes `proposed`, which Q3 says is not a transition). So r51 has no trigger in this capability unless another initiative's draft adds one, such as `work withdraw`/`work resolve` of an initiative. Should r51 (a) stay as a standing rule, or (b) be held until a line that sets an initiative's status exists?
5. features/work-queue.feature: the scenarios "a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done" and "retry that makes an initiative's last open work-item green again sets the initiative to done" verify r23. They contradict r50 and need to be retired or rewritten by formulation. Not edited here.

## Cut sentences

None.
