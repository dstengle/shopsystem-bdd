# batch-measurement: every live line with its intended reading (b240)

## r23
Retires: r18. From: b156 r23. Audit: distortion, fixed by the number of (construct `number-of`) in place of the count noun.

```reading
When the person runs `measure show` on a measurement that has a stage row that has a round trip, `measure` shall print the number of round trips of the stage row, every stage row of the measurement and the total row of the measurement.
shall [x1: agent the person (constant), x2: command `measure show` (parameter), x6: tool `measure` (constant)]
  when [x3: measurement, x4: stage row, x5: round trip]
    of(x5, x4)
    of(x4, x3)
    run(e1, subject: x1, object: x2, on: x3)
  response [x7: number, x10: total row]
    number x7 of [x8: round trip]
      of(x8, x4)
    print(e2, subject: x6, object: x7)
    every [x9: stage row]
      of(x9, x3)
      scope
        print(e3, subject: x6, object: x9)
    of(x10, x3)
    print(e4, subject: x6, object: x10)
```

## r24
Retires: r19. From: b156 r24. Audit: distortion, fixed by "has no round trip" and "not print a round trip" in place of the count noun.

```reading
When the person runs `measure show` on a measurement that has a stage row that has no round trip, `measure` shall print every stage row of the measurement and not print a round trip.
shall [x1: agent the person (constant), x2: command `measure show` (parameter), x6: tool `measure` (constant)]
  when [x3: measurement, x4: stage row]
    not [x5: round trip]
      of(x5, x4)
    of(x4, x3)
    run(e1, subject: x1, object: x2, on: x3)
  response
    every [x7: stage row]
      of(x7, x3)
      scope
        print(e2, subject: x6, object: x7)
    not [x8: round trip]
      print(e3, subject: x6, object: x8)
```

## r25
Retires: r20. From: b156 r25. Audit: distortion, fixed by the number of (construct `number-of`). The tool uses by tool are the implementation's.

```reading
When the person runs `measure show` on a measurement that has a session row, `measure` shall print the number of tool uses of the session row, every dispatch of the session row and the number of compactions of the session row.
shall [x1: agent the person (constant), x2: command `measure show` (parameter), x5: tool `measure` (constant)]
  when [x3: measurement, x4: session row]
    of(x4, x3)
    run(e1, subject: x1, object: x2, on: x3)
  response [x6: number, x9: number]
    number x6 of [x7: tool use]
      of(x7, x4)
    print(e2, subject: x5, object: x6)
    every [x8: dispatch]
      of(x8, x4)
      scope
        print(e3, subject: x5, object: x8)
    number x9 of [x10: compaction]
      of(x10, x4)
    print(e4, subject: x5, object: x9)
```

## r26
Retires: r21. From: b156 r26. Audit: distortion, fixed by identity (construct `two`). Known limit: #10 (the total row of each of the measurements) and #18 (the ratio).

```reading
When the person runs `measure compare` on two measurements, `measure` shall print two total rows and a ratio.
shall [x1: agent the person (constant), x2: command `measure compare` (parameter), x5: tool `measure` (constant)]
  when [x3: measurement, x4: measurement]
    run(e1, subject: x1, object: x2, on: x3)
    distinct(x4, x3)
    run(e2, subject: x1, object: x2, on: x4)
  response [x6: total row, x7: total row, x8: ratio]
    print(e3, subject: x5, object: x6)
    distinct(x7, x6)
    print(e4, subject: x5, object: x7)
    print(e5, subject: x5, object: x8)
```

## r27
Retires: r22. From: b156 r27. Audit: distortion, fixed by the number of (construct `number-of`) over the measurement's tool uses and compactions, the totals over its session rows.

```reading
When the person runs `measure compare` on a measurement that has a session row, `measure` shall print the number of tool uses in the measurement and the number of compactions in the measurement.
shall [x1: agent the person (constant), x2: command `measure compare` (parameter), x5: tool `measure` (constant)]
  when [x3: measurement, x4: session row]
    of(x4, x3)
    run(e1, subject: x1, object: x2, on: x3)
  response [x6: number, x8: number]
    number x6 of [x7: tool use]
      in(x7, x3)
    print(e2, subject: x5, object: x6)
    number x8 of [x9: compaction]
      in(x9, x3)
    print(e3, subject: x5, object: x8)
```
