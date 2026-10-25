# Research notes: w148 (work-queue r7, `work request --lines` missing file)

Search note: `tools map` has no map, so `tests-of` and `untested` answer nothing here. Test lists below are `by search`.
`tools refs` ran on `request` and found the definition and two measure callers only; the rest is `by search`.
Scratch: `.shop/scratch/w148-1-research/` (probe_work.py, probe_split.py, probe_dir.py). Ignored by git; `git status` clean.
Run note: the `--work-item w148` plugin filters collection; `test_requests.py` then refuses to collect. Probes ran with `-n 0`.

## 1. Why each scenario is red today

Command: `python3 -m pytest -q --tb=short tests/scenarios/test_work_queue.py` (run: 13 selected, 12 passed, 1 failed).

- `request ... --lines lines.md` missing file (features/work-queue.feature:190): RED. Undefined step
  `Given an upstream that keeps no request` (StepDefinitionNotFoundError). The step exists in
  `tests/scenarios/requests_write_steps.py:26` but only `test_requests.py` imports it. The next Given,
  `Given no file lines.md`, is also undefined (grep of tests: no definition). Once those are bound, the Then
  `work says that the file lines.md does not exist` needs that exact text in stderr. Code behind it:
  `scripts/workqueue_request.py:request`, line 68, reads the lines file with `workqueue.read(Path(lines_file), ...)`
  and nothing checks that the file exists. `workqueue.read` (`scripts/workqueue.py:50`) catches only
  UnicodeDecodeError, so FileNotFoundError escapes `scripts/work:main` (it catches only `Refused`) as a traceback.
- The other 7 scenarios (12 selected tests) are GREEN by run: r7 outline (4 examples), transition of a missing
  work-item, add outline (`../../spec`), add newline, show non-UTF-8, lacks outline (2), log fault outline (2).

## 2. What the system answers today

Probes (run, `python3 -m pytest -q -s -n 0 .shop/scratch/w148-1-research/probe_*.py`). Each repository is a git repo on main
with spec/index.md; `WORK` is the worktree's `scripts/work`.

Request (`probe_work.py`):
- `request "Show the queue" --from ctx-a --lines lines.md --source o1`, lines.md absent (the scenario's When): rc 1,
  stderr ends `FileNotFoundError: [Errno 2] No such file or directory: 'lines.md'`, git status clean. Traceback.
- same, `--lines` names a directory: rc 1, `IsADirectoryError: [Errno 21] Is a directory: 'lines.md'`. Traceback.
- same, lines.md not UTF-8 bytes: rc 1, `work: lines.md is not UTF-8 text`. Refused, nothing written. Note the name:
  `read` names the file relative to its parent, so `--lines sub/lines.md` would be named `lines.md` (read).
- lines absent and no `--source`: rc 1, `work: the request names neither an origin (--source) nor a job-thread (--thread)`.
  The source check runs before the lines read.
- lines absent, repository not a git repo: rc 1, the same FileNotFoundError traceback. The lines read comes before
  `committed`'s git check.

Add, show, withdraw (`probe_work.py`, `probe_split.py`, `probe_dir.py`):
- `add ""`, `add i1/../x`, `add ..`, `add ../../spec`: rc 1, `work: the initiative <x> is not a name`. Refused, clean.
- `add i9 ...` (no such initiative): rc 1, `work: the initiative i9 does not exist (no .shop/work/i9)`. Clean.
- `add i1 ... --part-of "p<LF>status: ready"`: rc 1, newline refusal. Clean.
- `add ... --part-of "p<CR>status: ready"`: rc 1, newline refusal. Clean.
- `add` with U+000B, U+000C, U+0085, U+2028, U+2029 in `--part-of`: ACCEPTED (rc 0, `w1`). See D7.
- `add` with a directory named `i1/w9.md`: rc 1, `IsADirectoryError` traceback from `highest`. See D5.
- `add` while `i1/w2.md` is not UTF-8: rc 1, `work: .shop/work/i1/w2.md is not UTF-8 text`. Clean.
- `show` with `i1/w2.md` not UTF-8: rc 1, `work: .shop/work/i1/w2.md is not UTF-8 text`, stdout `i1/w1 drafted`. Clean.
- `show` with a directory named `i1/w1.md`: rc 1, IsADirectoryError traceback. See D4.
- `withdraw w9` (absent): rc 1, `work: there is no work-item w9 under .shop/work`. Clean.
- `withdraw w1` with `log.jsonl` line 2 `not json`: rc 1, `work: line 2 of .shop/work/i1/log.jsonl is not a JSON object;
  no move is made`. File unchanged (checked by read of w1.md).
- `withdraw w1` with `log.jsonl` a directory: rc 1, IsADirectoryError traceback; w1.md still `ready`. See D6.
- Transition of a work-item with no status, no frontmatter, log not writable: covered by the green tests only
  (ENOSPC is monkeypatched in the step). Not probed by run.

Read of the code, no probe:
- `move` (`workqueue.py:142`) refuses a file with no status or a log disagreeing, and restores the file when
  the log append fails (`append`, `workqueue.py:170`, cuts back a partial write). read.

## 3. Old assumptions

The accepted r7 requirement replaces the assumption that a file the command names exists and is readable. One row
per place that still makes it. Tests column is `by search`: no map exists.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_request.py:request, line 68 | reads `--lines` via `workqueue.read`; a missing or directory path escapes as traceback | must refuse "the file lines.md does not exist" before any write | requests.feature r1-r5 (tests/scenarios/test_requests.py, by search; none uses a missing file) | grep `workqueue.read(Path(lines_file)` |
| scripts/workqueue.py:read, line 50 | catches UnicodeDecodeError only; FileNotFoundError, IsADirectoryError, PermissionError escape | every caller's missing or unreadable path becomes a refusal | every work-queue scenario that reads (by search) | grep `def read` and its callers |
| scripts/workqueue.py:highest, line 64 | globs `*/*.md`, reads each (a directory named `w<n>.md` raises) | add refuses it naming the path, changes nothing | tests/scripts/test_work_item_ids.py; work-queue r12 scenario (by search); no directory case | read; probe_dir |
| scripts/workqueue.py:items, line 105 | globs and reads each file for `show` | show refuses a directory named `w<n>.md` | work-queue r3, r11 and r7 show scenarios (by search); no directory case | grep `def items` |
| scripts/workqueue.py:requests, line 113 | globs `requests/q*.md` and reads each for `show` | same refusal for a directory named `q<n>.md` (read) | requests.feature show scenarios (by search) | read |
| scripts/workqueue.py:last_logged, line 123 | `log.exists()` then `read(log)`; a directory raises | refuse naming log.jsonl; nothing written | by search: no test gives log.jsonl a directory; `none` | probe_work: withdraw with log directory |
| scripts/workqueue.py:move, line 142 (write_text lines 161, 165) | write_text of the file runs before the try that covers only the append; an OSError from the file write is a traceback | refuse naming the file (r7) | none (read) | read |
| scripts/workqueue.py:committed, line 260 | `write()` runs outside its try; an OSError from write is a traceback | refuse naming the file (r7) | none (read) | read |
| scripts/workqueue_request.py:_change, line 47 | `path.write_text(after)` inside `committed`; no OSError handling | refuse naming the file (r7) | requests outcome/turn scenarios (by search) | read |
| scripts/workqueue_request.py:path_of, line 18 | checks `is_file()` and refuses "there is no request ..." | the existing pattern the lines check copies | requests.feature scenarios naming a missing request (by search) | read |
| scripts/workqueue_status.py:43, 86, 119, 122, 134; workqueue_done.py:28-65; workqueue_start.py:14, 29; workqueue_answer.py:33, 38; supervise_draft.py:20; measure_read.py:55, 61 | each calls `workqueue.read` on a path it built; a missing or directory path is a traceback | refuse naming the file | by search: status, withdraw, start, answer scenarios; none with a missing file | grep `workqueue.read(` |

## 4. Tests the requirements make impossible to keep

The change adds refusals; it does not alter any success. Looked at all tests that touch the code:
- tests/scenarios/test_work_queue.py: the 12 green r7 tests pass today and still pass; the one red test needs the step bindings
  (not an old assumption). Found sound.
- tests/scenarios/test_requests.py (by search, collection refused under the w148 filter; read): the r1-r5 request scenarios
  use an existing `lines.md`, which the check leaves alone. Found sound.
- tests/scripts/test_work_add_title.py: refuses `\n` and `\r` in the title with the reason "newline". Widening the
  field-value check to the seven breaks does not contradict it. Found sound.
- tests/scripts/test_work_item_ids.py: a `w2.md` with no frontmatter is refused "not a work-item", not a traceback. The new
  directory refusal in `highest` does not change it. Found sound.
- tests/scripts/test_work_withdraw.py, test_work_items.py: no old form of a missing file or a directory. Found sound.
- By search for `Traceback`: every hit asserts its absence; none asserts a traceback. None impossible.
- Mismatch to note: `work_queue_*_steps.py` has no test for a directory or for a line break other than `\n` in a field
  value. Nothing asserts that a field value with VT, FF, NEL, LS or PS is accepted. Found sound.

## 5. A step the work-item skips

The existing way to read a file the command names is `workqueue.read`. Effects only it produces, read or run:
- Refusal "X is not UTF-8 text" for a non-UTF-8 lines file (run: `probe_work` request, lines not UTF-8). The new
  existence check must keep this refusal, not replace it with a check that lets a non-UTF-8 file through.
- Naming the file relative to its parent (read): `--lines sub/lines.md` is named `lines.md`. A new check that names
  the path given keeps the message correct.
- The check sits before the git check and the context check (`committed` and `context_path` are after the lines read).
  A missing lines file in a non-git directory is a traceback today (run). The new check comes before both: the
  refusal for a missing lines file must not depend on git.
- A directory named as `--lines`: an `exists()` check lets it through to IsADirectoryError (run: `probe_work` request,
  lines is a directory); `is_file()` refuses both missing and directory paths (read of Path semantics).

## 6. Defects

D1. `work request --lines` with a missing file: traceback, not a refusal (the work-item's own).
  `work request "Show the queue" --from ctx-a --lines lines.md --source o1` in a repository with spec/index.md and git init
  rc 1, stderr `FileNotFoundError: [Errno 2] No such file or directory: 'lines.md'`, `git status` clean. (run)

D2. `work request --lines <directory>`: traceback. Same command, `lines.md` a directory; rc 1,
  `IsADirectoryError: [Errno 21] Is a directory: 'lines.md'`. (run)

D3. `work request --lines` missing in a directory that is not a git repository: traceback, same
  FileNotFoundError; the lines read runs first. (run)

D4. `work show` with a directory named `.shop/work/i1/w1.md`: rc 1, `IsADirectoryError` traceback from `items`. (run)

D5. `work add` with a directory named `.shop/work/i1/w9.md`: rc 1, `IsADirectoryError` traceback from `highest`
  (reached before any write; git status clean). (run)

D6. `work withdraw w1` with `.shop/work/i1/log.jsonl` a directory: rc 1, `IsADirectoryError` traceback from
  `last_logged`. w1.md unchanged (`ready`). (run)

D7. `work add` accepts a field value with a line break that the reader treats as one, and writes a status line:
  `work add i1 w1 --part-of capability-proposal/p1 --under "thing<U+000B>status: ready" --accepts thing#r1`
  (the same with U+001C, U+0085 or U+2028 in place of U+000B). Result: rc 0, `w1`; the file holds
  `status: drafted`, then `under: thing<X>status: ready`; `work show` prints `i1/w1 ready`. The add check (`workqueue.py:82-86`)
  refuses only LF and CR; `model_parse.frontmatter` splits lines with `str.splitlines()`, which breaks on all seven.
  r15 and r21 list the seven. A title with U+2028 also splits the `# ` heading (run: heading `# T status: ready`).
  Also accepted: U+000B, U+000C, U+0085, U+2028, U+2029 in `--part-of` (rc 0), with the status line still `drafted`
  because the real one comes later. (run: `probe_work` add line-break kinds; `probe_split`)

## 7. The file set

Production:
- scripts/workqueue_request.py (131 lines, room 169): a check that the `--lines` file exists and is a file, naming it, before the read at line 68. Found by grep and the request probe.
- scripts/workqueue.py (286 lines, room 14): the one place a refusal for the directory and the other OSErrors belongs, in `read` or next to it; also widen the field newline check at lines 82-86 to the seven breaks if D7 is in scope. Found by grep and probes D5, D7. Room is tight: any addition here must be short.
- scripts/work (147 lines, room 153): only if the refusal of a file's OSError is caught in `main` rather than in the library. Found by read of `main`.
- scripts/model_parse.py (271 lines, room 29): on the change's path (frontmatter reader); edited only if the fix moves the line-break refusal into the reader. Found by read.

Tests:
- tests/scenarios/test_work_queue.py (287 lines, room 13): the red scenario needs `upstream_keeps_none` and a `no file lines.md` Given. Adding them here leaves 13 lines. Prefer a new module.
- tests/scenarios/work_queue_request_steps.py (new, about 30 lines): the two Givens (`an upstream that keeps no request` imported from requests_write_steps.py, and `no file lines.md`), imported into test_work_queue.py. Found by collect and the red run.
- tests/scenarios/requests_write_steps.py (109 lines): imported only, not changed. Found by grep.
- tests/scenarios/work_queue_git_steps.py (71 lines): `init` and the git steps; unchanged, imported. Found by read.

Modules on the path, not edited: scripts/work, scripts/workqueue.py, scripts/workqueue_request.py, scripts/model_parse.py, scripts/workqueue_done.py (67 lines, room 233), scripts/workqueue_status.py (170 lines, room 130), scripts/workqueue_start.py (43 lines, room 257).
