# requests, formulate round 1

Draft: /home/vscode/shopsystem-bdd/.shop/worktrees/requests-3-formulate/.shop/scratch/3-formulate/round-1/requests.feature

It holds new scenarios for r28, r44, r29, r45, r30, r31, r32, r40 and r42. It also holds changed scenarios for r19, r22, r2 and r14. Those four lines are unchanged, but their existing scenarios now break under r30:
- The @r19, @r22 and @r2 scenarios run `--from ctx-a ... --source o1`, which r30 now refuses. They now give `--thread t1`.
- The @r14 scenario's request from ctx-a has an origin, which r30 now gives only to internal requests. Its request is now one whose asker is the upstream itself.

The @r1 and @r3 scenarios are to be removed. Six new lines get no scenario because each has two readings: r25, r33, r34, r39, r41 and r43 (see Questions).

## Coverage

| id | line | scenario |
|---|---|---|
| r25 | "`work` shall give every asker and every upstream one set of commands for a request (raise, take in, give a line outcome, ask, answer, pass the turn, resolve and show) and one lifecycle." | none: question 1 |
| r28 | "**When** an asker raises a request, answers a question or passes the turn, `work` shall do it from the asker's own repository, with no checkout of the upstream's repository." | the asker <doing> from its own repository, with no checkout of the upstream's repository (new, outline) |
| r44 | "**When** `work request <title> --from <asker> --lines <file>` is run with one or more `--source <id>`, with `--thread <id>` or with `--raised-for <request>`, `work` shall write an `open` request with the file's lines as its lines, the asker given as its asker, the origins `--source` names or the job-thread `--thread` names, and the turn the upstream's, and print its id." | request with <given> writes an open request in the upstream's turn with the lines and asker given and <where from>, and prints its id (new, outline; replaces @r1) |
| r29 | "**Where** `--raised-for <request>` is given to `work request`, `work` shall write in the upstream's request the request it is raised for." | request with --raised-for writes in the upstream's request the request it is raised for (new) |
| r19 | "**Where** `--delegation <text>` is given to `work request`, `work` shall write the delegation in the request." | request with --delegation writes the delegation given in the request (changed: --thread t1) |
| r22 | "**If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing." | request with an empty delegation is refused, and nothing changes (changed: --thread t1) |
| r2 | "**If** a line given to `work request` is not in the strict form `model check` holds (v_e1, v_e2), **then** `work request` shall refuse, naming the line, and change nothing." | request with a line that <fault> is refused, naming the line, and nothing changes (changed: --thread t1) |
| r45 | "**If** a request whose asker is the upstream itself is raised with neither `--source` nor `--thread`, **then** `work request` shall refuse, because the request names neither an origin nor a job-thread, and change nothing." | a request the upstream raises for itself with neither --source nor --thread is refused, and nothing changes (new; replaces @r3) |
| r30 | "**If** a request whose asker is not the upstream itself is raised with `--source`, **then** `work request` shall refuse, because an origin belongs to an internal request, and change nothing." | a request from another asker raised with --source is refused, and nothing changes (new) |
| r31 | "**If** a request whose asker is not the upstream itself is raised with neither `--raised-for` nor `--thread`, **then** `work request` shall refuse, because the request names neither a request it is raised for nor a job-thread, and change nothing." | a request from another asker raised with neither --raised-for nor --thread is refused, and nothing changes (new) |
| r32 | "**If** the asker given to `work request` is not the bounded-context or product level whose repository raises the request, **then** `work request` shall refuse, naming the asker, and change nothing." | request raised from <role>'s repository giving the asker <given asker> is refused, naming the asker, and nothing changes (new, outline) |
| r4 | "`work` shall write the asker's part of a request, its lines and its answers, only when `work request` is run or the asker answers a question." | outcome writing a line outcome leaves the request's lines and answers as the asker wrote them (existing) |
| r5 | "`work` shall write the upstream's part of a request, its questions, its line outcomes and its resolution, only when the upstream asks a question or `work outcome` or `work resolve` is run." | the asker answering a question leaves the request's questions and line outcomes as they were and writes no resolution (existing) |
| r33 | "**When** a `work` command writes a part of a request, `work` shall take the side that writes it from the repository the command is run in, never from an argument." | none: question 2 |
| r34 | "**If** a side writes a part of a request that is the other side's part, **then** `work` shall refuse, naming the side that writes that part, and change nothing." | none: question 2 |
| r15 | "**When** `work outcome <request> <n> <outcome>` is run in the upstream's turn, `work` shall write `<outcome>` as the line outcome of line n." | outcome in the upstream's turn writes the outcome given as the line outcome of the line named (existing) |
| r20 | "**When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request." | the upstream asking a question on a line in its turn writes the question in the request (existing) |
| r21 | "**When** the asker answers a question on a request in its turn, `work` shall write the answer in the request." | the asker answering a question in its turn writes the answer in the request (existing) |
| r16 | "**If** a side runs a command other than `work resolve` that writes a part of a request in the other side's turn, **then** `work` shall refuse, because it is the other side's turn, and change nothing." | a side writing a part of a request in the other side's turn is refused, and nothing changes (existing) |
| r7 | "**When** `work turn <request>` is run on a request that it does not set to `accepted`, `work` shall pass the request's turn to the other side." | turn on a request it does not set to accepted passes the request's turn from the <side> to the <other side> (existing) |
| r17 | "**When** `work turn` passes a request's turn to its asker with a line that has no line outcome or a line outcome other than accepted, refused or withdrawn, `work` shall set the request's status to `awaiting-asker`." | turn passing a request to its asker with a line that has <line 2> sets the request's status to awaiting-asker (existing) |
| r18 | "**When** `work turn` passes a request's turn to its upstream, `work` shall set the request's status to `awaiting-upstream`." | turn passing a request to its upstream sets the request's status to awaiting-upstream (existing) |
| r8 | "**When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome accepted, refused or withdrawn and at least one line the line outcome accepted, `work` shall set the request's status to `accepted`." | the upstream ending its turn with every line accepted, refused or withdrawn and one accepted sets the status to accepted; the upstream ending its turn on a delivered request with every line accepted leaves the status delivered (existing) |
| r23 | "**When** the upstream ends its turn on a request and `work` sets the request's status to `accepted`, `work` shall keep the request's turn the upstream's." | the upstream ending its turn on a request that turn sets to accepted keeps the request's turn the upstream's (existing) |
| r9 | "**When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn, `work` shall set the request's status to `refused`." | the upstream ending its turn with every line refused or withdrawn sets the status to refused (existing) |
| r10 | "**When** `work resolve <request>` is run on an `accepted` request with each accepted line's requirement id and the version that holds it, whichever side's turn it is, `work` shall write them as the request's resolution." | resolve on an accepted request in the asker's turn writes each accepted line's requirement id and version as the resolution (existing) |
| r11 | "**When** `work resolve` writes a request's resolution, `work` shall set the request's status to `delivered`." | resolve writing a request's resolution sets the request's status to delivered (existing) |
| r24 | "**When** `work` sets a request's status to `delivered`, `work` shall pass the request's turn to its asker." | resolve setting a request's status to delivered passes the request's turn to its asker (existing) |
| r12 | "**When** `work request`, `work outcome`, `work turn`, `work resolve` or a command that writes a question or an answer changes a request, `work` shall commit the request on the current branch." | a change to a request commits the request on the current branch (existing) |
| r13 | "**When** `work show` is run, `work` shall print each request with its status and whose turn it is." | show prints each request with its status and whose turn it is (existing) |
| r39 | "**When** the upstream takes in what has been sent to the upstream, `work` shall take in every request and message sent before the take-in began, whether or not a listing of what has been sent shows it yet." | none: question 3 |
| r40 | "**When** `work run` is run in an upstream's repository, `work` shall take in what has been sent to the upstream before `work run` starts the rounds of the kind `intake`." | run in an upstream's repository takes in what has been sent to it before its intake rounds start (new) |
| r41 | "**If** a request or a message comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why." | none: question 3 |
| r42 | "`work` shall tell one asker from another by the asker id the asker's repository is registered under." | requests from repositories registered under different asker ids are taken in as different askers' requests (new) |
| r43 | "**When** `work` takes in a request or a message, `work` shall read its body only as the fields of a request's form, following nothing written in it." | none: question 3 |
| r14 | "**When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names." | status with no initiative prints, with its date, each observation no initiative's or request's source names (changed: the request with an origin is the upstream's own) |

## Questions

1. r25: "`work` shall give every asker and every upstream one set of commands for a request (raise, take in, give a line outcome, ask, answer, pass the turn, resolve and show) and one lifecycle."
   - Reading A: asker and upstream share a single set of `work` commands. No separate tool exists for either side.
   - Reading B: every kind of asker (another context, the product level, the context itself) raises and negotiates a request with the same commands, and its request goes through the same statuses.
   - Also: "take in" is listed as a command, but no line names the command or its arguments. Under either reading, which command is it?

2. r33: "**When** a `work` command writes a part of a request, `work` shall take the side that writes it from the repository the command is run in, never from an argument." This also covers r34: "**If** a side writes a part of a request that is the other side's part, **then** `work` shall refuse, naming the side that writes that part, and change nothing."
   - The problem: when a request's asker is the upstream itself, the asker's repository and the upstream's repository are the same. So the repository does not say which side is writing.
   - Reading A: in that repository a command writes as whichever side owns the part it writes. A line outcome is written as the upstream, an answer as the asker, and r34 never refuses on an internal request.
   - Reading B: that repository is the upstream's side only. A command writing the asker's part of an internal request (an answer) is refused under r34.

3. r39, r41 and r43: "a request or a message" / "every request and message". "message" is not in the Glossary and no line says what one is.
   - Reading A: a message is what an asker sends besides a request: its answer to a question or its passing of the turn (the acts r28 lists).
   - Reading B: a message is a separate kind of thing sent to the upstream. If so, it needs its own command and form, and no line gives either.

## Cases no line mentions

- `--raised-for` naming a request the asker does not keep, or one that does not exist.
- `--raised-for` and `--thread` given together by another asker, or `--source` and `--thread` given together by the upstream for itself.
- `--raised-for` given on a request whose asker is the upstream itself.
- The product level giving `--source`: r30 applies to it as an asker that is not the upstream itself, but no line says so.
- r28 when the upstream's repository cannot be reached from the asker's repository.
- r39 for a request or message sent after the take-in began.
- The same request taken in twice, by two take-ins or by `work run` and a take-in.
- r40 when nothing has been sent to the upstream, or when something is sent after the intake rounds have started.
- A request from a repository registered under an asker id the upstream's settings name for no asker at all.
- r16 for a request whose asker is the upstream itself: whose turn holds when the one repository is both sides.
- `--delegation` on a request the upstream raises for itself.
