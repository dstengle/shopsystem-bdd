# universal: every live condition with its intended reading (b240)

## U17
Retires: U12. Reworded in request words (0.38.0).

```reading
If a service refuses a request, then the service shall name a reason and change nothing.
shall []
  if [x1: service, x2: request]
    refuse(e1, subject: x1, object: x2)
  response [x3: reason]
    name(e2, subject: x1, object: x3)
    not [x4: thing]
      change(e3, subject: x1, object: x4)
```

## U18
Retires: U14. Reworded in request words (0.38.0).

```reading
A session shall not change an item.
shall []
  response [x1: session]
    not [x2: item]
      change(e1, subject: x1, object: x2)
```

## U19
Retires: U15. Reworded in request words (0.38.0).

```reading
While a session has a workspace, the session shall change only files in the workspace.
shall []
  while [x1: session, x2: workspace]
    of(x2, x1)
  response
    only [x3: file]
      in(x3, x2)
      scope
        change(e1, subject: x1, object: x3)
```

