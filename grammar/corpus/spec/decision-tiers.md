# decision-tiers: every live line with its intended reading (b240)

## r13
Retires: r1. From: b159 r13. Audit: distortion ("untiered" said by values, which also held of a tier outside the three), fixed by "has no tier" and "is not `superseded` or `rejected`" (value sets and a value's absence).

```reading
While a design-decision is not `superseded` or `rejected` and the design-decision has no tier, when the person runs `model check`, `model` shall print `w_untiered`.
shall [x2: agent the person (constant), x3: command `model check` (parameter), x4: tool `model` (constant), x5: thing `w_untiered` (parameter)]
  while [x1: design-decision]
    not
      status(x1) = `superseded`
    not
      status(x1) = `rejected`
    tier(x1) = none
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x5)
```

## r26
Retires: r14. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the tier of a design-decision is `check` and no test enforces the design-decision, if the person runs `model check`, then `model` shall exit with an error naming `v_d6`.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant), x6: thing `v_d6` (parameter)]
  while [x1: design-decision]
    tier(x1) = `check`
    not [x2: test]
      enforce(subject: x2, object: x1)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x6)
```

## r27
Retires: r15. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the tier of a design-decision is `requirement` and no requirement enforces the design-decision, if the person runs `model check`, then `model` shall exit with an error naming `v_d7`.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant), x6: thing `v_d7` (parameter)]
  while [x1: design-decision]
    tier(x1) = `requirement`
    not [x2: requirement]
      enforce(subject: x2, object: x1)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x6)
```

## r28
Retires: r16. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the tier of a design-decision is `check` and a test enforces the design-decision, when the person runs `model decisions --check`, `model` shall run `pytest` on the test.
shall [x3: agent the person (constant), x4: command `model decisions --check` (parameter), x5: tool `model` (constant), x6: command `pytest` (parameter)]
  while [x1: design-decision, x2: test]
    tier(x1) = `check`
    enforce(subject: x2, object: x1)
  when
    run(e1, subject: x3, object: x4)
  response
    run(e2, subject: x5, object: x6, on: x2)
```

## r29
Retires: r17. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the tier of a design-decision is `check` and a test whose outcome is `failed` enforces the design-decision, if the person runs `model decisions --check`, then `model` shall exit with an error naming the design-decision.
shall [x3: agent the person (constant), x4: command `model decisions --check` (parameter), x5: tool `model` (constant)]
  while [x1: design-decision, x2: test]
    tier(x1) = `check`
    outcome(x2) = `failed`
    enforce(subject: x2, object: x1)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## r18
Retires: r6. From: b159 r18. Audit: fine.

```reading
While a design-decision whose status is `accepted` supersedes a design-decision whose status is `accepted`, if the person runs `model check`, then `model` shall exit with an error naming `v_d8`.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant), x6: thing `v_d8` (parameter)]
  while [x1: design-decision, x2: design-decision]
    status(x1) = `accepted`
    status(x2) = `accepted`
    supersede(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x6)
```

## r19
Retires: r7. From: b159 r19. Audit: distortion ("a decisions index", a new one), fixed by section 5 (`This:` on decisions index: "the decisions index").

```reading
When the person runs `work decision`, `work` shall write a design-decision and the decisions index and commit the design-decision and the decisions index.
shall [x1: agent the person (constant), x2: command `work decision` (parameter), x3: tool `work` (constant), x5: decisions index "the decisions index of the bounded context the command runs in" (indexical)]
  when
    run(e1, subject: x1, object: x2)
  response [x4: design-decision]
    write(e2, subject: x3, object: x4)
    write(e3, subject: x3, object: x5)
    commit(e4, subject: x3, object: x4)
    commit(e5, subject: x3, object: x5)
```

## r20
Retires: r8, r9. From: b159 r20. Audit: distortion (an argument "that `work decision` does not have"), fixed by the option in the trigger ("without the `--tier` option"), one line an option that `work decision` requires.

```reading
If the person runs `work decision` without the `--tier` option, then `work` shall refuse the command and name `--tier`.
shall [x1: agent the person (constant), x2: command `work decision` (parameter), x3: option `--tier` (parameter), x4: tool `work` (constant)]
  if
    run(e1, subject: x1, object: x2, without: x3)
  response
    refuse(e2, subject: x4, object: x2)
    name(e3, subject: x4, object: x3)
```

## r21
Retires: r10. From: b159 r21. Audit: fine.

```reading
When the person runs `work decision` with the `--verified-by` option, `work` shall write a design-decision that has a route and commit the design-decision.
shall [x1: agent the person (constant), x2: command `work decision` (parameter), x3: option `--verified-by` (parameter), x4: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2, with: x3)
  response [x5: design-decision, x6: route]
    of(x6, x5)
    write(e2, subject: x4, object: x5)
    commit(e3, subject: x4, object: x5)
```

## r22
Retires: r11. From: b159 r22. Audit: coined (verify's gloss held a status condition; the condition put into the trigger's on), fixed by "every universal condition that no design-decision verifies" in the response (b238) and a plain gloss.

```reading
When the person runs `model check`, `model` shall print every universal condition that no design-decision verifies.
shall [x1: agent the person (constant), x2: command `model check` (parameter), x3: tool `model` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    every [x4: universal condition]
      not [x5: design-decision]
        verify(subject: x5, object: x4)
      scope
        print(e2, subject: x3, object: x4)
```

## r30
Retires: r23. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the kind of a route of a design-decision is not `scenario`, `check`, `judgement` or `monitor`, if the person runs `model check`, then `model` shall exit with an error naming the design-decision.
shall [x3: agent the person (constant), x4: command `model check` (parameter), x5: tool `model` (constant)]
  while [x1: route, x2: design-decision]
    of(x1, x2)
    not
      kind(x1) = `scenario`
    not
      kind(x1) = `check`
    not
      kind(x1) = `judgement`
    not
      kind(x1) = `monitor`
  if
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x2)
```

## r24
Retires: r9. From: b159 r20. Audit: distortion, fixed as r20 is ("without the `--summary` option").

```reading
If the person runs `work decision` without the `--summary` option, then `work` shall refuse the command and name `--summary`.
shall [x1: agent the person (constant), x2: command `work decision` (parameter), x3: option `--summary` (parameter), x4: tool `work` (constant)]
  if
    run(e1, subject: x1, object: x2, without: x3)
  response
    refuse(e2, subject: x4, object: x2)
    name(e3, subject: x4, object: x3)
```

## r25
Retires: r9. From: b159 r20. Audit: distortion, fixed as r20 is ("without the `--decision` option").

```reading
If the person runs `work decision` without the `--decision` option, then `work` shall refuse the command and name `--decision`.
shall [x1: agent the person (constant), x2: command `work decision` (parameter), x3: option `--decision` (parameter), x4: tool `work` (constant)]
  if
    run(e1, subject: x1, object: x2, without: x3)
  response
    refuse(e2, subject: x4, object: x2)
    name(e3, subject: x4, object: x3)
```
