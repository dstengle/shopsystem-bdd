---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-job-migration-release-integration-report
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-19
---

# Integrating i10, i11 and i8 into release-0.21.0: the coordinator's report

The coordinator's report on integrating the drafts of i10, i11 and i8 into branch release-0.21.0 as commit b0231c6 (2026-10-19, unapproved): where each draft went, how the five capability files two initiatives changed were merged, id collisions and blocked_by links added, `model check`'s counts after the integration (382 violations, 23 warnings, 35 unresolved, 248 file problems, each explained), the test run, and the 53 work-items in build order. The drafts are decision-argument/2026-10-19-job-i10-delivery-drafts and decision-argument/2026-10-19-job-i11-i8-final-layout-and-migration-drafts. Copied out of a job workspace on 2026-10-22.

Archived from `.shop/scratch/from-job/integration-report.md` (git-ignored scratch), text as it was.

---

# Integration report: i10, i11, i8 into release-0.21.0

Commit `b0231c6` on release-0.21.0 (not pushed): "spec: the migration release's drafts (i10, i11, i8), unapproved".
None of it is approved. 22 capability-proposals and 53 work-items are `drafted`, 15 decisions are `proposed`,
and i10, i11 and i8 are still `proposed` with their priorities unchanged (1, 2, 3).

## Placement

- `scripts/model` `read_work` reads only `work/<initiative>/*.md`, one level and not recursive. So each
  work-item sits beside its proposals in the initiative's directory, as `work/i2-model-check/model-check-1.md`
  already does. No `work-items/` subdirectory was made.
- The three initiative.md files were replaced by the drafts. Their id, status and priority were already the same.
- i10 has 14 proposals and 29 work-items in `work/i10-delivery-on-v3/`. Its other two work-items,
  `spec-integration-1` and `-2`, are in `work/i1-first-spec/` under `capability-proposal/first-spec-spec-integration` (ruling Q7).
- i11 has 6 proposals and 15 work-items in `work/i11-final-layout/`.
- i8 has 2 proposals and 7 work-items in `work/i8-model-in-consumers/`.
- Decisions 0037-0050 were copied into `decisions/` (the old location) and 0053 was written there.
  `scripts/model decisions` regenerated `spec/decisions.md`, and `--check` says it is current.

## Capabilities

The files only one initiative changes were copied whole from its draft:
- i10: code-research, delivery (new), planning (new), red-green, review, role-boundaries, spec-consistency,
  supervision (new), work-queue (new)
- i11: batch-measurement, spec-integration
- i8: migration-tools (new)

Five files were merged. Each was a three-way merge against the base (`git merge-file`), with conflicts settled line id by line id.

**analysis-tools** (i10 + i11, no conflict). From i10: r4 (`tools probe --log` no longer names `plan log`).
From i11: `formulated_as` dropped, r8 (`.shop/scratch/tools/coverage`), and r14 in plain words.

**spec-migration** (i10 + i8, no conflict). From i10: r1 (stop when a work-item is `claimed`, in place of
a slice in progress). From i8: everything else, meaning the new Purpose and rests_on, `formulated_as`
dropped, r4, r9, r11, r13 and r14 changed, r15-r23 added, and the Implementation (`.shop/scratch/migration/`, `scripts/migrate`).

**formulation** (i10 + i11, 2 conflicts):
- r4: both drafts changed it. Merged as the union of the two: i11's `@deprecated`, " (deprecated)" and
  `Deprecated for:`, ending in "until the work-item that turns its replacement green retires it". That joins
  i10's "a work-item" to i11's "the work that turns its replacement green".
- r10: i10's text (a work-item's implementer hands back a scenario and the person rules on it). i11 did not change r10 in substance.
- r11 and r12: i11's text ("has the tag", `@deprecated`).
- Not in conflict: r1, r6 and the Implementation came from i11, and i10's rests_on and Implementation lines were kept.

**feature-file-tools** (i10 + i11, 7 conflicts):
- Frontmatter: rests_on is i11's, with plugin-scenarios-run-as-pytest-bdd added. `formulated_as` is dropped
  (i11, decision 0047). `retired` is i10's list: r8, r9, r30-r34, r43-r45, r47-r50.
- Purpose: a union of the two. From i10: "sets a scenario's requirement tag", with no `slice_expectations.py`.
  From i11: "deprecates" and "checks that every scenario has exactly one test binding it".
- r10: i11's plain words. r11: i10's text (only `r<n>`).
- r18-r24: i11's text (deprecate, deprecated). For r21, i10 only removed the slice clause, and i11's
  rewrite has no slice clause either, so i11's text covers both drafts.
- r35, r39, r41, r51: i11's text.
- r40: both drafts changed it. Took i11's text ("or whose replacement has no `@r<n>` tag"), which also
  meets i10's aim of having no slice tag.
- r57-r59: i11's additions. They did not collide with i10, which added no ids here.
- The retired slice lines were dropped, even though i11 had reworded r8 and r45.
- Implementation: the `tag`/`deprecate` bullet is a union. It keeps i10's "replaces the first `@r<n>` tag
  or adds one" and i11's `deprecate`. The bindings and Output bullets are i11's. The `plugin` and
  `slice_expectations.py` bullets are dropped (i10).

**design-model-check** (i10 + i11, 6 conflicts):
- Frontmatter: rests_on is i11's list (final-layout, references-are-ids, light-decisions; no
  plugin-adopts-the-design-model) with i10's one-requirement-form and review-of-work-items added.
  `formulated_as` is dropped. `retired: [r42, r45]`: i10 retired r42 and i11 retired r45.
- r2-r8 and r59: i11's plain labels.
- r6 was changed by both drafts. It is now one line: i10's "that is `drafted` or `approved`" plus i11's
  label "a proposal changes a requirement no capability has".
- r22 and r24: i10's text (no `#behaviour/r<n>`; `fixes` and `findings`). i11 had not changed either.
- r23 was changed by both drafts and is now one line. It starts from i10's text: a `merged`, `formulated`
  or `withdrawn` proposal may name a retired id in `adds`, `changes` or `removes` without a report. It adds
  i11's point: "an id it removes being read as that requirement".
- r43: i10's text. r44: i11's text (`@deprecated`, "has").
- i11's r60-r66 kept their numbers. **i10's r60 is renumbered r67** (see Ids below).
- Not yet: i10 dropped "A work-queue view". i11 had kept it and changed its trigger to i10, but the
  work-queue capability now covers it, so it is dropped.

**Plain-word fixes to i10's lines.** These came from i11's glossary (**deprecated scenario**; `carry` in
requirement's Not: list), as i11's NOTES asked:
- delivery r4 and r7: "carries a check" became "has a check"
- red-green r11: "the plan carries code" became "contains code"
- red-green r17: "the work-item that holds it" became "whose claim has it"
- supervision r15: "holding the path" became "whose claim has the path"
- the same kind of rewording in prose: code-research r3, work-queue r19, review r12, the planning Purpose,
  red-green's Purpose, the supervision Implementation, and the role-boundaries Implementation

**Decision 0053 (`design-decision/the-v3-agents`, light form, proposed).** It lists the ten v3 agents, with
their tools and models, `bdd-planner` among them. It supersedes rules-held-by-agent-tools (0020) and
model-pinned-in-agent-definitions (0021), because the drafted role-boundaries r2, r5 and r6 restate both.
The rests_on of role-boundaries, review and supervision, and the Constraints in spec/index.md, now cite it
in place of 0020 and 0021. 0020 and 0021 stay `accepted` until the gate. No 0051 or 0052 was created.

## spec/index.md

It is i11's `spec-index.md` with i10's changes added:
- Purpose: "work-items pulled through their stages by a script supervisor" in place of thin vertical slices.
- Constraints: the superpowers constraint is removed.
- Composition: the build side is "started by the supervisor", with delivery, code-research, planning,
  red-green, review and role-boundaries under their new narrators. The tools section gains work-queue,
  supervision and migration-tools. No capability was removed.
- Testing: workflow scenarios run as fixture sessions under pytest-bdd (decision 0043).
- Glossary:
  - From i11: **deprecated scenario** (Not: held, holding, superseded), and **requirement** with carry,
    carries, carried, carrying in its Not: list (ruling Q1).
  - From i10: **work-item**, **file set**, **claim** and **ruling**. The **claim** entry is reworded to
    avoid "hold": "the file set a claimed work-item has to itself…".
  - batch, controller and slice are left for i12 (ruling Q11).
- Where things live: `.shop/delivery.toml` and `.shop/worktrees/` are added.
- State: names the migration release's drafts.

## Ids

- design-model-check: both drafts added r60. i10's r60 (`#behaviour/r<n>` is unresolved) is now **r67**,
  one above i11's highest id, r66. Fixed in `delivery-on-v3-design-model-check.md` (`adds`, body) and
  `design-model-check-2.md` (`accepts`, body). No other new ids collided.
- References to the ids i10 retires were removed:
  - `final-layout-feature-file-tools` `changes` no longer has feature-file-tools#r8 or #r45, and its body notes it.
  - `feature-file-tools-scenarios` `accepts` no longer has r8, r9, r30-r34, r43-r45 or r47-r50.
  - `design-model-check-scenarios-2` `accepts` no longer has #r42.
- blocked_by links added so that i11 comes first (Ruling 2, and i10's NOTES):
  - formulation-1 and work-queue-1: pytest-bdd-suite and final-layout-read
  - design-model-check-2: proposal-lists-read (both change r23)
  - analysis-tools-1: analysis-tools-scenarios
  - feature-file-tools-1: every-scenario-bound

## model check (`--limit 100000`): 382 violations, 23 warnings, 35 unresolved, 248 file problems

| code | rows | what |
|---|---|---|
| v_s3 | 260 | lines not formulated yet (expected) |
| v_w4 | 29 | work-items whose every accepted line has no scenario yet (expected) |
| file problems | 248 | all "accepts … which no scenario names yet" (expected) |
| v_s1 | 16 | old scenarios of retired lines: feature-file-tools r8, r9, r30-r34, r43-r45, r47-r50, design-model-check r42, r45 (expected) |
| v15c, v15d | 17 each | the same 16 scenarios naming retired ids, plus code-research#r2 named by its drafted proposal's `removes` |
| v15e | 1 | i3's merged requirement-ids-design-model-check changes the now-retired dmc#r42. This is the gap in question 9, which dmc#r6's change fixes. |
| v_t1 | 42 | 7 on capability lines, all literal `@holding` or " (held)" (dmc r51 and r62, migration-tools r2 and r27, spec-migration r18), which r51's change fixes. 35 on scenarios (feature-file-tools, design-model-check, batch-measurement), which rename-sweep, formulation-deprecates and batch-measurement's reworded steps fix. |
| warnings | 6 + 17 | w_uncited_obs and w_unserved_cap |

The 35 unresolved references are three kinds, all left on purpose:
- **16** are the same old scenarios, now naming retired ids. Formulation deprecates or removes them.
- **17** are drafted proposals whose `removes` names an id the capability file already retires: i10's
  feature-file-tools (14), design-model-check r42, code-research r2, and i11's design-model-check r45. This
  is a side effect of the capability files taking the proposed text before the merge. It clears when the
  proposals merge and dmc#r23's change is built.
- **2** are `term/deprecated-scenario` and `term/requirement` in i11's proposal. Ruling Q10 says model check
  will read them, which is dmc#r66 (work-item proposal-lists-read).

There are no id collisions, no file-read problems, and no unresolved `part_of`, `blocked_by`, `rests_on` or `supersedes`.

## Tests

`python3 -m unittest discover -s tests` runs 0 tests, because `tests/` is not a package. The suite as
spec/index.md names it, `python3 -m unittest discover -s tests/scripts`, ran 335 tests: OK, 1 skipped.
**No test fails.** The tests bind by scenario title, and no feature file changed. The scenarios of the
retired and changed lines still pass against today's code until their work-items change it.

## Work-items in build order (a topological order, Ruling 2: i11, then i10, then i8 through `work run`, removals last)

1. pytest-bdd-suite (i11): none
2. analysis-tools-scenarios (i11): pytest-bdd-suite
3. design-model-check-scenarios-1 (i11): pytest-bdd-suite
4. design-model-check-scenarios-2 (i11): design-model-check-scenarios-1
5. feature-file-tools-scenarios (i11): pytest-bdd-suite
6. bindings-unbound (i11): feature-file-tools-scenarios
7. deprecate-commands (i11): feature-file-tools-scenarios
8. final-layout-read (i11): design-model-check-scenarios-2
9. deprecated-and-sources (i11): final-layout-read
10. decision-files-taught (i11): deprecated-and-sources
11. proposal-lists-read (i11): design-model-check-scenarios-2
12. rule-labels (i11): design-model-check-scenarios-2
13. every-scenario-bound (i11): analysis-tools-scenarios, deprecate-commands, bindings-unbound, final-layout-read, rule-labels, deprecated-and-sources
14. rename-sweep (i11): deprecate-commands, deprecated-and-sources, rule-labels
15. formulation-deprecates (i11): deprecate-commands, rename-sweep
16. work-queue-1 (i10): pytest-bdd-suite, final-layout-read
17. work-queue-2 (i10): work-queue-1
18. work-queue-3 (i10): work-queue-1
19. supervision-1 (i10): work-queue-2, work-queue-3
20. supervision-2 (i10): supervision-1
21. supervision-3 (i10): supervision-2
22. supervision-4 (i10): supervision-3
23. supervision-5 (i10): supervision-3
24. analysis-tools-1 (i10): analysis-tools-scenarios
25. design-model-check-2 (i10): proposal-lists-read
26. formulation-1 (i10): pytest-bdd-suite, final-layout-read
27. formulation-2 (i10): formulation-1
28. spec-consistency-1 (i10): formulation-1
29. spec-integration-1 (i1): formulation-1
30. spec-integration-2 (i1): spec-integration-1
31. spec-migration-1 (i10): formulation-1
32. spec-migration-2 (i10): spec-migration-1
33. code-research-1 (i10): formulation-1, supervision-1
34. planning-1 (i10): formulation-1, supervision-1
35. red-green-1 (i10): formulation-1, supervision-2
36. red-green-2 (i10): red-green-1
37. review-1 (i10): formulation-1, supervision-5
38. review-2 (i10): review-1
39. delivery-1 (i10): formulation-1, supervision-5
40. delivery-2 (i10): delivery-1, supervision-4
41. role-boundaries-1 (i10): planning-1, review-2, red-green-1, code-research-1
42. work-queue-4 (i10): work-queue-1
43. migrate-status-and-ids (i8): final-layout-read, deprecated-and-sources
44. migrate-deprecated (i8): migrate-status-and-ids
45. migrate-layout (i8): migrate-status-and-ids
46. migrate-decisions (i8): migrate-layout
47. migrate-plan (i8): migrate-layout. It needs `scripts/plan`'s format, so it goes before delivery-3 and delivery-4 delete it.
48. migration-skill (i8): migrate-decisions, migrate-deprecated, migrate-plan
49. kb-trial (i8): migration-skill
50. feature-file-tools-1 (i10, removal): work-queue-4, every-scenario-bound
51. delivery-3 (i10, removal): delivery-2, red-green-2, review-2, planning-1, code-research-1, feature-file-tools-1
52. delivery-4 (i10, removal): delivery-3
53. delivery-5 (i10): delivery-4

Items 1-15 are i11, which the coordinator dispatches (Ruling 2B). Items 16-23 (work-queue and supervision)
are the coordinator's too (Ruling 2C). From item 24 on, they go through `work run`.
