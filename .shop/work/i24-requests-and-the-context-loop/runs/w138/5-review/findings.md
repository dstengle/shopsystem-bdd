# Review of w138 (second review, after the answer of 2026-10-25)

**Verdict: DONE.** The commits are the same ones the first review (4-review) read, and nothing was added after it. That review's one fix-now finding was the range gap in `retires()`. The person has answered it: accept w138 as it stands and fix the gap in its own work-item. That work-item exists as w150 (drafted, accepts supervision#r73, its range scenario to be formulated first). So the gap is recorded below as answered and not raised again. No finding is Critical, and none still needs fixing now.

## Commits reviewed

The branch `work/w138` is gone. The `ready -> claimed` commit is `7a341cf` and `claimed -> done` is `1e03263`. Between them on HEAD, after leaving out `work run`'s `work:` commits, one commit remains:

- `e0ba985` work run drafts a formulated proposal's work-items with their Retires, and a work-item for fix-now findings

The implementer's result lists `9277e80` under the same subject. `git diff 9277e80 e0ba985 -- CLAUDE.md scripts tests` is empty, so it is the same commit, rebased. No difference.

Files: CLAUDE.md, scripts/supervise.py, scripts/supervise_draft.py (new), scripts/supervise_review.py, scripts/workqueue.py, tests/scenarios/supervision_proposal_steps.py (new), tests/scenarios/test_supervision.py. All are in the fileset.

Later commits by other work-items touch supervise.py and workqueue.py. They are not w138's, so they are not reviewed here.

## Removed and weakened tests

None. I searched with `git diff --stat 7a341cf 1e03263 -- features tests`. Under tests/ there are only additions (83 lines added, 0 removed): the new step module and one import. No skip, no xfail, no parametrize change. features/ is unchanged.

## Allowances

The report gives "none", and the commits agree.

## Cannot verify

- The report's green run (`--work-item w138`: 145 passed). I did not rerun it; `work run` ran the suite before the merge.
- The red run, failing for the reason the report gives. Only the report records it.

## Findings

### 1. Important, answered (was fix now). A range in `accepts` retires nothing: scripts/supervise_draft.py:30-33

- **What is wrong.** `retires()` compares `r3-r6` to a single `@r<n>` tag by equality, so r73 misses deprecated scenarios that are accepted through a range.
- **The answer (2026-10-25).** Accept w138 as it stands. The fix is its own work-item, w150 (drafted, supervision#r73), with a range scenario row formulated first.
- **Triage.** No longer fix now under w138.

### 2. Minor, observation. A named work-item without `part_of` or `under`: scripts/supervise_draft.py:76-78

- **What is wrong.** The fix work-item would be written with the literal `part_of: None`.
- **Why it is only an observation.** Every work-item that `work add` writes has both fields.
- **Reproduction.** Code reading: `str(None)` goes to `workqueue.add` unchecked.

### 3. Minor, observation. Only the first `w<n>` of a findings line is tried: scripts/supervise_draft.py:73-75

- **What is wrong.** `WORK_ITEM.search` takes the first match. A line that names a foreign w-number before the initiative's own work-item is skipped.
- **Fix.** Use `finditer` and take the first match that is in `concerned`.

### 4. Minor, observation. `questions` given as one string lists nothing: scripts/supervise_draft.py:64-66

- **What is wrong.** The capability's Implementation section reads a single string as one question. `fix_work_item` reads the raw `result.json` and returns False when `questions` is a string.
- **Fix.** Wrap a string in a list.

### Checked, no finding

- **Code no line asks for.** None:
  - drafting: r72
  - Retires: r73
  - the fix work-item and its `findings:` field: r74 and design-decision/review-of-work-items
  - the push after drafting: r38
  - one review a run, with the fix pulled: r1 and r27, as plan decision 11 gives
- **Behaviour against r72-r74 and the Purpose.** No contradiction apart from finding 1.

## Tools

- `tools check --base 7a341cf`:
  - ruff: 2 errors, neither from w138.
    - `scripts/supervise_rounds.py:49` RUF059 comes from w137's commit 395fd37, not from e0ba985.
    - `scripts/workqueue.py:239` I001 is the local `import workqueue_done` in `withdraw`, which predates 7a341cf.
  - vulture: clean.
  - import-linter: the project states no contracts.
- `tools size --limit 300`: printed nothing, so no file is over the limit.

## Commands run

- `git log --format='%H %s' --grep="^work: w138 "`
- `git log --oneline -15`
- `git log --format='%h %s' --ancestry-path 7a341cf..1e03263 | grep -v ' work: '`
- `git diff 9277e80 e0ba985 -- CLAUDE.md scripts tests | wc -l` (0)
- `git show --stat e0ba985`, `git show e0ba985 -- scripts tests CLAUDE.md`
- `git diff e0ba985 HEAD --stat -- <w138's scripts>`
- `git diff --stat 7a341cf 1e03263 -- features tests`
- `grep` of r72-r74 and `rests_on` in spec/capabilities/supervision.md
- `grep -l -i range` of the i24 work-items, and `head` of w150.md
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 7a341cf55761b1f71ad06db0c25d1bc9adfabe5c`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
