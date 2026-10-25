# Plan of w148: `work request` refuses a --lines file that does not exist (work-queue#r7)

## 1. What goes green

- **work-queue#r7**, scenario "request with a --lines file that does not exist is refused, naming the file, and changes nothing" (features/work-queue.feature:190).
  Red today (notes §1): the Givens `an upstream that keeps no request` and `no file lines.md` are unbound in tests/scenarios/test_work_queue.py (the first lives in requests_write_steps.py, imported only by test_requests.py; the second is defined nowhere). Once bound, the command ends on a FileNotFoundError traceback (notes §2, D1): `workqueue_request.request` reads the lines file through `workqueue.read` with no check, and `scripts/work`'s `main` catches only `Refused`.
- The other r7 scenarios (12 tests) are green today and stay green.
- The work-item retires no scenario.

## 2. Where the change lands

- `scripts/workqueue_request.py`: in `request`, before the lines file is read (line 68) and before any git check or write, a check that the path given as `--lines` is a regular file; when it is not, a `Refused` that names the path as given and says it does not exist. The existing read through `workqueue.read` stays after it, so the non-UTF-8 refusal is kept.
- `tests/scenarios/work_queue_request_steps.py` (new, small): the Given `no file lines.md` (makes sure no such path is in the repository) and the binding of `an upstream that keeps no request` for the work-queue feature.
- `tests/scenarios/test_work_queue.py`: one star-import line for the new steps module (287 lines, goes to 288, under the 300 limit).

Dropped from the researcher's set:
- `scripts/workqueue.py`: leaving it alone is decision 3. It has 14 lines of room, and the change it would get (directory and OSError refusals in `read`, `highest`, `items`, `last_logged`, and the wider line-break check) goes past this work-item's scenario.
- `scripts/work`: the refusal is raised as `Refused`, which `main` already turns into the `work: <reason>` exit 1. No change there.

Read only, not changed: `tests/scenarios/requests_write_steps.py`, `tests/scenarios/work_queue_git_steps.py`.

## 3. Decisions

1. **Where the check sits**: in `workqueue_request.request`, just before the read of the lines file. That is after the existing `--source`/`--thread` check (which already runs first; notes §2) and before `committed` and the git check. So a missing lines file is refused even outside a git repository (D3), and nothing is written (r7: "change nothing"). Rests on work-queue#r7.
2. **What the check tests**: whether the path is a regular file, not only whether it exists. A directory given as `--lines` (D2) is then refused too, not left to raise IsADirectoryError. The refusal names the path exactly as given on the command line (notes §5: `workqueue.read` names a file relative to its parent, so `sub/lines.md` would show as `lines.md`). For the scenario, the text in stderr must contain `the file lines.md does not exist`. Rests on work-queue#r7 ("say why"); it copies `path_of`'s existing `is_file()` refusal in the same module.
3. **Scope**: only the `--lines` path of `work request`. The other tracebacks the notes found go to the work queue as defects for another work-item, not into this one: D4 (`show` on a directory `w<n>.md`), D5 (`add` on one), D6 (`withdraw` with `log.jsonl` a directory) and D7 (`add` takes VT/FF/NEL/LS/PS in a field value). The work-item names one scenario. Widening `workqueue.read` or the field check would change scripts/workqueue.py, which has 14 lines of room, and would add behaviour that no accepted scenario pins. Rests on work-queue#r7 and design-decision/the-file-set-is-the-claim.
4. **Binding the upstream Given**: the new steps module binds the step text `an upstream that keeps no request` with the same effect as `requests_write_steps.upstream_keeps_none` (spec/index.md written, git initialised), reusing that function. It must not star-import all of requests_write_steps into test_work_queue.py: that module defines its own `it exits with an error` and `the asker runs`, which would clash with or shadow test_work_queue's steps. Only the one step's binding comes in. Rests on work-queue#r7's scenario; it changes nothing the narrator sees.

## 4. Tests the decisions break

None. What I checked, using the notes' §4 and the step code:
- tests/scenarios/test_requests.py: requests r1 to r5 give an existing regular `lines.md`, which passes the new check, so the read and its refusals are unchanged.
- test_requests' non-UTF-8 lines case, if there is one: the file exists, so the check lets it through and `workqueue.read` still refuses it as before.
- tests/scenarios/test_work_queue.py: the shared Then steps `work says that`, `it exits with an error` and `nothing under the repository has changed` are used as they are. The `snapshot` the When step takes comes after the Givens, so the git init is part of "before".
- tests/scripts/*: none of them reaches `workqueue_request.request` with a missing path.

## 5. Open cases (for the implementer to name, not to choose)

- The wording of the refusal for a `--lines` path that exists but is a directory: the scenario covers only a missing file.
- A `--lines` file that exists but cannot be read (permissions): it still escapes as a PermissionError traceback through `workqueue.read`. No scenario covers it.
- A missing lines file when `--source` and `--thread` are both absent: the origin refusal comes first today, and decision 1 keeps that order. No scenario says which reason wins.
- D4 to D7 (notes §6) are left as they are. Name them as defects for the queue.
