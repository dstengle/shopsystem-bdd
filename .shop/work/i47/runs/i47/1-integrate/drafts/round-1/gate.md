# Gate, i47 round 1 (request q33)

## supervision

Added:
- [r177] **While** no work-item accepts a requirement that a scenario names, `work run` shall count a failure of that scenario in the whole-suite run of a work-item's branch as expected.
- [r178] **When** a work-item's researcher gives an empty file set and no question, `work run` shall take the empty file set as the researcher's output.

## requests

Removed (id retired):
- [r9] **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn, `work` shall set the request's status to `refused`. (Line 3 gives `withdrawn` for the all-withdrawn case.)

Added:
- [r47] **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn and at least one line the line outcome refused, `work` shall set the request's status to `refused`.
- [r48] **When** `work turn` passes a request's turn with every line's line outcome withdrawn, `work` shall set the request's status to `withdrawn`.

## glossary

No entry added, changed or removed.

## decisions

None.

## Questions

1. requests, r48 against r18: line 3 says "passes a request's turn" without saying which side. When the asker passes the turn to the upstream with every line withdrawn, r18 sets `awaiting-upstream` and r48 sets `withdrawn`.
   - Reading A (recommended): r48 holds for either side; change r18 to "[r18] **When** `work turn` passes a request's turn to its upstream with a line whose line outcome is not withdrawn, `work` shall set the request's status to `awaiting-upstream`." and keep r48 as drafted.
   - Reading B: r48 holds only for the upstream's turn: "[r48] **When** `work turn` passes a request's turn to its asker with every line's line outcome withdrawn, `work` shall set the request's status to `withdrawn`." and r18 stays.
2. requests, r48 and `delivered`: r9 and r47 apply only to a request that is not `delivered`; line 3 does not say whether r48 does.
   - Reading A (recommended): yes: "[r48] **When** `work turn` passes the turn of a request that is not `delivered` with every line's line outcome withdrawn, `work` shall set the request's status to `withdrawn`."
   - Reading B: no: r48 as drafted.
3. requests, r48 and the turn: r7 still passes the turn of a request r48 sets `withdrawn` to the other side; line 3 does not say where the turn goes.
   - Reading A: the turn stays with the side that ran `work turn`: add "[r49] **When** `work` sets a request's status to `withdrawn`, `work` shall keep the request's turn with the side that ran `work turn`.", and r7 gets the same exception it makes for `accepted`.
   - Reading B (recommended): nothing changes.
4. supervision, r177 against r4: r4 merges a work-item branch only if the whole suite passes "but for the failing scenarios r43 counts as expected". As drafted, a failure r177 counts as expected still blocks the merge.
   - Reading A (recommended): r177 lets the merge through: change r4 to "[r4] **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r177 count as expected."
   - Reading B: r4 stays.
5. supervision, Implementation for r177: the existing note "r122: the checks are the whole-suite runs of r24 and r43" names the runs; line 1 says only "the whole-suite run of a work-item's branch".
   - Reading A (recommended): r177 covers both runs: add the Implementation line "r177: the whole-suite runs are those of r24 and r43; `--whole-suite` marks each such scenario as xfail."
   - Reading B: only r43's run before a merge: "r177: the whole-suite run is r43's, before a merge."
