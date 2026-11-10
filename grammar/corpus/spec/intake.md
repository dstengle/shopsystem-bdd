# intake: every live line with its intended reading (b240)

## r10
Retires: r6. From: b159 r10. Audit: distortion (three "is not" clauses), fixed by "is not `accepted`, `refused` or `withdrawn`" (value sets).

```reading
While an item is `shaped` and a request line of the item is not `accepted`, `refused` or `withdrawn`, if a session runs `work ready` on the item, then `work` shall refuse the command and name the request line.
shall [x4: command `work ready` (parameter), x5: tool `work` (constant)]
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
    run(e1, subject: x3, object: x4, on: x1)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x2)
```

## r11
Retires: r7. From: b159 r11. Audit: distortion, fixed by section 5 (the verb counter: "a request line of the request that counters the request line"; "a request line of a request" for the participle row "proposed in"; the comment "on the request").

```reading
When a session runs `work outcome rewritten` on a request line of a request, `work` shall set the line outcome of the request line to `rewritten`, write a request line of the request that counters the request line, set the side of the request to `asker` and post a comment on the request.
shall [x2: command `work outcome rewritten` (parameter), x5: tool `work` (constant)]
  when [x1: session, x3: request line, x4: request]
    of(x3, x4)
    run(e1, subject: x1, object: x2, on: x3)
  response [x6: request line, x7: comment]
    initiates(e2, subject: x5, line outcome(x3) = `rewritten`)
    of(x6, x4)
    counter(subject: x6, object: x3)
    write(e3, subject: x5, object: x6)
    initiates(e4, subject: x5, side(x4) = `asker`)
    on(x7, x4)
    post(e5, subject: x5, object: x7)
```

## r12
Retires: r8. From: b159 r12. Audit: distortion, fixed by section 5 (the reason of the line: "a reason for the request line", the row reason for request line).

```reading
When a session runs `work outcome refused` on a request line of a request, `work` shall set the line outcome of the request line to `refused`, write a reason for the request line and commit the request.
shall [x2: command `work outcome refused` (parameter), x5: tool `work` (constant)]
  when [x1: session, x3: request line, x4: request]
    of(x3, x4)
    run(e1, subject: x1, object: x2, on: x3)
  response [x6: reason]
    initiates(e2, subject: x5, line outcome(x3) = `refused`)
    for(x6, x3)
    write(e3, subject: x5, object: x6)
    commit(e4, subject: x5, object: x4)
```

## r13
Retires: r9. From: b159 r13. Audit: distortion (an argument "that `work outcome refused` does not have"), fixed by the option in the trigger ("without the `--reason` option").

```reading
If a session runs `work outcome refused` without the `--reason` option on a request line, then `work` shall refuse the command and name `--reason`.
shall [x2: command `work outcome refused` (parameter), x3: option `--reason` (parameter), x5: tool `work` (constant)]
  if [x1: session, x4: request line]
    run(e1, subject: x1, object: x2, without: x3, on: x4)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x3)
```
