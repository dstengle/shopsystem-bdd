---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-86/review-1
kind: review
batch: batch-86
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/109
head: 9786637ce3304fa19bcb54d1d550bd81d5524661
range: 5cfe8edb82dbcd7b2b1ac69ac2270834c1e06c46..9786637ce3304fa19bcb54d1d550bd81d5524661
result: clean
---

# batch-86 review 1

## Verdict

The batch builds all three items: b574's chore, b579's r41 and r42, and b580's r102 and r103. Every run exits 0. The change is 597 lines against a limit of 1000. I found nothing to fix now. There are two observations on b580's summary and one on b574's calibration.

## Findings

### f1 Minor observation: the batch summary states $0.00 and 0 tokens when no transcript was found
- item: b580
- where: scripts/batch_summary.py:407
`batch_summary`'s docstring says "a figure no record gives is written `unknown`". `values` writes `unknown` only when `figures["cost"]` or a token count is None. `measure_batch.figures_of` never gives None for these. With no session directory, `measure_batch_read.requests_of` returns `[]` (measure_batch_read.py:51). Then `cost = round(sum(... for s in sessions), 6)` is `0` and each token kind sums to `0` (measure_batch.py:126, 134).

So `work batch merged`, run where Claude Code's store has no sessions for the root, prints:
```
- cost: $0.00
- output tokens: 0
```
It should print `unknown` for these figures.

I checked how real use reaches this. `work batch merged` is normally run from the checkout the batch was started in, and its project directory then holds the sessions. So the zeros appear only when the store is missing or empty, for example on CI or on another machine. No line names that case.

Suggested fix: when `figures["sessions_found"]` is 0 or `figures["sessions"]` is empty, write cost and tokens as `unknown`.

### f2 Minor observation: an exception other than transcripts' Refused from the summary fails `work batch merged` after the merge is recorded
- item: b580
- where: scripts/batch_summary.py:426
`merged` catches only `transcripts.Refused`. `batch_cli.merged` prints the summary after `batch_close.merged` has already delivered the items and committed the batch `merged`. Any other exception would print a traceback and exit non-zero, even though the merge is done. Examples are an `OSError` while reading the store, or a `ValueError` from `datetime.fromisoformat` in `_between`.

I checked what is caught today. `figures_of` turns `shop_files.Refused` into transcripts' `Refused` (measure_batch.py:95). Nothing else is caught.

This is hardening: no line names the case. Suggested fix: catch `Exception` around `figures_of` in `merged`, and print every figure `unknown` with the reason, as the `Refused` branch already does.

### f3 Minor observation: the reference's quiet time is a constant that no test pins
- item: b574
- where: tests/scripts/cpu_budget.py:25
`QUIET = 0.35` is said to be "median of ten runs alone", but nothing checks it. The 5 s budget becomes a ratio of 5 / QUIET ≈ 14.3 references. If the workload (2,000,000 dict and format iterations) takes longer than 0.35 s on a quiet machine, the live-repo check is looser than 5 s by the same factor. If it takes less, the check is tighter.

`test_cpu_budget.py` checks that the ratios behave (about one reference, about two references). It does not check that the reference's measured quiet time is near `QUIET`. A loosened ceiling would therefore pass unseen. I could not measure the workload here.

Suggested fix: a test, marked `budget`, that runs the reference alone and asserts that its CPU time is within a loose band of `QUIET`. An alternative is to record the calibration machine and how it was run in a comment.
