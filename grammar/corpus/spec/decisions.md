# decisions: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: decision-tiers#r13, reworded in request words (0.38.0).

```reading
While a design-decision is not `superseded` or `rejected` and the design-decision has no tier, when the person validates this specification, the specification service shall return `w_untiered`.
shall [x2: agent the person (constant), x3: specification "the specification of this bounded context" (indexical), x4: service the specification service (constant), x5: thing `w_untiered` (parameter)]
  while [x1: design-decision]
    not
      status(x1) = `superseded`
    not
      status(x1) = `rejected`
    tier(x1) = none
  when
    request(e1, specification.check, subject: x2, object: x3)
  response
    return(e2, subject: x4, object: x5)
```

## r2
From: decision-tiers#r26, reworded in request words (0.38.0).

```reading
While the tier of a design-decision is `check` and no test enforces the design-decision, if the person validates this specification, then the specification service shall fail the check and name `v_d6`.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical), x7: thing `v_d6` (parameter)]
  while [x1: design-decision]
    tier(x1) = `check`
    not [x2: test]
      enforce(subject: x2, object: x1)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x7)
```

## r3
From: decision-tiers#r27, reworded in request words (0.38.0).

```reading
While the tier of a design-decision is `requirement` and no requirement enforces the design-decision, if the person validates this specification, then the specification service shall fail the check and name `v_d7`.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical), x7: thing `v_d7` (parameter)]
  while [x1: design-decision]
    tier(x1) = `requirement`
    not [x2: requirement]
      enforce(subject: x2, object: x1)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x7)
```

## r4
From: decision-tiers#r28, reworded in request words (0.38.0).

```reading
While the tier of a design-decision is `check` and a test enforces the design-decision, when the person rebuilds the decisions index with the audit, the decisions service shall return the verdict of the test.
shall [x3: agent the person (constant), x4: decisions index "the decisions index of this bounded context" (indexical), x5: service the decisions service (constant)]
  while [x1: design-decision, x2: test]
    tier(x1) = `check`
    enforce(subject: x2, object: x1)
  when
    request(e1, decisions.rebuild, subject: x3, object: x4)
    param(e1, audit, on)
  response [x6: verdict]
    verdict(x2) = x6
    return(e2, subject: x5, object: x6)
```

## r5
From: decision-tiers#r29, reworded in request words (0.38.0).

```reading
While the tier of a design-decision is `check` and a test whose verdict is `failed` enforces the design-decision, if the person rebuilds the decisions index with the audit, then the decisions service shall fail the check and name the design-decision.
shall [x3: agent the person (constant), x4: decisions index "the decisions index of this bounded context" (indexical), x5: service the decisions service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: design-decision, x2: test]
    tier(x1) = `check`
    verdict(x2) = `failed`
    enforce(subject: x2, object: x1)
  if
    request(e1, decisions.rebuild, subject: x3, object: x4)
    param(e1, audit, on)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r6
From: decision-tiers#r18, reworded in request words (0.38.0).

```reading
While a design-decision whose status is `accepted` supersedes a design-decision whose status is `accepted`, if the person validates this specification, then the specification service shall fail the check and name `v_d8`.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical), x7: thing `v_d8` (parameter)]
  while [x1: design-decision, x2: design-decision]
    status(x1) = `accepted`
    status(x2) = `accepted`
    supersede(subject: x1, object: x2)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x7)
```

## r7
From: decision-tiers#r19, reworded in request words (0.38.0).

```reading
When the person enters a design-decision, the decisions service shall keep the design-decision and the decisions index.
shall [x1: agent the person (constant), x3: service the decisions service (constant), x4: decisions index "the decisions index of this bounded context" (indexical)]
  when [x2: design-decision]
    request(e1, decisions.enter, subject: x1, object: x2)
  response
    keep(e2, subject: x3, object: x2)
    keep(e3, subject: x3, object: x4)
```

## r8
From: decision-tiers#r20, reworded in request words (0.38.0).

```reading
If the person enters a design-decision without a tier, then the decisions service shall refuse the request and name the tier.
shall [x1: agent the person (constant), x3: service the decisions service (constant), x4: request "the request the trigger makes" (indexical), x5: parameter tier (constant)]
  if [x2: design-decision]
    request(e1, decisions.enter, subject: x1, object: x2)
    noparam(e1, tier)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x5)
```

## r9
From: decision-tiers#r24, reworded in request words (0.38.0).

```reading
If the person enters a design-decision without a summary, then the decisions service shall refuse the request and name the summary.
shall [x1: agent the person (constant), x3: service the decisions service (constant), x4: request "the request the trigger makes" (indexical), x5: parameter summary (constant)]
  if [x2: design-decision]
    request(e1, decisions.enter, subject: x1, object: x2)
    noparam(e1, summary)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x5)
```

## r10
From: decision-tiers#r25, reworded in request words (0.38.0).

```reading
If the person enters a design-decision without a wording, then the decisions service shall refuse the request and name the wording.
shall [x1: agent the person (constant), x3: service the decisions service (constant), x4: request "the request the trigger makes" (indexical), x5: parameter wording (constant)]
  if [x2: design-decision]
    request(e1, decisions.enter, subject: x1, object: x2)
    noparam(e1, wording)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x5)
```

## r11
From: decision-tiers#r21, reworded in request words (0.38.0).

```reading
When the person enters a design-decision with a route, the decisions service shall keep a design-decision that has a route.
shall [x1: agent the person (constant), x4: service the decisions service (constant)]
  when [x2: design-decision, x3: route]
    request(e1, decisions.enter, subject: x1, object: x2)
    param(e1, route, x3)
  response [x5: design-decision, x6: route]
    of(x6, x5)
    keep(e2, subject: x4, object: x5)
```

## r12
From: decision-tiers#r22, reworded in request words (0.38.0).

```reading
When the person validates this specification, the specification service shall return every universal condition that no design-decision verifies.
shall [x1: agent the person (constant), x2: specification "the specification of this bounded context" (indexical), x3: service the specification service (constant)]
  when
    request(e1, specification.check, subject: x1, object: x2)
  response
    every [x4: universal condition]
      not [x5: design-decision]
        verify(subject: x5, object: x4)
      scope
        return(e2, subject: x3, object: x4)
```

## r13
From: decision-tiers#r30, reworded in request words (0.38.0).

```reading
While the kind of a route of a design-decision is not `scenario`, `check`, `judgement` or `monitor`, if the person validates this specification, then the specification service shall fail the check and name the design-decision.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
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
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x2)
```

## r14
From: decision-tiers#r31, reworded in request words (0.38.0).

```reading
When the person enters a design-decision over a design-decision whose status is `accepted`, the decisions service shall set the status of the design-decision to `superseded` and keep the design-decision.
shall [x1: agent the person (constant), x4: service the decisions service (constant)]
  when [x2: design-decision, x3: design-decision]
    status(x3) = `accepted`
    request(e1, decisions.enter, subject: x1, object: x2, over: x3)
  response
    initiates(e2, subject: x4, status(x3) = `superseded`)
    keep(e3, subject: x4, object: x3)
```

## r15
From: decision-tiers#r32, reworded in request words (0.38.0).

```reading
If the person enters a design-decision over a design-decision whose status is not `accepted`, then the decisions service shall refuse the request and name the design-decision.
shall [x1: agent the person (constant), x4: service the decisions service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: design-decision, x3: design-decision]
    not
      status(x3) = `accepted`
    request(e1, decisions.enter, subject: x1, object: x2, over: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x3)
```

## r16
From: design-model-check#r50, reworded in request words (0.38.0).

```reading
When the person rebuilds the decisions index, the decisions service shall keep the decisions index.
shall [x1: agent the person (constant), x2: decisions index "the decisions index of this bounded context" (indexical), x3: service the decisions service (constant)]
  when
    request(e1, decisions.rebuild, subject: x1, object: x2)
  response
    keep(e2, subject: x3, object: x2)
```

## r17
From: design-model-check#r194, reworded in request words (0.38.0).

```reading
While a design-decision has no id, if the person validates this specification, then the specification service shall fail the check and name the design-decision.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: design-decision]
    not [x2: id]
      of(x2, x1)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r18
From: design-model-check#r202, reworded in request words (0.38.0).

```reading
While a design-decision has an index entry that a decisions index does not hold, if the person rebuilds the decisions index with the audit, then the decisions service shall fail the check, name the decisions index and change no file.
shall [x4: agent the person (constant), x5: service the decisions service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: design-decision, x2: index entry, x3: decisions index]
    not
      in(x2, x3)
    of(x2, x1)
  if
    request(e1, decisions.rebuild, subject: x4, object: x3)
    param(e1, audit, on)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
    not [x7: file]
      change(e4, subject: x5, object: x7)
```

## r19
From: design-model-check#r203, reworded in request words (0.38.0).

```reading
While no decisions index lacks an index entry, when the person rebuilds the decisions index with the audit, the decisions service shall complete the request.
shall [x3: agent the person (constant), x4: decisions index "the decisions index of this bounded context" (indexical), x5: service the decisions service (constant), x6: request "the request the trigger makes" (indexical)]
  while
    not [x1: decisions index, x2: index entry]
      lack(subject: x1, object: x2)
  when
    request(e1, decisions.rebuild, subject: x3, object: x4)
    param(e1, audit, on)
  response
    complete(e2, subject: x5, object: x6)
```

## r20
From: design-model-check#r286, reworded in request words (0.38.0).

```reading
While a design-decision has no section whose heading is `Decision`, if the person validates this specification, then the specification service shall fail the check and name the design-decision.
shall [x3: agent the person (constant), x4: specification "the specification of this bounded context" (indexical), x5: service the specification service (constant), x6: check "the check the trigger makes" (indexical)]
  while [x1: design-decision]
    not [x2: section]
      heading(x2) = `Decision`
      of(x2, x1)
  if
    request(e1, specification.check, subject: x3, object: x4)
  response
    fail(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```
