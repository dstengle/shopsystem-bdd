# Gate: i33 round 1 (request q10)

No glossary entry, no decision drafted.

## work-queue (spec/capabilities/work-queue.md)

Added:
- [r31] **If** every work-item of an initiative is `withdrawn`, **then** `work` shall leave the initiative's status as it is.
- [r32] **If** `work add` is given an initiative that is `done` or `abandoned`, **then** `work add` shall refuse, naming the initiative's status, and change nothing.

## supervision (spec/capabilities/supervision.md)

Added:
- [r120] **When** the delegation-answerer answers a reviewer's question on a work-item, the delegation-answerer shall give in its result whether its answer asks for a change or accepts the work-item as it is.
- [r121] **When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever its status.

## Questions

1. r31 against work-queue r23 (and supervision r105, r75). r23 sets an initiative `done` when every work-item is `green` or `withdrawn`, which an all-`withdrawn` initiative meets, so r23 and r31 contradict.
   - (a, recommended) Change r23 to: "[r23] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." Likewise change supervision r105 "that has at least one work-item" to "that has at least one work-item that is `green`", and add to r75 "and at least one of them is `green`".
   - (b) Leave r23, r105, r75 as they are; r31 overrides them and they read as contradicting it.
2. r120's subject. "the delegation-answerer" is no glossary term; r77 calls it "a session of its own, given the delegation".
   - (a, recommended) Recast: "[r120] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item, the session shall give in its result whether its answer asks for a change or accepts the work-item as it is."
   - (b) Keep r120 as drafted and add the glossary entry "- **delegation-answerer**: the session `work run` starts under a request's delegation to answer one question of an initiative."
3. r120, the result's field. The note gives none.
   - (a, recommended) Draft none.
   - (b) Add under Implementation: "- r120: the answer's result gives `change` or `accept`, as `work answer`'s `--change` and `--accept` (work-queue r26, r27)."
4. r121, "whatever its status".
   - (a, recommended) The status of the review's result (its outcome, e.g. `DONE` or `PARTIAL`): r121 as drafted.
   - (b) The review's verdict: "[r121] **When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever verdict the review gives."
5. r121 and a branch reviewer's session that ends in error, at its turn limit, or with no readable result.
   - (a, recommended) Add nothing.
   - (b) Add "[r122] **If** a branch reviewer's session ends in an error or at its turn limit or leaves no result `work run` can read, then `work run` shall take the review as not read."

## Cut sentences

- "Initiatives done only when delivered, and reviews read as they now report" (the note's title; intent, no section).
