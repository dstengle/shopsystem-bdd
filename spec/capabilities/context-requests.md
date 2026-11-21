---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/context-requests
title: Context requests
narrator: the person
group: service
area: tracking
specifies: object context request, service context requests
language: codified-2
retired: [g19, r19, g29, r29]
unbuilt: [r56]
---

# Context requests

## Purpose
The requests between bounded contexts: raised by an asker, answered by its upstream turn by turn, settled line by line,
accepted into an item and resolved once delivered.

## Behaviour

### [g1] A counter-proposal passes the turn to the asker
- [r1] When a session settles a request line of a context request with the line outcome `rewritten`, the context
  requests service shall set the line outcome of the request line to `rewritten`, keep a request line of the context
  request that counters the request line, set the side of the context request to `asker` and keep an entry on the
  context request.

### [g2] A refused request line keeps its reason
- [r2] When a session settles a request line of a context request with the line outcome `refused`, the context requests
  service shall set the line outcome of the request line to `refused`, keep a line reason of the request line and keep
  the context request.

### [g3] A request line is not refused without a reason
- [r3] If a session settles a request line with the line outcome `refused` and without a line reason, then the context
  requests service shall refuse the request and name the line reason.

### [g4] A context request raised for another is kept
Restates: requests#r29@0.29.
- [r4] When the person raises a context request for a context request, the context requests service shall keep the
  context request.

### [g5] A context request with neither an origin nor a thread is refused
Restates: requests#r45@0.29, requests#r31@0.29.
- [r5] If the person raises a context request without an origin and a thread, then the context requests service shall
  refuse the request and name the thread.

### [g6] A context request of an upstream entry with an origin and a thread is refused
Restates: requests#r30@0.29.
- [r6] While this bounded context holds an upstream entry, if the person raises a context request with an origin and a
  thread, then the context requests service shall refuse the request and name the origin.

### [g7] A context request from a text that does not identify this bounded context is refused
Restates: requests#r32@0.29.
- [r7] If the person raises a context request with a text that does not identify this bounded context, then the context
  requests service shall refuse the request and name the text.

### [g8] A request line accepted in an open context request is kept
Restates: requests#r12@0.29, requests#r15@0.29, requests#r5@0.29.
- [r8] While a context request is `open`, when the person settles a request line in the context request with the line
  outcome `accepted`, the context requests service shall set the line outcome of the request line to `accepted` and keep
  the context request.

### [g9] A request line is not settled while the context request awaits its asker
Restates: requests#r16@0.29.
- [r9] While a context request is `awaiting-asker`, if the person settles a request line in the context request, then
  the context requests service shall refuse the request and name the context request.

### [g10] A request line of a context request not asked of this bounded context is not settled
Restates: requests#r33@0.29, requests#r55@0.29.
- [r10] While a context request is `open` and the context request does not address this bounded context, if the person
  settles a request line in the context request, then the context requests service shall refuse the request and name the
  context request.

### [g11] A question asked on an open context request is kept
Restates: requests#r20@0.29, requests#r5@0.29.
- [r11] While a context request is `open`, when the person asks a question on the context request, the context requests
  service shall keep the question.

### [g12] A reply to a context request this bounded context asked is kept
Restates: requests#r21@0.29, requests#r4@0.29.
- [r12] While a context request is `awaiting-asker` and the context request originates from this bounded context, when
  the person replies to the context request, the context requests service shall keep an answer.

### [g13] A context request that is not accepted is not resolved
Restates: requests#r10@0.29.
- [r13] While a context request is not `accepted`, if the person resolves the context request, then the context requests
  service shall refuse the request and name the context request.

### [g14] The context requests are given with their status and the observations no context request cites
Restates: requests#r50@0.29, requests#r64@0.29.
- [r14] When the person surveys this bounded context, the context requests service shall return every context request,
  the status of every context request and every observation that no context request cites.

### [g15] A context request inspected gives its status and request lines
Restates: work-queue#r59@0.29.
- [r15] When the person inspects a context request, the context requests service shall return the status of the context
  request and every request line in the context request.

### [g16] A context request raised is kept open with its thread
Restates: requests#r12@0.29, requests#r4@0.29, requests#r44@0.29, requests#r28@0.29.
- [r16] When the person raises a context request, the context requests service shall keep a context request whose status
  is `open` and a thread of the context request.

### [g17] A context request to a bounded context with no channel is refused
- [r17] If the person raises a context request with a bounded context that has no channel, then the context requests
  service shall refuse the request and name the bounded context.

### [g18] An offer on an open context request awaits its asker
- [r18] While a context request is `open`, when a session offers on the context request, the context requests service
  shall keep an entry on the context request and set the status of the context request to `awaiting-asker`.

### [g20] Lines proposed to a context request are kept
- [r20] While a context request is `awaiting-asker`, when the person proposes to the context request, the context
  requests service shall keep a request line.

### [g21] An entry not held is kept when the session catches up
- [r21] While an entry on a context request conforms to the entry form and the context request does not hold the entry,
  when a session catches up, the context requests service shall keep the entry and return every context request.

### [g22] The asker's turn passed goes to the upstream
Restates: requests#r18@0.29, requests#r7@0.29.
- [r22] While a context request is `awaiting-asker`, when the person passes the turn of the context request, the context
  requests service shall set the status of the context request to `awaiting-upstream`, set the side of the context
  request to `upstream` and keep an entry on the context request.

### [g23] The upstream's turn passed with a request line not settled goes to the asker
Restates: requests#r17@0.29.
- [r23] While a context request is `open` and a request line in the context request is not `accepted`, `refused` or
  `withdrawn`, when the person passes the turn of the context request, the context requests service shall set the status
  of the context request to `awaiting-asker` and keep an entry on the context request.

### [g24] The upstream's turn passed with every request line settled and one accepted keeps the side
Restates: requests#r23@0.29, requests#r8@0.29.
- [r24] While a context request is `open` and a request line in the context request is `accepted` and every request line
  in the context request is one of `accepted`, `refused` or `withdrawn`, when the person passes the turn of the context
  request, the context requests service shall keep an entry on the context request and keep the side of the context
  request.

### [g25] The upstream's turn passed with every request line refused refuses the context request
Restates: requests#r9@0.29.
- [r25] While a context request is `open` and a request line in the context request is `refused` and every request line
  in the context request is `refused`, when the person passes the turn of the context request, the context requests
  service shall set the status of the context request to `refused` and keep an entry on the context request.

### [g26] A request line that does not conform to the requirement grammar is not accepted
Restates: requests#r2@0.29, requests#r59@0.29.
- [r26] While a request line does not conform to the requirement grammar of this bounded context, if a session settles
  the request line with the line outcome `accepted`, then the context requests service shall refuse the request and name
  the request line.

### [g27] A context request accepted is kept as a shaped item
- [r27] While a context request is `open` and a request line in the context request is `accepted` and every request line
  in the context request is one of `accepted`, `refused` or `withdrawn`, when the person accepts the context request,
  the context requests service shall set the status of the context request to `accepted`, keep an item whose status is
  `shaped` and keep an entry on the context request.

### [g28] A context request with a request line not settled is not accepted
- [r28] While a request line in a context request is not `accepted`, `refused` or `withdrawn`, if the person accepts the
  context request, then the context requests service shall refuse the request and name the request line.

### [g30] No context request is raised while this repository rejects a change
- [r30] While this repository is `rejecting`, if the person raises a context request, then the context requests service
  shall refuse the request, name this repository and not keep a thread.

### [g31] No turn is passed while this repository rejects a change
- [r31] While this repository is `rejecting` and a context request is `open`, if the person passes the turn of the
  context request, then the context requests service shall refuse the request, name this repository and not keep an
  entry on the context request.

### [g32] No context request is served while this repository rejects a change
- [r32] While this repository is `rejecting` and a context request is `awaiting-asker`, if the person serves the context
  request, then the context requests service shall refuse the request, name this repository and not keep an entry on the
  context request.

### [g33] A context request asked of this bounded context is not replied to
- [r33] While a context request addresses this bounded context and the context request does not originate from this
  bounded context, if the person replies to the context request, then the context requests service shall refuse the
  request and name the context request.

### [g34] The asker's turn of a context request asked of this bounded context is not passed
- [r34] While a context request addresses this bounded context and the context request does not originate from this
  bounded context and the context request is `awaiting-asker`, if the person passes the turn of the context request,
  then the context requests service shall refuse the request and name the context request.

### [g35] The upstream's turn of an open context request this bounded context asked is not passed
- [r35] While a context request originates from this bounded context and the context request does not address this
  bounded context and the context request is `open`, if the person passes the turn of the context request, then the
  context requests service shall refuse the request and name the context request.

### [g36] The upstream's turn of a context request this bounded context asked is not passed
- [r36] While a context request originates from this bounded context and the context request does not address this
  bounded context and the context request is `awaiting-upstream`, if the person passes the turn of the context request,
  then the context requests service shall refuse the request and name the context request.

### [g37] An asker's entry holding an upstream's field is kept without the field
- [r37] While an entry on a context request conforms to the entry form and the side of the entry is `asker` and the
  entry holds a field whose side is `upstream` and the context request does not hold the entry, when a session catches
  up, the context requests service shall keep the entry and not keep the field.

### [g38] An entry on a closed context request changes neither its status nor its side
- [r38] While a context request is one of `delivered`, `refused` or `withdrawn` and an entry on the context request
  conforms to the entry form and the context request does not hold the entry, when a session catches up, the context
  requests service shall keep the entry and keep the status of the context request and the side of the context request.

### [g39] A context request for another raised with an origin from an upstream entry is refused
Restates: requests#r30@0.29.
- [r39] While this bounded context holds an upstream entry, if the person raises a context request for a context request
  with an origin, then the context requests service shall refuse the request and name the origin.

### [g40] An upstream's entry holding an asker's field is kept without the field
- [r40] While an entry on a context request conforms to the entry form and the side of the entry is `upstream` and the
  entry holds a field whose side is `asker` and the context request does not hold the entry, when a session catches up,
  the context requests service shall keep the entry and not keep the field.

### [g41] A context request inspected gives the line reasons
- [r41] While a request line in a context request has a line reason, when the person inspects the context request, the
  context requests service shall return the line reason.

### [g42] An offer gives the context request and its status
- [r42] When the person offers on a context request, the context requests service shall return the context request and
  the status of the context request.

### [g43] A proposal gives the context request and its status
- [r43] When the person proposes to a context request, the context requests service shall return the context request and
  the status of the context request.

### [g44] A reply gives the context request and its status
- [r44] When the person replies to a context request, the context requests service shall return the context request and
  the status of the context request.

### [g45] A turn passed gives the context request and its status
- [r45] When the person passes the turn of a context request, the context requests service shall return the context
  request and the status of the context request.

### [g46] A context request raised with no sender originates from this bounded context
- [r46] When the person raises a context request without a text, the context requests service shall keep a context
  request that originates from this bounded context.

### [g47] An offer of a capability holds every requirement of it
- [r47] When a session offers on a context request with a capability, the context requests service shall keep an entry
  that holds every requirement of the capability.

### [g48] An offer of a capability holds each term its requirements mention
- [r48] While a requirement of a capability mentions a term, when a session offers on a context request with the
  capability, the context requests service shall keep an entry that holds the term.

### [g49] An offer of a capability holds no given block of it
- [r49] While a capability holds a given block, when a session offers on a context request with the capability, the
  context requests service shall keep an entry that does not hold the given block.

### [g50] An offer of a capability holds no term its requirements do not mention
- [r50] While a term is in the bounded context and a capability has no requirement that mentions the term, when a
  session offers on a context request with the capability, the context requests service shall keep an entry that does
  not hold the term.

### [g51] A context request is not resolved while its channel rejects a change to its thread
- [r51] While a context request is `accepted` and the context request has a thread on a channel whose availability is `rejecting`, if the person resolves the context request, then the context requests service shall refuse the request and name the thread.

### [g52] A context request is not served while its channel rejects a change to its thread
- [r52] While a context request is `awaiting-asker` and the context request has a thread on a channel whose availability is `rejecting`, if the person serves the context request, then the context requests service shall refuse the request and name the thread.

### [g54] A request's issue is never left out of step with its record
- [r54] While a context request is `awaiting-asker`, when the person serves the context request, the context requests service shall set the status of the context request to `delivered`, keep a resolution, keep an entry on the context request and set the status of the thread of the context request to `closed`.

### [g55] An accepted context request resolved is delivered and its thread closed
- [r55] While a context request is `accepted`, when the person resolves the context request, the context requests service shall set the status of the context request to `delivered`, keep a resolution, set the side of the context request to `asker`, keep an entry on the context request and set the status of the thread of the context request to `closed`.

### [g56] A turn passed is posted though the channel does not provide its thread
- [r56] While a context request is `awaiting-asker` and a channel does not provide the thread of the context request, when the person passes the turn of the context request, the context requests service shall set the status of the context request to `awaiting-upstream`, set the side of the context request to `upstream` and keep an entry on the context request.

## Dropped
- requests#r11@0.29: retired with context-requests#r29 by b68.
- requests#r24@0.29: retired with context-requests#r29 by b68.
