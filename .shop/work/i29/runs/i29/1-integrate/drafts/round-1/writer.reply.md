## Drafts

/tmp/work-run-i29-wjhtu4f_/i29-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md
/tmp/work-run-i29-wjhtu4f_/i29-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/requests.md

## Change list

| change | capability | id | line | note sentence |
|---|---|---|---|---|
| added | supervision | r105 | **When** `work run` finds an initiative that is not `done`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`. | "**When** `work run` finds an initiative that is not `done`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now and whose every raised request is `delivered`, `work run` shall set the initiative to `done`." (line 1) |
| added | supervision | r106 | **When** `work run` has written an initiative's measurement and its analysis record, `work run` shall commit them on the initiative branch. | "**When** `work run` has written an initiative's measurement and its analysis, `work run` shall commit them on the initiative branch." (line 2) |
| added | supervision | r107 | **If** a change list that `work run` reads names a capability that `spec/capabilities/` does not have, **then** `work run` shall write no capability-proposal for it and exit with an error, naming the capability. | "**If** a change list that `work run` reads names a capability that `spec/capabilities/` does not have, **then** `work run` shall write no capability-proposal for it and exit with an error naming the capability." (line 3) |
| added | supervision | r108 | **When** `work run` starts a round of the kind `gate` or `apply` for a capability-proposal, `work run` shall give the round the path of the kept drafts of the round of the kind `integrate` that wrote the proposal. | "**When** `work run` starts a round of the kind `gate` or `apply` for a capability-proposal, `work run` shall give the round the path of the kept drafts of the integrate round that wrote the proposal." (line 4) |
| added | requests | r22 | **If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing. | "**If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing." (line 5) |

No glossary term is added, changed or removed.

Also changed, with no Behaviour line of its own: supervision's Purpose now says `work run` commits the initiative's measurement and analysis and sets the initiative `done` (from lines 1 and 2).

## Decision files

None.

## Questions

1. supervision r105, "every raised request": the glossary has no term "raised request". I wrote it the way work-queue r23 says it ("every request kept in this context whose asker is this context and that names the initiative"). Recommended reading: keep r105 as drafted. Other reading: only the requests the initiative's own rounds raised, so r105 says "every request that a round of the initiative raised is `delivered`".
2. supervision r105, an initiative with no work-item: "every work-item is `green` or `withdrawn`" also holds when there is none, while work-queue r23 requires at least one work-item and r94/r97 start no branch review and no measurement without one. If yes: r105 reads "...an initiative that is not `done`, that has at least one work-item, whose every work-item is ...". If no: r105 stays as drafted.
3. supervision r105 and r75/r76/r106, order: r105's condition is the same as r75's, and r66 takes no `done` initiative, so an initiative set `done` first may never be measured or analysed. If done waits for them: r105 adds "and whose measurement and analysis record `work run` has committed". If not: r105 stays as drafted.
4. supervision r105, commit: the note does not say that the initiative's new status is committed. If yes, a new line: "**When** `work run` sets an initiative's status to `done`, `work run` shall commit the initiative on the initiative branch." If no: no line.
5. supervision r107, a capability the round adds: a change list may name a new capability that the round's drafts write whole, which `spec/capabilities/` does not have yet. If such a capability is exempt: r107 reads "...names a capability that neither `spec/capabilities/` nor the round's drafts have...". If it is refused too: r107 stays as drafted.
6. supervision r107 and r92, the other capabilities: "write no capability-proposal for it" can mean only the missing capability, or none at all. Reading A (only that one): r107 stays as drafted, and r92 still writes a proposal for each other capability. Reading B (none): r107 reads "...shall write no capability-proposal for the change list and exit with an error, naming the capability."

## Cut sentences

None.
