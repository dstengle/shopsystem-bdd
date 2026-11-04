---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/intake
title: Intake
narrator: a session answering a peer bounded context's request
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: []
---

# Intake

## Purpose
Work from outside the bounded context comes in by a negotiation with another system, not with a person (design goal
4). A peer bounded context or the product proposes lines; a session of this context, started by intake, answers each
one: accept, refuse with a reason, or counter-propose. The exchange repeats until the item is ready or refused, with no
person in the loop unless the two sides cannot agree. The brainstorming route is the `brainstorming` capability's.

## Behaviour

### [g1] A peer's request becomes an item
- [r1] When a session runs `work intake` on a request that is `open`, `work` shall write a `shaped` item asked by a
  bounded context, set the provenance of the item to `peer` and commit the item.

### [g2] An accepted line stays on the item
- [r2] When a session runs `work outcome accepted` on a request line of an item, `work` shall set the line outcome of
  the request line to `accepted` and commit the item.

### [g3] A refused line is written with its reason
- [r3] When a session runs `work outcome refused` on a request line of an item, `work` shall set the line outcome of
  the request line to `refused`, write the reason and commit the item.

### [g4] A counter-proposal passes the turn to the asker
- [r4] When a session runs `work outcome rewritten` on a request line proposed in a request, `work` shall set the
  line outcome of the request line to `rewritten`, write a request line and change the side of the request.

### [g5] No person in the loop
- [r5] While a request is `awaiting-upstream`, when a session runs `work intake` on the request, `work` shall not ask
  a question.

### [g6] An item with a request line that is not settled is not readied
- [r6] While an item is `shaped` and a request line of the item is not settled, if a session runs `work ready` on the
  item, then `work` shall exit with an error naming the request line and change nothing.

## Implementation, may change
- `work intake <request>` writes a `shaped` item and changes nothing in the request: titled by the request's heading,
  with `request: q<n>` and `asked_by: <the request's asker>` in its frontmatter, its provenance read off the asker
  (this context's own asker: `own`; a `product/` id: `product`; any other: `peer`), and the note `taken in from
  request q<n> "<title>"`. It takes a request in the upstream's turn (`open` or `awaiting-upstream`), and refuses one
  another item was already taken in from, naming that item.
- The request lines of an item are the lines of its request whose line outcome is not `rewritten`: a rewritten line is
  no longer the item's, its counter-proposal is. So every request line of the item is settled once each is `accepted`,
  `refused` or `withdrawn`.
- `work outcome <request> <n> <word>` with `--into`, `--group`, `--reason` or `--line`, or on a request an item was
  taken in from, keeps the old refusals (the asker's turn, the upstream's part) and: `accepted` writes the line into
  the item's `## Requirements` under `--into <capability>`; `refused` needs `--reason`; `rewritten --line <text>`
  checks the counter-proposal in the context's grammar, appends it to the request's `## Lines` and passes the turn to
  the asker (`awaiting-asker`). On a request taken in, the item gains a note naming the line and its outcome, and the
  request and the item are one commit. Without these options, on a request no item was taken in from, `work outcome`
  is as before.
- A reason (`--reason`, or `rewritten as line <m>`) is written under the request's `## Reasons` as `<n>. <text>`, a
  section `model check` accepts.

## Not yet
- The item tied to the request's asker: r1 writes an item asked by a bounded context, but the grammar cannot yet say
  that this bounded context is the request's asker, nor that the request's upstream is this bounded context.
- The intake session started by `work backlog` (design: "a session started when the backlog command runs intake"):
  waits for plan 4's batches, which build the `claude -p` plumbing. Until then the skill `taking-in-a-request` is that
  session's instructions, run by any session.
