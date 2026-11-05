---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-7-rulings
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# Plan 7 of the workflow simplification: rulings on the review, and what was done with each finding

`plan-7-review.md` (committed in `abbe4847`) asked the person three questions. The person was not available. Each
ruling below was **ruled by the main session without the person, 2026-11-05; revisit.** The fixes are on branch
`workflow-simplification`, from `e7b604e5` to this record's commit, not pushed.

## Rulings

| # | Question | Ruling (main session, without the person, 2026-11-05; revisit) | What was done |
|---|---|---|---|
| Q1 (B1) | How do the reviewer's findings reach the findings file? | As the reviewer's reply. Write leaves `pr-reviewer`'s tools; the batch session saves the reply byte for byte at the brief's `Findings file:` path (saving is not editing), then runs `work batch reviewed`. The file is not renamed to get past the harness's guard. | `e7b604e5`, `7cd94c5b`: see B1. |
| Q2 (S2) | Is a subagent that dispatched a counted batch subagent the batch's driver? | Yes: `planning`, counted like a main session (its requests inside the window), and S2's summary lines in any case. | `6f3f2865`: see S2. |
| Q3 (S1) | What do `changed_lines` cover? | The whole batch as last reviewed, `forked_from..<last review head>`; each review keeps its own `lines`. | `ab76ced7`: see S1. |

## The findings

| # | What was done |
|---|---|
| B1 | Fixed as ruled (Q1) in `e7b604e5`. `agents/pr-reviewer.md` has tools Read, Glob and Grep; its last section reads "Your final reply is the findings file's content and nothing else, starting at `## Verdict`", and its triage and findings-file sections say the findings are given in the reply. building-a-batch step 7 saves the reply byte for byte at the brief's `Findings file:` path, then runs `reviewed`; "Saving is not editing" is said, and the refused-`reviewed` bullet saves the fresh reviewer's reply the same way. The brief gains a `Reply:` line after `Findings file:` (`scripts/batch_brief.py`), and `reviewed`'s missing-file refusal says "and save its reply there". The pr-review Implementation section, README's agent table, `batch_findings`' docstring and `reviewed`'s help say the same. Tests (each red first): `test_the_findings_travel_as_the_reply` and the tool lists of `test_r3_…` and `test_the_reviewer_changes_nothing_…` (no Write), `test_r8_…`'s sentence, the skill's "byte for byte at the brief's `Findings file:` path" and "Saving is not editing", and the brief's `Reply:` line. `7cd94c5b` parenthesises the `Reply:` string for ruff. |
| S1 | Fixed as ruled (Q3) in `ab76ced7`. `knobs.changed_lines` is numstat over `forked_from..<last review head>`, `.shop/` left out, and each entry of `reviews` gains `lines`, its own range's count. `test_the_knobs_are_given` now checks both on the `merged` fixture (two reviews); it failed first. The telemetry Implementation section says so. |
| S2 | Fixed as ruled (Q2) in `6f3f2865`. `measure_batch_read.parents` reads `parentAgentId` from the meta files. In `sessions_of`, a subagent that is not counted whole (its first request is before the window) but is the parent of one that is, is the driver: `planning`, its requests inside the window counted. Each session entry gains `driver`. `summary` adds `no main session in the window at <dir>: … needs --sessions <the main session's directory>` when no main session or driver is counted, and `no session in the window at <dir>; …` when transcripts were found but none was counted (deviation 3). Tests: `test_the_subagent_that_drove_the_batch_plans`, `test_a_subagent_that_is_its_own_batch_subagents_parent_is_counted_whole`, `test_the_parents_are_read_from_the_meta_files`, `test_the_summary_says_when_no_main_session_was_counted`, `test_the_summary_says_when_no_session_was_in_the_window`. |
| M1 | Fixed in `6f3f2865`. D6 rule 4 (implementing before the first review, fixing after) applies only to a subagent with no description; one described otherwise is `planning`, the session's own helper work. Test: the `Explore` "Find the parser" case. |
| M2 | Fixed in `6f3f2865`. `role_of` takes the measured batch's name, and only `<that batch> review|fix|t<k>` gives a role; another batch's description falls to M1's `planning`. Test: the `batch-7 review 3` case. The existing role cases pass `batch="batch-1"`. |
| M3 | Fixed in `309ffdf1`. The key `claude-opus-4` is gone. `claude-opus-4-6`, `-4-7` and `-4-8` are priced $5 / $25 / $0.50, the models the claude-api skill's table (2026-10-06) states. An older Opus 4 (4.0, 4.1 and 4.5, which that table does not list) is unpriced and named. Claude Haiku 5.5 takes its long rate when a request's prompt (new input, cache writes and reads) is over 100K tokens. The skill gives $0.50 / $2.50, and its migration guide says cache reads are 0.1 × input, so $0.05 (`measure_cost.LONG`). An override of `claude-haiku-5-5` in `.shop/delivery.toml` sets both rates. Tests: `test_an_opus_4_the_table_states_no_price_for_is_unpriced` (3 ids), `test_opus_4_6_to_4_8_are_priced`, `test_haiku_5_5_over_a_100k_prompt_takes_its_long_rate` (exactly 100K is the short rate). `claude-sonnet-4` and `claude-haiku-4` still match by prefix, as before: Sonnet 4.6 and Haiku 4.5 are what the table states, and an older Sonnet 4 is priced at Sonnet 4.6's rate. |
| M4 | Fixed in `6f3f2865`. A row with no `requestId`, `message.id` or `uuid` is keyed by (session, agent, time), so the same row in two files counts once. Test: `test_a_request_with_no_id_in_two_files_is_counted_once`. |
| M5 | Fixed in `6f3f2865`. A session none of whose requests is priced has `cost` None, and `show` prints `-`. The role and batch totals add its cost as 0, and `unpriced` names it. Test: `test_a_session_priced_nowhere_has_no_cost`. |
| M6 | Fixed in `2ba3c236`. `compare` of two batches refuses a record that lacks any of `tokens`, `cost`, `defects`, `findings_by_grade` or `knobs`, naming the missing figures and `measure batch <batch> --replace`. Test: `test_a_batch_record_compare_cannot_read_is_refused`. |
| M7 | Fixed in `2ba3c236`. `compare` gives `items`, `changed lines` and `reviews`, from the knobs, last, each with its ratio. Test: `test_compare_gives_the_sizes_beside_the_ratio`. The contract in `scripts/measure` and the telemetry Implementation section say so. |
| M8 | Fixed in `ae62317a`. building-a-batch says that the batch session runs `measure batch` and commits its record, after `merged` and after `abandon`. analyzing-a-batch step 1 reads that measurement (`measure show`) and runs `measure batch` only when there is none, and it carries "no main session in the window" into the report. Tests: `test_it_reads_the_measurement_building_a_batch_wrote`, `test_an_abandoned_batch_is_measured_too`. |
| M9 | Fixed in `aeff18e6`. `scripts/measure` prints `measure <command>: <why>`, and `measure defect` and `compare` no longer prefix their own refusals. Tests: the D11 refusal cases check that stderr starts `measure defect: ` and names `measure` once, `test_an_unknown_item_is_refused_naming_the_command` (`b9`), and the mixed-pair compare case. |
| M10 | Corrected in this record's commit. D5 in `plan-7-telemetry.md` now says that Claude Code writes caches of either time to live: the smoke run's 5 requests all wrote 5 min caches. D5's key list notes M3's change. |

Two tests went red only through the new signature, not through new behaviour: the `batch-1 review 3` and no-meta cases of `test_a_description_gives_a_role_only_for_this_batch`. They guard the behaviour that was kept.

## Not done here

- `CLAUDE.md`'s row for `scripts/batch_findings.py` still says "the findings file `pr-reviewer` writes". The row is
  left for the main session, since this agent does not edit `CLAUDE.md`. It should read "the findings file
  (`pr-reviewer`'s reply, saved by the batch session)". The module-map rows of `measure_batch_read.py` and
  `measure_batch_sessions.py` could name `parents` and the driver.

## For plan 9

- The old `bdd-branch-reviewer` and `bdd-task-reviewer` hit the same harness refusal of a subagent's Write of
  `findings.md`. In the review's sweep, 2 of the 4 refused writes were `bdd-branch-reviewer`'s. That is one more
  reason to retire them with `work run`.

## Figures after the fixes

| Check | Result |
|---|---|
| Suite (`python3 -m pytest -q`) | **1481 passed**, 1 skipped, 4 xfailed, 135 subtests passed (30.9 s). That is 22 more passes than plan 7's 1459. The ceiling report lists `test_e2e_codified` (13.8 s) and `test_supervision`'s flaky-scenario test (12.3 s), as before. |
| Timing run (`python3 -m pytest -m timing -n 0 -q`) | `2 passed, 1486 deselected` |
| Unbuilt | `False 5 []` |
| `model check` / `logic` / `lexicon --check` | 53 / 16 / 19 / 0; `11 findings: 6 L5, 5 L6`; `401 terms, 0 problems` |
| `model decisions --check` | `4 check decisions: 4 hold, 0 failing` |
| `features generate --check` / `vocab --check` / `bindings --unbound` | exit 0; `every step has one handler`; `every binding names a scenario` |
| `tools size --limit 300` | silent, exit 0. Own limits: `scripts/measure` 143 (≤ 150), `measure_show.py` 122 (≤ 135), `measure_write.py` 42 (≤ 50) |
| `tools check $(git diff --name-only 9d765bb8...HEAD -- '*.py' scripts/measure)` | ruff "All checks passed!", vulture clean, no import contracts |
