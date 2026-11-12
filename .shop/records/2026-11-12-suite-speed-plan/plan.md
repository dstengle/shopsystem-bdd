# Speed up the test suite (b265) Plan

**Goal:** the suite (`python3 -m pytest -q -n 8`, warm caches) from about 60 s to 30-35 s wall, with no test
weakened, by the five changes of the analysis `.shop/records/2026-11-12-suite-speed.md` (the person, 2026-11-12:
"Can we get these implemented?").

**Branch:** `plan-suite-speed` from `origin/main`, worktree `.shop/worktrees/plan-suite-speed`; one implementer doing
the sections in order, each its own commit with its measured effect, then one fresh reviewer of the whole branch.

## 0. The baseline

Before any change: the suite's wall time and `--durations=0 --durations-min=1.0`, kept for the comparison in the
last commit's message.

## 1. `work` starts lazily

`scripts/work` and the CLI modules it dispatches to (`backlog_cli`, `batch_cli`, `request_cli`, `conversation_cli`
and the others) import a command's implementing modules only when that command runs; the parsers stay complete
(every `--help` the same, test_retirement and test_docs_truth green). `spec_unbuilt` imports pytest inside the
function that makes the xfail mark. The same for `scripts/features` and `scripts/model` where a module is only one
command's. Target: `work --help` under 70 ms (was 165 ms), measured with `python3 -X importtime`. The hooks
(`conversation_hook`, `request_hook`) already avoid `work`; leave them. Keep the import-linter contracts
(`tools check`) green; a function-level import is acceptable where the module map row says why only if a comment is
needed for a cycle, otherwise none.

## 2. No default review checks in the batch test repository

`tests/scripts/conftest.py`'s `batch_repo` writes `[review] checks = []` beside `[batch] tests`; each test that
reads the brief's runs (test_batch_brief and any other that asserts on a check's output or exit code) sets the
checks it needs. Confirm every test that relied on the defaults still asserts what it did.

## 3. Template batch repositories

`review_testing.published` and test_measure_batch's / test_measure_defect's `merged` build their state once per
worker (session-scoped, under `tmp_path_factory`, keyed by its arguments such as `park`) and copy it per test:
the repository and its `outside` directory (bare origin, stand-in gh files) copied to the test's own tmp dirs, the
origin URL reset (`git remote set-url`), the stand-in gh's env pointed at the copy, and any worktree paths
repaired (`git worktree repair`) or the template taken before worktrees exist. Every path a test reads (the
repository, scratch, outside) is the copy's. A test that mutates state gets its own copy; the template is never
written by a test. Use `shutil.copytree(..., symlinks=True)`; never chain `cp` and `rm` in one shell command.

## 4. The forward stand-in's race

`tests/scripts/stub_gh.py`'s `forward`: an `issue list` the watch wrote after it spawned the forward counts even
when it was written before the forward's own Python started (count from the last `extension list` line, which the
watch writes before it spawns the forward, or an equivalent that holds at any load). test_requests'
`work watch --forward wakes on a new ask` then takes about 1-2 s under `-n 8`; the other watch tests stay green.

## 5. One lexicon per corpus run; a compiled `_fields`

test_corpus_spec's `faults` makes one `spec_context.Four(root)` and passes it to `reading`. `spec_lexicon._fields`
compiles its pattern once per field name (a module-level cache). Measure test_corpus_spec alone before and after.

## 6. The gate

The suite twice under `-n 8` (no new flakiness), `-m timing -n 0`, `model check`, `model logic`,
`features generate --check`, `features vocab --check`, `model rules --check`, `model constructs --check`,
`tools size --limit 300`, `tools check`; the module map in CLAUDE.md updated where a row's concern changes (e.g.
`review_testing.py`'s templates). The last commit's message gives the before and after wall times and the slowest
remaining tests.
