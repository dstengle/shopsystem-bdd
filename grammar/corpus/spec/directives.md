# directives: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: conversation#r16, reworded in request words (0.38.0).

```reading
When a session gives a directive, the conversation service shall keep a directive whose quote cites a message.
shall [x3: service the conversation service (constant)]
  when [x1: session, x2: directive]
    request(e1, conversation.give, subject: x1, object: x2)
  response [x4: directive, x5: quote, x6: message]
    of(x5, x4)
    cite(subject: x5, object: x6)
    keep(e2, subject: x3, object: x4)
```

## r2
From: conversation#r10, reworded in request words (0.38.0).

```reading
When a session starts, the conversation service shall notify the session of the quote of every directive whose status is `live`.
shall [x2: service the conversation service (constant)]
  when [x1: session]
    start(e1, subject: x1)
  response
    every [x3: directive]
      status(x3) = `live`
      scope [x4: quote]
        of(x4, x3)
        notify(e2, subject: x2, object: x1, of: x4)
```

## r3
From: conversation#r11, reworded in request words (0.38.0).

```reading
When a session promotes a directive whose status is `live` to an item, the conversation service shall set the status of the directive to `promoted` and keep the directive.
shall [x4: service the conversation service (constant)]
  when [x1: session, x2: directive, x3: item]
    status(x2) = `live`
    request(e1, conversation.promote, subject: x1, object: x2, to: x3)
  response
    initiates(e2, subject: x4, status(x2) = `promoted`)
    keep(e3, subject: x4, object: x2)
```

## r4
From: conversation#r14, reworded in request words (0.38.0).

```reading
When a session drops a directive whose status is `live` with a reason, the conversation service shall set the status of the directive to `dropped` and keep the directive.
shall [x3: service the conversation service (constant)]
  when [x1: session, x2: directive]
    status(x2) = `live`
    request(e1, conversation.drop, subject: x1, object: x2)
    param(e1, reason, some)
  response
    initiates(e2, subject: x3, status(x2) = `dropped`)
    keep(e3, subject: x3, object: x2)
```

## r5
From: conversation#r12, reworded in request words (0.38.0).

```reading
When a session promotes a directive whose status is not `live` to an item, the conversation service shall refuse the request and name the directive.
shall [x4: service the conversation service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x1: session, x2: directive, x3: item]
    not
      status(x2) = `live`
    request(e1, conversation.promote, subject: x1, object: x2, to: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

## r6
From: conversation#r13, reworded in request words (0.38.0).

```reading
When a session promotes a directive to an item that does not exist, the conversation service shall refuse the request and name the item.
shall [x4: service the conversation service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x1: session, x2: directive, x3: item]
    not
      exists(x3)
    request(e1, conversation.promote, subject: x1, object: x2, to: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x3)
```

## r7
From: conversation#r15, reworded in request words (0.38.0).

```reading
When a session drops a directive whose status is not `live` with a reason, the conversation service shall refuse the request and name the directive.
shall [x3: service the conversation service (constant), x4: request "the request the trigger makes" (indexical)]
  when [x1: session, x2: directive]
    not
      status(x2) = `live`
    request(e1, conversation.drop, subject: x1, object: x2)
    param(e1, reason, some)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x2)
```
