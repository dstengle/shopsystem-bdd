# Gate, i47 round 3 (request q33, requests)

## requests

Added:
- [r59] **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn and at least one line the line outcome refused, `work` shall set the request's status to `refused`. (replaces r9)
- [r60] **When** `work turn` passes the turn of a request that is not `delivered` with every line's line outcome withdrawn, `work` shall set the request's status to `withdrawn`. (q33 line 3; answers Q1 and Q2, reading A)
- [r61] **When** `work turn` passes a request's turn to its upstream with a line whose line outcome is not withdrawn, `work` shall set the request's status to `awaiting-upstream`. (replaces r18; answer Q1, reading A)

Removed (id retired):
- [r9] **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn, `work` shall set the request's status to `refused`.
- [r18] **When** `work turn` passes a request's turn to its upstream, `work` shall set the request's status to `awaiting-upstream`.

r7 is unchanged (answer Q3, reading B).

## glossary

No entry added, changed or removed.

## decisions

None.

## Questions

None.
