---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/laying
title: Laying
narrator: the batches service
group: service
area: laying
specifies: service laying
language: codified-2
retired: [g1, r1, g42, r42, g3, r3, g4, r4, g19, r19, g20, r20, g7, r7, g8, r8, g21, r21, g22, r22, g23, r23, g24, r24, g25, r25, g26, r26, g27, r27, g28, r28, g29, r29, g30, r30, g31, r31, g32, r32, g33, r33, g34, r34, g35, r35, g36, r36, g37, r37, g38, r38, g39, r39, g40, r40, g41, r41, g48, r48, g49, r49, g6, r6, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g15, r15, g16, r16, g17, r17, g18, r18]
unbuilt: []
---

# Laying

## Purpose
The specification a batch works on, reached by the batches service through a driven port: an item laid in a workspace and lifted from it, the item checked there and its scenarios generated there, whichever adapter does it.

## Behaviour
### [g2] An item lifted is no longer held by the workspace
- [r2] While a workspace holds a requirement of an item, when the batches service lifts the item from the workspace, the laying service shall keep a workspace that does not hold the requirement.
Relied on by: batches#r182

### [g5] A lift of an item keeps out a requirement of the same group that another requirement in the workspace retires
- [r5] While an item holds a requirement that retires the requirement id of a requirement of a requirement group and a workspace holds another requirement that retires the requirement id of another requirement of the requirement group, when the batches service lifts the item from the workspace, the laying service shall keep a workspace that does not hold the requirement.
Relied on by: batches#r182

### [g43] A lift of an item whose model line restates an operation keeps the operation in the domain model
- [r43] While an item holds a model line that restates an operation and the domain model holds the model line, when the batches service lifts the item from a workspace, the laying service shall keep a domain model that holds the operation.
Relied on by: batches#r182, batches#r185

### [g44] A lift of an item restating an element keeps another item's member line of the element
- [r44] While an item holds a model line that holds a member line and another item holds a model line that restates an element and the element does not hold the member line, when the batches service lifts the item from a workspace, the laying service shall keep the member line in the domain model and keep a domain model that does not hold the model line.
Relied on by: batches#r182, batches#r185

### [g45] A lift of another item keeps a port area holding a capability of an item and importing a supporting area
- [r45] While the kind of an area is `port` and the area holds a capability that an item holds and the area imports an area whose kind is `supporting`, when the batches service lifts another item from a workspace, the laying service shall keep the area.
Relied on by: batches#r182, batches#r185

### [g46] A lift of an item that holds a capability of a port area takes out the import its lay added
- [r46] While the kind of the `registry` area is `port` and an item holds a capability that the `registry` area holds and the `registry` area imports the `tracking` area, when the batches service lifts the item from a workspace, the laying service shall keep the `registry` area and keep an area that does not import the `tracking` area.
Relied on by: batches#r182, batches#r185

### [g47] A lift that puts back a group leaves out the Relied on by of a line another requirement in the workspace retires
- [r47] While an item holds a requirement that retires the requirement id of a requirement of a requirement group and a workspace holds another requirement that retires the requirement id of another requirement of the requirement group and the requirement supports a requirement id, when the batches service lifts the item from the workspace, the laying service shall keep a requirement of the requirement group that does not support the requirement id.
Relied on by: batches#r182

