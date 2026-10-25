# Review of w138

**Verdict: DONE_WITH_CONCERNS.** One Important finding, triaged fix now: r73's Retires misses a deprecated scenario whose requirement the work-item accepts through a range (`cap#r3-r6`), and ranges are the usual form of a real proposal's `changes`. Otherwise the commits do what r72, r73 and r74 ask. features/ is untouched and no test was removed or weakened.

## Commits reviewed

The branch `work/w138` is gone. Between `7a341cf work: w138 ready -> claimed` and `1e03263 work: w138 claimed -> done` on HEAD, after leaving out `work run`'s own `work:` commits (w139, w140, w141), one commit remains:

- `e0ba985` work run drafts a formulated proposal's work-items with their Retires, and a work-item for fix-now findings

The implementer's result lists `9277e80` under the same subject. That is the same commit before `work run` rebased it: `git diff 9277e80 e0ba985 -- CLAUDE.md scripts tests` is empty, and both have the same 7 files with 187 lines added and 9 removed. No difference.

Files: CLAUDE.md, scripts/supervise.py, scripts/supervise_draft.py (new), scripts/supervise_review.py, scripts/workqueue.py, tests/scenarios/supervision_proposal_steps.py (new), tests/scenarios/test_supervision.py (one import). Every file is in the fileset. `supervision_review_steps.py` is in the fileset but was not touched; the report says so.

## Removed and weakened tests

None. I searched the diff for removed lines under `tests/`: there are none (test_supervision.py gains only one import). I also searched for added `skip` or `xfail` (none), for changed parametrize lists (none) and for any change under `features/` (none). The plan lists no tests the decisions break, and none were changed.

## Allowances

The report's `## Tests changed under an allowance` is "none". That matches the commits.

## Cannot verify

- The report's green run (`--work-item w138`: 145 passed). I did not rerun it; `work run` ran the suite before it merged.
- The report says the red run failed for the right reason (the drafting module was written but not yet wired in). Only the report records this.

## Findings

### 1. Important, fix now. A range in `accepts` retires nothing: scripts/supervise_draft.py:30-33 (`retires`)

- **What is wrong.** `wanted = {a.split("#", 1)[1] for a in accepts}` keeps a range entry such as `thing#r3-r6` as the one string `r3-r6`. It then checks `tag in wanted` by equality, so a scenario tagged `@deprecated @r4` is not listed under `## Retires`, even though the work-item accepts r4.
- **Why it matters.** r73 says to list "each scenario tagged `@deprecated` whose `@r<n>` tag names a requirement the work-item accepts". Ranges are how proposals write `changes`: i13 (`supervision#r1-r10`, `work-queue#r1-r7`, `design-model-check#r1-r27`, ...), i11, i10 and i8 all do. A changed line is exactly where a deprecated scenario comes from. Such a draft would leave out the scenarios it retires, which is a wrong answer.
- **The plan.** Decision 4 says "(a range included)". The implementer departed from it and listed the gap as an open case.
- **Elsewhere.** `scripts/supervise_brief.py:95-96` and `scripts/work_items.py:43-45` already expand `r<n>-r<m>`.
- **Fix.** Expand each accepted range the same way: `lo, _, hi = rs.lstrip("r").partition("-r")`, giving `r<lo>` through `r<hi>`. Add a scenario under r73 with a range in `changes`, through the line first if no Example covers it.

### 2. Minor, observation. A named work-item without `part_of` gives a fix work-item `part_of: None`: scripts/supervise_draft.py:76-78

- **What is wrong.** `str(data.get("part_of"))` and `str(data.get("under"))` write the literal `None` when the named work-item lacks the field. The report says that in this case "nothing is drafted", but the code drafts the work-item with `part_of: None`.
- **Why it matters.** Every work-item `work add` writes has both fields, so no client sends this today.
- **Reproduction.** Code reading only: `str(None) == "None"` goes to `workqueue.add` unchecked.
- **Fix.** Skip a named work-item that has no `part_of` or `under`.

### 3. Minor, observation. Only the first `w<n>` in a findings line is tried: scripts/supervise_draft.py:73-75

- **What is wrong.** `WORK_ITEM.search` takes the first match only. If a line names a w-number from another initiative or context first (for example "w121 was moved by …") and an initiative work-item later, that line is skipped.
- **Fix.** Use `finditer`, and take the first match that is in `concerned`.

### 4. Minor, observation. `questions` given as one string lists nothing: scripts/supervise_draft.py:64-66

- **What is wrong.** The capability's Implementation section says "A result's `questions` given as one string is read as one question". `fix_work_item` returns False for a string.
- **Why it is low.** The branch review's result goes through `supervise_worker.py:192-193`, which turns a string into a list, but `fix_work_item` reads the raw `result.json` again.
- **Reproduction.** Code reading: `isinstance("x", list)` is False, so the method returns False.
- **Fix.** `lines = [lines] if isinstance(lines, str) else lines`.

### Checked, no finding

- **Code no line asks for.** Each piece of behaviour has a line:
  - drafting: r72
  - Retires: r73
  - the fix work-item and its `findings:` field: r74
  - the push after drafting: r38
  - one review a run, with the fix pulled: r1 and r27, as plan decision 11 gives
- **Retires bullet form.** `- "<title>" (<cap> @r<n>)` matches the existing w100 form. No script parses `## Retires` (grep of scripts/).
- **Duplicate drafting on i24's real data.** Each of i24's 15 formulated proposals already has a work-item `part_of` it and `under` each capability its adds and changes name: I compared their frontmatter with the work-items'. The next `work run i24` drafts nothing new.

## Tools

- `tools check --base 7a341cf`:
  - ruff: 1 error, `scripts/workqueue.py:235` I001. This is the local `import workqueue_done` in `withdraw`, which predates the commits (`git show 7a341cf:scripts/workqueue.py`), so it is already there and not introduced here.
  - vulture: clean.
  - import-linter: the project states no contracts.
- `tools size --limit 300`: printed nothing. The touched files: supervise.py 228, workqueue.py 282, supervise_draft.py 80, supervise_review.py 78, test_supervision.py 247, supervision_proposal_steps.py 82.

## Commands run

- `git log --format='%H %s' --grep="^work: w138 "`
- `git log --ancestry-path 7a341cf..1e03263`
- `git show --stat 9277e80`, `git show --stat e0ba985`, `git diff 9277e80 e0ba985 -- CLAUDE.md scripts tests`, `git show e0ba985`
- `grep -rn Retires scripts/`, and the `## Retires` sections in `.shop/work/*/w*.md`
- grep for `status`/`adds`/`changes` of i24's proposals, and for `part_of`/`under`/`status` of i24's work-items
- grep for range handling in work_items.py and supervise_brief.py, and for the `questions` string handling in supervise*.py
- Grep `^changes:.*#r[0-9]+-r` over .shop/work
- `git show 7a341cf:scripts/workqueue.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 7a341cf55761b1f71ad06db0c25d1bc9adfabe5c`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` of the touched files
