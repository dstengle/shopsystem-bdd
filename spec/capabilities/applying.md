---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/applying
title: Applying
narrator: the batches service
group: service
area: specification
specifies: service language
language: codified-2
retired: [g1, r1]
unbuilt: [r49]
---

# Applying

## Purpose
An item applied to a specification: its requirements, groups, capabilities, model lines, terms, packs and operation tables kept in the specification, whichever service applies it.

## Behaviour
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

### [g37] Applying an item prepares the specification: scenarios, corpus, catalogues and index
- [r37] While an item holds a requirement, when the batches service applies the item to a specification, the specification service shall keep the specification that holds the requirement and keep a scenario that refers to the requirement id of the requirement.

### [g38] An item applied keeps the logical form of each of its requirements in the corpus
- [r38] While a requirement of an item has a logical form, when the batches service applies the item to a specification, the specification service shall keep the logical form in the corpus.

### [g39] An item applied keeps no corpus block of a requirement id it retires
- [r39] While a requirement id is in an item and a requirement in the corpus has the requirement id, when the batches service applies the item to a specification, the specification service shall keep a corpus that does not hold the requirement.

### [g40] An item applied keeps the catalogue entry of a rule its requirements use
- [r40] While a requirement of an item uses a rule, when the batches service applies the item to a specification, the specification service shall keep the catalogue entry of the rule.

### [g41] An item applied keeps the construct catalogue when its requirements use a construct
- [r41] While an item holds a requirement that uses a construct, when the batches service applies the item to a specification, the specification service shall keep the construct catalogue.

### [g42] An item applied whose requirements use no construct keeps no construct catalogue
- [r42] While an item holds no requirement that uses a construct and no construct catalogue exists, when the batches service applies the item to a specification, the specification service shall keep no construct catalogue.

### [g43] An item applied keeps an index file of the index form
- [r43] When the batches service applies an item to a specification, the specification service shall keep an index file that conforms to the index form.

### [g44] An item applied keeps a capability with no requirement out of the index file
- [r44] While a capability has no requirement, when the batches service applies an item to a specification, the specification service shall keep an index file that does not hold the capability.

### [g45] An item applied keeps a capability with a requirement in the index file
- [r45] While a capability has a requirement, when the batches service applies an item to a specification, the specification service shall keep an index file that holds the capability.

### [g46] An item applied generates the feature of a capability whose operation its model lines specify
- [r46] While an item holds a model line that specifies an operation and a requirement of a capability governs the operation and the item holds no requirement id that is in the capability, when the batches service applies the item to a specification, the specification service shall generate the feature of the capability and keep the logical form of the requirement in the corpus.

### [g47] An item applied keeps in the corpus the logical form of a requirement that uses a verb it gives a sense
- [r47] While an item holds a verb that has a sense and a requirement of a capability uses the verb and the item holds no requirement id that is in the capability, when the batches service applies the item to a specification, the specification service shall keep the logical form of the requirement in the corpus.

### [g48] An item applied that retires an area keeps a domain model without it
- [r48] While an item retires an area, when the batches service applies the item to a specification, the specification service shall keep a domain model that does not hold the area.

### [g49] An item applied that retires an area keeps no area importing it
- [r49] While an item retires an area and another area imports the area, when the batches service applies the item to a specification, the specification service shall keep a domain model that holds no area that imports the area.

### [g50] An item applied that retires an area keeps its capabilities in no area
- [r50] While an item retires an area and a capability is in the area, when the batches service applies the item to a specification, the specification service shall keep the capability in the specification and keep no capability in the area.

