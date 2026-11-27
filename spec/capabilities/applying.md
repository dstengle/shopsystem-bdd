---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/applying
title: Applying
narrator: the batches service
group: service
area: specification
specifies: service language
language: codified-2
retired: []
unbuilt: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25]
---

# Applying

## Purpose
An item applied to a specification: its requirements, groups, capabilities, model lines, terms, packs and operation tables kept in the specification, whichever service applies it.

## Behaviour
### [g1] An item applied is held by the specification it is applied to
- [r1] While an item holds a requirement, when the batches service applies the item to a specification, the specification service shall keep the specification that holds the requirement.

### [g2] An item applied that holds a universal condition where none exists keeps universal in the new language
- [r2] While `universal` does not exist and a universal condition is in an item, when the batches service applies the item to a specification, the specification service shall keep `universal` and set the language of `universal` to `codified-2`.

### [g3] An item applied that holds a capability keeps the capability of the capability form
- [r3] While an item holds a capability, when the batches service applies the item to a specification, the specification service shall keep the capability that conforms to the capability form.

### [g4] An item applied that holds a requirement group serving a job keeps the group serving the job
- [r4] While an item holds a requirement group that serves a job, when the batches service applies the item to a specification, the specification service shall keep a capability that has a requirement group that serves the job.

### [g5] An item applied that holds a capability in an area keeps the capability in the area
- [r5] While an item holds a capability and the item holds an area that holds the capability, when the batches service applies the item to a specification, the specification service shall keep the capability that the area holds.

### [g6] An item applied that holds a capability in a driven port keeps the capability in the driven port
- [r6] While an item holds a capability and the item holds a driven port that holds the capability, when the batches service applies the item to a specification, the specification service shall keep the driven port that holds the capability.

### [g7] An item applied that holds a term of a pack keeps the pack with the term and imports it
- [r7] While an item holds a term of a pack, when the batches service applies the item to a specification, the specification service shall keep the pack that has the term and keep the pack that this bounded context imports.

### [g8] An item applied that holds a term of a pack beside its requirements keeps the pack with the term
- [r8] While an item holds a term of a pack and a capability holds a requirement id that the item holds, when the batches service applies the item to a specification, the specification service shall keep the pack that has the term.

### [g9] An item applied that imports a pack keeps the pack imported
- [r9] While an item imports a pack, when the batches service applies the item to a specification, the specification service shall keep the pack that this bounded context imports.

### [g10] An item applied that holds an operation table keeps it in the adapter contract
- [r10] While an item holds an operation table, when the batches service applies the item to a specification, the specification service shall keep an adapter contract that holds the operation table.

### [g11] An item applied that holds an operation keeps no operation table of it
- [r11] While an item holds an operation, when the batches service applies the item to a specification, the specification service shall keep an adapter contract and keep no operation table of the operation.

### [g12] An item applied whose model line specifies a new operation with no table keeps a table of it
- [r12] While an item holds a model line and the model line specifies an operation and the domain model does not hold the operation and the item holds no operation table of the operation, when the batches service applies the item to a specification, the specification service shall keep an adapter contract that holds an operation table of the operation.

### [g13] An item applied that holds an operation table beside its requirements keeps it in the adapter contract
- [r13] While an item holds an operation table and a capability holds a requirement id that the item holds, when the batches service applies the item to a specification, the specification service shall keep an adapter contract that holds the operation table.

### [g14] An item applied whose model line restates an operation keeps the model line in place of the operation
- [r14] While an item holds a model line that restates an operation, when the batches service applies the item to a specification, the specification service shall keep the model line in the domain model and keep a domain model that does not hold the operation.

### [g15] An item applied whose model line restates an element keeps the model line in place of the element
- [r15] While an item holds a model line that restates an element, when the batches service applies the item to a specification, the specification service shall keep the model line in the domain model and keep a domain model that does not hold the element.

### [g16] An item applied whose model line restates an event keeps the model line in place of the event
- [r16] While an item holds a model line that restates an event, when the batches service applies the item to a specification, the specification service shall keep the model line in the domain model and keep a domain model that does not hold the event.

### [g17] An item applied whose model line restates an actor keeps the model line in place of the actor
- [r17] While an item holds a model line that restates an actor, when the batches service applies the item to a specification, the specification service shall keep the model line in the domain model and keep a domain model that does not hold the actor.

### [g18] An item applied whose model line moves to an area keeps the area holding the model line
- [r18] While an item holds a model line that moves to an area, when the batches service applies the item to a specification, the specification service shall keep the area that holds the model line.

### [g19] An item applied that moves a term keeps the term in the area of its element
- [r19] While an item moves a term that means an element and an area holds the element, when the batches service applies the item to a specification, the specification service shall keep the area that holds the term.

### [g20] An item applied that moves a term beside its requirements keeps the term in the area of its element
- [r20] While an item moves a term that means an element and an area holds the element and a capability holds a requirement id that the item holds, when the batches service applies the item to a specification, the specification service shall keep the area that holds the term.

### [g21] An item applied that retires a model line keeps an area without it
- [r21] While an item retires a model line, when the batches service applies the item to a specification, the specification service shall keep an area that does not hold the model line.

### [g22] An item applied that retires a term keeps an area without it
- [r22] While an item retires a term, when the batches service applies the item to a specification, the specification service shall keep an area that does not hold the term.

### [g23] An item applied that retires an element and a term meaning it keeps an area without the term
- [r23] While an item retires a model line that restates an element and the item retires a term that means the element, when the batches service applies the item to a specification, the specification service shall keep an area that does not hold the term.

### [g24] An item applied that makes two areas imports into one the other whose term its requirement uses
- [r24] While an item holds the `watering` area and the item holds the `plots` area and the `plots` area holds a term and the `watering` area holds a capability and a requirement of the capability uses the term, when the batches service applies the item to a specification, the specification service shall keep the `watering` area and keep an area that imports the `plots` area.

### [g25] An item applied that holds a capability keeps the capability specifying the service its area holds
- [r25] While an item holds a capability and an area holds the capability, when the batches service applies the item to a specification, the specification service shall keep the capability that specifies the service of the area.

