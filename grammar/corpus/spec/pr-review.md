# pr-review: every live line with its intended reading (b240)

## r1
Kept. Known limit: #16 (liveness: a review follows the publication eventually, after `work batch brief`, not at the next step).

```reading
When `work` publishes a pull request of a batch, `pr-reviewer` shall write a review of the pull request.
shall [x1: tool `work` (constant), x4: dispatch `pr-reviewer` (constant)]
  when [x2: pull request, x3: batch]
    of(x2, x3)
    publish(e1, subject: x1, object: x2)
  response [x5: review]
    of(x5, x2)
    write(e2, subject: x4, object: x5)
```

## r17
Retires: r4. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the tier of a design-decision is `judgement`, when `pr-reviewer` writes a review of a pull request, `pr-reviewer` shall read the design-decision.
shall [x2: dispatch `pr-reviewer` (constant)]
  while [x1: design-decision]
    tier(x1) = `judgement`
  when [x3: review, x4: pull request]
    of(x3, x4)
    write(e1, subject: x2, object: x3)
  response
    read(e2, subject: x2, object: x1)
```

## r10
Retires: r2. From: b159 r10. Audit: fine.

```reading
`pr-reviewer` shall write only reviews of a pull request.
shall [x1: dispatch `pr-reviewer` (constant)]
  response
    only [x2: review, x3: pull request]
      of(x2, x3)
      scope
        write(e1, subject: x1, object: x2)
```

## r11
Retires: r3. From: b159 r11. Audit: fine.

```reading
While a pull request of a batch has no review, when `pr-reviewer` writes a review of the pull request, `pr-reviewer` shall read every requirement that an item in the batch proposes and every commit of the batch.
shall [x4: dispatch `pr-reviewer` (constant)]
  while [x1: pull request, x2: batch]
    of(x1, x2)
    not [x3: review]
      of(x3, x1)
  when [x5: review]
    of(x5, x1)
    write(e1, subject: x4, object: x5)
  response
    every [x6: requirement, x7: item]
      in(x7, x2)
      propose(subject: x7, object: x6)
      scope
        read(e2, subject: x4, object: x6)
    every [x8: commit]
      of(x8, x2)
      scope
        read(e3, subject: x4, object: x8)
```

## r12
Retires: r3. From: b159 r12. Audit: fine.

```reading
When `pr-reviewer` writes a review of a pull request of a batch, `pr-reviewer` shall read only commits of the batch.
shall [x1: dispatch `pr-reviewer` (constant)]
  when [x2: review, x3: pull request, x4: batch]
    of(x3, x4)
    of(x2, x3)
    write(e1, subject: x1, object: x2)
  response
    only [x5: commit]
      of(x5, x4)
      scope
        read(e2, subject: x1, object: x5)
```

## r18
Retires: r13. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the triage of a review finding on a pull request of a batch is `fix now`, when a session runs `work batch reviewed` on the batch, `work` shall set the status of the batch to `building`.
shall [x5: command `work batch reviewed` (parameter), x6: tool `work` (constant)]
  while [x1: review finding, x2: pull request, x3: batch]
    of(x2, x3)
    on(x1, x2)
    triage(x1) = `fix now`
  when [x4: session]
    run(e1, subject: x4, object: x5, on: x3)
  response
    initiates(e2, subject: x6, status(x3) = `building`)
```

## r19
Retires: r14. From: b257. Audit: the short form of a noun value, said in the full form.

```reading
While the triage of a review finding on a pull request is `fix now`, when `pr-reviewer` writes a review of the pull request, `pr-reviewer` shall read every commit for the review finding.
shall [x3: dispatch `pr-reviewer` (constant)]
  while [x1: review finding, x2: pull request]
    on(x1, x2)
    triage(x1) = `fix now`
  when [x4: review]
    of(x4, x2)
    write(e1, subject: x3, object: x4)
  response
    every [x5: commit]
      for(x5, x1)
      scope
        read(e2, subject: x3, object: x5)
```

## r20
Retires: r15. From: b257. Audit: the short form of a noun value, said in the full form, "no review finding ... exists".

```reading
While a batch has a pull request and no review finding on the pull request whose triage is `fix now` exists, when a session runs `work batch reviewed` on the batch, `work` shall set the status of the batch to `awaiting-merge`.
shall [x5: command `work batch reviewed` (parameter), x6: tool `work` (constant)]
  while [x1: batch, x2: pull request]
    of(x2, x1)
    not [x3: review finding]
      on(x3, x2)
      triage(x3) = `fix now`
      exists(x3)
  when [x4: session]
    run(e1, subject: x4, object: x5, on: x1)
  response
    initiates(e2, subject: x6, status(x1) = `awaiting-merge`)
```

## r16
Retires: r9. From: b159 r16. Audit: fine.

```reading
When `pr-reviewer` writes a review finding, `pr-reviewer` shall name the grade of the review finding and the triage of the review finding.
shall [x1: dispatch `pr-reviewer` (constant)]
  when [x2: review finding]
    write(e1, subject: x1, object: x2)
  response [x3: grade, x4: triage]
    grade(x2) = x3
    name(e2, subject: x1, object: x3)
    triage(x2) = x4
    name(e3, subject: x1, object: x4)
```
