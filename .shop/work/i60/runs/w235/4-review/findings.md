# Review of w235: `work delegate` and the UserPromptSubmit hook (r65–r68, r70–r72)

**Verdict: DONE.** No Critical finding and no fix-now finding. Two Minor findings, both triaged drop.

## Commits reviewed

From the brief's `Commits:`, oldest first. They match the implementer's `result.json`.
- `ed25c279` work delegate: write, replace and commit a request's delegation (r65-r71)
  - scripts/work, scripts/workqueue_request.py, tests/scenarios/requests_steps.py, tests/scenarios/requests_write_steps.py
- `ab71c3fc` UserPromptSubmit hook tells a session to write a delegation with work delegate (r72)
  - CLAUDE.md, README.md, hooks/hooks.json, scripts/migrate, scripts/migrate_prompt.py (new), tests/scenarios/requests_session_steps.py (new), tests/scenarios/test_requests.py

Every file is in the plan's file set. Nothing under `features/` changed.

Suite, from the brief's record: 1080 passed, 0 failed at ab71c3fc. The expected failures listed there are other work-items' scenarios. None of them is a w235 delegate scenario.

## Removed and weakened tests

None.

I searched the diff for:
- removed `def test_` or step functions;
- removed or changed `assert` lines;
- parametrize or Examples changes;
- added `skip` or `xfail`.

The only change to an existing function is `requests_steps.py::the_upstream_runs`. It gains a `delegate` branch, and resolve's `version` branch is unchanged under `elif`. It is a step, and the plan's §4 lists it. Every other test change is an addition.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing assertion changed.

## Cannot verify

- **That a real Claude session follows the hook's text in the same reply (r72).** The scenario uses a session double. The double acts when the hook's stdout contains `work delegate`, `same reply` and the form `The person, <date>: "<the person`, and the scenario then checks the command the double ran. This is the plan's Decision 6, on the precedent of supervision r120. Whether a live model obeys can only be watched, not tested. This review session's own prompt hook printed the text as intended.
- **The harness runs `UserPromptSubmit` hooks from `hooks/hooks.json` with the cwd in the repository.** This is assumed as for SessionStart and PreCompact.

## Findings

### 1. Minor (drop): the hook never reads its stdin

- **Where:** scripts/migrate_prompt.py:31-36 (`run`).
- **What:** the hook ignores the prompt JSON the harness writes to its stdin. The plan (Decision 5) said it "reads the harness's prompt JSON on stdin". The output does not depend on the prompt, so behaviour is unaffected. The scenario passes input and the run exits 0.
- **Why it matters:** only if a harness blocked on an unread pipe, which does not happen for prompt-sized input.
- **Fix:** `sys.stdin.read()` guarded by try/except, or note the deviation from the plan.

### 2. Minor (drop): the hook text goes out on every prompt and lists every open request

- **Where:** scripts/migrate_prompt.py:24-28.
- **What:** in a repository with many open requests (this one has 25), every prompt carries the same paragraph.
- **Why it matters:** context cost only. The text is correct and serves r72 (the plan's Decision 5 keys it on open requests).
- **Fix:** none needed now.

### Risks checked, no finding

- **A behaviour no line asks for.**
  - `delegate` refuses only empty text and delivered/refused/withdrawn requests (r67, r68). An unknown request is refused by `path_of`, as every request command is.
  - There is no turn check (r70), and status and turn are untouched (r71). The edit rewrites only `delegation`.
  - The commit goes through `_change`, so through `workqueue.committed` (r66).
  - The hook's output and its exit 0 serve r72. Exit 0 is mechanism, the same as `compacting`.
- **Whitespace-only text.** It is refused as empty (`text.strip()`). That is a reading of r67's "empty", consistent with the request command's `--delegation` handling.
- **Newlines or quotes in the delegation.** `json.dumps` keeps the value on one frontmatter line, and `supervise_answers.delegation` decodes the JSON form.
- **Insert when absent.** The line is placed before the closing `\n---` of the frontmatter, the same boundary that `_with_field` and `field` use.
- **The hook on unreadable request files.** `workqueue.requests` raises only `Refused` (non-UTF-8), which is caught. The `model_parse.frontmatter` parser is lenient (it returns `{}` on a malformed head), so the hook keeps exit 0.
- **Size.** `migrate_prompt.py` is 36 lines, and `tools size --limit 300` prints nothing.

## Commands run

- `git log --stat ed25c279~1..ab71c3fc`, then `git diff ed25c279~1 ab71c3fc`
- `grep` over spec/capabilities/requests.md (r65–r72, rests_on, Implementation) and features/requests.feature (`delegat`)
- `grep` for `_change`, `field`, `_with_field`, `path_of` in scripts/workqueue_request.py, and for `requests` and `read` in scripts/workqueue.py and model_parse.frontmatter
- `grep` for `"written"` in tests/scenarios (the "nothing changes" Then reads it)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base ae85edd3`:
  - **ruff:** 8 errors, none in w235's files (.shop/.../splice.py, tests/scenarios/test_supervision.py:14, tests/scenarios/work_queue_list_steps.py:134; all outside these commits);
  - **vulture:** clean;
  - **import-linter:** no contracts stated.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output, so no file is over the limit.
