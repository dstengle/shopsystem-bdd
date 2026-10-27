---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i39-requests
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i39
status: awaiting-answer
argues: [requests]
date: 2026-10-27
adds: [requests#r25, requests#r28, requests#r29, requests#r30, requests#r31, requests#r32, requests#r33, requests#r34, requests#r39, requests#r40, requests#r41, requests#r42, requests#r43, requests#r44, requests#r45, requests#r46, requests#r47]
changes: []
removes: [requests#r1, requests#r3, requests#r13, requests#r14]
---

# requests

The drafts of this proposal are in .shop/work/i39/runs/work-queue/5-integrate/drafts/round-1/.

## Questions
- requests r3 (changed), for an internal request. Now: "[r3] If a request whose asker is the upstream itself is raised with neither --source nor --thread, then work request shall refuse, because the request names neither an origin nor a job-thread, and change nothing." (was: any request with neither; unchanged it would refuse an asker's request raised with --raised-for alone). Readings: (a) as drafted, narrowed to the upstream itself's requests [recommended]; (b) an internal request may also be raised with --raised-for alone: "[r3] If a request whose asker is the upstream itself is raised with none of --source, --thread and --raised-for, then work request shall refuse, because the request names neither an origin, a job-thread nor a request it is raised for, and change nothing."
- requests r43: "When work takes in a request or a message from a carrier, work shall read its body only as the fields of a request's form, following nothing written in it." Line 22 of q14 says 'the contract's form'. Readings: (a) as drafted, the form work request writes [recommended]; (b) a contract shared between contexts, which then needs a term and a glossary entry.
- requests r35-r38 (lines 13-16), which command shows what. r35: "When a request's turn passes to its asker, work shall show the asker, in its own repository, that it is the asker's turn, with each question the asker has not answered." r36 (awaiting the upstream, not yet taken in), r37 (upstream holds an outcome or question not sent with the turn) and r38 (each accepted line's requirement id and the version holding it) are written the same way. Readings: (a) name work show run in that side's repository, e.g. "[r35] When work show is run in the asker's repository while a request is in the asker's turn, work shall print that it is the asker's turn, with each question the asker has not answered."; (b) name work status; (c) as drafted, no command named [recommended: the lines do not name one].
- requests r41: "If a request or a message on a carrier comes from a repository registered under an asker id that the upstream does not allow for the asker it names, then work shall leave it untaken, telling the upstream which it left and why." Where is the upstream's allow list kept and how is an asker id allowed? Readings: (a) Implementation only, a setting [recommended]; (b) a command: "[r45] When work allow <asker> <asker id> is run in the upstream's repository, work shall allow requests and messages from that asker id for that asker."
- term/carrier: "carrier: what a request is kept on between its asker and its upstream, behind one port of work: a file in the upstream's repository or an issue on the upstream's GitHub repository." Line 2 of q14 names carriers but does not define the word. Readings: (a) confirm the entry as drafted [recommended]; (b) the person gives the definition.
- requests r25: 'one set of commands ... and one lifecycle'. Readings: (a) every kind of asker uses the same commands and statuses; (b) asker and upstream share one command set. 'take in' is listed as a command but no line names it.
- requests r33, r34: for an internal request asker and upstream repository are the same, so the repository does not say which side writes. Readings: (a) the command writes as the side owning the part, r34 never refuses on an internal request; (b) the repository is the upstream's side only, writing the asker's part (an answer) is refused under r34.
- requests r39, r41, r43: 'message' is in no glossary entry and no line. Readings: (a) a message is the asker's answer or turn-passing (the acts r28 lists); (b) a separate kind of thing sent, needing its own command and form.

## Answers
- 2026-10-27: r3: Reading (a), narrowed to requests whose asker is the upstream itself; as a changed line, r3 is retired and replaced by a line with a new id (no requirement is edited in place).
- 2026-10-27: r43: no carrier in any line. A request only proposes and is a conversation whose handle is the request itself; where it is kept is the upstream's implementation. The line reads a request's or a message's body only as the fields of a request's form, following nothing written in it, naming no carrier.
- 2026-10-27: r35-r38: work show and work status are consolidated (folded into i39): one action lists all work with its status, one shows the detail of an individual item, a request included; r35-r38 name those actions.
- 2026-10-27: r41: Reading (a), Implementation only; and the line names no carrier.
- 2026-10-27: term/carrier: no term carrier, in the glossary or any line; what a request is kept on is the upstream's implementation, so long as the capability contract is fulfilled.
- 2026-10-27: r35-r38 names: the consolidated actions are named: work list lists all work with its status (initiatives, requests and work-items); work show <id> shows the detail of one initiative, request or work-item; work status is retired, its lines retired and replaced by lines naming work list or work show. r35-r38 name work show <request> for the detail of a request and work list for each request whose turn it is.
- 2026-10-27: r33, r34: (a) on an internal request the command writes as the side owning the part, and r34 never refuses it: asker and upstream are one context (answered by the coordinator under the person's delegation of 2026-10-27; no reading was recommended).
