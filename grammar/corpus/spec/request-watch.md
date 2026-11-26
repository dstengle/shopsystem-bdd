# request-watch: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: requests#r86, reworded in request words (0.38.0).

```reading
While an entry on a context request conforms to the entry form and the context request does not hold the entry, when a session watches this bounded context, the context requests service shall notify the session of the entry, complete the request and not keep the entry.
shall [x3: artifact the entry form (constant), x5: bounded context "the bounded context the request is made in" (indexical), x6: service the context requests service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: entry, x2: context request]
    on(x1, x2)
    conforms(x1, x3)
    not
      in(x1, x2)
  when [x4: session]
    request(e1, context requests.watch, subject: x4, object: x5)
  response
    notify(e2, subject: x6, object: x4, of: x1)
    complete(e3, subject: x6, object: x7)
    not
      keep(e4, subject: x6, object: x1)
```

## r2
From: requests#r87, reworded in request words (0.38.0).

```reading
While a thread on the channel of this bounded context is `open` and the thread conforms to the entry form and no context request has the thread, when a session watches this bounded context, the context requests service shall notify the session of the thread and complete the request.
shall [x2: bounded context "the bounded context the request is made in" (indexical), x4: artifact the entry form (constant), x7: service the context requests service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: thread, x3: channel]
    of(x3, x2)
    on(x1, x3)
    status(x1) = `open`
    conforms(x1, x4)
    not [x5: context request]
      of(x1, x5)
  when [x6: session]
    request(e1, context requests.watch, subject: x6, object: x2)
  response
    notify(e2, subject: x7, object: x6, of: x1)
    complete(e3, subject: x7, object: x8)
```

## r3
From: requests#r97, reworded in request words (0.38.0).

```reading
While a context request originates from this bounded context and the context request does not address this bounded context and the context request is `awaiting-upstream`, when a session starts, the context requests service shall notify the session of the context request.
shall [x2: bounded context "the bounded context the request is made in" (indexical), x4: service the context requests service (constant)]
  while [x1: context request]
    originate(subject: x1, from: x2)
    not
      address#2(subject: x1, object: x2)
    status(x1) = `awaiting-upstream`
  when [x3: session]
    start(e1, subject: x3)
  response
    notify(e2, subject: x4, object: x3, of: x1)
```

## r4
From: requests#r98, reworded in request words (0.38.0).

```reading
While a context request addresses this bounded context and the context request does not originate from this bounded context and the context request is `awaiting-asker`, when a session starts, the context requests service shall notify the session of the context request.
shall [x2: bounded context "the bounded context the request is made in" (indexical), x4: service the context requests service (constant)]
  while [x1: context request]
    address#2(subject: x1, object: x2)
    not
      originate(subject: x1, from: x2)
    status(x1) = `awaiting-asker`
  when [x3: session]
    start(e1, subject: x3)
  response
    notify(e2, subject: x4, object: x3, of: x1)
```

## r5
From: requests#r99, reworded in request words (0.38.0).

```reading
While no context request that originates from this bounded context is `awaiting-upstream` and no context request that addresses this bounded context is `awaiting-asker`, when a session starts, the context requests service shall not notify the session of a context request.
shall [x2: bounded context "the bounded context the request is made in" (indexical), x5: service the context requests service (constant)]
  while
    not [x1: context request]
      originate(subject: x1, from: x2)
      status(x1) = `awaiting-upstream`
    not [x3: context request]
      address#2(subject: x3, object: x2)
      status(x3) = `awaiting-asker`
  when [x4: session]
    start(e1, subject: x4)
  response
    not [x6: context request]
      notify(e2, subject: x5, object: x4, of: x6)
```

## r6
From: requests#r105, reworded in request words (0.38.0).

```reading
While an entry on a context request does not conform to the entry form and the context request does not hold the entry, when a session catches up, the context requests service shall notify the session of the entry, keep the entry and keep the status of the context request.
shall [x3: artifact the entry form (constant), x5: service the context requests service (constant)]
  while [x1: entry, x2: context request]
    on(x1, x2)
    not
      conforms(x1, x3)
    not
      in(x1, x2)
  when [x4: session]
    request(e1, context requests.catch up, subject: x4)
  response [x6: status]
    notify(e2, subject: x5, object: x4, of: x1)
    keep(e3, subject: x5, object: x1)
    status(x2) = x6
    keep(e4, subject: x5, object: x6)
```

## r7
From: requests#r106, reworded in request words (0.38.0).

```reading
While an entry on a context request does not conform to the entry form and the context request holds the entry, when a session catches up, the context requests service shall not notify the session of the entry.
shall [x3: artifact the entry form (constant), x5: service the context requests service (constant)]
  while [x1: entry, x2: context request]
    on(x1, x2)
    not
      conforms(x1, x3)
    in(x1, x2)
  when [x4: session]
    request(e1, context requests.catch up, subject: x4)
  response
    not
      notify(e2, subject: x5, object: x4, of: x1)
```
