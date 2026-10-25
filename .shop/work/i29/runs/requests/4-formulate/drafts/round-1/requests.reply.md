## (2) Coverage

| id | line | scenario |
|---|---|---|
| r22 | "**If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing." | request with an empty delegation is refused, and nothing changes |

## (3) Questions

None.

## (4) Cases no line mentions

- A delegation of only spaces or newlines: r22 does not say whether that counts as empty, so the draft has no scenario for it.
- `--delegation` given with no value after it: r22 does not say whether that is an empty delegation or an argument error.
- `--delegation` given twice, once empty and once not: no line says which one counts.

## Drafts

- /tmp/work-run-i29-xe9tuer6/requests-4-formulate/.shop/scratch/4-formulate/drafts/round-1/requests.feature
- /tmp/work-run-i29-xe9tuer6/requests-4-formulate/.shop/scratch/4-formulate/drafts/round-1/requests.reply.md
