# batches: every live line with its intended reading (the domain contract, 0.38.0)

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

## r78
From: b456 r78.

```reading
While a task of an item is `running` and a scenario breaks in the workspace of the task and the scenario has a capability and the item holds no requirement id that is in the capability and no kept change in the workspace of the task touches the feature of the capability, when a session finishes the task, the batches service shall set the status of the task to `done`.
shall [x10: service the batches service (constant)]
  while [x1: task, x2: item, x3: scenario, x4: workspace, x5: capability]
    of(x1, x2)
    status(x1) = `running`
    of(x4, x1)
    break(subject: x3, in: x4)
    of(x5, x3)
    not [x6: requirement id]
      in(x6, x5)
      in(x6, x2)
    not [x7: kept change, x8: feature]
      in(x7, x4)
      of(x8, x5)
      touch(subject: x7, object: x8)
  when [x9: session]
    request(e1, batches.finish, subject: x9, object: x1)
  response
    initiates(e2, subject: x10, status(x1) = `done`)
```

## r79
From: b355 r79.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds an operation table, when the person opens a batch, the batches service shall keep an adapter contract that holds the operation table.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x4: agent the person (constant), x6: service the batches service (constant)]
  while [x1: item, x3: operation table]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    in(x3, x1)
  when [x5: batch]
    request(e1, batches.open, subject: x4, object: x5)
  response [x7: adapter contract]
    in(x3, x7)
    keep(e2, subject: x6, object: x7)
```

## r80
From: b355 r80.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds an operation, when the person opens a batch, the batches service shall keep an adapter contract and keep no operation table of the operation.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x4: agent the person (constant), x6: service the batches service (constant)]
  while [x1: item, x3: operation]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    in(x3, x1)
  when [x5: batch]
    request(e1, batches.open, subject: x4, object: x5)
  response [x7: adapter contract]
    keep(e2, subject: x6, object: x7)
    not [x8: operation table]
      of(x8, x3)
      keep(e3, subject: x6, object: x8)
```

## r81
From: b460 r81.

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and the item holds a requirement, when the person amends the item, the batches service shall keep a workspace of the batch that holds the requirement and keep a workspace of the task that holds the requirement.
shall [x5: agent the person (constant), x6: service the batches service (constant)]
  while [x1: item, x2: batch, x3: task, x4: requirement]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    in(x4, x1)
  when
    request(e1, batches.amend, subject: x5, object: x1)
  response [x7: workspace, x8: workspace]
    of(x7, x2)
    in(x4, x7)
    keep(e2, subject: x6, object: x7)
    of(x8, x3)
    in(x4, x8)
    keep(e3, subject: x6, object: x8)
```

## r83
From: b460 r83.

```reading
While an item is not `in-batch`, if the person amends the item, then the batches service shall refuse the request and name the item.
shall [x2: agent the person (constant), x3: service the batches service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: item]
    not
      status(x1) = `in-batch`
  if
    request(e1, batches.amend, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r84
From: b462 r84.

```reading
When the person configures a setting with a setting value, the batches service shall keep a settings file that holds the setting, keep the settings file that conforms to the delivery settings form and complete the request.
shall [x1: agent the person (constant), x4: service the batches service (constant), x6: artifact the delivery settings form (constant), x7: request "the request the trigger makes" (indexical)]
  when [x2: setting, x3: setting value]
    request(e1, batches.configure, subject: x1, object: x2)
    param(e1, setting value, x3)
  response [x5: settings file]
    in(x2, x5)
    keep(e2, subject: x4, object: x5)
    conforms(x5, x6)
    keep(e3, subject: x4, object: x5)
    complete(e4, subject: x4, object: x7)
```

## r85
From: b462 r85.

```reading
If the person configures a setting that does not conform to the delivery settings form, then the batches service shall refuse the request and name the setting.
shall [x1: agent the person (constant), x3: artifact the delivery settings form (constant), x4: service the batches service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: setting]
    not
      conforms(x2, x3)
    request(e1, batches.configure, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r86
From: b462 r86.

```reading
If the person configures a setting with a setting value that does not conform to the delivery settings form, then the batches service shall refuse the request and name the setting value.
shall [x1: agent the person (constant), x4: artifact the delivery settings form (constant), x5: service the batches service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: setting, x3: setting value]
    not
      conforms(x3, x4)
    request(e1, batches.configure, subject: x1, object: x2)
    param(e1, setting value, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r87
From: b463 r87.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a model line that restates an operation, when the person opens a batch, the batches service shall keep the model line in the domain model and keep a domain model that does not hold the operation.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant), x8: domain model "the domain model of this bounded context" (indexical)]
  while [x1: item, x3: model line, x4: operation]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    restate#2(subject: x3, object: x4)
    in(x3, x1)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response [x9: domain model]
    in(x3, x8)
    keep(e2, subject: x7, object: x3)
    not
      in(x4, x9)
    keep(e3, subject: x7, object: x9)
```

## r90
Retires: r82. From: b466 r90.

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and the workspace of the batch holds a requirement of the item and the workspace of the task holds the requirement and the item does not hold the requirement, when the person amends the item, the batches service shall keep a workspace of the batch that does not hold the requirement and keep a workspace of the task that does not hold the requirement.
shall [x7: agent the person (constant), x8: service the batches service (constant)]
  while [x1: item, x2: batch, x3: task, x4: workspace, x5: requirement, x6: workspace]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    of(x4, x2)
    of(x5, x1)
    in(x5, x4)
    of(x6, x3)
    in(x5, x6)
    not
      in(x5, x1)
  when
    request(e1, batches.amend, subject: x7, object: x1)
  response [x9: workspace, x10: workspace]
    of(x9, x2)
    not
      in(x5, x9)
    keep(e2, subject: x8, object: x9)
    of(x10, x3)
    not
      in(x5, x10)
    keep(e3, subject: x8, object: x10)
```

## r91
Retires: r88. From: b485 r91.

```reading
While an item in a batch is `in-batch` and the item holds a model line that restates an operation and the domain model holds the model line, when a session parks the item, the batches service shall keep a domain model that holds the operation.
shall [x5: domain model "the domain model of this bounded context" (indexical), x7: service the batches service (constant)]
  while [x1: item, x2: batch, x3: model line, x4: operation]
    in(x1, x2)
    status(x1) = `in-batch`
    restate#2(subject: x3, object: x4)
    in(x3, x1)
    in(x3, x5)
  when [x6: session]
    request(e1, batches.park, subject: x6, object: x1)
  response [x8: domain model]
    in(x4, x8)
    keep(e2, subject: x7, object: x8)
```

## r92
From: b489 r92.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a model line and the model line specifies an operation and the domain model does not hold the operation and the item holds no operation table of the operation, when the person opens a batch, the batches service shall keep an adapter contract that holds an operation table of the operation.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: domain model "the domain model of this bounded context" (indexical), x7: agent the person (constant), x9: service the batches service (constant)]
  while [x1: item, x3: model line, x4: operation]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    in(x3, x1)
    specify(subject: x3, object: x4)
    not
      in(x4, x5)
    not [x6: operation table]
      of(x6, x4)
      in(x6, x1)
  when [x8: batch]
    request(e1, batches.open, subject: x7, object: x8)
  response [x10: adapter contract, x11: operation table]
    of(x11, x4)
    in(x11, x10)
    keep(e2, subject: x9, object: x10)
```

## r95
From: b472 r95.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a term of a pack, when the person opens a batch, the batches service shall keep the pack that has the term and keep the pack that this bounded context imports.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant), x8: bounded context "the bounded context whose repository the command runs in" (indexical)]
  while [x1: item, x3: term, x4: pack]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    of(x3, x4)
    in(x3, x1)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response
    of(x3, x4)
    keep(e2, subject: x7, object: x4)
    import(subject: x8, object: x4)
    keep(e3, subject: x7, object: x4)
```

## r96
From: b486 r96.

```reading
While an item in a batch is `in-batch` and the item does not meet the readiness bar, if the person amends the item, then the batches service shall refuse the request, name the item and change nothing.
shall [x3: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x4: agent the person (constant), x5: service the batches service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `in-batch`
    not
      meet(subject: x1, object: x3)
  if
    request(e1, batches.amend, subject: x4, object: x1)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
    not [x7: thing]
      change(e4, subject: x5, object: x7)
```

## r98
From: b75 r98.

```reading
While a settings file holds a batch rule, when the person opens a batch, the batches service shall keep a batch brief that holds the batch rule.
shall [x3: agent the person (constant), x5: service the batches service (constant)]
  while [x1: settings file, x2: batch rule]
    in(x2, x1)
  when [x4: batch]
    request(e1, batches.open, subject: x3, object: x4)
  response [x6: batch brief]
    in(x2, x6)
    keep(e2, subject: x5, object: x6)
```

## r99
From: b75 r99.

```reading
While no settings file holds a batch rule, when the person opens a batch, the batches service shall keep a batch brief that holds no batch rule.
shall [x3: agent the person (constant), x5: service the batches service (constant)]
  while
    not [x1: settings file, x2: batch rule]
      in(x2, x1)
  when [x4: batch]
    request(e1, batches.open, subject: x3, object: x4)
  response [x6: batch brief]
    not [x7: batch rule]
      in(x7, x6)
    keep(e2, subject: x5, object: x6)
```

## r100
Retires: r50. From: b578 r100.

```reading
While an item in a batch is `in-batch`, when the person merges the proposed change of the batch, the batches service shall deliver the item and set the status of the batch to `merged`.
shall [x3: agent the person (constant), x5: service the batches service (constant)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `in-batch`
  when [x4: proposed change]
    of(x4, x2)
    request(e1, batches.merge, subject: x3, object: x4)
  response
    deliver(e2, subject: x5, object: x1)
    initiates(e3, subject: x5, status(x2) = `merged`)
```

## r102
Retires: r59. From: b580 r102.

```reading
When the person merges the proposed change of a batch, the batches service shall keep no review folder of the batch and return the batch summary of the batch.
shall [x1: agent the person (constant), x4: service the batches service (constant)]
  when [x2: batch, x3: proposed change]
    of(x3, x2)
    request(e1, batches.merge, subject: x1, object: x3)
  response [x6: batch summary]
    not [x5: review folder]
      of(x5, x2)
      keep(e2, subject: x4, object: x5)
    of(x6, x2)
    return(e3, subject: x4, object: x6)
```

## r104
Retires: r103. From: b581 r104.

```reading
When the person opens a batch, the batches service shall keep a batch brief that holds a batch summary form and return the batch brief.
shall [x1: agent the person (constant), x3: service the batches service (constant)]
  when [x2: batch]
    request(e1, batches.open, subject: x1, object: x2)
  response [x4: batch brief, x5: batch summary form]
    in(x5, x4)
    keep(e2, subject: x3, object: x4)
    return(e3, subject: x3, object: x4)
```

## r105
Retires: r65. From: b578 r105.

```reading
While an item in a batch is `in-batch` and the item has a request line of a context request and the context request is `accepted`, when the person merges the proposed change of the batch, the batches service shall resolve the context request.
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
  response
    resolve(e2, subject: x7, object: x4)
```

## r106
Retires: r89. From: b578 r106.

```reading
While an item is `ready` and the item meets the readiness bar and a requirement of the item violates a rule whose severity is `error`, if the person opens a batch, then the batches service shall reopen the item and name the rule.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant)]
  while [x1: item, x3: requirement, x4: rule]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    of(x3, x1)
    severity(x4) = `error`
    violate(subject: x3, object: x4)
  if [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response
    reopen#2(e2, subject: x7, object: x1)
    name(e3, subject: x7, object: x4)
```

## r108
Retires: r94. From: b578 r108.

```reading
While an item is `ready` and the item meets the readiness bar and the item has no dependency on an item whose status is not `delivered` and the item does not exceed the review limit, when the person opens a batch, the batches service shall allocate the item, keep a batch that holds the item and keep a batch plan of the batch.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the review limit (constant), x6: agent the person (constant), x8: service the batches service (constant)]
  while [x1: item]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    not [x3: dependency, x4: item]
      not
        status(x4) = `delivered`
      on(x3, x4)
      of(x3, x1)
    not
      exceed#2(subject: x1, object: x5)
  when [x7: batch]
    request(e1, batches.open, subject: x6, object: x7)
  response [x9: batch, x10: batch plan]
    allocate(e2, subject: x8, object: x1)
    in(x1, x9)
    keep(e3, subject: x8, object: x9)
    of(x10, x9)
    keep(e4, subject: x8, object: x10)
```

## r109
Retires: r97. From: b578 r109.

```reading
While an item is `ready` and the item meets the readiness bar and a requirement of the item retires no requirement id and a scenario of the item refers to the requirement id of the requirement and the scenario succeeds in a workspace of a batch, if the person opens the batch, then the batches service shall reopen the item and name the scenario.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x9: agent the person (constant), x10: service the batches service (constant)]
  while [x1: item, x3: requirement, x5: scenario, x6: requirement id, x7: workspace, x8: batch]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    of(x3, x1)
    not [x4: requirement id]
      retire(subject: x3, object: x4)
    of(x5, x1)
    of(x6, x3)
    refer(subject: x5, to: x6)
    of(x7, x8)
    succeed(subject: x5, in: x7)
  if
    request(e1, batches.open, subject: x9, object: x8)
  response
    reopen#2(e2, subject: x10, object: x1)
    name(e3, subject: x10, object: x5)
```

## r110
Retires: r55. From: b578 r110.

```reading
While an item is not `ready` or `delivered` and a dependency on the item exists and another item whose status is `ready` has the dependency, when the person opens a batch, the batches service shall not allocate the item.
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
      allocate(e2, subject: x6, object: x3)
```

## r111
Retires: r57. From: b578 r111.

```reading
While an item in a batch is `in-batch`, when a session parks the item, the batches service shall suspend the item with a question and not set the status of the batch to `abandoned`.
shall [x4: service the batches service (constant)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `in-batch`
  when [x3: session]
    request(e1, batches.park, subject: x3, object: x1)
  response [x5: question]
    request(e2, backlog.suspend, subject: x4, object: x1)
    param(e2, question, x5)
    not
      initiates(e3, subject: x4, status(x2) = `abandoned`)
```

## r112
Retires: r58. From: b578 r112.

```reading
While a batch is `building`, when the person abandons the batch, the batches service shall set the status of the batch to `abandoned` and restore every item in the batch whose status is `in-batch`.
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
        restore(e3, subject: x3, object: x4)
```

## r113
From: b606 r113.

```reading
While an item is `ready` and the item meets the readiness bar, when the person opens a batch, the batches service shall keep an index file that conforms to the index form.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x3: agent the person (constant), x5: service the batches service (constant), x7: artifact the index form (constant)]
  while [x1: item]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
  when [x4: batch]
    request(e1, batches.open, subject: x3, object: x4)
  response [x6: index file]
    conforms(x6, x7)
    keep(e2, subject: x5, object: x6)
```

## r114
From: b606 r114.

```reading
While a capability has no requirement and an item is `ready` and the item meets the readiness bar, when the person opens a batch, the batches service shall keep an index file that does not hold the capability.
shall [x4: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant)]
  while [x1: capability, x3: item]
    not [x2: requirement]
      of(x2, x1)
    status(x3) = `ready`
    meet(subject: x3, object: x4)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response [x8: index file]
    not
      in(x1, x8)
    keep(e2, subject: x7, object: x8)
```

## r115
From: b606 r115.

```reading
While a capability has a requirement and an item is `ready` and the item meets the readiness bar, when the person opens a batch, the batches service shall keep an index file that holds the capability.
shall [x4: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant)]
  while [x1: capability, x2: requirement, x3: item]
    of(x2, x1)
    status(x3) = `ready`
    meet(subject: x3, object: x4)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response [x8: index file]
    in(x1, x8)
    keep(e2, subject: x7, object: x8)
```

## r116
From: b598 r116.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a model line that restates an element, when the person opens a batch, the batches service shall keep the model line in the domain model and keep a domain model that does not hold the element.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant), x8: domain model "the domain model of this bounded context" (indexical)]
  while [x1: item, x3: model line, x4: element]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    restate(subject: x3, object: x4)
    in(x3, x1)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response [x9: domain model]
    in(x3, x8)
    keep(e2, subject: x7, object: x3)
    not
      in(x4, x9)
    keep(e3, subject: x7, object: x9)
```

## r117
From: b607 r117.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a model line that moves to an area, when the person opens a batch, the batches service shall keep the area that holds the model line.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant)]
  while [x1: item, x3: model line, x4: area]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    move#3(subject: x3, to: x4)
    in(x3, x1)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response
    in(x3, x4)
    keep(e2, subject: x7, object: x4)
```

## r118
From: b607 r118.

```reading
While an item is `ready` and the item meets the readiness bar and the item moves a term that means an element and an area holds the element, when the person opens a batch, the batches service shall keep the area that holds the term.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x6: agent the person (constant), x8: service the batches service (constant)]
  while [x1: item, x3: term, x4: element, x5: area]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    mean(subject: x3, object: x4)
    move#4(subject: x1, object: x3)
    in(x4, x5)
  when [x7: batch]
    request(e1, batches.open, subject: x6, object: x7)
  response
    in(x3, x5)
    keep(e2, subject: x8, object: x5)
```

## r119
From: b647 r119.

```reading
While an item in a batch holds a model line that holds a member line and another item in the batch holds a model line that restates an element and the element does not hold the member line and the item is `in-batch`, when a session parks the item, the batches service shall keep the member line in the domain model and keep a domain model that does not hold the model line.
shall [x9: service the batches service (constant), x10: domain model "the domain model of this bounded context" (indexical)]
  while [x1: item, x2: batch, x3: model line, x4: member line, x5: item, x6: model line, x7: element]
    in(x1, x2)
    in(x4, x3)
    in(x3, x1)
    distinct(x5, x1)
    in(x5, x2)
    restate(subject: x6, object: x7)
    in(x6, x5)
    not
      in(x4, x7)
    status(x5) = `in-batch`
  when [x8: session]
    request(e1, batches.park, subject: x8, object: x5)
  response [x11: domain model]
    in(x4, x10)
    keep(e2, subject: x9, object: x4)
    not
      in(x6, x11)
    keep(e3, subject: x9, object: x11)
```

## r120
From: b647 r120.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a model line that restates an event, when the person opens a batch, the batches service shall keep the model line in the domain model and keep a domain model that does not hold the event.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant), x8: domain model "the domain model of this bounded context" (indexical)]
  while [x1: item, x3: model line, x4: event]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    restate(subject: x3, object: x4)
    in(x3, x1)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response [x9: domain model]
    in(x3, x8)
    keep(e2, subject: x7, object: x3)
    not
      in(x4, x9)
    keep(e3, subject: x7, object: x9)
```

## r121
From: b647 r121.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a model line that restates an actor, when the person opens a batch, the batches service shall keep the model line in the domain model and keep a domain model that does not hold the actor.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant), x8: domain model "the domain model of this bounded context" (indexical)]
  while [x1: item, x3: model line, x4: actor]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    restate(subject: x3, object: x4)
    in(x3, x1)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response [x9: domain model]
    in(x3, x8)
    keep(e2, subject: x7, object: x3)
    not
      in(x4, x9)
    keep(e3, subject: x7, object: x9)
```

## r124
From: b641 r124.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a requirement group that serves a job, when the person opens a batch, the batches service shall keep a capability that has a requirement group that serves the job.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant)]
  while [x1: item, x3: requirement group, x4: job]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    serve(subject: x3, object: x4)
    in(x3, x1)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response [x8: capability, x9: requirement group]
    serve(subject: x9, object: x4)
    of(x9, x8)
    keep(e2, subject: x7, object: x8)
```

## r125
From: b600 r125.

```reading
While an item in a batch is `in-batch` and a review of the batch holds a review finding, when the person amends the item with the review finding, the batches service shall keep a kept change for the review finding.
shall [x5: agent the person (constant), x6: service the batches service (constant)]
  while [x1: item, x2: batch, x3: review, x4: review finding]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x2)
    in(x4, x3)
  when
    request(e1, batches.amend, subject: x5, object: x1)
    param(e1, review finding, x4)
  response [x7: kept change]
    for(x7, x4)
    keep(e2, subject: x6, object: x7)
```

## r126
From: b660 r126.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds an operation table and a capability holds a requirement id that the item holds, when the person opens a batch, the batches service shall keep an adapter contract that holds the operation table.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x6: agent the person (constant), x8: service the batches service (constant)]
  while [x1: item, x3: operation table, x4: capability, x5: requirement id]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    in(x3, x1)
    in(x5, x1)
    in(x5, x4)
  when [x7: batch]
    request(e1, batches.open, subject: x6, object: x7)
  response [x9: adapter contract]
    in(x3, x9)
    keep(e2, subject: x8, object: x9)
```

## r127
From: b660 r127.

```reading
While an item is `ready` and the item meets the readiness bar and the item moves a term that means an element and an area holds the element and a capability holds a requirement id that the item holds, when the person opens a batch, the batches service shall keep the area that holds the term.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x8: agent the person (constant), x10: service the batches service (constant)]
  while [x1: item, x3: term, x4: element, x5: area, x6: capability, x7: requirement id]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    mean(subject: x3, object: x4)
    move#4(subject: x1, object: x3)
    in(x4, x5)
    in(x7, x1)
    in(x7, x6)
  when [x9: batch]
    request(e1, batches.open, subject: x8, object: x9)
  response
    in(x3, x5)
    keep(e2, subject: x10, object: x5)
```

## r128
From: b660 r128.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a term of a pack and a capability holds a requirement id that the item holds, when the person opens a batch, the batches service shall keep the pack that has the term.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x7: agent the person (constant), x9: service the batches service (constant)]
  while [x1: item, x3: term, x4: pack, x5: capability, x6: requirement id]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    of(x3, x4)
    in(x3, x1)
    in(x6, x1)
    in(x6, x5)
  when [x8: batch]
    request(e1, batches.open, subject: x7, object: x8)
  response
    of(x3, x4)
    keep(e2, subject: x9, object: x4)
```

## r129
From: b645 r129.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a capability and the item holds an area that holds the capability, when the person opens a batch, the batches service shall keep the capability that the area holds.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x7: service the batches service (constant)]
  while [x1: item, x3: capability, x4: area]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    in(x3, x1)
    in(x3, x4)
    in(x4, x1)
  when [x6: batch]
    request(e1, batches.open, subject: x5, object: x6)
  response
    in(x3, x4)
    keep(e2, subject: x7, object: x3)
```

## r130
Retires: r101. From: b663 r130.

```reading
While an item is `ready` and the item does not meet the readiness bar and the item does not exceed the review limit, when the person opens a batch, the batches service shall reopen the item.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x3: agent the review limit (constant), x4: agent the person (constant), x6: service the batches service (constant)]
  while [x1: item]
    status(x1) = `ready`
    not
      meet(subject: x1, object: x2)
    not
      exceed#2(subject: x1, object: x3)
  when [x5: batch]
    request(e1, batches.open, subject: x4, object: x5)
  response
    reopen#2(e2, subject: x6, object: x1)
```

## r131
Retires: r107. From: b663 r131.

```reading
While an item is `ready` and the item exceeds the review limit, when the person opens a batch, the batches service shall not allocate the item.
shall [x2: agent the review limit (constant), x3: agent the person (constant), x5: service the batches service (constant)]
  while [x1: item]
    status(x1) = `ready`
    exceed#2(subject: x1, object: x2)
  when [x4: batch]
    request(e1, batches.open, subject: x3, object: x4)
  response
    not
      allocate(e2, subject: x5, object: x1)
```
