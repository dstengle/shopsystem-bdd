---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-16-release-review-0-35-2
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-16
---

# Release review 0.35.2

A fresh agent's adversarial review of the branch `plan-release-0.35.2` (five commits) against `.shop/records/2026-11-16-release-0.35.2/plan.md`, each claim of the notes tested in scratch directories with the branch's scripts. Verdict: do not merge as 0.35.2 until the regression of finding 1 is settled, and drop the false hook clause of finding 2. The session held the release, recorded finding 1 as `.shop/batches/40/defect-1.md` against b300, shaped its fix b328 (built in batch-42), corrected findings 2 and 3 on the branch, generalized the test of finding 6 on main, and added finding 4's reproduction to b323. The release goes on under plan-2.md.

## Findings

1. **Blocks the merge.** b300 made `<T>_<K>_Every` an argument of K's own slot, which gives "every K in the Y, ordered by T" after a verb whose frame names K a second reading beside `r<n>_in_By_<T>`. In a copy of grammar/corpus/constructs/spec, "When the person runs `work start` on a worktree, `work` shall give every file in the worktree, ordered by version, in ascending order to the person." gives `refused: more than one meaning: ... reads 2 ways` with the branch's scripts, and one form with the 0.35.1 `orders` hunk. A line that parsed is refused: a y change under decision 0092 unless fixed.
2. **Fix before merge.** CHANGELOG's b303 bullet said the SessionStart hook kept offering the upgrade; `session_text` returns "" with no step pending (migrate_upgrade.py:105-107). Checked on a scratch repository at 0.34.1: `migrate status --hook` printed nothing; `migrate upgrade` recorded 0.35.2 and committed; a second run changed nothing.
3. **Observation.** docs/reference/commands.md's `migrate upgrade` did not say it records the release with no step pending.
4. **Observation, a defect of b14 on main.** `backlog_reword._retiring` finds the id a line retires by searching the item's history for `<id> retires`; item line ids are reused after a remove, so removing a plain line can drop an id that `--no-line` retired. Reproduced on a clone: `retired: [r40, r41]` became `[r40]`. Already b323.
5. **Observation.** writing-requirements says "after any verb whose frame takes K"; it also works when the frame takes a kind above K.
6. **Observation.** The branch's change to tests/scripts/test_decision_checks.py (0086-0088 keep `tier: check` once superseded) is consistent with `work decision --supersedes` (only `status:` rewritten) and `model decisions` (superseded decisions never run), but hard-coding the three files is brittle.

## Checked and holding

Version strings; `git diff --stat v0.35.1 main -- features/` additions only; b14's `--reword` and `--remove` and their refusals; b271's `--no-line` and its refusals; b179's `--supersedes` and its refusals; b310's precondition read and generated; b300 on give, a subkind, end and "every report from the stage", and an order still refused in a While clause, a trigger and after shall not; b203's one-word fix; the docs tests and `model decisions --check`.
