---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/requests
title: Requests
narrator: a context taking in or raising a request
group: service
language: codified-1
rests_on: [design-decision/requests-written-through-work, design-decision/exits-are-successful-or-errors, design-decision/an-asker-is-told-by-its-registered-asker-id]
retired: [r1, r3, r4, r5, r10, r11, r12, r13, r19, r20, r21, r22, r23, r42, g42]
unbuilt: []
---

# Requests

## Purpose
`scripts/work` keeps the requests of a bounded context, as asker and as upstream: it opens a request's issue for its
asker, posts each step of the conversation on the issue and records the other side's, passes the turn between the
asker and the upstream, writes each side's part of the request for that side only, makes the item an accepted
request becomes, and records the request's resolution. It is the only way either side writes its part of a request.
It does not judge a request's lines (the upstream's session and person do) and does not build the item that fulfils
a request (backlog, batches).

## Terms
- **resolution** (kind): the requirement id and version of each accepted line, under a request's `## Resolution`. Kind of: text.
- **wording** (attribute of delegation): Values: `empty`, `written`.
- **closed** (condition of request): A request is closed when the request is `delivered` or the request is `refused` or the request is `withdrawn`.
- **unparsed** (condition of request line): a request line that does not parse in its upstream's requirement grammar.
- **observation** (kind): an entry of `.shop/records/observations.md`, with its id and its date.
- **uncited** (condition of observation): an observation that the `source` of no initiative and of no request names.
- **origin** (kind): what a request is raised from: an observation `--source` names, a job-thread `--thread` names, or a request `--raised-for` names.
- **originless** (condition of command): a command that gives none of `--source`, `--thread` and `--raised-for`.
- **sourced** (condition of command): a command that gives `--source` with `--thread` or `--raised-for`.
- **foreign** (condition of command): a command that gives `--from` an asker other than its own bounded context.
- **downstream** (condition of bounded context): a bounded context whose `spec/index.md` lists an upstream under `## Upstreams`.

- **issue** (kind): the GitHub issue, on the GitHub repository of a request's upstream, that carries the request's conversation. Kind of: text.
- **comment** (kind): one step of a request's conversation, posted on its issue, read only as the one block of fields it holds. Kind of: text.
- **post** (event): `work` puts an issue or a comment on GitHub. Forms: posts, posted. Frame: `work` posts text.
- **close** (event): `work` closes the issue of a request on GitHub. Forms: closes, closed. Frame: `work` closes issue.
- **unrecorded** (condition of comment): a comment on a request's issue that its request does not yet hold.
- **unreadable** (condition of comment): a comment whose block of fields does not parse.
- **unhosted** (condition of bounded context): an upstream whose entry under `## Upstreams` names no GitHub repository.

- **untaken** (condition of issue): an open issue on the GitHub repository of this bounded context whose body is an ask that no request holds.

- **uncommittable** (condition of repository): a repository in which git refuses to commit a request's record, as when a pre-commit hook fails or another process holds the index lock.

- **received** (condition of request): a request whose record is kept in its upstream's repository and whose asker is another bounded context.
- **sent** (condition of request): a request whose record is kept in its asker's repository and whose upstream is another bounded context.

- **foreign entry** (kind): an entry of a comment (`<field> <n>: <text>`) of the part of the side that did not post the comment's step: an entry of the upstream's part (`question`, `outcome`, `counter`, `reason`, `into`, and `resolution` but on a `fits`) in a step of the asker (`ask`, `fits`, or a `turn` posted in the asker's turn), or an entry of the asker's part (`line`, `answer`) in a step of the upstream (`offer`, `accept`, `resolve`, or a `turn` posted in the upstream's turn). Kind of: text.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| comment | holds | foreign entry |  |
| comment | on | request | one |

## Behaviour

### [g2] `work request` writes the request it is raised for
Restates: r29@0.29.
- [r2] Where `--raised-for` is given, when the person runs `work request` on a request, `work` shall write a request
  raised for the request.

### [g6] An internal request names an origin
Restates: r45@0.29.
- [r6] While a command is originless, if the person runs `work request`, then `work` shall exit with an error naming
  an origin and change nothing.

### [g7] A request to an upstream cites no observation
Restates: r30@0.29.
- [r7] While a bounded context is downstream and a command is sourced, if the person runs `work request`, then
  `work` shall exit with an error naming an origin and change nothing.

### [g8] A request to an upstream names the request it is raised for or a job-thread
Restates: r31@0.29.
- [r8] While a bounded context is downstream and a command is originless, if the person runs `work request`, then
  `work` shall exit with an error naming an origin and change nothing.

### [g9] A repository raises requests only as itself
Restates: r32@0.29.
- [r9] While a command is foreign, if the person runs `work request`, then `work` shall exit with an error naming a
  bounded context and change nothing.

### [g14] `work outcome` writes a line outcome in the upstream's turn
Restates: r12@0.29, r15@0.29, r5@0.29.
- [r14] When the person runs `work outcome` on a request that is `open`, `work` shall write a line outcome and commit
  the request.

### [g15] A side writes nothing in the other side's turn
Restates: r16@0.29.
- [r15] If the person runs `work outcome` on a request that is `awaiting-asker`, then `work` shall exit with an error
  naming the request and change nothing.

### [g16] The asker's repository does not write the upstream's part
Restates: r33@0.29, r55@0.29.
- [r16] While a bounded context is downstream, if the person runs `work outcome` on a request that is `open`, then
  `work` shall exit with an error naming the request and change nothing.

### [g17] `work ask` writes the upstream's question
Restates: r20@0.29, r5@0.29.
- [r17] When the person runs `work ask` on a request that is `open`, `work` shall write a question and commit the
  request.

### [g18] `work reply` writes the asker's answer
Restates: r21@0.29, r4@0.29.
- [r18] When the person runs `work reply` on a request that is `awaiting-asker`, `work` shall write an answer and
  commit the request.

### [g24] `work resolve` refuses a request that is not accepted
Restates: r10@0.29.
- [r24] If the person runs `work resolve` on a request that is not `accepted`, then `work` shall exit with an error
  naming the status of the request and change nothing.

### [g25] `work list` prints every request with its status and every observation no node cites
Restates: r50@0.29, r64@0.29.
- [r25] When the person runs `work list`, `work` shall print every request and the status of the request and print
  every observation that is uncited.

### [g26] `work show` on a request prints its status and its lines
Restates: work-queue#r59@0.29.
- [r26] When the person runs `work show` on a request, `work` shall print the status of the request and every
  request line proposed in the request.

### [g27] `work request` opens the request's issue
Restates: r12@0.29, r4@0.29, r44@0.29, r28@0.29.
- [r27] When the person runs `work request`, `work` shall post an issue, write a request that is `open` and commit the request.

### [g28] `work request` refuses an upstream with no GitHub repository
- [r28] While a bounded context is unhosted, if the person runs `work request`, then `work` shall exit with an error naming the bounded context and change nothing.

### [g29] `work offer` answers an ask with what may serve it
- [r29] When a session runs `work offer` on a request that is `open`, `work` shall post a comment, set the status of the request to `awaiting-asker` and commit the request.

### [g30] `work fits` ends a request an offer serves
- [r30] When the person runs `work fits` on a request that is `awaiting-asker`, `work` shall set the status of the request to `delivered`, write a resolution, post a comment, close an issue and commit the request.

### [g31] `work propose` writes the asker's lines
- [r31] When the person runs `work propose` on a request that is `awaiting-asker`, `work` shall write a request line and commit the request.

### [g32] `work sync` records what the other side posted
- [r32] When a session runs `work sync`, `work` shall write every comment that is unrecorded and print every request.

### [g33] `work sync` acts on no comment it cannot read
Restates: r58@0.29.
- [r33] While a comment is unreadable, when a session runs `work sync`, `work` shall print the comment, and `work` shall not write the comment.

### [g34] `work turn` posts the asker's turn
Restates: r18@0.29, r7@0.29.
- [r34] When the person runs `work turn` on a request that is `awaiting-asker`, `work` shall set its status to `awaiting-upstream`, change the side of the request and post a comment.

### [g35] The upstream's turn ends with a line not settled, posted
Restates: r17@0.29.
- [r35] While a request is `open` and a request line proposed in the request is not settled, when the person runs `work turn` on the request, `work` shall set the status of the request to `awaiting-asker` and post a comment.

### [g36] The upstream's turn ends with every line settled and one accepted, posted for the person to accept
Restates: r23@0.29, r8@0.29.
- [r36] While a request is `open` and every request line proposed in the request is settled and a request line proposed in the request is `accepted`, when the person runs `work turn` on the request, `work` shall post a comment, and `work` shall not change the side of the request.

### [g37] The upstream's turn ends with every line refused, and the issue closed
Restates: r9@0.29.
- [r37] While a request is `open` and a request line proposed in the request is `refused` and every request line proposed in the request is `refused`, when the person runs `work turn` on the request, `work` shall set the status of the request to `refused`, post a comment and close an issue.

### [g38] A line that does not parse is not accepted
Restates: r2@0.29, r59@0.29.
- [r38] While a request line is unparsed, if a session runs `work outcome accepted` on the request line, then `work` shall exit with an error naming the request line and change nothing.

### [g39] `work accept` accepts a request and writes its item
- [r39] While a request is `open` and every request line proposed in the request is settled and a request line proposed in the request is `accepted`, when the person runs `work accept` on the request, `work` shall set the status of the request to `accepted`, write an item that is `shaped`, post a comment and commit the request.

### [g40] `work accept` refuses a request with a line not settled
- [r40] While a request line proposed in a request is not settled, if the person runs `work accept` on the request, then `work` shall exit with an error naming the request line and change nothing.

### [g41] `work resolve` posts the resolution and closes the issue
Restates: r10@0.29, r11@0.29, r12@0.29, r24@0.29.
- [r41] When the person runs `work resolve` on a request that is `accepted`, `work` shall set its status to `delivered`, write a resolution, change the side of the request, post a comment, close an issue and commit the request.

### [g44] `work watch` wakes on a readable comment the request does not hold
- [r44] While a comment is unrecorded and the comment is not unreadable, when a session runs `work watch`, `work` shall print the comment and exit successfully, and `work` shall not write the comment.

### [g43] `work watch` wakes on a new ask
- [r43] While an issue is untaken, when a session runs `work watch`, `work` shall print the issue and exit successfully.

### [g45] `work request` opens no issue when its record is not committed
- [r45] While a repository is uncommittable, if the person runs `work request`, then `work` shall not post an issue.

### [g46] `work turn` posts nothing when its record is not committed
- [r46] While a repository is uncommittable, if the person runs `work turn` on a request that is `open`, then `work` shall not post a comment or close an issue.

### [g47] `work fits` posts nothing when its record is not committed
- [r47] While a repository is uncommittable, if the person runs `work fits` on a request that is `awaiting-asker`, then `work` shall not post a comment or close an issue.

### [g49] `work reply` refuses a request this context received
- [r49] If the person runs `work reply` on a request that is received, then `work` shall exit with an error naming the request.

### [g50] The upstream's `work turn` refuses the asker's turn
- [r50] While a request is received and the request is `awaiting-asker`, if the person runs `work turn` on the request, then `work` shall exit with an error naming the request.

### [g51] The asker's `work turn` refuses the upstream's turn
- [r51] While a request is sent and the request is `open`, if the person runs `work turn` on the request, then `work` shall exit with an error naming the request.

### [g48] The asker's `work turn` refuses a turn it has passed
- [r48] While a request is sent and the request is `awaiting-upstream`, if the person runs `work turn` on the request, then `work` shall exit with an error naming the request.

### [g52] `work sync` writes no entry of the other side's part
- [r52] While a comment that is unrecorded holds a foreign entry, when a session runs `work sync`, `work` shall write the comment, and `work` shall not write the foreign entry.

### [g53] `work sync` reopens no closed request
- [r53] While a request is closed and a comment on the request is unrecorded, when a session runs `work sync`, `work` shall write the comment, and `work` shall not change the status of the request or change the side of the request.

### [g54] The SessionStart hook names a sent request awaiting the upstream
- [r54] While a request is sent and the request is `awaiting-upstream`, when the SessionStart hook runs `work watch --hook`, `work` shall print the request.

### [g55] The SessionStart hook names a received request awaiting the asker
- [r55] While a request is received and the request is `awaiting-asker`, when the SessionStart hook runs `work watch --hook`, `work` shall print the request.

### [g56] The SessionStart hook is silent with every request closed
- [r56] While every request is closed, when the SessionStart hook runs `work watch --hook`, `work` shall exit successfully, and `work` shall not print a request.

### [g57] `work watch --forward` wakes on a readable comment the request does not hold
- [r57] While a comment is unrecorded and the comment is not unreadable, when a session runs `work watch --forward`, `work` shall print the comment and exit successfully, and `work` shall not write the comment.

### [g58] `work watch --forward` wakes on a new ask
- [r58] While an issue is untaken, when a session runs `work watch --forward`, `work` shall print the issue and exit successfully.

## Implementation, may change
- A request between two bounded contexts, each in its own git repository, is one conversation on one GitHub issue on
  the upstream's GitHub repository; nothing reads or writes the other side's git repository. Each step is a comment a
  `work` command posts through `gh` (`$SHOPSYSTEM_WORK_GH`, else `gh`), and each side keeps its own record of the
  conversation as `.shop/requests/q<n>.md`, its number one above the highest of `.shop/requests/` and the frozen
  `.shop/work/requests/`, the two sides' numbers apart and linked by the issue's URL. A context's own request is an
  issue on its own GitHub repository, its asker and its upstream the same context. How a request is kept is `work`'s
  own (design-decision/requests-written-through-work).
- Where the issue lives: an upstream's bullet under `## Upstreams` in `spec/index.md` names its GitHub repository,
  `github: <owner>/<name>` (an upstream with none is unhosted, r28); a context's own repository is read off its git
  remote `origin`.
- The record's form: frontmatter `id: request/<context path>/q<n>`, `kind: request`, `asker` (a context id,
  `internal`, or the product level), `upstream` (the context that answers it), `issue` (its URL), `part_of` (a
  job-thread) or `source` (origins), `raised_for`, `asked_as` (the asker's own request id, on the upstream's
  record), `status`, `turn` (`asker` | `upstream`, the request's side); sections `## Ask` (the asker's words),
  `## Offer` (the upstream's offer, quoted), `## Lines` and `## Answers` (the asker's), `## Questions`,
  `## Outcomes`, `## Counter-proposals`, `## Reasons`, `## Into` and `## Resolution` (the upstream's), and
  `## Comments`, `<k>. <URL> <step>` for each comment the record holds. A record kept from before requests went
  through issues has no `upstream` and no `issue`, posts nothing and is written by this repository as either side.
- The comment form: one fenced block, `~~~shop-request` to `~~~`, of fields `<name>: <value>` (a value of more than
  one line continued on lines indented by two spaces) above any free text: `step` (`ask`, `offer`, `fits`, `turn`,
  `accept`, `resolve`), `request`, `status` and `turn` after the step, and the entries of the poster's part as
  `<field> <n>: <text>` (`line`, `answer`, `question`, `outcome`, `counter`, `reason`, `into`, `resolution`). Only
  the block is read; free text and anything else in an issue is shown, never acted on. A body with no block, or a
  block that does not parse, is unreadable.
- `work request <title> --from <asker> [--ask <words>] [--to <upstream>]` with `--source <id>`, `--thread <id>` or
  `--raised-for <request>` opens the issue, its body the `ask` form, and writes the record open in the upstream's
  turn; it prints the request's id and the issue's URL. `--to` defaults to the one upstream of a request to an
  upstream (no `--source`), else this context.
- `work offer <request> [--capability <c>]... [--note <words>]` (the upstream, on an open request) posts the note,
  each named capability's file whole and the glossary of `spec/index.md`, and passes the turn to the asker. `work
  fits <request> --serves <requirement>...` (the asker) writes the requirements that serve as the resolution, posts
  it, closes the issue (an issue's author may close it) and sets the request `delivered`. `work propose <request>
  --line <text>...` (the asker) appends lines; `work turn` posts them.
- The asker's part is written only by `work propose`, `work reply` and `work fits`; the upstream's part only by
  `work offer`, `work ask`, `work outcome`, `work accept` and `work resolve`. The side that writes is the repository
  the command runs in, read off the record's `upstream` and `asker`, never an argument.
- `work turn` posts the side's part with the request's status and turn after it. From the upstream, every line
  proposed settled with one accepted keeps the turn and the status, for `work accept`; every line refused sets the
  request `refused` and closes its issue.
- `work accept <request>` (the upstream's person, or a session the person told) takes a request in the upstream's
  turn whose lines proposed are all settled with one accepted, each accepted line naming the capability it goes into
  (`## Into`): it writes the `shaped` item, sets the request `accepted` and posts the acceptance, one commit.
- `work resolve <request> --line <n> <requirement> <version>` writes each accepted line's requirement id and the
  version that holds it, posts the resolution and closes the issue; `work resolve` on a request that is not
  `accepted` is refused (U11). A delivered request's turn is the asker's.
- `work sync` lists the open issues of this context's own repository and writes a record for each `ask` no record
  holds, then reads the issue of every record, closed or not, and records each comment it does not hold, applying
  only the part of the side that posted its step (r52): its entries written into their sections by number, its
  status and turn set, an offer quoted under `## Offer`. The poster is the asker of an `ask` or a `fits`, the
  upstream of an `offer`, an `accept` or a `resolve`, and of a `turn` the side whose turn the request was; a foreign
  entry is recorded with its comment, so no watch wakes on it again, and never applied. A comment on a closed
  request sets neither its status nor its turn (r53), so a late comment reopens no request. An unreadable comment is printed and never
  recorded. The records changed are one commit, on the current branch; then every request is printed with its status
  and, unless it is `delivered`, `refused` or `withdrawn`, whose move it waits on.
- `work watch [--every <seconds>] [--polls <n>]` polls GitHub every `--every` seconds (default 60), as `work sync`
  reads it: the issue of each request not `delivered`, `refused` or `withdrawn`, and the open issues of this context's
  own repository. After the first poll that finds a comment a request does not hold or an `ask` no record holds, it
  prints one line for each and exits successfully, so a session runs it in the background and is woken when it ends;
  the session then runs `work sync` and starts the watch again. A readable comment and an untaken ask are printed by
  every watch that finds them, until `work sync` records or takes them in (r44, r43). An unreadable comment, which
  `work sync` prints and never records (r33), is printed by one watch only and passed over by later ones, so it does
  not wake a session in a loop; r44's condition leaves it out: its URL is kept in `<git dir>/shopsystem/watched.json`, the file holding only unreadable comments, never
  committed. A poll whose `gh` fails is said on stderr and tried again at the next. `--polls <n>` makes a bounded
  watch, used by the tests: it stops after n polls that found nothing and exits 1, so a caller tells "nothing new"
  from a wake. `work watch` writes nothing in the repository and commits nothing.
- `work watch --forward [--every <seconds>] [--polls <n>]` waits on GitHub's events instead of polling the issues
  (r57, r58). It watches this context's own repository and the repository of each request's issue not `delivered`,
  `refused` or `withdrawn`, read again at each wake. On a repository whose `viewerPermission` is `ADMIN` it runs `gh
  webhook forward` for the `issues` and `issue_comment` events to a listener on 127.0.0.1, first running `gh
  extension install cli/gh-webhook` when `gh extension list` does not name it. On any other repository, or when the
  extension does not install or a forward ends, it polls GitHub's notifications instead (`GET /notifications` with
  If-Modified-Since, no sooner than its X-Poll-Interval asks, else 60 s), and says so on stderr: `work watch: polling
  GitHub's notifications for <repositories>`. At its start it takes the notifications' baseline, then checks once as
  `work watch` polls; each event, and each notification of a polled repository, wakes the same check, which prints
  what it finds and exits successfully. Under `--forward`, `--every` (default 60) is the longest wait for an event,
  and `--polls <n>` ends a watch whose n waits found nothing, printing `work watch: nothing new after <n> waits` on
  stderr and exiting 1. Its forwards end with it, and it writes nothing in the repository.
- `work watch --hook` is the requests' SessionStart hook (r54-r56): it prints each request that waits on the other
  side, a sent request that is `awaiting-upstream` or a received one that is `awaiting-asker`, one line each as
  `<name> <status>: <title> (<issue>)` (the issue left out of a request with none), then one line, last,
  telling the session to start `work watch --forward` with the Monitor tool and to run `work sync` when it wakes.
  With no request waiting it prints nothing. It reads only the records under `.shop/requests/`, never GitHub, and writes
  nothing; whatever goes wrong, it prints nothing and exits 0, so a hook never fails a session's start.
  `hooks/hooks.json` runs it as `request_hook watch`, an entry point apart from `work`: `work` imports the grammar's
  modules, which need site packages (clingo), and a hook runs under any `python3`, with site packages or without.
  `request_hook watch` prints what `work watch --hook` prints and, whatever goes wrong, an import included, exits 0.
- `work show <request>` prints the request's status and turn, then whose turn it is and, for a request on an issue,
  the issue's URL (`it is the <side>'s turn, on <URL>`), then each line with its line outcome, each question with its
  answer and the resolution.
- A question is written under `## Questions`, an answer under `## Answers`, the n-th answering the n-th.
- `## Counter-proposals` holds `<n>. <m>` for each line n that the upstream's `work outcome <request> <n> rewritten
  --line <text>` rewrote as its line m. Line n is then no longer a request line proposed in the request, and its
  counter-proposal m is: `work turn` counts and reads the lines proposed. A request without the section is read as
  before.
- Tests run against the stand-in gh (`tests/scripts/stub_gh.py`); the test against GitHub runs only when
  `$SHOPSYSTEM_TEST_GITHUB_REPO` names a repository it may open and close issues on.
- The asker ids the upstream allows for each asker are a setting of the upstream's repository
  (design-decision/an-asker-is-told-by-its-registered-asker-id).

## Not yet
- The detail of turns, which the person reserved ("the person will ask for more detail later", the Approval of
  2026-10-23) — trigger: the person giving that detail.
- Commands for the other parts of a request: the asker's revisions and withdrawals of lines — trigger: a request whose negotiation needs one, shown by using the walking skeleton.
- `work withdraw <request>`, withdrawing a whole request — trigger: an asker who needs to withdraw a request.
- The upstream taking in what has been sent to it whatever a listing shows (0.29's r40, r56): `work sync` reads what
  gh's listing of open issues shows; telling askers apart by their registered asker id and leaving untaken what comes
  from an id not allowed (r42, r57), the backlog's b32 — trigger: that item.
- `work list` printing whose turn each request is (r50), and `work show <request>` printing, in the asker's
  repository, that it is the asker's turn with each unanswered question (r51), that what the asker sent is not yet
  taken in (r52), that the asker has not seen what the upstream holds unsent (r53), and the resolution's requirement
  ids and versions after the upstream resolves (r54).

## Dropped
- r25@0.29: one set of commands and one lifecycle for every asker and upstream is a statement about the command set, kept under Implementation, may change; each command's groups restate its behaviour.
- r40@0.29: not implemented; kept under Not yet.
- r42@0.29: not implemented; kept under Not yet.
- r51@0.29: not implemented; kept under Not yet.
- r52@0.29: not implemented; kept under Not yet.
- r53@0.29: not implemented; kept under Not yet.
- r54@0.29: not implemented; kept under Not yet.
- r56@0.29: not implemented; kept under Not yet.
- r57@0.29: not implemented; kept under Not yet.
- r72@0.29: what a session does with a delegation the person gives it is no behaviour of `work`; the hook that tells the session is `migrate prompting`'s (migration-tools).
- r19@0.29: retired with requests#r3 in 2.0.0 (the-old-workflow-retired).
- r22@0.29: retired with requests#r4 in 2.0.0 (the-old-workflow-retired).
- r65@0.29: retired with requests#r10 in 2.0.0 (the-old-workflow-retired).
- r66@0.29: retired with requests#r10 in 2.0.0 (the-old-workflow-retired).
- r67@0.29: retired with requests#r12 in 2.0.0 (the-old-workflow-retired).
- r68@0.29: retired with requests#r13 in 2.0.0 (the-old-workflow-retired).
- r70@0.29: retired with requests#r11 in 2.0.0 (the-old-workflow-retired).
- r71@0.29: retired with requests#r10 in 2.0.0 (the-old-workflow-retired).
