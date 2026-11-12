---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-12-suite-speed
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-12
---

# The test suite's slow tests and how to speed them up

## Question

The person, 2026-11-12: go through every test over 1 s and look for optimizations. Measured on main at f788e9e35
(plugin 0.34.1), `python3 -m pytest -q -n 8` with warm grammar caches: 2077 passed in 60.6 s wall.

## Where the time goes

- 88 test phases take over 1 s: 223 worker-seconds, 131 of them in fixture setup and 92 in test calls.
- Subprocesses are almost all of it: 12,381 `subprocess.run` calls from the test processes, 422 of the ~480
  worker-seconds. Of those, 2,099 are runs of the plugin's own tools (400 s); 10,282 are `git` (22 s).
- `work batch ...`: 723 runs, 198 s; `work line` 125 (18 s); `model check` 141 (18 s); `features generate` 71 (12 s);
  every other command under 12 s.
- Start-up cost of a bare `--help`: `work` 165 ms, `features` 107 ms, `model` 75 ms, `migrate` 56 ms, `measure` 52 ms,
  `tools` 36 ms; a bare `python3 -c pass` is 12 ms. `work` imports every command module eagerly (`backlog_cli` 56 ms,
  `batch_cli` 61 ms cumulative), and `spec_unbuilt` imports pytest (43 ms) for its xfail mark, which no `work`
  command uses.

By file (phases over 1 s): test_batch_fix_loop 33.8 s (15), test_measure_batch 33.6 s (10), test_batch_reviewed
30.4 s (14), test_measure_defect 23.1 s (7), test_requests 20.7 s (1), test_batch_brief 14.6 s (12),
test_corpus_spec 10.3 s (1), test_bound 9.2 s (2), test_migrate_upgrade_codified 6.3 s (2), test_request_flow 6.0 s
(3), test_batch_close 5.8 s (5), test_retirement 4.1 s (1), then 13 more between 1 and 4 s.

## Findings and proposed changes, largest first

1. **`work`'s start-up (about 100 ms of 165 ms a run, ~1,450 runs: ~145 worker-s, ~18 s wall).** Import each
   command's module in its dispatch, not at the top of `scripts/work` and `backlog_cli`/`batch_cli`; move
   `spec_unbuilt`'s `import pytest` into the function that makes the mark. The same for `features` (107 ms) and
   `model`'s `model_check` (32 ms). Also speeds every real session's `work` call and the SessionStart hooks.
2. **`work batch brief` runs the default `[review] checks` twice (0.76 s of its 0.94 s).** `batch_repo`'s
   `delivery.toml` gives no `[review] checks`, so every brief in the batch, fix-loop and measure tests runs
   `tools size`, `tools check`, `features generate --check`, `features bindings --unbound` and
   `model decisions --check` on the head and on a base worktree. `batch_repo` should set `[review] checks = []`
   (or one cheap command); the tests of the runs (test_batch_brief) set their own.
3. **Each measure, fix-loop and reviewed test builds a published batch from nothing (2.4-3.6 s of setup each, ~45
   tests).** `review_testing.published` and test_measure_batch's `merged` run start, resume, done, review, brief,
   reviewed and merged per test. Build each state once per worker (a session-scoped template under
   `tmp_path_factory`) and copy the repository and its `outside` directory per test, resetting the origin URL and
   the stand-in gh's env to the copy (`batch merged` removes the worktrees, so the merged state copies cleanly; the
   published state's worktrees need `git worktree repair` after the copy, or the template stops before them).
4. **test_requests' `work watch --forward` waits its full `--every 20` under load (20.7 s; 1.3 s alone).** The
   stand-in's `webhook forward` (tests/scripts/stub_gh.py `forward`) waits for an `issue list` call after its own
   start, counted as `len(calls())` once its Python is up; under load the watch's start-of-watch `issue list` is
   written first, so the forward never sees it and the watch wakes only at its timeout. Count from the forward's
   own call line minus any `issue list` lines the watch wrote since it spawned the forward (or from the last
   `extension list` line), and the test takes ~1.3 s at any load. This also removes a timing dependence.
5. **test_corpus_spec builds the lexicon 343 times (13 of its 18 profiled seconds).** `reading()` makes a new
   `spec_context.Four(root)` per corpus line; each reads every layer's lexicon again. Make one `Four` per root in
   `faults()`. Separately, `spec_lexicon._fields` builds its regex with `re.escape(name)` on each of ~2 million
   calls (re's cache lookup alone 1.75 s profiled): compile one pattern per field name once (a dict or
   `functools.cache`), which speeds every `model` and `work` command that reads a lexicon.
6. **test_bound (5.2 s, 4.0 s) and test_retirement (4.1 s)** are whole-repository checks (`features bindings`,
   `features vocab --check`, `--help` of every `work` command); they shrink with finding 1 and need nothing of
   their own.

## Expected effect

Findings 1-3 together cut about half the suite's worker time; with finding 4 removing a 20 s straggler, the wall
time should fall from about 60 s to 30-35 s on 8 workers. Each is independent and can land alone; 1 and 5 also make
the tools faster for sessions. Not measured: a cold run (fresh checkout, grammar compiled and parse cache empty).
