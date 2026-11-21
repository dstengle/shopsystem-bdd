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

## r6
From: b449 r6.

```reading
While a batch is `building` and every task of the batch is `done` and the workspace of the batch holds a virtual environment, when the person submits the batch, the batches service shall keep a proposed change of the batch and set the status of the batch to `in-review`.
shall [x5: agent the person (constant), x6: service the batches service (constant)]
  while [x1: batch, x3: workspace, x4: virtual environment]
    status(x1) = `building`
    every [x2: task]
      of(x2, x1)
      scope
        status(x2) = `done`
    of(x3, x1)
    in(x4, x3)
  when
    request(e1, batches.submit, subject: x5, object: x1)
  response [x7: proposed change]
    of(x7, x1)
    keep(e2, subject: x6, object: x7)
    initiates(e3, subject: x6, status(x1) = `in-review`)
```

## r7
From: b491 r7.

```reading
While a batch is `building` and every task of the batch is `done` and an item in the batch is `in-batch` and a kept change that touches a file cites the item and another kept change touches the file and another item in the batch is `in-batch` and the kept change cites the item and no kept change conflicts with a kept change, when the person submits the batch, the batches service shall keep a proposed change of the batch that holds the kept change and set the status of the batch to `in-review`.
shall [x10: agent the person (constant), x11: service the batches service (constant)]
  while [x1: batch, x3: item, x4: kept change, x5: file, x6: kept change, x7: item]
    status(x1) = `building`
    every [x2: task]
      of(x2, x1)
      scope
        status(x2) = `done`
    in(x3, x1)
    status(x3) = `in-batch`
    touch(subject: x4, object: x5)
    cite(subject: x4, object: x3)
    distinct(x6, x4)
    touch(subject: x6, object: x5)
    distinct(x7, x3)
    in(x7, x1)
    status(x7) = `in-batch`
    cite(subject: x6, object: x7)
    not [x8: kept change, x9: kept change]
      conflict(subject: x8, with: x9)
  when
    request(e1, batches.submit, subject: x10, object: x1)
  response [x12: proposed change]
    of(x12, x1)
    in(x6, x12)
    keep(e2, subject: x11, object: x12)
    initiates(e3, subject: x11, status(x1) = `in-review`)
```

## r8
From: b491 r8.

```reading
While an item in a batch is `in-batch` and a kept change cites the item and another item in the batch is `in-batch` and the kept change conflicts with another kept change that cites the item and the kept change touches a file, if the person submits the batch, then the batches service shall refuse the request and name the file, the item and every item in the batch that a kept change that conflicts with the kept change cites.
shall [x7: agent the person (constant), x8: service the batches service (constant), x9: request "the request the trigger makes" (indexical)]
  while [x1: item, x2: batch, x3: kept change, x4: item, x5: kept change, x6: file]
    in(x1, x2)
    status(x1) = `in-batch`
    cite(subject: x3, object: x1)
    distinct(x4, x1)
    in(x4, x2)
    status(x4) = `in-batch`
    distinct(x5, x3)
    cite(subject: x5, object: x4)
    conflict(subject: x3, with: x5)
    touch(subject: x5, object: x6)
  if
    request(e1, batches.submit, subject: x7, object: x2)
  response
    refuse(e2, subject: x8, object: x9)
    name(e3, subject: x8, object: x6)
    name(e4, subject: x8, object: x4)
    every [x10: item, x11: kept change]
      in(x10, x2)
      conflict(subject: x11, with: x5)
      cite(subject: x11, object: x10)
      scope
        name(e5, subject: x8, object: x10)
```

## r9
From: b492 r9.

```reading
While a batch is `awaiting-merge` and the workspace of the batch holds a base merge, when the person submits the batch, the batches service shall keep a proposed change of the batch and set the status of the batch to `in-review`.
shall [x4: agent the person (constant), x5: service the batches service (constant)]
  while [x1: batch, x2: workspace, x3: base merge]
    status(x1) = `awaiting-merge`
    of(x2, x1)
    in(x3, x2)
  when
    request(e1, batches.submit, subject: x4, object: x1)
  response [x6: proposed change]
    of(x6, x1)
    keep(e2, subject: x5, object: x6)
    initiates(e3, subject: x5, status(x1) = `in-review`)
```

## r10
From: b492 r10.

```reading
While a batch is `awaiting-merge` and the workspace of the batch holds no base merge, if the person submits the batch, then the batches service shall refuse the request and name the batch.
shall [x4: agent the person (constant), x5: service the batches service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: batch, x2: workspace]
    status(x1) = `awaiting-merge`
    of(x2, x1)
    not [x3: base merge]
      in(x3, x2)
  if
    request(e1, batches.submit, subject: x4, object: x1)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r11
From: b69 r11.

```reading
While a batch is `awaiting-merge`, when the person reopens the batch with a review finding, the batches service shall keep a review of the batch that holds the review finding and set the status of the batch to `building`.
shall [x2: agent the person (constant), x4: service the batches service (constant)]
  while [x1: batch]
    status(x1) = `awaiting-merge`
  when [x3: review finding]
    request(e1, batches.reopen, subject: x2, object: x1)
    param(e1, review finding, x3)
  response [x5: review]
    of(x5, x1)
    in(x3, x5)
    keep(e2, subject: x4, object: x5)
    initiates(e3, subject: x4, status(x1) = `building`)
```

## r12
From: b69 r12.

```reading
While a batch is not `awaiting-merge`, if the person reopens the batch with a review finding, then the batches service shall refuse the request and name the batch.
shall [x2: agent the person (constant), x4: service the batches service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: batch]
    not
      status(x1) = `awaiting-merge`
  if [x3: review finding]
    request(e1, batches.reopen, subject: x2, object: x1)
    param(e1, review finding, x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```
