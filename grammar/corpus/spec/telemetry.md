# telemetry: every live line with its intended reading (b240)

## r5
Retires: r1. From: b156 r5. Audit: coined ("figure"), fixed by section 5 (the four figures listed in the line).

```reading
While a batch is `merged`, when the person runs `measure batch` on the batch, `measure` shall write a measurement of the batch that includes the wall time of the batch, the session time of the batch, the tokens of the batch and the cost of every role of the batch.
shall [x2: agent the person (constant), x3: command `measure batch` (parameter), x4: tool `measure` (constant)]
  while [x1: batch]
    status(x1) = `merged`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: measurement, x6: wall time, x7: session time, x8: token]
    of(x5, x1)
    of(x6, x1)
    include(subject: x5, object: x6)
    of(x7, x1)
    include(subject: x5, object: x7)
    of(x8, x1)
    include(subject: x5, object: x8)
    every [x9: role]
      of(x9, x1)
      scope [x10: cost]
        of(x10, x9)
        include(subject: x5, object: x10)
    write(e2, subject: x4, object: x5)
```

## r6
Retires: r2. From: b156 r6. Audit: distortion, fixed by the number of (construct `number-of`), one count of each grade.

```reading
When the person runs `measure batch` on a batch that has a pull request, `measure` shall write a measurement of the batch that includes the number of review findings on the pull request whose grade is `Critical`, the number of review findings on the pull request whose grade is `Important` and the number of review findings on the pull request whose grade is `Minor`.
shall [x1: agent the person (constant), x2: command `measure batch` (parameter), x5: tool `measure` (constant)]
  when [x3: batch, x4: pull request]
    of(x4, x3)
    run(e1, subject: x1, object: x2, on: x3)
  response [x6: measurement, x7: number, x9: number, x11: number]
    of(x6, x3)
    number x7 of [x8: review finding]
      on(x8, x4)
      grade(x8) = `Critical`
    include(subject: x6, object: x7)
    number x9 of [x10: review finding]
      on(x10, x4)
      grade(x10) = `Important`
    include(subject: x6, object: x9)
    number x11 of [x12: review finding]
      on(x12, x4)
      grade(x12) = `Minor`
    include(subject: x6, object: x11)
    write(e2, subject: x5, object: x6)
```

## r7
Retires: r3. From: b156 r7. Audit: fine.

```reading
While an item in a batch is `delivered`, when the person runs `measure defect` on the item, `measure` shall write a defect for the batch that the item has.
shall [x3: agent the person (constant), x4: command `measure defect` (parameter), x5: tool `measure` (constant)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `delivered`
  when
    run(e1, subject: x3, object: x4, on: x1)
  response [x6: defect]
    for(x6, x2)
    of(x6, x1)
    write(e2, subject: x5, object: x6)
```

## r8
Retires: r4. From: b156 r8. Audit: distortion, fixed by identity (construct `two`: two batches). Known limit: #10 (the measurement of each of the batches) and #18 (the ratio).

```reading
When the person runs `measure compare` on two batches, `measure` shall print two measurements and a ratio.
shall [x1: agent the person (constant), x2: command `measure compare` (parameter), x5: tool `measure` (constant)]
  when [x3: batch, x4: batch]
    run(e1, subject: x1, object: x2, on: x3)
    distinct(x4, x3)
    run(e2, subject: x1, object: x2, on: x4)
  response [x6: measurement, x7: measurement, x8: ratio]
    print(e3, subject: x5, object: x6)
    distinct(x7, x6)
    print(e4, subject: x5, object: x7)
    print(e5, subject: x5, object: x8)
```
