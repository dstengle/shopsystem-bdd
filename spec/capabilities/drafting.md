---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/drafting
title: Drafting
narrator: the person
group: service
area: tracking
specifies: service drafting
language: codified-2
retired: []
unbuilt: [r26]
---

# Drafting

## Purpose
An item's lines drafted: requirement lines, relation rows, given blocks, universal conditions, upstream entries, new
capabilities, retirements, rewordings and chores.

## Behaviour

### [g1] A relation row drafted into an item is kept
- [r1] When the person drafts an item with a relation row, the drafting service shall keep the relation row in the item.

### [g2] A relation row that does not conform to its form is refused
- [r2] If the person drafts an item with a relation row that does not conform to the relation-row form, then the
  drafting service shall refuse the request and name the relation row.

### [g3] A universal condition drafted into an item is kept
- [r3] When the person drafts an item with a universal condition, the drafting service shall keep the universal
  condition in the item.

### [g4] An upstream entry drafted into an item is kept
- [r4] When the person drafts an item with an upstream entry, the drafting service shall keep the upstream entry in the
  item.

### [g5] An upstream entry that does not conform to its form is refused
- [r5] If the person drafts an item with an upstream entry that does not conform to the upstream-entry form, then the
  drafting service shall refuse the request and name the upstream entry.

### [g6] A given block drafted into an item is kept
- [r6] When the person drafts an item with a given block, the drafting service shall keep the given block in the item.

### [g7] A given block that does not conform to the example-data form is refused
- [r7] If the person drafts an item with a given block that does not conform to the example-data form, then the drafting
  service shall refuse the request and name the given block.

### [g8] A line that retires a requirement is kept in the item
- [r8] When the person drafts an item with a requirement id, the drafting service shall keep a requirement in the item.

### [g9] Retiring a requirement id that no requirement has is refused
- [r9] If the person drafts an item with a requirement id that no requirement has, then the drafting service shall
  refuse the request and name the requirement id.

### [g10] Recodifying a capability in an item sets its language
- [r10] When the person recodifies a capability in an item, the drafting service shall set the language of the
  capability in the item to `codified-2` and keep the item.

### [g11] Recodifying the universal conditions in an item sets their language
- [r11] When the person recodifies `universal` in an item, the drafting service shall set the language of the capability
  in the item to `codified-2` and keep the item.

### [g12] A universal condition that retires another is kept in the item
- [r12] When the person drafts an item with a universal condition id, the drafting service shall keep a universal
  condition in the item.

### [g13] Retiring a universal condition id that no universal condition has is refused
- [r13] If the person drafts an item with a universal condition id that no universal condition has, then the drafting
  service shall refuse the request and name the universal condition id.

### [g14] Rewording a requirement of an item keeps the new requirement
- [r14] When the person rewords a requirement in an item, the drafting service shall keep a different requirement in the
  item.

### [g15] Rewording a requirement of a capability is refused
- [r15] If the person rewords a requirement of a capability, then the drafting service shall refuse the request and name
  the requirement.

### [g16] Removing a requirement of a capability is refused
- [r16] If the person removes a requirement of a capability, then the drafting service shall refuse the request and name
  the requirement.

### [g17] Retiring a requirement with no line replacing it keeps only the requirement id
- [r17] When the person drafts an item with a requirement id and without a requirement, the drafting service shall keep
  the requirement id in the item and not keep a requirement in the item.

### [g18] Retiring with no line a requirement id that no requirement has is refused
- [r18] If the person drafts an item with a requirement id that no requirement has and without a requirement, then the
  drafting service shall refuse the request and name the requirement id.

### [g19] A chore assigned to an item is kept
- [r19] When the person assigns a chore to an item, the drafting service shall keep the chore in the item.

### [g20] A chore is not assigned to an item that holds a requirement
- [r20] If the person assigns a chore to an item that holds a requirement, then the drafting service shall refuse the
  request and name the requirement.

### [g21] An item that holds a chore is not drafted
- [r21] If the person drafts an item that holds a chore, then the drafting service shall refuse the request and name the
  chore.

### [g22] A new capability drafted into an item is kept
- [r22] When the person drafts an item with a capability, the drafting service shall keep the capability in the item.

### [g23] Drafting a capability that exists is refused
- [r23] If the person drafts an item with a capability that exists, then the drafting service shall refuse the request
  and name the capability.

### [g24] Removing a requirement of an item keeps the requirement ids it does not retire
- [r24] When the person removes a requirement in an item, the drafting service shall keep every requirement id in the
  item that the requirement does not retire.

### [g25] A term written for a new capability of an item is kept
- [r25] While an item holds a capability that does not exist, when the person writes a term into the item, the drafting service shall keep the term in the item.

### [g26] A model line declared for a new capability of an item is kept
- [r26] While an item holds a capability that does not exist, when the person declares a model line in the item, the drafting service shall keep the model line in the item.

