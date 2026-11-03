---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/requests
title: Requests
narrator: a context taking in or raising a request
group: service
language: codified-1
rests_on: [design-decision/requests-written-through-work, design-decision/exits-are-successful-or-errors, design-decision/an-asker-is-told-by-its-registered-asker-id]
retired: []
---

# Requests

## Purpose
`scripts/work` keeps the requests of a bounded context: it takes in a request from its asker, passes the turn
between the asker and the upstream, writes each side's part of the request for that side only, and records the
request's resolution. It is the only way either side writes its part of a request. It does not judge a request's
lines (the upstream's gate judges the capability-proposal they become) and does not start or close the initiative
that fulfils a request (work-queue).

## Terms
- **proposed in** (relation request line → request): a line of a request, under its `## Lines`.
- **resolution** (kind): the requirement id and version of each accepted line, under a request's `## Resolution`.
- **wording** (attribute of delegation): Values: `empty`, `written`.
- **closed** (condition of request): A request is closed when the request is `delivered` or the request is `refused` or the request is `withdrawn`.
- **unparsed** (condition of request line): a request line that does not parse in the requirement grammar of the upstream.
- **observation** (kind): an entry of `.shop/records/observations.md`, with its id and its date.
- **uncited** (condition of observation): an observation that the `source` of no initiative and of no request names.
- **origin** (kind): what a request is raised from: an observation `--source` names, a job-thread `--thread` names, or a request `--raised-for` names.
- **originless** (condition of command): a command that gives none of `--source`, `--thread` and `--raised-for`.
- **sourced** (condition of command): a command that gives `--source` with `--thread` or `--raised-for`.
- **foreign** (condition of command): a command that gives `--from` an asker other than the bounded context it is run in.
- **downstream** (condition of bounded context): a bounded context whose `spec/index.md` lists an upstream under `## Upstreams`.

## Behaviour

### [g1] `work request` takes in an open request
Restates: r44@0.29, r4@0.29, r12@0.29.
- [r1] When the person runs `work request`, `work` shall write a request that is `open`.
- [r2] When the person runs `work request`, `work` shall commit a request.

### [g2] `work request` writes the request it is raised for
Restates: r29@0.29.
- [r3] Where `--raised-for` is given, when the person runs `work request` on a request, `work` shall write a request raised for the request.

### [g3] `work request` writes a delegation it is given
Restates: r19@0.29.
- [r4] Where `--delegation` is given, when the person runs `work request`, `work` shall write a delegation.

### [g4] `work request` refuses an empty delegation
Restates: r22@0.29.
- [r5] While a delegation is `empty`, if the person runs `work request`, then `work` shall exit with an error naming the delegation and change nothing.

```given
a delegation d1 that is `empty`
```

### [g5] `work request` refuses a line that does not parse
Restates: r2@0.29, r59@0.29.
- [r6] While a request line is unparsed, if the person runs `work request`, then `work` shall exit with an error naming the request line and change nothing.

```given
a request line r1
the request line r1 is unparsed
```

### [g6] An internal request names an origin
Restates: r45@0.29.
- [r7] While a command is originless, if the person runs `work request`, then `work` shall exit with an error naming an origin and change nothing.

```given
a command c1
the command c1 is originless
```

### [g7] A request to an upstream cites no observation
Restates: r30@0.29.
- [r8] While a bounded context is downstream and a command is sourced, if the person runs `work request`, then `work` shall exit with an error naming an origin and change nothing.

```given
a bounded context b1
the bounded context b1 is downstream
a command c1
the command c1 is sourced
```

### [g8] A request to an upstream names the request it is raised for or a job-thread
Restates: r31@0.29.
- [r9] While a bounded context is downstream and a command is originless, if the person runs `work request`, then `work` shall exit with an error naming an origin and change nothing.

```given
a bounded context b1
the bounded context b1 is downstream
a command c1
the command c1 is originless
```

### [g9] A repository raises requests only as itself
Restates: r32@0.29.
- [r10] While a command is foreign, if the person runs `work request`, then `work` shall exit with an error naming a bounded context and change nothing.

```given
a command c1
the command c1 is foreign
```

### [g10] `work delegate` writes a delegation in place of any
Restates: r65@0.29, r66@0.29, r71@0.29.
- [r11] When the person runs `work delegate` on a request that is `open`, `work` shall write a delegation.
- [r12] When the person runs `work delegate` on a request that is `open`, `work` shall commit the request.
- [r13] When the person runs `work delegate` on a request that is `open`, `work` shall not change the status of the request.
- [r14] When the person runs `work delegate` on a request that is `open`, `work` shall not change the side of the request.

### [g11] `work delegate` writes a delegation in the asker's turn
Restates: r70@0.29.
- [r15] When the person runs `work delegate` on a request that is `awaiting-asker`, `work` shall write a delegation.

### [g12] `work delegate` refuses an empty delegation
Restates: r67@0.29.
- [r16] While a delegation is `empty`, if the person runs `work delegate` on a request that is `open`, then `work` shall exit with an error naming the delegation and change nothing.

```given
a delegation d1 that is `empty`
```

### [g13] `work delegate` refuses a closed request
Restates: r68@0.29.
- [r17] If the person runs `work delegate` on a request that is closed, then `work` shall exit with an error naming the status of the request and change nothing.

### [g14] `work outcome` writes a line outcome in the upstream's turn
Restates: r15@0.29, r5@0.29, r12@0.29.
- [r18] When the person runs `work outcome` on a request that is `open`, `work` shall write a line outcome.
- [r19] When the person runs `work outcome` on a request that is `open`, `work` shall commit the request.

### [g15] A side writes nothing in the other side's turn
Restates: r16@0.29.
- [r20] If the person runs `work outcome` on a request that is `awaiting-asker`, then `work` shall exit with an error naming the request and change nothing.

### [g16] The asker's repository does not write the upstream's part
Restates: r55@0.29, r33@0.29.
- [r21] While a bounded context is downstream, if the person runs `work outcome` on a request that is `open`, then `work` shall exit with an error naming the request and change nothing.

```given
a bounded context b1
the bounded context b1 is downstream
```

### [g17] `work ask` writes the upstream's question
Restates: r20@0.29, r5@0.29.
- [r22] When the person runs `work ask` on a request that is `open`, `work` shall write a question.
- [r23] When the person runs `work ask` on a request that is `open`, `work` shall commit the request.

### [g18] `work reply` writes the asker's answer
Restates: r21@0.29, r4@0.29.
- [r24] When the person runs `work reply` on a request that is `awaiting-asker`, `work` shall write an answer.
- [r25] When the person runs `work reply` on a request that is `awaiting-asker`, `work` shall commit the request.

### [g19] `work turn` passes the asker's turn to the upstream
Restates: r7@0.29, r18@0.29.
- [r26] When the person runs `work turn` on a request that is `awaiting-asker`, `work` shall set its status to `awaiting-upstream`.
- [r27] When the person runs `work turn` on a request that is `awaiting-asker`, `work` shall change the side of the request.

### [g20] The upstream's turn ends with a line not settled
Restates: r17@0.29.
- [r28] While a request line is not settled, when the person runs `work turn` on a request that is `open`, `work` shall set the status of the request to `awaiting-asker`.

### [g21] The upstream's turn ends with every line settled and one accepted
Restates: r8@0.29, r23@0.29.
- [r29] While a request line is `accepted`, when the person runs `work turn` on a request that is `open`, `work` shall set the status of the request to `accepted`.
- [r30] While a request line is `accepted`, when the person runs `work turn` on a request that is `open`, `work` shall not change the side of the request.

```given
a request line r1 that is `accepted`
```

### [g22] The upstream's turn ends with every line refused
Restates: r9@0.29.
- [r31] While a request line is `refused`, when the person runs `work turn` on a request that is `open`, `work` shall set the status of the request to `refused`.

```given
a request line r1 that is `refused`
```

### [g23] `work resolve` delivers an accepted request
Restates: r10@0.29, r11@0.29, r24@0.29, r12@0.29.
- [r32] When the person runs `work resolve` on a request that is `accepted`, `work` shall set its status to `delivered`.
- [r33] When the person runs `work resolve` on a request that is `accepted`, `work` shall write a resolution.
- [r34] When the person runs `work resolve` on a request that is `accepted`, `work` shall change the side of the request.
- [r35] When the person runs `work resolve` on a request that is `accepted`, `work` shall commit the request.

### [g24] `work resolve` refuses a request that is not accepted
Restates: r10@0.29.
- [r36] If the person runs `work resolve` on a request that is not `accepted`, then `work` shall exit with an error naming the status of the request and change nothing.

### [g25] `work list` prints every request with its status
Restates: r50@0.29.
- [r37] When the person runs `work list`, `work` shall print every request and its status.

### [g26] `work list` prints every observation no node cites
Restates: r64@0.29.
- [r38] When the person runs `work list`, `work` shall print every observation that is uncited.

### [g27] `work show` on a request prints its status and its lines
Restates: work-queue#r59@0.29.
- [r39] When the person runs `work show` on a request, `work` shall print the status of the request and every request line proposed in the request.

## Implementation, may change
- `work request`, `work outcome`, `work ask`, `work reply`, `work turn`, `work resolve` and `work delegate` are
  commands of `scripts/work`, one set for every asker and every upstream, with one lifecycle; how a request is kept
  is `work`'s own (design-decision/requests-written-through-work).
- A request is kept in its upstream's repository as `.shop/work/requests/q<n>.md`; the asker writes and reads it
  there through the upstream's `work`.
- The file's form: frontmatter `id: request/<context path>/q<n>`, `kind: request`, `asker` (a context id,
  `internal`, or the product level), `part_of` (a job-thread) or `source` (origins), `raised_for`, `status`, `turn`
  (`asker` | `upstream`, the request's side), `delegation`; sections `## Lines` (the asker's), `## Questions`,
  `## Answers`, `## Outcomes` (the upstream's, one a line), `## Resolution` (the upstream's).
- `work request <title> --from <asker> --lines <file>` takes `--source <id>`, `--thread <id>`, `--raised-for <request>`
  and `--delegation <text>`, writes the file's lines as the request's lines with the turn the upstream's, and prints
  its id. A line is parsed in the upstream's requirement grammar where its `spec/index.md` is codified, and held to
  0.29's strict form otherwise.
- The asker's part (its lines and answers) is written only by `work request` and `work reply`; the upstream's part
  (its questions, line outcomes and resolution) only by `work ask`, `work outcome` and `work resolve`. The side that
  writes is the repository the command runs in, never an argument.
- `work resolve <request> --line <n> <requirement> <version>` writes each accepted line's requirement id and the
  version that holds it, whichever side's turn it is; `work resolve` on a request that is not `accepted` is refused
  (U3). A delivered request's turn is the asker's.
- `work turn` from the upstream keeps the turn the upstream's when it sets the request `accepted`.
- A question is written under `## Questions`, an answer under `## Answers`, the n-th answering the n-th.
- The asker ids the upstream allows for each asker are a setting of the upstream's repository
  (design-decision/an-asker-is-told-by-its-registered-asker-id).

## Not yet
- The detail of turns, which the person reserved ("the person will ask for more detail later", the Approval of
  2026-10-23) — trigger: the person giving that detail.
- Commands for the other parts of a request: the asker's revisions and withdrawals of lines — trigger: a request whose negotiation needs one, shown by using the walking skeleton.
- `work withdraw <request>`, withdrawing a whole request — trigger: an asker who needs to withdraw a request.
- Raising a request, answering a question or passing the turn from the asker's own repository, with no checkout of
  the upstream's (0.29's r28), and the upstream taking in what has been sent to it, before `work run`'s intake rounds
  and whatever a listing shows (r40, r56), telling askers apart by their registered asker id and leaving untaken what
  comes from an id not allowed (r42, r57), reading a sent body only as a request's fields (r58).
- `work list` printing whose turn each request is (r50), and `work show <request>` printing, in the asker's
  repository, that it is the asker's turn with each unanswered question (r51), that what the asker sent is not yet
  taken in (r52), that the asker has not seen what the upstream holds unsent (r53), and the resolution's requirement
  ids and versions after the upstream resolves (r54).

## Dropped
- r25@0.29: one set of commands and one lifecycle for every asker and upstream is a statement about the command set, kept under Implementation, may change; each command's groups restate its behaviour.
- r28@0.29: not implemented; kept under Not yet.
- r40@0.29: not implemented; kept under Not yet.
- r42@0.29: not implemented; kept under Not yet.
- r51@0.29: not implemented; kept under Not yet.
- r52@0.29: not implemented; kept under Not yet.
- r53@0.29: not implemented; kept under Not yet.
- r54@0.29: not implemented; kept under Not yet.
- r56@0.29: not implemented; kept under Not yet.
- r57@0.29: not implemented; kept under Not yet.
- r58@0.29: not implemented; kept under Not yet.
- r72@0.29: what a session does with a delegation the person gives it is no behaviour of `work`; the hook that tells the session is `migrate prompting`'s (migration-tools).
