---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/requests
title: Requests
narrator: a context taking in or raising a request
group: service
language: codified-2
rests_on: [design-decision/requests-written-through-work, design-decision/exits-are-successful-or-errors, design-decision/an-asker-is-told-by-its-registered-asker-id]
retired: [r1, r3, r4, r5, r10, r11, r12, r13, r19, r20, r21, r22, r23, r42, g42, g2, r2, g6, r6, g7, r7, g8, r8, g9, r9, g14, r14, g15, r15, g16, r16, g17, r17, g18, r18, g24, r24, g25, r25, g26, r26, g27, r27, g28, r28, g29, r29, g30, r30, g31, r31, g32, r32, g33, r33, g34, r34, g35, r35, g36, r36, g37, r37, g38, r38, g39, r39, g40, r40, g41, r41, g44, r44, g43, r43, g45, r45, g46, r46, g47, r47, g49, r49, g50, r50, g51, r51, g48, r48, g52, r52, g53, r53, g54, r54, g55, r55, g56, r56, g57, r57, g58, r58, g77, r77, g59, r59, g60, r60, g61, r61, g62, r62, g63, r63, g64, r64, g65, r65, g66, r66, g67, r67, g68, r68, g69, r69, g70, r70, g71, r71, g72, r72, g73, r73, g74, r74, g75, r75, g76, r76, g78, r78, g79, r79, g80, r80, g81, r81, g82, r82, g83, r83, g84, r84, g85, r85, g86, r86, g87, r87, g88, r88, g89, r89, g90, r90, g91, r91, g92, r92, g93, r93, g94, r94, g95, r95, g96, r96, g97, r97, g98, r98, g99, r99, g100, r100, g101, r101, g102, r102, g103, r103, g104, r104, g105, r105, g106, r106, g107, r107, g108, r108, g109, r109, g110, r110, g111, r111, g112, r112, g114, r113, g115, r114, g113, r115]
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

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

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
- `work request <title> [--from <asker>] [--ask <words>] [--to <upstream>]` with `--source <id>`, `--thread <id>` or
  `--raised-for <request>` opens the issue, its body the `ask` form, and writes the record open in the upstream's
  turn; it prints the request's id and the issue's URL. `--from` defaults to this context (r111). `--to` defaults to the one upstream of a request to an
  upstream (no `--source`), else this context.
- `work offer <request> [--capability <c>]... [--note <words>]` (the upstream, on an open request) posts the note,
  each named capability's groups (each title over its requirements; no frontmatter, prose or given blocks) and, of the
  imported packs, the glossary and the capabilities' `## Terms`, only the entries those requirements mention, and
  passes the turn to the asker. `work
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
  that is `delivered`, `refused` or `withdrawn` sets neither its status nor its turn (r96), so a late comment reopens no request. A comment that does not conform to the comment form is printed once
  and recorded under `## Comments` marked `unreadable`, nothing of it applied (r105, r106). The records changed are one commit, on the current branch; then every request is printed with its status
  and, unless it is `delivered`, `refused` or `withdrawn`, whose move it waits on.
- `work watch [--every <seconds>] [--polls <n>]` polls GitHub every `--every` seconds (default 60), as `work sync`
  reads it: the issue of each request not `delivered`, `refused` or `withdrawn`, and the open issues of this context's
  own repository. After the first poll that finds a comment a request does not hold or an `ask` no record holds, it
  prints one line for each and exits successfully, so a session runs it in the background and is woken when it ends;
  the session then runs `work sync` and starts the watch again. A comment that conforms to the comment form and an open issue that no request has are printed by
  every watch that finds them, until `work sync` records or takes them in (r86, r87). A comment that does not
  conform, which `work sync` prints once and records with nothing of it applied (r105), is printed by one watch only and passed over by later ones, so it does
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
- r19@0.29: retired with requests#r3 in 0.31.0 (the-old-workflow-retired).
- r22@0.29: retired with requests#r4 in 0.31.0 (the-old-workflow-retired).
- r65@0.29: retired with requests#r10 in 0.31.0 (the-old-workflow-retired).
- r66@0.29: retired with requests#r10 in 0.31.0 (the-old-workflow-retired).
- r67@0.29: retired with requests#r12 in 0.31.0 (the-old-workflow-retired).
- r68@0.29: retired with requests#r13 in 0.31.0 (the-old-workflow-retired).
- r70@0.29: retired with requests#r11 in 0.31.0 (the-old-workflow-retired).
- r71@0.29: retired with requests#r10 in 0.31.0 (the-old-workflow-retired).
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g59 | context-requests#g4 |
| r59 | context-requests#r4 |
| g60 | context-requests#g5 |
| r60 | context-requests#r5 |
| g61 | context-requests#g6 |
| r61 | context-requests#r6 |
| g62 | context-requests#g7 |
| r62 | context-requests#r7 |
| g63 | context-requests#g8 |
| r63 | context-requests#r8 |
| g64 | context-requests#g9 |
| r64 | context-requests#r9 |
| g65 | context-requests#g10 |
| r65 | context-requests#r10 |
| g66 | context-requests#g11 |
| r66 | context-requests#r11 |
| g67 | context-requests#g12 |
| r67 | context-requests#r12 |
| g68 | context-requests#g13 |
| r68 | context-requests#r13 |
| g69 | context-requests#g14 |
| r69 | context-requests#r14 |
| g70 | context-requests#g15 |
| r70 | context-requests#r15 |
| g71 | context-requests#g16 |
| r71 | context-requests#r16 |
| g72 | context-requests#g17 |
| r72 | context-requests#r17 |
| g73 | context-requests#g18 |
| r73 | context-requests#r18 |
| g74 | context-requests#g19 |
| r74 | context-requests#r19 |
| g75 | context-requests#g20 |
| r75 | context-requests#r20 |
| g76 | context-requests#g21 |
| r76 | context-requests#r21 |
| g78 | context-requests#g22 |
| r78 | context-requests#r22 |
| g79 | context-requests#g23 |
| r79 | context-requests#r23 |
| g80 | context-requests#g24 |
| r80 | context-requests#r24 |
| g81 | context-requests#g25 |
| r81 | context-requests#r25 |
| g82 | context-requests#g26 |
| r82 | context-requests#r26 |
| g83 | context-requests#g27 |
| r83 | context-requests#r27 |
| g84 | context-requests#g28 |
| r84 | context-requests#r28 |
| g85 | context-requests#g29 |
| r85 | context-requests#r29 |
| g86 | request-watch#g1 |
| r86 | request-watch#r1 |
| g87 | request-watch#g2 |
| r87 | request-watch#r2 |
| g88 | context-requests#g30 |
| r88 | context-requests#r30 |
| g89 | context-requests#g31 |
| r89 | context-requests#r31 |
| g90 | context-requests#g32 |
| r90 | context-requests#r32 |
| g91 | context-requests#g33 |
| r91 | context-requests#r33 |
| g92 | context-requests#g34 |
| r92 | context-requests#r34 |
| g93 | context-requests#g35 |
| r93 | context-requests#r35 |
| g94 | context-requests#g36 |
| r94 | context-requests#r36 |
| g95 | context-requests#g37 |
| r95 | context-requests#r37 |
| g96 | context-requests#g38 |
| r96 | context-requests#r38 |
| g97 | request-watch#g3 |
| r97 | request-watch#r3 |
| g98 | request-watch#g4 |
| r98 | request-watch#r4 |
| g99 | request-watch#g5 |
| r99 | request-watch#r5 |
| g100 | dropped |
| r100 | dropped |
| g101 | dropped |
| r101 | dropped |
| g102 | context-requests#g39 |
| r102 | context-requests#r39 |
| g103 | context-requests#g40 |
| r103 | context-requests#r40 |
| g104 | context-requests#g41 |
| r104 | context-requests#r41 |
| g105 | request-watch#g6 |
| r105 | request-watch#r6 |
| g106 | request-watch#g7 |
| r106 | request-watch#r7 |
| g107 | context-requests#g42 |
| r107 | context-requests#r42 |
| g108 | context-requests#g43 |
| r108 | context-requests#r43 |
| g109 | context-requests#g44 |
| r109 | context-requests#r44 |
| g110 | context-requests#g45 |
| r110 | context-requests#r45 |
| g111 | context-requests#g46 |
| r111 | context-requests#r46 |
| g112 | context-requests#g47 |
| r112 | context-requests#r47 |
| g114 | context-requests#g48 |
| r113 | context-requests#r48 |
| g115 | context-requests#g49 |
| r114 | context-requests#r49 |
| g113 | context-requests#g50 |
| r115 | context-requests#r50 |
