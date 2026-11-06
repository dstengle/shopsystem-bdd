---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/intake
title: Intake
narrator: a session answering a peer bounded context's request
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [r1, r2, r3, r4, r5]
unbuilt: []
---

# Intake

## Purpose
Work from outside the bounded context comes in by a negotiation with another system, not with a person (design goal
4). A peer bounded context, the product or this context itself asks on a request's issue; a session of this context
offers what may serve and answers each line proposed: accept it into a capability, refuse it with a reason, or
counter-propose. The exchange repeats until the lines are settled, with no person in the loop unless the two sides
cannot agree; the person accepts the request, which becomes an item. The brainstorming route is the `brainstorming`
capability's.

## Behaviour

### [g6] An item with a request line that is not settled is not readied
- [r6] While an item is `shaped` and a request line of the item is not settled, if a session runs `work ready` on the
  item, then `work` shall exit with an error naming the request line and change nothing.

### [g7] A counter-proposal passes the turn to the asker, posted
- [r7] When a session runs `work outcome rewritten` on a request line proposed in a request, `work` shall set the line outcome of the request line to `rewritten`, write a request line, change the side of the request and post a comment.

### [g8] `work outcome refused` writes the reason
- [r8] When a session runs `work outcome refused` on a request line proposed in a request, `work` shall set the line outcome of the request line to `refused`, write a reason and commit the request.

### [g9] `work outcome refused` refuses a refusal with no reason
- [r9] While the argument `--reason` is absent, if a session runs `work outcome refused` on a request line, then `work` shall exit with an error naming the argument `--reason`.

## Implementation, may change
- A request asked of this context is a conversation on one GitHub issue on this context's own repository (the
  requests capability); `work sync` writes it as a record here, and this context's session answers it there.
- `work outcome <request> <n> <word>` (the upstream, in its own turn) writes line n's line outcome, and refuses a
  word that is not a `line outcome`: `accepted --into <capability> [--group g<n>|<title>]` parses the line in this
  context's grammar (requests r38) and writes `<n>. <capability> [<group>]` under the request's `## Into`, the
  capability the person approves with the line when they accept the request; `refused` takes `--reason`;
  `rewritten --line <text>` checks the counter-proposal in the context's grammar, appends it to the request's
  `## Lines` as line m, writes `<n>. <m>` under the request's `## Counter-proposals`, passes the turn to the asker
  (`awaiting-asker`) by the one turn rule `work turn` follows, and posts the turn on the issue.
- A session's `accepted` is a proposal of acceptance; no item is written before the person's `work accept`
  (requests r39), which writes the `shaped` item with `request: q<n>` and `asked_by: <the request's asker>`, its
  provenance read off the asker (this context's own asker: `own`; a `product/` id: `product`; any other: `peer`).
- The request lines of an item are the lines of its request whose line outcome is not `rewritten`: a rewritten line is
  no longer the item's, its counter-proposal is. So every request line of the item is settled once each is `accepted`,
  `refused` or `withdrawn`.
- A reason (`--reason`, or `rewritten as line <m>`) is written under the request's `## Reasons` as `<n>. <text>`, a
  section `model check` accepts.

## Not yet
- The intake session started by `work backlog` (design: "a session started when the backlog command runs intake"):
  `work` starts no session (workflow simplification plan 4, D2). The batch session catches up first: the first step
  of the skill `building-a-batch` runs `work sync` and follows `taking-in-a-request` for each request in this
  context's turn, and any session may run that skill on its own.
