# universal: every live condition with its intended reading (b240)

## U12
Retires: U11. From: b155 U12, with "change nothing" for its "change no file" (change's frame now takes a thing, as the CLI pack's does). Audit: distortion; "nothing" fixed by the frame, the reason tied to the refusal is not. Known limit: #15.

```reading
If a tool refuses a command, then the tool shall exit with an error naming a reason and change nothing.
shall []
  if [x1: tool, x2: command]
    refuse(e1, subject: x1, object: x2)
  response [x3: reason]
    exit(e2, subject: x1, with an error naming: x3)
    not [x4: thing]
      change(e3, subject: x1, object: x4)
```

## U13
Retires: U4. From: b155 U13, with the row `commit | of | transition` added to spec/index.md's Relations (the plan's `commit | of | text` would give commit of batch and commit of item a second row, v_t10). Audit: coined (transition stands for the change of a status). Known limit: #8.

```reading
When `work` writes a transition, `work` shall commit the transition and push the commit of the transition.
shall [x1: tool `work` (constant)]
  when [x2: transition]
    write(e1, subject: x1, object: x2)
  response [x3: commit]
    commit(e2, subject: x1, object: x2)
    of(x3, x2)
    push(e3, subject: x1, object: x3)
```

## U14
Retires: U5. From: b155 U14. Audit: coined (transition stands for the change of a status; "change the status of" has no form). Known limit: #8.

```reading
A session shall not write a transition.
shall []
  response [x1: session]
    not [x2: transition]
      write(e1, subject: x1, object: x2)
```

## U15
Retires: U7. From: b155 U15, narrowed to a dispatch that has a worktree. Audit: distortion, fixed by section 5 (worktree glossed for a task of a batch, the row `worktree | of | session | one`, the line narrowed to the dispatch of a task).

```reading
While a dispatch has a worktree, the dispatch shall change only files in the worktree.
shall []
  while [x1: dispatch, x2: worktree]
    of(x2, x1)
  response
    only [x3: file]
      in(x3, x2)
      scope
        change(e1, subject: x1, object: x3)
```

## U16
Retires: U8. From: b155 U16. Audit: fine, with the row `command | of | tool | one` (the option in the trigger).

```reading
When an agent runs a command of a tool with the `--json` option, the tool shall print one JSON object.
shall [x4: option `--json` (parameter)]
  when [x1: agent, x2: command, x3: tool]
    of(x2, x3)
    run(e1, subject: x1, object: x2, with: x4)
  response
    count exactly 1 [x5: JSON object]
      scope
        print(e2, subject: x3, object: x5)
```
