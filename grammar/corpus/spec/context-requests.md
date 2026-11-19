# context-requests: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: intake#r11, reworded in request words (0.38.0).

```reading
When a session settles a request line of a context request with the line outcome `rewritten`, the context requests service shall set the line outcome of the request line to `rewritten`, keep a request line of the context request that counters the request line, set the side of the context request to `asker` and keep an entry on the context request.
shall [x4: service the context requests service (constant)]
  when [x1: session, x2: request line, x3: context request]
    of(x2, x3)
    request(e1, context requests.settle, subject: x1, object: x2)
    param(e1, line outcome, `rewritten`)
  response [x5: request line, x6: entry]
    initiates(e2, subject: x4, line outcome(x2) = `rewritten`)
    of(x5, x3)
    counter(subject: x5, object: x2)
    keep(e3, subject: x4, object: x5)
    initiates(e4, subject: x4, side(x3) = `asker`)
    on(x6, x3)
    keep(e5, subject: x4, object: x6)
```

## r2
From: intake#r12, reworded in request words (0.38.0).

```reading
When a session settles a request line of a context request with the line outcome `refused`, the context requests service shall set the line outcome of the request line to `refused`, keep a line reason of the request line and keep the context request.
shall [x4: service the context requests service (constant)]
  when [x1: session, x2: request line, x3: context request]
    of(x2, x3)
    request(e1, context requests.settle, subject: x1, object: x2)
    param(e1, line outcome, `refused`)
  response [x5: line reason]
    initiates(e2, subject: x4, line outcome(x2) = `refused`)
    of(x5, x2)
    keep(e3, subject: x4, object: x5)
    keep(e4, subject: x4, object: x3)
```

## r3
From: intake#r13, reworded in request words (0.38.0).

```reading
If a session settles a request line with the line outcome `refused` and without a line reason, then the context requests service shall refuse the request and name the line reason.
shall [x3: service the context requests service (constant), x4: request "the request the trigger makes" (indexical)]
  if [x1: session, x2: request line]
    request(e1, context requests.settle, subject: x1, object: x2)
    param(e1, line outcome, `refused`)
    noparam(e1, line reason)
  response [x5: line reason]
    refuse(e2, subject: x3, object: x4)
    of(x5, x2)
    name(e3, subject: x3, object: x5)
```

## r4
From: requests#r59, reworded in request words (0.38.0).

```reading
When the person raises a context request for a context request, the context requests service shall keep the context request.
shall [x1: agent the person (constant), x4: service the context requests service (constant)]
  when [x2: context request, x3: context request]
    for(x2, x3)
    request(e1, context requests.raise, subject: x1, object: x2)
  response
    keep(e2, subject: x4, object: x3)
```

## r5
From: requests#r60, reworded in request words (0.38.0).

```reading
If the person raises a context request without an origin and a thread, then the context requests service shall refuse the request and name the thread.
shall [x1: agent the person (constant), x3: service the context requests service (constant), x4: request "the request the trigger makes" (indexical)]
  if [x2: context request]
    request(e1, context requests.raise, subject: x1, object: x2)
    noparam(e1, origin)
    noparam(e1, thread)
  response [x5: thread]
    refuse(e2, subject: x3, object: x4)
    of(x5, x2)
    name(e3, subject: x3, object: x5)
```

## r6
From: requests#r61, reworded in request words (0.38.0).

```reading
While this bounded context holds an upstream entry, if the person raises a context request with an origin and a thread, then the context requests service shall refuse the request and name the origin.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x6: service the context requests service (constant), x7: request "the request the trigger makes" (indexical), x8: parameter origin (constant)]
  while [x2: upstream entry]
    in(x2, x1)
  if [x4: context request, x5: thread]
    request(e1, context requests.raise, subject: x3, object: x4)
    param(e1, origin, some)
    param(e1, thread, x5)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x8)
```

## r7
From: requests#r62, reworded in request words (0.38.0).

```reading
If the person raises a context request with a text that does not identify this bounded context, then the context requests service shall refuse the request and name the text.
shall [x1: agent the person (constant), x4: bounded context "the bounded context whose repository the command runs in" (indexical), x5: service the context requests service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: context request, x3: text]
    not
      identify(subject: x3, object: x4)
    request(e1, context requests.raise, subject: x1, object: x2)
    param(e1, text, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r8
From: requests#r63, reworded in request words (0.38.0).

```reading
While a context request is `open`, when the person settles a request line in the context request with the line outcome `accepted`, the context requests service shall set the line outcome of the request line to `accepted` and keep the context request.
shall [x2: agent the person (constant), x4: service the context requests service (constant)]
  while [x1: context request]
    status(x1) = `open`
  when [x3: request line]
    in(x3, x1)
    request(e1, context requests.settle, subject: x2, object: x3)
    param(e1, line outcome, `accepted`)
  response
    initiates(e2, subject: x4, line outcome(x3) = `accepted`)
    keep(e3, subject: x4, object: x1)
```

## r9
From: requests#r64, reworded in request words (0.38.0).

```reading
While a context request is `awaiting-asker`, if the person settles a request line in the context request, then the context requests service shall refuse the request and name the context request.
shall [x2: agent the person (constant), x4: service the context requests service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: context request]
    status(x1) = `awaiting-asker`
  if [x3: request line]
    in(x3, x1)
    request(e1, context requests.settle, subject: x2, object: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r10
From: requests#r65, reworded in request words (0.38.0).

```reading
While a context request is `open` and the context request does not address this bounded context, if the person settles a request line in the context request, then the context requests service shall refuse the request and name the context request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x5: service the context requests service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: context request]
    status(x1) = `open`
    not
      address(subject: x1, object: x2)
  if [x4: request line]
    in(x4, x1)
    request(e1, context requests.settle, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r11
From: requests#r66, reworded in request words (0.38.0).

```reading
While a context request is `open`, when the person asks a question on the context request, the context requests service shall keep the question.
shall [x2: agent the person (constant), x4: service the context requests service (constant)]
  while [x1: context request]
    status(x1) = `open`
  when [x3: question]
    on(x3, x1)
    request(e1, context requests.ask, subject: x2, object: x3)
  response
    keep(e2, subject: x4, object: x3)
```

## r12
From: requests#r67, reworded in request words (0.38.0).

```reading
While a context request is `awaiting-asker` and the context request originates from this bounded context, when the person replies to the context request, the context requests service shall keep an answer.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: service the context requests service (constant)]
  while [x1: context request]
    status(x1) = `awaiting-asker`
    originate(subject: x1, from: x2)
  when
    request(e1, context requests.reply, subject: x3, to: x1)
  response [x5: answer]
    keep(e2, subject: x4, object: x5)
```

## r13
From: requests#r68, reworded in request words (0.38.0).

```reading
While a context request is not `accepted`, if the person resolves the context request, then the context requests service shall refuse the request and name the context request.
shall [x2: agent the person (constant), x3: service the context requests service (constant), x4: request "the request the trigger makes" (indexical)]
  while [x1: context request]
    not
      status(x1) = `accepted`
  if
    request(e1, context requests.resolve, subject: x2, object: x1)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x1)
```

## r14
From: requests#r69, reworded in request words (0.38.0).

```reading
When the person surveys this bounded context, the context requests service shall return every context request, the status of every context request and every observation that no context request cites.
shall [x1: agent the person (constant), x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: service the context requests service (constant)]
  when
    request(e1, context requests.survey, subject: x1, object: x2)
  response
    every [x4: context request]
      scope
        return(e2, subject: x3, object: x4)
    every [x5: context request]
      scope [x6: status]
        status(x5) = x6
        return(e3, subject: x3, object: x6)
    every [x7: observation]
      not [x8: context request]
        cite(subject: x8, object: x7)
      scope
        return(e4, subject: x3, object: x7)
```

## r15
From: requests#r70, reworded in request words (0.38.0).

```reading
When the person inspects a context request, the context requests service shall return the status of the context request and every request line in the context request.
shall [x1: agent the person (constant), x3: service the context requests service (constant)]
  when [x2: context request]
    request(e1, context requests.inspect, subject: x1, object: x2)
  response [x4: status]
    status(x2) = x4
    return(e2, subject: x3, object: x4)
    every [x5: request line]
      in(x5, x2)
      scope
        return(e3, subject: x3, object: x5)
```

## r16
From: requests#r71, reworded in request words (0.38.0).

```reading
When the person raises a context request, the context requests service shall keep a context request whose status is `open` and a thread of the context request.
shall [x1: agent the person (constant), x3: service the context requests service (constant)]
  when [x2: context request]
    request(e1, context requests.raise, subject: x1, object: x2)
  response [x4: context request, x5: thread]
    status(x4) = `open`
    keep(e2, subject: x3, object: x4)
    of(x5, x4)
    keep(e3, subject: x3, object: x5)
```

## r17
From: requests#r72, reworded in request words (0.38.0).

```reading
If the person raises a context request with a bounded context that has no channel, then the context requests service shall refuse the request and name the bounded context.
shall [x1: agent the person (constant), x5: service the context requests service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: context request, x3: bounded context]
    not [x4: channel]
      of(x4, x3)
    request(e1, context requests.raise, subject: x1, object: x2)
    param(e1, bounded context, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r18
From: requests#r73, reworded in request words (0.38.0).

```reading
While a context request is `open`, when a session offers on the context request, the context requests service shall keep an entry on the context request and set the status of the context request to `awaiting-asker`.
shall [x3: service the context requests service (constant)]
  while [x1: context request]
    status(x1) = `open`
  when [x2: session]
    request(e1, context requests.offer, subject: x2, on: x1)
  response [x4: entry]
    on(x4, x1)
    keep(e2, subject: x3, object: x4)
    initiates(e3, subject: x3, status(x1) = `awaiting-asker`)
```

## r19
From: requests#r74, reworded in request words (0.38.0).

```reading
While a context request is `awaiting-asker`, when the person serves the context request, the context requests service shall set the status of the context request to `delivered`, keep a resolution and keep an entry on the context request.
shall [x2: agent the person (constant), x3: service the context requests service (constant)]
  while [x1: context request]
    status(x1) = `awaiting-asker`
  when
    request(e1, context requests.serve, subject: x2, object: x1)
  response [x4: resolution, x5: entry]
    initiates(e2, subject: x3, status(x1) = `delivered`)
    keep(e3, subject: x3, object: x4)
    on(x5, x1)
    keep(e4, subject: x3, object: x5)
```

## r20
From: requests#r75, reworded in request words (0.38.0).

```reading
While a context request is `awaiting-asker`, when the person proposes to the context request, the context requests service shall keep a request line.
shall [x2: agent the person (constant), x3: service the context requests service (constant)]
  while [x1: context request]
    status(x1) = `awaiting-asker`
  when
    request(e1, context requests.propose, subject: x2, to: x1)
  response [x4: request line]
    keep(e2, subject: x3, object: x4)
```

## r21
From: requests#r76, reworded in request words (0.38.0).

```reading
While an entry on a context request conforms to the entry form and the context request does not hold the entry, when a session catches up, the context requests service shall keep the entry and return every context request.
shall [x3: artifact the entry form (constant), x5: service the context requests service (constant)]
  while [x1: entry, x2: context request]
    on(x1, x2)
    conforms(x1, x3)
    not
      in(x1, x2)
  when [x4: session]
    request(e1, context requests.catch up, subject: x4)
  response
    keep(e2, subject: x5, object: x1)
    every [x6: context request]
      scope
        return(e3, subject: x5, object: x6)
```

## r22
From: requests#r78, reworded in request words (0.38.0).

```reading
While a context request is `awaiting-asker`, when the person passes the turn of the context request, the context requests service shall set the status of the context request to `awaiting-upstream`, set the side of the context request to `upstream` and keep an entry on the context request.
shall [x2: agent the person (constant), x4: service the context requests service (constant)]
  while [x1: context request]
    status(x1) = `awaiting-asker`
  when [x3: turn]
    of(x3, x1)
    request(e1, context requests.pass turn, subject: x2, object: x3)
  response [x5: entry]
    initiates(e2, subject: x4, status(x1) = `awaiting-upstream`)
    initiates(e3, subject: x4, side(x1) = `upstream`)
    on(x5, x1)
    keep(e4, subject: x4, object: x5)
```

## r23
From: requests#r79, reworded in request words (0.38.0).

```reading
While a context request is `open` and a request line in the context request is not `accepted`, `refused` or `withdrawn`, when the person passes the turn of the context request, the context requests service shall set the status of the context request to `awaiting-asker` and keep an entry on the context request.
shall [x3: agent the person (constant), x5: service the context requests service (constant)]
  while [x1: context request, x2: request line]
    status(x1) = `open`
    in(x2, x1)
    not
      line outcome(x2) = `accepted`
    not
      line outcome(x2) = `refused`
    not
      line outcome(x2) = `withdrawn`
  when [x4: turn]
    of(x4, x1)
    request(e1, context requests.pass turn, subject: x3, object: x4)
  response [x6: entry]
    initiates(e2, subject: x5, status(x1) = `awaiting-asker`)
    on(x6, x1)
    keep(e3, subject: x5, object: x6)
```

## r24
From: requests#r80, reworded in request words (0.38.0).

```reading
While a context request is `open` and a request line in the context request is `accepted` and every request line in the context request is one of `accepted`, `refused` or `withdrawn`, when the person passes the turn of the context request, the context requests service shall keep an entry on the context request and keep the side of the context request.
shall [x4: agent the person (constant), x6: service the context requests service (constant)]
  while [x1: context request, x2: request line]
    status(x1) = `open`
    in(x2, x1)
    line outcome(x2) = `accepted`
    every [x3: request line]
      in(x3, x1)
      scope
        or
          case
            line outcome(x3) = `accepted`
          case
            line outcome(x3) = `refused`
          case
            line outcome(x3) = `withdrawn`
  when [x5: turn]
    of(x5, x1)
    request(e1, context requests.pass turn, subject: x4, object: x5)
  response [x7: entry, x8: side]
    on(x7, x1)
    keep(e2, subject: x6, object: x7)
    side(x1) = x8
    keep(e3, subject: x6, object: x8)
```

## r25
From: requests#r81, reworded in request words (0.38.0).

```reading
While a context request is `open` and a request line in the context request is `refused` and every request line in the context request is `refused`, when the person passes the turn of the context request, the context requests service shall set the status of the context request to `refused` and keep an entry on the context request.
shall [x4: agent the person (constant), x6: service the context requests service (constant)]
  while [x1: context request, x2: request line]
    status(x1) = `open`
    in(x2, x1)
    line outcome(x2) = `refused`
    every [x3: request line]
      in(x3, x1)
      scope
        line outcome(x3) = `refused`
  when [x5: turn]
    of(x5, x1)
    request(e1, context requests.pass turn, subject: x4, object: x5)
  response [x7: entry]
    initiates(e2, subject: x6, status(x1) = `refused`)
    on(x7, x1)
    keep(e3, subject: x6, object: x7)
```

## r26
From: requests#r82, reworded in request words (0.38.0).

```reading
While a request line does not conform to the requirement grammar of this bounded context, if a session settles the request line with the line outcome `accepted`, then the context requests service shall refuse the request and name the request line.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x5: service the context requests service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: request line, x3: requirement grammar]
    of(x3, x2)
    not
      conforms(x1, x3)
  if [x4: session]
    request(e1, context requests.settle, subject: x4, object: x1)
    param(e1, line outcome, `accepted`)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r27
From: requests#r83, reworded in request words (0.38.0).

```reading
While a context request is `open` and a request line in the context request is `accepted` and every request line in the context request is one of `accepted`, `refused` or `withdrawn`, when the person accepts the context request, the context requests service shall set the status of the context request to `accepted`, keep an item whose status is `shaped` and keep an entry on the context request.
shall [x4: agent the person (constant), x5: service the context requests service (constant)]
  while [x1: context request, x2: request line]
    status(x1) = `open`
    in(x2, x1)
    line outcome(x2) = `accepted`
    every [x3: request line]
      in(x3, x1)
      scope
        or
          case
            line outcome(x3) = `accepted`
          case
            line outcome(x3) = `refused`
          case
            line outcome(x3) = `withdrawn`
  when
    request(e1, context requests.accept, subject: x4, object: x1)
  response [x6: item, x7: entry]
    initiates(e2, subject: x5, status(x1) = `accepted`)
    status(x6) = `shaped`
    keep(e3, subject: x5, object: x6)
    on(x7, x1)
    keep(e4, subject: x5, object: x7)
```

## r28
From: requests#r84, reworded in request words (0.38.0).

```reading
While a request line in a context request is not `accepted`, `refused` or `withdrawn`, if the person accepts the context request, then the context requests service shall refuse the request and name the request line.
shall [x3: agent the person (constant), x4: service the context requests service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: request line, x2: context request]
    in(x1, x2)
    not
      line outcome(x1) = `accepted`
    not
      line outcome(x1) = `refused`
    not
      line outcome(x1) = `withdrawn`
  if
    request(e1, context requests.accept, subject: x3, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r29
From: requests#r85, reworded in request words (0.38.0).

```reading
While a context request is `accepted`, when the person resolves the context request, the context requests service shall set the status of the context request to `delivered`, keep a resolution, set the side of the context request to `asker` and keep an entry on the context request.
shall [x2: agent the person (constant), x3: service the context requests service (constant)]
  while [x1: context request]
    status(x1) = `accepted`
  when
    request(e1, context requests.resolve, subject: x2, object: x1)
  response [x4: resolution, x5: entry]
    initiates(e2, subject: x3, status(x1) = `delivered`)
    keep(e3, subject: x3, object: x4)
    initiates(e4, subject: x3, side(x1) = `asker`)
    on(x5, x1)
    keep(e5, subject: x3, object: x5)
```

## r30
From: requests#r88, reworded in request words (0.38.0).

```reading
While this repository is `rejecting`, if the person raises a context request, then the context requests service shall refuse the request, name this repository and not keep a thread.
shall [x1: repository "the repository the request is made in" (indexical), x2: agent the person (constant), x4: service the context requests service (constant), x5: request "the request the trigger makes" (indexical)]
  while
    store(x1) = `rejecting`
  if [x3: context request]
    request(e1, context requests.raise, subject: x2, object: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
    not [x6: thread]
      keep(e4, subject: x4, object: x6)
```

## r31
From: requests#r89, reworded in request words (0.38.0).

```reading
While this repository is `rejecting` and a context request is `open`, if the person passes the turn of the context request, then the context requests service shall refuse the request, name this repository and not keep an entry on the context request.
shall [x1: repository "the repository the request is made in" (indexical), x3: agent the person (constant), x5: service the context requests service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x2: context request]
    store(x1) = `rejecting`
    status(x2) = `open`
  if [x4: turn]
    of(x4, x2)
    request(e1, context requests.pass turn, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
    not [x7: entry]
      on(x7, x2)
      keep(e4, subject: x5, object: x7)
```

## r32
From: requests#r90, reworded in request words (0.38.0).

```reading
While this repository is `rejecting` and a context request is `awaiting-asker`, if the person serves the context request, then the context requests service shall refuse the request, name this repository and not keep an entry on the context request.
shall [x1: repository "the repository the request is made in" (indexical), x3: agent the person (constant), x4: service the context requests service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x2: context request]
    store(x1) = `rejecting`
    status(x2) = `awaiting-asker`
  if
    request(e1, context requests.serve, subject: x3, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
    not [x6: entry]
      on(x6, x2)
      keep(e4, subject: x4, object: x6)
```

## r33
From: requests#r91, reworded in request words (0.38.0).

```reading
While a context request addresses this bounded context and the context request does not originate from this bounded context, if the person replies to the context request, then the context requests service shall refuse the request and name the context request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: service the context requests service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: context request]
    address(subject: x1, object: x2)
    not
      originate(subject: x1, from: x2)
  if
    request(e1, context requests.reply, subject: x3, to: x1)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r34
From: requests#r92, reworded in request words (0.38.0).

```reading
While a context request addresses this bounded context and the context request does not originate from this bounded context and the context request is `awaiting-asker`, if the person passes the turn of the context request, then the context requests service shall refuse the request and name the context request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x5: service the context requests service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: context request]
    address(subject: x1, object: x2)
    not
      originate(subject: x1, from: x2)
    status(x1) = `awaiting-asker`
  if [x4: turn]
    of(x4, x1)
    request(e1, context requests.pass turn, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r35
From: requests#r93, reworded in request words (0.38.0).

```reading
While a context request originates from this bounded context and the context request does not address this bounded context and the context request is `open`, if the person passes the turn of the context request, then the context requests service shall refuse the request and name the context request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x5: service the context requests service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: context request]
    originate(subject: x1, from: x2)
    not
      address(subject: x1, object: x2)
    status(x1) = `open`
  if [x4: turn]
    of(x4, x1)
    request(e1, context requests.pass turn, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r36
From: requests#r94, reworded in request words (0.38.0).

```reading
While a context request originates from this bounded context and the context request does not address this bounded context and the context request is `awaiting-upstream`, if the person passes the turn of the context request, then the context requests service shall refuse the request and name the context request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x5: service the context requests service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: context request]
    originate(subject: x1, from: x2)
    not
      address(subject: x1, object: x2)
    status(x1) = `awaiting-upstream`
  if [x4: turn]
    of(x4, x1)
    request(e1, context requests.pass turn, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r37
From: requests#r95, reworded in request words (0.38.0).

```reading
While an entry on a context request conforms to the entry form and the side of the entry is `asker` and the entry holds a field whose side is `upstream` and the context request does not hold the entry, when a session catches up, the context requests service shall keep the entry and not keep the field.
shall [x3: artifact the entry form (constant), x6: service the context requests service (constant)]
  while [x1: entry, x2: context request, x4: field]
    on(x1, x2)
    conforms(x1, x3)
    side(x1) = `asker`
    side(x4) = `upstream`
    in(x4, x1)
    not
      in(x1, x2)
  when [x5: session]
    request(e1, context requests.catch up, subject: x5)
  response
    keep(e2, subject: x6, object: x1)
    not
      keep(e3, subject: x6, object: x4)
```

## r38
From: requests#r96, reworded in request words (0.38.0).

```reading
While a context request is one of `delivered`, `refused` or `withdrawn` and an entry on the context request conforms to the entry form and the context request does not hold the entry, when a session catches up, the context requests service shall keep the entry and keep the status of the context request and the side of the context request.
shall [x3: artifact the entry form (constant), x5: service the context requests service (constant)]
  while [x1: context request, x2: entry]
    or
      case
        status(x1) = `delivered`
      case
        status(x1) = `refused`
      case
        status(x1) = `withdrawn`
    on(x2, x1)
    conforms(x2, x3)
    not
      in(x2, x1)
  when [x4: session]
    request(e1, context requests.catch up, subject: x4)
  response [x6: status, x7: side]
    keep(e2, subject: x5, object: x2)
    status(x1) = x6
    keep(e3, subject: x5, object: x6)
    side(x1) = x7
    keep(e4, subject: x5, object: x7)
```

## r39
From: requests#r102, reworded in request words (0.38.0).

```reading
While this bounded context holds an upstream entry, if the person raises a context request for a context request with an origin, then the context requests service shall refuse the request and name the origin.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x6: service the context requests service (constant), x7: request "the request the trigger makes" (indexical), x8: parameter origin (constant)]
  while [x2: upstream entry]
    in(x2, x1)
  if [x4: context request, x5: context request]
    for(x4, x5)
    request(e1, context requests.raise, subject: x3, object: x4)
    param(e1, origin, some)
  response
    refuse(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x8)
```

## r40
From: requests#r103, reworded in request words (0.38.0).

```reading
While an entry on a context request conforms to the entry form and the side of the entry is `upstream` and the entry holds a field whose side is `asker` and the context request does not hold the entry, when a session catches up, the context requests service shall keep the entry and not keep the field.
shall [x3: artifact the entry form (constant), x6: service the context requests service (constant)]
  while [x1: entry, x2: context request, x4: field]
    on(x1, x2)
    conforms(x1, x3)
    side(x1) = `upstream`
    side(x4) = `asker`
    in(x4, x1)
    not
      in(x1, x2)
  when [x5: session]
    request(e1, context requests.catch up, subject: x5)
  response
    keep(e2, subject: x6, object: x1)
    not
      keep(e3, subject: x6, object: x4)
```

## r41
From: requests#r104, reworded in request words (0.38.0).

```reading
While a request line in a context request has a line reason, when the person inspects the context request, the context requests service shall return the line reason.
shall [x4: agent the person (constant), x5: service the context requests service (constant)]
  while [x1: request line, x2: context request, x3: line reason]
    in(x1, x2)
    of(x3, x1)
  when
    request(e1, context requests.inspect, subject: x4, object: x2)
  response
    return(e2, subject: x5, object: x3)
```

## r42
From: requests#r107, reworded in request words (0.38.0).

```reading
When the person offers on a context request, the context requests service shall return the context request and the status of the context request.
shall [x1: agent the person (constant), x3: service the context requests service (constant)]
  when [x2: context request]
    request(e1, context requests.offer, subject: x1, on: x2)
  response [x4: status]
    return(e2, subject: x3, object: x2)
    status(x2) = x4
    return(e3, subject: x3, object: x4)
```

## r43
From: requests#r108, reworded in request words (0.38.0).

```reading
When the person proposes to a context request, the context requests service shall return the context request and the status of the context request.
shall [x1: agent the person (constant), x3: service the context requests service (constant)]
  when [x2: context request]
    request(e1, context requests.propose, subject: x1, to: x2)
  response [x4: status]
    return(e2, subject: x3, object: x2)
    status(x2) = x4
    return(e3, subject: x3, object: x4)
```

## r44
From: requests#r109, reworded in request words (0.38.0).

```reading
When the person replies to a context request, the context requests service shall return the context request and the status of the context request.
shall [x1: agent the person (constant), x3: service the context requests service (constant)]
  when [x2: context request]
    request(e1, context requests.reply, subject: x1, to: x2)
  response [x4: status]
    return(e2, subject: x3, object: x2)
    status(x2) = x4
    return(e3, subject: x3, object: x4)
```

## r45
From: requests#r110, reworded in request words (0.38.0).

```reading
When the person passes the turn of a context request, the context requests service shall return the context request and the status of the context request.
shall [x1: agent the person (constant), x4: service the context requests service (constant)]
  when [x2: context request, x3: turn]
    of(x3, x2)
    request(e1, context requests.pass turn, subject: x1, object: x3)
  response [x5: status]
    return(e2, subject: x4, object: x2)
    status(x2) = x5
    return(e3, subject: x4, object: x5)
```

## r46
From: requests#r111, reworded in request words (0.38.0).

```reading
When the person raises a context request without a text, the context requests service shall keep a context request that originates from this bounded context.
shall [x1: agent the person (constant), x3: service the context requests service (constant), x5: bounded context "the bounded context whose repository the command runs in" (indexical)]
  when [x2: context request]
    request(e1, context requests.raise, subject: x1, object: x2)
    noparam(e1, text)
  response [x4: context request]
    originate(subject: x4, from: x5)
    keep(e2, subject: x3, object: x4)
```

## r47
From: requests#r112, reworded in request words (0.38.0).

```reading
When a session offers on a context request with a capability, the context requests service shall keep an entry that holds every requirement of the capability.
shall [x4: service the context requests service (constant)]
  when [x1: session, x2: context request, x3: capability]
    request(e1, context requests.offer, subject: x1, on: x2)
    param(e1, capability, x3)
  response [x5: entry]
    every [x6: requirement]
      of(x6, x3)
      scope
        in(x6, x5)
    keep(e2, subject: x4, object: x5)
```

## r48
From: requests#r113, reworded in request words (0.38.0).

```reading
While a requirement of a capability mentions a term, when a session offers on a context request with the capability, the context requests service shall keep an entry that holds the term.
shall [x6: service the context requests service (constant)]
  while [x1: requirement, x2: capability, x3: term]
    of(x1, x2)
    mention(subject: x1, object: x3)
  when [x4: session, x5: context request]
    request(e1, context requests.offer, subject: x4, on: x5)
    param(e1, capability, x2)
  response [x7: entry]
    in(x3, x7)
    keep(e2, subject: x6, object: x7)
```

## r49
From: requests#r114, reworded in request words (0.38.0).

```reading
While a capability holds a given block, when a session offers on a context request with the capability, the context requests service shall keep an entry that does not hold the given block.
shall [x5: service the context requests service (constant)]
  while [x1: capability, x2: given block]
    in(x2, x1)
  when [x3: session, x4: context request]
    request(e1, context requests.offer, subject: x3, on: x4)
    param(e1, capability, x1)
  response [x6: entry]
    not
      in(x2, x6)
    keep(e2, subject: x5, object: x6)
```

## r50
From: requests#r115, reworded in request words (0.38.0).

```reading
While a term is in the bounded context and a capability has no requirement that mentions the term, when a session offers on a context request with the capability, the context requests service shall keep an entry that does not hold the term.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x7: service the context requests service (constant)]
  while [x1: term, x3: capability]
    in(x1, x2)
    not [x4: requirement]
      mention(subject: x4, object: x1)
      of(x4, x3)
  when [x5: session, x6: context request]
    request(e1, context requests.offer, subject: x5, on: x6)
    param(e1, capability, x3)
  response [x8: entry]
    not
      in(x1, x8)
    keep(e2, subject: x7, object: x8)
```
