# laying: every live line with its intended reading

## r1
From: b611 r1.

```reading
While an item holds a requirement, when the batches service lays the item in a workspace, the laying service shall keep the workspace that holds the requirement and keep a scenario that refers to the requirement id of the requirement.
shall [x3: service the batches service (constant), x5: service the laying service (constant)]
  while [x1: item, x2: requirement]
    in(x2, x1)
  when [x4: workspace]
    request(e1, laying.lay, subject: x3, object: x1, in: x4)
  response [x6: scenario, x7: requirement id]
    in(x2, x4)
    keep(e2, subject: x5, object: x4)
    of(x7, x2)
    refer(subject: x6, to: x7)
    keep(e3, subject: x5, object: x6)
```

## r2
From: b611 r2.

```reading
While a workspace holds a requirement of an item, when the batches service lifts the item from the workspace, the laying service shall keep a workspace that does not hold the requirement.
shall [x4: service the batches service (constant), x5: service the laying service (constant)]
  while [x1: workspace, x2: requirement, x3: item]
    of(x2, x3)
    in(x2, x1)
  when
    request(e1, laying.lift, subject: x4, object: x3, from: x1)
  response [x6: workspace]
    not
      in(x2, x6)
    keep(e2, subject: x5, object: x6)
```

## r3
From: b611 r3.

```reading
While a requirement of an item violates a rule whose severity is `error`, when the batches service checks the item in a workspace, the laying service shall fail the request and name the rule.
shall [x4: service the batches service (constant), x6: service the laying service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: requirement, x2: item, x3: rule]
    of(x1, x2)
    severity(x3) = `error`
    violate(subject: x1, object: x3)
  when [x5: workspace]
    request(e1, laying.check, subject: x4, object: x2, in: x5)
  response
    fail(e2, subject: x6, object: x7)
    name(e3, subject: x6, object: x3)
```

## r4
From: b611 r4.

```reading
While an item holds no requirement that violates a rule whose severity is `error`, when the batches service checks the item in a workspace, the laying service shall complete the request.
shall [x4: service the batches service (constant), x6: service the laying service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: item]
    not [x2: requirement, x3: rule]
      severity(x3) = `error`
      violate(subject: x2, object: x3)
      in(x2, x1)
  when [x5: workspace]
    request(e1, laying.check, subject: x4, object: x1, in: x5)
  response
    complete(e2, subject: x6, object: x7)
```

## r5
From: b755 r5.

```reading
While an item holds a requirement that retires the requirement id of a requirement of a requirement group and a workspace holds another requirement that retires the requirement id of another requirement of the requirement group, when the batches service lifts the item from the workspace, the laying service shall keep a workspace that does not hold the requirement.
shall [x10: service the batches service (constant), x11: service the laying service (constant)]
  while [x1: item, x2: requirement, x3: requirement, x4: requirement group, x5: requirement id, x6: workspace, x7: requirement, x8: requirement, x9: requirement id]
    of(x3, x4)
    of(x5, x3)
    retire(subject: x2, object: x5)
    in(x2, x1)
    distinct(x7, x3)
    distinct(x8, x3)
    of(x8, x4)
    of(x9, x8)
    retire(subject: x7, object: x9)
    in(x7, x6)
  when
    request(e1, laying.lift, subject: x10, object: x1, from: x6)
  response [x12: workspace]
    not
      in(x8, x12)
    keep(e2, subject: x11, object: x12)
```
