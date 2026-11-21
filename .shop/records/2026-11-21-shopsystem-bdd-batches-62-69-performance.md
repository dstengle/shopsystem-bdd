---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-21-shopsystem-bdd-batches-62-69-performance
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-21
---

# shopsystem-bdd, batches 62-69: performance

Plugin 0.44.0. Batches 62-69, 2026-11-20 to 2026-11-21. Measurements: `.shop/records/measurements/2026-11-21-batch-62.md` … `-batch-69.md`. Compared with: batches 58-61 (`.shop/records/measurements/*-batch-58.md` … `-batch-61.md`).

## The delivery

Every figure is from `measure show` of each batch's measurement. The cost per 100 lines is cost ÷ changed_lines × 100.

| batch | items | changed lines | reviews | wall | cost | implementing | fixing | Critical/Important/Minor | cost per 100 lines |
|---|---|---|---|---|---|---|---|---|---|
| 58 | 2 | 819 | 1 | 32m53s | 44.66 | 9.54 | 0 | 0/0/2 | 5.45 |
| 59 | 7 | 888 | 2 | 14m47s | 13.27 | 8.44 | 0.38 | 0/0/3 | 1.49 |
| 60 | 7 | 2930 | 2 | 25m23s | 36.60 | 21.19 | 0 | 0/0/6 | 1.25 |
| 61 | 7 | 3191 | 2 | 29m31s | 41.27 | 23.63 | 2.08 | 0/1/8 | 1.29 |
| 62 | 7 | 1438 | 2 | 10h20m (restart) | 33.94 | 11.03 | 0 | 0/1/3 | 2.36 |
| 63 | 7 | 1009 | 2 | 21m42s | 15.77 | 10.79 | 1.02 | 0/1/3 | 1.56 |
| 64 | 7 | 854 | 2 | 10m22s | 10.96 | 7.28 | 0 | 0/2/3 | 1.28 |
| 65 | 3 | 738 | 2 | 14m26s | 10.56 | 6.95 | 0.42 | 0/0/5 | 1.43 |
| 66 | 3 | 547 | 1 | 9m26s | 6.98 | 4.77 | 0 | 0/0/2 | 1.28 |
| 67 | 2 | 771 | 1 | 10m53s | 7.88 | 5.67 | 0 | 0/1/4 | 1.02 |
| 68 | 1 | 730 | 1 | 8m56s | 4.44 | 2.38 | 0 | 0/0/3 | 0.61 |
| 69 | 2 | 873 | 1 | 12m09s | 7.55 | 5.33 | 0 | 0/0/2 | 0.86 |

## Against batches 58-61

- Batches 60 and 61 changed 2930 and 3191 lines, against the review limit of 1000. Batches 65-69, picked under b483's limit, changed 547-873 lines.
- Cost per 100 changed lines: 1.25 and 1.29 for batches 60-61, against 0.61-1.43 for batches 65-69.
- Reviews: batches 59-64 each took 2. Batches 66-69 each took 1.
- Fixing cost: 2.08 in batch 61, against 0-0.42 in batches 64-69.

## Findings and defects

| finding or defect | grade | item | earliest it could have been caught | cited |
|---|---|---|---|---|
| f1: unused import makes `tools check` fail | Important | b367 | the task: `tools check` is not among the checks `work batch done` runs | .shop/batches/62/review-1.md |
| f1: `tools check` with no paths lints files only the base branch changed | Important | b490 | the item's lines: they said "the branch's change" without saying committed or since the fork | .shop/batches/63/review-1.md |
| f1: an item over the review limit skips the readiness bar | Important | b483 | the item's lines: no line set the order of the limit and the bar (batches#r54 says the bar comes first) | .shop/batches/64/review-1.md |
| f1: kinds assertion loosened from == to <= | Minor | b472 | the task: the rule "an existing test changed only in its setup" was broken | .shop/batches/65/review-1.md |

No defects after a merge were recorded for any of the batches (each measurement's defects table).

## Items parked

None in batches 63-69. b471 was parked in batch-62 before the restart, then answered and delivered in batch-65 (.shop/batches/62/plan.md).

## Observations

- Under b483's review limit, batches hold 1-3 items, and each took one review from batch 66 on. (knobs `items`, `reviews` of batches 65-69)
- Cost per 100 changed lines fell from 1.25-1.29 (batches 60-61) to 0.61-0.86 (batches 68-69). (cost, changed_lines)
- Implementing is the largest role in every batch: in batch 69, 5.33 of 7.55. Its cache reads were 12653726, against planning's 2982645. (batch-69 cost by role)
- Batch 62's wall time of 10h20m covers the stopped driver and the restart, not work. (batch-62 totals)
- Two of the four `fix now` findings came from lines that left an order or a scope unsaid (b490, b483).

## Candidates

- Try: run `tools check` in `work batch done`, beside the tests. Rests on: batch 62's f1. It worked if: fewer reviews per batch, and fixing cost stays at 0.
- Try: let the batch-start limit fill a batch to the limit with smaller items instead of stopping at the first that does not fit. Rests on: batches 66-69 holding 1-3 items, each under 1000 lines. It worked if: changed lines per batch nearer 1000, and cost per 100 lines does not rise. This changes a knob, so it would be a design-decision.

## Not counted

- The time `work batch start` takes: the readiness re-check, the lay and, since b488, a scenario run. Each measurement's window starts after the start commit. This is directive-11's target, so it is a request for `measure batch`.
- Batch 62's wall time and cost mix the earlier driver's session with the restart's.
- Whether line estimates under b483 matched the actual changed lines: the estimates are not kept in the measurement.
