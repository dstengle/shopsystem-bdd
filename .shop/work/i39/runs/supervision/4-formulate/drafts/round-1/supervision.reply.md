## (2) Coverage

| id | line | scenario |
|---|---|---|
| r136 | "**While** a request that an initiative raised into an upstream is not `delivered`, `work run` shall draft no work-item for the capability-proposal whose lines it raised." | a formulated capability-proposal whose integrate round raised the lines of a request into an upstream gets no work-item while that request is not delivered |

## (3) Questions

None. The reading of r136 was settled: only the capability-proposal whose integrate round gave the raised lines waits.

## (4) Cases no line mentions (no scenario written)

- One integrate round writes several capability-proposals and gives the lines of a request into an upstream. The settled reading ties the lines to "the one whose integrate round gave the raised lines", but here that round wrote every proposal, so no line says which proposal the lines belong to.
- A raised request that ends `refused` or `withdrawn` is never `delivered`. Read as written, r136 then stops the proposal's work-items from being drafted for good, and no line says what happens next.
- No line says whether a proposal that is waiting on its raised request is shown to the person, or how `work run` exits while it waits.
- No line says what happens when an integrate round redrafts a proposal anew (r142) and that redraft raises no lines, while a request an earlier round raised for that proposal is still not `delivered`.
- No line says whether the r123 retiring work-item and the r74 fix-now work-item are also held back under a proposal that is waiting on its raised request.

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-4-formulate/.shop/scratch/4-formulate/drafts/round-1/supervision.feature
