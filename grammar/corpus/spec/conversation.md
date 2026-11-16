# conversation: every live line with its intended reading (b240)

## r1
Kept.

```reading
When a session runs `work quote`, `work` shall write a quote from the session that cites a message and commit the quote.
shall [x2: command `work quote` (parameter), x3: tool `work` (constant)]
  when [x1: session]
    run(e1, subject: x1, object: x2)
  response [x4: quote, x5: message]
    from(x4, x1)
    cite#2(subject: x4, object: x5)
    write(e2, subject: x3, object: x4)
    commit(e3, subject: x3, object: x4)
```

## r6
Retires: r2. From: b159 r6. Audit: distortion, fixed by section 5 (the git directory and the transcript named: "a file in the git directory that lists the transcript of the session"; the prompt hook's gloss holds no rule).

```reading
When the prompt hook runs `work quote` with the `--hook` option, `work` shall write a file in the git directory that lists the transcript of the session.
shall [x1: agent the prompt hook (constant), x2: command `work quote` (parameter), x3: option `--hook` (parameter), x4: tool `work` (constant), x6: git directory "the git directory of the repository the command runs in" (indexical), x7: session "the session that runs the command" (indexical)]
  when
    run(e1, subject: x1, object: x2, with: x3)
  response [x5: file, x8: transcript]
    in(x5, x6)
    of(x8, x7)
    list(subject: x5, object: x8)
    write(e2, subject: x4, object: x5)
```

## r7
Retires: r3. From: b159 r7. Audit: fine.

```reading
When the person runs `work show` on a quote, `work` shall print every message that the quote cites.
shall [x1: agent the person (constant), x2: command `work show` (parameter), x4: tool `work` (constant)]
  when [x3: quote]
    run(e1, subject: x1, object: x2, on: x3)
  response
    every [x5: message]
      cite#2(subject: x3, object: x5)
      scope
        print(e2, subject: x4, object: x5)
```

## r8
Retires: r4. From: b159 r8. Known limit: #10 (for each item its title: the item and its title are printed, but not paired).

```reading
When the SessionStart hook runs `work names`, `work` shall print every item, every title of an item and every batch.
shall [x1: agent the SessionStart hook (constant), x2: command `work names` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    every [x4: item]
      scope
        print(e2, subject: x3, object: x4)
    every [x5: title, x6: item]
      of(x5, x6)
      scope
        print(e3, subject: x3, object: x5)
    every [x7: batch]
      scope
        print(e4, subject: x3, object: x7)
```

## r9
From: b52 r9. Not in the audit (b52 is no reword item).

```reading
When a session runs `work quote` on a queued message, `work` shall write a quote that cites the queued message and commit the quote.
shall [x2: command `work quote` (parameter), x4: tool `work` (constant)]
  when [x1: session, x3: queued message]
    run(e1, subject: x1, object: x2, on: x3)
  response [x5: quote]
    cite#2(subject: x5, object: x3)
    write(e2, subject: x4, object: x5)
    commit(e3, subject: x4, object: x5)
```

## r10
From: b20 r10. Not in the audit (b20 is no reword item).

```reading
When the SessionStart hook runs `work directives` with the `--hook` option, `work` shall print the quote of every directive whose status is `live`.
shall [x1: agent the SessionStart hook (constant), x2: command `work directives` (parameter), x3: option `--hook` (parameter), x4: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2, with: x3)
  response
    every [x5: directive]
      status(x5) = `live`
      scope [x6: quote]
        of(x6, x5)
        print(e2, subject: x4, object: x6)
```

## r11
From: b20 r11. Not in the audit (b20 is no reword item).

```reading
When a session runs `work promote` with the `--to` option set to an item on a directive whose status is `live`, `work` shall set the status of the directive to `promoted` and commit the directive.
shall [x2: command `work promote` (parameter), x3: option `--to` (parameter), x6: tool `work` (constant)]
  when [x1: session, x4: item, x5: directive]
    argument(x3, x4)
    status(x5) = `live`
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response
    initiates(e2, subject: x6, status(x5) = `promoted`)
    commit(e3, subject: x6, object: x5)
```

## r12
From: b20 r12. Not in the audit (b20 is no reword item).

```reading
When a session runs `work promote` with the `--to` option on a directive whose status is not `live`, `work` shall refuse the command and name the directive.
shall [x2: command `work promote` (parameter), x3: option `--to` (parameter), x5: tool `work` (constant)]
  when [x1: session, x4: directive]
    not
      status(x4) = `live`
    run(e1, subject: x1, object: x2, with: x3, on: x4)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x4)
```

## r13
From: b20 r13. Not in the audit (b20 is no reword item).

```reading
When a session runs `work promote` with the `--to` option set to an item that does not exist on a directive, `work` shall refuse the command and name the item.
shall [x2: command `work promote` (parameter), x3: option `--to` (parameter), x6: tool `work` (constant)]
  when [x1: session, x4: item, x5: directive]
    not
      exists(x4)
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3, on: x5)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r14
From: b20 r14. Not in the audit (b20 is no reword item).

```reading
When a session runs `work drop` with the `--why` option on a directive whose status is `live`, `work` shall set the status of the directive to `dropped` and commit the directive.
shall [x2: command `work drop` (parameter), x3: option `--why` (parameter), x5: tool `work` (constant)]
  when [x1: session, x4: directive]
    status(x4) = `live`
    run(e1, subject: x1, object: x2, with: x3, on: x4)
  response
    initiates(e2, subject: x5, status(x4) = `dropped`)
    commit(e3, subject: x5, object: x4)
```

## r15
From: b20 r15. Not in the audit (b20 is no reword item).

```reading
When a session runs `work drop` with the `--why` option on a directive whose status is not `live`, `work` shall refuse the command and name the directive.
shall [x2: command `work drop` (parameter), x3: option `--why` (parameter), x5: tool `work` (constant)]
  when [x1: session, x4: directive]
    not
      status(x4) = `live`
    run(e1, subject: x1, object: x2, with: x3, on: x4)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x4)
```

## r16
From: b20 r9. Not in the audit (b20 is no reword item).

```reading
When a session runs `work directive`, `work` shall write a directive whose quote cites a message and commit the directive.
shall [x2: command `work directive` (parameter), x3: tool `work` (constant)]
  when [x1: session]
    run(e1, subject: x1, object: x2)
  response [x4: directive, x5: quote, x6: message]
    of(x5, x4)
    cite#2(subject: x5, object: x6)
    write(e2, subject: x3, object: x4)
    commit(e3, subject: x3, object: x4)
```
