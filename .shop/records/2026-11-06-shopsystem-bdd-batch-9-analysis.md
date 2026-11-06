---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-06-shopsystem-bdd-batch-9-analysis
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-06
---

# shopsystem-bdd, batch-9: analysis

Plugin 2.2.0 (released as 2.3.0 after the merge). 2026-11-06T14:38:14Z to 2026-11-06T17:21:39Z. Measurement: .shop/records/measurements/2026-11-06-batch-9.md. Compared with: .shop/records/measurements/2026-11-06-batch-8.md.

The person asked where the time went, and whether the test suite is a measurable share of it.

## The delivery

```
totals
total             | value
------------------+------------------------------
wall time         | 2 hours 43 minutes 25 seconds
session time      | 1 hour 8 minutes 47 seconds
waiting for merge | 15 minutes 35 seconds
output tokens     | 170957
new input tokens  | 987380
cache-read tokens | 23975370
cost              | 13.41

cost by role
role         | sessions | session time          | output tokens | new input tokens | cache-read tokens | cost
-------------+----------+-----------------------+---------------+------------------+-------------------+-----
planning     | 2        | 23 minutes 58 seconds | 44133         | 144014           | 7395443           | 3.34
implementing | 4        | 28 minutes 8 seconds  | 62311         | 345595           | 10432535          | 5.06
review       | 4        | 4 minutes             | 24697         | 267455           | 1831798           | 2.20
fixing       | 4        | 12 minutes 41 seconds | 39816         | 230316           | 4315594           | 2.81

review findings by grade
grade     | findings
----------+---------
Critical  | 0
Important | 2
Minor     | 6

defects
item     | review | after merge
---------+--------+------------
b30      | 1      | 0
b36      | 2      | 0
per item | 0.75   |

knobs
knob          | value
--------------+-----------
batch_size    | 4
items         | 4
changed_lines | 775
size_limit    | 1000
reviews       | 4
readiness_bar | mechanical
```

## Against batch-8

```
total              | batch-8               | batch-9                       | ratio
-------------------+-----------------------+-------------------------------+------
wall time          | 40 minutes 38 seconds | 2 hours 43 minutes 25 seconds | 4.02
session time       | 37 minutes 23 seconds | 1 hour 8 minutes 47 seconds   | 1.84
output tokens      | 94248                 | 170957                        | 1.81
new input tokens   | 396486                | 987380                        | 2.49
cache-read tokens  | 16614149              | 23975370                      | 1.44
cost               | 7.25                  | 13.41                         | 1.85
defects per item   | 1.00                  | 0.75                          | 0.75
planning cost      | 3.11                  | 3.34                          | 1.07
implementing cost  | 2.24                  | 5.06                          | 2.26
review cost        | 0.78                  | 2.20                          | 2.82
fixing cost        | 1.12                  | 2.81                          | 2.51
Critical findings  | 0                     | 0                             | -
Important findings | 2                     | 2                             | 1
Minor findings     | 5                     | 6                             | 1.2
items              | 2                     | 4                             | 2
changed lines      | 326                   | 775                           | 2.38
reviews            | 3                     | 4                             | 1.33
```

Batch-9 had twice the items and 2.38 times the changed lines of batch-8, and cost 1.85 times as much.

## Findings and defects

| finding or defect | grade | item | earliest it could have been caught | cited |
|---|---|---|---|---|
| f1 `work turn` posts with no commit before it when the turn leaves the record unchanged | Important | b36 | The item's lines. r46's scenario starts from a request with no settled outcome, so it never reaches the unchanged turn of r36 | .shop/batches/9/review-1.md:19; spec/capabilities/requests.md:180 |
| f2 `tools check` fails at the head (ruff I001) | Minor | b30 | The task. `work batch done` runs the tests but not `tools check`, so the lint error first surfaced in the review | .shop/batches/9/review-1.md:35 |
| f6 a post GitHub accepted is left in place, and a retry posts it again, when the commit recording its URL fails | Important | b36 | Review 1. It raised the same fault for the issue as f5 and triaged it observation, not fix now. The person raised it on the pull request after review 2 was clean | .shop/batches/9/review-1.md:58; .shop/batches/9/review-3.md:19 |

No defect after the merge is recorded.

## Items parked

none

## Observations

- Batch-9 was `awaiting-merge` with a clean review from 14:57:12 to 16:58:12. That is 7260 s (2 h 1 min), 74% of the wall time of 9805 s. (`git log .shop/batches/9/`: commits 1b4aef0c and 3ec9acf7; measurement `wall_time_seconds`)
- That gap is not under waiting for merge, which counts only the 935 s from the last `built` (17:06:04) to `closed` (17:21:39). The batch went back to review by hand (3ec9acf7), so the measurement counts the first wait as building time. (measurement `window`, `waiting_for_merge_seconds`)
- Without the gap, the wall time is 9805 − 7260 = 2545 s (42 min 25 s), next to batch-8's 40 min 38 s for half the items. (measurement `wall_time_seconds`; comparison `wall time`)
- The four tasks were built and `done` 9 min 55 s after the start (14:38:14 to 14:48:09). The first review was clean of everything to fix 19 min after the start (14:57:12). (`git log .shop/batches/9/`)
- Implementing was the largest cost, 5.06 of 13.41, and the largest session time, 28 min 8 s. (cost by role)
- Fixing cost 2.81 over 4 sessions. The person's finding f6 accounts for 2.18 of it (1.20 + 0.98), and the two review-1 fixes for 0.62 (0.40 + 0.22). (sessions table)
- Two of the three fix-now findings were on b36, whose lines r45-r47 cover only an uncommittable repository before a post. Neither caught a commit that fails after a post GitHub accepted. (.shop/batches/9/review-1.md:19, review-3.md:19; spec/capabilities/requests.md:177-183)

## Candidates

- Try: a person's comment on a clean pull request reopens the batch by command (b69), so the time awaiting merge is counted as waiting, not building. Rests on: the 7260 s gap counted as building time. It worked if: `wall_time_seconds` minus `waiting_for_merge_seconds` falls to the session-driven span (here 2545 s), with the wait under waiting for merge.
- Try: a finding where GitHub and the record can come out of step is graded fix now in a review, not left as an observation. Rests on: f5 in review 1 being the fault the person later raised as f6. It worked if: the fix-now findings raised after a clean review (here 1) fall to 0, and so does the fixing cost spent after one (here 2.18).
- Try: `work batch done` runs `tools check` as well as the tests. Rests on: f2, a lint error first found by the review. It worked if: the Minor fix-now findings that are lint (here 1) fall to 0, and with them a review round.

## Not counted

- **The test suite's share of the time:** the measurement doesn't count it. It sums the agents' session time and tokens, but not how long a command's test run took inside it. Outside the measurement, the whole suite on `main` after the merge took 26.82 s for 1383 tests (`-n auto`). In batch-9, `work batch done` ran it once per task (4) and `work batch review` ran it once per round (3). At about 27 s a run, that is roughly 7 × 27 = 189 s, against a session time of 4127 s. This is an estimate, not a measured figure: an agent's own pytest runs while it built each scenario are not counted either. Counting the test runs of `done` and `review` would be a request for `measure batch`.
- No transcript was read, and the requests were all priced (`unpriced: {}`).
