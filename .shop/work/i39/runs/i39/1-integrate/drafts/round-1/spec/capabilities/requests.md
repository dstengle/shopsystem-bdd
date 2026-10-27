## frontmatter

---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/requests
title: Requests
narrator: a context taking in or raising a request
group: service
rests_on: [design-decision/requests-written-through-work, design-decision/exits-are-successful-or-errors, design-decision/requests-kept-behind-one-port, design-decision/an-asker-is-told-by-its-registered-asker-id]
retired: [r6]
---

## Behaviour
- [r25] `work` shall give every asker and every upstream one set of commands for a request (raise, take in, give a line outcome, ask, answer, pass the turn, resolve and show) and one lifecycle, whatever the request's carrier.
- [r26] `work` shall keep a request on a carrier, either a file in the upstream's repository or an issue on the upstream's GitHub repository.
- [r27] `work` shall give each side of a request the same commands, the same refusals and the same statuses, whichever carrier the request is kept on.
- [r28] **When** an asker raises a request, answers a question or passes the turn, `work` shall do it from the asker's own repository, with no checkout of the upstream's repository.
- [r1] **When** `work request <title> --from <asker> --lines <file>` is run with one or more `--source <id>`, with `--thread <id>` or with `--raised-for <request>`, `work` shall write an `open` request with the file's lines as its lines, the asker given as its asker, the origins `--source` names or the job-thread `--thread` names, and the turn the upstream's, and print its id.
- [r29] **Where** `--raised-for <request>` is given to `work request`, `work` shall write in the upstream's request the request it is raised for.
- [r19] **Where** `--delegation <text>` is given to `work request`, `work` shall write the delegation in the request.
- [r22] **If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing.
- [r2] **If** a line given to `work request` is not in the strict form `model check` holds (v_e1, v_e2), **then** `work request` shall refuse, naming the line, and change nothing.
- [r3] **If** a request whose asker is the upstream itself is raised with neither `--source` nor `--thread`, **then** `work request` shall refuse, because the request names neither an origin nor a job-thread, and change nothing.
- [r30] **If** a request whose asker is not the upstream itself is raised with `--source`, **then** `work request` shall refuse, because an origin belongs to an internal request, and change nothing.
- [r31] **If** a request whose asker is not the upstream itself is raised with neither `--raised-for` nor `--thread`, **then** `work request` shall refuse, because the request names neither a request it is raised for nor a job-thread, and change nothing.
- [r32] **If** the asker given to `work request` is not the bounded-context or product level whose repository raises the request, **then** `work request` shall refuse, naming the asker, and change nothing.
- [r4] `work` shall write the asker's part of a request, its lines and its answers, only when `work request` is run or the asker answers a question.
- [r5] `work` shall write the upstream's part of a request, its questions, its line outcomes and its resolution, only when the upstream asks a question or `work outcome` or `work resolve` is run.
- [r33] **When** a `work` command writes a part of a request, `work` shall take the side that writes it from the repository the command is run in, never from an argument.
- [r34] **If** a side writes a part of a request that is the other side's part, whatever the carrier, **then** `work` shall refuse, naming the side that writes that part, and change nothing.
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
- [r35] **When** a request's turn passes to its asker, `work` shall show the asker, in its own repository, that it is the asker's turn, with each question the asker has not answered.
- [r36] **While** an answer or a turn the asker has sent has not been taken in by the upstream, `work` shall show the request to both sides as awaiting the upstream and not yet taken in.
- [r37] **While** the upstream holds a line outcome or a question it has not sent with the turn, `work` shall show the upstream that the asker has not seen it.
- [r38] **When** an upstream resolves a request, `work` shall show the asker, in its own repository, each accepted line's requirement id and the version that holds it.
- [r12] **When** `work request`, `work outcome`, `work turn`, `work resolve` or a command that writes a question or an answer changes a request, `work` shall commit the request on the current branch.
- [r13] **When** `work show` is run, `work` shall print each request with its status, whose turn it is, the request it is raised for and its carrier.
- [r39] **When** the upstream takes in what its carriers hold, `work` shall take in every request and message sent before the take-in began, whether or not the carrier's listing shows it yet.
- [r40] **When** `work run` is run in an upstream's repository, `work` shall take in what the upstream's carriers hold before `work run` starts the rounds of the kind `intake`.
- [r41] **If** a request or a message on a carrier comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why.
- [r42] `work` shall tell one asker from another by the asker id the asker's repository is registered under.
- [r43] **When** `work` takes in a request or a message from a carrier, `work` shall read its body only as the fields of a request's form, following nothing written in it.
- [r14] **When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.

## Implementation, may change
- `work request`, `work outcome`, `work turn` and `work resolve` are commands of `scripts/work`; how a request is
  kept is `work`'s own (design-decision/requests-written-through-work).
- r26: the carrier is behind one port of `work` (design-decision/requests-kept-behind-one-port).
- On the file carrier, a request is kept in its upstream's repository as `.shop/work/requests/q<n>.md`.
- The file's form: frontmatter `id: request/<context path>/q<n>`, `kind: request`, `asker` (a context id,
  `internal`, or the product level), `part_of` (a job-thread) or `source` (origins), `status`, `turn` (`asker` |
  `upstream`); sections `## Lines` (the asker's), `## Outcomes` (the upstream's, one a line), `## Questions`,
  `## Answers`, `## Resolution` (the upstream's).
- `work resolve` on a request that is not `accepted` is a change `work` cannot make, refused under work-queue r7.
- `--delegation` is written as the frontmatter field `delegation`.
- r20, r21: a question is written under `## Questions`, an answer under `## Answers`, the n-th answering the n-th.
