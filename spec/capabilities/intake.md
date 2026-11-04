---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/intake
title: Intake
narrator: a session answering a peer bounded context's request
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r2, r3, r4]
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

## Not yet
- The item tied to the request's asker: r1 writes an item asked by a bounded context, but the grammar cannot yet say
  that this bounded context is the request's asker, nor that the request's upstream is this bounded context.
