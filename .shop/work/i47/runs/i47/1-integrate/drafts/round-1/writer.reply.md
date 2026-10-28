/tmp/work-run-i47-4gxq_o97/i47-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md
/tmp/work-run-i47-4gxq_o97/i47-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/requests.md

## Change list

| change | capability | id | line | note sentence |
|---|---|---|---|---|
| added | supervision | r177 | **While** no work-item accepts a requirement that a scenario names, `work run` shall count a failure of that scenario in the whole-suite run of a work-item's branch as expected. | 1. "**While** no work-item accepts a requirement that a scenario names, the whole-suite run of a work-item's branch shall count a failure of that scenario as expected." |
| added | supervision | r178 | **When** a work-item's researcher gives an empty file set and no question, `work run` shall take the empty file set as the researcher's output. | 2. "**When** a work-item's researcher gives an empty file set and no question, `work run` shall take the empty file set as the researcher's output." |
| removed | requests | r9 | **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn, `work` shall set the request's status to `refused`. | 3. "**When** `work turn` passes a request's turn with every line's outcome `withdrawn`, `work` shall set the request's status to `withdrawn`." (r9 gives `refused` for a request whose every line is withdrawn; line 3 gives `withdrawn`) |
| added | requests | r47 | **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn and at least one line the line outcome refused, `work` shall set the request's status to `refused`. | 3. "**When** `work turn` passes a request's turn with every line's outcome `withdrawn`, `work` shall set the request's status to `withdrawn`." (r9 narrowed to leave the all-withdrawn case to r48) |
| added | requests | r48 | **When** `work turn` passes a request's turn with every line's line outcome withdrawn, `work` shall set the request's status to `withdrawn`. | 3. "**When** `work turn` passes a request's turn with every line's outcome `withdrawn`, `work` shall set the request's status to `withdrawn`." |

Notes on the rows:
- r177 is placed after r122, r178 after r132; r132 is unchanged.
- r9's id is added to requests' `retired` (frontmatter drafted whole); r47 takes r9's place.
- r48 says "line outcome" where the note says "outcome": the glossary's **outcome** is the one word a session's result gives, and **line outcome** is the upstream's answer to one line.
- No glossary change: `withdrawn` is a request status in the glossary's **status** entry already.
- No decisions.

Conflict check for r48: r8 does not conflict, because it needs at least one accepted line. r17 does not conflict, because it needs a line with no line outcome or a line outcome other than accepted, refused or withdrawn. r18 does conflict (question 1).

## Questions

1. requests, r48 against r18: line 3 says "passes a request's turn" without saying which side. When the asker passes the turn to the upstream with every line withdrawn, r18 sets `awaiting-upstream` and r48 sets `withdrawn`.
   - If r48 holds for either side: change r18 to "[r18] **When** `work turn` passes a request's turn to its upstream with a line whose line outcome is not withdrawn, `work` shall set the request's status to `awaiting-upstream`." and keep r48 as drafted.
   - If r48 holds only for the upstream's turn: change r48 to "[r48] **When** `work turn` passes a request's turn to its asker with every line's line outcome withdrawn, `work` shall set the request's status to `withdrawn`." and leave r18 as is.
2. requests, r48 and `delivered`: r9 and r47 apply only to a request that is not `delivered`. Line 3 does not say whether r48 does.
   - If yes: "[r48] **When** `work turn` passes the turn of a request that is not `delivered` with every line's line outcome withdrawn, `work` shall set the request's status to `withdrawn`."
   - If no: r48 as drafted.
3. requests, r48 and the turn: r7 still passes the turn of a request r48 sets `withdrawn` to the other side. Line 3 does not say where the turn goes.
   - If the turn is to stay with the side that passed it: "[r49] **When** `work` sets a request's status to `withdrawn`, `work` shall keep the request's turn with the side that ran `work turn`.", and r7 would need the same exception it makes for `accepted`.
   - Otherwise: nothing changes.
4. supervision, r177 against r4: r4 merges a work-item branch only if the whole suite passes "but for the failing scenarios r43 counts as expected". As drafted, a failure that r177 counts as expected still blocks the merge.
   - If r177 is to let the merge through: change r4 to "[r4] **When** an implementer's session ends with a result that gives no question, `work run` shall merge its work-item branch into the initiative branch only if the work-item's scenarios pass on it and the whole suite passes on it but for the failing scenarios r43 and r177 count as expected."
   - If not: r4 stays.
5. supervision, Implementation for r177: the existing note "r122: the checks are the whole-suite runs of r24 and r43" names the runs that count as expected. Line 1 says only "the whole-suite run of a work-item's branch".
   - If r177 covers both runs: add the Implementation line "r177: the whole-suite runs are those of r24 and r43; `--whole-suite` marks each such scenario as xfail."
   - If it covers only r43's run before a merge: the line would say "r177: the whole-suite run is r43's, before a merge."

## Cut sentences

- "Faults work run and work met in i46: unaccepted scenarios in the whole suite, an empty file set, a request withdrawn whole" (the note's title)
