---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/directives
title: Directives
narrator: a session
group: service
area: tracking
specifies: object directive, service conversation: give, promote, drop
language: codified-2
retired: []
unbuilt: []
---

# Directives

## Purpose
The person's short-term directions: given with their quote, told to every session while live, promoted or dropped.

## Behaviour

### [g1] A directive given is kept with its quote
- [r1] When a session gives a directive, the conversation service shall keep a directive whose quote cites a message.

### [g2] A session that starts is told every live directive
- [r2] When a session starts, the conversation service shall notify the session of the quote of every directive whose
  status is `live`.

### [g3] A live directive promoted to an item becomes promoted
- [r3] When a session promotes a directive whose status is `live` to an item, the conversation service shall set the
  status of the directive to `promoted` and keep the directive.

### [g4] A live directive dropped with its reason becomes dropped
- [r4] When a session drops a directive whose status is `live` with a reason, the conversation service shall set the
  status of the directive to `dropped` and keep the directive.

### [g5] A directive that is not live is not promoted
- [r5] When a session promotes a directive whose status is not `live` to an item, the conversation service shall refuse
  the request and name the directive.

### [g6] A directive is not promoted to an item that does not exist
- [r6] When a session promotes a directive to an item that does not exist, the conversation service shall refuse the
  request and name the item.

### [g7] A directive that is not live is not dropped
- [r7] When a session drops a directive whose status is not `live` with a reason, the conversation service shall refuse
  the request and name the directive.
