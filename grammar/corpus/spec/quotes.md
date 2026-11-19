# quotes: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: conversation#r1, reworded in request words (0.38.0).

```reading
When a session quotes a message, the conversation service shall keep a quote from the session that cites the message.
shall [x3: service the conversation service (constant)]
  when [x1: session, x2: message]
    request(e1, conversation.quote, subject: x1, object: x2)
  response [x4: quote]
    from(x4, x1)
    cite(subject: x4, object: x2)
    keep(e2, subject: x3, object: x4)
```

## r2
From: conversation#r6, reworded in request words (0.38.0).

```reading
When the person prompts a session, the conversation service shall keep the transcript of the session.
shall [x1: agent the person (constant), x3: service the conversation service (constant)]
  when [x2: session]
    request(e1, conversation.prompt, subject: x1, object: x2)
  response [x4: transcript]
    of(x4, x2)
    keep(e2, subject: x3, object: x4)
```

## r3
From: conversation#r7, reworded in request words (0.38.0).

```reading
When the person reads a quote, the conversation service shall return every message that the quote cites.
shall [x1: agent the person (constant), x3: service the conversation service (constant)]
  when [x2: quote]
    request(e1, conversation.read, subject: x1, object: x2)
  response
    every [x4: message]
      cite(subject: x2, object: x4)
      scope
        return(e2, subject: x3, object: x4)
```

## r4
From: conversation#r9, reworded in request words (0.38.0).

```reading
When a session quotes a queued message, the conversation service shall keep a quote that cites the queued message and return the quote.
shall [x3: service the conversation service (constant)]
  when [x1: session, x2: queued message]
    request(e1, conversation.quote, subject: x1, object: x2)
  response [x4: quote]
    cite(subject: x4, object: x2)
    keep(e2, subject: x3, object: x4)
    return(e3, subject: x3, object: x4)
```
