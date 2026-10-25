# CLAUDE.md

## Size limit

Code and test files, every tracked Python file, stay at 300 lines or fewer. `python3 scripts/tools size --limit 300` prints each one over it with its line count and exits 1 when there is any. A change does not push a file over the limit; a file that is over it already is split by the work that names it.

## Module map

| Module | Concern |
|---|---|
| `scripts/tools` | the `tools` command: its contract and argument parsing |
| `scripts/tools_env.py` | the project's interpreter, `probe` and `install` |
| `scripts/tools_map.py` | the coverage map: `map`, `tests-of`, `untested` |
| `scripts/tools_refs.py` | `refs` |
| `scripts/tools_check.py` | `check`: ruff, vulture, import-linter |
| `scripts/tools_size.py` | `size`: tracked Python files over a line limit |
| `scripts/features*.py` | the `features` command: Gherkin reading, editing, bindings, reports |
| `scripts/migrate_session.py` | the hooks' text about initiatives: `work status` at SessionStart, `migrate compacting` at PreCompact |
| `scripts/model*.py` | the `model` command: parsing, facts, checks, work, reports |
| `scripts/model_requests.py` | the reading of requests by `model`: `.shop/work/requests/q<n>.md` |
| `scripts/work` with `scripts/workqueue.py` | the `work` command: the work-item queue, its statuses and log |
| `scripts/workqueue_answer.py` | `work answer` |
| `scripts/workqueue_status.py` | `work status` |
| `scripts/workqueue_note.py` | `work note` |
| `scripts/workqueue_start.py` | `work start`: the initiative an accepted request begins |
| `scripts/workqueue_done.py` | an initiative done: the condition and the rewrite `work withdraw` and `work resolve` commit |
| `scripts/workqueue_request.py` | the requests of a context: `work request`, `outcome`, `turn`, `resolve` |
| `scripts/supervise*.py` | `work run`: briefs, workers, the pool of workers side by side (`supervise_pool.py`), merging, faults, the branch review, a capability-proposal's apply and formulate rounds (`supervise_rounds.py`) |
| `scripts/supervise_analysis.py` | `work run`'s measure of a finished initiative (`measure initiative`) and the analysis session that follows it |
| `scripts/supervise_draft.py` | `work run`'s drafting: the work-items of a formulated capability-proposal and of a branch review's fix-now findings |
| `scripts/work_items.py` | the pytest plugin of `--work-item`, loaded by `work run`'s tests and this repository's conftest |
| `scripts/measure` with `scripts/measure_*.py` | the `measure` command: `initiative` (reading `measure_read.py`, figures `measure_build.py`, the record `measure_write.py`) and `show`, `compare` (`measure_show.py`) |
| `scripts/migrate*.py` | the `migrate` command |
| `scripts/migrate_upgrade*.py` | `migrate status` and `migrate upgrade`: the upgrade steps between plugin releases, one module a step |
| `hooks/hooks.json` | the plugin's SessionStart hook, running `migrate status --hook` |
| `tests/scenarios/` | step definitions, one `<capability>_*_steps.py` module a concern |
| `tests/scripts/` | tests of the scripts that no scenario drives |

A new concern gets a new module and a row here.
