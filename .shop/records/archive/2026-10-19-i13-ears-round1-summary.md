---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-i13-ears-round1-summary
kind: initiative-archive
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-19
---

# 0.21.0 EARS restructure (i13), round 1: summary and gate questions

The coordinator's summary of round 1 of initiative i13-ears (release 0.21.0): lines before and after per capability, scenario tags gained under decision 0052, the consistency pass, and 76 questions for the gate grouped by kind (one line or two, which pattern, changed by 0052, named system, overlaps, readings of a split line). It preceded the person's verdict that the drafts were far too detailed, which led to round 2 and the skeletons.

Archived from `.shop/scratch/ears/SUMMARY.md` (git-ignored scratch), text as it was.

---

# i13 EARS restructure: summary

Drafts in `.shop/scratch/ears/capabilities/` (17 files), one map each in `.shop/scratch/ears/map/`. Nothing outside
`.shop/scratch/ears/` changed; nothing committed. `alt/` (an unused alternative migration-tools) is not part of it.

## Lines and scenarios, per capability

"Gain tags": the scenarios that name each new id of their old line (0052; no scenario is added). Where the
feature file does not exist yet, the count is of the scenarios that will name several ids when formulated.

| capability | lines before → after | new ids (unused) | scenarios gaining tags |
|---|---|---|---|
| analysis-tools | 35 → 45 | r36–r47 (r45, r46) | 8 scenarios of features/analysis-tools.feature gain 10 tags |
| batch-measurement | 38 → 62 | r39–r66 (r39, r40, r41, r66) | 15 scenarios of features/batch-measurement.feature gain 24 tags |
| code-research | 11 → 18 | r13–r19 | no feature file; 5 scenarios when formulated |
| delivery | 17 → 34 | r18–r34 | no feature file; 14 when formulated |
| design-model-check | 65 → 98 | r68–r102 (r70, r72) | 17 scenarios of features/design-model-check.feature gain 31 tags; r64, r66 have no scenario yet (their scenarios will name r101, r102) |
| feature-file-tools | 45 → 64 | r60–r78 | 12 scenarios of features/feature-file-tools.feature gain 16 tags; r57, r58 have no scenario yet (r76; r77, r78) |
| formulation | 14 → 21 | r15–r21 | no feature file; 5 when formulated |
| migration-tools | 45 → 69 | r46–r71 (r47, r70) | no feature file; 19 when formulated |
| planning | 14 → 21 | r15–r21 | no feature file; 6 when formulated |
| red-green | 19 → 38 | r20–r38 | no feature file; 14 when formulated |
| review | 14 → 27 | r15–r27 | no feature file; 9 when formulated |
| role-boundaries | 6 → 12 | r7–r12 | no feature file; 2 when formulated |
| spec-consistency | 11 → 20 | r12–r20 | no feature file; 8 when formulated |
| spec-integration | 22 → 32 | r23–r32 | no feature file; 10 when formulated |
| spec-migration | 23 → 40 | r24–r40 | no feature file; 12 when formulated |
| supervision | 35 → 84 | r36–r85 (r62) | no feature file; 28 when formulated |
| work-queue | 24 → 47 | r25–r48 (r39) | no feature file; 16 when formulated |
| **total** | **438 → 732** | | 52 existing scenarios gain 81 tags |

Unused ids were drafted and merged back in the consistency pass; they were never published, so no `retired:`
entry is needed and no id is reused. `retired:` is unchanged in every file.

The lines that stated one tag per scenario now state 0052's rule: formulation r11 (and r13, r12), design-model-check
r20 (and r44), feature-file-tools r51, work-queue r20, spec-migration r11 (and r12), delivery r2 (with r19),
migration-tools r34.

Deprecated at formulation: feature-file-tools' "tagging with a requirement id makes it the scenario's one requirement
tag" (@r51) contradicts r51 under 0052; it is to be deprecated and replaced by a scenario in which the other
`@r<m>` tags are kept.

## Rewritten maps

In analysis-tools, feature-file-tools, planning, spec-migration and supervision the capability file and its map
came from different writers. Each capability file was kept and its map rewritten to match it: every old id maps to
the new ids the file has, every file id appears once (checked by script for all 17 maps), the scenario titles and
present tags checked against `features/<name>.feature`.

## Consistency pass

Shared rule applied: a message with its exit status, or a refusal that changes no file, is one line; a separate
effect or condition is its own line. All `**If**` lines have "then"; clauses are in the order Where, While, When or
If; no line uses an avoided word except as a quoted literal of the old system (`@holding`, " (held)", `Held for:`).

- Merged back (shared rule): analysis-tools r48 → r18, r45 → r44, r46 → r33; batch-measurement r39 → r6,
  r40 → r7, r41 → r8, r66 → r38; design-model-check r70 → r11, r72 → r15; migration-tools r47 → r3, r70 → r45;
  work-queue r39 → r18; supervision r62 → r17.
- System named in the line: delivery r2, r19, r4, r20, r21, r5, formulation r12, r17, spec-integration r26 ("it"
  → the skill); spec-integration r29 ("formulation" → `formulating-features`); spec-consistency r11 ("the round"
  → "the `initiative-round` running it"); work-queue r4 (`work add` → `work`); role-boundaries r5 (same subject as
  the other lines); delivery r24, r34 (skill names in code spans).
- design-model-check `rests_on`: design-decision/scenario-names-requirement-by-tag → design-decision/a-scenario-may-name-several-requirements.
- Left alone: batch-measurement's Implementation says "carrying" (an avoided word), outside Behaviour, which the
  brief keeps as it is.

## Questions for the gate, by kind

Each with the choice made. Ids are the capability's.

### One line or two

1. analysis-tools, feature-file-tools, design-model-check, migration-tools, work-queue, spec-migration r6: "print
   X and exit N", "refuse …, naming X, and change no file", "stop and report" are one line; a separate effect or
   a separate condition is its own line. Choice: that rule everywhere (the consistency pass merged the 13 lines
   that did otherwise). If every exit status and "change no file" must be its own line, many more lines
   follow (about 30 in feature-file-tools alone).
2. migration-tools r4, r7, r8, r9: one rule for `migrate run` or `migrate plan`. Choice: one trigger, one line.
3. design-model-check r1, r2, r9, r12, r17, r30, r33, r37, r39, r65: each a message with its exit status. Choice:
   one line each.
4. code-research r3 / r15: "changes or replaces" read as two triggers. Choice: two lines.
5. formulation r10: rewrite, or a question with two readings, kept as one response with two alternatives.
6. analysis-tools r34 / r47: not running import-linter and saying so. Choice: two effects, two lines.

### Which pattern

7. Where → When, the condition being no option: analysis-tools r33 (no file to check); batch-measurement r2, r25,
   r26, r52 (no archive file is the command's input); delivery r17 (a question's content); migration-tools r37
   (a fact about the plan). Choice: When.
8. Where → ubiquitous: design-model-check r18, r66 (an input form is no option). Choice: ubiquitous rules of
   `model`.
9. Where kept: analysis-tools r34 (the project's import contracts); spec-consistency r4, r15 (report mode, read as
   an option beside fix mode); spec-migration r9, r28, r29 (a repository whose lines have no ids), though r30 puts
   a like fact in a When. Choice: kept; the person may make spec-migration r9, r28, r29 When.
10. When → If … then, a fault: design-model-check r2, r30 (violations, file problems), r15 (a stale index);
    feature-file-tools r25, r40 (a bad binding, a scenario it cannot place); supervision r20 (the run's budget
    reached); review r5 (behaviour that contradicts a line). Choice: If … then.
11. Restrictions: delivery r6 ("`blocked_by` only when …") and work-queue r9 / r33 ("moves only when"). Choice:
    If … then shall not; restriction only, the move itself being `work run`'s (supervision r8).
12. supervision r8 / r51: "as soon as the guard allows it" read as an event. Choice: When.
13. supervision r9 / r52: the limit with its default "2 when it says nothing". Choice: one ubiquitous line, not an
    Optional one.
14. analysis-tools r1 / r36: "Unless `--log` is given" read as `tools probe` run without `--log`. Choice: When.
15. analysis-tools r18: two conditions that hold together. Choice: While (not a virtualenv) + If (a tool missing).
16. planning r12 / r20: "the work-item writes it when none exists". Choice: Where + When no such test exists.
17. spec-consistency r11: "where a round runs" is a period. Choice: While.

### Changed by 0052

18. feature-file-tools r51: `features tag` adds `@r<n>` and keeps the other `@r<m>` tags. Choice: add and keep;
    not "replace, with a flag to add". Its scenario is deprecated and replaced at formulation.
19. formulation r13 and r15, spec-migration r12: "names no line or two / more than one". Choice: formulation r13
    reports a scenario whose lines are of two capabilities (what 0052 still forbids) and r15 reads "at least one
    line"; spec-migration r12 asks at the gate only about a scenario that formulates no line.
20. work-queue r20: a scenario with several tags is accepted by a work-item when any one of its tags is a
    requirement it accepts. Choice: any one, not all.
21. migration-tools r34: a migrated slice's work-item accepts each `@r<n>` tag of its scenarios. Choice: all of
    them.
22. delivery r2 / r19: r19 is an addition, keeping the requirements one scenario names on one work-item, since a
    scenario is accepted whole. Choice: added; the person may drop it.

### Named system

23. red-green r1 / r20: "When a work-item is done" has no actor. Choice: the implementer reporting it done.
24. red-green r10: "the code does not choose" written as the implementer not having the code choose.
25. planning r2–r6, r9: lines about "the plan". Choice: "When the planner writes the plan, the planner shall …".
26. formulation r20 / r21: "the round says so", to whom unstated. Choice: the `initiative-round` that formulates,
    to whom left unstated.
27. spec-integration r29: an obligation on formulation stated here. Choice: kept here, system
    `formulating-features`; it could move to capability/formulation.
28. review r1, r2, r16, r20, r21 (and the like in code-research, planning, spec-migration): "When … ends, X is Y".
    Choice: "shall have …", the trigger kept at the end.
29. planning r12 / r20: "the system" is the system the work-item changes, not the named system. Choice: kept.

### Overlaps kept so nothing is dropped

30. supervision r40 / r25: two triggers for the branch review, r25 stricter. Choice: both kept; the person may
    retire r40.
31. analysis-tools r44 / r14: where the name is defined, said twice. Choice: both kept.
32. feature-file-tools r75 / r28: every binding of the old title rewritten, said twice. Choice: both kept.
33. spec-integration r28 / r12: no retired id given again. Choice: both kept.
34. design-model-check r12 / r55 / r57: a missing clingo exits 2 (r12) and first runs again elsewhere (r55).
    Choice: r12 kept as written, not narrowed.
35. design-model-check r41 / r95 / r17: r95 states only the case r41 added (every naming proposal only removes
    it). Choice: as written.
36. role-boundaries r9: "so the listing never enters its context", a consequence of r8. Choice: its own line.

### Readings of a split line

37. supervision r10 / r55: "only when they pass and nothing fails that passed in the last suite record". Choice:
    merge when they pass (r54); no merge if anything that passed fails (r55).
38. supervision r13 / r58: "at most three times in a row". Choice: first to third `PARTIAL` continue, the fourth
    goes to `awaiting-ruling`.
39. supervision r26 / r77: the fix work-item goes to `green` only when no finding gets a further fix work-item.
40. supervision r27 / r78: the end line repeats the start line's fields.
41. supervision r33: "changes no initiative's or capability-proposal's status" kept in r33, not made ubiquitous.
42. feature-file-tools r10 / r35: the no-file lines only refuse; the several-files lines (r64, r72) name the files.
43. feature-file-tools r37 / r73: only in `--from` is missing, only in the other tree is added.
44. feature-file-tools r58 / r78: exit 1 when any scenario is bound by no call, whichever files `--unbound` reads.
45. feature-file-tools r3 / r62: "checks nothing else of the result" as its own line.
46. feature-file-tools r19 / r65: "whether or not the replacement exists yet" on the `--for` line.
47. planning r10 / r19: "otherwise" written out as a defect neither a wrong answer nor lost data on the path.
48. planning r13: "and no other code" means no code beyond the file set.
49. spec-migration r1 / r24 / r25: "says which" as each line saying its own condition.
50. spec-migration r10 / r30: the person is asked for the context path only when `spec/index.md` lacks it.
51. spec-migration r31: "tags nothing before the answer" means no scenario at all.
52. spec-migration r40: "are the next" means the next commit, one commit.
53. spec-migration r38: "its test still binds it" as the skill having left it bound.
54. batch-measurement r14 / r47: "each commit" read as each commit made inside the batch.
55. batch-measurement r29 / r54 / r55 / r56: each condition leaves tasks uncounted; the note lines are triggered by
    leaving them uncounted.
56. batch-measurement r15 / r48 / r49: the Lands line's source split by archive file and open batch.
57. batch-measurement r21 / r50: no living plan, several living plans: two conditions, the same refusal.
58. code-research r9 / r18: "never on the checkout's data" as its own response.
59. delivery r5 / r22: "only the first three are reviewed alone" stated as what the skill does with the risk.
60. delivery r30: `work run` started again when the answers are recorded.
61. design-model-check r11: the exit status is the one the other findings give, warnings counting for nothing.
62. design-model-check r34 / r92: no v_k5 for several capability-proposals directly under a capability-change
    initiative; parts of other kinds left unstated.
63. design-model-check r43 / r98: a bare name where `<kind>/<name>` is needed is unresolved.
64. formulation r18: a deprecated scenario counted as formulating no line, without naming `model check`.
65. migration-tools r11: an `id` equal to `--context` needs no line (r48 covers a different one).
66. migration-tools r31 / r64: no living plan refuses "saying so"; several name those found.
67. migration-tools r30 / r63: r30 the default with no `--plan`, r63 Where `--plan`.
68. review r12 / r23–r25: the triage's three cases each their own line, "hardening" as "something to harden".
69. spec-consistency r14: the reply follows the findings being written.
70. spec-consistency r10 / r19: no "Where fix mode", the trigger arising only in fix mode.
71. spec-consistency r20: "runs when the person asks" read as "only when".
72. spec-integration r8 / r26: "write" read as drafting (r8) and as writing to `spec/` (r26).
73. spec-integration r30: "writes nothing to `spec/`" means nothing at all.
74. spec-integration r10: the recommendation comes before the integration starts.
75. work-queue r18 / r40: a command given wrongly exits 2, its own line.
76. red-green r9: the `PARTIAL` stop keeps r9; the other three responses take r27–r29.
