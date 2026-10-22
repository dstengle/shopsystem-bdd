---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-06-agent-efficiency-sdd-final-fix
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-07
---

# Agent efficiency final fix wave report

Fixer report for the final review's fix wave of the 2026-10-06 agent-efficiency run (0.10.0), commits 72d33af..34279e8: the seven findings addressed, with the RED and GREEN unittest output (38 tests).

Archived from `.superpowers/sdd/2026-10-06-agent-efficiency/final-fix-report.md` (git-ignored scratch), text as it was.

---

# Final fix wave report — agent-efficiency 0.10.0

Commits:
- 1200891 scripts: archive keeps open questions and re-logs the last Suite: entry; move --carry-feature-tags
- 34279e8 Prose: Scripts: in every task, NEEDS_CONTEXT on a missing script, fix-wave suite run, plan status for green, porcelain noted before dispatch, carry feature tags and archive's kept entries

## 1. archive hid the suite record

- scripts/plan:261 — after the note line (kept unchanged, still `...; last <Suite line>`), the last `Suite:` entry is re-logged verbatim (with any continuation lines) as its own bullet, so `show --last-suite` finds it.
- scripts/plan:28-32 — contract: "...one line naming the archive and the last 'Suite:' line, and that 'Suite:' entry again, so show --last-suite still finds it".
- tests/scripts/test_plan.py:169 `test_last_suite_holds_after_archive` (new): git fixture, checkpoint commit, archive, commit, `show --last-suite --current` prints the record and `current`, exit 0.
- tests/scripts/test_plan.py `test_archive_moves_green_slices_and_log_keeping_requests`: exact-ending assertion extended by the re-logged `- 2026-10-01 Suite: ...` line, consistent with the new contract. `test_archive_keeps_continuation_lines_with_their_entries` unchanged and passing.

## 2. archive moved open questions out

- scripts/plan:47 `KEPT = r"^- \S+ (REQUEST |RE-FORMULATE\b|QUESTION FOR THE SPEC:)"`; scripts/plan:250 keeps those entries (continuation lines included), in log order, before the note.
- scripts/plan:28-32 — contract names REQUEST, RE-FORMULATE and QUESTION FOR THE SPEC: entries.
- skills/slicing-into-increments/SKILL.md:109 — archive paragraph: keeps the `REQUEST`, `RE-FORMULATE` and `QUESTION FOR THE SPEC:` entries, and the note is followed by the `Suite:` entry.
- tests/scripts/test_plan.py:157 `test_archive_keeps_open_questions_in_the_log` (new): RE-FORMULATE with a continuation line and a QUESTION FOR THE SPEC stay; an ordinary entry goes.

## 3. migration stopped on feature-level tags

- Default carrying would break `test_verify_catches_a_lost_feature_tag`, so carrying is behind `--carry-feature-tags` (scripts/features:360). With it, the source file's feature tags the destination file's feature tags lack go on a tag line of their own just above the Scenario: line, at its indentation (scripts/features cmd_move). Own line rather than joined to the last tag line, so a trailing `# comment` on a tag line cannot swallow them.
- scripts/features:27-29 — contract text.
- skills/migrating-to-capabilities/SKILL.md:26 — step 4's move command carries `--carry-feature-tags` "(the old file's feature tags go onto the scenario)".
- tests/scripts/test_features.py:141 `test_move_carrying_feature_tags_verifies` (new): tagged `@cart` source into untagged destination with the flag; the moved block has `@slice-1\n  @cart\n  Scenario: ...`, and `verify-moved` prints `3 scenarios match`. All existing tests unchanged and passing.

## 4. Scripts: did not reach the implementer

- skills/slicing-into-increments/SKILL.md:73 — Global Constraints carry `Scripts:`, and each task repeats that `Scripts:` line, since a task brief carries its task's section, not the Global Constraints.
- agents/bdd-implementer.md:21 — `Scripts:` is in the brief; only empty output with exit 0 means no record; a brief without `Scripts:`, or a script that exits non-zero or is not found, is `NEEDS_CONTEXT`, never "no record".

## 5. fix-wave whole run

- agents/bdd-implementer.md (resumed-with-findings bullet): "After the last fix commit, run the whole suite once and log its record as in the checkpoint."

## 6. Status set with sed

- skills/bdd-red-green/SKILL.md:98 — "set the slice's Status with `plan status <n> green`".
- agents/bdd-implementer.md:25 — checkpoint commit: "the slice's Status set with `python3 <Scripts>/plan status <n> green` and its entries written with `python3 <Scripts>/plan log`".

## 7. porcelain check assumed a clean tree

- skills/integrating-a-proposal/SKILL.md:16-17, skills/formulating-features/SKILL.md:16-17, skills/migrating-to-capabilities/SKILL.md:21-22 — step 1 ends "Then note `git status --porcelain`." (after the `.gitignore` commit, before dispatch); step 2: "check `git status --porcelain` matches the porcelain noted before dispatch: only an entry new since then is the agent's, and an agent that wrote outside the drafts path goes back with those files removed." formulating-features:95 ("as in step 2") inherits it.

## RED (before the script changes, tests added first)

```
....F................FF....F..........
FAIL: test_move_carrying_feature_tags_verifies
AssertionError: 2 != 0 : ... features: error: unrecognized arguments: --carry-feature-tags
FAIL: test_archive_keeps_open_questions_in_the_log
AssertionError: '- 2026-10-03 RE-FORMULATE cart / Adding several\n  evidence: red\n- 2026-10-03 QUESTION FOR THE SPEC: clamp or raise?\n- 2026-10-06 Batch 14' not found in '...## Log\n- 2026-10-02 REQUEST shopsystem-kb: kb serve is not built\n- 2026-10-06 Batch 14 archived to archive/cart-slices-14.md; last 2026-10-01 Suite: ...\n'
FAIL: test_archive_moves_green_slices_and_log_keeping_requests
AssertionError: False is not true   (ending lacked the re-logged Suite: entry)
FAIL: test_last_suite_holds_after_archive
AssertionError: 1 != 0 : plan: no suite record
Ran 38 tests in 1.253s
FAILED (failures=4)
```

## GREEN / final run

`python3 -m unittest discover -s tests/scripts -v`: all 38 ok (35 previous + 3 new).

```
Ran 38 tests in 1.273s

OK
```

## Concerns

- None blocking. The re-logged Suite entry means the living log shows the record twice (inside the note and as its own bullet); the note was kept as instructed.
- No headless runs (per ruling).
