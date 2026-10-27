# Review of w206 (second review): fix the findings of branch review 2 of i39

**Verdict: DONE.** The commits have not changed since review 5: one implementation commit, `e4e61321`. Review 5's one fix-now finding was that no Behaviour line asks for the merge into another held proposal. The person has answered it: request q20, line 3, raised 2026-10-27, carries that supervision line. I checked q20, and its line 3 states the behaviour the code implements. This review finds nothing new that is Critical or fix now.

## Commits reviewed

- `git log --format=%H -1 --grep="^work: w206 ready -> claimed$"` gives `694a5f8e`. The branch `work/w206` is gone (`unknown revision`), so the range runs from `694a5f8e` to `85589330` (`work: w206 claimed -> done`), plus what came after it on HEAD.
- `694a5f8e..HEAD` holds:
  - `e4e61321` Fix branch review 2 findings: the implementer's commit. It touches `scripts/supervise_change.py`, `scripts/supervise_rounds.py`, `scripts/workqueue_list.py`, `tests/scripts/test_supervise_change.py` and the new `tests/scripts/test_workqueue_list.py`.
  - `85589330` `work: w206 claimed -> done`, `61fb5d8d` `work: w206 done -> awaiting-answer`, `b5bf81a4` `work request: q20` and `7abd1e9e` `work answer: w206 awaiting-answer -> done`. These are `work run`'s and `work`'s own commits, and they touch only `.shop/work/`.
- `git diff --stat e4e61321 HEAD -- scripts tests features` is empty, so nothing else changed code, tests or features.
- This matches the implementer's `result.json` (`commits: ["e4e61321 …"]`). Every file is in the work-item's fileset, and nothing under `features/` changed.

## Removed and weakened tests

None. I searched the diff of `tests/` for removed lines, for `skip` or `xfail`, and for changed asserts. `test_supervise_change.py` gains a helper (`proposal`) and one test, and its existing test and its helper `write` are unchanged. `test_workqueue_list.py` is new.

## Allowances

The report says "none". That holds, because no existing test changed.

## Cannot verify

- The report's runs: red then green on the two unit files, `--work-item w206` (154 passed, 1 skipped), and the supervision integrate/draft/proposal scenarios (84 passed, 1 xfailed). I did not run the suite, because `work run` ran it before the merge.
- The plan's §4 asked the implementer to check `supervision_reintegrate_steps.py` and `supervision_integrate_steps.py`. The only evidence that this was done is the report's run of 84.

## Findings

### 1. Important, answered (code no line asks for): another held proposal's lists merged (w206)

- **Where:** `scripts/supervise_change.py:79-89` and `:108-112`, called from `scripts/supervise_rounds.py:195`.
- **What it was:** this was review 5's finding 1. A redraft integrate round merges its ids (a union) into another held capability-proposal's `adds`, `changes` and `removes`, and no supervision line asked for that.
- **Status:** the person answered it on 2026-10-27: "the supervision line is carried in q20, line 3".
  - I verified q20 (`.shop/work/requests/q20.md`, commit `b5bf81a4`). Its line 3 reads: "When a round of the kind `integrate` started for a capability-proposal ends with a change list that names another capability for which the initiative holds a capability-proposal, `work run` shall add the round's ids for that capability to that proposal's `adds`, `changes` and `removes`, keeping the ids it holds."
  - That matches `merge_lists`: the proposal's own ids are kept in their order, and the round's ids it lacks are appended.
- **Not reopened:** the fix is a line written through integrating-a-proposal. That path has begun with q20, so this review raises no question for it.

### 2. Minor, observation: q20 line 3 is narrower than the code (w206)

- **What:** line 3 covers an integrate round "started for a capability-proposal". The code also merges in an initiative's first integrate round, where `own` is the initiative's name, so every held proposal is merged into (plan D-e).
- **Why it matters:** if a held proposal exists when a first round ends, no line would cover the merge that follows. Normally a first round runs before any proposal is held, so no client hits this today.
- **Fix:** when q20 is taken in, have line 3 say "a round of the kind `integrate`", without "started for a capability-proposal". Or confirm that the first round never finds a held proposal.
- **How I found it:** by reading `supervise_rounds.py:195` (`write_proposals(..., name)`) against q20 line 3. I ran no probe.

### 3. Minor, observation (carried from review 5): `merge_lists` writes nothing for a field missing from the frontmatter (w206)

- **Where:** `scripts/supervise_change.py:88`. `re.sub(..., count=1)` rewrites only a line that already exists, and it searches the whole file, not just the frontmatter.
- **Reproduction (review 5):** `grep -L "^changes:" .shop/work/*/*.md` lists `.shop/work/i1-first-spec/spec-integration.md`, an old proposal. Every held proposal of i39 has all three fields, and `write_proposals` always writes all three.

### 4. Minor, drop: ruff B023 at `scripts/supervise_change.py:88` (w206)

- This is a false positive. `re.sub` calls the lambda within the same loop iteration.
- B023 at `:114` and RUF100 at `tests/scripts/test_supervise_change.py:7` were there before w206.

### Verified, no finding

These are as review 5 found them, and the code is unchanged since:

- `list --json` now gives `{"request", "status"}`, which is what r35 asks for.
- An unreadable `raised.jsonl` line raises `Refused`, naming the file and the line (r7), with no traceback.
- `own` is the round's `name`, the same key as `held.stem`.

## Checks

- `tools check --base 694a5f8e`:
  - ruff: 4 findings (B023 twice at `supervise_change.py:88`, new; B023 at `:114` and RUF100, both from before w206).
  - vulture: clean.
  - import-linter: "the project states no import contracts".
- `tools size --limit 300`: printed nothing, so no file is over the limit.

## Commands run

- `git log --format=%H -1 --grep="^work: w206 ready -> claimed$"` and the same for `claimed -> done`
- `git log --oneline -1 work/w206` (failed: no such branch)
- `git log --format='%h %s' 694a5f8e..HEAD`
- `git show --stat 85589330 61fb5d8d b5bf81a4 7abd1e9e`
- `git show e4e61321 -- scripts tests features`
- `git diff --stat e4e61321 HEAD -- scripts tests features`
- `cat .shop/work/requests/q20.md`
- `python3 <Scripts>/tools check --base 694a5f8e…`
- `python3 <Scripts>/tools size --limit 300`
