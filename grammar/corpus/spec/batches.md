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

## r135
From: b683 r135.

```reading
While a batch is `awaiting-merge`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `stop`.
shall [x2: agent the driver (constant), x3: service the batches service (constant)]
  while [x1: batch]
    status(x1) = `awaiting-merge`
  when
    request(e1, batches.poll, subject: x2, object: x1)
  response [x4: batch step]
    instruction(x4) = `stop`
    return(e2, subject: x3, object: x4)
```

## r141
From: b683 r141.

```reading
While a batch is `building` and every task of the batch is `done`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `submit batch`.
shall [x3: agent the driver (constant), x4: service the batches service (constant)]
  while [x1: batch]
    status(x1) = `building`
    every [x2: task]
      of(x2, x1)
      scope
        status(x2) = `done`
  when
    request(e1, batches.poll, subject: x3, object: x1)
  response [x5: batch step]
    instruction(x5) = `submit batch`
    return(e2, subject: x4, object: x5)
```

## r143
Retires: r138. From: b692 r143.

```reading
While a batch is `building` and a task of an item in the batch is `failed` and the item is `in-batch`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `park item` and the task.
shall [x4: agent the driver (constant), x5: service the batches service (constant)]
  while [x1: batch, x2: task, x3: item]
    status(x1) = `building`
    in(x3, x1)
    of(x2, x3)
    status(x2) = `failed`
    status(x3) = `in-batch`
  when
    request(e1, batches.poll, subject: x4, object: x1)
  response [x6: batch step]
    instruction(x6) = `park item`
    return(e2, subject: x5, object: x6)
    return(e3, subject: x5, object: x2)
```

## r144
Retires: r140. From: b692 r144.

```reading
While a batch is `building` and a task of an item in the batch is `running` and the item is `in-batch` and the workspace of the task holds a kept change that cites the item and no task of the batch is `failed`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `finish task` and the task.
shall [x7: agent the driver (constant), x8: service the batches service (constant)]
  while [x1: batch, x2: task, x3: item, x4: workspace, x5: kept change]
    status(x1) = `building`
    in(x3, x1)
    of(x2, x3)
    status(x2) = `running`
    status(x3) = `in-batch`
    of(x4, x2)
    cite(subject: x5, object: x3)
    in(x5, x4)
    not [x6: task]
      of(x6, x1)
      status(x6) = `failed`
  when
    request(e1, batches.poll, subject: x7, object: x1)
  response [x9: batch step]
    instruction(x9) = `finish task`
    return(e2, subject: x8, object: x9)
    return(e3, subject: x8, object: x2)
```

## r147
Retires: r136. From: b692 r147.

```reading
While a batch is `in-review`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `review change`, a review folder of the batch and a findings file in the review folder.
shall [x2: agent the driver (constant), x3: service the batches service (constant)]
  while [x1: batch]
    status(x1) = `in-review`
  when
    request(e1, batches.poll, subject: x2, object: x1)
  response [x4: batch step, x5: review folder, x6: findings file]
    instruction(x4) = `review change`
    return(e2, subject: x3, object: x4)
    of(x5, x1)
    return(e3, subject: x3, object: x5)
    in(x6, x5)
    return(e4, subject: x3, object: x6)
```

## r148
Retires: r137. From: b692 r148.

```reading
While a batch is `building` and a review of the batch holds a review finding whose triage is `fix now` and no kept change for the review finding exists, when the driver polls the batch, the batches service shall return a batch step whose instruction is `fix finding` and the review finding.
shall [x5: agent the driver (constant), x6: service the batches service (constant)]
  while [x1: batch, x2: review, x3: review finding]
    status(x1) = `building`
    of(x2, x1)
    triage(x3) = `fix now`
    in(x3, x2)
    not [x4: kept change]
      for(x4, x3)
      exists(x4)
  when
    request(e1, batches.poll, subject: x5, object: x1)
  response [x7: batch step]
    instruction(x7) = `fix finding`
    return(e2, subject: x6, object: x7)
    return(e3, subject: x6, object: x3)
```

## r150
From: b698 r150.

```reading
While a batch is `building` and a task of an item in the batch is `running` and the item is `in-batch` and the workspace of the task holds an amendment that cites the item and the workspace of the task holds exactly one kept change that cites the item and no task of the batch is `failed`, if the driver polls the batch, then the batches service shall return a batch step whose instruction is `build task`, the task and the batch brief of the batch.
shall [x8: agent the driver (constant), x9: service the batches service (constant)]
  while [x1: batch, x2: task, x3: item, x4: workspace, x5: amendment]
    status(x1) = `building`
    in(x3, x1)
    of(x2, x3)
    status(x2) = `running`
    status(x3) = `in-batch`
    of(x4, x2)
    cite(subject: x5, object: x3)
    in(x5, x4)
    count exactly 1 [x6: kept change]
      cite(subject: x6, object: x3)
      scope
        in(x6, x4)
    not [x7: task]
      of(x7, x1)
      status(x7) = `failed`
  if
    request(e1, batches.poll, subject: x8, object: x1)
  response [x10: batch step, x11: batch brief]
    instruction(x10) = `build task`
    return(e2, subject: x9, object: x10)
    return(e3, subject: x9, object: x2)
    of(x11, x1)
    return(e4, subject: x9, object: x11)
```

## r153
Retires: r146. From: b702 r153.

```reading
While a batch is `building` and two tasks of items in the batch are `pending` and no task of the batch is `failed` and no task of the batch is `running`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `prepare task` and every task of the batch whose status is `pending`.
shall [x7: agent the driver (constant), x8: service the batches service (constant)]
  while [x1: batch, x2: task, x3: item, x4: task]
    status(x1) = `building`
    in(x3, x1)
    of(x2, x3)
    status(x2) = `pending`
    distinct(x4, x2)
    of(x4, x3)
    status(x4) = `pending`
    not [x5: task]
      of(x5, x1)
      status(x5) = `failed`
    not [x6: task]
      of(x6, x1)
      status(x6) = `running`
  when
    request(e1, batches.poll, subject: x7, object: x1)
  response [x9: batch step]
    instruction(x9) = `prepare task`
    return(e2, subject: x8, object: x9)
    every [x10: task]
      of(x10, x1)
      status(x10) = `pending`
      scope
        return(e3, subject: x8, object: x10)
```

## r158
From: b710 r158.

```reading
While a batch is `building` and every task of the batch is `done` and a kept change that cites an item in the batch touches a file and the kept change conflicts with another kept change, if the driver polls the batch, then the batches service shall return a batch step whose instruction is `fix task`, the task of the item and the file.
shall [x7: agent the driver (constant), x8: service the batches service (constant)]
  while [x1: batch, x3: kept change, x4: item, x5: file, x6: kept change]
    status(x1) = `building`
    every [x2: task]
      of(x2, x1)
      scope
        status(x2) = `done`
    in(x4, x1)
    cite(subject: x3, object: x4)
    touch(subject: x3, object: x5)
    distinct(x6, x3)
    conflict(subject: x3, with: x6)
  if
    request(e1, batches.poll, subject: x7, object: x1)
  response [x9: batch step, x10: task]
    instruction(x9) = `fix task`
    return(e2, subject: x8, object: x9)
    of(x10, x4)
    return(e3, subject: x8, object: x10)
    return(e4, subject: x8, object: x5)
```

## r159
Retires: r152. From: b711 r159.

```reading
While a batch is `building` and two tasks of items in the batch are `running` and no task of the batch is `failed` and no workspace of a task of the batch holds a kept change that cites an item in the batch, when the driver polls the batch, the batches service shall return a batch step whose instruction is `build task`, every task of the batch whose status is `running` and the batch brief of the batch.
shall [x10: agent the driver (constant), x11: service the batches service (constant)]
  while [x1: batch, x2: task, x3: item, x4: task]
    status(x1) = `building`
    in(x3, x1)
    of(x2, x3)
    status(x2) = `running`
    distinct(x4, x2)
    of(x4, x3)
    status(x4) = `running`
    not [x5: task]
      of(x5, x1)
      status(x5) = `failed`
    not [x6: workspace, x7: task, x8: kept change, x9: item]
      of(x7, x1)
      of(x6, x7)
      in(x9, x1)
      cite(subject: x8, object: x9)
      in(x8, x6)
  when
    request(e1, batches.poll, subject: x10, object: x1)
  response [x12: batch step, x14: batch brief]
    instruction(x12) = `build task`
    return(e2, subject: x11, object: x12)
    every [x13: task]
      of(x13, x1)
      status(x13) = `running`
      scope
        return(e3, subject: x11, object: x13)
    of(x14, x1)
    return(e4, subject: x11, object: x14)
```

## r161
Retires: r149. From: b713 r161.

```reading
While a batch is `building` and a task of an item in the batch is `done` and every task of the batch is `done` and a scenario of the item breaks in the workspace of the batch and no fix exists, if the driver polls the batch, then the batches service shall return a batch step whose instruction is `fix task` and the task.
shall [x8: agent the driver (constant), x9: service the batches service (constant)]
  while [x1: batch, x2: task, x3: item, x5: scenario, x6: workspace]
    status(x1) = `building`
    in(x3, x1)
    of(x2, x3)
    status(x2) = `done`
    every [x4: task]
      of(x4, x1)
      scope
        status(x4) = `done`
    of(x5, x3)
    of(x6, x1)
    break(subject: x5, in: x6)
    not [x7: fix]
      exists(x7)
  if
    request(e1, batches.poll, subject: x8, object: x1)
  response [x10: batch step]
    instruction(x10) = `fix task`
    return(e2, subject: x9, object: x10)
    return(e3, subject: x9, object: x2)
```

## r162
Retires: r154. From: b713 r162.

```reading
While a batch is `building` and every task of the batch is `done` and a scenario breaks in the workspace of the batch and no scenario of an item in the batch breaks in the workspace of the batch and no fix exists, if the driver polls the batch, then the batches service shall return a batch step whose instruction is `look at failure` and the scenario.
shall [x8: agent the driver (constant), x9: service the batches service (constant)]
  while [x1: batch, x3: scenario, x4: workspace]
    status(x1) = `building`
    every [x2: task]
      of(x2, x1)
      scope
        status(x2) = `done`
    of(x4, x1)
    break(subject: x3, in: x4)
    not [x5: scenario, x6: item]
      in(x6, x1)
      of(x5, x6)
      break(subject: x5, in: x4)
    not [x7: fix]
      exists(x7)
  if
    request(e1, batches.poll, subject: x8, object: x1)
  response [x10: batch step]
    instruction(x10) = `look at failure`
    return(e2, subject: x9, object: x10)
    return(e3, subject: x9, object: x3)
```

## r163
From: b713 r163.

```reading
While a batch is `building` and every task of the batch is `done` and a scenario breaks in the workspace of the batch and a fix exists, when the driver polls the batch, the batches service shall return a batch step whose instruction is `submit batch`.
shall [x6: agent the driver (constant), x7: service the batches service (constant)]
  while [x1: batch, x3: scenario, x4: workspace, x5: fix]
    status(x1) = `building`
    every [x2: task]
      of(x2, x1)
      scope
        status(x2) = `done`
    of(x4, x1)
    break(subject: x3, in: x4)
    exists(x5)
  when
    request(e1, batches.poll, subject: x6, object: x1)
  response [x8: batch step]
    instruction(x8) = `submit batch`
    return(e2, subject: x7, object: x8)
```

## r165
From: b722 r165.

```reading
While a batch is `building` and the status of every item in the batch is `needs-input`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `abandon batch`.
shall [x3: agent the driver (constant), x4: service the batches service (constant)]
  while [x1: batch]
    status(x1) = `building`
    every [x2: item]
      in(x2, x1)
      scope
        status(x2) = `needs-input`
  when
    request(e1, batches.poll, subject: x3, object: x1)
  response [x5: batch step]
    instruction(x5) = `abandon batch`
    return(e2, subject: x4, object: x5)
```

## r168
Retires: r166. From: b730 r168.

```reading
While an item is `ready` and the item meets the readiness bar and the item has no dependency on an item whose status is not `delivered` and the item does not exceed the review limit and the item holds a port line that governs an operation and another port line that governs the operation is not in the item and the operation has an operation outcome and no core line handles the operation outcome and no port line excludes the operation outcome, when the person opens a batch, the batches service shall allocate the item.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the review limit (constant), x12: agent the person (constant), x14: service the batches service (constant)]
  while [x1: item, x6: port line, x7: operation, x8: port line, x9: operation outcome]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    not [x3: dependency, x4: item]
      not
        status(x4) = `delivered`
      on(x3, x4)
      of(x3, x1)
    not
      exceed#2(subject: x1, object: x5)
    govern(subject: x6, object: x7)
    in(x6, x1)
    distinct(x8, x6)
    govern(subject: x8, object: x7)
    not
      in(x8, x1)
    of(x9, x7)
    not [x10: core line]
      handle(subject: x10, object: x9)
    not [x11: port line]
      exclude(subject: x11, object: x9)
  when [x13: batch]
    request(e1, batches.open, subject: x12, object: x13)
  response
    allocate(e2, subject: x14, object: x1)
```

## r170
From: b740 r170.

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and the item holds a requirement and the workspace of the batch has a feature generator, when the person amends the item, the batches service shall keep a workspace of the batch that holds a feature of the feature generator.
shall [x7: agent the person (constant), x8: service the batches service (constant)]
  while [x1: item, x2: batch, x3: task, x4: requirement, x5: workspace, x6: feature generator]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    in(x4, x1)
    of(x5, x2)
    of(x6, x5)
  when
    request(e1, batches.amend, subject: x7, object: x1)
  response [x9: workspace, x10: feature]
    of(x9, x2)
    of(x10, x6)
    in(x10, x9)
    keep(e2, subject: x8, object: x9)
```

## r171
From: b740 r171.

```reading
While an item in a batch is `in-batch` and a review of the batch holds a review finding, when the person amends the item, the batches service shall keep a kept change for the review finding.
shall [x5: agent the person (constant), x6: service the batches service (constant)]
  while [x1: item, x2: batch, x3: review, x4: review finding]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x2)
    in(x4, x3)
  when
    request(e1, batches.amend, subject: x5, object: x1)
  response [x7: kept change]
    for(x7, x4)
    keep(e2, subject: x6, object: x7)
```

## r172
From: b740 r172.

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and the item holds a requirement and this corpus holds the requirement, when the person amends the item, the batches service shall keep a corpus that conforms to the corpus form and keep a workspace of the batch that holds the corpus.
shall [x5: corpus "the corpus of the bounded context the command runs in" (indexical), x6: agent the person (constant), x7: service the batches service (constant), x9: artifact the corpus form (constant)]
  while [x1: item, x2: batch, x3: task, x4: requirement]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    in(x4, x1)
    in(x4, x5)
  when
    request(e1, batches.amend, subject: x6, object: x1)
  response [x8: corpus, x10: workspace]
    conforms(x8, x9)
    keep(e2, subject: x7, object: x8)
    of(x10, x2)
    in(x8, x10)
    keep(e3, subject: x7, object: x10)
```

## r173
From: b741 r173.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a requirement and the requirement retires the requirement id of a requirement that enforces a design-decision whose status is `accepted`, when the person opens a batch, the batches service shall set the status of the design-decision to `superseded`, keep a design-decision that supersedes the design-decision and name the design-decision.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x7: agent the person (constant), x9: service the batches service (constant)]
  while [x1: item, x3: requirement, x4: requirement, x5: design-decision, x6: requirement id]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    in(x3, x1)
    status(x5) = `accepted`
    enforce(subject: x4, object: x5)
    of(x6, x4)
    retire(subject: x3, object: x6)
  when [x8: batch]
    request(e1, batches.open, subject: x7, object: x8)
  response [x10: design-decision]
    initiates(e2, subject: x9, status(x5) = `superseded`)
    supersede(subject: x10, object: x5)
    keep(e3, subject: x9, object: x10)
    name(e4, subject: x9, object: x10)
```

## r174
From: b741 r174.

```reading
While an item in a batch is `in-batch` and the item holds a requirement and the requirement retires the requirement id of a requirement that enforces a design-decision whose status is `superseded`, when the person parks the item, the batches service shall set the status of the design-decision to `accepted` and keep no design-decision that supersedes the design-decision.
shall [x7: agent the person (constant), x8: service the batches service (constant)]
  while [x1: item, x2: batch, x3: requirement, x4: requirement, x5: design-decision, x6: requirement id]
    in(x1, x2)
    status(x1) = `in-batch`
    in(x3, x1)
    status(x5) = `superseded`
    enforce(subject: x4, object: x5)
    of(x6, x4)
    retire(subject: x3, object: x6)
  when
    request(e1, batches.park, subject: x7, object: x1)
  response
    initiates(e2, subject: x8, status(x5) = `accepted`)
    not [x9: design-decision]
      supersede(subject: x9, object: x5)
      keep(e3, subject: x8, object: x9)
```

## r175
From: b749 r175.

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and the workspace of the batch has a feature generator and the feature generator is `unresponsive`, if the person amends the item, then the batches service shall refuse the request, name the feature generator and change nothing.
shall [x6: agent the person (constant), x7: service the batches service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: batch, x3: task, x4: workspace, x5: feature generator]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    of(x4, x2)
    of(x5, x4)
    responsiveness(x5) = `unresponsive`
  if
    request(e1, batches.amend, subject: x6, object: x1)
  response
    refuse(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x5)
    not [x9: thing]
      change(e4, subject: x7, object: x9)
```

## r176
From: b749 r176.

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and the workspace of the batch has a feature generator and the feature generator is `unresponsive`, if the person parks the item, then the batches service shall refuse the request, name the feature generator and change nothing.
shall [x6: agent the person (constant), x7: service the batches service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: batch, x3: task, x4: workspace, x5: feature generator]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    of(x4, x2)
    of(x5, x4)
    responsiveness(x5) = `unresponsive`
  if
    request(e1, batches.park, subject: x6, object: x1)
  response
    refuse(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x5)
    not [x9: thing]
      change(e4, subject: x7, object: x9)
```

## r177
From: b750 r177.

```reading
While an item is `ready` and the item meets the readiness bar and the item holds a requirement and the requirement retires the requirement id of a requirement that enforces a design-decision whose status is `accepted` and a requirement that enforces the design-decision has a requirement id and another item that meets the readiness bar holds another requirement and the requirement retires the requirement id, when the person opens a batch, the batches service shall keep a design-decision that the requirement enforces.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x11: agent the person (constant), x13: service the batches service (constant)]
  while [x1: item, x3: requirement, x4: requirement, x5: design-decision, x6: requirement id, x7: requirement, x8: requirement id, x9: item, x10: requirement]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    in(x3, x1)
    status(x5) = `accepted`
    enforce(subject: x4, object: x5)
    of(x6, x4)
    retire(subject: x3, object: x6)
    enforce(subject: x7, object: x5)
    of(x8, x7)
    distinct(x9, x1)
    meet(subject: x9, object: x2)
    distinct(x10, x7)
    in(x10, x9)
    retire(subject: x10, object: x8)
  when [x12: batch]
    request(e1, batches.open, subject: x11, object: x12)
  response [x14: design-decision]
    enforce(subject: x10, object: x14)
    keep(e2, subject: x13, object: x14)
```

## r178
From: b750 r178.

```reading
While an item in a batch is `in-batch` and the item holds a requirement and the requirement retires the requirement id of a requirement that enforces a design-decision whose status is `superseded` and a requirement that enforces the design-decision has a requirement id and another requirement retires the requirement id, when the person parks the item, the batches service shall keep a design-decision that the requirement enforces.
shall [x10: agent the person (constant), x11: service the batches service (constant)]
  while [x1: item, x2: batch, x3: requirement, x4: requirement, x5: design-decision, x6: requirement id, x7: requirement, x8: requirement id, x9: requirement]
    in(x1, x2)
    status(x1) = `in-batch`
    in(x3, x1)
    status(x5) = `superseded`
    enforce(subject: x4, object: x5)
    of(x6, x4)
    retire(subject: x3, object: x6)
    enforce(subject: x7, object: x5)
    of(x8, x7)
    distinct(x9, x7)
    retire(subject: x9, object: x8)
  when
    request(e1, batches.park, subject: x10, object: x1)
  response [x12: design-decision]
    enforce(subject: x9, object: x12)
    keep(e2, subject: x11, object: x12)
```

## r179
Retires: r108. From: b611 r179.

```reading
While an item is `ready` and the item meets the readiness bar and the item has no dependency on an item whose status is not `delivered` and the item does not exceed the review limit, when the person opens a batch, the batches service shall allocate the item, keep a batch that holds the item, keep a batch plan of the batch and lay the item in the workspace of the batch.
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
  response [x9: batch, x10: batch plan, x11: workspace]
    allocate(e2, subject: x8, object: x1)
    in(x1, x9)
    keep(e3, subject: x8, object: x9)
    of(x10, x9)
    keep(e4, subject: x8, object: x10)
    of(x11, x9)
    lay(e5, subject: x8, object: x1, in: x11)
```

## r180
From: b611 r180.

```reading
When the laying service completes the request to lay an item in a workspace, the batches service shall check the item in the workspace.
shall [x1: service the laying service (constant), x5: service the batches service (constant)]
  when [x2: request, x3: item, x4: workspace]
    request(x2, laying.lay, object: x3, in: x4)
    complete(e1, subject: x1, object: x2)
  response
    check(e2, subject: x5, object: x3, in: x4)
```

## r181
Retires: r106. From: b611 r181.

```reading
When the laying service fails the request to check an item in a workspace, the batches service shall reopen the item and name every rule that a requirement of the item violates.
shall [x1: service the laying service (constant), x5: service the batches service (constant)]
  when [x2: request, x3: item, x4: workspace]
    request(x2, laying.check, object: x3, in: x4)
    fail(e1, subject: x1, object: x2)
  response
    reopen#2(e2, subject: x5, object: x3)
    every [x6: rule, x7: requirement]
      of(x7, x3)
      violate(subject: x7, object: x6)
      scope
        name(e3, subject: x5, object: x6)
```

## r182
Retires: r60. From: b611 r182.

```reading
While an item in a batch is `in-batch` and the workspace of the batch holds a requirement of the item, when a session parks the item, the batches service shall lift the item from the workspace of the batch.
shall [x6: service the batches service (constant)]
  while [x1: item, x2: batch, x3: workspace, x4: requirement]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x2)
    of(x4, x1)
    in(x4, x3)
  when [x5: session]
    request(e1, batches.park, subject: x5, object: x1)
  response
    lift(e2, subject: x6, object: x1, from: x3)
```

## r183
From: b611 r183.

```reading
When the laying service completes the request to lift an item from a workspace, the batches service shall keep a kept change that cites the item.
shall [x1: service the laying service (constant), x5: service the batches service (constant)]
  when [x2: request, x3: item, x4: workspace]
    request(x2, laying.lift, object: x3, from: x4)
    complete(e1, subject: x1, object: x2)
  response [x6: kept change]
    cite(subject: x6, object: x3)
    keep(e2, subject: x5, object: x6)
```

## r184
From: b611 r184.

```reading
When the laying service completes the request to check an item in a workspace, the batches service shall keep a kept change that cites the item.
shall [x1: service the laying service (constant), x5: service the batches service (constant)]
  when [x2: request, x3: item, x4: workspace]
    request(x2, laying.check, object: x3, in: x4)
    complete(e1, subject: x1, object: x2)
  response [x6: kept change]
    cite(subject: x6, object: x3)
    keep(e2, subject: x5, object: x6)
```

## r185
Retires: r81. From: b747 r185.

```reading
While an item in a batch is `in-batch` and a task of the item is `running`, when the person amends the item, the batches service shall lift the item from the workspace of the batch, lift the item from the workspace of the task, lay the item in the workspace of the batch and lay the item in the workspace of the task.
shall [x4: agent the person (constant), x5: service the batches service (constant)]
  while [x1: item, x2: batch, x3: task]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
  when
    request(e1, batches.amend, subject: x4, object: x1)
  response [x6: workspace, x7: workspace]
    of(x6, x2)
    lift(e2, subject: x5, object: x1, from: x6)
    of(x7, x3)
    lift(e3, subject: x5, object: x1, from: x7)
    lay(e4, subject: x5, object: x1, in: x6)
    lay(e5, subject: x5, object: x1, in: x7)
```

## r187
Retires: r130. From: b758 r187.

```reading
While an item is `ready` and the item does not meet the readiness bar and the item does not exceed the review limit, when the person opens a batch, the batches service shall reopen the item and name every bar check that the item does not meet.
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
    every [x7: bar check]
      not
        meet(subject: x1, object: x7)
      scope
        name(e3, subject: x6, object: x7)
```

## r188
From: b758 r188.

```reading
While a batch holds an item, when the laying service completes the request to lay the item in a workspace, the batches service shall prepare the workspace for the batch.
shall [x3: service the laying service (constant), x6: service the batches service (constant)]
  while [x1: batch, x2: item]
    in(x2, x1)
  when [x4: request, x5: workspace]
    request(x4, laying.lay, object: x2, in: x5)
    complete(e1, subject: x3, object: x4)
  response
    prepare(e2, subject: x6, object: x5, for: x1)
```

## r189
From: b758 r189.

```reading
While a batch holds an item, when the laying service completes the request to prepare a workspace for the batch, the batches service shall check the item in the workspace.
shall [x3: service the laying service (constant), x6: service the batches service (constant)]
  while [x1: batch, x2: item]
    in(x2, x1)
  when [x4: request, x5: workspace]
    request(x4, laying.prepare, object: x5, for: x1)
    complete(e1, subject: x3, object: x4)
  response
    check(e2, subject: x6, object: x2, in: x5)
```

## r190
From: b764 r190.

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

## r191
From: b764 r191.

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

## r192
From: b764 r192.

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
