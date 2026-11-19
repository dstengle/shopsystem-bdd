# reviews: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: batches#r11, reworded in request words (0.38.0).

```reading
While an item in a batch is `in-batch`, when the person submits the batch, the batches service shall keep a proposed change of the batch that cites the item.
shall [x3: agent the person (constant), x4: service the batches service (constant)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `in-batch`
  when
    request(e1, batches.submit, subject: x3, object: x2)
  response [x5: proposed change]
    of(x5, x2)
    cite(subject: x5, object: x1)
    keep(e2, subject: x4, object: x5)
```

## r2
From: batches#r37, reworded in request words (0.38.0).

```reading
While the status of an item in a batch is `needs-input` and a kept change cites the item, when the person submits the batch, the batches service shall keep a proposed change of the batch that does not hold the kept change.
shall [x4: agent the person (constant), x5: service the batches service (constant)]
  while [x1: item, x2: batch, x3: kept change]
    in(x1, x2)
    status(x1) = `needs-input`
    cite(subject: x3, object: x1)
  when
    request(e1, batches.submit, subject: x4, object: x2)
  response [x6: proposed change]
    of(x6, x2)
    not
      in(x3, x6)
    keep(e2, subject: x5, object: x6)
```

## r3
From: batches#r29, reworded in request words (0.38.0).

```reading
While a task of a batch is not `done`, if the person submits the batch, then the batches service shall refuse the request and name the task.
shall [x3: agent the person (constant), x4: service the batches service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: task, x2: batch]
    of(x1, x2)
    not
      status(x1) = `done`
  if
    request(e1, batches.submit, subject: x3, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r4
From: batches#r30, reworded in request words (0.38.0).

```reading
While a workspace of a task of a batch holds a kept change that cites no item, if the person submits the batch, then the batches service shall refuse the request and name the kept change.
shall [x6: agent the person (constant), x7: service the batches service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: workspace, x2: task, x3: batch, x4: kept change]
    of(x2, x3)
    of(x1, x2)
    not [x5: item]
      cite(subject: x4, object: x5)
    in(x4, x1)
  if
    request(e1, batches.submit, subject: x6, object: x3)
  response
    refuse(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x4)
```

## r5
From: batches#r35, reworded in request words (0.38.0).

```reading
While a batch is `building` and every task of the batch is `done`, when the person submits the batch, the batches service shall keep a proposed change of the batch and set the status of the batch to `in-review`.
shall [x3: agent the person (constant), x4: service the batches service (constant)]
  while [x1: batch]
    status(x1) = `building`
    every [x2: task]
      of(x2, x1)
      scope
        status(x2) = `done`
  when
    request(e1, batches.submit, subject: x3, object: x1)
  response [x5: proposed change]
    of(x5, x1)
    keep(e2, subject: x4, object: x5)
    initiates(e3, subject: x4, status(x1) = `in-review`)
```
