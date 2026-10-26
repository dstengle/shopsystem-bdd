## Coverage

| id | line | scenario |
|---|---|---|
| r7 (changed) | "**When** `work turn <request>` is run on a request that it does not set to `accepted`, `work` shall pass the request's turn to the other side." | Scenario Outline: turn on a request it does not set to accepted passes the request's turn from the <side> to the <other side> |
| r23 (added) | "**When** the upstream ends its turn on a request and `work` sets the request's status to `accepted`, `work` shall keep the request's turn the upstream's." | the upstream ending its turn on a request that turn sets to accepted keeps the request's turn the upstream's |
| r24 (added) | "**When** `work` sets a request's status to `delivered`, `work` shall pass the request's turn to its asker." | resolve setting a request's status to delivered passes the request's turn to its asker |

The other lines are unchanged and keep their existing scenarios. The r7 outline keeps its two rows and the step wording it had. It gains one step, "Then q1's status is not accepted", which shows that the line's condition holds.

## Questions

None.

## Cases no line mentions

- The upstream runs `work turn` on a request that is already `accepted` and in its own turn. I read r8 as setting it to accepted again, so r23 keeps the turn the upstream's and r7 does not pass it. That means once a request is accepted, `work turn` can never hand it to the asker. If "sets to accepted" is meant only as a change from another status, r7 would pass the turn instead.
- `work turn` on a `delivered` request in the asker's turn: r7 passes the turn to the upstream. r18 would then set the status to `awaiting-upstream`, which would replace `delivered`.
- `work turn` on a `refused` request: r7 passes the turn, and r17 or r18 may then change the status, which would replace `refused`.
- `work resolve` on an accepted request in the asker's turn (which r10 allows): r24 passes the turn to the asker, so the turn does not change.
- A status set to `delivered` by anything other than `work resolve`: no line names another way. The r24 scenario uses `work resolve` as its one way.

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/requests-3-formulate/.shop/scratch/3-formulate/drafts/round-1/requests.feature
