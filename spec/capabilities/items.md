---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/items
title: Items
narrator: the person
group: service
area: tracking
specifies: object item, service backlog, the readiness policy
language: codified-2
retired: [g3, r3, g18, r18, g33, r33]
unbuilt: []
---

# Items

## Purpose
The backlog's items through their lifecycle: noted as ideas, shaped, rated, linked, readied against the readiness bar,
declined, withdrawn, answered and listed.

## Behaviour

### [g1] A shaped item that meets the readiness bar is readied
- [r1] While an item is `shaped` and the item meets the readiness bar, when the person readies the item, the backlog
  service shall set the status of the item to `ready`.

### [g2] An item that does not meet the readiness bar is refused, naming each bar check it does not meet
- [r2] While an item is `shaped` and the item does not meet the readiness bar, if the person readies the item, then the
  backlog service shall refuse the request and name every bar check that the item does not meet.

### [g4] Readying an item asks the person nothing
- [r4] When the person readies an item, the backlog service shall not ask a question.

### [g5] An item a term of which violates a rule is not readied
- [r5] While an item is `shaped` and a term in the item violates a rule, if the person readies the item, then the
  backlog service shall refuse the request and name the term and the rule.

### [g6] An item a requirement of which has no translation is not readied
- [r6] While an item is `shaped` and a requirement in the item has no translation, if the person readies the item, then
  the backlog service shall refuse the request and name the requirement.

### [g7] An item a universal condition of which has no translation is not readied
- [r7] While `universal` does not exist and an item is `shaped` and a universal condition in the item has no
  translation, if the person readies the item, then the backlog service shall refuse the request and name the universal
  condition.

### [g8] Every requirement of an item that has no parse and every one that has no translation is named at once
- [r8] While an item is `shaped` and a requirement in the item has no parse and a different requirement in the item has
  no translation, if the person readies the item, then the backlog service shall refuse the request and name every
  requirement in the item that has no parse and every requirement in the item that has no translation.

### [g9] A shaped item that holds a chore and no requirement is readied
- [r9] While an item is `shaped` and the item holds a chore and the item holds no requirement, when the person readies
  the item, the backlog service shall set the status of the item to `ready`.

### [g10] An item a requirement group of which violates a rule is not readied
- [r10] While an item is `shaped` and a requirement group in the item violates a rule, if the person readies the item,
  then the backlog service shall refuse the request and name the requirement group and the rule.

### [g11] A dependency linked to an item is kept
- [r11] When the person links an item, the backlog service shall keep a dependency on the item.

### [g12] An item shown gives its title
- [r12] When the person shows an item, the backlog service shall return the title of the item.

### [g13] An idea noted is kept as an item
- [r13] When the person notes an idea, the backlog service shall keep an item whose status is `idea`.

### [g14] An idea shaped becomes shaped
- [r14] While the status of an item is `idea`, when the person shapes the item, the backlog service shall set the status
  of the item to `shaped`.

### [g15] Only an idea is shaped
- [r15] While the status of an item is not `idea`, if the person shapes the item, then the backlog service shall refuse
  the request and name the item.

### [g16] An item rated keeps its value, urgency and size
- [r16] When the person rates an item with the value `high-value` and the urgency `low-urgency` and the size `small`,
  the backlog service shall set the value of the item to `high-value`, set the urgency of the item to `low-urgency`, set
  the size of the item to `small` and keep the item.

### [g17] The backlog gives an open item's dependencies
- [r17] While an item is not `delivered` and a dependency on the item exists and another item has the dependency, when
  the person lists the backlog, the backlog service shall return the item and the dependency.

### [g19] An idea or a shaped item declined becomes refused
- [r19] While the status of an item is one of `idea` or `shaped`, when the person declines the item, the backlog service
  shall set the status of the item to `refused`.

### [g20] An item that needs input answered becomes shaped
- [r20] While the status of an item is `needs-input`, when the person answers the item, the backlog service shall set
  the status of the item to `shaped` and keep the item.

### [g21] The backlog gives the questions of an item that needs input
- [r21] While the status of an item is `needs-input`, when the person lists the backlog, the backlog service shall
  return the item and every question on the item.

### [g22] An idea is kept while the shared store rejects a change
- [r22] While the shared store is `rejecting`, when the person notes an idea, the backlog service shall keep an item
  whose status is `idea`, name the shared store and complete the request.

### [g23] An idea is kept while the shared store does not answer
- [r23] While the shared store is `unreachable`, when the person notes an idea, the backlog service shall keep an item
  whose status is `idea`, name the shared store and complete the request.

### [g24] No idea is noted in the workspace of a task
- [r24] While this repository is in the workspace of a task, if the person notes an idea, then the backlog service shall
  refuse the request and name the task.

### [g25] An idea noted in a workspace keeps its shared workspace of another name
- [r25] While this repository is in a workspace that has a workspace name and the shared workspace of the workspace has
  a different workspace name, when the person notes an idea, the backlog service shall keep an item whose status is
  `idea` and keep the shared workspace.

### [g26] The backlog gives each item's title, status, provenance and ratings
- [r26] While an item exists, when the person lists the backlog, the backlog service shall return the item, the title of
  the item, the status of the item, the provenance of the item, the value of the item, the urgency of the item and the
  size of the item.

### [g27] An idea with no shaping note is not shaped without a note
- [r27] While the status of an item is `idea` and the item has no shaping note, if the person shapes the item without a
  note, then the backlog service shall refuse the request and name the note.

### [g28] The backlog names the note an idea with no shaping note waits on
- [r28] While the status of an item is `idea` and the item has no shaping note, when the person lists the backlog, the
  backlog service shall return the item and name the note.

### [g29] A session that starts is told every item and batch
- [r29] When a session starts, the backlog service shall notify the session of every item, every title of an item and
  every batch.

### [g30] An item with a request line not settled is not readied
- [r30] While an item is `shaped` and a request line of the item is not `accepted`, `refused` or `withdrawn`, if a
  session readies the item, then the backlog service shall refuse the request and name the request line.

### [g31] A ready item reopened becomes shaped
- [r31] While an item is `ready`, when the person reopens the item, the backlog service shall set the status of the item to `shaped` and keep the item.

### [g32] Only a ready item is reopened
- [r32] While an item is not `ready`, if the person reopens the item, then the backlog service shall refuse the request and name the item.

### [g38] A note on an open item is kept
- [r38] While the status of an item is one of `idea`, `shaped`, `ready` or `needs-input`, when the person annotates the item with a note, the backlog service shall keep the item.

### [g39] A closed item takes no note
- [r39] While the status of an item is one of `delivered`, `refused` or `withdrawn`, if the person annotates the item, then the backlog service shall refuse the request and name the item.

### [g34] A closed item is not merged
- [r34] While the status of an item is one of `delivered`, `refused` or `withdrawn`, if the person merges the item, then the backlog service shall refuse the request and name the item.

### [g35] A ready item that meets the readiness bar is checked again
- [r35] While an item is `ready` and the item meets the readiness bar, when the person readies the item, the backlog service shall complete the request and keep the item.

### [g36] A ready item that does not meet the readiness bar is refused, naming each bar check it does not meet
- [r36] While an item is `ready` and the item does not meet the readiness bar, if the person readies the item, then the backlog service shall refuse the request and name every bar check that the item does not meet.

### [g37] An item that is neither shaped nor ready is not readied
- [r37] While an item is not `shaped` and the item is not `ready`, if the person readies the item, then the backlog service shall refuse the request and name the item.

### [g40] An item a requirement of which uses a construct the construct catalogue does not define is not readied
- [r40] While an item is `shaped` and a requirement in the item uses a construct that has no catalogue entry, if the person readies the item, then the backlog service shall refuse the request and name the requirement and the construct.

### [g41] An item a model line of which violates a rule is not readied
- [r41] While an item is `shaped` and a model line in the item violates a rule, if the person readies the item, then the backlog service shall refuse the request and name the model line and the rule.

### [g42] An open item withdrawn with its reason becomes withdrawn
- [r42] While the status of an item is one of `idea`, `shaped`, `ready` or `needs-input`, when the person withdraws the item with a reason, the backlog service shall set the status of the item to `withdrawn` and keep the item.

### [g44] An open item merged into a successor is withdrawn
- [r44] While a successor exists and the status of an item is one of `idea`, `shaped`, `ready` or `needs-input`, when the person merges the item with the successor and a reason, the backlog service shall set the status of the item to `withdrawn` and keep the item.

### [g45] An item is not merged into a closed successor
- [r45] While the status of a successor is one of `delivered`, `refused` or `withdrawn` and the status of an item is one of `idea`, `shaped`, `ready` or `needs-input`, if the person merges the item with the successor and a reason, then the backlog service shall refuse the request and name the successor.

### [g43] An item is not merged into itself
- [r43] If the person merges a successor with the successor and a reason, then the backlog service shall refuse the request and name the successor.

### [g46] An in-batch item is not merged
- [r46] While the status of an item is `in-batch`, if the person merges the item, then the backlog service shall refuse the request and name the item.

### [g47] An in-batch item takes no note
- [r47] While the status of an item is `in-batch`, if the person annotates the item, then the backlog service shall refuse the request and name the item.

