---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-92/review-1
kind: review
batch: batch-92
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/115
head: cd82fdcc9969ee9ef687a6376d189a0d0fb5d19a
range: b73163970b33ac328901552dba72d5e0ed16ba1c..cd82fdcc9969ee9ef687a6376d189a0d0fb5d19a
result: clean
---

# batch-92 review 1

## Verdict

The batch builds all three items. b585's four refusals and b589's version refusal match their lines, and b588's chore stays within its files. Nothing needs fixing before the merge; one observation.

## Findings

### f1 Minor observation: every test that runs `work batch merged` now leaves a detached warming running in the shared cache
- item: b588
- where: scripts/batch_close.py:109
`merged` now always calls `batch_warm.start(root)`. That starts a detached interpreter in its own session (`start_new_session=True`), and nothing waits on it. The interpreter compiles grammar 4 for the repository and parses its lines. Through `spec_prefetch` it does this in up to `min(8, cpus // 4)` worker interpreters, and it writes into the cache `$XDG_CACHE_HOME` points to.

Only `tests/scripts/test_batch_opening.py` sets `XDG_CACHE_HOME` to a temporary folder. I grepped `tests/` for `XDG_CACHE_HOME`: no other test that runs `merged` sets it, and neither does any conftest. That covers test_batch_close, the batches scenarios that merge, and test_measure_batch's `merged` template.

The risk is in the suite, not in the product. Under xdist, each of those tests leaves a background compile and prefetch running. It outlives the test, works on a temporary repository that is about to be deleted, and writes into the developer's real cache. That load can make budget-timed tests flaky, such as test_grammar4_guards' parse budget and the tests marked `budget`.

The warmer fails quietly when its repository is gone (`__main__`'s `except Exception`), so the result is wasted CPU, not wrong results.

To reproduce: run `pytest tests/scripts/test_batch_close.py`, then `ps -eo pid,args | grep batch_warm` straight after. Warmers from the finished tests are still running.

Hardening: let the environment switch the warming off, for example with a `$SHOPSYSTEM_NO_WARM` set by the test conftest, and turn it back on in test_batch_opening.
