---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/request-watch
title: Request watch
narrator: a session
group: service
area: tracking
specifies: notifications of context requests
language: codified-2
retired: []
unbuilt: []
---

# Request watch

## Purpose
What a session is told of the context requests waiting on this bounded context: at its start, while it watches, and as
it catches up.

## Behaviour

### [g1] A watch tells of an entry not held
- [r1] While an entry on a context request conforms to the entry form and the context request does not hold the entry,
  when a session watches this bounded context, the context requests service shall notify the session of the entry,
  complete the request and not keep the entry.

### [g2] A watch tells of an open thread that no context request has
- [r2] While a thread on the channel of this bounded context is `open` and the thread conforms to the entry form and no
  context request has the thread, when a session watches this bounded context, the context requests service shall notify
  the session of the thread and complete the request.

### [g3] A session that starts is told of a context request awaiting its upstream
- [r3] While a context request originates from this bounded context and the context request does not address this
  bounded context and the context request is `awaiting-upstream`, when a session starts, the context requests service
  shall notify the session of the context request.

### [g4] A session that starts is told of a context request awaiting this bounded context's asker
- [r4] While a context request addresses this bounded context and the context request does not originate from this
  bounded context and the context request is `awaiting-asker`, when a session starts, the context requests service shall
  notify the session of the context request.

### [g5] A session that starts is told nothing when no context request waits
- [r5] While no context request that originates from this bounded context is `awaiting-upstream` and no context request
  that addresses this bounded context is `awaiting-asker`, when a session starts, the context requests service shall not
  notify the session of a context request.

### [g6] An unreadable entry is told once and kept
Restates: requests#r58@0.29.
- [r6] While an entry on a context request does not conform to the entry form and the context request does not hold the
  entry, when a session catches up, the context requests service shall notify the session of the entry, keep the entry
  and keep the status of the context request.

### [g7] An unreadable entry held is not told again
- [r7] While an entry on a context request does not conform to the entry form and the context request holds the entry,
  when a session catches up, the context requests service shall not notify the session of the entry.
