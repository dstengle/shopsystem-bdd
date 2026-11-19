# shaping-guarantees: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: brainstorming#r2, reworded in request words (0.38.0).

```reading
When the brainstorming session readies an item, the brainstorming session shall not ask a question.
shall [x1: session the brainstorming session (constant)]
  when [x2: item]
    request(e1, backlog.ready, subject: x1, object: x2)
  response
    not [x3: question]
      ask(e2, subject: x1, object: x3)
```

## r2
From: brainstorming#r4, reworded in request words (0.38.0).

```reading
When the brainstorming session shapes an item, the brainstorming session shall draft the item and ready the item.
shall [x1: session the brainstorming session (constant)]
  when [x2: item]
    request(e1, backlog.shape, subject: x1, object: x2)
  response
    draft(e2, subject: x1, object: x2)
    ready(e3, subject: x1, object: x2)
```

## r3
From: brainstorming#r5, reworded in request words (0.38.0).

```reading
When the person prompts the brainstorming session, the brainstorming session shall quote a message.
shall [x1: agent the person (constant), x2: session the brainstorming session (constant)]
  when
    request(e1, conversation.prompt, subject: x1, object: x2)
  response [x3: message]
    quote(e2, subject: x2, object: x3)
```
