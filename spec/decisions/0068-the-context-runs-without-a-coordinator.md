---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-context-runs-without-a-coordinator
summary: "No session coordinates a bounded context: `work run` takes every open initiative's nodes through their transitions, starting the rounds that integrate, gate, apply and formulate its capability-proposals, drafting the work-items and starting the analysis, and the person works through `work status`, `work answer`, `work note`, `work turn` and `work run`."
date: 2026-10-23
status: proposed
supersedes: [design-decision/the-session-keeps-the-gate]
source: [observation/2026-10-23-decision-0030-misread, observation/2026-10-21-session-keeps-the-gate, design-decision/the-session-keeps-the-gate, design-decision/a-script-supervises-delivery, design-decision/the-ledger-is-tracked]
by: "the person, 2026-10-23, approving the design note 2026-10-23-requests-and-the-context-loop-design, R5; the answers of 2026-10-24 to R5's gate, given by the coordinator under the person's delegation of 2026-10-24 (\"Please get everying delivered. Do not stop to ask me questions or permission.\"); the i22 analysis (.shop/records/2026-10-23-i22-analysis.md), candidates 2 and 3 (hand merges and work with no task review)"
---

# 0068. The context runs without a coordinator

## Decision

No session coordinates a bounded context. `work run` takes every initiative that is neither `done` nor `abandoned`
through every transition its nodes can make: it starts the `intake` round of a request this context is the upstream
of and the `integrate` round of a `proposed` initiative, starts the `gate` round that writes each `drafted`
capability-proposal's gate as questions on the proposal, starts the `apply` and `formulate` rounds once they are
answered, drafts the work-items of a `formulated` proposal and of a branch review's fix-now findings, delivers them,
and starts `measure initiative` and the analysis when the initiative's work is done. Where the request an initiative
fulfils gives a delegation, a question the delegation covers is answered by a session given the delegation, and the
answer names it. The person's surface is `work status`, `work answer`, `work note`, `work turn` and `work run`. No
skill tells a session to write spec or feature files itself (the small-change paths go), skills lose their "If the
person is talking to you" sections, and starting `claude -p` sessions or merging branches by hand is not a practice:
a tool `work run` disallows and a change `work run` cannot deliver are put to the person as questions. This replaces
design-decision/the-session-keeps-the-gate, whose ledger sentence design-decision/the-ledger-is-tracked already
replaced; its trial-runner, and its rule that a new scenario or examples row a fix needs is written by the
`feature-formulator` in a `formulate` round, stand. It also replaces design-decision/a-script-supervises-delivery's
sentence on the session that drafts the work-items and starts `work run`; the rest of that decision stands.
