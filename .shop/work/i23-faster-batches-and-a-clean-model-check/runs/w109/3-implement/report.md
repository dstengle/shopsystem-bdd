# Report of w109 (implement)

## Budget

scripts/supervise.py, scripts/supervise_pool.py (new), scripts/supervise_worker.py, scripts/supervise_merge.py, scripts/supervise_review.py, tests/scenarios/supervision_parallel_steps.py (new), supervision_given.py, supervision_then_workers.py, supervision_world.py, tests/scripts/stub_claude.py, tests/scenarios/test_supervision.py, features/supervision.feature (only `features retire`), CLAUDE.md. 13 files; all touched.

## What changed

- `supervise_pool.py` (new, row added to CLAUDE.md): `Pool.pull` starts a worker thread per movable work-item in queue order up to the workers number; `choose` skips blocked_by items not green (r63) and starts an implementer only if its claim shares no file with a running one (no file set = claims everything); `read_delivery` reads `.shop/delivery.toml` once in `check()` (top-level `workers`, default 4; malformed file or bad `workers` is a Refused before anything changes); merge queue `await_turn`/`release` merges implementers in the order of their end log lines (r61). After a fault no worker starts; running ones end, then the first error is raised.
- `supervise.py`: `run` calls `pull`; `pair`, `together`, `claimed` removed.
- `supervise_worker.py`: `delivery()` returns the one read; `session.json` gets `transcript_path` (found by session id under `$CLAUDE_CONFIG_DIR` or `~/.claude`, `projects/*/<id>.jsonl`); an implementer's end enters the merge queue under the log lock. `supervise_review.py`: same transcript path for the branch review. `supervise_merge.py`: waits its turn before merging.
- Tests: new `supervision_parallel_steps.py`; stub gained `meet_all`, `meet_agents`, `hold`, and a transcript file under `$CLAUDE_CONFIG_DIR`; world's `item_text` takes `blocked_by`; the run env sets `CLAUDE_CONFIG_DIR`.
- Retired with `features retire` the three deprecated scenarios (Retires); removed the two steps only they used (`no worker was started before the one before it had ended`, `the initiative branch has both implementers' commits...`).

## Red and green

Red (start, `python3 -m pytest -q --work-item w109`): 8 failed, 143 passed. Reasons: r59, r60 x2, r62, r20 own worktree, r20 workers number, r61 had an unbound Given/Then (StepDefinitionNotFoundError); r63's Given bound once I wrote it and failed on its Then: `AssertionError: (['shopsystem-bdd:code-scout', 'shopsystem-bdd:bdd-planner', 'shopsystem-bdd:bdd-implementer', 'shopsystem-bdd:bdd-task-reviewer'], '')` (probe D2 confirmed).
I wrote the remaining steps and the pool together after that, not scenario by scenario (a departure from the cycle); the reds above are the observed ones.
Green: `python3 -m pytest -q --work-item w109`: 148 passed, 1 skipped. Also `--whole-suite tests/scenarios/test_supervision.py tests/scripts/test_work_items.py`: 135 passed (before the retired steps' removal, one failed: the retired "no more than two" scenario, as the plan said). Module run three more times: green.

Suite at the start (brief): 681 passed, 8 failed at e8a6dda; the 8 failing were this work-item's.

## Tests changed under an allowance

none (tests removed are those of the three retired scenarios, by Retires).

## Open questions

- No transcript found for a session id: `session.json` is left as claude printed it (no key). Output that is not a JSON object likewise.
- blocked_by naming no work-item, or one in another initiative: counts as not green, never moved; exit code follows existing rules.
- blocked_by cycle: neither moves.
- Order in which free slots are filled: queue order.
- Planned→ready moves take no worker slot.

## Other

The plan contained no code; nothing pasted. Size check (`tools size --limit 300`): no file over. `tools check`: nothing to check.
Concern: the main loop reads the work-items under `self.lock`, which a merge holds during its suite run, so starting new workers waits for a merge. Not verified: `faults` scenarios with stages in flight (their module passes).

Files changed: CLAUDE.md, features/supervision.feature, scripts/supervise.py, supervise_merge.py, supervise_pool.py, supervise_review.py, supervise_worker.py, tests/scenarios/supervision_given.py, supervision_parallel_steps.py, supervision_then_workers.py, supervision_world.py, test_supervision.py, tests/scripts/stub_claude.py.
Commit: 4232bc6.
