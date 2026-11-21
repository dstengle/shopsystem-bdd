# review-guarantees: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: pr-review#r1, reworded in request words (0.38.0).

```reading
When the batches service submits a batch, `pr-reviewer` shall review the proposed change of the batch.
shall [x1: service the batches service (constant), x3: dispatch `pr-reviewer` (constant)]
  when [x2: batch]
    request(e1, batches.submit, subject: x1, object: x2)
  response [x4: proposed change]
    of(x4, x2)
    review(e2, subject: x3, object: x4)
```

## r2
From: pr-review#r17, reworded in request words (0.38.0).

```reading
While the tier of a design-decision is `judgement`, when `pr-reviewer` reviews a proposed change, `pr-reviewer` shall review the design-decision.
shall [x2: dispatch `pr-reviewer` (constant)]
  while [x1: design-decision]
    tier(x1) = `judgement`
  when [x3: proposed change]
    request(e1, reviews.review, subject: x2, object: x3)
  response
    review(e2, subject: x2, object: x1)
```

## r3
From: pr-review#r10, reworded in request words (0.38.0).

```reading
`pr-reviewer` shall change only reviews of a proposed change.
shall [x1: dispatch `pr-reviewer` (constant)]
  response
    only [x2: review, x3: proposed change]
      of(x2, x3)
      scope
        change(e1, subject: x1, object: x2)
```

## r4
From: pr-review#r11, reworded in request words (0.38.0).

```reading
While a proposed change of a batch has no review, when `pr-reviewer` reviews the proposed change, `pr-reviewer` shall review every requirement that an item in the batch proposes and every kept change of the batch.
shall [x4: dispatch `pr-reviewer` (constant)]
  while [x1: proposed change, x2: batch]
    of(x1, x2)
    not [x3: review]
      of(x3, x1)
  when
    request(e1, reviews.review, subject: x4, object: x1)
  response
    every [x5: requirement, x6: item]
      in(x6, x2)
      propose(subject: x6, object: x5)
      scope
        review(e2, subject: x4, object: x5)
    every [x7: kept change]
      of(x7, x2)
      scope
        review(e3, subject: x4, object: x7)
```

## r5
From: pr-review#r12, reworded in request words (0.38.0).

```reading
When `pr-reviewer` reviews a proposed change of a batch, `pr-reviewer` shall review only kept changes of the batch.
shall [x1: dispatch `pr-reviewer` (constant)]
  when [x2: proposed change, x3: batch]
    of(x2, x3)
    request(e1, reviews.review, subject: x1, object: x2)
  response
    only [x4: kept change]
      of(x4, x3)
      scope
        review(e2, subject: x1, object: x4)
```

## r6
From: pr-review#r18, reworded in request words (0.38.0).

```reading
While the triage of a review finding on the proposed change of a batch is `fix now`, when a session concludes a review of the batch, the reviews service shall set the status of the batch to `building`.
shall [x6: service the reviews service (constant)]
  while [x1: review finding, x2: batch, x3: proposed change]
    of(x3, x2)
    on(x1, x3)
    triage(x1) = `fix now`
  when [x4: session, x5: review]
    of(x5, x2)
    request(e1, reviews.conclude, subject: x4, object: x5)
  response
    initiates(e2, subject: x6, status(x2) = `building`)
```

## r7
From: pr-review#r19, reworded in request words (0.38.0).

```reading
While the triage of a review finding on a proposed change is `fix now`, when `pr-reviewer` reviews the proposed change, `pr-reviewer` shall review every kept change for the review finding.
shall [x3: dispatch `pr-reviewer` (constant)]
  while [x1: review finding, x2: proposed change]
    on(x1, x2)
    triage(x1) = `fix now`
  when
    request(e1, reviews.review, subject: x3, object: x2)
  response
    every [x4: kept change]
      for(x4, x1)
      scope
        review(e2, subject: x3, object: x4)
```

## r8
From: pr-review#r20, reworded in request words (0.38.0).

```reading
While a batch has a proposed change and no review finding on the proposed change whose triage is `fix now` exists, when a session concludes a review of the batch, the reviews service shall set the status of the batch to `awaiting-merge`.
shall [x6: service the reviews service (constant)]
  while [x1: batch, x2: proposed change]
    of(x2, x1)
    not [x3: review finding]
      on(x3, x2)
      triage(x3) = `fix now`
      exists(x3)
  when [x4: session, x5: review]
    of(x5, x1)
    request(e1, reviews.conclude, subject: x4, object: x5)
  response
    initiates(e2, subject: x6, status(x1) = `awaiting-merge`)
```

## r9
From: pr-review#r16, reworded in request words (0.38.0).

```reading
When `pr-reviewer` reviews a proposed change, `pr-reviewer` shall name the grade of every review finding on the proposed change and the triage of every review finding on the proposed change.
shall [x1: dispatch `pr-reviewer` (constant)]
  when [x2: proposed change]
    request(e1, reviews.review, subject: x1, object: x2)
  response
    every [x3: review finding]
      on(x3, x2)
      scope [x4: grade]
        grade(x3) = x4
        name(e2, subject: x1, object: x4)
    every [x5: review finding]
      on(x5, x2)
      scope [x6: triage]
        triage(x5) = x6
        name(e3, subject: x1, object: x6)
```

## r10
From: b492 r10.

```reading
While the workspace of a batch holds a base merge and the proposed change of the batch has a review and no review finding on the proposed change whose triage is `fix now` exists, when `pr-reviewer` reviews the proposed change, `pr-reviewer` shall review only the base merge.
shall [x7: dispatch `pr-reviewer` (constant)]
  while [x1: batch, x2: workspace, x3: base merge, x4: proposed change, x5: review]
    of(x2, x1)
    in(x3, x2)
    of(x4, x1)
    of(x5, x4)
    not [x6: review finding]
      on(x6, x4)
      triage(x6) = `fix now`
      exists(x6)
  when
    request(e1, reviews.review, subject: x7, object: x4)
  response
    only
      scope
        review(e2, subject: x7, object: x3)
```
