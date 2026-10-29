---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i60-requests
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i60
status: awaiting-answer
argues: [requests]
date: 2026-10-29
adds: [requests#r65, requests#r66, requests#r67, requests#r68, requests#r69, requests#r70, requests#r71]
changes: []
removes: []
---

# requests

The drafts of this proposal are in .shop/work/i60/runs/requests/19-integrate/drafts/round-1/.

## Questions
- requests#r60 (added): "**When** `work delegate` writes a delegation in a request, `work` shall commit the request." On which branch is the request committed? Reading A (recommended): "**When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch." Reading B: r60 stays as drafted.
- Whose part is the delegation, and may either side run `work delegate` (concerns r59: "**When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has.", and r4)? Reading A: only the asker's side: "**If** a side other than the request's asker runs `work delegate`, **then** `work delegate` shall refuse, naming the side that writes the delegation, and change nothing." (r4 then names `work delegate`.) Reading B: either side, no line.
- Does `work delegate` keep to turns as r16 does (concerns r59)? Reading A: "**If** `work delegate` is run in the other side's turn, **then** `work delegate` shall refuse, because it is the other side's turn, and change nothing." Reading B (recommended, since a delegation comes from the person at any moment): "**When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is."
- Does `work delegate` change a request's status or turn (concerns r59 and r60)? Reading A (recommended): "**When** `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn." Reading B: no line.
- requests#r62 (added): "**If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing." It names `withdrawn`, a status this spec does not yet name. Reading A (recommended): keep as drafted. Reading B: drop it until it exists: "...`delivered` or `refused`...".
- requests#r63 (added): "**When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date." Its narrator is a session; requests' narrator is a context taking in or raising a request. Reading A (recommended): stay in requests. Reading B: move to role-boundaries.
- Do r16 and r55 reach `work delegate`? Lines concerned: [r70] "**When** `work delegate` is run, `work` shall write the delegation whichever side's turn it is." (added) and the person's answer that either side may run `work delegate`; r16 ("a command other than `work resolve` ... in the other side's turn ... refuse") and r55 (a side writing the other side's part is refused when the asker is not the upstream itself). Reading A (recommended): the delegation belongs to neither side's part, so r16 and r55 do not reach `work delegate`; no line changes. Reading B: r16 and r55 are retired and redrafted with "other than `work resolve` and `work delegate`".
- requests#r69: "**When** the person gives a session a delegation for a request outside `work request`, the session shall write the delegation in the request with `work delegate` in the same reply, in the person's words and with the date." Reading 1: the session puts the date into the text it gives `work delegate`, so the request holds the person's words followed by the date. Reading 2: the request holds the person's words alone, word for word, and the date is written beside it, apart from the delegation.

## Faults
- the session answering requests's question faulted: while its answerer worked, .shop/work/i55/work-queue.md, .shop/work/i55/runs/work-queue/7-answer/brief.md, .shop/work/i55/runs/work-queue/7-answer/result.json, .shop/work/i55/runs/work-queue/7-answer/session.json changed in the repository's own checkout and not committed; work run put them back

## Answers
- 2026-10-29: Reading A, as the person delegated (2026-10-29: answer every question with its recommended reading): r60 becomes "**When** `work delegate` writes a delegation in a request, `work` shall commit the request on the current branch."
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- 2026-10-29: Reading B: either side may run work delegate, no line; a delegation is the person handing over decisions, mostly the upstream's gate questions (answered by the person, 2026-10-29)
- 2026-10-29: Reading B: When `work delegate` is run, `work` shall write the delegation whichever side's turn it is (the delegation comes from the person at any moment, so it does not keep to turns as r16 does).
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- 2026-10-29: Reading A, as the person's delegation directs (2026-10-28 'I take recommendations'; 2026-10-29 answer every question with its recommended reading): 'When `work delegate` writes a delegation in a request, `work` shall keep the request's status and turn.'
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- 2026-10-29: Reading A, as recommended and under the person's delegation of 2026-10-29: keep r62 as drafted, naming delivered, refused or withdrawn.
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- 2026-10-29: Reading A: r63 stays in requests, as the person's delegation of 2026-10-28/29 says to take the recommended reading.
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
- 2026-10-29: Reading A: the delegation belongs to neither side's part, so r16 and r55 do not reach `work delegate`; no line changes (the person, 2026-10-29: answer every question with its recommended reading).
  by: work run, under the delegation "The person, 2026-10-28: "i am delegating to you" and "I take recommendations"; 2026-10-29: answer every question with its recommended reading; questions of a glossary-proposal are the person's."
