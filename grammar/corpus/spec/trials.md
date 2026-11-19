# trials: every live line with its intended reading (the domain contract, 0.38.0)

## r11
From: trials#r6, reworded in request words (0.38.0).

```reading
When a session hands a trial to `trial-runner`, `trial-runner` shall conduct the trial.
shall [x3: session `trial-runner` (constant)]
  when [x1: session, x2: trial]
    request(e1, measurement.hand, subject: x1, object: x2, to: x3)
  response
    conduct(e2, subject: x3, object: x2)
```

## r12
From: trials#r7, reworded in request words (0.38.0).

```reading
`trial-runner` shall review only files in the target of a trial.
shall [x1: session `trial-runner` (constant)]
  response
    only [x2: file, x3: trial, x4: target]
      of(x4, x3)
      in(x2, x4)
      scope
        review(e1, subject: x1, object: x2)
```

## r13
From: trials#r8, reworded in request words (0.38.0).

```reading
`trial-runner` shall change only the measurement of a trial.
shall [x1: session `trial-runner` (constant)]
  response [x2: trial]
    only [x3: measurement]
      of(x3, x2)
      scope
        change(e1, subject: x1, object: x3)
```

## r14
From: trials#r9, reworded in request words (0.38.0).

```reading
When `trial-runner` conducts a trial, `trial-runner` shall change a measurement of the trial that includes the target of the trial.
shall [x1: session `trial-runner` (constant)]
  when [x2: trial]
    request(e1, measurement.conduct, subject: x1, object: x2)
  response [x3: measurement, x4: target]
    of(x3, x2)
    of(x4, x2)
    include(subject: x3, object: x4)
    change(e2, subject: x1, object: x3)
```

## r15
From: trials#r10, reworded in request words (0.38.0).

```reading
While a trial has a measurement, when `trial-runner` conducts the trial, `trial-runner` shall name the measurement of the trial.
shall [x3: session `trial-runner` (constant)]
  while [x1: trial, x2: measurement]
    of(x2, x1)
  when
    request(e1, measurement.conduct, subject: x3, object: x1)
  response [x4: measurement]
    of(x4, x1)
    name(e2, subject: x3, object: x4)
```
