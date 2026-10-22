# Plan of w2: work add, a title is free text (work-queue#r1, #r7)

## 1. What goes green

None of the accepted scenarios is red today: the research ran all 14 accepted tests of `features/work-queue.feature` (through `tests/scenarios/test_work_queue.py`) and all passed. No accepted scenario covers the title rule, which is where the defects are (notes, parts 1 and 6).

- work-queue#r1
  - "add with --part-of, --under and --accepts writes a drafted work-item with the fields given (deprecated)" (`@r1 @deprecated`): passes. `add i1 w1` now writes the title `w1` to `w1.md`, since w1 is the first id. It stays green; this work-item retires nothing.
  - "add with a title, --part-of, --under and --accepts writes a drafted work-item named by its id and prints the id": passes.
  - Defect D1, which no scenario covers: a title containing `/` (`Show a/b`) is refused with `the name Show a/b is not a file name`. Under r1 a title is free text and is written as the heading.
- work-queue#r7
  - "a command that cannot be done exits with an error, says why and changes nothing" (outline), "a transition of a work-item that does not exist is refused…", "add refuses an initiative that is not one directory entry under .shop/work/…", "add refuses a field value with a newline in it…", "show refuses a file under an initiative that is not UTF-8 text…", "a transition of a work-item whose file <lacks> is refused…" (outline) and "a transition whose log.jsonl <fault> is refused…" (outline): all pass.
  - Defects D2 and D3, which no scenario covers: a title with a newline (`Show\nstatus: ready`) or a carriage return (`Show\rthing`) is written. The program exits 0 and the file gets a heading `# Show` followed by a second body line.

Because nothing is red, the implementer first writes a test of the title rules (part 2) and sees it fail for D1, D2 and D3, then makes the change.

## 2. Where the change lands

- `scripts/workqueue.py`, in `add`:
  - Drop the old file-name check on the title (the `entry(title, "name")` call). `entry` itself stays, because the initiative still uses it.
  - Refuse a title that contains a newline or a carriage return, with its reason. This follows the existing field newline check.
  - Write the title as the `# ` heading, unchanged.
- `scripts/work`: rename the `add` positional argument and its use in `cmd_add` from `name` to `title`, so the help text matches r1.
- `skills/migrating-to-capabilities/SKILL.md`, line 111: change `work add <initiative> <name> …` to `work add <initiative> <title> …`, taking the printed id as the work-item's name. This comes from the work-item text.
- Added: `tests/scripts/test_work_add_title.py`, a new test of `work add` run as a process in a temporary repository. It covers:
  - a title with `/` is written as the heading;
  - a title with a newline is refused, and so is one with a carriage return, each with exit 1, its reason, and no file changed.
  
  Why added: no accepted scenario drives these rules (part 1), and `tests/scripts/` is the home for tests of scripts that no scenario drives (CLAUDE.md module map). It does not go in `tests/scenarios/test_work_queue.py`, which has 23 lines of room.

## 3. Decisions

- **D-a. A title may hold any character except a newline or a carriage return.** `/`, `\`, `.` and `..` are written as given. Rests on work-queue#r1: the title is free text and the file is named by the id (design-decision/work-items-named-by-ids), so the file-name rule has no object.
- **D-b. A carriage return counts as a newline in a title, so a title with one is refused under r7.** Rests on work-queue#r1 and #r7. r1 requires the title to be the file's `# ` heading, and a heading is one line. A CR breaks that line when the file is read back: the probe shows the heading `# Show` and a body line `thing`. Writing it would therefore break r1. The work can't be done as asked, so r7 refuses it and changes nothing. This settles the researcher's second question.
- **D-c. The refusal's reason names the title and says it has a newline in it**, worded like the field refusal ("the value of --part-of has a newline in it"). Rests on work-queue#r7 ("say why").
- **Empty title: not taken; see the question below.**

## 4. Tests the decisions break

None. Checked as follows:
- The research searched `tests/` for `add(`, `work add`, `file name` and `/`. No test asserts that a `/` title is refused or that the title is a file name.
- All accepted add scenarios pass a title without `/`, newline or CR, so they stay green under D-a to D-c. That includes the deprecated `add i1 w1`, the r7 outline whose `<name>` is `w1`, and the `--part-of` newline scenario.
- The r9 add outline (`add i1 w1 …`) is not accepted. On reading, it still passes, because w1 is the first id.
- `tests/scripts/test_work_withdraw.py` and `test_work_items.py` do not call `add`.

## 5. Open cases

- The exact wording of the title refusal, inside D-c.
- Other control characters in a title (a tab, a form feed, U+2028 and similar): the implementer names how each behaves. Only LF and CR are decided here.
- A title with leading or trailing spaces: the implementer names whether it is written as given.
- Whether an empty title is refused or written: this is the question in the result, and the plan does not choose.
