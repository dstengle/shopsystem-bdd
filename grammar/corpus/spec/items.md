# items: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: readiness#r23, reworded in request words (0.38.0).

```reading
While an item is `shaped` and the item meets the readiness bar, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x3: agent the person (constant), x4: service the backlog service (constant)]
  while [x1: item]
    status(x1) = `shaped`
    meet(subject: x1, object: x2)
  when
    request(e1, backlog.ready, subject: x3, object: x1)
  response
    initiates(e2, subject: x4, status(x1) = `ready`)
```

## r2
From: readiness#r24, reworded in request words (0.38.0).

```reading
While an item is `shaped` and the item does not meet the readiness bar, if the person readies the item, then the backlog service shall refuse the request and name every bar check that the item does not meet.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x3: agent the person (constant), x4: service the backlog service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: item]
    status(x1) = `shaped`
    not
      meet(subject: x1, object: x2)
  if
    request(e1, backlog.ready, subject: x3, object: x1)
  response
    refuse(e2, subject: x4, object: x5)
    every [x6: bar check]
      not
        meet(subject: x1, object: x6)
      scope
        name(e3, subject: x4, object: x6)
```

## r4
From: readiness#r4, reworded in request words (0.38.0).

```reading
When the person readies an item, the backlog service shall not ask a question.
shall [x1: agent the person (constant), x3: service the backlog service (constant)]
  when [x2: item]
    request(e1, backlog.ready, subject: x1, object: x2)
  response
    not [x4: question]
      ask(e2, subject: x3, object: x4)
```

## r5
From: readiness#r36, reworded in request words (0.38.0).

```reading
While an item is `shaped` and a term in the item violates a rule, if the person readies the item, then the backlog service shall refuse the request and name the term and the rule.
shall [x4: agent the person (constant), x5: service the backlog service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: term, x3: rule]
    status(x1) = `shaped`
    in(x2, x1)
    violate(subject: x2, object: x3)
  if
    request(e1, backlog.ready, subject: x4, object: x1)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
    name(e4, subject: x5, object: x3)
```

## r6
From: readiness#r41, reworded in request words (0.38.0).

```reading
While an item is `shaped` and a requirement in the item has no translation, if the person readies the item, then the backlog service shall refuse the request and name the requirement.
shall [x4: agent the person (constant), x5: service the backlog service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: requirement]
    status(x1) = `shaped`
    in(x2, x1)
    not [x3: translation]
      of(x3, x2)
  if
    request(e1, backlog.ready, subject: x4, object: x1)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r7
From: readiness#r46, reworded in request words (0.38.0).

```reading
While `universal` does not exist and an item is `shaped` and a universal condition in the item has no translation, if the person readies the item, then the backlog service shall refuse the request and name the universal condition.
shall [x1: capability `universal` (constant), x5: agent the person (constant), x6: service the backlog service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x2: item, x3: universal condition]
    not
      exists(x1)
    status(x2) = `shaped`
    in(x3, x2)
    not [x4: translation]
      of(x4, x3)
  if
    request(e1, backlog.ready, subject: x5, object: x2)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x3)
```

## r8
From: readiness#r50, reworded in request words (0.38.0).

```reading
While an item is `shaped` and a requirement in the item has no parse and a different requirement in the item has no translation, if the person readies the item, then the backlog service shall refuse the request and name every requirement in the item that has no parse and every requirement in the item that has no translation.
shall [x6: agent the person (constant), x7: service the backlog service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: requirement, x4: requirement]
    status(x1) = `shaped`
    in(x2, x1)
    not [x3: parse]
      of(x3, x2)
    distinct(x4, x2)
    in(x4, x1)
    not [x5: translation]
      of(x5, x4)
  if
    request(e1, backlog.ready, subject: x6, object: x1)
  response
    refuse(e2, subject: x7, object: x8)
    every [x9: requirement]
      in(x9, x1)
      not [x10: parse]
        of(x10, x9)
      scope
        name(e3, subject: x7, object: x9)
    every [x11: requirement]
      in(x11, x1)
      not [x12: translation]
        of(x12, x11)
      scope
        name(e4, subject: x7, object: x11)
```

## r9
From: readiness#r54, reworded in request words (0.38.0).

```reading
While an item is `shaped` and the item holds a chore and the item holds no requirement, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x4: agent the person (constant), x5: service the backlog service (constant)]
  while [x1: item, x2: chore]
    status(x1) = `shaped`
    in(x2, x1)
    not [x3: requirement]
      in(x3, x1)
  when
    request(e1, backlog.ready, subject: x4, object: x1)
  response
    initiates(e2, subject: x5, status(x1) = `ready`)
```

## r10
From: readiness#r58, reworded in request words (0.38.0).

```reading
While an item is `shaped` and a requirement group in the item violates a rule, if the person readies the item, then the backlog service shall refuse the request and name the requirement group and the rule.
shall [x4: agent the person (constant), x5: service the backlog service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: requirement group, x3: rule]
    status(x1) = `shaped`
    in(x2, x1)
    violate(subject: x2, object: x3)
  if
    request(e1, backlog.ready, subject: x4, object: x1)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
    name(e4, subject: x5, object: x3)
```

## r11
From: backlog#r5, reworded in request words (0.38.0).

```reading
When the person links an item, the backlog service shall keep a dependency on the item.
shall [x1: agent the person (constant), x3: service the backlog service (constant)]
  when [x2: item]
    request(e1, backlog.link, subject: x1, object: x2)
  response [x4: dependency]
    on(x4, x2)
    keep(e2, subject: x3, object: x4)
```

## r12
From: backlog#r15, reworded in request words (0.38.0).

```reading
When the person shows an item, the backlog service shall return the title of the item.
shall [x1: agent the person (constant), x3: service the backlog service (constant)]
  when [x2: item]
    request(e1, backlog.show, subject: x1, object: x2)
  response [x4: title]
    of(x4, x2)
    return(e2, subject: x3, object: x4)
```

## r13
From: backlog#r22, reworded in request words (0.38.0).

```reading
When the person notes an idea, the backlog service shall keep an item whose status is `idea`.
shall [x1: agent the person (constant), x3: service the backlog service (constant)]
  when [x2: idea]
    request(e1, backlog.note idea, subject: x1, object: x2)
  response [x4: item]
    status(x4) = `idea`
    keep(e2, subject: x3, object: x4)
```

## r14
From: backlog#r37, reworded in request words (0.38.0).

```reading
While the status of an item is `idea`, when the person shapes the item, the backlog service shall set the status of the item to `shaped`.
shall [x2: agent the person (constant), x3: service the backlog service (constant)]
  while [x1: item]
    status(x1) = `idea`
  when
    request(e1, backlog.shape, subject: x2, object: x1)
  response
    initiates(e2, subject: x3, status(x1) = `shaped`)
```

## r15
From: backlog#r38, reworded in request words (0.38.0).

```reading
While the status of an item is not `idea`, if the person shapes the item, then the backlog service shall refuse the request and name the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: item]
    not
      status(x1) = `idea`
  if
    request(e1, backlog.shape, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r16
From: backlog#r25, reworded in request words (0.38.0).

```reading
When the person rates an item with the value `high-value` and the urgency `low-urgency` and the size `small`, the backlog service shall set the value of the item to `high-value`, set the urgency of the item to `low-urgency`, set the size of the item to `small` and keep the item.
shall [x1: agent the person (constant), x3: service the backlog service (constant)]
  when [x2: item]
    request(e1, backlog.rate, subject: x1, object: x2)
    param(e1, value, `high-value`)
    param(e1, urgency, `low-urgency`)
    param(e1, size, `small`)
  response
    initiates(e2, subject: x3, value(x2) = `high-value`)
    initiates(e3, subject: x3, urgency(x2) = `low-urgency`)
    initiates(e4, subject: x3, size(x2) = `small`)
    keep(e5, subject: x3, object: x2)
```

## r17
From: backlog#r26, reworded in request words (0.38.0).

```reading
While an item is not `delivered` and a dependency on the item exists and another item has the dependency, when the person lists the backlog, the backlog service shall return the item and the dependency.
shall [x4: agent the person (constant), x5: backlog "the backlog of this bounded context" (indexical), x6: service the backlog service (constant)]
  while [x1: item, x2: dependency, x3: item]
    not
      status(x1) = `delivered`
    on(x2, x1)
    exists(x2)
    distinct(x3, x1)
    of(x2, x3)
  when
    request(e1, backlog.list, subject: x4, object: x5)
  response
    return(e2, subject: x6, object: x3)
    return(e3, subject: x6, object: x2)
```

## r19
From: backlog#r40, reworded in request words (0.38.0).

```reading
While the status of an item is one of `idea` or `shaped`, when the person declines the item, the backlog service shall set the status of the item to `refused`.
shall [x2: agent the person (constant), x3: service the backlog service (constant)]
  while [x1: item]
    or
      case
        status(x1) = `idea`
      case
        status(x1) = `shaped`
  when
    request(e1, backlog.decline, subject: x2, object: x1)
  response
    initiates(e2, subject: x3, status(x1) = `refused`)
```

## r20
From: backlog#r41, reworded in request words (0.38.0).

```reading
While the status of an item is `needs-input`, when the person answers the item, the backlog service shall set the status of the item to `shaped` and keep the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant)]
  while [x1: item]
    status(x1) = `needs-input`
  when
    request(e1, backlog.answer, subject: x2, object: x1)
  response
    initiates(e2, subject: x3, status(x1) = `shaped`)
    keep(e3, subject: x3, object: x1)
```

## r21
From: backlog#r42, reworded in request words (0.38.0).

```reading
While the status of an item is `needs-input`, when the person lists the backlog, the backlog service shall return the item and every question on the item.
shall [x2: agent the person (constant), x3: backlog "the backlog of this bounded context" (indexical), x4: service the backlog service (constant)]
  while [x1: item]
    status(x1) = `needs-input`
  when
    request(e1, backlog.list, subject: x2, object: x3)
  response
    return(e2, subject: x4, object: x1)
    every [x5: question]
      on(x5, x1)
      scope
        return(e3, subject: x4, object: x5)
```

## r22
From: backlog#r32, reworded in request words (0.38.0).

```reading
While the shared store is `rejecting`, when the person notes an idea, the backlog service shall keep an item whose status is `idea`, name the shared store and complete the request.
shall [x1: shared store "the shared store of this repository" (indexical), x2: agent the person (constant), x4: service the backlog service (constant), x6: request "the request the trigger makes" (indexical)]
  while
    availability(x1) = `rejecting`
  when [x3: idea]
    request(e1, backlog.note idea, subject: x2, object: x3)
  response [x5: item]
    status(x5) = `idea`
    keep(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
    complete(e4, subject: x4, object: x6)
```

## r23
From: backlog#r33, reworded in request words (0.38.0).

```reading
While the shared store is `unreachable`, when the person notes an idea, the backlog service shall keep an item whose status is `idea`, name the shared store and complete the request.
shall [x1: shared store "the shared store of this repository" (indexical), x2: agent the person (constant), x4: service the backlog service (constant), x6: request "the request the trigger makes" (indexical)]
  while
    availability(x1) = `unreachable`
  when [x3: idea]
    request(e1, backlog.note idea, subject: x2, object: x3)
  response [x5: item]
    status(x5) = `idea`
    keep(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
    complete(e4, subject: x4, object: x6)
```

## r24
From: backlog#r34, reworded in request words (0.38.0).

```reading
While this repository is in the workspace of a task, if the person notes an idea, then the backlog service shall refuse the request and name the task.
shall [x1: repository "the repository the request is made in" (indexical), x4: agent the person (constant), x6: service the backlog service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x2: task, x3: workspace]
    of(x3, x2)
    in(x1, x3)
  if [x5: idea]
    request(e1, backlog.note idea, subject: x4, object: x5)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
```

## r25
From: backlog#r35, reworded in request words (0.38.0).

```reading
While this repository is in a workspace that has a workspace name and the shared workspace of the workspace has a different workspace name, when the person notes an idea, the backlog service shall keep an item whose status is `idea` and keep the shared workspace.
shall [x1: repository "the repository the request is made in" (indexical), x6: agent the person (constant), x8: service the backlog service (constant)]
  while [x2: workspace, x3: workspace name, x4: shared workspace, x5: workspace name]
    of(x3, x2)
    in(x1, x2)
    of(x4, x2)
    distinct(x5, x3)
    of(x5, x4)
  when [x7: idea]
    request(e1, backlog.note idea, subject: x6, object: x7)
  response [x9: item]
    status(x9) = `idea`
    keep(e2, subject: x8, object: x9)
    keep(e3, subject: x8, object: x4)
```

## r26
From: backlog#r36, reworded in request words (0.38.0).

```reading
While an item exists, when the person lists the backlog, the backlog service shall return the item, the title of the item, the status of the item, the provenance of the item, the value of the item, the urgency of the item and the size of the item.
shall [x2: agent the person (constant), x3: backlog "the backlog of this bounded context" (indexical), x4: service the backlog service (constant)]
  while [x1: item]
    exists(x1)
  when
    request(e1, backlog.list, subject: x2, object: x3)
  response [x5: title, x6: status, x7: provenance, x8: value, x9: urgency, x10: size]
    return(e2, subject: x4, object: x1)
    of(x5, x1)
    return(e3, subject: x4, object: x5)
    status(x1) = x6
    return(e4, subject: x4, object: x6)
    provenance(x1) = x7
    return(e5, subject: x4, object: x7)
    value(x1) = x8
    return(e6, subject: x4, object: x8)
    urgency(x1) = x9
    return(e7, subject: x4, object: x9)
    size(x1) = x10
    return(e8, subject: x4, object: x10)
```

## r27
From: backlog#r43, reworded in request words (0.38.0).

```reading
While the status of an item is `idea` and the item has no shaping note, if the person shapes the item without a note, then the backlog service shall refuse the request and name the note.
shall [x3: agent the person (constant), x4: service the backlog service (constant), x5: request "the request the trigger makes" (indexical), x6: parameter note (constant)]
  while [x1: item]
    status(x1) = `idea`
    not [x2: shaping note]
      of(x2, x1)
  if
    request(e1, backlog.shape, subject: x3, object: x1)
    noparam(e1, note)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x6)
```

## r28
From: backlog#r44, reworded in request words (0.38.0).

```reading
While the status of an item is `idea` and the item has no shaping note, when the person lists the backlog, the backlog service shall return the item and name the note.
shall [x3: agent the person (constant), x4: backlog "the backlog of this bounded context" (indexical), x5: service the backlog service (constant), x6: parameter note (constant)]
  while [x1: item]
    status(x1) = `idea`
    not [x2: shaping note]
      of(x2, x1)
  when
    request(e1, backlog.list, subject: x3, object: x4)
  response
    return(e2, subject: x5, object: x1)
    name(e3, subject: x5, object: x6)
```

## r29
From: conversation#r8, reworded in request words (0.38.0).

```reading
When a session starts, the backlog service shall notify the session of every item, every title of an item and every batch.
shall [x2: service the backlog service (constant)]
  when [x1: session]
    start(e1, subject: x1)
  response
    every [x3: item]
      scope
        notify(e2, subject: x2, object: x1, of: x3)
    every [x4: title, x5: item]
      of(x4, x5)
      scope
        notify(e3, subject: x2, object: x1, of: x4)
    every [x6: batch]
      scope
        notify(e4, subject: x2, object: x1, of: x6)
```

## r30
From: intake#r10, reworded in request words (0.38.0).

```reading
While an item is `shaped` and a request line of the item is not `accepted`, `refused` or `withdrawn`, if a session readies the item, then the backlog service shall refuse the request and name the request line.
shall [x4: service the backlog service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: request line]
    status(x1) = `shaped`
    of(x2, x1)
    not
      line outcome(x2) = `accepted`
    not
      line outcome(x2) = `refused`
    not
      line outcome(x2) = `withdrawn`
  if [x3: session]
    request(e1, backlog.ready, subject: x3, object: x1)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r31
From: b431 r31.

```reading
While an item is `ready`, when the person reopens the item, the backlog service shall set the status of the item to `shaped` and keep the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant)]
  while [x1: item]
    status(x1) = `ready`
  when
    request(e1, backlog.reopen, subject: x2, object: x1)
  response
    initiates(e2, subject: x3, status(x1) = `shaped`)
    keep(e3, subject: x3, object: x1)
```

## r32
From: b431 r32.

```reading
While an item is not `ready`, if the person reopens the item, then the backlog service shall refuse the request and name the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: item]
    not
      status(x1) = `ready`
  if
    request(e1, backlog.reopen, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r34
From: b281 r34.

```reading
While the status of an item is one of `delivered`, `refused` or `withdrawn`, if the person merges the item, then the backlog service shall refuse the request and name the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: item]
    or
      case
        status(x1) = `delivered`
      case
        status(x1) = `refused`
      case
        status(x1) = `withdrawn`
  if
    request(e1, backlog.merge, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r35
From: b281 r35.

```reading
While an item is `ready` and the item meets the readiness bar, when the person readies the item, the backlog service shall complete the request and keep the item.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x3: agent the person (constant), x4: service the backlog service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: item]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
  when
    request(e1, backlog.ready, subject: x3, object: x1)
  response
    complete(e2, subject: x4, object: x5)
    keep(e3, subject: x4, object: x1)
```

## r36
From: b281 r36.

```reading
While an item is `ready` and the item does not meet the readiness bar, if the person readies the item, then the backlog service shall refuse the request and name every bar check that the item does not meet.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x3: agent the person (constant), x4: service the backlog service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: item]
    status(x1) = `ready`
    not
      meet(subject: x1, object: x2)
  if
    request(e1, backlog.ready, subject: x3, object: x1)
  response
    refuse(e2, subject: x4, object: x5)
    every [x6: bar check]
      not
        meet(subject: x1, object: x6)
      scope
        name(e3, subject: x4, object: x6)
```

## r37
Retires: r3. From: b281 r37.

```reading
While an item is not `shaped` and the item is not `ready`, if the person readies the item, then the backlog service shall refuse the request and name the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: item]
    not
      status(x1) = `shaped`
    not
      status(x1) = `ready`
  if
    request(e1, backlog.ready, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r38
From: b281 r38.

```reading
While the status of an item is one of `idea`, `shaped`, `ready` or `needs-input`, when the person annotates the item with a note, the backlog service shall keep the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant)]
  while [x1: item]
    or
      case
        status(x1) = `idea`
      case
        status(x1) = `shaped`
      case
        status(x1) = `ready`
      case
        status(x1) = `needs-input`
  when
    request(e1, backlog.annotate, subject: x2, object: x1)
    param(e1, note, some)
  response
    keep(e2, subject: x3, object: x1)
```

## r39
From: b281 r39.

```reading
While the status of an item is one of `delivered`, `refused` or `withdrawn`, if the person annotates the item, then the backlog service shall refuse the request and name the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: item]
    or
      case
        status(x1) = `delivered`
      case
        status(x1) = `refused`
      case
        status(x1) = `withdrawn`
  if
    request(e1, backlog.annotate, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r40
From: b444 r40.

```reading
While an item is `shaped` and a requirement in the item uses a construct that has no catalogue entry, if the person readies the item, then the backlog service shall refuse the request and name the requirement and the construct.
shall [x5: agent the person (constant), x6: service the backlog service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: requirement, x3: construct]
    status(x1) = `shaped`
    in(x2, x1)
    not [x4: catalogue entry]
      of(x4, x3)
    use(subject: x2, object: x3)
  if
    request(e1, backlog.ready, subject: x5, object: x1)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x2)
    name(e4, subject: x6, object: x3)
```

## r41
From: b477 r41.

```reading
While an item is `shaped` and a model line in the item violates a rule, if the person readies the item, then the backlog service shall refuse the request and name the model line and the rule.
shall [x4: agent the person (constant), x5: service the backlog service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: model line, x3: rule]
    status(x1) = `shaped`
    in(x2, x1)
    violate(subject: x2, object: x3)
  if
    request(e1, backlog.ready, subject: x4, object: x1)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
    name(e4, subject: x5, object: x3)
```

## r42
Retires: r18. From: b465 r42.

```reading
While the status of an item is one of `idea`, `shaped`, `ready` or `needs-input`, when the person withdraws the item with a reason, the backlog service shall set the status of the item to `withdrawn` and keep the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant)]
  while [x1: item]
    or
      case
        status(x1) = `idea`
      case
        status(x1) = `shaped`
      case
        status(x1) = `ready`
      case
        status(x1) = `needs-input`
  when
    request(e1, backlog.withdraw, subject: x2, object: x1)
    param(e1, reason, some)
  response
    initiates(e2, subject: x3, status(x1) = `withdrawn`)
    keep(e3, subject: x3, object: x1)
```

## r43
From: b484 r43.

```reading
If the person merges a successor with the successor and a reason, then the backlog service shall refuse the request and name the successor.
shall [x1: agent the person (constant), x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical)]
  if [x2: successor]
    request(e1, backlog.merge, subject: x1, object: x2)
    param(e1, successor, x2)
    param(e1, reason, some)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x2)
```

## r44
Retires: r33. From: b484 r44.

```reading
While a successor exists and the status of an item is one of `idea`, `shaped`, `ready` or `needs-input`, when the person merges the item with the successor and a reason, the backlog service shall set the status of the item to `withdrawn` and keep the item.
shall [x3: agent the person (constant), x4: service the backlog service (constant)]
  while [x1: successor, x2: item]
    exists(x1)
    or
      case
        status(x2) = `idea`
      case
        status(x2) = `shaped`
      case
        status(x2) = `ready`
      case
        status(x2) = `needs-input`
  when
    request(e1, backlog.merge, subject: x3, object: x2)
    param(e1, successor, x1)
    param(e1, reason, some)
  response
    initiates(e2, subject: x4, status(x2) = `withdrawn`)
    keep(e3, subject: x4, object: x2)
```

## r45
From: b484 r45.

```reading
While the status of a successor is one of `delivered`, `refused` or `withdrawn` and the status of an item is one of `idea`, `shaped`, `ready` or `needs-input`, if the person merges the item with the successor and a reason, then the backlog service shall refuse the request and name the successor.
shall [x3: agent the person (constant), x4: service the backlog service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: successor, x2: item]
    or
      case
        status(x1) = `delivered`
      case
        status(x1) = `refused`
      case
        status(x1) = `withdrawn`
    or
      case
        status(x2) = `idea`
      case
        status(x2) = `shaped`
      case
        status(x2) = `ready`
      case
        status(x2) = `needs-input`
  if
    request(e1, backlog.merge, subject: x3, object: x2)
    param(e1, successor, x1)
    param(e1, reason, some)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r46
From: b480 r46.

```reading
While the status of an item is `in-batch`, if the person merges the item, then the backlog service shall refuse the request and name the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: item]
    status(x1) = `in-batch`
  if
    request(e1, backlog.merge, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r47
From: b480 r47.

```reading
While the status of an item is `in-batch`, if the person annotates the item, then the backlog service shall refuse the request and name the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: item]
    status(x1) = `in-batch`
  if
    request(e1, backlog.annotate, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r48
From: b459 r48.

```reading
While the status of an item is one of `idea`, `shaped`, `ready`, `in-batch` or `needs-input`, when the person retitles the item with a title, the backlog service shall keep the item and the title of the item.
shall [x2: agent the person (constant), x4: service the backlog service (constant)]
  while [x1: item]
    or
      case
        status(x1) = `idea`
      case
        status(x1) = `shaped`
      case
        status(x1) = `ready`
      case
        status(x1) = `in-batch`
      case
        status(x1) = `needs-input`
  when [x3: title]
    request(e1, backlog.retitle, subject: x2, object: x1)
    param(e1, title, x3)
  response [x5: title]
    keep(e2, subject: x4, object: x1)
    of(x5, x1)
    keep(e3, subject: x4, object: x5)
```

## r49
From: b459 r49.

```reading
While the status of an item is one of `delivered`, `refused` or `withdrawn`, if the person retitles the item, then the backlog service shall refuse the request and name the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: item]
    or
      case
        status(x1) = `delivered`
      case
        status(x1) = `refused`
      case
        status(x1) = `withdrawn`
  if
    request(e1, backlog.retitle, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r50
From: b459 r50.

```reading
While the status of an item is one of `idea` or `shaped` and the item holds a requirement, when the person splits the item with the requirement, the backlog service shall keep another item that holds the requirement and name the item.
shall [x3: agent the person (constant), x4: service the backlog service (constant)]
  while [x1: item, x2: requirement]
    or
      case
        status(x1) = `idea`
      case
        status(x1) = `shaped`
    in(x2, x1)
  when
    request(e1, backlog.split, subject: x3, object: x1)
    param(e1, requirement, x2)
  response [x5: item]
    distinct(x5, x1)
    in(x2, x5)
    keep(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x5)
```

## r51
From: b459 r51.

```reading
While a requirement is in an item and the status of another item is one of `idea` or `shaped`, if the person splits the item with the requirement, then the backlog service shall refuse the request and name the requirement.
shall [x4: agent the person (constant), x5: service the backlog service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: item, x3: item]
    in(x1, x2)
    distinct(x3, x2)
    or
      case
        status(x3) = `idea`
      case
        status(x3) = `shaped`
  if
    request(e1, backlog.split, subject: x4, object: x3)
    param(e1, requirement, x1)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r52
From: b459 r52.

```reading
While the status of an item is not `idea` or `shaped`, if the person splits the item, then the backlog service shall refuse the request and name the item.
shall [x2: agent the person (constant), x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: item]
    not
      status(x1) = `idea`
    not
      status(x1) = `shaped`
  if
    request(e1, backlog.split, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r53
From: b516 r53.

```reading
While an item is `shaped` and the item holds a universal condition and the item holds no requirement and the item meets the readiness bar, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x4: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x6: service the backlog service (constant)]
  while [x1: item, x2: universal condition]
    status(x1) = `shaped`
    in(x2, x1)
    not [x3: requirement]
      in(x3, x1)
    meet(subject: x1, object: x4)
  when
    request(e1, backlog.ready, subject: x5, object: x1)
  response
    initiates(e2, subject: x6, status(x1) = `ready`)
```

## r54
From: b516 r54.

```reading
While an item is `shaped` and the item holds no requirement and a universal condition in the item has no translation, if the person readies the item, then the backlog service shall refuse the request and name the universal condition.
shall [x5: agent the person (constant), x6: service the backlog service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: item, x3: universal condition]
    status(x1) = `shaped`
    not [x2: requirement]
      in(x2, x1)
    in(x3, x1)
    not [x4: translation]
      of(x4, x3)
  if
    request(e1, backlog.ready, subject: x5, object: x1)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x3)
```

## r55
From: b581 r55.

```reading
While an item is `shaped` and a requirement group of a capability has a group title and the item holds another requirement group of the capability that has the group title, if the person readies the item, then the backlog service shall refuse the request and name the group title.
shall [x6: agent the person (constant), x7: service the backlog service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: requirement group, x3: capability, x4: group title, x5: requirement group]
    status(x1) = `shaped`
    of(x2, x3)
    of(x4, x2)
    distinct(x5, x2)
    of(x5, x3)
    of(x4, x5)
    in(x5, x1)
  if
    request(e1, backlog.ready, subject: x6, object: x1)
  response
    refuse(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x4)
```

## r56
From: b578 r56.

```reading
While an item is `in-batch`, when a session delivers the item, the backlog service shall set the status of the item to `delivered`.
shall [x3: service the backlog service (constant)]
  while [x1: item]
    status(x1) = `in-batch`
  when [x2: session]
    request(e1, backlog.deliver, subject: x2, object: x1)
  response
    initiates(e2, subject: x3, status(x1) = `delivered`)
```

## r57
From: b578 r57.

```reading
While an item is `in-batch`, when a session restores the item, the backlog service shall set the status of the item to `ready`.
shall [x3: service the backlog service (constant)]
  while [x1: item]
    status(x1) = `in-batch`
  when [x2: session]
    request(e1, backlog.restore, subject: x2, object: x1)
  response
    initiates(e2, subject: x3, status(x1) = `ready`)
```

## r58
From: b578 r58.

```reading
While an item is `in-batch`, when a session suspends the item with a question, the backlog service shall set the status of the item to `needs-input` and keep the question on the item.
shall [x4: service the backlog service (constant)]
  while [x1: item]
    status(x1) = `in-batch`
  when [x2: session, x3: question]
    request(e1, backlog.suspend, subject: x2, object: x1)
    param(e1, question, x3)
  response
    initiates(e2, subject: x4, status(x1) = `needs-input`)
    on(x3, x1)
    keep(e3, subject: x4, object: x3)
```

## r59
From: b578 r59.

```reading
While an item is `ready`, when a session allocates the item, the backlog service shall set the status of the item to `in-batch`.
shall [x3: service the backlog service (constant)]
  while [x1: item]
    status(x1) = `ready`
  when [x2: session]
    request(e1, backlog.allocate, subject: x2, object: x1)
  response
    initiates(e2, subject: x3, status(x1) = `in-batch`)
```

## r60
From: b585 r60.

```reading
While an item is not `ready`, if a session allocates the item, then the backlog service shall refuse the request and name the item and the `item not ready` reason.
shall [x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical), x5: reason `item not ready` (parameter)]
  while [x1: item]
    not
      status(x1) = `ready`
  if [x2: session]
    request(e1, backlog.allocate, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
    name(e4, subject: x3, object: x5)
```

## r61
From: b585 r61.

```reading
While an item is not `in-batch`, if a session delivers the item, then the backlog service shall refuse the request and name the item and the `item not in-batch` reason.
shall [x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical), x5: reason `item not in-batch` (parameter)]
  while [x1: item]
    not
      status(x1) = `in-batch`
  if [x2: session]
    request(e1, backlog.deliver, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
    name(e4, subject: x3, object: x5)
```

## r62
From: b585 r62.

```reading
While an item is not `in-batch`, if a session restores the item, then the backlog service shall refuse the request and name the item and the `item not in-batch` reason.
shall [x3: service the backlog service (constant), x4: request "the request the trigger makes" (indexical), x5: reason `item not in-batch` (parameter)]
  while [x1: item]
    not
      status(x1) = `in-batch`
  if [x2: session]
    request(e1, backlog.restore, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
    name(e4, subject: x3, object: x5)
```

## r63
From: b585 r63.

```reading
While an item is not `in-batch`, if a session suspends the item with a question, then the backlog service shall refuse the request and name the item and the `item not in-batch` reason.
shall [x4: service the backlog service (constant), x5: request "the request the trigger makes" (indexical), x6: reason `item not in-batch` (parameter)]
  while [x1: item]
    not
      status(x1) = `in-batch`
  if [x2: session, x3: question]
    request(e1, backlog.suspend, subject: x2, object: x1)
    param(e1, question, x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
    name(e4, subject: x4, object: x6)
```

## r64
From: b654 r64.

```reading
While an item is `shaped` and the item holds a model line that moves to an area and the item holds no requirement and the item meets the readiness bar, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x5: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x6: agent the person (constant), x7: service the backlog service (constant)]
  while [x1: item, x2: model line, x3: area]
    status(x1) = `shaped`
    move#3(subject: x2, to: x3)
    in(x2, x1)
    not [x4: requirement]
      in(x4, x1)
    meet(subject: x1, object: x5)
  when
    request(e1, backlog.ready, subject: x6, object: x1)
  response
    initiates(e2, subject: x7, status(x1) = `ready`)
```

## r65
From: b654 r65.

```reading
While an item is `shaped` and the item moves a term and the item holds no requirement and the item meets the readiness bar, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x4: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x6: service the backlog service (constant)]
  while [x1: item, x2: term]
    status(x1) = `shaped`
    move#4(subject: x1, object: x2)
    not [x3: requirement]
      in(x3, x1)
    meet(subject: x1, object: x4)
  when
    request(e1, backlog.ready, subject: x5, object: x1)
  response
    initiates(e2, subject: x6, status(x1) = `ready`)
```

## r66
From: b648 r66.

```reading
While an item is `shaped` and the item meets the readiness bar and a capability holds a requirement id that the item holds, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x6: service the backlog service (constant)]
  while [x1: item, x3: capability, x4: requirement id]
    status(x1) = `shaped`
    meet(subject: x1, object: x2)
    in(x4, x1)
    in(x4, x3)
  when
    request(e1, backlog.ready, subject: x5, object: x1)
  response
    initiates(e2, subject: x6, status(x1) = `ready`)
```

## r67
From: b648 r67.

```reading
While an item is `ready` and the item meets the readiness bar and a capability holds a requirement id that the item holds, when the person readies the item, the backlog service shall complete the request and keep the item.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x6: service the backlog service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: item, x3: capability, x4: requirement id]
    status(x1) = `ready`
    meet(subject: x1, object: x2)
    in(x4, x1)
    in(x4, x3)
  when
    request(e1, backlog.ready, subject: x5, object: x1)
  response
    complete(e2, subject: x6, object: x7)
    keep(e3, subject: x6, object: x1)
```

## r68
From: b688 r68.

```reading
While an item is `shaped` and the item imports a pack and the item holds no requirement and the item meets the readiness bar, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x4: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x6: service the backlog service (constant)]
  while [x1: item, x2: pack]
    status(x1) = `shaped`
    import#5(subject: x1, object: x2)
    not [x3: requirement]
      in(x3, x1)
    meet(subject: x1, object: x4)
  when
    request(e1, backlog.ready, subject: x5, object: x1)
  response
    initiates(e2, subject: x6, status(x1) = `ready`)
```

## r69
From: b688 r69.

```reading
While an item is `shaped` and the item retires a term and the item holds no requirement and the item meets the readiness bar, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x4: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x6: service the backlog service (constant)]
  while [x1: item, x2: term]
    status(x1) = `shaped`
    retire#4(subject: x1, object: x2)
    not [x3: requirement]
      in(x3, x1)
    meet(subject: x1, object: x4)
  when
    request(e1, backlog.ready, subject: x5, object: x1)
  response
    initiates(e2, subject: x6, status(x1) = `ready`)
```

## r70
From: b694 r70.

```reading
While an item is `shaped` and the item imports a pack and the pack has a term and an element refers to the term and the term spells another element and the item retires another term that means the element and the item meets the readiness bar, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x7: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x8: agent the person (constant), x9: service the backlog service (constant)]
  while [x1: item, x2: pack, x3: term, x4: element, x5: element, x6: term]
    status(x1) = `shaped`
    import#5(subject: x1, object: x2)
    of(x3, x2)
    refer#3(subject: x4, to: x3)
    distinct(x5, x4)
    spell(subject: x3, object: x5)
    distinct(x6, x3)
    mean(subject: x6, object: x5)
    retire#4(subject: x1, object: x6)
    meet(subject: x1, object: x7)
  when
    request(e1, backlog.ready, subject: x8, object: x1)
  response
    initiates(e2, subject: x9, status(x1) = `ready`)
```

## r71
From: b705 r71.

```reading
While an item is `shaped` and the item holds a port line and the item holds a core line and the port line supports the requirement id of the core line, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x5: agent the person (constant), x6: service the backlog service (constant)]
  while [x1: item, x2: port line, x3: core line, x4: requirement id]
    status(x1) = `shaped`
    in(x2, x1)
    in(x3, x1)
    of(x4, x3)
    support(subject: x2, object: x4)
  when
    request(e1, backlog.ready, subject: x5, object: x1)
  response
    initiates(e2, subject: x6, status(x1) = `ready`)
```

## r72
From: b721 r72.

```reading
While an item is `shaped` and the item holds a port line that governs an operation and the operation has an operation outcome and no core line handles the operation outcome and no port line excludes the operation outcome, if the person readies the item, then the backlog service shall refuse the request and name the operation outcome and `v_pb2`.
shall [x7: agent the person (constant), x8: service the backlog service (constant), x9: request "the request the trigger makes" (indexical), x10: thing `v_pb2` (parameter)]
  while [x1: item, x2: port line, x3: operation, x4: operation outcome]
    status(x1) = `shaped`
    govern(subject: x2, object: x3)
    in(x2, x1)
    of(x4, x3)
    not [x5: core line]
      handle(subject: x5, object: x4)
    not [x6: port line]
      exclude(subject: x6, object: x4)
  if
    request(e1, backlog.ready, subject: x7, object: x1)
  response
    refuse(e2, subject: x8, object: x9)
    name(e3, subject: x8, object: x4)
    name(e4, subject: x8, object: x10)
```

## r73
From: b731 r73.

```reading
While an item is `shaped` and an area holds a lifecycle and the lifecycle has a transition and another area holds an operation that performs the transition and the item holds a core line that uses the operation, if the person readies the item, then the backlog service shall refuse the request and name the core line and `v_m9`.
shall [x8: agent the person (constant), x9: service the backlog service (constant), x10: request "the request the trigger makes" (indexical), x11: thing `v_m9` (parameter)]
  while [x1: item, x2: area, x3: lifecycle, x4: transition, x5: area, x6: operation, x7: core line]
    status(x1) = `shaped`
    in(x3, x2)
    of(x4, x3)
    distinct(x5, x2)
    perform(subject: x6, object: x4)
    in(x6, x5)
    use(subject: x7, object: x6)
    in(x7, x1)
  if
    request(e1, backlog.ready, subject: x8, object: x1)
  response
    refuse(e2, subject: x9, object: x10)
    name(e3, subject: x9, object: x7)
    name(e4, subject: x9, object: x11)
```

## r74
From: b845 r74.

```reading
While an item is `shaped` and the item holds a requirement group that serves a job and the item holds no requirement and the item meets the readiness bar, when the person readies the item, the backlog service shall set the status of the item to `ready`.
shall [x5: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x6: agent the person (constant), x7: service the backlog service (constant)]
  while [x1: item, x2: requirement group, x3: job]
    status(x1) = `shaped`
    serve(subject: x2, object: x3)
    in(x2, x1)
    not [x4: requirement]
      in(x4, x1)
    meet(subject: x1, object: x5)
  when
    request(e1, backlog.ready, subject: x6, object: x1)
  response
    initiates(e2, subject: x7, status(x1) = `ready`)
```
