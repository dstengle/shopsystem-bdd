# Research of w2 (accepts work-queue#r1, r7)

Tools: `tools map` never made (no map; it runs the suite). `tests-of` and `untested` not used: by search for tests.
`tools refs` is blind to `scripts/work` (it imports `workqueue` by sys.path): `refs workqueue.add` gives 0, text search gives scripts/work:15.
Scratch: `.shop/scratch/w2-1-research/` (probe_title.py, repo_* fixtures). `git status --porcelain` empty at the end.

## 1. Why each scenario is red today

None is red. Command for all 14 accepted node ids (`features/work-queue.feature` via `tests/scenarios/test_work_queue.py`; 11 of 25 deselected by the work-item filter):
`python3 -m pytest -q --tb=short -p no:warnings tests/scenarios/test_work_queue.py` → `14 passed` (run).
The accepted scenarios are:
- r1 deprecated `add ... (deprecated)` (`@r1 @deprecated`): passes (run).
- r1 `add with a title ...`: passes (run).
- r7 `a command that cannot be done ...` (4 examples), `a transition of a work-item that does not exist`, `add refuses an initiative ... ../../spec`, `add refuses a field value with a newline` (--part-of only), `show refuses ... not UTF-8`, `a transition of a work-item whose file <lacks>` (2), `a transition whose log.jsonl <fault>` (2): all pass (run).

The gap: no accepted scenario covers the title rule of r1 or the title newline of r7, so they pass while `scripts/workqueue.py` breaks the requirement (part 6).

## 2. What the system answers today

Scenarios: run as in part 1, all 14 passed.

Probe: `python3 -m pytest -q -s -p no:warnings -o addopts="" .shop/scratch/w2-1-research/probe_title.py` (the file's `addopts` clears xdist, which swallowed `-s` output). Run against the worktree's `scripts/work`, each in a fresh git repo under scratch with spec/index.md and `.shop/work/i1`:

- control `add i1 "Show the queue" --part-of capability-proposal/p1 --under thing --accepts thing#r1`: exit 0, prints `w1`, writes `.shop/work/i1/w1.md` with id `work-item/missingmass.io/shopsystem/probe/w1`, status drafted, `# Show the queue` (run).
- title `Show a/b`: exit 1, stderr `work: the name Show a/b is not a file name`, no files (run). Nearest case, a `/` title: refused.
- title `Show\nstatus: ready`: exit 0, prints `w1`; heading `# Show`, then body line `status: ready` (run). Nearest case: the newline is written.
- title `Show\rthing`: exit 0, prints `w1`; heading `# Show`, body `thing` (run).
- title `` (empty): exit 1, stderr `work: the name  is not a file name` (run). The message names nothing; the plan decides whether an empty title is refused.

## 3. Old assumptions

The old form: the second `add` argument is the file name, checked as a path. The new form: it is a free-text title written as the heading, and the file is named by the id.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:add line 71 `entry(title, "name")` | refuses `/`, `\`, `.`, `..`, empty: the old file-name rule | title is free text (r1): this check goes; `/` must be written | the add scenarios of test_work_queue.py, through the process; none passes a `/` title | refs: 0 (blind); search for `entry(` (2 refs: lines 71, 58) |
| scripts/workqueue.py:entry lines 56-59 message `is not a file name` | words the refusal of a title as a file name | goes with the check above | none | search |
| scripts/workqueue.py:add lines 72-74 newline check over `--part-of`, `--under`, `--accepts` | title not in the loop | title with newline refused (r7) | the r7 newline scenario, `--part-of` only; none for title | search |
| scripts/workqueue.py:add line 84 `# %s` written with title unescaped | a title with newline or CR writes a second line | one line (r7) | the r1 control only; none with newline | search |
| scripts/work:49 `a.add_argument("name")` and cmd_add line 15 `args.name` | the title is called `name` | rename to title (cosmetic; help text) | the add scenarios | search |
| skills/migrating-to-capabilities/SKILL.md:111 `work add <initiative> <name> ...` | old form, the name as the file name | `work add <initiative> <title> ...`, taking the printed id (work-item text) | none (markdown) | search |
| skills/delivering-an-initiative/SKILL.md:33 | already `<title>` and the printed id | consistent, no change | none | search |

## 4. Tests the requirements make impossible to keep

`tests-of` has no map to read; by search (grep for `add(`, `work add`, `file name`, `/` in tests/).
- tests/scenarios/test_work_queue.py and work_queue_add_steps.py: all 14 accepted tests pass as they are (run). Also the r9 add outline (`add i1 w1 ...`) is not accepted; by read it still passes, w1 being the first id (read, not run).
- tests/scripts/test_work_withdraw.py, test_work_items.py: do not call `add`; unaffected (read).
- No test asserts that a `/` title is refused or that a title is a file name. Verdict: none.

## 5. A step the work-item skips

The newline check (scripts/workqueue.py add lines 72-74) is the step that refuses a value with a newline. Title is not in its loop, so the title skips it. Shown by probe: `Show\nstatus: ready` and `Show\rthing` are written with exit 0 (part 2, run). Effects only this step produces: the refusal with the reason `the value of ... has a newline in it; a work-item's field is one line` (run through the r7 scenario for `--part-of`). A title with a newline gets no such refusal.

## 6. Defects

### D1. A title with `/` is refused (r1)
Repro: `python3 -m pytest -q -s -p no:warnings -o addopts="" .shop/scratch/w2-1-research/probe_title.py::test_title_with_slash`
Came back: `work: the name Show a/b is not a file name`, exit 1, no files. r1: the title is free text.

### D2. A title with a newline is written (r7)
Repro: `... probe_title.py::test_title_with_newline_and_status`
Came back: exit 0, `w1`; the file has heading `# Show` then the body line `status: ready`. r7: refused with its reason, nothing changed.

### D3. A title with a carriage return is written (r7)
Repro: `... probe_title.py::test_title_with_carriage_return`
Came back: exit 0, `w1`; heading `# Show`, body `thing`.

## 7. The file set

Must change for the work-item's requirements:
- `scripts/workqueue.py`: title check in `add` (lines 70-71, 72-74, 84): free text with `/`, refuse a newline or CR in the title. Found by search and probe D1-D3. 252 lines, room 48.
- `scripts/work`: argparse `name` for add (line 49, 15), rename to title; cosmetic. 71 lines, room 229.
- `skills/migrating-to-capabilities/SKILL.md`: line 111 `work add <initiative> <title>`, taking the printed id. 206 lines (markdown; the size limit does not apply).

Changes needed by none of the accepted scenarios; they pass today. Any test added for the title rules would be in tests/scenarios/work_queue_add_steps.py (60 lines, room 240), which the work-item may add to; and tests/scenarios/test_work_queue.py (277 lines, room 23), which is over the room needed.

Path modules, unedited:
- `scripts/model`: 137 lines, room 163 (the frontmatter reader workqueue.py loads).
- `tools size --limit 300` printed nothing: no tracked Python file is over 300.
