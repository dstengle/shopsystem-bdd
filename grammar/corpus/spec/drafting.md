# drafting: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: readiness#r26, reworded in request words (0.38.0).

```reading
When the person drafts an item with a relation row, the drafting service shall keep the relation row in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: item, x3: relation row]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, relation row, x3)
  response
    in(x3, x2)
    keep(e2, subject: x4, object: x3)
```

## r2
From: readiness#r27, reworded in request words (0.38.0).

```reading
If the person drafts an item with a relation row that does not conform to the relation-row form, then the drafting service shall refuse the request and name the relation row.
shall [x1: agent the person (constant), x4: artifact the relation-row form (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: item, x3: relation row]
    not
      conforms(x3, x4)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, relation row, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r3
From: readiness#r28, reworded in request words (0.38.0).

```reading
When the person drafts an item with a universal condition, the drafting service shall keep the universal condition in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: item, x3: universal condition]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, universal condition, x3)
  response
    in(x3, x2)
    keep(e2, subject: x4, object: x3)
```

## r4
From: readiness#r29, reworded in request words (0.38.0).

```reading
When the person drafts an item with an upstream entry, the drafting service shall keep the upstream entry in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: item, x3: upstream entry]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, upstream entry, x3)
  response
    in(x3, x2)
    keep(e2, subject: x4, object: x3)
```

## r5
From: readiness#r30, reworded in request words (0.38.0).

```reading
If the person drafts an item with an upstream entry that does not conform to the upstream-entry form, then the drafting service shall refuse the request and name the upstream entry.
shall [x1: agent the person (constant), x4: artifact the upstream-entry form (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: item, x3: upstream entry]
    not
      conforms(x3, x4)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, upstream entry, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r6
From: readiness#r31, reworded in request words (0.38.0).

```reading
When the person drafts an item with a given block, the drafting service shall keep the given block in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: item, x3: given block]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, given block, x3)
  response
    in(x3, x2)
    keep(e2, subject: x4, object: x3)
```

## r7
From: readiness#r32, reworded in request words (0.38.0).

```reading
If the person drafts an item with a given block that does not conform to the example-data form, then the drafting service shall refuse the request and name the given block.
shall [x1: agent the person (constant), x4: artifact the example-data form (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: item, x3: given block]
    not
      conforms(x3, x4)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, given block, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r8
From: readiness#r34, reworded in request words (0.38.0).

```reading
When the person drafts an item with a requirement id, the drafting service shall keep a requirement in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: item, x3: requirement id]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, requirement id, x3)
  response [x5: requirement]
    in(x5, x2)
    keep(e2, subject: x4, object: x5)
```

## r9
From: readiness#r35, reworded in request words (0.38.0).

```reading
If the person drafts an item with a requirement id that no requirement has, then the drafting service shall refuse the request and name the requirement id.
shall [x1: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: item, x3: requirement id]
    not [x4: requirement]
      of(x3, x4)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, requirement id, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r10
From: readiness#r37, reworded in request words (0.38.0).

```reading
When the person recodifies a capability in an item, the drafting service shall set the language of the capability in the item to `codified-2` and keep the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: capability, x3: item]
    request(e1, drafting.recodify, subject: x1, object: x2, in: x3)
  response
    in(x2, x3)
    initiates(e2, subject: x4, language(x2) = `codified-2`)
    keep(e3, subject: x4, object: x3)
```

## r11
From: readiness#r38, reworded in request words (0.38.0).

```reading
When the person recodifies `universal` in an item, the drafting service shall set the language of the capability in the item to `codified-2` and keep the item.
shall [x1: agent the person (constant), x2: capability `universal` (constant), x4: service the drafting service (constant)]
  when [x3: item]
    request(e1, drafting.recodify, subject: x1, object: x2, in: x3)
  response
    in(x2, x3)
    initiates(e2, subject: x4, language(x2) = `codified-2`)
    keep(e3, subject: x4, object: x3)
```

## r12
From: readiness#r39, reworded in request words (0.38.0).

```reading
When the person drafts an item with a universal condition id, the drafting service shall keep a universal condition in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: item, x3: universal condition id]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, universal condition id, x3)
  response [x5: universal condition]
    in(x5, x2)
    keep(e2, subject: x4, object: x5)
```

## r13
From: readiness#r40, reworded in request words (0.38.0).

```reading
If the person drafts an item with a universal condition id that no universal condition has, then the drafting service shall refuse the request and name the universal condition id.
shall [x1: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: item, x3: universal condition id]
    not [x4: universal condition]
      of(x3, x4)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, universal condition id, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r14
From: readiness#r42, reworded in request words (0.38.0).

```reading
When the person rewords a requirement in an item, the drafting service shall keep a different requirement in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: requirement, x3: item]
    in(x2, x3)
    request(e1, drafting.reword, subject: x1, object: x2)
  response [x5: requirement]
    distinct(x5, x2)
    in(x5, x3)
    keep(e2, subject: x4, object: x5)
```

## r15
From: readiness#r44, reworded in request words (0.38.0).

```reading
If the person rewords a requirement of a capability, then the drafting service shall refuse the request and name the requirement.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: capability]
    of(x2, x3)
    request(e1, drafting.reword, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r16
From: readiness#r45, reworded in request words (0.38.0).

```reading
If the person removes a requirement of a capability, then the drafting service shall refuse the request and name the requirement.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: requirement, x3: capability]
    of(x2, x3)
    request(e1, drafting.remove, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r17
From: readiness#r47, reworded in request words (0.38.0).

```reading
When the person drafts an item with a requirement id and without a requirement, the drafting service shall keep the requirement id in the item and not keep a requirement in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: item, x3: requirement id]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, requirement id, x3)
    noparam(e1, requirement)
  response
    in(x3, x2)
    keep(e2, subject: x4, object: x3)
    not [x5: requirement]
      in(x5, x2)
      keep(e3, subject: x4, object: x5)
```

## r18
From: readiness#r48, reworded in request words (0.38.0).

```reading
If the person drafts an item with a requirement id that no requirement has and without a requirement, then the drafting service shall refuse the request and name the requirement id.
shall [x1: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: item, x3: requirement id]
    not [x4: requirement]
      of(x3, x4)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, requirement id, x3)
    noparam(e1, requirement)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r19
From: readiness#r51, reworded in request words (0.38.0).

```reading
When the person assigns a chore to an item, the drafting service shall keep the chore in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: chore, x3: item]
    request(e1, drafting.assign, subject: x1, object: x2, to: x3)
  response
    in(x2, x3)
    keep(e2, subject: x4, object: x2)
```

## r20
From: readiness#r52, reworded in request words (0.38.0).

```reading
If the person assigns a chore to an item that holds a requirement, then the drafting service shall refuse the request and name the requirement.
shall [x1: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: chore, x3: item, x4: requirement]
    in(x4, x3)
    request(e1, drafting.assign, subject: x1, object: x2, to: x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x4)
```

## r21
From: readiness#r53, reworded in request words (0.38.0).

```reading
If the person drafts an item that holds a chore, then the drafting service shall refuse the request and name the chore.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: item, x3: chore]
    in(x3, x2)
    request(e1, drafting.draft, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x3)
```

## r22
From: readiness#r55, reworded in request words (0.38.0).

```reading
When the person drafts an item with a capability, the drafting service shall keep the capability in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: item, x3: capability]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, capability, x3)
  response
    in(x3, x2)
    keep(e2, subject: x4, object: x3)
```

## r23
From: readiness#r56, reworded in request words (0.38.0).

```reading
If the person drafts an item with a capability that exists, then the drafting service shall refuse the request and name the capability.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: item, x3: capability]
    exists(x3)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, capability, x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x3)
```

## r24
From: readiness#r57, reworded in request words (0.38.0).

```reading
When the person removes a requirement in an item, the drafting service shall keep every requirement id in the item that the requirement does not retire.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: requirement, x3: item]
    in(x2, x3)
    request(e1, drafting.remove, subject: x1, object: x2)
  response
    every [x5: requirement id]
      in(x5, x3)
      not
        retire(subject: x2, object: x5)
      scope
        keep(e2, subject: x4, object: x5)
```

## r25
From: b354 r25.

```reading
While an item holds a capability that does not exist, when the person writes a term into the item, the drafting service shall keep the term in the item.
shall [x3: agent the person (constant), x5: service the drafting service (constant)]
  while [x1: item, x2: capability]
    not
      exists(x2)
    in(x2, x1)
  when [x4: term]
    request(e1, drafting.write, subject: x3, object: x4, into: x1)
  response
    in(x4, x1)
    keep(e2, subject: x5, object: x4)
```

## r26
From: b387 r26.

```reading
While an item holds a capability that does not exist, when the person declares a model line in the item, the drafting service shall keep the model line in the item.
shall [x3: agent the person (constant), x5: service the drafting service (constant)]
  while [x1: item, x2: capability]
    not
      exists(x2)
    in(x2, x1)
  when [x4: model line]
    request(e1, drafting.declare, subject: x3, object: x4, in: x1)
  response
    in(x4, x1)
    keep(e2, subject: x5, object: x4)
```

## r27
From: b448 r27.

```reading
While an item holds a capability that does not exist, when the person removes a requirement of the capability, the drafting service shall keep the capability in the item.
shall [x3: agent the person (constant), x5: service the drafting service (constant)]
  while [x1: item, x2: capability]
    not
      exists(x2)
    in(x2, x1)
  when [x4: requirement]
    of(x4, x2)
    request(e1, drafting.remove, subject: x3, object: x4)
  response
    in(x2, x1)
    keep(e2, subject: x5, object: x2)
```

## r28
From: b458 r28.

```reading
When the person drafts an item with a requirement id of a requirement that enforces a design-decision, the drafting service shall keep a requirement in the item and name the design-decision.
shall [x1: agent the person (constant), x6: service the drafting service (constant)]
  when [x2: item, x3: requirement id, x4: requirement, x5: design-decision]
    enforce(subject: x4, object: x5)
    of(x3, x4)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, requirement id, x3)
  response [x7: requirement]
    in(x7, x2)
    keep(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x5)
```

## r29
From: b461 r29.

```reading
When the person applies a retirement list to an item, the drafting service shall keep the item and every requirement that the retirement list holds.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: retirement list, x3: item]
    request(e1, drafting.apply, subject: x1, object: x2, to: x3)
  response
    keep(e2, subject: x4, object: x3)
    every [x5: requirement]
      in(x5, x2)
      scope
        keep(e3, subject: x4, object: x5)
```

## r30
From: b461 r30.

```reading
If the person applies a retirement list that holds a requirement id that no requirement has to an item, then the drafting service shall refuse the request, name the requirement id and not keep the item.
shall [x1: agent the person (constant), x6: service the drafting service (constant), x7: request "the request the trigger makes" (indexical)]
  if [x2: retirement list, x3: requirement id, x5: item]
    not [x4: requirement]
      of(x3, x4)
    in(x3, x2)
    request(e1, drafting.apply, subject: x1, object: x2, to: x5)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x3)
    not
      keep(e4, subject: x6, object: x5)
```

## r31
From: b355 r31.

```reading
When the person exposes an operation table in an item, the drafting service shall keep the operation table in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: operation table, x3: item]
    request(e1, drafting.expose, subject: x1, object: x2, in: x3)
  response
    in(x2, x3)
    keep(e2, subject: x4, object: x2)
```

## r32
From: b355 r32.

```reading
While an operation does not exist, if the person exposes an operation table of the operation in an item, then the drafting service shall refuse the request and name the operation table.
shall [x2: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: operation]
    not
      exists(x1)
  if [x3: operation table, x4: item]
    of(x3, x1)
    request(e1, drafting.expose, subject: x2, object: x3, in: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r33
From: b355 r33.

```reading
While an item holds an operation table of an operation, when the person exposes another operation table of the operation in the item, the drafting service shall keep only one operation table of the operation in the item.
shall [x4: agent the person (constant), x6: service the drafting service (constant)]
  while [x1: item, x2: operation table, x3: operation]
    of(x2, x3)
    in(x2, x1)
  when [x5: operation table]
    distinct(x5, x2)
    of(x5, x3)
    request(e1, drafting.expose, subject: x4, object: x5, in: x1)
  response
    only [x7: operation table]
      in(x3, x1)
      of(x7, x3)
      scope
        keep(e2, subject: x6, object: x7)
```

## r34
From: b355 r34.

```reading
When the person withholds an operation in an item, the drafting service shall keep the operation in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: operation, x3: item]
    request(e1, drafting.withhold, subject: x1, object: x2, in: x3)
  response
    in(x2, x3)
    keep(e2, subject: x4, object: x2)
```

## r35
From: b450 r35.

```reading
While an item holds a capability and the item holds a model line, when the person removes the capability from the item, the drafting service shall not keep the capability in the item and not keep the model line in the item.
shall [x4: agent the person (constant), x5: service the drafting service (constant)]
  while [x1: item, x2: capability, x3: model line]
    in(x2, x1)
    in(x3, x1)
  when
    request(e1, drafting.retract, subject: x4, object: x2, from: x1)
  response
    not
      in(x2, x1)
      keep(e2, subject: x5, object: x2)
    not
      in(x3, x1)
      keep(e3, subject: x5, object: x3)
```

## r36
From: b450 r36.

```reading
While an item holds a capability that does not exist, if the person drafts another item with the capability, then the drafting service shall refuse the request and name another item that holds the capability.
shall [x3: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: capability]
    not
      exists(x2)
    in(x2, x1)
  if [x4: item]
    distinct(x4, x1)
    request(e1, drafting.draft, subject: x3, object: x4)
    param(e1, capability, x2)
  response [x7: item]
    refuse(e2, subject: x5, object: x6)
    distinct(x7, x4)
    in(x2, x7)
    name(e3, subject: x5, object: x7)
```

## r37
From: b450 r37.

```reading
While a batch holds an item and the item holds a capability that does not exist, if the person drafts another item with a requirement of the capability, then the drafting service shall refuse the request and name the batch and another item that holds the capability.
shall [x4: agent the person (constant), x7: service the drafting service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: batch, x2: item, x3: capability]
    in(x2, x1)
    not
      exists(x3)
    in(x3, x2)
  if [x5: item, x6: requirement]
    distinct(x5, x2)
    of(x6, x3)
    request(e1, drafting.draft, subject: x4, object: x5)
    param(e1, requirement, x6)
  response [x9: item]
    refuse(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x1)
    distinct(x9, x5)
    in(x3, x9)
    name(e4, subject: x7, object: x9)
```

## r38
From: b460 r38.

```reading
While an item is `in-batch`, when the person rewords a requirement in the item, the drafting service shall keep a different requirement in the item.
shall [x2: agent the person (constant), x4: service the drafting service (constant)]
  while [x1: item]
    status(x1) = `in-batch`
  when [x3: requirement]
    in(x3, x1)
    request(e1, drafting.reword, subject: x2, object: x3)
  response [x5: requirement]
    distinct(x5, x3)
    in(x5, x1)
    keep(e2, subject: x4, object: x5)
```

## r39
From: b460 r39.

```reading
While an item is `in-batch`, when the person drafts the item with a requirement, the drafting service shall keep the requirement in the item.
shall [x2: agent the person (constant), x4: service the drafting service (constant)]
  while [x1: item]
    status(x1) = `in-batch`
  when [x3: requirement]
    request(e1, drafting.draft, subject: x2, object: x1)
    param(e1, requirement, x3)
  response
    in(x3, x1)
    keep(e2, subject: x4, object: x3)
```

## r40
From: b460 r40.

```reading
While an item is `in-batch`, when the person removes a requirement in the item, the drafting service shall not keep the requirement in the item.
shall [x2: agent the person (constant), x4: service the drafting service (constant)]
  while [x1: item]
    status(x1) = `in-batch`
  when [x3: requirement]
    in(x3, x1)
    request(e1, drafting.remove, subject: x2, object: x3)
  response
    not
      in(x3, x1)
      keep(e2, subject: x4, object: x3)
```

## r41
From: b463 r41.

```reading
While a model line restates an operation, when the person declares the model line in an item, the drafting service shall keep the model line in the item.
shall [x3: agent the person (constant), x5: service the drafting service (constant)]
  while [x1: model line, x2: operation]
    restate#2(subject: x1, object: x2)
  when [x4: item]
    request(e1, drafting.declare, subject: x3, object: x1, in: x4)
  response
    in(x1, x4)
    keep(e2, subject: x5, object: x1)
```

## r42
From: b482 r42.

```reading
When the person exposes the operation table of an operation in an item, the drafting service shall keep the operation table that conforms to the operation-table form and keep the operation table in the item.
shall [x1: agent the person (constant), x5: service the drafting service (constant), x6: artifact the operation-table form (constant)]
  when [x2: operation, x3: operation table, x4: item]
    of(x3, x2)
    request(e1, drafting.expose, subject: x1, object: x3, in: x4)
  response
    conforms(x3, x6)
    keep(e2, subject: x5, object: x3)
    in(x3, x4)
    keep(e3, subject: x5, object: x3)
```

## r43
From: b367 r43.

```reading
When the person removes a model line from an item, the drafting service shall not keep the model line in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: model line, x3: item]
    request(e1, drafting.remove model line, subject: x1, object: x2, from: x3)
  response
    not
      in(x2, x3)
      keep(e2, subject: x4, object: x2)
```

## r44
From: b367 r44.

```reading
If the person removes a model line from an item that does not hold the model line, then the drafting service shall refuse the request and name the model line.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: model line, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.remove model line, subject: x1, object: x2, from: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r45
From: b367 r45.

```reading
When the person rewords a model line in an item, the drafting service shall keep a different model line in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: model line, x3: item]
    request(e1, drafting.reword model line, subject: x1, object: x2, in: x3)
  response [x5: model line]
    distinct(x5, x2)
    in(x5, x3)
    keep(e2, subject: x4, object: x5)
```

## r46
From: b367 r46.

```reading
If the person rewords a model line in an item that does not hold the model line, then the drafting service shall refuse the request and name the model line.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: model line, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.reword model line, subject: x1, object: x2, in: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r47
From: b367 r47.

```reading
When the person removes a term from an item, the drafting service shall not keep the term in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: term, x3: item]
    request(e1, drafting.remove term, subject: x1, object: x2, from: x3)
  response
    not
      in(x2, x3)
      keep(e2, subject: x4, object: x2)
```

## r48
From: b367 r48.

```reading
If the person removes a term from an item that does not hold the term, then the drafting service shall refuse the request and name the term.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: term, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.remove term, subject: x1, object: x2, from: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r49
From: b367 r49.

```reading
When the person rewords a term in an item, the drafting service shall keep a different term in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: term, x3: item]
    request(e1, drafting.reword term, subject: x1, object: x2, in: x3)
  response [x5: term]
    distinct(x5, x2)
    in(x5, x3)
    keep(e2, subject: x4, object: x5)
```

## r50
From: b367 r50.

```reading
If the person rewords a term in an item that does not hold the term, then the drafting service shall refuse the request and name the term.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: term, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.reword term, subject: x1, object: x2, in: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r51
From: b472 r51.

```reading
When the person writes a term into a pack with an item, the drafting service shall keep the term in the item.
shall [x1: agent the person (constant), x5: service the drafting service (constant)]
  when [x2: term, x3: pack, x4: item]
    request(e1, drafting.write into pack, subject: x1, object: x2, into: x3)
    param(e1, item, x4)
  response
    in(x2, x4)
    keep(e2, subject: x5, object: x2)
```

## r52
From: b472 r52.

```reading
While a pack has a term, if the person writes the term into the pack with an item, then the drafting service shall refuse the request and name the term.
shall [x3: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: pack, x2: term]
    of(x2, x1)
  if [x4: item]
    request(e1, drafting.write into pack, subject: x3, object: x2, into: x1)
    param(e1, item, x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r53
From: b48 r53.

```reading
When the person removes a universal condition from an item, the drafting service shall not keep the universal condition in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: universal condition, x3: item]
    request(e1, drafting.take out, subject: x1, object: x2, from: x3)
  response
    not
      in(x2, x3)
      keep(e2, subject: x4, object: x2)
```

## r54
From: b48 r54.

```reading
When the person removes an upstream entry from an item, the drafting service shall not keep the upstream entry in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: upstream entry, x3: item]
    request(e1, drafting.take out, subject: x1, object: x2, from: x3)
  response
    not
      in(x2, x3)
      keep(e2, subject: x4, object: x2)
```

## r55
From: b48 r55.

```reading
When the person removes a given block from an item, the drafting service shall not keep the given block in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: given block, x3: item]
    request(e1, drafting.take out, subject: x1, object: x2, from: x3)
  response
    not
      in(x2, x3)
      keep(e2, subject: x4, object: x2)
```

## r56
From: b48 r56.

```reading
If the person removes a universal condition from an item that does not hold the universal condition, then the drafting service shall refuse the request and name the universal condition.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: universal condition, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.take out, subject: x1, object: x2, from: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r57
From: b48 r57.

```reading
If the person removes an upstream entry from an item that does not hold the upstream entry, then the drafting service shall refuse the request and name the upstream entry.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: upstream entry, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.take out, subject: x1, object: x2, from: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r58
From: b48 r58.

```reading
If the person removes a given block from an item that does not hold the given block, then the drafting service shall refuse the request and name the given block.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: given block, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.take out, subject: x1, object: x2, from: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r59
From: b48 r59.

```reading
When the person replaces a universal condition in an item, the drafting service shall keep a different universal condition in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: universal condition, x3: item]
    request(e1, drafting.replace, subject: x1, object: x2, in: x3)
  response [x5: universal condition]
    distinct(x5, x2)
    in(x5, x3)
    keep(e2, subject: x4, object: x5)
```

## r60
From: b48 r60.

```reading
When the person replaces an upstream entry in an item, the drafting service shall keep a different upstream entry in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: upstream entry, x3: item]
    request(e1, drafting.replace, subject: x1, object: x2, in: x3)
  response [x5: upstream entry]
    distinct(x5, x2)
    in(x5, x3)
    keep(e2, subject: x4, object: x5)
```

## r61
From: b48 r61.

```reading
When the person replaces a given block in an item, the drafting service shall keep a different given block in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: given block, x3: item]
    request(e1, drafting.replace, subject: x1, object: x2, in: x3)
  response [x5: given block]
    distinct(x5, x2)
    in(x5, x3)
    keep(e2, subject: x4, object: x5)
```

## r62
From: b48 r62.

```reading
If the person replaces a universal condition in an item that does not hold the universal condition, then the drafting service shall refuse the request and name the universal condition.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: universal condition, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.replace, subject: x1, object: x2, in: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r63
From: b48 r63.

```reading
If the person replaces an upstream entry in an item that does not hold the upstream entry, then the drafting service shall refuse the request and name the upstream entry.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: upstream entry, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.replace, subject: x1, object: x2, in: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r64
From: b48 r64.

```reading
If the person replaces a given block in an item that does not hold the given block, then the drafting service shall refuse the request and name the given block.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: given block, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.replace, subject: x1, object: x2, in: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r65
From: b583 r65.

```reading
While an item holds a requirement group of a capability and the requirement group has a group title, when the person drafts the item with a requirement of the capability, the drafting service shall keep only one requirement group that has the group title.
shall [x5: agent the person (constant), x7: service the drafting service (constant)]
  while [x1: item, x2: requirement group, x3: capability, x4: group title]
    of(x2, x3)
    in(x2, x1)
    of(x4, x2)
  when [x6: requirement]
    of(x6, x3)
    request(e1, drafting.draft, subject: x5, object: x1)
    param(e1, requirement, x6)
  response
    only [x8: requirement group]
      of(x4, x8)
      scope
        keep(e2, subject: x7, object: x8)
```

## r66
From: b607 r66.

```reading
When the person moves a model line in an item, the drafting service shall keep the model line in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: model line, x3: item]
    request(e1, drafting.move, subject: x1, object: x2, in: x3)
  response
    in(x2, x3)
    keep(e2, subject: x4, object: x2)
```

## r67
From: b607 r67.

```reading
If the person moves a model line that the domain model does not hold in an item, then the drafting service shall refuse the request and name the model line.
shall [x1: agent the person (constant), x3: domain model "the domain model of this bounded context" (indexical), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: model line, x4: item]
    not
      in(x2, x3)
    request(e1, drafting.move, subject: x1, object: x2, in: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r68
From: b607 r68.

```reading
When the person moves a term in an item, the drafting service shall keep the term in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: term, x3: item]
    request(e1, drafting.move term, subject: x1, object: x2, in: x3)
  response
    in(x2, x3)
    keep(e2, subject: x4, object: x2)
```

## r69
From: b607 r69.

```reading
If the person moves a term that no area holds in an item, then the drafting service shall refuse the request and name the term.
shall [x1: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: term, x4: item]
    not [x3: area]
      in(x2, x3)
    request(e1, drafting.move term, subject: x1, object: x2, in: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```
