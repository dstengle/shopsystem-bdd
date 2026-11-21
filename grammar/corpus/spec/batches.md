# batches: every live line with its intended reading (the domain contract, 0.38.0)

## r50
From: batches#r9, reworded in request words (0.38.0).

```reading
While an item in a batch is `in-batch`, when the person merges the proposed change of the batch, the batches service shall set the status of the item to `delivered` and set the status of the batch to `merged`.
shall [x3: agent the person (constant), x5: service the batches service (constant)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `in-batch`
  when [x4: proposed change]
    of(x4, x2)
    request(e1, batches.merge, subject: x3, object: x4)
  response
    initiates(e2, subject: x5, status(x1) = `delivered`)
    initiates(e3, subject: x5, status(x2) = `merged`)
```

## r51
From: batches#r14, reworded in request words (0.38.0).

```reading
When the person opens a batch, the batches service shall keep a batch brief and return the batch brief.
shall [x1: agent the person (constant), x3: service the batches service (constant)]
  when [x2: batch]
    request(e1, batches.open, subject: x1, object: x2)
  response [x4: batch brief]
    keep(e2, subject: x3, object: x4)
    return(e3, subject: x3, object: x4)
```

## r52
From: batches#r15, reworded in request words (0.38.0).

```reading
When the person abandons a batch, the batches service shall keep no review folder of the batch.
shall [x1: agent the person (constant), x3: service the batches service (constant)]
  when [x2: batch]
    request(e1, batches.abandon, subject: x1, object: x2)
  response
    not [x4: review folder]
      of(x4, x2)
      keep(e2, subject: x3, object: x4)
```

## r53
From: batches#r22, reworded in request words (0.38.0).

```reading
While an item is `ready` and the item meets the readiness bar and the item has no dependency on an item whose status is not `delivered`, when the person opens a batch, the batches service shall set the status of the item to `in-batch`, keep a batch that holds the item and keep a batch plan of the batch.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant)]
  while [x1: item]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    not [x3: dependency, x4: item]
      not
        status(x4) = `delivered`
      on(x3, x4)
      of(x3, x1)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response [x8: batch, x9: batch plan]
    initiates(e2, subject: x7, status(x1) = `in-batch`)
    in(x1, x8)
    keep(e3, subject: x7, object: x8)
    of(x9, x8)
    keep(e4, subject: x7, object: x9)
```

## r54
From: batches#r23, reworded in request words (0.38.0).

```reading
While an item is `ready` and the item does not meet the readiness bar, when the person opens a batch, the batches service shall set the status of the item to `shaped`.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x3: agent the person (constant), x5: service the batches service (constant)]
  while [x1: item]
    status(x1) = `ready`
    not
      meet(subject: x1, object: x2)
  when [x4: batch]
    request(e1, batches.open, subject: x3, object: x4)
  response
    initiates(e2, subject: x5, status(x1) = `shaped`)
```

## r55
From: batches#r24, reworded in request words (0.38.0).

```reading
While an item is not `ready` or `delivered` and a dependency on the item exists and another item whose status is `ready` has the dependency, when the person opens a batch, the batches service shall not set the status of the item to `in-batch`.
shall [x4: agent the person (constant), x6: service the batches service (constant)]
  while [x1: item, x2: dependency, x3: item]
    not
      status(x1) = `ready`
    not
      status(x1) = `delivered`
    on(x2, x1)
    exists(x2)
    distinct(x3, x1)
    status(x3) = `ready`
    of(x2, x3)
  when [x5: batch]
    request(e1, batches.open, subject: x4, object: x5)
  response
    not
      initiates(e2, subject: x6, status(x3) = `in-batch`)
```

## r56
From: batches#r25, reworded in request words (0.38.0).

```reading
While a batch is `building`, when a session resumes the batch, the batches service shall return the batch plan of the batch and not ask a question.
shall [x3: service the batches service (constant)]
  while [x1: batch]
    status(x1) = `building`
  when [x2: session]
    request(e1, batches.resume, subject: x2, object: x1)
  response [x4: batch plan]
    of(x4, x1)
    return(e2, subject: x3, object: x4)
    not [x5: question]
      ask(e3, subject: x3, object: x5)
```

## r57
From: batches#r26, reworded in request words (0.38.0).

```reading
While an item in a batch is `in-batch`, when a session parks the item, the batches service shall set the status of the item to `needs-input`, keep a question on the item and not set the status of the batch to `abandoned`.
shall [x4: service the batches service (constant)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `in-batch`
  when [x3: session]
    request(e1, batches.park, subject: x3, object: x1)
  response [x5: question]
    initiates(e2, subject: x4, status(x1) = `needs-input`)
    on(x5, x1)
    keep(e3, subject: x4, object: x5)
    not
      initiates(e4, subject: x4, status(x2) = `abandoned`)
```

## r58
From: batches#r28, reworded in request words (0.38.0).

```reading
While a batch is `building`, when the person abandons the batch, the batches service shall set the status of the batch to `abandoned` and set the status of every item in the batch whose status is `in-batch` to `ready`.
shall [x2: agent the person (constant), x3: service the batches service (constant)]
  while [x1: batch]
    status(x1) = `building`
  when
    request(e1, batches.abandon, subject: x2, object: x1)
  response
    initiates(e2, subject: x3, status(x1) = `abandoned`)
    every [x4: item]
      in(x4, x1)
      status(x4) = `in-batch`
      scope
        initiates(e3, subject: x3, status(x4) = `ready`)
```

## r59
From: batches#r31, reworded in request words (0.38.0).

```reading
When the person merges the proposed change of a batch, the batches service shall keep no review folder of the batch.
shall [x1: agent the person (constant), x4: service the batches service (constant)]
  when [x2: batch, x3: proposed change]
    of(x3, x2)
    request(e1, batches.merge, subject: x1, object: x3)
  response
    not [x5: review folder]
      of(x5, x2)
      keep(e2, subject: x4, object: x5)
```

## r60
From: batches#r32, reworded in request words (0.38.0).

```reading
While an item in a batch is `in-batch` and the workspace of the batch holds a requirement of the item, when a session parks the item, the batches service shall keep a workspace of the batch that does not hold the requirement.
shall [x6: service the batches service (constant)]
  while [x1: item, x2: batch, x3: workspace, x4: requirement]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x2)
    of(x4, x1)
    in(x4, x3)
  when [x5: session]
    request(e1, batches.park, subject: x5, object: x1)
  response [x7: workspace]
    of(x7, x2)
    not
      in(x4, x7)
    keep(e2, subject: x6, object: x7)
```

## r61
From: batches#r38, reworded in request words (0.38.0).

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and the status of an item in the batch is `needs-input` and a scenario of the item breaks in the workspace of the task, when a session finishes the task, the batches service shall set the status of the task to `done`.
shall [x8: service the batches service (constant)]
  while [x1: item, x2: batch, x3: task, x4: item, x5: scenario, x6: workspace]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    in(x4, x2)
    status(x4) = `needs-input`
    of(x5, x4)
    of(x6, x3)
    break(subject: x5, in: x6)
  when [x7: session]
    request(e1, batches.finish, subject: x7, object: x3)
  response
    initiates(e2, subject: x8, status(x3) = `done`)
```

## r62
From: batches#r34, reworded in request words (0.38.0).

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and another item in the batch is `in-batch` and a scenario of the item succeeds in the workspace of the task, when a session finishes the task, the batches service shall set the status of the task to `done`.
shall [x8: service the batches service (constant)]
  while [x1: item, x2: batch, x3: task, x4: item, x5: scenario, x6: workspace]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    distinct(x4, x1)
    in(x4, x2)
    status(x4) = `in-batch`
    of(x5, x4)
    of(x6, x3)
    succeed(subject: x5, in: x6)
  when [x7: session]
    request(e1, batches.finish, subject: x7, object: x3)
  response
    initiates(e2, subject: x8, status(x3) = `done`)
```

## r63
From: batches#r36, reworded in request words (0.38.0).

```reading
While a batch holds an item and the batch has a task, when the person monitors the batch, the batches service shall return the item, the task and the status of the task.
shall [x4: agent the person (constant), x5: service the batches service (constant)]
  while [x1: batch, x2: item, x3: task]
    in(x2, x1)
    of(x3, x1)
  when
    request(e1, batches.monitor, subject: x4, object: x1)
  response [x6: status]
    return(e2, subject: x5, object: x2)
    return(e3, subject: x5, object: x3)
    status(x3) = x6
    return(e4, subject: x5, object: x6)
```

## r64
From: batches#r39, reworded in request words (0.38.0).

```reading
While `universal` does not exist and an item is `ready` and the item meets the readiness bar and a universal condition is in the item, when the person opens a batch, the batches service shall keep `universal` and set the language of `universal` to `codified-2`.
shall [x1: capability `universal` (constant), x3: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant)]
  while [x2: item, x4: universal condition]
    not
      exists(x1)
    status(x2) = `ready`
    meet(subject: x2, object: x3)
    in(x4, x2)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response
    keep(e2, subject: x7, object: x1)
    initiates(e3, subject: x7, language(x1) = `codified-2`)
```

## r65
From: batches#r40, reworded in request words (0.38.0).

```reading
While an item in a batch is `in-batch` and the item has a request line of a context request and the context request is `accepted`, when the person merges the proposed change of the batch, the batches service shall set the status of the context request to `delivered`, keep a resolution, set the side of the context request to `asker` and keep an entry on the context request.
shall [x5: agent the person (constant), x7: service the batches service (constant)]
  while [x1: item, x2: batch, x3: request line, x4: context request]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x4)
    of(x3, x1)
    status(x4) = `accepted`
  when [x6: proposed change]
    of(x6, x2)
    request(e1, batches.merge, subject: x5, object: x6)
  response [x8: resolution, x9: entry]
    initiates(e2, subject: x7, status(x4) = `delivered`)
    keep(e3, subject: x7, object: x8)
    initiates(e4, subject: x7, side(x4) = `asker`)
    on(x9, x4)
    keep(e5, subject: x7, object: x9)
```

## r66
From: batches#r42, reworded in request words (0.38.0).

```reading
While a task of an item is `running` and the item holds a chore and the chore breaks in the workspace of the task, if a session finishes the task, then the batches service shall refuse the request and name the chore.
shall [x6: service the batches service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: task, x2: item, x3: chore, x4: workspace]
    of(x1, x2)
    status(x1) = `running`
    in(x3, x2)
    of(x4, x1)
    break(subject: x3, in: x4)
  if [x5: session]
    request(e1, batches.finish, subject: x5, object: x1)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x3)
```

## r67
From: batches#r43, reworded in request words (0.38.0).

```reading
While a task of an item is `running` and the item holds a chore and a kept change in the workspace of the task touches a file that is not in the chore, if a session finishes the task, then the batches service shall refuse the request and name the file.
shall [x8: service the batches service (constant), x9: request "the request the trigger makes" (indexical)]
  while [x1: task, x2: item, x3: chore, x4: kept change, x5: workspace, x6: file]
    of(x1, x2)
    status(x1) = `running`
    in(x3, x2)
    of(x5, x1)
    in(x4, x5)
    not
      in(x6, x3)
    touch(subject: x4, object: x6)
  if [x7: session]
    request(e1, batches.finish, subject: x7, object: x1)
  response
    refuse(e2, subject: x8, object: x9)
    name(e3, subject: x8, object: x6)
```

## r68
From: batches#r41, reworded in request words (0.38.0).

```reading
While an item is `ready` and the item holds a chore and the item meets the readiness bar, when the person opens a batch, the batches service shall keep a batch brief that holds the chore.
shall [x3: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x4: agent the person (constant), x6: service the batches service (constant)]
  while [x1: item, x2: chore]
    status(x1) = `ready`
    in(x2, x1)
    meet(subject: x1, object: x3)
  when [x5: batch]
    request(e1, batches.open, subject: x4, object: x5)
  response [x7: batch brief]
    in(x2, x7)
    keep(e2, subject: x6, object: x7)
```

## r70
From: batches#r45, reworded in request words (0.38.0).

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and the status of an item in the batch is `needs-input` and the item has a requirement that is not in the workspace of the batch and a scenario of the item breaks in the workspace of the task, when a session finishes the task, the batches service shall set the status of the task to `done`.
shall [x10: service the batches service (constant)]
  while [x1: item, x2: batch, x3: task, x4: item, x5: requirement, x6: workspace, x7: scenario, x8: workspace]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    in(x4, x2)
    status(x4) = `needs-input`
    of(x6, x2)
    not
      in(x5, x6)
    of(x5, x4)
    of(x7, x4)
    of(x8, x3)
    break(subject: x7, in: x8)
  when [x9: session]
    request(e1, batches.finish, subject: x9, object: x3)
  response
    initiates(e2, subject: x10, status(x3) = `done`)
```

## r71
From: batches#r46, reworded in request words (0.38.0).

```reading
While an item is `ready` and the item meets the readiness bar and a requirement of the item has a logical form, when the person opens a batch, the batches service shall keep the logical form in the corpus.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant), x8: corpus "the corpus of the bounded context the command runs in" (indexical)]
  while [x1: item, x3: requirement, x4: logical form]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    of(x3, x1)
    of(x4, x3)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response
    in(x4, x8)
    keep(e2, subject: x7, object: x4)
```

## r72
From: batches#r47, reworded in request words (0.38.0).

```reading
While an item is `ready` and the item meets the readiness bar and a requirement id is in the item and a requirement in the corpus has the requirement id, when the person opens a batch, the batches service shall keep a corpus that does not hold the requirement.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: corpus "the corpus of the bounded context the command runs in" (indexical), x6: agent the person (constant), x8: service the batches service (constant)]
  while [x1: item, x3: requirement id, x4: requirement]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    in(x3, x1)
    in(x4, x5)
    of(x3, x4)
  when [x7: batch]
    request(e1, batches.open, subject: x6, object: x7)
  response [x9: corpus]
    not
      in(x4, x9)
    keep(e2, subject: x8, object: x9)
```

## r73
From: batches#r48, reworded in request words (0.38.0).

```reading
While an item is `ready` and the item meets the readiness bar and a requirement of the item uses a rule, when the person opens a batch, the batches service shall keep the catalogue entry of the rule.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant)]
  while [x1: item, x3: requirement, x4: rule]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    of(x3, x1)
    use(subject: x3, object: x4)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response [x8: catalogue entry]
    of(x8, x4)
    keep(e2, subject: x7, object: x8)
```

## r74
From: batches#r49, reworded in request words (0.38.0).

```reading
While an item is `ready` and the item meets the readiness bar and a requirement of the item uses a construct, when the person opens a batch, the batches service shall keep the construct catalogue.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant), x8: construct catalogue "the construct catalogue of the bounded context the command runs in" (indexical)]
  while [x1: item, x3: requirement, x4: construct]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    of(x3, x1)
    use(subject: x3, object: x4)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response
    keep(e2, subject: x7, object: x8)
```

## r75
From: b390 r75.

```reading
While no requirement of an item whose status is `ready` uses a construct and no construct catalogue exists, when the person opens a batch, the batches service shall keep no construct catalogue.
shall [x5: agent the person (constant), x7: service the batches service (constant)]
  while
    not [x1: requirement, x2: item, x3: construct]
      status(x2) = `ready`
      of(x1, x2)
      use(subject: x1, object: x3)
    not [x4: construct catalogue]
      exists(x4)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response
    not [x8: construct catalogue]
      keep(e2, subject: x7, object: x8)
```

## r76
Retires: r69. From: b391 r76.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a capability, when the person opens a batch, the batches service shall keep the capability that conforms to the capability form and keep an index file that conforms to the index form.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x4: agent the person (constant), x6: service the batches service (constant), x7: artifact the capability form (constant), x9: artifact the index form (constant)]
  while [x1: item, x3: capability]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    in(x3, x1)
  when [x5: batch]
    request(e1, batches.open, subject: x4, object: x5)
  response [x8: index file]
    conforms(x3, x7)
    keep(e2, subject: x6, object: x3)
    conforms(x8, x9)
    keep(e3, subject: x6, object: x8)
```

## r77
From: b449 r77.

```reading
While a task of an item is `running` and the workspace of the task holds a virtual environment and a scenario of the item succeeds in the workspace of the task, when a session finishes the task, the batches service shall set the status of the task to `done`.
shall [x7: service the batches service (constant)]
  while [x1: task, x2: item, x3: workspace, x4: virtual environment, x5: scenario]
    of(x1, x2)
    status(x1) = `running`
    of(x3, x1)
    in(x4, x3)
    of(x5, x2)
    succeed(subject: x5, in: x3)
  when [x6: session]
    request(e1, batches.finish, subject: x6, object: x1)
  response
    initiates(e2, subject: x7, status(x1) = `done`)
```
