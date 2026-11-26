---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/laying
title: Laying
narrator: the batches service
group: service
area: laying
specifies: service laying
language: codified-2
retired: [g1, r1]
unbuilt: [r21, r6, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20]
---

# Laying

## Purpose
The specification a batch works on, reached by the batches service through a driven port: an item laid in a workspace and lifted from it, the item checked there and its scenarios generated there, whichever adapter does it.

## Behaviour
### [g2] An item lifted is no longer held by the workspace
- [r2] While a workspace holds a requirement of an item, when the batches service lifts the item from the workspace, the laying service shall keep a workspace that does not hold the requirement.
Relied on by: batches#r182

### [g3] A check of an item that violates a rule of severity error fails naming the rule
- [r3] While a requirement of an item violates a rule whose severity is `error`, when the batches service checks the item in a workspace, the laying service shall fail the request and name the rule.
Relied on by: batches#r180

### [g4] A check of an item that violates no rule of severity error completes
- [r4] While an item holds no requirement that violates a rule whose severity is `error`, when the batches service checks the item in a workspace, the laying service shall complete the request.
Relied on by: batches#r180

### [g5] A lift of an item keeps out a requirement of the same group that another requirement in the workspace retires
- [r5] While an item holds a requirement that retires the requirement id of a requirement of a requirement group and a workspace holds another requirement that retires the requirement id of another requirement of the requirement group, when the batches service lifts the item from the workspace, the laying service shall keep a workspace that does not hold the requirement.
Relied on by: batches#r182

### [g21] An item laid is held by the workspace before its batch is prepared
- [r21] While an item holds a requirement, when the batches service lays the item in a workspace, the laying service shall keep the workspace that holds the requirement.
Relied on by: batches#r179

### [g6] A workspace prepared for a batch holds a scenario of each requirement of its items
- [r6] While a batch holds an item and the item holds a requirement, when the batches service prepares a workspace for the batch, the laying service shall keep a scenario that refers to the requirement id of the requirement.
Relied on by: batches#r188

### [g9] A workspace prepared for a batch keeps the logical form of each requirement of its items in the corpus
- [r9] While a batch holds an item and a requirement of the item has a logical form, when the batches service prepares a workspace for the batch, the laying service shall keep the logical form in the corpus.
Relied on by: batches#r188

### [g10] A workspace prepared for a batch keeps no corpus block of a requirement id its items retire
- [r10] While a batch holds an item and a requirement id is in the item and a requirement in the corpus has the requirement id, when the batches service prepares a workspace for the batch, the laying service shall keep a corpus that does not hold the requirement.
Relied on by: batches#r188

### [g11] A workspace prepared for a batch keeps the catalogue entry of a rule its items use
- [r11] While a batch holds an item and a requirement of the item uses a rule, when the batches service prepares a workspace for the batch, the laying service shall keep the catalogue entry of the rule.
Relied on by: batches#r188

### [g12] A workspace prepared for a batch keeps the construct catalogue when its items use a construct
- [r12] While a batch holds an item and a requirement of the item uses a construct, when the batches service prepares a workspace for the batch, the laying service shall keep the construct catalogue.
Relied on by: batches#r188

### [g13] A workspace prepared for a batch whose items use no construct keeps no construct catalogue
- [r13] While a batch holds an item and no requirement of an item that the batch holds uses a construct and no construct catalogue exists, when the batches service prepares a workspace for the batch, the laying service shall keep no construct catalogue.
Relied on by: batches#r188

### [g14] A workspace prepared for a batch keeps an index file of the index form
- [r14] While a batch holds an item, when the batches service prepares a workspace for the batch, the laying service shall keep an index file that conforms to the index form.
Relied on by: batches#r188

### [g15] A workspace prepared for a batch keeps a capability with no requirement out of the index file
- [r15] While a capability has no requirement and a batch holds an item, when the batches service prepares a workspace for the batch, the laying service shall keep an index file that does not hold the capability.
Relied on by: batches#r188

### [g16] A workspace prepared for a batch keeps a capability with a requirement in the index file
- [r16] While a capability has a requirement and a batch holds an item, when the batches service prepares a workspace for the batch, the laying service shall keep an index file that holds the capability.
Relied on by: batches#r188

### [g17] A workspace prepared for a batch generates the feature of a capability whose operation its items' model lines specify
- [r17] While a batch holds an item and the item holds a model line that specifies an operation and a requirement of a capability governs the operation and the item holds no requirement id that is in the capability, when the batches service prepares a workspace for the batch, the laying service shall generate the feature of the capability and keep the logical form of the requirement in the corpus.
Relied on by: batches#r188

### [g18] A workspace prepared for a batch keeps in the corpus the logical form of a requirement that uses a verb its items give a sense
- [r18] While a batch holds an item and the item holds a verb that has a sense and a requirement of a capability uses the verb and the item holds no requirement id that is in the capability, when the batches service prepares a workspace for the batch, the laying service shall keep the logical form of the requirement in the corpus.
Relied on by: batches#r188

### [g19] A check of an item whose port line leaves an operation outcome unhandled fails naming the outcome
- [r19] While an item holds a port line that governs an operation and every port line that governs the operation is in the item and the operation has an operation outcome and no core line handles the operation outcome and no port line excludes the operation outcome, when the batches service checks the item in a workspace, the laying service shall fail the request and name the operation outcome.
Relied on by: batches#r180, batches#r189

### [g20] A check of an item whose core line uses another area's operation that performs a transition fails naming the line and v_m9
- [r20] While an area holds a lifecycle and the lifecycle has a transition and another area holds an operation that performs the transition and an item holds a core line that uses the operation, when the batches service checks the item in a workspace, the laying service shall fail the request and name the core line and `v_m9`.
Relied on by: batches#r180, batches#r189

