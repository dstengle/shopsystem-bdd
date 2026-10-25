## Behaviour
- [r1] **When** `work request <title> --from <asker> --lines <file>` is run with one or more `--source <id>` or with `--thread <id>`, `work` shall write an `open` request with the file's lines as its lines, the asker given as its asker, the origins `--source` names or the job-thread `--thread` names, and the turn the upstream's, and print its id.
- [r19] **Where** `--delegation <text>` is given to `work request`, `work` shall write the delegation in the request.
- [r2] **If** a line given to `work request` is not in the strict form `model check` holds (v_e1, v_e2), **then** `work request` shall refuse, naming the line, and change nothing.
- [r3] **If** `work request` is run with neither `--source` nor `--thread`, **then** `work request` shall refuse, because the request names neither an origin nor a job-thread, and change nothing.
- [r4] `work` shall write the asker's part of a request, its lines, only when `work request` is run.
- [r5] `work` shall write the upstream's part of a request, its line outcomes and its resolution, only when `work outcome` or `work resolve` is run.
- [r15] **When** `work outcome <request> <n> <outcome>` is run in the upstream's turn, `work` shall write `<outcome>` as the line outcome of line n.
- [r20] **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request.
- [r21] **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request.
- [r16] **If** a side runs a command other than `work resolve` that writes a part of a request in the other side's turn, **then** `work` shall refuse, because it is the other side's turn, and change nothing.
- [r7] **When** `work turn <request>` is run, `work` shall pass the request's turn to the other side.
- [r17] **When** `work turn` passes a request's turn to its asker with a line that has no line outcome or a line outcome other than accepted, refused or withdrawn, `work` shall set the request's status to `awaiting-asker`.
- [r18] **When** `work turn` passes a request's turn to its upstream, `work` shall set the request's status to `awaiting-upstream`.
- [r8] **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome accepted, refused or withdrawn and at least one line the line outcome accepted, `work` shall set the request's status to `accepted`.
- [r9] **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn, `work` shall set the request's status to `refused`.
- [r10] **When** `work resolve <request>` is run on an `accepted` request with each accepted line's requirement id and the version that holds it, whichever side's turn it is, `work` shall write them as the request's resolution.
- [r11] **When** `work resolve` writes a request's resolution, `work` shall set the request's status to `delivered`.
- [r12] **When** `work request`, `work outcome`, `work turn` or `work resolve` changes a request, `work` shall commit the request on the current branch.
- [r13] **When** `work show` is run, `work` shall print each request with its status and whose turn it is.
- [r14] **When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.

## Not yet
- The detail of turns, which the person reserved ("the person will ask for more detail later", the Approval of
  2026-10-23) — trigger: the person giving that detail.
- Commands for the other parts of a request: the asker's revisions and withdrawals of lines — trigger: a request
  whose negotiation needs one, shown by using the walking skeleton.
- `work withdraw <request>`, withdrawing a whole request — trigger: an asker who needs to withdraw a request.
