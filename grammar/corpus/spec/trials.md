# trials: every live line with its intended reading (b240)

## r6
Retires: r1. From: b154 r6. Audit: fine.

```reading
When a session sends a trial to `trial-runner`, `trial-runner` shall start the trial.
shall [x3: dispatch `trial-runner` (constant)]
  when [x1: session, x2: trial]
    send(e1, subject: x1, object: x2, to: x3)
  response
    start(e2, subject: x3, object: x2)
```

## r7
Retires: r2. From: b154 r7. Audit: distortion, fixed by section 5 (an invariant with no trigger, not "When `trial-runner` starts a trial").

```reading
`trial-runner` shall read only files in the target of a trial.
shall [x1: dispatch `trial-runner` (constant)]
  response
    only [x2: file, x3: trial, x4: target]
      of(x4, x3)
      in(x2, x4)
      scope
        read(e1, subject: x1, object: x2)
```

## r8
Retires: r3. From: b154 r8. Audit: distortion, fixed by section 5 (an invariant with no trigger, not "When `trial-runner` starts a trial").

```reading
`trial-runner` shall write only the measurement of a trial.
shall [x1: dispatch `trial-runner` (constant)]
  response [x2: trial]
    only [x3: measurement]
      of(x3, x2)
      scope
        write(e1, subject: x1, object: x3)
```

## r9
Retires: r4. From: b154 r9. Audit: fine.

```reading
When `trial-runner` ends a trial, `trial-runner` shall write a measurement of the trial that lists the target of the trial.
shall [x1: dispatch `trial-runner` (constant)]
  when [x2: trial]
    end(e1, subject: x1, object: x2)
  response [x3: measurement, x4: target]
    of(x3, x2)
    of(x4, x2)
    list(subject: x3, object: x4)
    write(e2, subject: x1, object: x3)
```

## r10
Retires: r5. From: b154 r10. Audit: fine.

```reading
When `trial-runner` writes a measurement, `trial-runner` shall write a reply that lists the measurement.
shall [x1: dispatch `trial-runner` (constant)]
  when [x2: measurement]
    write(e1, subject: x1, object: x2)
  response [x3: reply]
    list(subject: x3, object: x2)
    write(e2, subject: x1, object: x3)
```
