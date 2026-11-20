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
