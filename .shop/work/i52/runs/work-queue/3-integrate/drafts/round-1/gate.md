# Gate, round 3, i52 (request q38), work-queue

## work-queue

Added, changed, removed Behaviour lines:

- [r23] REMOVED (id retired; answer Q1 (b) of 2026-10-28). It was: **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
- [r50] ADDED. **When** a `work` command's change leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now. (q38 line 3; answer Q1 (b))
- [r51] ADDED. **When** `work` sets an initiative's status, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the time, the initiative, its status before and after, and who set it. (q38 line 4; answer Q2 (a))

Not added, as answered: a line for `work start` writing `proposed` (Q3), a line committing r51's log line (Q4).

(Ids: work-queue ids drafted elsewhere reach r49, so the added lines are r50 and r51.)

## Glossary

No term added, changed or removed. No decision drafted.

## Questions

1. work-queue Purpose says `work` "makes it `done` when its work and the requests it raised are", which the removal of r23 contradicts. (a) Purpose stays as it is. (b) Purpose reads "...it starts an initiative from an `accepted` request and leaves its `done` to `work run`; ...". Recommended: (b).
2. work-queue Implementation, may change: "r23: a request names the initiative in its `part_of` or its `source`." points at a retired id. (a) It stays. (b) It is removed, or moved to the supervision line that sets `done` if that line uses the same condition. Recommended: (b).
3. work-queue r31 ("If every work-item of an initiative is `withdrawn`, then `work` shall leave the initiative's status as it is") is now a case r50 covers; it does not conflict. (a) Kept as it stands. (b) Removed, r31 added to `retired`. Recommended: (a).
4. work-queue r51: once r23 is gone, no work-queue line has `work` set an initiative's status (r22 writes `proposed`, which Q3 says is not a transition), so r51 has no trigger here unless another initiative's draft adds one. (a) r51 stays as a standing rule. (b) r51 is held until a line that sets an initiative's status exists. Recommended: (a).
5. features/work-queue.feature: two scenarios verify r23 ("a command whose change leaves an initiative with a green work-item, every work-item green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done" and "retry that makes an initiative's last open work-item green again sets the initiative to done") and contradict r50. Formulation retires or rewrites them after the apply; no decision is asked.
