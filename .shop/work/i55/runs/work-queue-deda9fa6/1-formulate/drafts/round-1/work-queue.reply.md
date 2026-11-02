## Coverage

| id | line | scenario |
|---|---|---|
| r47 | **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`. | withdraw that leaves every work-item green or withdrawn while a capability-proposal is neither formulated nor withdrawn keeps the initiative started |

The scenario follows the setup of r62 and r31: one green work-item and one ready work-item that is then withdrawn. It differs from r62 only in having capability-proposal p2 `approved`. No request names i1, so the proposal is the only thing that can hold the initiative open.

## Questions

None. r47 has only one reading.

## Cases no line mentions

- An initiative that is not `started` (for example `proposed`) with every work-item green or withdrawn and a proposal neither formulated nor withdrawn. "Keep `started`" assumes the initiative is already `started`, and no line says whether `work` leaves another status alone or sets it to `started`.
- Which `work` command's change can end an initiative held open under r47. The capability-proposal still has to become `formulated` or `withdrawn`, but no line of work-queue says that this transition is a `work` command whose change triggers r62.
- The scenario uses `work withdraw` as the triggering command. Whether `work retry` back to `green` behaves the same under r47 is implied by "every work-item" but not shown.

## Drafts

- /tmp/work-run-i55-bbqcq18a/work-queue-deda9fa6-1-formulate/.shop/scratch/1-formulate/drafts/round-1/work-queue.feature
