# Review of w132: model check's request rules v16a, v_d1, v17, v3, v18, v_d3

**Verdict: DONE.** There is nothing Critical and nothing to fix now. The change does what r113–r117 and r119 say, the way the plan says to. It touches nothing under `features/`, removes or weakens no test, and puts no file over the size limit. There are three Minor findings, all triaged drop.

## Commits reviewed

The branch `work/w132` is gone, so I took the commits on the checked-out HEAD between `92e8889 work: w132 ready -> claimed` and `5240195 work: w132 claimed -> done`, leaving out `work run`'s own `work:` commits (dcecb35 for w137, 51322b8 and 527e373 for w127):

- `1303b55 model check: request rules v16a, v_d1, v_d3, v17, v3, v18`. It changes 6 files, +195/−17, which are the six files in the work-item's fileset and the report's Budget.

The implementer's result lists `437dc1c` instead. `git diff 437dc1c 1303b55` differs only in `.shop/work/…` run and log files of w127 and w137, so 1303b55 is 437dc1c replayed onto later queue commits, with the same code and test change. This is Minor finding 3.

## Removed and weakened tests

None.

What I searched for in the diff of `tests/`: removed `def test_`/step functions, removed or changed `assert` lines, dropped parametrize cases or Examples rows, and added `skip`/`xfail`.

- The existing Then steps in `design_model_check_then.py` are untouched. Two steps are added: `request_rule_names` and `once_done_not_named`.
- `request_text` in `design_model_check_requests.py` gained keyword arguments, each with a default (`links`, `resolution`, `status`, `path`).
  - Called with no arguments, it builds the same file as before: `"request/%s/%s" % (path, name)` with `path=PATH` equals `full("request", name)`, and the defaults are still the obs-1 source and `status: open`.
  - Its callers in `design_model_check_reading.py:107` and `design_model_check_requests.py:42,48` are unchanged.
  - `work_queue_start_steps.py` has its own, unrelated `request_text`.

The plan's "Tests the decisions break" says none, and none broke.

## Allowances

The report's `## Tests changed under an allowance` is "none". There are no rows to verify, and the commits change no existing test.

## Cannot verify

- **This repository's own `model check`.** The plan's open case says it now reports v16a for i24 (dated 2026-10-24, no `fulfils`). It may also report v17 or v18 on the repository's own requests. I could not run `python3 scripts/model check` here, because the review shell refused the command.
- **The report's figure of 752 passed, 15 failed at start.** It comes from the brief's record and was not rerun. Per my instructions the whole suite is `work run`'s to run.

## Findings

### 1. Minor: stray whitespace edit, `scripts/model_facts.py:30` (w132). Triage: drop

- **What is wrong:** `CONTEXT_PATH = rf"…"` became `CONTEXT_PATH =rf"…"`. No line or plan step asks for this edit.
- **Why it matters:** it changes no behaviour, but it is noise in the diff and against PEP 8 (E225). Ruff, as configured, does not flag it.
- **Fix:** restore the space the next time the file is touched.

### 2. Minor: ruff FURB167, `tests/scenarios/design_model_check_requests.py:132` (w132). Triage: drop

- **What is wrong:** `nothing_has_the_id` uses the alias `re.M`, which ruff reports as FURB167. `tools check` reports it against this commit.
- **Fix:** write `re.MULTILINE` instead, a one-word change.

### 3. Minor: the result's commit id is not the commit on the branch (w132). Triage: drop

- **What is wrong:** `3-implement/result.json` lists `437dc1c`, but the commit in history is `1303b55`.
- **Why it doesn't matter:** I verified that the two carry the same change to the six files (see "Commits reviewed").

### Risks I named and verified (no finding)

- **v_d1's "this context".** `own_asker` accepts `internal` or an asker that is a `bounded-context` node. Only `model_facts.py:145` creates such a node, and it is the context's own id. A request from another context therefore never counts, and the "another context" Example in the feature checks exactly that.
- **v16a's date comparison.** It compares strings (`D > "2026-10-23"`). The `date` fact is emitted only after `date.fromisoformat` succeeds, so the date is always ISO `YYYY-MM-DD` and the string order is the date order.
- **v3's requirement kind.** v3 tests for node kind `capability-requirement`, which is the kind `model_facts.py:226` gives requirements.
- **v3's label.** v3 keeps a single label, so RulesTest still holds. The old `needs` rule it replaces had no line under r116's code. No test outside the two step files names v3, v_d1, v16a, v17, v18 or v_d3 (by grep over `tests/`).
- **v18 fires only on another context's id.** `foreign()` needs a head in WORK_KINDS, a full `<context path>/<name>`, and a path other than this one, so an id of this context never fires it. It runs only when `self.path` is set.
- **A request's links go under request-only relations.** `req_part_of` and `req_source` carry them, so a request still fires none of v_k3, v_k5, v_d2, v9e or v10a (plan decision 3).

### Code no line asks for

None. Each new fact serves one of the accepted lines:

- `asker`, `req_part_of` and `req_source` serve r114 and r115;
- `resolution` serves r116;
- `fulfils` serves r113 and r119;
- `date` serves r113;
- `foreign` serves r117.

### Checks

- **`tools check --base 92e8889`:**
  - ruff: 3 issues, one of them w132's (finding 2). The other two, `scripts/workqueue.py:232` I001 and `tests/scenarios/test_work_queue.py:7` I001, are in files w132 did not touch.
  - vulture: 1 issue, `tests/scenarios/work_queue_status_steps.py:77`, in a file w132 did not touch.
  - import-linter: the project states no import contracts.
- **`tools size --limit 300`:** nothing printed. The touched files are now 287 (`model_facts.py`), 219 (`model_work.py`), 63 (`model_requests.py`), 132 (`design_model_check_requests.py`) and 255 (`design_model_check_then.py`) lines.
- **`pytest -q -n 0 --work-item w132`:** 157 passed, 1 skipped.

## Commands run

- `git log --format='%H %s' --grep="^work: w132 "`
- `git log --oneline -15`
- `git log --format='%H %s' 92e8889..5240195`
- `git show --stat 1303b55`
- `git cat-file -t 437dc1c`
- `git diff 437dc1c 1303b55 --stat`
- `git show 1303b55`
- greps over `scripts/model*.py`, `scripts/model.lp`, `tests/`, `features/design-model-check.feature`, `spec/capabilities/design-model-check.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 92e88890731062e7b05d22604ebcfde846c6bf26`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` of the touched files
- `python3 -m pytest -q -n 0 --work-item w132 -p no:cacheprovider`
- `python3 scripts/model check --json`, which the review shell refused
