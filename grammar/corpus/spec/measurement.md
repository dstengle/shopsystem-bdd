# measurement: every live line with its intended reading (the domain contract, 0.38.0)

## r2
From: telemetry#r6, reworded in request words (0.38.0).

```reading
When the person measures a batch that has a proposed change, the measurement service shall keep a measurement of the batch and return the number of review findings on the proposed change whose grade is `Critical`, the number of review findings on the proposed change whose grade is `Important` and the number of review findings on the proposed change whose grade is `Minor`.
shall [x1: agent the person (constant), x4: service the measurement service (constant)]
  when [x2: batch, x3: proposed change]
    of(x3, x2)
    request(e1, measurement.measure, subject: x1, object: x2)
  response [x5: measurement, x6: number, x8: number, x10: number]
    of(x5, x2)
    keep(e2, subject: x4, object: x5)
    number x6 of [x7: review finding]
      on(x7, x3)
      grade(x7) = `Critical`
    return(e3, subject: x4, object: x6)
    number x8 of [x9: review finding]
      on(x9, x3)
      grade(x9) = `Important`
    return(e4, subject: x4, object: x8)
    number x10 of [x11: review finding]
      on(x11, x3)
      grade(x11) = `Minor`
    return(e5, subject: x4, object: x10)
```

## r3
From: telemetry#r7, reworded in request words (0.38.0).

```reading
While an item in a batch is `delivered`, when the person reports a defect in the item, the measurement service shall keep a defect for the batch that the item has.
shall [x3: agent the person (constant), x5: service the measurement service (constant)]
  while [x1: item, x2: batch]
    in(x1, x2)
    status(x1) = `delivered`
  when [x4: defect]
    request(e1, measurement.report, subject: x3, object: x4, in: x1)
  response [x6: defect]
    for(x6, x2)
    of(x6, x1)
    keep(e2, subject: x5, object: x6)
```

## r5
From: batch-measurement#r23, reworded in request words (0.38.0).

```reading
When the person views a measurement that has a stage row that has a round trip, the measurement service shall return the number of round trips of the stage row, every stage row of the measurement and the total row of the measurement.
shall [x1: agent the person (constant), x5: service the measurement service (constant)]
  when [x2: measurement, x3: stage row, x4: round trip]
    of(x4, x3)
    of(x3, x2)
    request(e1, measurement.view, subject: x1, object: x2)
  response [x6: number, x9: total row]
    number x6 of [x7: round trip]
      of(x7, x3)
    return(e2, subject: x5, object: x6)
    every [x8: stage row]
      of(x8, x2)
      scope
        return(e3, subject: x5, object: x8)
    of(x9, x2)
    return(e4, subject: x5, object: x9)
```

## r6
From: batch-measurement#r24, reworded in request words (0.38.0).

```reading
When the person views a measurement that has a stage row that has no round trip, the measurement service shall return every stage row of the measurement and not return a round trip.
shall [x1: agent the person (constant), x5: service the measurement service (constant)]
  when [x2: measurement, x3: stage row]
    not [x4: round trip]
      of(x4, x3)
    of(x3, x2)
    request(e1, measurement.view, subject: x1, object: x2)
  response
    every [x6: stage row]
      of(x6, x2)
      scope
        return(e2, subject: x5, object: x6)
    not [x7: round trip]
      return(e3, subject: x5, object: x7)
```

## r7
From: batch-measurement#r25, reworded in request words (0.38.0).

```reading
When the person views a measurement that has a session row, the measurement service shall return the number of tool uses of the session row, every dispatch of the session row and the number of compactions of the session row.
shall [x1: agent the person (constant), x4: service the measurement service (constant)]
  when [x2: measurement, x3: session row]
    of(x3, x2)
    request(e1, measurement.view, subject: x1, object: x2)
  response [x5: number, x8: number]
    number x5 of [x6: tool use]
      of(x6, x3)
    return(e2, subject: x4, object: x5)
    every [x7: dispatch]
      of(x7, x3)
      scope
        return(e3, subject: x4, object: x7)
    number x8 of [x9: compaction]
      of(x9, x3)
    return(e4, subject: x4, object: x8)
```

## r9
From: batch-measurement#r27, reworded in request words (0.38.0).

```reading
When the person compares a measurement that has a session row, the measurement service shall return the number of tool uses in the measurement and the number of compactions in the measurement.
shall [x1: agent the person (constant), x4: service the measurement service (constant)]
  when [x2: measurement, x3: session row]
    of(x3, x2)
    request(e1, measurement.compare, subject: x1, object: x2)
  response [x5: number, x7: number]
    number x5 of [x6: tool use]
      in(x6, x2)
    return(e2, subject: x4, object: x5)
    number x7 of [x8: compaction]
      in(x8, x2)
    return(e3, subject: x4, object: x7)
```

## r10
Retires: r4. From: b420 r10.

```reading
When the person compares a batch with another batch, the measurement service shall return two measurements and a ratio.
shall [x1: agent the person (constant), x4: service the measurement service (constant)]
  when [x2: batch, x3: batch]
    distinct(x3, x2)
    request(e1, measurement.compare, subject: x1, object: x2, with: x3)
  response [x5: measurement, x6: measurement, x7: ratio]
    return(e2, subject: x4, object: x5)
    distinct(x6, x5)
    return(e3, subject: x4, object: x6)
    return(e4, subject: x4, object: x7)
```

## r11
Retires: r8. From: b420 r11.

```reading
When the person compares a measurement with another measurement, the measurement service shall return two total rows and a ratio.
shall [x1: agent the person (constant), x4: service the measurement service (constant)]
  when [x2: measurement, x3: measurement]
    distinct(x3, x2)
    request(e1, measurement.compare, subject: x1, object: x2, with: x3)
  response [x5: total row, x6: total row, x7: ratio]
    return(e2, subject: x4, object: x5)
    distinct(x6, x5)
    return(e3, subject: x4, object: x6)
    return(e4, subject: x4, object: x7)
```

## r13
Retires: r12. From: b876 r13.

```reading
While a batch is `merged`, when the person measures the batch, the measurement service shall keep a measurement of the batch and return the wall time of the batch, the session time of the batch, the tokens of the batch, the cost of every role of the batch, the duration of every test run of the measurement, the opening time of the measurement and the duration of every opening phase of the measurement.
shall [x2: agent the person (constant), x3: service the measurement service (constant)]
  while [x1: batch]
    status(x1) = `merged`
  when
    request(e1, measurement.measure, subject: x2, object: x1)
  response [x4: measurement, x5: wall time, x6: session time, x7: token, x12: opening time]
    of(x4, x1)
    keep(e2, subject: x3, object: x4)
    of(x5, x1)
    return(e3, subject: x3, object: x5)
    of(x6, x1)
    return(e4, subject: x3, object: x6)
    of(x7, x1)
    return(e5, subject: x3, object: x7)
    every [x8: role]
      of(x8, x1)
      scope [x9: cost]
        of(x9, x8)
        return(e6, subject: x3, object: x9)
    every [x10: test run]
      of(x10, x4)
      scope [x11: duration]
        of(x11, x10)
        return(e7, subject: x3, object: x11)
    of(x12, x4)
    return(e8, subject: x3, object: x12)
    every [x13: opening phase]
      of(x13, x4)
      scope [x14: duration]
        of(x14, x13)
        return(e9, subject: x3, object: x14)
```
