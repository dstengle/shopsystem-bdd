# backlog: every live line with its intended reading (b240)

## r5
Kept. Audit: fine.

```reading
When the person runs `work depend` on an item, `work` shall write a dependency of the item and commit the item.
shall [x1: agent the person (constant), x2: command `work depend` (parameter), x4: tool `work` (constant)]
  when [x3: item]
    run(e1, subject: x1, object: x2, on: x3)
  response [x5: dependency]
    of(x5, x3)
    write(e2, subject: x4, object: x5)
    commit(e3, subject: x4, object: x3)
```

## r15
Kept. Audit: fine.

```reading
When the person runs `work show` on an item, `work` shall print the title of the item.
shall [x1: agent the person (constant), x2: command `work show` (parameter), x4: tool `work` (constant)]
  when [x3: item]
    run(e1, subject: x1, object: x2, on: x3)
  response [x5: title]
    of(x5, x3)
    print(e2, subject: x4, object: x5)
```

## r22
Retires: r1. From: b158 r22. Audit: fine.

```reading
When the person runs `work idea`, `work` shall write an item whose status is `idea` and commit the item.
shall [x1: agent the person (constant), x2: command `work idea` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response [x4: item]
    status(x4) = `idea`
    write(e2, subject: x3, object: x4)
    commit(e3, subject: x3, object: x4)
```

## r37
Retires: r23. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the status of an item is `idea`, when the person runs `work shape` on the item, `work` shall set the status of the item to `shaped`.
shall [x2: agent the person (constant), x3: command `work shape` (parameter), x4: tool `work` (constant)]
  while [x1: item]
    status(x1) = `idea`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response
    initiates(e2, subject: x4, status(x1) = `shaped`)
```

## r38
Retires: r24. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the status of an item is not `idea`, if the person runs `work shape` on the item, then `work` shall refuse the command and name the status of the item.
shall [x2: agent the person (constant), x3: command `work shape` (parameter), x4: tool `work` (constant)]
  while [x1: item]
    not
      status(x1) = `idea`
  if
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: status]
    refuse(e2, subject: x4, object: x3)
    status(x1) = x5
    name(e3, subject: x4, object: x5)
```

## r25
Retires: r4. From: b158 r25. Audit: unsayable (the value an option is set to). Known limit: #12.

```reading
When the person runs `work rate --value high-value --urgency low-urgency --size small` on an item, `work` shall set the value of the item to `high-value`, set the urgency of the item to `low-urgency`, set the size of the item to `small` and commit the item.
shall [x1: agent the person (constant), x2: command `work rate --value high-value --urgency low-urgency --size small` (parameter), x4: tool `work` (constant)]
  when [x3: item]
    run(e1, subject: x1, object: x2, on: x3)
  response
    initiates(e2, subject: x4, value(x3) = `high-value`)
    initiates(e3, subject: x4, urgency(x3) = `low-urgency`)
    initiates(e4, subject: x4, size(x3) = `small`)
    commit(e5, subject: x4, object: x3)
```

## r26
Retires: r7. From: b158 r26. Audit: distortion, fixed by identity ("another item", the item that has the dependency named last, so "the item" binds to it).

```reading
While an item is not `delivered` and a dependency on the item exists and another item has the dependency, when the person runs `work backlog`, `work` shall print the item and the dependency.
shall [x4: agent the person (constant), x5: command `work backlog` (parameter), x6: tool `work` (constant)]
  while [x1: item, x2: dependency, x3: item]
    not
      status(x1) = `delivered`
    on(x2, x1)
    exists(x2)
    distinct(x3, x1)
    of(x2, x3)
  when
    run(e1, subject: x4, object: x5)
  response
    print(e2, subject: x6, object: x3)
    print(e3, subject: x6, object: x2)
```

## r27
Retires: r8. From: b158 r27. Audit: distortion, fixed by section 5 ("one JSON object", with the `--json` option).

```reading
When the person runs `work backlog` with the `--json` option, `work` shall print one JSON object and exit successfully.
shall [x1: agent the person (constant), x2: command `work backlog` (parameter), x3: option `--json` (parameter), x4: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2, with: x3)
  response
    count exactly 1 [x5: JSON object]
      scope
        print(e2, subject: x4, object: x5)
    exit(e3, subject: x4, successfully)
```

## r39
Retires: r28. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the status of an item is one of `idea`, `shaped`, `ready` or `needs-input`, when the person runs `work withdraw` on the item, `work` shall set the status of the item to `withdrawn`.
shall [x2: agent the person (constant), x3: command `work withdraw` (parameter), x4: tool `work` (constant)]
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
    run(e1, subject: x2, object: x3, on: x1)
  response
    initiates(e2, subject: x4, status(x1) = `withdrawn`)
```

## r40
Retires: r29. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the status of an item is one of `idea` or `shaped`, when the person runs `work refuse` on the item, `work` shall set the status of the item to `refused`.
shall [x2: agent the person (constant), x3: command `work refuse` (parameter), x4: tool `work` (constant)]
  while [x1: item]
    or
      case
        status(x1) = `idea`
      case
        status(x1) = `shaped`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response
    initiates(e2, subject: x4, status(x1) = `refused`)
```

## r41
Retires: r30. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the status of an item is `needs-input`, when the person runs `work answer` on the item, `work` shall set the status of the item to `shaped` and commit the item.
shall [x2: agent the person (constant), x3: command `work answer` (parameter), x4: tool `work` (constant)]
  while [x1: item]
    status(x1) = `needs-input`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response
    initiates(e2, subject: x4, status(x1) = `shaped`)
    commit(e3, subject: x4, object: x1)
```

## r42
Retires: r31. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the status of an item is `needs-input`, when the person runs `work backlog`, `work` shall print the item and every question on the item.
shall [x2: agent the person (constant), x3: command `work backlog` (parameter), x4: tool `work` (constant)]
  while [x1: item]
    status(x1) = `needs-input`
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x1)
    every [x5: question]
      on(x5, x1)
      scope
        print(e3, subject: x4, object: x5)
```

## r32
Retires: r18. From: b158 r36. Audit: distortion, fixed by section 5 (the remote of this repository) and the push of the command.

```reading
While the remote of this repository rejects the push of the command, when the person runs `work idea`, `work` shall write an item whose status is `idea`, commit the item, print the remote and exit successfully.
shall [x1: repository "the repository the command runs in" (indexical), x3: command "the command the run runs" (indexical), x5: agent the person (constant), x6: command `work idea` (parameter), x7: tool `work` (constant)]
  while [x2: remote, x4: push]
    of(x2, x1)
    of(x4, x3)
    reject(subject: x2, object: x4)
  when
    run(e1, subject: x5, object: x6)
  response [x8: item]
    status(x8) = `idea`
    write(e2, subject: x7, object: x8)
    commit(e3, subject: x7, object: x8)
    print(e4, subject: x7, object: x2)
    exit(e5, subject: x7, successfully)
```

## r33
Retires: r19. From: b158 r37. Audit: unsayable (no answer within the push timeout). Known limit: #16.

```reading
While the remote of this repository does not answer the push of the command, when the person runs `work idea`, `work` shall write an item whose status is `idea`, commit the item, print the remote and exit successfully.
shall [x1: repository "the repository the command runs in" (indexical), x3: command "the command the run runs" (indexical), x5: agent the person (constant), x6: command `work idea` (parameter), x7: tool `work` (constant)]
  while [x2: remote, x4: push]
    of(x2, x1)
    of(x4, x3)
    not
      answer(subject: x2, object: x4)
  when
    run(e1, subject: x5, object: x6)
  response [x8: item]
    status(x8) = `idea`
    write(e2, subject: x7, object: x8)
    commit(e3, subject: x7, object: x8)
    print(e4, subject: x7, object: x2)
    exit(e5, subject: x7, successfully)
```

## r34
Retires: r20. From: b158 r38. Audit: fine.

```reading
While this repository checks out a git branch of a task, if the person runs `work idea`, then `work` shall refuse the command and name the task.
shall [x1: repository "the repository the command runs in" (indexical), x4: agent the person (constant), x5: command `work idea` (parameter), x6: tool `work` (constant)]
  while [x2: git branch, x3: task]
    of(x2, x3)
    check out(subject: x1, object: x2)
  if
    run(e1, subject: x4, object: x5)
  response
    refuse(e2, subject: x6, object: x5)
    name(e3, subject: x6, object: x3)
```

## r35
Retires: r21. From: b158 r39. Audit: distortion, fixed by identity ("a different branch name").

```reading
While this repository checks out a git branch that has a branch name and the upstream branch of the git branch has a different branch name, when the person runs `work idea`, `work` shall write an item whose status is `idea`, commit the item and keep the upstream branch.
shall [x1: repository "the repository the command runs in" (indexical), x6: agent the person (constant), x7: command `work idea` (parameter), x8: tool `work` (constant)]
  while [x2: git branch, x3: branch name, x4: upstream branch, x5: branch name]
    of(x3, x2)
    check out(subject: x1, object: x2)
    of(x4, x2)
    distinct(x5, x3)
    of(x5, x4)
  when
    run(e1, subject: x6, object: x7)
  response [x9: item]
    status(x9) = `idea`
    write(e2, subject: x8, object: x9)
    commit(e3, subject: x8, object: x9)
    keep(e4, subject: x8, object: x4)
```

## r36
Retires: r6. From: b158 r6. Audit: unsayable, fixed by R2's boxes (the item given in the While, each of its fields said of it).

```reading
While an item exists, when the person runs `work backlog`, `work` shall print the item, the title of the item, the status of the item, the provenance of the item, the value of the item, the urgency of the item and the size of the item.
shall [x2: agent the person (constant), x3: command `work backlog` (parameter), x4: tool `work` (constant)]
  while [x1: item]
    exists(x1)
  when
    run(e1, subject: x2, object: x3)
  response [x5: title, x6: status, x7: provenance, x8: value, x9: urgency, x10: size]
    print(e2, subject: x4, object: x1)
    of(x5, x1)
    print(e3, subject: x4, object: x5)
    status(x1) = x6
    print(e4, subject: x4, object: x6)
    provenance(x1) = x7
    print(e5, subject: x4, object: x7)
    value(x1) = x8
    print(e6, subject: x4, object: x8)
    urgency(x1) = x9
    print(e7, subject: x4, object: x9)
    size(x1) = x10
    print(e8, subject: x4, object: x10)
```
