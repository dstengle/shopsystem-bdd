---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/requests
title: Requests
narrator: a context taking in or raising a request
group: service
language: codified-2
rests_on: [design-decision/requests-written-through-work, design-decision/exits-are-successful-or-errors, design-decision/an-asker-is-told-by-its-registered-asker-id]
retired: [r1, r3, r4, r5, r10, r11, r12, r13, r19, r20, r21, r22, r23, r42, g42, g2, r2, g6, r6, g7, r7, g8, r8, g9, r9, g14, r14, g15, r15, g16, r16, g17, r17, g18, r18, g24, r24, g25, r25, g26, r26, g27, r27, g28, r28, g29, r29, g30, r30, g31, r31, g32, r32, g33, r33, g34, r34, g35, r35, g36, r36, g37, r37, g38, r38, g39, r39, g40, r40, g41, r41, g44, r44, g43, r43, g45, r45, g46, r46, g47, r47, g49, r49, g50, r50, g51, r51, g48, r48, g52, r52, g53, r53, g54, r54, g55, r55, g56, r56, g57, r57, g58, r58]
unbuilt: [r59, r60, r61, r62, r63, r64, r65, r67, r68, r69, r70, r71, r72, r73, r74, r75, r76, r77, r78, r79, r80, r81, r82, r83, r84, r85, r86, r87, r88, r89, r90, r91, r92, r93, r94, r95, r96, r97, r98, r99, r100, r101, r102, r103]
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
- **resolution** (noun): the requirement id and version of each accepted line, under a request's `## Resolution`. Kind of: text.
- **observation** (noun): an entry of `.shop/records/observations.md`, with its id and its date.
- **issue** (noun): the GitHub issue, on the GitHub repository of a request's upstream, that carries the request's conversation. Kind of: text.
- **comment** (noun): one step of a request's conversation, posted on its issue. Kind of: text.
- **post** (verb, action): `work` puts an issue or a comment on GitHub. Forms: posts, posted. Frame: `work` posts text.
- **close** (verb, action): `work` closes the issue of a request on GitHub. Forms: closes, closed. Frame: `work` closes issue.
- **address** (verb, state): a request asks a bounded context, its upstream. Forms: addresses, addressed. Frame: request addresses bounded context.
- **originate** (verb, state): a request is raised by a bounded context, its asker. Forms: originates, originated. Frame: request originates from bounded context.
- **identify** (verb, state): a text is the id of a bounded context, its path or the path's last part, or `internal` for this bounded context. Forms: identifies, identified. Frame: text identifies bounded context.
- **cite** (verb, state): a request or an initiative names an observation under its `source:`. Forms: cites, cited. Frame: thing cites observation.
- **reject** (verb, state): git refuses to commit in a repository, as when a pre-commit hook fails or another process holds the index lock. Forms: rejects, rejected. Frame: repository rejects commit.
- **the comment form** (artifact): one fenced block of fields, `~~~shop-request` to `~~~`, of `<name>: <value>` lines that the comment's step names, above any free text.
- **requirement grammar** (artifact): the grammar a bounded context's requirements are parsed in, over its glossary and its capabilities' terms.
- **GitHub repository** (noun): the repository on GitHub that the issues of the requests to a bounded context are posted on. Kind of: thing.
- **entry** (noun): one field of a comment, `<field> <n>: <text>`, of the part of one side: `line` or `answer` of the asker's, `question`, `outcome`, `counter`, `reason`, `into` or `resolution` of the upstream's. Plural: entries. Kind of: text.
- **side** (attribute of comment): Values: `asker`, `upstream`.
- **side** (attribute of entry): Values: `asker`, `upstream`.
- **status** (attribute of issue): Values: `open`, `closed`.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| issue | of | request | one |
| comment | on | request | one |
| comment | in | request |  |
| entry | in | comment |  |
| requirement grammar | of | bounded context | one |
| GitHub repository | of | bounded context | one |
| issue | in | GitHub repository | one |
| upstream entry | in | bounded context |  |

## Behaviour

### [g59] `work request` writes the request it is raised for
Restates: r29@0.29.
- [r59] When the person runs `work request` with the `--raised-for` option set to a request, `work` shall write a request raised for the request.

### [g60] `work request` refuses a request with no origin
Restates: r45@0.29, r31@0.29.
- [r60] If the person runs `work request` without the `--source`, `--thread` and `--raised-for` options, then `work` shall refuse the command and name `--thread`.

### [g61] `work request` to an upstream refuses an observation beside a job-thread
Restates: r30@0.29.
- [r61] While this bounded context holds an upstream entry, if the person runs `work request` with the `--source` and `--thread` options, then `work` shall refuse the command and name `--source`.

### [g62] A repository raises requests only as itself
Restates: r32@0.29.
- [r62] If the person runs `work request` with the `--from` option set to a text that does not identify this bounded context, then `work` shall refuse the command and name the text.

### [g63] `work outcome` writes a line outcome in the upstream's turn
Restates: r12@0.29, r15@0.29, r5@0.29.
- [r63] While a request is `open`, when the person runs `work outcome accepted` on a request line proposed in the request, `work` shall set the line outcome of the request line to `accepted` and commit the request.

### [g64] A side writes nothing in the other side's turn
Restates: r16@0.29.
- [r64] While a request is `awaiting-asker`, if the person runs `work outcome` on the request, then `work` shall refuse the command and name the request.

### [g65] The asker's repository does not write the upstream's part
Restates: r33@0.29, r55@0.29.
- [r65] While a request is `open` and the request does not address this bounded context, if the person runs `work outcome` on the request, then `work` shall refuse the command and name the request.

### [g66] `work ask` writes the upstream's question
Restates: r20@0.29, r5@0.29.
- [r66] While a request is `open`, when the person runs `work ask` on the request, `work` shall write a question and commit the request.

### [g67] `work reply` writes the asker's answer
Restates: r21@0.29, r4@0.29.
- [r67] While a request is `awaiting-asker` and the request originates from this bounded context, when the person runs `work reply` on the request, `work` shall write an answer and commit the request.

### [g68] `work resolve` refuses a request that is not accepted
Restates: r10@0.29.
- [r68] While a request is not `accepted`, if the person runs `work resolve` on the request, then `work` shall refuse the command and name the status of the request.

### [g69] `work list` prints every request with its status and every observation no request or initiative cites
Restates: r50@0.29, r64@0.29.
- [r69] When the person runs `work list`, `work` shall print every request, the status of every request and every observation that no request and no initiative cite.

### [g70] `work show` on a request prints its status and its lines
Restates: work-queue#r59@0.29.
- [r70] When the person runs `work show` on a request, `work` shall print the status of the request and every request line proposed in the request.

### [g71] `work request` opens the request's issue
Restates: r12@0.29, r4@0.29, r44@0.29, r28@0.29.
- [r71] When the person runs `work request`, `work` shall post an issue, write a request whose status is `open` and commit the request.

### [g72] `work request` refuses an upstream with no GitHub repository
- [r72] If the person runs `work request` with the `--to` option set to a bounded context that has no GitHub repository, then `work` shall refuse the command and name the bounded context.

### [g73] `work offer` answers an ask with what may serve it
- [r73] While a request is `open`, when a session runs `work offer` on the request, `work` shall post a comment, set the status of the request to `awaiting-asker` and commit the request.

### [g74] `work fits` ends a request an offer serves
- [r74] While a request is `awaiting-asker`, when the person runs `work fits` on the request, `work` shall set the status of the request to `delivered`, write a resolution, post a comment, close the issue of the request and commit the request.

### [g75] `work propose` writes the asker's lines
- [r75] While a request is `awaiting-asker`, when the person runs `work propose` on the request, `work` shall write a request line and commit the request.

### [g76] `work sync` records what the other side posted
- [r76] While a comment on a request conforms to the comment form and the request does not hold the comment, when a session runs `work sync`, `work` shall write the comment and print every request.

### [g77] `work sync` acts on no comment that does not conform to the comment form
Restates: r58@0.29.
- [r77] While a comment on a request does not conform to the comment form, when a session runs `work sync`, `work` shall print the comment and not write the comment.

### [g78] `work turn` posts the asker's turn
Restates: r18@0.29, r7@0.29.
- [r78] While a request is `awaiting-asker`, when the person runs `work turn` on the request, `work` shall set the status of the request to `awaiting-upstream`, set the side of the request to `upstream` and post a comment.

### [g79] The upstream's turn ends with a line that has no outcome, posted
Restates: r17@0.29.
- [r79] While a request is `open` and a request line proposed in the request is not `accepted`, `refused` or `withdrawn`, when the person runs `work turn` on the request, `work` shall set the status of the request to `awaiting-asker` and post a comment.

### [g80] The upstream's turn ends with every line accepted, refused or withdrawn and one accepted, posted for the person to accept
Restates: r23@0.29, r8@0.29.
- [r80] While a request is `open` and a request line proposed in the request is `accepted` and every request line proposed in the request is one of `accepted`, `refused` or `withdrawn`, when the person runs `work turn` on the request, `work` shall post a comment and keep the side of the request.

### [g81] The upstream's turn ends with every line refused, and the issue closed
Restates: r9@0.29.
- [r81] While a request is `open` and a request line proposed in the request is `refused` and every request line proposed in the request is `refused`, when the person runs `work turn` on the request, `work` shall set the status of the request to `refused`, post a comment and close the issue of the request.

### [g82] A line that does not parse is not accepted
Restates: r2@0.29, r59@0.29.
- [r82] While a request line does not conform to the requirement grammar of this bounded context, if a session runs `work outcome accepted` on the request line, then `work` shall refuse the command and name the request line.

### [g83] `work accept` accepts a request and writes its item
- [r83] While a request is `open` and a request line proposed in the request is `accepted` and every request line proposed in the request is one of `accepted`, `refused` or `withdrawn`, when the person runs `work accept` on the request, `work` shall set the status of the request to `accepted`, write an item whose status is `shaped`, post a comment and commit the request.

### [g84] `work accept` refuses a request with a line that has no outcome
- [r84] While a request line proposed in a request is not `accepted`, `refused` or `withdrawn`, if the person runs `work accept` on the request, then `work` shall refuse the command and name the request line.

### [g85] `work resolve` posts the resolution and closes the issue
Restates: r10@0.29, r11@0.29, r12@0.29, r24@0.29.
- [r85] While a request is `accepted`, when the person runs `work resolve` on the request, `work` shall set the status of the request to `delivered`, write a resolution, set the side of the request to `asker`, post a comment, close the issue of the request and commit the request.

### [g86] `work watch` wakes on a comment that conforms to the comment form and that the request does not hold
- [r86] While a comment on a request conforms to the comment form and the request does not hold the comment, when a session runs `work watch`, `work` shall print the comment, exit successfully and not write the comment.

### [g87] `work watch` wakes on a new ask
- [r87] While an issue in the GitHub repository of this bounded context is `open` and the issue conforms to the comment form and no request has the issue, when a session runs `work watch`, `work` shall print the issue and exit successfully.

### [g88] `work request` opens no issue when its record is not committed
- [r88] While this repository rejects the commit, if the person runs `work request`, then `work` shall refuse the command, name this repository and not post an issue.

### [g89] `work turn` posts nothing when its record is not committed
- [r89] While this repository rejects the commit and a request is `open`, if the person runs `work turn` on the request, then `work` shall refuse the command, name this repository, not post a comment and not close the issue of the request.

### [g90] `work fits` posts nothing when its record is not committed
- [r90] While this repository rejects the commit and a request is `awaiting-asker`, if the person runs `work fits` on the request, then `work` shall refuse the command, name this repository, not post a comment and not close the issue of the request.

### [g91] `work reply` refuses a request this bounded context is asked
- [r91] While a request addresses this bounded context and the request does not originate from this bounded context, if the person runs `work reply` on the request, then `work` shall refuse the command and name the request.

### [g92] The upstream's `work turn` refuses the asker's turn
- [r92] While a request addresses this bounded context and the request does not originate from this bounded context and the request is `awaiting-asker`, if the person runs `work turn` on the request, then `work` shall refuse the command and name the request.

### [g93] The asker's `work turn` refuses the upstream's turn
- [r93] While a request originates from this bounded context and the request does not address this bounded context and the request is `open`, if the person runs `work turn` on the request, then `work` shall refuse the command and name the request.

### [g94] The asker's `work turn` refuses a turn it has passed
- [r94] While a request originates from this bounded context and the request does not address this bounded context and the request is `awaiting-upstream`, if the person runs `work turn` on the request, then `work` shall refuse the command and name the request.

### [g95] `work sync` writes no entry of the upstream's part that the asker posted
- [r95] While a comment on a request conforms to the comment form and the side of the comment is `asker` and the comment holds an entry whose side is `upstream` and the request does not hold the comment, when a session runs `work sync`, `work` shall write the comment and not write the entry.

### [g96] `work sync` reopens no request that is `delivered`, `refused` or `withdrawn`
- [r96] While a request is one of `delivered`, `refused` or `withdrawn` and a comment on the request conforms to the comment form and the request does not hold the comment, when a session runs `work sync`, `work` shall write the comment and keep the status of the request and the side of the request.

### [g97] The SessionStart hook names a request awaiting the upstream that this bounded context asked
- [r97] While a request originates from this bounded context and the request does not address this bounded context and the request is `awaiting-upstream`, when the SessionStart hook runs `work watch` with the `--hook` option, `work` shall print the request.

### [g98] The SessionStart hook names a request awaiting the asker that this bounded context is asked
- [r98] While a request addresses this bounded context and the request does not originate from this bounded context and the request is `awaiting-asker`, when the SessionStart hook runs `work watch` with the `--hook` option, `work` shall print the request.

### [g99] The SessionStart hook is silent with no request waiting on the other side
- [r99] While no request that originates from this bounded context is `awaiting-upstream` and no request that addresses this bounded context is `awaiting-asker`, when the SessionStart hook runs `work watch` with the `--hook` option, `work` shall exit successfully and not print a request.

### [g100] `work watch --forward` wakes on a comment that conforms to the comment form and that the request does not hold
- [r100] While a comment on a request conforms to the comment form and the request does not hold the comment, when a session runs `work watch` with the `--forward` option, `work` shall print the comment, exit successfully and not write the comment.

### [g101] `work watch --forward` wakes on a new ask
- [r101] While an issue in the GitHub repository of this bounded context is `open` and the issue conforms to the comment form and no request has the issue, when a session runs `work watch` with the `--forward` option, `work` shall print the issue and exit successfully.

### [g102] `work request` to an upstream refuses an observation beside a request it is raised for
Restates: r30@0.29.
- [r102] While this bounded context holds an upstream entry, if the person runs `work request` with the `--source` and `--raised-for` options, then `work` shall refuse the command and name `--source`.

### [g103] `work sync` writes no entry of the asker's part that the upstream posted
- [r103] While a comment on a request conforms to the comment form and the side of the comment is `upstream` and the comment holds an entry whose side is `asker` and the request does not hold the comment, when a session runs `work sync`, `work` shall write the comment and not write the entry.

## Implementation, may change
- A request between two bounded contexts, each in its own git repository, is one conversation on one GitHub issue on
  the upstream's GitHub repository; nothing reads or writes the other side's git repository. Each step is a comment a
  `work` command posts through `gh` (`$SHOPSYSTEM_WORK_GH`, else `gh`), and each side keeps its own record of the
  conversation as `.shop/requests/q<n>.md`, its number one above the highest of `.shop/requests/` and the frozen
  `.shop/work/requests/`, the two sides' numbers apart and linked by the issue's URL. A context's own request is an
  issue on its own GitHub repository, its asker and its upstream the same context. How a request is kept is `work`'s
  own (design-decision/requests-written-through-work).
- Where the issue lives: an upstream's bullet under `## Upstreams` in `spec/index.md` names its GitHub repository,
  `github: <owner>/<name>` (an upstream with none has no GitHub repository, r72); a context's own repository is read off its git
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
  block that does not parse, does not conform to the comment form. The side of a comment is the side
  that posted its step (the asker of an `ask` or a `fits`, the upstream of an `offer`, an `accept` or a `resolve`, and of
  a `turn` the side whose turn the request was); the side of an entry is the side whose part holds it (the asker's
  `line` and `answer`, the upstream's `question`, `outcome`, `counter`, `reason`, `into` and `resolution`).
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
  only the part of the side that posted its step (r95, r103): its entries written into their sections by number, its
  status and turn set, an offer quoted under `## Offer`. The poster is the asker of an `ask` or a `fits`, the
  upstream of an `offer`, an `accept` or a `resolve`, and of a `turn` the side whose turn the request was; an entry
  of the other side's part is recorded with its comment, so no watch wakes on it again, and never applied. A comment on a request
  that is `delivered`, `refused` or `withdrawn` sets neither its status nor its turn (r96), so a late comment reopens no request. A comment that does not conform to the comment form is printed and never
  recorded. The records changed are one commit, on the current branch; then every request is printed with its status
  and, unless it is `delivered`, `refused` or `withdrawn`, whose move it waits on.
- `work watch [--every <seconds>] [--polls <n>]` polls GitHub every `--every` seconds (default 60), as `work sync`
  reads it: the issue of each request not `delivered`, `refused` or `withdrawn`, and the open issues of this context's
  own repository. After the first poll that finds a comment a request does not hold or an `ask` no record holds, it
  prints one line for each and exits successfully, so a session runs it in the background and is woken when it ends;
  the session then runs `work sync` and starts the watch again. A comment that conforms to the comment form and an open issue that no request has are printed by
  every watch that finds them, until `work sync` records or takes them in (r86, r87). A comment that does not
  conform, which `work sync` prints and never records (r77), is printed by one watch only and passed over by later ones, so it does
  not wake a session in a loop; r86's condition leaves it out: its URL is kept in `<git dir>/shopsystem/watched.json`, the file holding only comments that do not conform, never
  committed. A poll whose `gh` fails is said on stderr and tried again at the next. `--polls <n>` makes a bounded
  watch, used by the tests: it stops after n polls that found nothing and exits 1, so a caller tells "nothing new"
  from a wake. `work watch` writes nothing in the repository and commits nothing.
- `work watch --forward [--every <seconds>] [--polls <n>]` waits on GitHub's events instead of polling the issues
  (r100, r101). It watches this context's own repository and the repository of each request's issue not `delivered`,
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
- `work watch --hook` is the requests' SessionStart hook (r97-r99): it prints each request that waits on the other
  side, one that originates from this context and does not address it and is `awaiting-upstream`, or one that
  addresses this context and does not originate from it and is `awaiting-asker`, one line each as
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
