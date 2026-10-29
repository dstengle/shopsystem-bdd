---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i60-requests
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i60
status: awaiting-answer
argues: [requests]
adds: [requests#r59, requests#r60, requests#r61, requests#r62, requests#r63]
changes: []
removes: []
date: 2026-10-29
---

# requests

The drafts of this proposal are in .shop/work/i60/runs/i60/1-integrate/drafts/round-1/.

## Questions
- requests#r60 (added): "**When** `work delegate` writes a delegation in a request, `work` shall commit the request." On which branch is the request committed? Reading A (recommended): "**When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch." Reading B: r60 stays as drafted.
- Whose part is the delegation, and may either side run `work delegate` (concerns r59: "**When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has.", and r4)? Reading A: only the asker's side: "**If** a side other than the request's asker runs `work delegate`, **then** `work delegate` shall refuse, naming the side that writes the delegation, and change nothing." (r4 then names `work delegate`.) Reading B: either side, no line.
- Does `work delegate` keep to turns as r16 does (concerns r59)? Reading A: "**If** `work delegate` is run in the other side's turn, **then** `work delegate` shall refuse, because it is the other side's turn, and change nothing." Reading B (recommended, since a delegation comes from the person at any moment): "**When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is."
- Does `work delegate` change a request's status or turn (concerns r59 and r60)? Reading A (recommended): "**When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn." Reading B: no line.
- requests#r62 (added): "**If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing." It names `withdrawn`, a status this spec does not yet name. Reading A (recommended): keep as drafted. Reading B: drop it until it exists: "...`delivered` or `refused`...".
- requests#r63 (added): "**When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date." Its narrator is a session; requests' narrator is a context taking in or raising a request. Reading A (recommended): stay in requests. Reading B: move to role-boundaries.
