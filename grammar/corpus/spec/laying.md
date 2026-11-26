# laying: every live line with its intended reading

## r2
From: b611 r2.

```reading
While a workspace holds a requirement of an item, when the batches service lifts the item from the workspace, the laying service shall keep a workspace that does not hold the requirement.
shall [x4: service the batches service (constant), x5: service the laying service (constant)]
  while [x1: workspace, x2: requirement, x3: item]
    of(x2, x3)
    in(x2, x1)
  when
    request(e1, laying.lift, subject: x4, object: x3, from: x1)
  response [x6: workspace]
    not
      in(x2, x6)
    keep(e2, subject: x5, object: x6)
```

## r3
From: b611 r3.

```reading
While a requirement of an item violates a rule whose severity is `error`, when the batches service checks the item in a workspace, the laying service shall fail the request and name the rule.
shall [x4: service the batches service (constant), x6: service the laying service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: item, x3: rule]
    of(x1, x2)
    severity(x3) = `error`
    violate(subject: x1, object: x3)
  when [x5: workspace]
    request(e1, laying.check, subject: x4, object: x2, in: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x3)
```

## r4
From: b611 r4.

```reading
While an item holds no requirement that violates a rule whose severity is `error`, when the batches service checks the item in a workspace, the laying service shall complete the request.
shall [x4: service the batches service (constant), x6: service the laying service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: item]
    not [x2: requirement, x3: rule]
      severity(x3) = `error`
      violate(subject: x2, object: x3)
      in(x2, x1)
  when [x5: workspace]
    request(e1, laying.check, subject: x4, object: x1, in: x5)
  response
    complete(e2, subject: x6, object: x7)
```

## r5
From: b755 r5.

```reading
While an item holds a requirement that retires the requirement id of a requirement of a requirement group and a workspace holds another requirement that retires the requirement id of another requirement of the requirement group, when the batches service lifts the item from the workspace, the laying service shall keep a workspace that does not hold the requirement.
shall [x10: service the batches service (constant), x11: service the laying service (constant)]
  while [x1: item, x2: requirement, x3: requirement, x4: requirement group, x5: requirement id, x6: workspace, x7: requirement, x8: requirement, x9: requirement id]
    of(x3, x4)
    of(x5, x3)
    retire(subject: x2, object: x5)
    in(x2, x1)
    distinct(x7, x3)
    distinct(x8, x3)
    of(x8, x4)
    of(x9, x8)
    retire(subject: x7, object: x9)
    in(x7, x6)
  when
    request(e1, laying.lift, subject: x10, object: x1, from: x6)
  response [x12: workspace]
    not
      in(x8, x12)
    keep(e2, subject: x11, object: x12)
```

## r6
From: b758 r6.

```reading
While a batch holds an item and the item holds a requirement, when the batches service prepares a workspace for the batch, the laying service shall keep a scenario that refers to the requirement id of the requirement.
shall [x4: service the batches service (constant), x6: service the laying service (constant)]
  while [x1: batch, x2: item, x3: requirement]
    in(x2, x1)
    in(x3, x2)
  when [x5: workspace]
    request(e1, laying.prepare, subject: x4, object: x5, for: x1)
  response [x7: scenario, x8: requirement id]
    of(x8, x3)
    refer(subject: x7, to: x8)
    keep(e2, subject: x6, object: x7)
```

## r7
From: b745 r7.

```reading
While an item holds a requirement group that serves a job, when the batches service lays the item in a workspace, the laying service shall keep a capability that has a requirement group that serves the job.
shall [x4: service the batches service (constant), x6: service the laying service (constant)]
  while [x1: item, x2: requirement group, x3: job]
    serve(subject: x2, object: x3)
    in(x2, x1)
  when [x5: workspace]
    request(e1, laying.lay, subject: x4, object: x1, in: x5)
  response [x7: capability, x8: requirement group]
    serve(subject: x8, object: x3)
    of(x8, x7)
    keep(e2, subject: x6, object: x7)
```

## r8
From: b745 r8.

```reading
While an item holds a capability and the item holds an area that holds the capability, when the batches service lays the item in a workspace, the laying service shall keep the capability that the area holds.
shall [x4: service the batches service (constant), x6: service the laying service (constant)]
  while [x1: item, x2: capability, x3: area]
    in(x2, x1)
    in(x2, x3)
    in(x3, x1)
  when [x5: workspace]
    request(e1, laying.lay, subject: x4, object: x1, in: x5)
  response
    in(x2, x3)
    keep(e2, subject: x6, object: x2)
```

## r9
From: b758 r9.

```reading
While a batch holds an item and a requirement of the item has a logical form, when the batches service prepares a workspace for the batch, the laying service shall keep the logical form in the corpus.
shall [x5: service the batches service (constant), x7: service the laying service (constant), x8: corpus "the corpus of the bounded context the command runs in" (indexical)]
  while [x1: batch, x2: item, x3: requirement, x4: logical form]
    in(x2, x1)
    of(x3, x2)
    of(x4, x3)
  when [x6: workspace]
    request(e1, laying.prepare, subject: x5, object: x6, for: x1)
  response
    in(x4, x8)
    keep(e2, subject: x7, object: x4)
```

## r10
From: b758 r10.

```reading
While a batch holds an item and a requirement id is in the item and a requirement in the corpus has the requirement id, when the batches service prepares a workspace for the batch, the laying service shall keep a corpus that does not hold the requirement.
shall [x5: corpus "the corpus of the bounded context the command runs in" (indexical), x6: service the batches service (constant), x8: service the laying service (constant)]
  while [x1: batch, x2: item, x3: requirement id, x4: requirement]
    in(x2, x1)
    in(x3, x2)
    in(x4, x5)
    of(x3, x4)
  when [x7: workspace]
    request(e1, laying.prepare, subject: x6, object: x7, for: x1)
  response [x9: corpus]
    not
      in(x4, x9)
    keep(e2, subject: x8, object: x9)
```

## r11
From: b758 r11.

```reading
While a batch holds an item and a requirement of the item uses a rule, when the batches service prepares a workspace for the batch, the laying service shall keep the catalogue entry of the rule.
shall [x5: service the batches service (constant), x7: service the laying service (constant)]
  while [x1: batch, x2: item, x3: requirement, x4: rule]
    in(x2, x1)
    of(x3, x2)
    use(subject: x3, object: x4)
  when [x6: workspace]
    request(e1, laying.prepare, subject: x5, object: x6, for: x1)
  response [x8: catalogue entry]
    of(x8, x4)
    keep(e2, subject: x7, object: x8)
```

## r12
From: b758 r12.

```reading
While a batch holds an item and a requirement of the item uses a construct, when the batches service prepares a workspace for the batch, the laying service shall keep the construct catalogue.
shall [x5: service the batches service (constant), x7: service the laying service (constant), x8: construct catalogue "the construct catalogue of the bounded context the command runs in" (indexical)]
  while [x1: batch, x2: item, x3: requirement, x4: construct]
    in(x2, x1)
    of(x3, x2)
    use(subject: x3, object: x4)
  when [x6: workspace]
    request(e1, laying.prepare, subject: x5, object: x6, for: x1)
  response
    keep(e2, subject: x7, object: x8)
```

## r13
From: b758 r13.

```reading
While a batch holds an item and no requirement of an item that the batch holds uses a construct and no construct catalogue exists, when the batches service prepares a workspace for the batch, the laying service shall keep no construct catalogue.
shall [x7: service the batches service (constant), x9: service the laying service (constant)]
  while [x1: batch, x2: item]
    in(x2, x1)
    not [x3: requirement, x4: item, x5: construct]
      in(x4, x1)
      of(x3, x4)
      use(subject: x3, object: x5)
    not [x6: construct catalogue]
      exists(x6)
  when [x8: workspace]
    request(e1, laying.prepare, subject: x7, object: x8, for: x1)
  response
    not [x10: construct catalogue]
      keep(e2, subject: x9, object: x10)
```

## r14
From: b758 r14.

```reading
While a batch holds an item, when the batches service prepares a workspace for the batch, the laying service shall keep an index file that conforms to the index form.
shall [x3: service the batches service (constant), x5: service the laying service (constant), x7: artifact the index form (constant)]
  while [x1: batch, x2: item]
    in(x2, x1)
  when [x4: workspace]
    request(e1, laying.prepare, subject: x3, object: x4, for: x1)
  response [x6: index file]
    conforms(x6, x7)
    keep(e2, subject: x5, object: x6)
```

## r15
From: b758 r15.

```reading
While a capability has no requirement and a batch holds an item, when the batches service prepares a workspace for the batch, the laying service shall keep an index file that does not hold the capability.
shall [x5: service the batches service (constant), x7: service the laying service (constant)]
  while [x1: capability, x3: batch, x4: item]
    not [x2: requirement]
      of(x2, x1)
    in(x4, x3)
  when [x6: workspace]
    request(e1, laying.prepare, subject: x5, object: x6, for: x3)
  response [x8: index file]
    not
      in(x1, x8)
    keep(e2, subject: x7, object: x8)
```

## r16
From: b758 r16.

```reading
While a capability has a requirement and a batch holds an item, when the batches service prepares a workspace for the batch, the laying service shall keep an index file that holds the capability.
shall [x5: service the batches service (constant), x7: service the laying service (constant)]
  while [x1: capability, x2: requirement, x3: batch, x4: item]
    of(x2, x1)
    in(x4, x3)
  when [x6: workspace]
    request(e1, laying.prepare, subject: x5, object: x6, for: x3)
  response [x8: index file]
    in(x1, x8)
    keep(e2, subject: x7, object: x8)
```

## r17
From: b758 r17.

```reading
While a batch holds an item and the item holds a model line that specifies an operation and a requirement of a capability governs the operation and the item holds no requirement id that is in the capability, when the batches service prepares a workspace for the batch, the laying service shall generate the feature of the capability and keep the logical form of the requirement in the corpus.
shall [x8: service the batches service (constant), x10: service the laying service (constant), x12: corpus "the corpus of the bounded context the command runs in" (indexical)]
  while [x1: batch, x2: item, x3: model line, x4: operation, x5: requirement, x6: capability]
    in(x2, x1)
    specify(subject: x3, object: x4)
    in(x3, x2)
    of(x5, x6)
    govern(subject: x5, object: x4)
    not [x7: requirement id]
      in(x7, x6)
      in(x7, x2)
  when [x9: workspace]
    request(e1, laying.prepare, subject: x8, object: x9, for: x1)
  response [x11: feature, x13: logical form]
    of(x11, x6)
    generate(e2, subject: x10, object: x11)
    in(x5, x12)
    of(x13, x5)
    keep(e3, subject: x10, object: x13)
```

## r18
From: b758 r18.

```reading
While a batch holds an item and the item holds a verb that has a sense and a requirement of a capability uses the verb and the item holds no requirement id that is in the capability, when the batches service prepares a workspace for the batch, the laying service shall keep the logical form of the requirement in the corpus.
shall [x8: service the batches service (constant), x10: service the laying service (constant), x11: corpus "the corpus of the bounded context the command runs in" (indexical)]
  while [x1: batch, x2: item, x3: verb, x4: sense, x5: requirement, x6: capability]
    in(x2, x1)
    of(x4, x3)
    in(x3, x2)
    of(x5, x6)
    use(subject: x5, object: x3)
    not [x7: requirement id]
      in(x7, x6)
      in(x7, x2)
  when [x9: workspace]
    request(e1, laying.prepare, subject: x8, object: x9, for: x1)
  response [x12: logical form]
    in(x5, x11)
    of(x12, x5)
    keep(e2, subject: x10, object: x12)
```

## r19
From: b758 r19.

```reading
While an item holds a port line that governs an operation and every port line that governs the operation is in the item and the operation has an operation outcome and no core line handles the operation outcome and no port line excludes the operation outcome, when the batches service checks the item in a workspace, the laying service shall fail the request and name the operation outcome.
shall [x8: service the batches service (constant), x10: service the laying service (constant), x11: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: port line, x3: operation, x5: operation outcome]
    govern(subject: x2, object: x3)
    in(x2, x1)
    every [x4: port line]
      govern(subject: x4, object: x3)
      scope
        in(x4, x1)
    of(x5, x3)
    not [x6: core line]
      handle(subject: x6, object: x5)
    not [x7: port line]
      exclude(subject: x7, object: x5)
  when [x9: workspace]
    request(e1, laying.check, subject: x8, object: x1, in: x9)
  response
    fail(e2, subject: x10, object: x11)
    name(e3, subject: x10, object: x5)
```

## r20
From: b758 r20.

```reading
While an area holds a lifecycle and the lifecycle has a transition and another area holds an operation that performs the transition and an item holds a core line that uses the operation, when the batches service checks the item in a workspace, the laying service shall fail the request and name the core line and `v_m9`.
shall [x8: service the batches service (constant), x10: service the laying service (constant), x11: request "the request the trigger makes" (indexical), x12: thing `v_m9` (parameter)]
  while [x1: area, x2: lifecycle, x3: transition, x4: area, x5: operation, x6: item, x7: core line]
    in(x2, x1)
    of(x3, x2)
    distinct(x4, x1)
    perform(subject: x5, object: x3)
    in(x5, x4)
    use(subject: x7, object: x5)
    in(x7, x6)
  when [x9: workspace]
    request(e1, laying.check, subject: x8, object: x6, in: x9)
  response
    fail(e2, subject: x10, object: x11)
    name(e3, subject: x10, object: x7)
    name(e4, subject: x10, object: x12)
```

## r21
Retires: r1. From: b758 r21.

```reading
While an item holds a requirement, when the batches service lays the item in a workspace, the laying service shall keep the workspace that holds the requirement.
shall [x3: service the batches service (constant), x5: service the laying service (constant)]
  while [x1: item, x2: requirement]
    in(x2, x1)
  when [x4: workspace]
    request(e1, laying.lay, subject: x3, object: x1, in: x4)
  response
    in(x2, x4)
    keep(e2, subject: x5, object: x4)
```

## r22
From: b745 r22.

```reading
While `universal` does not exist and a universal condition is in an item, when the batches service lays the item in a workspace, the laying service shall keep `universal` and set the language of `universal` to `codified-2`.
shall [x1: capability `universal` (constant), x4: service the batches service (constant), x6: service the laying service (constant)]
  while [x2: universal condition, x3: item]
    not
      exists(x1)
    in(x2, x3)
  when [x5: workspace]
    request(e1, laying.lay, subject: x4, object: x3, in: x5)
  response
    keep(e2, subject: x6, object: x1)
    initiates(e3, subject: x6, language(x1) = `codified-2`)
```

## r23
From: b745 r23.

```reading
While an item holds a capability, when the batches service lays the item in a workspace, the laying service shall keep the capability that conforms to the capability form.
shall [x3: service the batches service (constant), x5: service the laying service (constant), x6: artifact the capability form (constant)]
  while [x1: item, x2: capability]
    in(x2, x1)
  when [x4: workspace]
    request(e1, laying.lay, subject: x3, object: x1, in: x4)
  response
    conforms(x2, x6)
    keep(e2, subject: x5, object: x2)
```

## r24
From: b745 r24.

```reading
While an item holds a capability and the item holds a driven port that holds the capability, when the batches service lays the item in a workspace, the laying service shall keep the driven port that holds the capability.
shall [x4: service the batches service (constant), x6: service the laying service (constant)]
  while [x1: item, x2: capability, x3: driven port]
    in(x2, x1)
    in(x2, x3)
    in(x3, x1)
  when [x5: workspace]
    request(e1, laying.lay, subject: x4, object: x1, in: x5)
  response
    in(x2, x3)
    keep(e2, subject: x6, object: x3)
```

## r25
From: b745 r25.

```reading
While an item holds a term of a pack, when the batches service lays the item in a workspace, the laying service shall keep the pack that has the term and keep the pack that this bounded context imports.
shall [x4: service the batches service (constant), x6: service the laying service (constant), x7: bounded context "the bounded context the request is made in" (indexical)]
  while [x1: item, x2: term, x3: pack]
    of(x2, x3)
    in(x2, x1)
  when [x5: workspace]
    request(e1, laying.lay, subject: x4, object: x1, in: x5)
  response
    of(x2, x3)
    keep(e2, subject: x6, object: x3)
    import(subject: x7, object: x3)
    keep(e3, subject: x6, object: x3)
```

## r26
From: b745 r26.

```reading
While an item holds a term of a pack and a capability holds a requirement id that the item holds, when the batches service lays the item in a workspace, the laying service shall keep the pack that has the term.
shall [x6: service the batches service (constant), x8: service the laying service (constant)]
  while [x1: item, x2: term, x3: pack, x4: capability, x5: requirement id]
    of(x2, x3)
    in(x2, x1)
    in(x5, x1)
    in(x5, x4)
  when [x7: workspace]
    request(e1, laying.lay, subject: x6, object: x1, in: x7)
  response
    of(x2, x3)
    keep(e2, subject: x8, object: x3)
```

## r27
From: b745 r27.

```reading
While an item imports a pack, when the batches service lays the item in a workspace, the laying service shall keep the pack that this bounded context imports.
shall [x3: service the batches service (constant), x5: service the laying service (constant), x6: bounded context "the bounded context the request is made in" (indexical)]
  while [x1: item, x2: pack]
    import#4(subject: x1, object: x2)
  when [x4: workspace]
    request(e1, laying.lay, subject: x3, object: x1, in: x4)
  response
    import(subject: x6, object: x2)
    keep(e2, subject: x5, object: x2)
```
