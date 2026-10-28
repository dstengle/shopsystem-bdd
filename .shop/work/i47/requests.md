---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i47-requests
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i47
status: awaiting-answer
argues: [requests]
adds: [requests#r47, requests#r48]
changes: []
removes: [requests#r9]
date: 2026-10-28
---

# requests

The drafts of this proposal are in .shop/work/i47/runs/i47/1-integrate/drafts/round-1/.

## Questions
- requests, r48 against r18: line 3 of q33 says 'passes a request's turn' without saying which side. When the asker passes the turn to the upstream with every line withdrawn, r18 sets awaiting-upstream and r48 sets withdrawn. Lines: [r47] When the upstream ends its turn on a request that is not delivered whose every line has the line outcome refused or withdrawn and at least one line refused, work shall set the request's status to refused (replaces r9, retired). [r48] When work turn passes a request's turn with every line's line outcome withdrawn, work shall set the request's status to withdrawn. Reading A (recommended): r48 holds for either side; change r18 to '[r18] When work turn passes a request's turn to its upstream with a line whose line outcome is not withdrawn, work shall set the request's status to awaiting-upstream.' and keep r48 as drafted. Reading B: r48 holds only for the upstream's turn: '[r48] When work turn passes a request's turn to its asker with every line's line outcome withdrawn, work shall set the request's status to withdrawn.' and r18 stays.
- requests, r48 and delivered: r9 and r47 apply only to a request that is not delivered; line 3 does not say whether r48 does. Line: [r48] When work turn passes a request's turn with every line's line outcome withdrawn, work shall set the request's status to withdrawn. Reading A (recommended): yes: '[r48] When work turn passes the turn of a request that is not delivered with every line's line outcome withdrawn, work shall set the request's status to withdrawn.' Reading B: no: r48 as drafted.
- requests, r48 and the turn: r7 still passes the turn of a request r48 sets withdrawn to the other side; line 3 does not say where the turn goes. Line: [r48] as above. Reading A: the turn stays with the side that ran work turn: add '[r49] When work sets a request's status to withdrawn, work shall keep the request's turn with the side that ran work turn.', and r7 gets the same exception it makes for accepted. Reading B (recommended): nothing changes.
