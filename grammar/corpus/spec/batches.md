# batches: every live line with its intended reading (b240)

## r9
Kept. Audit: fine (merge's gloss trimmed to its frame).

```reading
While an item in a batch is `in-batch`, when the person merges the pull request of the batch, `work` shall set the status of the item to `delivered` and set the status of the batch to `merged`.
shall [x3: agent the person (constant), x5: tool `work` (constant)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `in-batch`
  when [x4: pull request]
    of(x4, x2)
    merge(e1, subject: x3, object: x4)
  response
    initiates(e2, subject: x5, status(x1) = `delivered`)
    initiates(e3, subject: x5, status(x2) = `merged`)
```

## r11
Kept. Audit: fine.

```reading
While an item in a batch is `in-batch`, when the person runs `work batch review` on the batch, `work` shall publish a pull request that cites the item.
shall [x3: agent the person (constant), x4: command `work batch review` (parameter), x5: tool `work` (constant)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `in-batch`
  when
    run(e1, subject: x3, object: x4, on: x2)
  response [x6: pull request]
    cite(subject: x6, object: x1)
    publish(e2, subject: x5, object: x6)
```

## r14
Kept. Audit: fine.

```reading
When the person runs `work batch start`, `work` shall write a batch brief and print the batch brief.
shall [x1: agent the person (constant), x2: command `work batch start` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response [x4: batch brief]
    write(e2, subject: x3, object: x4)
    print(e3, subject: x3, object: x4)
```

## r15
Kept. Audit: fine.

```reading
When the person runs `work batch abandon` on a batch, `work` shall remove every review folder of the batch.
shall [x1: agent the person (constant), x2: command `work batch abandon` (parameter), x4: tool `work` (constant)]
  when [x3: batch]
    run(e1, subject: x1, object: x2, on: x3)
  response
    every [x5: review folder]
      of(x5, x3)
      scope
        remove(e2, subject: x4, object: x5)
```

## r22
Retires: r1. From: b158 r20. Audit: distortion, fixed by section 5 (the `in-batch` Then said, pick's gloss trimmed). Known limit: #14 (up to `batch_size` in rank order, a dependency picked earlier in the same pick).

```reading
While an item is `ready` and the item passes the readiness bar and the item has no dependency on an item whose status is not `delivered`, when the person runs `work batch start`, `work` shall pick the item, set the status of the item to `in-batch`, write a batch whose status is `building` and write a batch plan of the batch.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x5: agent the person (constant), x6: command `work batch start` (parameter), x7: tool `work` (constant)]
  while [x1: item]
    status(x1) = `ready`
    pass#2(subject: x1, object: x2)
    not [x3: dependency, x4: item]
      not
        status(x4) = `delivered`
      on(x3, x4)
      of(x3, x1)
  when
    run(e1, subject: x5, object: x6)
  response [x8: batch, x9: batch plan]
    pick(e2, subject: x7, object: x1)
    initiates(e3, subject: x7, status(x1) = `in-batch`)
    status(x8) = `building`
    write(e4, subject: x7, object: x8)
    of(x9, x8)
    write(e5, subject: x7, object: x9)
```

## r23
Retires: r2. From: b158 r21. Audit: fine.

```reading
While an item is `ready` and the item does not pass the readiness bar, when the person runs `work batch start`, `work` shall set the status of the item to `shaped`.
shall [x2: readiness bar "the readiness bar of the plugin that runs the command" (indexical), x3: agent the person (constant), x4: command `work batch start` (parameter), x5: tool `work` (constant)]
  while [x1: item]
    status(x1) = `ready`
    not
      pass#2(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4)
  response
    initiates(e2, subject: x5, status(x1) = `shaped`)
```

## r24
Retires: r3. From: b158 r22. Audit: distortion, fixed by identity ("another item", named last) and a value set.

```reading
While an item is not `ready` or `delivered` and a dependency on the item exists and another item whose status is `ready` has the dependency, when the person runs `work batch start`, `work` shall not pick the item.
shall [x4: agent the person (constant), x5: command `work batch start` (parameter), x6: tool `work` (constant)]
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
  when
    run(e1, subject: x4, object: x5)
  response
    not
      pick(e2, subject: x6, object: x3)
```

## r25
Retires: r5. From: b158 r23. Audit: fine.

```reading
While a batch is `building`, when a session runs `work batch resume` on the batch, `work` shall use the batch plan of the batch and ask no question.
shall [x3: command `work batch resume` (parameter), x4: tool `work` (constant)]
  while [x1: batch]
    status(x1) = `building`
  when [x2: session]
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: batch plan]
    of(x5, x1)
    use(e2, subject: x4, object: x5)
    not [x6: question]
      ask(e3, subject: x4, object: x6)
```

## r26
Retires: r6. From: b158 r24. Audit: fine.

```reading
While an item in a batch is `in-batch`, when a session runs `work batch park` on the item, `work` shall set the status of the item to `needs-input`, write a question on the item and not set the status of the batch to `abandoned`.
shall [x4: command `work batch park` (parameter), x5: tool `work` (constant)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `in-batch`
  when [x3: session]
    run(e1, subject: x3, object: x4, on: x1)
  response [x6: question]
    initiates(e2, subject: x5, status(x1) = `needs-input`)
    on(x6, x1)
    write(e3, subject: x5, object: x6)
    not
      initiates(e4, subject: x5, status(x2) = `abandoned`)
```

## r37
Retires: r27. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the status of an item in a batch is `needs-input` and a commit cites the item, when the person runs `work batch review` on the batch, `work` shall publish a pull request of the batch that does not hold the commit.
shall [x4: agent the person (constant), x5: command `work batch review` (parameter), x6: tool `work` (constant)]
  while [x1: item, x2: batch, x3: commit]
    in(x1, x2)
    status(x1) = `needs-input`
    cite(subject: x3, object: x1)
  when
    run(e1, subject: x4, object: x5, on: x2)
  response [x7: pull request]
    of(x7, x2)
    not
      in(x3, x7)
    publish(e2, subject: x6, object: x7)
```

## r28
Retires: r10. From: b158 r26. Audit: fine.

```reading
While a batch is `building`, when the person runs `work batch abandon` on the batch, `work` shall set the status of the batch to `abandoned` and set the status of every item in the batch whose status is `in-batch` to `ready`.
shall [x2: agent the person (constant), x3: command `work batch abandon` (parameter), x4: tool `work` (constant)]
  while [x1: batch]
    status(x1) = `building`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response
    initiates(e2, subject: x4, status(x1) = `abandoned`)
    every [x5: item]
      in(x5, x1)
      status(x5) = `in-batch`
      scope
        initiates(e3, subject: x4, status(x5) = `ready`)
```

## r29
Retires: r12. From: b158 r27. Audit: fine.

```reading
While a task of a batch is not `done`, if the person runs `work batch review` on the batch, then `work` shall refuse the command and name the task.
shall [x3: agent the person (constant), x4: command `work batch review` (parameter), x5: tool `work` (constant)]
  while [x1: task, x2: batch]
    of(x1, x2)
    not
      status(x1) = `done`
  if
    run(e1, subject: x3, object: x4, on: x2)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x1)
```

## r30
Retires: r13. From: b158 r28. Audit: fine.

```reading
While a git branch of a task of a batch has a commit that cites no item, if the person runs `work batch review` on the batch, then `work` shall refuse the command and name the commit.
shall [x6: agent the person (constant), x7: command `work batch review` (parameter), x8: tool `work` (constant)]
  while [x1: git branch, x2: task, x3: batch, x4: commit]
    of(x2, x3)
    of(x1, x2)
    not [x5: item]
      cite(subject: x4, object: x5)
    of(x4, x1)
  if
    run(e1, subject: x6, object: x7, on: x3)
  response
    refuse(e2, subject: x8, object: x7)
    name(e3, subject: x8, object: x4)
```

## r31
Retires: r16. From: b158 r29. Audit: fine.

```reading
When the person merges a pull request of a batch, `work` shall remove every review folder of the batch.
shall [x1: agent the person (constant), x4: tool `work` (constant)]
  when [x2: pull request, x3: batch]
    of(x2, x3)
    merge(e1, subject: x1, object: x2)
  response
    every [x5: review folder]
      of(x5, x3)
      scope
        remove(e2, subject: x4, object: x5)
```

## r32
Retires: r17. From: b158 r30. Audit: distortion, fixed by section 5 (a "from" frame for remove; a requirement of the item).

```reading
While an item in a batch is `in-batch` and the git branch of the batch holds a requirement of the item, when a session runs `work batch park` on the item, `work` shall remove the requirement from the git branch.
shall [x6: command `work batch park` (parameter), x7: tool `work` (constant)]
  while [x1: item, x2: batch, x3: git branch, x4: requirement]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x2)
    of(x4, x1)
    in(x4, x3)
  when [x5: session]
    run(e1, subject: x5, object: x6, on: x1)
  response
    remove(e2, subject: x7, object: x4, from: x3)
```

## r38
Retires: r33. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and the status of an item in the batch is `needs-input` and a scenario of the item fails in the worktree of the task, when a session runs `work batch done` on the task, `work` shall set the status of the task to `done`.
shall [x8: command `work batch done` (parameter), x9: tool `work` (constant)]
  while [x1: item, x2: batch, x3: task, x4: item, x5: scenario, x6: worktree]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    in(x4, x2)
    status(x4) = `needs-input`
    of(x5, x4)
    of(x6, x3)
    fail#2(subject: x5, in: x6)
  when [x7: session]
    run(e1, subject: x7, object: x8, on: x3)
  response
    initiates(e2, subject: x9, status(x3) = `done`)
```

## r34
Retires: r19. From: b158 r32. Audit: distortion, fixed by identity ("another item").

```reading
While an item in a batch is `in-batch` and a task of the item is `running` and another item in the batch is `in-batch` and a scenario of the item passes in the worktree of the task, when a session runs `work batch done` on the task, `work` shall set the status of the task to `done`.
shall [x8: command `work batch done` (parameter), x9: tool `work` (constant)]
  while [x1: item, x2: batch, x3: task, x4: item, x5: scenario, x6: worktree]
    in(x1, x2)
    status(x1) = `in-batch`
    of(x3, x1)
    status(x3) = `running`
    distinct(x4, x1)
    in(x4, x2)
    status(x4) = `in-batch`
    of(x5, x4)
    of(x6, x3)
    pass(subject: x5, in: x6)
  when [x7: session]
    run(e1, subject: x7, object: x8, on: x3)
  response
    initiates(e2, subject: x9, status(x3) = `done`)
```

## r35
Retires: r8. From: b158 r33. Audit: fine.

```reading
While a batch is `building` and every task of the batch is `done`, when the person runs `work batch review` on the batch, `work` shall publish a pull request of the batch and set the status of the batch to `in-review`.
shall [x3: agent the person (constant), x4: command `work batch review` (parameter), x5: tool `work` (constant)]
  while [x1: batch]
    status(x1) = `building`
    every [x2: task]
      of(x2, x1)
      scope
        status(x2) = `done`
  when
    run(e1, subject: x3, object: x4, on: x1)
  response [x6: pull request]
    of(x6, x1)
    publish(e2, subject: x5, object: x6)
    initiates(e3, subject: x5, status(x1) = `in-review`)
```

## r36
Retires: r4. From: b158 r4. Audit: unsayable, fixed by R2's boxes (the item and the task given in the While).

```reading
While a batch holds an item and the batch has a task, when the person runs `work batch status` on the batch, `work` shall print the item, the task and the status of the task.
shall [x4: agent the person (constant), x5: command `work batch status` (parameter), x6: tool `work` (constant)]
  while [x1: batch, x2: item, x3: task]
    in(x2, x1)
    of(x3, x1)
  when
    run(e1, subject: x4, object: x5, on: x1)
  response [x7: status]
    print(e2, subject: x6, object: x2)
    print(e3, subject: x6, object: x3)
    status(x3) = x7
    print(e4, subject: x6, object: x7)
```
