# brainstorming: every live line with its intended reading (b240)

## r2
Kept.

```reading
When the brainstorming session runs `work ready` on an item, the brainstorming session shall not ask a question.
shall [x1: session the brainstorming session (constant), x2: command `work ready` (parameter)]
  when [x3: item]
    run(e1, subject: x1, object: x2, on: x3)
  response
    not [x4: question]
      ask(e2, subject: x1, object: x4)
```

## r4
Retires: r1. From: b159 r4. Audit: fine.

```reading
When the brainstorming session shapes an item, the brainstorming session shall write a requirement that the item proposes and run `work ready` on the item.
shall [x1: session the brainstorming session (constant), x4: command `work ready` (parameter)]
  when [x2: item]
    shape(e1, subject: x1, object: x2)
  response [x3: requirement]
    propose(subject: x2, object: x3)
    write(e2, subject: x1, object: x3)
    run(e3, subject: x1, object: x4, on: x2)
```

## r5
Retires: r3. From: b159 r5. Audit: distortion, fixed by section 5 (a frame for what is quoted: "quotes a message of the person", run `work quote` on the message).

```reading
When the brainstorming session quotes a message of the person, the brainstorming session shall run `work quote` on the message.
shall [x1: session the brainstorming session (constant), x3: agent the person (constant), x4: command `work quote` (parameter)]
  when [x2: message]
    of(x2, x3)
    quote(e1, subject: x1, object: x2)
  response
    run(e2, subject: x1, object: x4, on: x2)
```
