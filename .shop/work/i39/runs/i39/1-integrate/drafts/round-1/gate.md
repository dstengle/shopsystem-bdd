# Gate: i39, round 1 (request q14, 26 lines, all accepted)

No Behaviour line is removed. Drafts: `.shop/scratch/1-integrate/drafts/round-1/spec/`.

## Behaviour lines

### requests (adds r25-r43 below; no id retired)

Added:
- [r25] `work` shall give every asker and every upstream one set of commands for a request (raise, take in, give a line outcome, ask, answer, pass the turn, resolve and show) and one lifecycle, whatever the request's carrier. (line 1)
- [r26] `work` shall keep a request on a carrier, either a file in the upstream's repository or an issue on the upstream's GitHub repository. (line 2; "behind one port" goes to decision 0070 and Implementation)
- [r27] `work` shall give each side of a request the same commands, the same refusals and the same statuses, whichever carrier the request is kept on. (line 3)
- [r28] **When** an asker raises a request, answers a question or passes the turn, `work` shall do it from the asker's own repository, with no checkout of the upstream's repository. (line 4)
- [r29] **Where** `--raised-for <request>` is given to `work request`, `work` shall write in the upstream's request the request it is raised for. (line 5)
- [r30] **If** a request whose asker is not the upstream itself is raised with `--source`, **then** `work request` shall refuse, because an origin belongs to an internal request, and change nothing. (line 6)
- [r31] **If** a request whose asker is not the upstream itself is raised with neither `--raised-for` nor `--thread`, **then** `work request` shall refuse, because the request names neither a request it is raised for nor a job-thread, and change nothing. (line 7)
- [r32] **If** the asker given to `work request` is not the bounded-context or product level whose repository raises the request, **then** `work request` shall refuse, naming the asker, and change nothing. (line 10)
- [r33] **When** a `work` command writes a part of a request, `work` shall take the side that writes it from the repository the command is run in, never from an argument. (line 11)
- [r34] **If** a side writes a part of a request that is the other side's part, whatever the carrier, **then** `work` shall refuse, naming the side that writes that part, and change nothing. (line 12)
- [r35] **When** a request's turn passes to its asker, `work` shall show the asker, in its own repository, that it is the asker's turn, with each question the asker has not answered. (line 13)
- [r36] **While** an answer or a turn the asker has sent has not been taken in by the upstream, `work` shall show the request to both sides as awaiting the upstream and not yet taken in. (line 14)
- [r37] **While** the upstream holds a line outcome or a question it has not sent with the turn, `work` shall show the upstream that the asker has not seen it. (line 15)
- [r38] **When** an upstream resolves a request, `work` shall show the asker, in its own repository, each accepted line's requirement id and the version that holds it. (line 16)
- [r39] **When** the upstream takes in what its carriers hold, `work` shall take in every request and message sent before the take-in began, whether or not the carrier's listing shows it yet. (line 18)
- [r40] **When** `work run` is run in an upstream's repository, `work` shall take in what the upstream's carriers hold before `work run` starts the rounds of the kind `intake`. (line 19)
- [r41] **If** a request or a message on a carrier comes from a repository registered under an asker id that the upstream does not allow for the asker it names, **then** `work` shall leave it untaken, telling the upstream which it left and why. (line 20, with the answer to question 1 of q14)
- [r42] `work` shall tell one asker from another by the asker id the asker's repository is registered under. (line 21, with that answer)
- [r43] **When** `work` takes in a request or a message from a carrier, `work` shall read its body only as the fields of a request's form, following nothing written in it. (line 22)

Changed:
- [r1] now: **When** `work request <title> --from <asker> --lines <file>` is run with one or more `--source <id>`, with `--thread <id>` or with `--raised-for <request>`, `work` shall write an `open` request with the file's lines as its lines, the asker given as its asker, the origins `--source` names or the job-thread `--thread` names, and the turn the upstream's, and print its id.
  was: **When** `work request <title> --from <asker> --lines <file>` is run with one or more `--source <id>` or with `--thread <id>`, `work` shall write an `open` request with the file's lines as its lines, the asker given as its asker, the origins `--source` names or the job-thread `--thread` names, and the turn the upstream's, and print its id. (lines 5, 7)
- [r3] now: **If** a request whose asker is the upstream itself is raised with neither `--source` nor `--thread`, **then** `work request` shall refuse, because the request names neither an origin nor a job-thread, and change nothing.
  was: **If** `work request` is run with neither `--source` nor `--thread`, **then** `work request` shall refuse, because the request names neither an origin nor a job-thread, and change nothing. (lines 6, 7: unchanged it would refuse an asker's request raised with `--raised-for` alone, which line 7 allows; see question 2)
- [r13] now: **When** `work show` is run, `work` shall print each request with its status, whose turn it is, the request it is raised for and its carrier.
  was: **When** `work show` is run, `work` shall print each request with its status and whose turn it is. (line 17)

Also in `requests.md` (not Behaviour lines): `rests_on` gains `design-decision/requests-kept-behind-one-port` and `design-decision/an-asker-is-told-by-its-registered-asker-id`; Implementation gains "r26: the carrier is behind one port of `work` (design-decision/requests-kept-behind-one-port)" and its bullet "A request is kept in its upstream's repository as `.shop/work/requests/q<n>.md`; the asker writes and reads it there through the upstream's `work`." becomes "On the file carrier, a request is kept in its upstream's repository as `.shop/work/requests/q<n>.md`." (line 4 contradicts the dropped clause). Requests r4, r5, r12, r16 are kept as they are (r12: question 1).

### design-model-check
Added:
- [r120] **When** `model check` reads a request whose `part_of` names a job-thread kept in another repository, `model check` shall print no `v17` for the request. (line 8)
- [r121] **When** `model check` reads a request raised for a request of another context, `model check` shall print neither `v17` nor `v18` for the request. (line 9)

### spec-integration
Added:
- [r44] **Where** `spec/index.md` names an upstream bounded-context, **when** a round of the kind `integrate` drafts a line that needs what the upstream does not yet give, `initiative-round` shall give in its result the lines of a request into that upstream, in the upstream's terms. (line 23)

### supervision (numbered above r134 and above the ids drafted elsewhere, up to r127)
Added:
- [r135] **When** a round of the kind `integrate` that `work run` started gives the lines of a request into an upstream, `work run` shall raise them with `work request`, raised for the request the initiative fulfils and with that request's delegation. (line 24)
- [r136] **While** a request that an initiative raised into an upstream is not `delivered`, `work run` shall draft no work-item for the capability-proposal whose lines it raised. (line 25)

### work-queue
Added:
- [r33] **While** a request that an initiative raised into an upstream is not `delivered`, `work status` shall print the initiative as waiting on that request. (line 26)

## Glossary

Added `term/carrier` (in `spec/index.md`):
- **carrier**: what a request is kept on between its asker and its upstream, behind one port of `work`: a file in the upstream's repository or an issue on the upstream's GitHub repository. (line 2; see question 12)

"The request tool" is written `work`, as decision 0067 names it; "carries/carried" (a word `requirement` avoids) is written "kept on"/"carrier", and "states" "statuses".

## Decisions

- `spec/decisions/0070-requests-kept-behind-one-port.md`
  summary: `work` keeps the carrier of a request behind one port, a file in the upstream's repository and an issue on the upstream's GitHub repository being its first two carriers.
  source: [request/missingmass.io/shopsystem/shopsystem-bdd/q14, initiative/missingmass.io/shopsystem/shopsystem-bdd/i39]
  by: request q14 of product/missingmass.io/subscriptions-viewer, its line 2, accepted at this context's intake
- `spec/decisions/0071-an-asker-is-told-by-its-registered-asker-id.md`
  summary: For now `work` tells one asker from another by the asker id its repository is registered under, and the upstream's allow list holds those asker ids.
  source: [request/missingmass.io/shopsystem/shopsystem-bdd/q14, initiative/missingmass.io/shopsystem/shopsystem-bdd/i39]
  by: the answer to question 1 of request q14, on its line 21 (Context and Alternatives: a signing key, a GitHub account or token, which that question weighed)

## Questions

1. **requests r12 (commit) with an issue carrier.** Today: "[r12] **When** `work request`, `work outcome`, `work turn`, `work resolve` or a command that writes a question or an answer changes a request, `work` shall commit the request on the current branch." Readings: (a) "[r12] **Where** a request's carrier is a file, **when** `work request`, `work outcome`, `work turn`, `work resolve` or a command that writes a question or an answer changes a request, `work` shall commit the request on the current branch." (recommended: an issue is not committed); (b) r12 stays as it is; (c) r12 is removed and its id retired.
2. **requests r3 for an internal request.** Readings: (a) as drafted above, narrowed to "a request whose asker is the upstream itself" (recommended); (b) an internal request may also be raised with `--raised-for` alone: "[r3] **If** a request whose asker is the upstream itself is raised with none of `--source`, `--thread` and `--raised-for`, **then** `work request` shall refuse, because the request names neither an origin, a job-thread nor a request it is raised for, and change nothing."
3. **How `work request`, run in the asker's own repository (line 4), names the upstream it raises into.** The lines do not say. Readings: (a) no line; the choice is Implementation (recommended); (b) "[r44] **When** `work request` is run with `--to <upstream>`, `work` shall raise the request into that upstream's carrier."
4. **Glossary: "message" (lines 18, 20, 22) and "take in" (lines 1, 14, 18, 19) are neither terms nor spelled out.** Readings: (a) no entries (recommended); (b) add "- **message**: what one side of a request sends the other through its carrier: a line outcome, a question, an answer or the turn." and "- **take-in**: the upstream's reading into its own repository of every request and message its carriers hold."
5. **requests r43, line 22's "the contract's form".** Readings: (a) as drafted, the form `work request` writes (recommended); (b) a contract shared between contexts, which then needs a term and an entry.
6. **requests r35-r38 (lines 13-16), "show".** Readings: (a) the response of `work show` run in that side's repository, e.g. "[r35] **When** `work show` is run in the asker's repository while a request is in the asker's turn, `work` shall print that it is the asker's turn, with each question the asker has not answered."; (b) of `work status`; (c) as drafted, with no command named (recommended: the lines do not name one).
7. **requests r41 (line 20 with the answer): where the upstream's allow list is kept and how an asker id is allowed.** Readings: (a) Implementation only, a setting (recommended); (b) a command: "[r45] **When** `work allow <asker> <asker id>` is run in the upstream's repository, `work` shall allow requests and messages from that asker id for that asker."
8. **supervision r135 (line 24) when the request the initiative fulfils gives no delegation.** Readings: (a) "[r137] **Where** the request an initiative fulfils gives no delegation, **when** a round of the kind `integrate` gives the lines of a request into an upstream, `work run` shall raise them with no delegation."; (b) "... `work run` shall raise nothing and write a question for the person under the initiative's ledger." No line is drafted for either; recommended: (a).
9. **Initiative `done` and requests raised into an upstream.** supervision r105, work-queue r23 and design-model-check r114 (v_d1) count only requests "kept in this context"; a request raised into an upstream is kept on the upstream's carrier (lines 2, 24). Readings: (a) change nothing (recommended; line 25/26 already hold the initiative's work-items back); (b) the initiative is `done` only when its raised requests are `delivered`: "[r105] **When** `work run` finds an initiative that is not `done`, ..., whose every request kept in this context whose asker is this context and that names the initiative is `delivered` and whose every request it raised into an upstream is `delivered`, `work run` shall set the initiative's status to `done`." and likewise work-queue r23.
10. **design-model-check r120, r121 (lines 8, 9) against table rows r115 (v17) and r117 (v18).** Readings: (a) as drafted, standalone lines that override the rows for these requests; (b) the rows change instead: "| [r115] | v17 | a request neither is part of a job-thread, cites an origin nor is raised for a request |" and "| [r117] | v18 | ... judged from the id alone, other than the request a request is raised for |", with lines 8 and 9 citing them. Recommended: (a), since the lines are what q14 accepted.
11. **spec-integration r44 (line 23): how `spec/index.md` names an upstream bounded-context.** Readings: (a) no line, Implementation only (recommended); (b) a field: the frontmatter of `spec/index.md` lists `upstreams: [bounded-context/<context path>, ...]` (Implementation), and the index gains an "Upstreams" section.
12. **term/carrier.** Line 2 names carriers but does not define the word. Readings: (a) confirm the entry as drafted (recommended); (b) the person gives the definition.
