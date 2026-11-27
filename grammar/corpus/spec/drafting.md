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

## r70
From: b647 r70.

```reading
While a model line restates an element and the element holds a member line that the model line does not hold, when the person declares the model line in an item, the drafting service shall keep the model line in the item and name the member line.
shall [x4: agent the person (constant), x6: service the drafting service (constant)]
  while [x1: model line, x2: element, x3: member line]
    restate(subject: x1, object: x2)
    not
      in(x3, x1)
    in(x3, x2)
  when [x5: item]
    request(e1, drafting.declare, subject: x4, object: x1, in: x5)
  response
    in(x1, x5)
    keep(e2, subject: x6, object: x1)
    name(e3, subject: x6, object: x3)
```

## r71
From: b641 r71.

```reading
When the person dedicates a requirement group to a job with an item, the drafting service shall keep the item that holds the requirement group that serves the job.
shall [x1: agent the person (constant), x5: service the drafting service (constant)]
  when [x2: requirement group, x3: job, x4: item]
    request(e1, drafting.dedicate, subject: x1, object: x2, to: x3)
    param(e1, item, x4)
  response
    serve(subject: x2, object: x3)
    in(x2, x4)
    keep(e2, subject: x5, object: x4)
```

## r72
From: b645 r72.

```reading
When the person drafts an item with a capability and an area, the drafting service shall keep the capability in the item and keep the area that holds the capability in the item.
shall [x1: agent the person (constant), x5: service the drafting service (constant)]
  when [x2: item, x3: capability, x4: area]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, capability, x3)
    param(e1, area, x4)
  response
    in(x3, x2)
    keep(e2, subject: x5, object: x3)
    in(x3, x4)
    keep(e3, subject: x5, object: x4)
```

## r73
From: b672 r73.

```reading
When the person imports a pack into an item, the drafting service shall keep the item that imports the pack.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: pack, x3: item]
    request(e1, drafting.import pack, subject: x1, object: x2, into: x3)
  response
    import#5(subject: x3, object: x2)
    keep(e2, subject: x4, object: x3)
```

## r74
From: b672 r74.

```reading
If the person imports a pack that does not exist into an item, then the drafting service shall refuse the request and name the pack.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: pack, x3: item]
    not
      exists(x2)
    request(e1, drafting.import pack, subject: x1, object: x2, into: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r75
From: b672 r75.

```reading
When the person retires a model line in an item, the drafting service shall keep the model line in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: model line, x3: item]
    request(e1, drafting.retire model line, subject: x1, object: x2, in: x3)
  response
    in(x2, x3)
    keep(e2, subject: x4, object: x2)
```

## r76
From: b672 r76.

```reading
If the person retires a model line that the domain model does not hold in an item, then the drafting service shall refuse the request and name the model line.
shall [x1: agent the person (constant), x3: domain model "the domain model of this bounded context" (indexical), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: model line, x4: item]
    not
      in(x2, x3)
    request(e1, drafting.retire model line, subject: x1, object: x2, in: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r77
From: b672 r77.

```reading
When the person retires a term in an item, the drafting service shall keep the term in the item.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: term, x3: item]
    request(e1, drafting.retire term, subject: x1, object: x2, in: x3)
  response
    in(x2, x3)
    keep(e2, subject: x4, object: x2)
```

## r78
From: b672 r78.

```reading
If the person retires a term that no area holds in an item, then the drafting service shall refuse the request and name the term.
shall [x1: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: term, x4: item]
    not [x3: area]
      in(x2, x3)
    request(e1, drafting.retire term, subject: x1, object: x2, in: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r79
From: b688 r79.

```reading
When the person reinstates a model line in an item, the drafting service shall keep an item that does not retire the model line.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: model line, x3: item]
    request(e1, drafting.reinstate model line, subject: x1, object: x2, in: x3)
  response [x5: item]
    not
      retire#4(subject: x5, object: x2)
    keep(e2, subject: x4, object: x5)
```

## r80
From: b688 r80.

```reading
If the person reinstates a model line in an item that does not retire the model line, then the drafting service shall refuse the request and name the model line.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: model line, x3: item]
    not
      retire#4(subject: x3, object: x2)
    request(e1, drafting.reinstate model line, subject: x1, object: x2, in: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r81
From: b688 r81.

```reading
When the person reinstates a term in an item, the drafting service shall keep an item that does not retire the term.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: term, x3: item]
    request(e1, drafting.reinstate term, subject: x1, object: x2, in: x3)
  response [x5: item]
    not
      retire#4(subject: x5, object: x2)
    keep(e2, subject: x4, object: x5)
```

## r82
From: b688 r82.

```reading
If the person reinstates a term in an item that does not retire the term, then the drafting service shall refuse the request and name the term.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: term, x3: item]
    not
      retire#4(subject: x3, object: x2)
    request(e1, drafting.reinstate term, subject: x1, object: x2, in: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r83
From: b688 r83.

```reading
When the person removes a pack from an item, the drafting service shall keep an item that does not import the pack.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: pack, x3: item]
    request(e1, drafting.remove import, subject: x1, object: x2, from: x3)
  response [x5: item]
    not
      import#5(subject: x5, object: x2)
    keep(e2, subject: x4, object: x5)
```

## r84
From: b688 r84.

```reading
If the person removes a pack from an item that does not import the pack, then the drafting service shall refuse the request and name the pack.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: pack, x3: item]
    not
      import#5(subject: x3, object: x2)
    request(e1, drafting.remove import, subject: x1, object: x2, from: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r85
From: b701 r85.

```reading
When the person drafts an item with a capability and a driven port, the drafting service shall keep the capability in the item and keep the driven port that holds the capability in the item.
shall [x1: agent the person (constant), x5: service the drafting service (constant)]
  when [x2: item, x3: capability, x4: driven port]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, capability, x3)
    param(e1, area, x4)
  response
    in(x3, x2)
    keep(e2, subject: x5, object: x3)
    in(x3, x4)
    keep(e3, subject: x5, object: x4)
```

## r86
From: b705 r86.

```reading
When the person drafts an item with a requirement that supports a requirement id, the drafting service shall keep the requirement in the item.
shall [x1: agent the person (constant), x5: service the drafting service (constant)]
  when [x2: item, x3: requirement, x4: requirement id]
    support(subject: x3, object: x4)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, requirement, x3)
  response
    in(x3, x2)
    keep(e2, subject: x5, object: x3)
```

## r87
From: b705 r87.

```reading
If the person drafts an item with a requirement that supports a requirement id that no requirement has, then the drafting service shall refuse the request and name the requirement id.
shall [x1: agent the person (constant), x6: service the drafting service (constant), x7: request "the request the trigger makes" (indexical)]
  if [x2: item, x3: requirement, x4: requirement id]
    not [x5: requirement]
      of(x4, x5)
    support(subject: x3, object: x4)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, requirement, x3)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x4)
```

## r88
From: b759 r88.

```reading
While a requirement supports a requirement id, when the person drafts an item with the requirement and a different requirement id, the drafting service shall keep the requirement in the item and keep the requirement id in the item.
shall [x3: agent the person (constant), x6: service the drafting service (constant)]
  while [x1: requirement, x2: requirement id]
    support(subject: x1, object: x2)
  when [x4: item, x5: requirement id]
    distinct(x5, x2)
    request(e1, drafting.draft, subject: x3, object: x4)
    param(e1, requirement, x1)
    param(e1, requirement id, x5)
  response
    in(x1, x4)
    keep(e2, subject: x6, object: x1)
    in(x5, x4)
    keep(e3, subject: x6, object: x5)
```

## r89
From: b760 r89.

```reading
If the person reinstates a requirement id in an item that does not hold the requirement id, then the drafting service shall refuse the request and name the requirement id.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: requirement id, x3: item]
    not
      in(x2, x3)
    request(e1, drafting.reinstate requirement, subject: x1, object: x2, in: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r90
From: b760 r90.

```reading
When the person reinstates a requirement id in an item, the drafting service shall keep an item that does not hold the requirement id.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: requirement id, x3: item]
    request(e1, drafting.reinstate requirement, subject: x1, object: x2, in: x3)
  response [x5: item]
    not
      in(x2, x5)
    keep(e2, subject: x4, object: x5)
```

## r91
From: b768 r91.

```reading
When the person reinstates a requirement id in an item that holds a requirement that retires the requirement id, the drafting service shall keep an item that holds no requirement that retires the requirement id.
shall [x1: agent the person (constant), x5: service the drafting service (constant)]
  when [x2: requirement id, x3: item, x4: requirement]
    retire(subject: x4, object: x2)
    in(x4, x3)
    request(e1, drafting.reinstate requirement, subject: x1, object: x2, in: x3)
  response [x6: item]
    not [x7: requirement]
      retire(subject: x7, object: x2)
      in(x7, x6)
    keep(e2, subject: x5, object: x6)
```

## r92
From: b799 r92.

```reading
While the product exists, if the person dedicates a requirement group to a job that the product does not hold with an item, then the drafting service shall refuse the request and name the job.
shall [x1: product "the product this bounded context belongs to" (indexical), x2: agent the person (constant), x6: service the drafting service (constant), x7: request "the request the trigger makes" (indexical)]
  while
    exists(x1)
  if [x3: requirement group, x4: job, x5: item]
    not
      in(x4, x1)
    request(e1, drafting.dedicate, subject: x2, object: x3, to: x4)
    param(e1, item, x5)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x4)
```

## r93
From: b799 r93.

```reading
When the person dedicates a requirement group to a job with an item and a requirement, the drafting service shall keep the requirement in the item and name the requirement, the requirement group and the job.
shall [x1: agent the person (constant), x6: service the drafting service (constant)]
  when [x2: requirement group, x3: job, x4: item, x5: requirement]
    request(e1, drafting.dedicate, subject: x1, object: x2, to: x3)
    param(e1, item, x4)
    param(e1, requirement, x5)
  response
    in(x5, x4)
    keep(e2, subject: x6, object: x5)
    name(e3, subject: x6, object: x5)
    name(e4, subject: x6, object: x2)
    name(e5, subject: x6, object: x3)
```

## r94
From: b801 r94.

```reading
While a term violates `v_t6`, when the person writes the term into an item, the drafting service shall keep the term in the item, name `v_t6` and complete the request.
shall [x2: rule `v_t6` (parameter), x3: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: term]
    violate(subject: x1, object: x2)
  when [x4: item]
    request(e1, drafting.write, subject: x3, object: x1, into: x4)
  response
    in(x1, x4)
    keep(e2, subject: x5, object: x1)
    name(e3, subject: x5, object: x2)
    complete(e4, subject: x5, object: x6)
```

## r95
From: b800 r95.

```reading
When the person rewords a term in an item with a capability, the drafting service shall keep a different term in the item.
shall [x1: agent the person (constant), x5: service the drafting service (constant)]
  when [x2: term, x3: item, x4: capability]
    request(e1, drafting.reword term, subject: x1, object: x2, in: x3)
    param(e1, capability, x4)
  response [x6: term]
    distinct(x6, x2)
    in(x6, x3)
    keep(e2, subject: x5, object: x6)
```

## r96
From: b803 r96.

```reading
While this product does not conform to the product form, when the person dedicates a requirement group to a job with an item, the drafting service shall keep the item that holds the requirement group that serves the job and name this product.
shall [x1: product "the product this bounded context belongs to" (indexical), x2: artifact the product form (constant), x3: agent the person (constant), x7: service the drafting service (constant)]
  while
    not
      conforms(x1, x2)
  when [x4: requirement group, x5: job, x6: item]
    request(e1, drafting.dedicate, subject: x3, object: x4, to: x5)
    param(e1, item, x6)
  response
    serve(subject: x4, object: x5)
    in(x4, x6)
    keep(e2, subject: x7, object: x6)
    name(e3, subject: x7, object: x1)
```

## r97
From: b803 r97.

```reading
While this product holds a job and the job has an id, when the person dedicates a requirement group to the job with an item, the drafting service shall keep the item that holds the requirement group that serves the job.
shall [x1: product "the product this bounded context belongs to" (indexical), x4: agent the person (constant), x7: service the drafting service (constant)]
  while [x2: job, x3: id]
    in(x2, x1)
    of(x3, x2)
  when [x5: requirement group, x6: item]
    request(e1, drafting.dedicate, subject: x4, object: x5, to: x2)
    param(e1, item, x6)
  response
    serve(subject: x5, object: x2)
    in(x5, x6)
    keep(e2, subject: x7, object: x6)
```

## r98
From: b815 r98.

```reading
When the person drafts an item with a requirement, the drafting service shall return the requirement id of the requirement and the requirement.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: item, x3: requirement]
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, requirement, x3)
  response [x5: requirement id]
    of(x5, x3)
    return(e2, subject: x4, object: x5)
    return(e3, subject: x4, object: x3)
```

## r101
Retires: r99. From: b826 r101.

```reading
While a term violates `v_t4`, `v_t7`, `v_t11`, `v_t13`, `v_t14` or `v_t19`, if the person writes the term into an item, then the drafting service shall refuse the request and name the term and every rule that the term violates.
shall [x2: rule `v_t4` (parameter), x3: rule `v_t7` (parameter), x4: rule `v_t11` (parameter), x5: rule `v_t13` (parameter), x6: rule `v_t14` (parameter), x7: rule `v_t19` (parameter), x8: agent the person (constant), x10: service the drafting service (constant), x11: request "the request the trigger makes" (indexical)]
  while [x1: term]
    or
      case
        violate(subject: x1, object: x2)
      case
        violate(subject: x1, object: x3)
      case
        violate(subject: x1, object: x4)
      case
        violate(subject: x1, object: x5)
      case
        violate(subject: x1, object: x6)
      case
        violate(subject: x1, object: x7)
  if [x9: item]
    request(e1, drafting.write, subject: x8, object: x1, into: x9)
  response
    refuse(e2, subject: x10, object: x11)
    name(e3, subject: x10, object: x1)
    every [x12: rule]
      violate(subject: x1, object: x12)
      scope
        name(e4, subject: x10, object: x12)
```

## r102
Retires: r100. From: b826 r102.

```reading
While a term violates `v_t4`, `v_t7`, `v_t11`, `v_t13`, `v_t14` or `v_t19`, if the person rewords the term in an item, then the drafting service shall refuse the request and name the term and every rule that the term violates.
shall [x2: rule `v_t4` (parameter), x3: rule `v_t7` (parameter), x4: rule `v_t11` (parameter), x5: rule `v_t13` (parameter), x6: rule `v_t14` (parameter), x7: rule `v_t19` (parameter), x8: agent the person (constant), x10: service the drafting service (constant), x11: request "the request the trigger makes" (indexical)]
  while [x1: term]
    or
      case
        violate(subject: x1, object: x2)
      case
        violate(subject: x1, object: x3)
      case
        violate(subject: x1, object: x4)
      case
        violate(subject: x1, object: x5)
      case
        violate(subject: x1, object: x6)
      case
        violate(subject: x1, object: x7)
  if [x9: item]
    request(e1, drafting.reword term, subject: x8, object: x1, in: x9)
  response
    refuse(e2, subject: x10, object: x11)
    name(e3, subject: x10, object: x1)
    every [x12: rule]
      violate(subject: x1, object: x12)
      scope
        name(e4, subject: x10, object: x12)
```

## r103
From: b829 r103.

```reading
When the person writes a term into an item, the drafting service shall return the term.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: term, x3: item]
    request(e1, drafting.write, subject: x1, object: x2, into: x3)
  response
    return(e2, subject: x4, object: x2)
```

## r105
Retires: r49. From: b829 r105.

```reading
When the person rewords a term in an item, the drafting service shall keep a different term in the item, return the term and complete the request.
shall [x1: agent the person (constant), x4: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  when [x2: term, x3: item]
    request(e1, drafting.reword term, subject: x1, object: x2, in: x3)
  response [x5: term]
    distinct(x5, x2)
    in(x5, x3)
    keep(e2, subject: x4, object: x5)
    return(e3, subject: x4, object: x5)
    complete(e4, subject: x4, object: x6)
```

## r106
Retires: r14. From: b829 r106.

```reading
When the person rewords a requirement in an item, the drafting service shall keep a different requirement in the item and return the requirement id of the requirement and the requirement.
shall [x1: agent the person (constant), x4: service the drafting service (constant)]
  when [x2: requirement, x3: item]
    in(x2, x3)
    request(e1, drafting.reword, subject: x1, object: x2)
  response [x5: requirement, x6: requirement id]
    distinct(x5, x2)
    in(x5, x3)
    keep(e2, subject: x4, object: x5)
    of(x6, x5)
    return(e3, subject: x4, object: x6)
    return(e4, subject: x4, object: x5)
```

## r107
From: b829 r107.

```reading
While an item holds a requirement, if the person rewords the requirement in the item with the same text, then the drafting service shall change nothing and name the requirement.
shall [x3: agent the person (constant), x4: service the drafting service (constant)]
  while [x1: item, x2: requirement]
    in(x2, x1)
  if
    in(x2, x1)
    request(e1, drafting.reword, subject: x3, object: x2)
    param(e1, text, x2)
  response
    not [x5: thing]
      change(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r108
From: b825 r108.

```reading
While a term means an element that the term does not fit, if the person writes the term into an item, then the drafting service shall refuse the request and name the term.
shall [x3: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: term, x2: element]
    not
      fit(subject: x1, object: x2)
    mean(subject: x1, object: x2)
  if [x4: item]
    request(e1, drafting.write, subject: x3, object: x1, into: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r109
From: b825 r109.

```reading
While a term means an element that the term does not fit, if the person rewords the term in an item, then the drafting service shall refuse the request and name the term.
shall [x3: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: term, x2: element]
    not
      fit(subject: x1, object: x2)
    mean(subject: x1, object: x2)
  if [x4: item]
    request(e1, drafting.reword term, subject: x3, object: x1, in: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r110
From: b840 r110.

```reading
While a term has a frame that does not end the term, if the person writes the term into an item, then the drafting service shall refuse the request and name the frame.
shall [x3: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: term, x2: frame]
    not
      end(subject: x2, object: x1)
    of(x2, x1)
  if [x4: item]
    request(e1, drafting.write, subject: x3, object: x1, into: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r111
From: b840 r111.

```reading
While a frame of a term has a slot and the slot refers to no term whose part of speech is `noun` and the slot refers to no term whose part of speech is `proper noun` and the slot refers to no parameter, if the person writes the term into an item, then the drafting service shall refuse the request and name the slot.
shall [x7: agent the person (constant), x9: service the drafting service (constant), x10: request "the request the trigger makes" (indexical)]
  while [x1: frame, x2: term, x3: slot]
    of(x1, x2)
    of(x3, x1)
    not [x4: term]
      part of speech(x4) = `noun`
      refer#4(subject: x3, to: x4)
    not [x5: term]
      part of speech(x5) = `proper noun`
      refer#4(subject: x3, to: x5)
    not [x6: parameter]
      refer#4(subject: x3, to: x6)
  if [x8: item]
    request(e1, drafting.write, subject: x7, object: x2, into: x8)
  response
    refuse(e2, subject: x9, object: x10)
    name(e3, subject: x9, object: x3)
```

## r112
From: b848 r112.

```reading
While a term violates `v_t6`, when the person rewords the term in an item, the drafting service shall keep the term in the item, name `v_t6` and complete the request.
shall [x2: rule `v_t6` (parameter), x3: agent the person (constant), x5: service the drafting service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: term]
    violate(subject: x1, object: x2)
  when [x4: item]
    request(e1, drafting.reword term, subject: x3, object: x1, in: x4)
  response
    in(x1, x4)
    keep(e2, subject: x5, object: x1)
    name(e3, subject: x5, object: x2)
    complete(e4, subject: x5, object: x6)
```

## r113
From: b882 r113.

```reading
When the person drafts an item with the requirement id of a requirement of a capability and another capability, the drafting service shall keep an item that holds a requirement of the capability that retires the requirement id.
shall [x1: agent the person (constant), x7: service the drafting service (constant)]
  when [x2: item, x3: requirement, x4: capability, x5: requirement id, x6: capability]
    of(x3, x4)
    of(x5, x3)
    distinct(x6, x4)
    request(e1, drafting.draft, subject: x1, object: x2)
    param(e1, requirement id, x5)
    param(e1, capability, x6)
  response [x8: item, x9: requirement]
    of(x9, x6)
    retire(subject: x9, object: x5)
    in(x9, x8)
    keep(e2, subject: x7, object: x8)
```
