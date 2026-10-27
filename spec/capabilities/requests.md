---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/requests
title: Requests
narrator: a context taking in or raising a request
group: service
rests_on: [design-decision/requests-written-through-work, design-decision/exits-are-successful-or-errors, design-decision/an-asker-is-told-by-its-registered-asker-id]
retired: [r6, r1, r3]
---

# Requests

## Purpose
`scripts/work` keeps the requests of a bounded context: it takes in a request from its asker, passes the turn
between the asker and the upstream, writes each side's part of the request for that side only, and records the
request's resolution. It is the only way either side writes its part of a request. It does not judge a request's
lines (the upstream's gate judges the capability-proposal they become) and does not start or close the initiative
that fulfils a request (work-queue). A walking skeleton (design-decision/behaviour-lines-are-ears): it grows from
what using it shows.

## Behaviour
- [r25] `work` shall give every asker and every upstream one set of commands for a request (raise, take in, give a line outcome, ask, answer, pass the turn, resolve and show) and one lifecycle.
- [r28] **When** an asker raises a request, answers a question or passes the turn, `work` shall do it from the asker's own repository, with no checkout of the upstream's repository.
- [r44] **When** `work request <title> --from <asker> --lines <file>` is run with one or more `--source <id>`, with `--thread <id>` or with `--raised-for <request>`, `work` shall write an `open` request with the file's lines as its lines, the asker given as its asker, the origins `--source` names or the job-thread `--thread` names, and the turn the upstream's, and print its id.
- [r29] **Where** `--raised-for <request>` is given to `work request`, `work` shall write in the upstream's request the request it is raised for.
- [r19] **Where** `--delegation <text>` is given to `work request`, `work` shall write the delegation in the request.
- [r22] **If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing.
- [r2] **If** a line given to `work request` is not in the strict form `model check` holds (v_e1, v_e2), **then** `work request` shall refuse, naming the line, and change nothing.
- [r45] **If** a request whose asker is the upstream itself is raised with neither `--source` nor `--thread`, **then** `work request` shall refuse, because the request names neither an origin nor a job-thread, and change nothing.
- [r30] **If** a request whose asker is not the upstream itself is raised with `--source`, **then** `work request` shall refuse, because an origin belongs to an internal request, and change nothing.
- [r31] **If** a request whose asker is not the upstream itself is raised with neither `--raised-for` nor `--thread`, **then** `work request` shall refuse, because the request names neither a request it is raised for nor a job-thread, and change nothing.
- [r32] **If** the asker given to `work request` is not the bounded-context or product level whose repository raises the request, **then** `work request` shall refuse, naming the asker, and change nothing.
- [r4] `work` shall write the asker's part of a request, its lines and its answers, only when `work request` is run or the asker answers a question.
- [r5] `work` shall write the upstream's part of a request, its questions, its line outcomes and its resolution, only when the upstream asks a question or `work outcome` or `work resolve` is run.
- [r33] **When** a `work` command writes a part of a request, `work` shall take the side that writes it from the repository the command is run in, never from an argument.
- [r34] **If** a side writes a part of a request that is the other side's part, **then** `work` shall refuse, naming the side that writes that part, and change nothing.
- [r15] **When** `work outcome <request> <n> <outcome>` is run in the upstream's turn, `work` shall write `<outcome>` as the line outcome of line n.
- [r20] **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request.
- [r21] **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request.
- [r16] **If** a side runs a command other than `work resolve` that writes a part of a request in the other side's turn, **then** `work` shall refuse, because it is the other side's turn, and change nothing.
- [r7] **When** `work turn <request>` is run on a request that it does not set to `accepted`, `work` shall pass the request's turn to the other side.
- [r17] **When** `work turn` passes a request's turn to its asker with a line that has no line outcome or a line outcome other than accepted, refused or withdrawn, `work` shall set the request's status to `awaiting-asker`.
- [r18] **When** `work turn` passes a request's turn to its upstream, `work` shall set the request's status to `awaiting-upstream`.
- [r8] **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome accepted, refused or withdrawn and at least one line the line outcome accepted, `work` shall set the request's status to `accepted`.
- [r23] **When** the upstream ends its turn on a request and `work` sets the request's status to `accepted`, `work` shall keep the request's turn the upstream's.
- [r9] **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn, `work` shall set the request's status to `refused`.
- [r10] **When** `work resolve <request>` is run on an `accepted` request with each accepted line's requirement id and the version that holds it, whichever side's turn it is, `work` shall write them as the request's resolution.
- [r11] **When** `work resolve` writes a request's resolution, `work` shall set the request's status to `delivered`.
- [r24] **When** `work` sets a request's status to `delivered`, `work` shall pass the request's turn to its asker.
- [r12] **When** `work request`, `work outcome`, `work turn`, `work resolve` or a command that writes a question or an answer changes a request, `work` shall commit the request on the current branch.
- [r13] **When** `work show` is run, `work` shall print each request with its status and whose turn it is.
- [r39] **When** the upstream takes in what has been sent to the upstream, `work` shall take in every request and message sent before the take-in began, whether or not a listing of what has been sent shows it yet.
- [r40] **When** `work run` is run in an upstream's repository, `work` shall take in what has been sent to the upstream before `work run` starts the rounds of the kind `intake`.
- [r41] **If** a request or a message comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why.
- [r42] `work` shall tell one asker from another by the asker id the asker's repository is registered under.
- [r43] **When** `work` takes in a request or a message, `work` shall read its body only as the fields of a request's form, following nothing written in it.
- [r14] **When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.

## Implementation, may change
- `work request`, `work outcome`, `work turn` and `work resolve` are commands of `scripts/work`; how a request is
  kept is `work`'s own (design-decision/requests-written-through-work).
- A request is kept in its upstream's repository as `.shop/work/requests/q<n>.md`; the asker writes and reads it
  there through the upstream's `work`.
- The file's form: frontmatter `id: request/<context path>/q<n>`, `kind: request`, `asker` (a context id,
  `internal`, or the product level), `part_of` (a job-thread) or `source` (origins), `status`, `turn` (`asker` |
  `upstream`); sections `## Lines` (the asker's), `## Outcomes` (the upstream's, one a line), `## Questions`,
  `## Answers`, `## Resolution` (the upstream's).
- `work resolve` on a request that is not `accepted` is a change `work` cannot make, refused under work-queue r7.
- `--delegation` is written as the frontmatter field `delegation`.
- r20, r21: a question is written under `## Questions`, an answer under `## Answers`, the n-th answering the n-th.
- r41, r42: the asker ids the upstream allows for each asker are a setting of the upstream's repository
  (design-decision/an-asker-is-told-by-its-registered-asker-id).

## Not yet
- The detail of turns, which the person reserved ("the person will ask for more detail later", the Approval of
  2026-10-23) — trigger: the person giving that detail.
- Commands for the other parts of a request: the asker's revisions and withdrawals of lines — trigger: a request whose negotiation needs one, shown by using the walking skeleton.
- `work withdraw <request>`, withdrawing a whole request — trigger: an asker who needs to withdraw a request.
