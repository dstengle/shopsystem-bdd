# Research of w111 (delivery r17, r18)

Tools: `tools` at the plugin path (probe: coverage, ruff, vulture, import-linter, hypothesis present). No coverage map: `tests-of` says `no map`; making one runs the suite, so tests are found `by search`. `refs workqueue.add` gave 0 references (not trusted; `scripts/work:16` found by search).

Work-item accepts delivery#r17, delivery#r18. The brief gives no `Accepted scenarios:` line and no fileset; the work-item has no `## Retires` section and no `fileset:`.

## 1. Why each scenario is red today

No accepted scenario exists. Search: `grep @r17|@r18` in `features/` gives 13 hits, none under delivery: `features/supervision.feature`, `design-model-check.feature`, `migration-tools.feature`, `analysis-tools.feature`, `feature-file-tools.feature` (by search). There is no `features/delivery.feature` (glob, by search; `git log -- features/delivery.feature` empty). Formulation commit e4ee75b (`git show --stat`) adds scenarios for other capabilities only; the proposal `drafting-retires` (status `formulated`, `adds: [delivery#r17-r18]`) has none. Nothing to run red. `none`.

## 2. What the system answers today

Scratch repo probe, run: `python3 -m pytest -q -s -n 0 .shop/scratch/w111-1-research/probe_retire.py` (`test_deprecated_json_on_a_retire_list_probe`, `test_work_add_on_a_scratch_repo_probe`).

- `features deprecated --json` on a file with `@r17 @deprecated` "Old way (deprecated)" and `Deprecated for: New way`, plus `@r17` "New way":
  `{"deprecated": [{"file": "features/f.feature", "title": "Old way (deprecated)", "deprecated_for": "New way", "replacement": {"file": "features/f.feature", "tags": ["r17"]}}]}` (run).
  It gives the replacement's tags, not the deprecated scenario's own `@r<n>`. r17 needs the latter: read the file's tags (run).
- `work add i1 "Retire probe" --part-of capability-proposal/p1 --under delivery --accepts delivery#r17` with `spec/index.md` present: prints `w1`, writes `.shop/work/i1/w1.md` as frontmatter (`status: drafted`, `accepts: [delivery#r17]`) plus `# Retire probe`, and commits it itself: `437fe71 work add: i1/w1 drafted`; `git status --porcelain` empty afterwards (run).
- `work add` without `spec/index.md`: `work: spec/index.md, which names the context, is missing`, exit 1 (run, first attempt).
- `work add` with `--retires x`: argparse `unrecognized arguments`, exit 2 (run). `work add --help` lists only `--part-of --under --accepts` (run).
- `work add` without `--accepts`: exit 2, `the following arguments are required: --accepts` (run).
- Refusal: initiative directory missing, `the initiative ... does not exist` (read, scripts/workqueue.py:86).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:add (lines 93-96) | writes a work-item of frontmatter and title only, then commits it (`committed`) | a `## Retires` list must reach the file: a flag, or an edit after the commit | none by search for the Retires case; tests/scripts/test_work_add_title.py, tests/scripts/test_work_item_ids.py, tests/scenarios/work_queue_add_steps.py run it (by search) | read, probe |
| scripts/work:cmd_add, argparse (lines 53-58) | no `--retires` option | same; a new option changes the CLI | tests/scenarios/test_work_queue.py (by search, `work add`) | read, probe |
| skills/delivering-an-initiative/SKILL.md "Commit them, alone" (lines 39-41) | assumes `work add` leaves files uncommitted, so the skill commits them | `work add` commits each work-item already (probe); a Retires edit after it needs a second commit | none (no test reads the skill) | probe |
| skills/delivering-an-initiative/SKILL.md "Before anything" and "Drafting" (lines 18-37) | no check on scenarios the formulation added or reworded | r18: stop, name the scenario, commit nothing | none | read |
| scripts/features `deprecated --json` (scripts/features_report.py:deprecated_entry) | reports the replacement's tags, not the deprecated scenario's | r17 needs the deprecated scenario's `@r<n>` | tests/scripts/test_features_scenarios.py:test_the_deprecated_list_shows_each_deprecated_scenario_and_what_will_retire_it, tests/scripts/test_features_deprecating.py (by search) | probe |
| skills/bdd-red-green/SKILL.md:60, agents/bdd-implementer.md:25, agents/bdd-task-reviewer.md:35, agents/bdd-branch-reviewer.md:44, agents/code-scout.md:15 | read `## Retires` by hand, as a list of quoted titles | a list written by r17 must keep this shape (`"<title> (deprecated)"` as in w110) | none (by search: no test reads a Retires list) | read |

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map: `by search`. Searched tests for `Retires`, `work add`, `deprecated --json`: no test asserts a work-item file has no `## Retires` section, and none reads the delivering skill. Read of tests/scripts/test_work_add_title.py (heading only), tests/scenarios/work_queue_add_steps.py (id and file) and features/work-queue.feature:118, 178 (commit of work add): all stay true if `add` gains an optional section. Result: none that can no longer pass.

## 5. A step the work-item skips

Retires written after `work add`: `work add` already commits the work-item (probe). The skill's commit step (SKILL.md:39-41) then finds nothing to commit, and an edit to add `## Retires` is a change that is not committed. Effects the existing step produces and a new path skips: the `work: draft <initiative>` commit (read, SKILL.md:41); `work add` refusals `spec/index.md missing` and `--accepts required` (run). r18's stop check is a step with no existing counterpart: read.

## 6. Defects

None shown by the probes. The `deprecated --json` shape (section 2) is a gap for r17, not a wrong answer.

## 7. The file set

Files the work-item must change (by read, probe):
- skills/delivering-an-initiative/SKILL.md (70 lines; prose, outside the 300-line rule): add the Retires list and the r18 stop; fix the commit step for `work add`'s own commit.
- scripts/work (80 lines, room 220): only if `work add` gains `--retires`.
- scripts/workqueue.py (262 lines, room 38): only if `add` writes a `## Retires` section.
- tests/scripts/test_work_add_title.py (50 lines), tests/scenarios/test_work_queue.py (282 lines, room 18), tests/scenarios/work_queue_add_steps.py (60 lines): keep passing if `add` changes; not edited unless it does.
- features/delivery.feature: missing; r17 and r18 need scenarios from a formulate round (not the work-item's file set). Open question below.
- spec/capabilities/delivery.md (46 lines): unchanged.

Modules on the path: scripts/features (148), scripts/features_report.py (116), scripts/features_edit.py (131), scripts/work (80), scripts/workqueue.py (262). None over 300 (`tools size --limit 300` printed nothing).

## Questions for the plan

- r17 and r18 have no scenarios: no `features/delivery.feature`; formulation e4ee75b did not write them. Both readings: (a) formulate them before this work-item runs; (b) the work-item lists no scenario and `work run` reads the requirements only.
- r17 write path: a `--retires` option on `work add` (scripts/work, scripts/workqueue.py), or an edit by the skill after `work add`'s commit (a second commit).
