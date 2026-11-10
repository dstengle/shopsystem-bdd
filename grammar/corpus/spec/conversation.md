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
