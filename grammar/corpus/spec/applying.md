# applying: every live line with its intended reading

## r1
From: b872 r1.

```reading
While an item holds a requirement, when the batches service applies the item to a specification, the specification service shall keep the specification that holds the requirement.
shall [x3: service the batches service (constant), x5: service the specification service (constant)]
  while [x1: item, x2: requirement]
    in(x2, x1)
  when [x4: specification]
    request(e1, specification.apply, subject: x3, object: x1, to: x4)
  response
    in(x2, x4)
    keep(e2, subject: x5, object: x4)
```

## r2
From: b872 r2.

```reading
While `universal` does not exist and a universal condition is in an item, when the batches service applies the item to a specification, the specification service shall keep `universal` and set the language of `universal` to `codified-2`.
shall [x1: capability `universal` (constant), x4: service the batches service (constant), x6: service the specification service (constant)]
  while [x2: universal condition, x3: item]
    not
      exists(x1)
    in(x2, x3)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x3, to: x5)
  response
    keep(e2, subject: x6, object: x1)
    initiates(e3, subject: x6, language(x1) = `codified-2`)
```

## r3
From: b872 r3.

```reading
While an item holds a capability, when the batches service applies the item to a specification, the specification service shall keep the capability that conforms to the capability form.
shall [x3: service the batches service (constant), x5: service the specification service (constant), x6: artifact the capability form (constant)]
  while [x1: item, x2: capability]
    in(x2, x1)
  when [x4: specification]
    request(e1, specification.apply, subject: x3, object: x1, to: x4)
  response
    conforms(x2, x6)
    keep(e2, subject: x5, object: x2)
```

## r4
From: b872 r4.

```reading
While an item holds a requirement group that serves a job, when the batches service applies the item to a specification, the specification service shall keep a capability that has a requirement group that serves the job.
shall [x4: service the batches service (constant), x6: service the specification service (constant)]
  while [x1: item, x2: requirement group, x3: job]
    serve(subject: x2, object: x3)
    in(x2, x1)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x1, to: x5)
  response [x7: capability, x8: requirement group]
    serve(subject: x8, object: x3)
    of(x8, x7)
    keep(e2, subject: x6, object: x7)
```

## r5
From: b872 r5.

```reading
While an item holds a capability and the item holds an area that holds the capability, when the batches service applies the item to a specification, the specification service shall keep the capability that the area holds.
shall [x4: service the batches service (constant), x6: service the specification service (constant)]
  while [x1: item, x2: capability, x3: area]
    in(x2, x1)
    in(x2, x3)
    in(x3, x1)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x1, to: x5)
  response
    in(x2, x3)
    keep(e2, subject: x6, object: x2)
```

## r6
From: b872 r6.

```reading
While an item holds a capability and the item holds a driven port that holds the capability, when the batches service applies the item to a specification, the specification service shall keep the driven port that holds the capability.
shall [x4: service the batches service (constant), x6: service the specification service (constant)]
  while [x1: item, x2: capability, x3: driven port]
    in(x2, x1)
    in(x2, x3)
    in(x3, x1)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x1, to: x5)
  response
    in(x2, x3)
    keep(e2, subject: x6, object: x3)
```

## r7
From: b872 r7.

```reading
While an item holds a term of a pack, when the batches service applies the item to a specification, the specification service shall keep the pack that has the term and keep the pack that this bounded context imports.
shall [x4: service the batches service (constant), x6: service the specification service (constant), x7: bounded context "the bounded context the request is made in" (indexical)]
  while [x1: item, x2: term, x3: pack]
    of(x2, x3)
    in(x2, x1)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x1, to: x5)
  response
    of(x2, x3)
    keep(e2, subject: x6, object: x3)
    import#2(subject: x7, object: x3)
    keep(e3, subject: x6, object: x3)
```

## r8
From: b872 r8.

```reading
While an item holds a term of a pack and a capability holds a requirement id that the item holds, when the batches service applies the item to a specification, the specification service shall keep the pack that has the term.
shall [x6: service the batches service (constant), x8: service the specification service (constant)]
  while [x1: item, x2: term, x3: pack, x4: capability, x5: requirement id]
    of(x2, x3)
    in(x2, x1)
    in(x5, x1)
    in(x5, x4)
  when [x7: specification]
    request(e1, specification.apply, subject: x6, object: x1, to: x7)
  response
    of(x2, x3)
    keep(e2, subject: x8, object: x3)
```

## r9
From: b872 r9.

```reading
While an item imports a pack, when the batches service applies the item to a specification, the specification service shall keep the pack that this bounded context imports.
shall [x3: service the batches service (constant), x5: service the specification service (constant), x6: bounded context "the bounded context the request is made in" (indexical)]
  while [x1: item, x2: pack]
    import#5(subject: x1, object: x2)
  when [x4: specification]
    request(e1, specification.apply, subject: x3, object: x1, to: x4)
  response
    import#2(subject: x6, object: x2)
    keep(e2, subject: x5, object: x2)
```

## r10
From: b872 r10.

```reading
While an item holds an operation table, when the batches service applies the item to a specification, the specification service shall keep an adapter contract that holds the operation table.
shall [x3: service the batches service (constant), x5: service the specification service (constant)]
  while [x1: item, x2: operation table]
    in(x2, x1)
  when [x4: specification]
    request(e1, specification.apply, subject: x3, object: x1, to: x4)
  response [x6: adapter contract]
    in(x2, x6)
    keep(e2, subject: x5, object: x6)
```

## r11
From: b872 r11.

```reading
While an item holds an operation, when the batches service applies the item to a specification, the specification service shall keep an adapter contract and keep no operation table of the operation.
shall [x3: service the batches service (constant), x5: service the specification service (constant)]
  while [x1: item, x2: operation]
    in(x2, x1)
  when [x4: specification]
    request(e1, specification.apply, subject: x3, object: x1, to: x4)
  response [x6: adapter contract]
    keep(e2, subject: x5, object: x6)
    not [x7: operation table]
      of(x7, x2)
      keep(e3, subject: x5, object: x7)
```

## r12
From: b872 r12.

```reading
While an item holds a model line and the model line specifies an operation and the domain model does not hold the operation and the item holds no operation table of the operation, when the batches service applies the item to a specification, the specification service shall keep an adapter contract that holds an operation table of the operation.
shall [x4: domain model "the domain model of this bounded context" (indexical), x6: service the batches service (constant), x8: service the specification service (constant)]
  while [x1: item, x2: model line, x3: operation]
    in(x2, x1)
    specify#2(subject: x2, object: x3)
    not
      in(x3, x4)
    not [x5: operation table]
      of(x5, x3)
      in(x5, x1)
  when [x7: specification]
    request(e1, specification.apply, subject: x6, object: x1, to: x7)
  response [x9: adapter contract, x10: operation table]
    of(x10, x3)
    in(x10, x9)
    keep(e2, subject: x8, object: x9)
```

## r13
From: b872 r13.

```reading
While an item holds an operation table and a capability holds a requirement id that the item holds, when the batches service applies the item to a specification, the specification service shall keep an adapter contract that holds the operation table.
shall [x5: service the batches service (constant), x7: service the specification service (constant)]
  while [x1: item, x2: operation table, x3: capability, x4: requirement id]
    in(x2, x1)
    in(x4, x1)
    in(x4, x3)
  when [x6: specification]
    request(e1, specification.apply, subject: x5, object: x1, to: x6)
  response [x8: adapter contract]
    in(x2, x8)
    keep(e2, subject: x7, object: x8)
```

## r14
From: b872 r14.

```reading
While an item holds a model line that restates an operation, when the batches service applies the item to a specification, the specification service shall keep the model line in the domain model and keep a domain model that does not hold the operation.
shall [x4: service the batches service (constant), x6: service the specification service (constant), x7: domain model "the domain model of this bounded context" (indexical)]
  while [x1: item, x2: model line, x3: operation]
    restate#2(subject: x2, object: x3)
    in(x2, x1)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x1, to: x5)
  response [x8: domain model]
    in(x2, x7)
    keep(e2, subject: x6, object: x2)
    not
      in(x3, x8)
    keep(e3, subject: x6, object: x8)
```

## r15
From: b872 r15.

```reading
While an item holds a model line that restates an element, when the batches service applies the item to a specification, the specification service shall keep the model line in the domain model and keep a domain model that does not hold the element.
shall [x4: service the batches service (constant), x6: service the specification service (constant), x7: domain model "the domain model of this bounded context" (indexical)]
  while [x1: item, x2: model line, x3: element]
    restate(subject: x2, object: x3)
    in(x2, x1)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x1, to: x5)
  response [x8: domain model]
    in(x2, x7)
    keep(e2, subject: x6, object: x2)
    not
      in(x3, x8)
    keep(e3, subject: x6, object: x8)
```

## r16
From: b872 r16.

```reading
While an item holds a model line that restates an event, when the batches service applies the item to a specification, the specification service shall keep the model line in the domain model and keep a domain model that does not hold the event.
shall [x4: service the batches service (constant), x6: service the specification service (constant), x7: domain model "the domain model of this bounded context" (indexical)]
  while [x1: item, x2: model line, x3: event]
    restate(subject: x2, object: x3)
    in(x2, x1)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x1, to: x5)
  response [x8: domain model]
    in(x2, x7)
    keep(e2, subject: x6, object: x2)
    not
      in(x3, x8)
    keep(e3, subject: x6, object: x8)
```

## r17
From: b872 r17.

```reading
While an item holds a model line that restates an actor, when the batches service applies the item to a specification, the specification service shall keep the model line in the domain model and keep a domain model that does not hold the actor.
shall [x4: service the batches service (constant), x6: service the specification service (constant), x7: domain model "the domain model of this bounded context" (indexical)]
  while [x1: item, x2: model line, x3: actor]
    restate(subject: x2, object: x3)
    in(x2, x1)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x1, to: x5)
  response [x8: domain model]
    in(x2, x7)
    keep(e2, subject: x6, object: x2)
    not
      in(x3, x8)
    keep(e3, subject: x6, object: x8)
```

## r18
From: b872 r18.

```reading
While an item holds a model line that moves to an area, when the batches service applies the item to a specification, the specification service shall keep the area that holds the model line.
shall [x4: service the batches service (constant), x6: service the specification service (constant)]
  while [x1: item, x2: model line, x3: area]
    move#3(subject: x2, to: x3)
    in(x2, x1)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x1, to: x5)
  response
    in(x2, x3)
    keep(e2, subject: x6, object: x3)
```

## r19
From: b872 r19.

```reading
While an item moves a term that means an element and an area holds the element, when the batches service applies the item to a specification, the specification service shall keep the area that holds the term.
shall [x5: service the batches service (constant), x7: service the specification service (constant)]
  while [x1: item, x2: term, x3: element, x4: area]
    mean(subject: x2, object: x3)
    move#4(subject: x1, object: x2)
    in(x3, x4)
  when [x6: specification]
    request(e1, specification.apply, subject: x5, object: x1, to: x6)
  response
    in(x2, x4)
    keep(e2, subject: x7, object: x4)
```

## r20
From: b872 r20.

```reading
While an item moves a term that means an element and an area holds the element and a capability holds a requirement id that the item holds, when the batches service applies the item to a specification, the specification service shall keep the area that holds the term.
shall [x7: service the batches service (constant), x9: service the specification service (constant)]
  while [x1: item, x2: term, x3: element, x4: area, x5: capability, x6: requirement id]
    mean(subject: x2, object: x3)
    move#4(subject: x1, object: x2)
    in(x3, x4)
    in(x6, x1)
    in(x6, x5)
  when [x8: specification]
    request(e1, specification.apply, subject: x7, object: x1, to: x8)
  response
    in(x2, x4)
    keep(e2, subject: x9, object: x4)
```

## r21
From: b872 r21.

```reading
While an item retires a model line, when the batches service applies the item to a specification, the specification service shall keep an area that does not hold the model line.
shall [x3: service the batches service (constant), x5: service the specification service (constant)]
  while [x1: item, x2: model line]
    retire#4(subject: x1, object: x2)
  when [x4: specification]
    request(e1, specification.apply, subject: x3, object: x1, to: x4)
  response [x6: area]
    not
      in(x2, x6)
    keep(e2, subject: x5, object: x6)
```

## r22
From: b872 r22.

```reading
While an item retires a term, when the batches service applies the item to a specification, the specification service shall keep an area that does not hold the term.
shall [x3: service the batches service (constant), x5: service the specification service (constant)]
  while [x1: item, x2: term]
    retire#4(subject: x1, object: x2)
  when [x4: specification]
    request(e1, specification.apply, subject: x3, object: x1, to: x4)
  response [x6: area]
    not
      in(x2, x6)
    keep(e2, subject: x5, object: x6)
```

## r23
From: b872 r23.

```reading
While an item retires a model line that restates an element and the item retires a term that means the element, when the batches service applies the item to a specification, the specification service shall keep an area that does not hold the term.
shall [x5: service the batches service (constant), x7: service the specification service (constant)]
  while [x1: item, x2: model line, x3: element, x4: term]
    restate(subject: x2, object: x3)
    retire#4(subject: x1, object: x2)
    mean(subject: x4, object: x3)
    retire#4(subject: x1, object: x4)
  when [x6: specification]
    request(e1, specification.apply, subject: x5, object: x1, to: x6)
  response [x8: area]
    not
      in(x4, x8)
    keep(e2, subject: x7, object: x8)
```

## r24
From: b872 r24.

```reading
While an item holds the `watering` area and the item holds the `plots` area and the `plots` area holds a term and the `watering` area holds a capability and a requirement of the capability uses the term, when the batches service applies the item to a specification, the specification service shall keep the `watering` area and keep an area that imports the `plots` area.
shall [x2: area `watering` (parameter), x3: area `plots` (parameter), x7: service the batches service (constant), x9: service the specification service (constant)]
  while [x1: item, x4: term, x5: capability, x6: requirement]
    in(x2, x1)
    in(x3, x1)
    in(x4, x3)
    in(x5, x2)
    of(x6, x5)
    use(subject: x6, object: x4)
  when [x8: specification]
    request(e1, specification.apply, subject: x7, object: x1, to: x8)
  response [x10: area]
    keep(e2, subject: x9, object: x2)
    import#3(subject: x10, object: x3)
    keep(e3, subject: x9, object: x10)
```

## r25
From: b872 r25.

```reading
While an item holds a capability and an area holds the capability, when the batches service applies the item to a specification, the specification service shall keep the capability that specifies the service of the area.
shall [x4: service the batches service (constant), x6: service the specification service (constant)]
  while [x1: item, x2: capability, x3: area]
    in(x2, x1)
    in(x2, x3)
  when [x5: specification]
    request(e1, specification.apply, subject: x4, object: x1, to: x5)
  response [x7: service]
    of(x7, x3)
    specify(subject: x2, object: x7)
    keep(e2, subject: x6, object: x2)
```
