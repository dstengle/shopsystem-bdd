# Review of w130 (work-queue#r22, work-queue#r23), second review after the answers

**Verdict: DONE.** No finding is Critical and none is triaged fix now.

- r22 and r23 are implemented, and their 5 scenarios pass.
- Nothing under `features/` changed, and no test was removed or weakened. The one allowance holds.
- 5-review's one fix-now finding was `work retry` not running the done check. The answer of 2026-10-25 accepts the work-item as it stands, so that finding is now an observation and is not raised again as fix now.
- What is left is Minor: lint, the file set, and two edges of `work start`.

## Commits reviewed

- Branch `work/w130` is gone. So I took the commits on HEAD between `5ce9f24 work: w130 ready -> claimed` and `d350d36 work: w130 claimed -> done`, less the `work:` commits. That leaves:
  - `7b769e8 work start and an initiative done (work-queue r22, r23)`: w130's commit.
  - `1303b55 model check: request rules …`: another work-item's commit, inside w132's claimed -> done span. It touches none of w130's files.
- The implementer's result lists `a1b01eb`. Its patch hashes the same as 7b769e8's (sha1 `33bb827…` for both `git show --format=`), so it is the same change, rebased on merge. Not a finding.
- After `d350d36` the only w130 commits are `work:` and `work answer:` commits: done -> awaiting-answer, then awaiting-answer -> done. They add no code.
- Later commits touch w130's files (e0ba985, e713679, fce7a8c), but each is another work-item's and is not reviewed here.

## Removed and weakened tests

None. What I searched the diff of 7b769e8 for:

- deleted `def test_` or step functions;
- dropped Examples or parametrize rows;
- removed or loosened `assert`s;
- added skip or xfail marks;
- edits under `features/` (there are none).

The only edit to an existing test file is `with_state` (see Allowances). `test_work_queue.py` gains one import line.

## Allowances

- `tests/scenarios/work_queue_status_steps.py` `with_state` (`setup`): **holds**.
  - It splits the tail " and whose work-item w2 is ready" into a second work-item file.
  - It adds, removes or changes no `assert`, no expected value and no case.
  - A Given without that tail writes exactly what it wrote before.

## Cannot verify

- The report's figures: the suite at start (752 passed / 5 failed), and the requests scenarios that run `work resolve` still passing. I did not run the whole suite; `work run` ran it.
- The `work resolve` done path (workqueue_request.py:115-124): no scenario drives it, so I could only read it. On reading:
  - `_path` still refuses a missing request;
  - `edit` still refuses a request that is not accepted, before anything is written;
  - initiative.md joins the commit only when `becomes` holds.

## Findings

### 1. Minor, observation: `work retry` back to green runs no done check (scripts/workqueue.py, `retry`)

- **What is wrong.** Plan D7 lists retry among the commands that set done, but the commit does not hook it.
- **When it shows.** After `work run`'s push fails, a work-item goes green -> failed (supervise_faults.py `fail`). Retrying it back to green leaves the initiative `started`.
- **Already settled.** The answer of 2026-10-25 accepts this and records it as an observation for a later line (records: observation 2026-10-25-i24-unpinned-cases, 4363b41). Listed only so the record is complete.
- **Reproduction.** By reading only: building a failing push needs commands this review may not run.

### 2. Minor, drop: ruff I001 on two import lines the commit wrote

- **Where.**
  - `scripts/workqueue.py:235` (line 232 at 7b769e8): the function-level `import workqueue_done` with its comment.
  - `tests/scenarios/test_work_queue.py:7`: `from .work_queue_start_steps import *` placed after `withdraw`.
- **Fix.** `ruff --fix` on the two files.
- **The check's other results are not w130's:**
  - `measure_build.py:3` I001;
  - FURB167 at `design_model_check_requests.py:132`;
  - vulture `notes` at `work_queue_status_steps.py:77`, which was already there at the base.

### 3. Minor, observation: a file edited outside the work-item's `fileset`

- `tests/scenarios/work_queue_status_steps.py` is not in the `fileset` (design-decision/the-file-set-is-the-claim).
- The report states it, and the edit is setup only. No fix is needed now.

### 4. Minor, observation: `work start` crashes where it should refuse, when `.shop/work/i<n+1>/` exists without initiative.md (scripts/workqueue_start.py:13,38)

- **What is wrong.**
  - `_highest` counts only directories that hold an initiative.md, so `directory.mkdir(parents=True)` raises FileExistsError.
  - `scripts/work` catches only `Refused`, so the user gets a traceback instead of the refusal r7 asks for.
- **Fix.** Count every `i<n>` directory name, or refuse when the directory exists.
- **Reproduction.** By reading only. No client makes such a directory today.

### 5. Minor, observation: `work start` with a scalar `source:` writes its characters as the source (scripts/workqueue_start.py:34,40)

- **What is wrong.** `model_parse.frontmatter` returns a scalar `source: o1` as the string `"o1"`. `", ".join(source)` then writes `source: [o, 1]`.
- **Why it is only an observation.** Requests are written by `work request`, which writes a list, and the scenario uses a list.
- **Fix.** Wrap a string source in a list.
- **Reproduction.** By reading model_parse.py:31-40.

### 6. Minor, drop: initiative.md has no frontmatter `title`

- design-decision/work-file-forms (0026) lists `title` among initiative.md's fields, and plan D2 says to write it.
- `start` writes the title only as the `# ` heading. r22 does not ask for a title, so no Behaviour line is contradicted.

No code without a line: `start` serves r22, and `workqueue_done` serves r23, with the hooks in `withdraw` and `resolve`. Leaving `work run` out is reading B.

## Commands run

- `git log --format='%H %s' --grep="^work: w130 "` and `git log --format='%h %s' f890f2f..HEAD | grep w130`: found the claim and done commits.
- `git log --format='%h %s' --stat 5ce9f24..d350d36`: the commits in that span.
- `git show 7b769e8 --format=`, and `git show --format= <c> | sha1sum` for 7b769e8 and a1b01eb: the same patch.
- `git log 7b769e8..HEAD -- <w130's code files>`: only other work-items' commits since.
- `grep` in spec/capabilities/work-queue.md, features/work-queue.feature:30-64 and spec/decisions/0026, 0061, and reading scripts/model_parse.py:12-40.
  - Risk: a scalar `source` breaks `start`'s join. Verified that it does (finding 5).
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 5ce9f243…`:
  - ruff: 4 errors, 2 of them w130's;
  - vulture: 1, already there;
  - import-linter: the project states no import contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output, so no file is over the limit.
- `python3 -m pytest -q --work-item w130 -n 0 -p no:cacheprovider tests/scenarios/test_work_queue.py`: 5 passed.
- `git status --short`: clean.
