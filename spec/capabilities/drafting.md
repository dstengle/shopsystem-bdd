---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/drafting
title: Drafting
narrator: the person
group: service
area: tracking
specifies: service drafting
language: codified-2
retired: [g99, r99, g100, r100, g49, r49, g14, r14]
unbuilt: [r107]
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

### [g27] Removing the last requirement of a new capability of an item keeps the capability
- [r27] While an item holds a capability that does not exist, when the person removes a requirement of the capability, the drafting service shall keep the capability in the item.

### [g28] `work line --retires` names the decisions the retired requirement enforces
- [r28] When the person drafts an item with a requirement id of a requirement that enforces a design-decision, the drafting service shall keep a requirement in the item and name the design-decision.

### [g29] A retirement list applied to an item keeps every requirement it holds
- [r29] When the person applies a retirement list to an item, the drafting service shall keep the item and every requirement that the retirement list holds.

### [g30] A retirement list that names a requirement id no requirement has is refused whole
- [r30] If the person applies a retirement list that holds a requirement id that no requirement has to an item, then the drafting service shall refuse the request, name the requirement id and not keep the item.

### [g31] An operation table exposed in an item is kept
- [r31] When the person exposes an operation table in an item, the drafting service shall keep the operation table in the item.

### [g32] An operation table of an operation that does not exist is refused
- [r32] While an operation does not exist, if the person exposes an operation table of the operation in an item, then the drafting service shall refuse the request and name the operation table.

### [g33] An operation exposed again keeps only its new operation table
- [r33] While an item holds an operation table of an operation, when the person exposes another operation table of the operation in the item, the drafting service shall keep only one operation table of the operation in the item.

### [g34] An operation withheld in an item is kept
- [r34] When the person withholds an operation in an item, the drafting service shall keep the operation in the item.

### [g35] Removing a capability from an item takes it and its model lines out
- [r35] While an item holds a capability and the item holds a model line, when the person removes the capability from the item, the drafting service shall not keep the capability in the item and not keep the model line in the item.

### [g36] Drafting a new capability that another item holds is refused naming that item
- [r36] While an item holds a capability that does not exist, if the person drafts another item with the capability, then the drafting service shall refuse the request and name another item that holds the capability.

### [g37] Drafting into a new capability an in-batch item holds is refused naming the item and its batch
- [r37] While a batch holds an item and the item holds a capability that does not exist, if the person drafts another item with a requirement of the capability, then the drafting service shall refuse the request and name the batch and another item that holds the capability.

### [g38] A requirement of an in-batch item is reworded
- [r38] While an item is `in-batch`, when the person rewords a requirement in the item, the drafting service shall keep a different requirement in the item.

### [g39] A requirement drafted into an in-batch item is kept
- [r39] While an item is `in-batch`, when the person drafts the item with a requirement, the drafting service shall keep the requirement in the item.

### [g40] A requirement removed from an in-batch item is not kept
- [r40] While an item is `in-batch`, when the person removes a requirement in the item, the drafting service shall not keep the requirement in the item.

### [g41] A model line that restates an operation is kept in the item
- [r41] While a model line restates an operation, when the person declares the model line in an item, the drafting service shall keep the model line in the item.

### [g42] An operation exposed in an item without a table given gets its table from the domain model
- [r42] When the person exposes the operation table of an operation in an item, the drafting service shall keep the operation table that conforms to the operation-table form and keep the operation table in the item.

### [g43] A model line removed from an item leaves it
- [r43] When the person removes a model line from an item, the drafting service shall not keep the model line in the item.

### [g44] Removing a model line that an item does not hold is refused
- [r44] If the person removes a model line from an item that does not hold the model line, then the drafting service shall refuse the request and name the model line.

### [g45] Rewording a model line of an item keeps the new model line
- [r45] When the person rewords a model line in an item, the drafting service shall keep a different model line in the item.

### [g46] Rewording a model line that an item does not hold is refused
- [r46] If the person rewords a model line in an item that does not hold the model line, then the drafting service shall refuse the request and name the model line.

### [g47] A term removed from an item leaves it
- [r47] When the person removes a term from an item, the drafting service shall not keep the term in the item.

### [g48] Removing a term that an item does not hold is refused
- [r48] If the person removes a term from an item that does not hold the term, then the drafting service shall refuse the request and name the term.

### [g50] Rewording a term that an item does not hold is refused
- [r50] If the person rewords a term in an item that does not hold the term, then the drafting service shall refuse the request and name the term.

### [g51] A term written into a pack for an item is kept
- [r51] When the person writes a term into a pack with an item, the drafting service shall keep the term in the item.

### [g52] A term that its pack has already is refused
- [r52] While a pack has a term, if the person writes the term into the pack with an item, then the drafting service shall refuse the request and name the term.

### [g53] A universal condition removed from an item is no longer kept
- [r53] When the person removes a universal condition from an item, the drafting service shall not keep the universal condition in the item.

### [g54] An upstream entry removed from an item is no longer kept
- [r54] When the person removes an upstream entry from an item, the drafting service shall not keep the upstream entry in the item.

### [g55] A given block removed from an item is no longer kept
- [r55] When the person removes a given block from an item, the drafting service shall not keep the given block in the item.

### [g56] Removing a universal condition that the item does not hold is refused
- [r56] If the person removes a universal condition from an item that does not hold the universal condition, then the drafting service shall refuse the request and name the universal condition.

### [g57] Removing an upstream entry that the item does not hold is refused
- [r57] If the person removes an upstream entry from an item that does not hold the upstream entry, then the drafting service shall refuse the request and name the upstream entry.

### [g58] Removing a given block that the item does not hold is refused
- [r58] If the person removes a given block from an item that does not hold the given block, then the drafting service shall refuse the request and name the given block.

### [g59] A universal condition replaced in an item keeps the new one
- [r59] When the person replaces a universal condition in an item, the drafting service shall keep a different universal condition in the item.

### [g60] An upstream entry replaced in an item keeps the new one
- [r60] When the person replaces an upstream entry in an item, the drafting service shall keep a different upstream entry in the item.

### [g61] A given block replaced in an item keeps the new one
- [r61] When the person replaces a given block in an item, the drafting service shall keep a different given block in the item.

### [g62] Replacing a universal condition that the item does not hold is refused
- [r62] If the person replaces a universal condition in an item that does not hold the universal condition, then the drafting service shall refuse the request and name the universal condition.

### [g63] Replacing an upstream entry that the item does not hold is refused
- [r63] If the person replaces an upstream entry in an item that does not hold the upstream entry, then the drafting service shall refuse the request and name the upstream entry.

### [g64] Replacing a given block that the item does not hold is refused
- [r64] If the person replaces a given block in an item that does not hold the given block, then the drafting service shall refuse the request and name the given block.

### [g65] A requirement drafted into an item joins its group of the same group title
- [r65] While an item holds a requirement group of a capability and the requirement group has a group title, when the person drafts the item with a requirement of the capability, the drafting service shall keep only one requirement group that has the group title.

### [g66] A model line moved in an item is kept
- [r66] When the person moves a model line in an item, the drafting service shall keep the model line in the item.

### [g67] Moving a model line that the domain model does not hold is refused
- [r67] If the person moves a model line that the domain model does not hold in an item, then the drafting service shall refuse the request and name the model line.

### [g68] A term moved in an item is kept
- [r68] When the person moves a term in an item, the drafting service shall keep the term in the item.

### [g69] Moving a term that no area holds is refused
- [r69] If the person moves a term that no area holds in an item, then the drafting service shall refuse the request and name the term.

### [g70] A restatement that leaves out a member line of its element names the member line
- [r70] While a model line restates an element and the element holds a member line that the model line does not hold, when the person declares the model line in an item, the drafting service shall keep the model line in the item and name the member line.

### [g71] A requirement group dedicated to a job serves the job in the item
- [r71] When the person dedicates a requirement group to a job with an item, the drafting service shall keep the item that holds the requirement group that serves the job.

### [g72] A new capability drafted with an area is kept in that area
- [r72] When the person drafts an item with a capability and an area, the drafting service shall keep the capability in the item and keep the area that holds the capability in the item.

### [g73] A plugin pack imported into an item is kept
- [r73] When the person imports a pack into an item, the drafting service shall keep the item that imports the pack.

### [g74] Importing a pack that does not exist is refused
- [r74] If the person imports a pack that does not exist into an item, then the drafting service shall refuse the request and name the pack.

### [g75] A model line retired in an item is kept
- [r75] When the person retires a model line in an item, the drafting service shall keep the model line in the item.

### [g76] Retiring a model line that the domain model does not hold is refused
- [r76] If the person retires a model line that the domain model does not hold in an item, then the drafting service shall refuse the request and name the model line.

### [g77] A term retired in an item is kept
- [r77] When the person retires a term in an item, the drafting service shall keep the term in the item.

### [g78] Retiring a term that no area holds is refused
- [r78] If the person retires a term that no area holds in an item, then the drafting service shall refuse the request and name the term.

### [g79] A model line reinstated in an item is no longer retired
- [r79] When the person reinstates a model line in an item, the drafting service shall keep an item that does not retire the model line.

### [g80] Reinstating a model line that the item does not retire is refused
- [r80] If the person reinstates a model line in an item that does not retire the model line, then the drafting service shall refuse the request and name the model line.

### [g81] A term reinstated in an item is no longer retired
- [r81] When the person reinstates a term in an item, the drafting service shall keep an item that does not retire the term.

### [g82] Reinstating a term that the item does not retire is refused
- [r82] If the person reinstates a term in an item that does not retire the term, then the drafting service shall refuse the request and name the term.

### [g83] A pack import removed from an item is no longer imported
- [r83] When the person removes a pack from an item, the drafting service shall keep an item that does not import the pack.

### [g84] Removing a pack that the item does not import is refused
- [r84] If the person removes a pack from an item that does not import the pack, then the drafting service shall refuse the request and name the pack.

### [g85] A capability drafted with a driven port keeps the port in the item
- [r85] When the person drafts an item with a capability and a driven port, the drafting service shall keep the capability in the item and keep the driven port that holds the capability in the item.

### [g86] A port line drafted with the core lines it supports is kept in the item
- [r86] When the person drafts an item with a requirement that supports a requirement id, the drafting service shall keep the requirement in the item.

### [g87] A port line drafted as supporting a requirement id no requirement has is refused
- [r87] If the person drafts an item with a requirement that supports a requirement id that no requirement has, then the drafting service shall refuse the request and name the requirement id.

### [g88] A port line drafted with the core lines it supports keeps the requirement id it retires
- [r88] While a requirement supports a requirement id, when the person drafts an item with the requirement and a different requirement id, the drafting service shall keep the requirement in the item and keep the requirement id in the item.

### [g90] A requirement id reinstated in an item is no longer retired by it
- [r90] When the person reinstates a requirement id in an item, the drafting service shall keep an item that does not hold the requirement id.

### [g89] Reinstating a requirement id that the item does not retire is refused
- [r89] If the person reinstates a requirement id in an item that does not hold the requirement id, then the drafting service shall refuse the request and name the requirement id.

### [g91] Reinstating a requirement id takes the retirement of the item's own requirement out
- [r91] When the person reinstates a requirement id in an item that holds a requirement that retires the requirement id, the drafting service shall keep an item that holds no requirement that retires the requirement id.

### [g92] Dedicating a requirement group to a job the product does not hold is refused
- [r92] While the product exists, if the person dedicates a requirement group to a job that the product does not hold with an item, then the drafting service shall refuse the request and name the job.

### [g93] A requirement drafted for a job is named with the job
- [r93] When the person dedicates a requirement group to a job with an item and a requirement, the drafting service shall keep the requirement in the item and name the requirement, the requirement group and the job.

### [g94] A term that violates v_t6 is kept and the rule named
- [r94] While a term violates `v_t6`, when the person writes the term into an item, the drafting service shall keep the term in the item, name `v_t6` and complete the request.

### [g95] Rewording a term of an item in a capability keeps the new term
- [r95] When the person rewords a term in an item with a capability, the drafting service shall keep a different term in the item.

### [g96] A requirement group dedicated to a job of a product not of the product form is kept and the product named
- [r96] While this product does not conform to the product form, when the person dedicates a requirement group to a job with an item, the drafting service shall keep the item that holds the requirement group that serves the job and name this product.

### [g97] A requirement group dedicated to a job the product holds, given by the job's id, is kept
- [r97] While this product holds a job and the job has an id, when the person dedicates a requirement group to the job with an item, the drafting service shall keep the item that holds the requirement group that serves the job.

### [g98] A requirement drafted into an item is returned with its id
- [r98] When the person drafts an item with a requirement, the drafting service shall return the requirement id of the requirement and the requirement.

### [g101] work line --term refuses a verb with no aspect, no Frame: or a Frame: that does not read
- [r101] While a term violates `v_t4`, `v_t7`, `v_t11`, `v_t13`, `v_t14` or `v_t19`, if the person writes the term into an item, then the drafting service shall refuse the request and name the term and every rule that the term violates.

### [g102] Rewording a term into one that breaks a lexicon rule is refused naming each rule
- [r102] While a term violates `v_t4`, `v_t7`, `v_t11`, `v_t13`, `v_t14` or `v_t19`, if the person rewords the term in an item, then the drafting service shall refuse the request and name the term and every rule that the term violates.

### [g108] A term whose part of speech does not fit the element it means is refused
- [r108] While a term means an element that the term does not fit, if the person writes the term into an item, then the drafting service shall refuse the request and name the term.

### [g109] Rewording a term into one whose part of speech does not fit the element it means is refused
- [r109] While a term means an element that the term does not fit, if the person rewords the term in an item, then the drafting service shall refuse the request and name the term.

### [g107] Rewording a requirement to the text the item holds changes nothing
- [r107] While an item holds a requirement, if the person rewords the requirement in the item with the same text, then the drafting service shall change nothing and name the requirement.

### [g103] A term written into an item is returned
- [r103] When the person writes a term into an item, the drafting service shall return the term.

### [g105] A reworded term is kept, returned and the request completed
- [r105] When the person rewords a term in an item, the drafting service shall keep a different term in the item, return the term and complete the request.

### [g106] A reworded requirement is kept and returned with its id
- [r106] When the person rewords a requirement in an item, the drafting service shall keep a different requirement in the item and return the requirement id of the requirement and the requirement.

