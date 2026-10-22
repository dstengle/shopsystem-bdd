---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-i13-ears-round1-maps
kind: initiative-archive
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-19
---

# 0.21.0 EARS restructure (i13), round 1: id maps

Round 1 of initiative i13-ears (release 0.21.0): per capability, the table old id -> new ids with the EARS pattern chosen, the scenario tags each feature-file scenario would gain under decision 0052, the meaning choices (Questions) and the consistency pass. The maps of delivery, migration-tools, planning, supervision and work-queue were never rewritten in round 2 (those capabilities became skeletons), so the final-round map/ folder holds identical copies. Last section: tmp/analysis-tools.behaviour, analysis-tools' Behaviour lines before the consistency pass merged r45, r46 and r48 back (kept as the only copy of that state).

Archived from git-ignored scratch; each file's text as it was.

## `.shop/scratch/ears/round1/map/analysis-tools.md`

~~~~~~
# analysis-tools: old ids to EARS lines

Highest id ever used before: r35 (none retired). New ids r36–r44 and r47; r45, r46 and r48 are not used (see
Consistency pass). Lines 35 → 45.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r36 | Event-Driven ×2 | split the two sentences: the interpreter chosen (core) / what `tools probe` without `--log` prints of it |
| r2 | r2 | Unwanted Behavior | the three commands moved into the condition so the line names one system, `tools` |
| r3 | r3, r37 | Event-Driven, Unwanted Behavior | the printout (core) / exit 1 if a tool is missing |
| r4 | r4 | Event-Driven | unchanged meaning |
| r5 | r5 | Event-Driven | unchanged meaning ("and edit no dependency file" kept in the line) |
| r6 | r6 | Unwanted Behavior | the command moved into the condition; system `tools` |
| r7 | r7 | Unwanted Behavior | unchanged meaning; the printout with its exit 1 is one line |
| r8 | r8, r38, r39 | Event-Driven, Complex (Where, When), Event-Driven | the coverage run (core) / arguments after `--` passed to pytest / the map kept in `.shop/scratch/tools/coverage` |
| r9 | r9 | Event-Driven | unchanged meaning |
| r10 | r10 | Complex (Where, When) | the trigger made explicit |
| r11 | r11, r40 | Unwanted Behavior ×2 | split by condition: nothing executed the target (core) / no function by that name |
| r12 | r12 | Unwanted Behavior | unchanged meaning |
| r13 | r13 | Event-Driven | unchanged meaning |
| r14 | r14 | Event-Driven | unchanged meaning |
| r15 | r15 | Unwanted Behavior | unchanged meaning |
| r16 | r16, r41, r42 | Event-Driven, Complex (Where, When), Unwanted Behavior | ruff and vulture (core) / import-linter where the project has import contracts / exit 1 if any reports |
| r17 | r17 | Unwanted Behavior | unchanged meaning |
| r18 | r18 | Complex (While, If) | two conditions: the interpreter not a virtualenv as the state, a tool missing at `tools install` as the condition; installing nothing, the printout and exit 1 one line |
| r19 | r19 | Event-Driven | unchanged meaning |
| r20 | r20 | Event-Driven | unchanged meaning |
| r21 | r21 | Unwanted Behavior | the three commands moved into the condition |
| r22 | r22 | Event-Driven | system named: `tools` names every tool in its line |
| r23 | r23, r43 | Event-Driven ×2 | the earlier map replaced (core) / the printout with exit 0 |
| r24 | r24 | Unwanted Behavior | unchanged meaning |
| r25 | r25 | Event-Driven | unchanged meaning |
| r26 | r26 | Unwanted Behavior | the command moved into the condition |
| r27 | r27 | Unwanted Behavior | the two commands moved into the condition |
| r28 | r28 | Unwanted Behavior | the command moved into the condition |
| r29 | r29 | Unwanted Behavior | unchanged meaning |
| r30 | r30, r44 | Event-Driven ×2 | no definition counted as a reference (core) / where it is defined named, with exit 0 however many references |
| r31 | r31 | Complex (Where, When) | the trigger made explicit |
| r32 | r32 | Unwanted Behavior | unchanged meaning |
| r33 | r33 | Event-Driven | was Where, but having no file to check is no option: When. The message and "not exit 1 for those two" one line |
| r34 | r34, r47 | Complex (Where, When) ×2 | import-linter not run (core) / said so under its heading |
| r35 | r35 | Event-Driven | unchanged meaning |

## Scenario tags

Of features/analysis-tools.feature:

- "the interpreter is the first of --python, .venv, venv, $VIRTUAL_ENV and the running one" (@r1): gains @r36
- "probe lists each tool, its version or that it is missing, and the interpreter" (@r3): gains @r37
- "map runs the suite once under coverage and keeps the map" (@r8): gains @r38, @r39
- "tests-of fails when nothing executed the target or the function does not exist" (@r11): gains @r40
- "check runs each tool under its own heading and fails when any reports" (@r16): gains @r41, @r42
- "map replaces the earlier map and succeeds whether or not the tests pass" (@r23): gains @r43
- "refs on a defined name gives its definition apart from its references" (@r30): gains @r44
- "check without import contracts does not run import-linter" (@r34): gains @r47

## Questions

1. One response. "Print X and exit N", "refuse …, naming X" and a qualifier on one action ("edit no dependency
   file") are one line each; separate effects (the map replaced and the printout, r23/r43) and separate
   conditions with their own exit (r3/r37, r16/r42) are split. Choice: as written (the shared rule).
2. r18 has two conditions that hold together (the interpreter not a virtualenv, a tool missing). Choice: Complex
   While + If, one line, since neither alone gives the response (r6 and r19 cover the others).
3. r33 was written Where, but having no file to check is not an option or configuration. Choice: When.
4. r34 / r47: "the project states no import contracts" kept as Where (a configuration of the project), as it was;
   not running import-linter and saying so are two effects. Choice: two lines.
5. r44 repeats that `tools refs` names where the name is defined, which r14's summary line already gives. Choice:
   kept, so nothing of r30 is dropped.
6. r1 / r36: "Unless `--log` is given" read as the trigger `tools probe` run without `--log`. Choice: When.

## Consistency pass

- r48 ("… then `tools` shall install nothing") merged back into r18: a refusal that changes no file is one line.
- r45 ("… shall exit 0 however many references there are") merged into r44: a message with its exit status is one
  line.
- r46 ("… shall not exit 1 for ruff or vulture") merged back into r33, for the same reason.
- r45, r46 and r48 are not used; they were never published, so they need no `retired:` entry.
~~~~~~

## `.shop/scratch/ears/round1/map/batch-measurement.md`

~~~~~~
# batch-measurement: map

Highest id before: r38 (retired: none). New ids: r39–r66, of which r39, r40, r41 and r66 are not used (see Consistency pass). Lines 38 → 62.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1 | Event-Driven | unchanged meaning |
| r2 | r2 | Event-Driven | was Optional: a missing archive file is the command's input, not an option (Q1) |
| r3 | r3 | Optional | unchanged meaning |
| r4 | r4 | Optional | unchanged meaning |
| r5 | r5 | Unwanted Behavior | unchanged meaning |
| r6 | r6 | Unwanted Behavior | refuse naming the file and what was missing, and write no facts file: one line |
| r7 | r7 | Unwanted Behavior | refuse, leaving the file as it was: one line |
| r8 | r8 | Unwanted Behavior | refuse naming the window, and write nothing: one line |
| r9 | r9, r42 | Event-Driven ×2 | was ubiquitous; inside counted (r9), outside not (r42) |
| r10 | r10, r43, r44 | Event-Driven, Ubiquitous ×2 | usage once (r10), reasoning "of which" output (r43), never added to output (r44) |
| r11 | r11 | Event-Driven | was ubiquitous with "when"; trigger moved to the front |
| r12 | r12, r45, r46 | Event-Driven ×3 | description (r12), "failing that" prompt (r45), "otherwise" unattributed (r46) |
| r13 | r13 | Ubiquitous | unchanged meaning; "as it wrote them" and its two parts are one response |
| r14 | r14, r47 | Event-Driven ×2 | commit to the running implementer (r14), files counted by kind (r47) (Q2) |
| r15 | r15, r48, r49 | Ubiquitous, Event-Driven ×2 | Lands line beside the files touched (r15), from the archive file (r48), from the living plan for the open batch (r49) |
| r16 | r16 | Ubiquitous | unchanged meaning; one response, a list |
| r17 | r17 | Ubiquitous | "The facts hold no …" as what `measure batch` shall not write |
| r18 | r18 | Event-Driven | unchanged meaning |
| r19 | r19 | Event-Driven | unchanged meaning |
| r20 | r20 | Unwanted Behavior | unchanged meaning |
| r21 | r21, r50 | Unwanted Behavior ×2 | no living plan (r21), several (r50) |
| r22 | r22 | Unwanted Behavior | unchanged meaning |
| r23 | r23 | Unwanted Behavior | unchanged meaning |
| r24 | r24, r51 | Unwanted Behavior ×2 | not a git repository (r24), a git command fails (r51) |
| r25 | r25, r52 | Event-Driven, Complex (Where + When) | batch name (r25), the default path without `--out` (r52) |
| r26 | r26 | Event-Driven | was Optional; as r2 (Q1) |
| r27 | r27, r53 | Event-Driven ×2 | was ubiquitous; archive batch's slices (r27), open batch's only attributed slices (r53) |
| r28 | r28 | Event-Driven | was ubiquitous; the commit made while several implementers ran is the trigger |
| r29 | r29, r54, r55, r56 | Unwanted Behavior ×2, Event-Driven ×2 | two conditions (no ledger and no `--tasks`: r29; plan in no commit: r54), each leaving tasks uncounted; note in the facts (r55) and on stderr (r56) chained on "leaves tasks uncounted" |
| r30 | r30 | Event-Driven | unchanged meaning |
| r31 | r31, r57 | Ubiquitous, Event-Driven | closing status (r31), BLOCKED/PARTIAL/NEEDS_CONTEXT not done (r57) |
| r32 | r32, r58, r59 | Ubiquitous ×2, Event-Driven | versions (r32), window as times (r58), "where known, commits" (r59) |
| r33 | r33, r60 | Event-Driven ×2 | was Optional; to the end commit (r33), "or to HEAD when the end is not a commit" (r60) |
| r34 | r34, r61, r62, r63, r64 | Event-Driven, Ubiquitous ×4 | resumed (r34), late share (r61), building time defined (r62), scouts left out (r63), starting context (r64) |
| r35 | r35 | Event-Driven | unchanged meaning; one printed response, in its order |
| r36 | r36 | Event-Driven | unchanged meaning; one printed comparison |
| r37 | r37, r65 | Unwanted Behavior ×2 | `compare` given a file not facts (r37), `show` or `compare` given non-JSON (r65) |
| r38 | r38 | Unwanted Behavior | why on stderr and exit 1: one line |

## Scenario tags

In features/batch-measurement.feature (no scenario is added):

- "an archive file's batch runs from the archive commit before it to its own" (@r1): none
- "a subagent transcript is a dispatch only when it starts inside the batch" (@r9): gains @r42
- "a request's usage is counted once, and its reasoning is part of its output" (@r10): gains @r43, @r44
- "a dispatch is attributed by its description, then its prompt, else unattributed" (@r12): gains @r45, @r46
- "a commit goes to the implementer running when it was made" (@r14): gains @r47
- "each slice's Lands line sits beside the files its dispatches touched" (@r15): gains @r48, @r49
- "the open batch needs --plan when the living plan cannot be found" (@r21): gains @r50
- "git's failures are refused with git's error" (@r24): gains @r51
- "the open batch is named by --name, default open" (@r25): gains @r52
- "the facts hold the slices the batch planned and the slices dispatches were attributed to" (@r27): gains @r53
- "tasks are left uncounted with a note when the batch plan cannot be had" (@r29): gains @r54, @r55, @r56
- "a reply closing <status> is counted as not done" (@r31): gains @r57
- "the facts record the versions the transcripts name and the window" (@r32): gains @r58, @r59
- "a batch starting at a commit gives the files and lines changed to its end" (@r33): gains @r60
- "the facts count resumed dispatches, the late share of building time without scouts, and starting context" (@r34): gains @r61, @r62, @r63, @r64
- "a file measure cannot read as its facts is refused" (@r37): gains @r65

Only the scenarios listed with gains change; the rest keep their one tag. No line of this capability stated
one tag per scenario.

## Questions

1. r2, r26 (and r25, r52): "Where no archive file is given" became "When `measure batch` is run with no archive
   file": the archive file is the command's input (When), not an option (Where). `--out`, `--from`, `--to`
   stay Where. Choice: as written; say if the archive-less mode is to read as an option.
2. r14/r47: "each commit" written "a commit made inside the batch", the commits the facts hold; the old
   line did not say "inside the batch". Choice: kept as the closest reading of "the facts give each commit".
3. r29/r54: the two conditions were joined by "or" with three responses (uncounted, note, stderr). Choice:
   each condition leaves tasks uncounted, and the note lines (r55, r56) are triggered by "leaves tasks
   uncounted", so the conditions are not repeated three times. The note's "why" is then per condition.
4. r15: the Lands line's source ("from the archive file, or the living plan for the open batch") split into
   r48 and r49; r15 keeps the comparison, the line's core.
5. r21/r50: no living plan and several living plans are two conditions with the same refusal; split.

## Consistency pass

- r39 merged back into r6, r40 into r7, r41 into r8: a refusal that changes no file is one line (the shared rule).
- r66 merged back into r38: a message with its exit status is one line.
- r39, r40, r41 and r66 are not used; they were never published, so they need no `retired:` entry. The scenarios
  of r6, r7, r8 and r38 no longer gain a tag.
~~~~~~

## `.shop/scratch/ears/round1/map/code-research.md`

~~~~~~
# code-research: old ids to EARS lines

Highest id ever used: r12 (retired: r2). New ids from r13.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r13, r14 | Event-Driven | split by response: r1 the notes file (core), r13 the file set in the result file, r14 the checkout unchanged |
| r3 | r3, r15 | Event-Driven | split by trigger: r3 a requirement that changes one code relies on, r15 one that replaces it |
| r4 | r4, r16, r17 | Event-Driven | split by response: r4 why each scenario is red (core), r16 probes marked `run`, r17 conclusions from reading marked `read` |
| r5 | r5 | Event-Driven | unchanged meaning |
| r6 | r6 | Event-Driven | unchanged meaning |
| r7 | r7 | Ubiquitous | unchanged meaning |
| r8 | r8 | Event-Driven | unchanged meaning |
| r9 | r9, r18 | Ubiquitous | split by response: r9 probes in a scratch directory (core), r18 never on the checkout's data |
| r10 | r10 | Ubiquitous | unchanged meaning |
| r11 | r11 | Ubiquitous | unchanged meaning |
| r12 | r12, r19 | Ubiquitous | split by response: r12 the status set, r19 the summary length |

Lines: 11 before, 18 after.

## Scenario tags

features/code-research.feature does not exist yet. When it is formulated, the scenario for each old id names its
new ids too: r1 + r13, r14; r3 + r15; r4 + r16, r17; r9 + r18; r12 + r19.

## Questions

1. r3/r15: "changes or replaces" read as two triggers, so two lines with one response each; the alternative is
   one trigger, "a requirement that changes or replaces one", kept as r3 alone.
2. r9/r18: "never on the checkout's data" read as its own response (a probe reads or writes no data of the
   checkout), not only a restatement of running in a scratch directory.

## Consistency pass

- No line changed.
~~~~~~

## `.shop/scratch/ears/round1/map/delivery.md`

~~~~~~
# delivery: map

17 lines → 34. New ids r18–r34 (highest used before: r17, nothing retired). The system is named as the skill,
`delivering-an-initiative` (the Purpose's "the session").

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r18 | Event-Driven ×2 | drafts / names those left out |
| r2 | r2, r19 | Event-Driven ×2 | changed to 0052's rule: r19 keeps the requirements one scenario names on one work-item |
| r3 | r3 | Event-Driven | unchanged meaning |
| r4 | r4, r20, r21 | Event-Driven ×3 | one capability or a check / one observable sentence / one unknown or none |
| r5 | r5, r22 | Event-Driven, Ubiquitous | the risk values / only the first three for work-items reviewed alone |
| r6 | r6 | Unwanted Behavior | "only when" restated as the case where `blocked_by` is not given |
| r7 | r7 | Optional | unchanged meaning |
| r8 | r8, r23 | Ubiquitous ×2 | drafts from these alone / reads no code |
| r9 | r9, r24 | Unwanted Behavior ×2 | no work-item / question shown |
| r10 | r10, r25, r26 | Event-Driven ×3 | commit / table / `work run` started |
| r11 | r11, r27 | Unwanted Behavior ×2 | changes in the tree / default branch |
| r12 | r12, r28 | State-Driven ×2 | reads nothing / waits |
| r13 | r13, r29 | Event-Driven ×2 | shows the questions / asks nothing else |
| r14 | r14, r30 | Event-Driven ×2 | records / starts `work run` again |
| r15 | r15, r31 | Event-Driven ×2 | tells, naming the proposals / closing is the owner's |
| r16 | r16, r32, r33 | Event-Driven ×2, State-Driven | what was spent / asks / changes nothing until the answer |
| r17 | r17, r34 | Event-Driven ×2 | was Where: a question's content is a trigger, not an option; shown as a formulation question / answer routed before `work rule` |

## Scenario tags

`features/delivery.feature` does not exist yet, so no scenario gains tags now. When it is written, under 0052
the scenario that formulates each old id names these tags (17 scenarios):

- r1: @r1 @r18
- r2: @r2 @r19
- r4: @r4 @r20 @r21
- r5: @r5 @r22
- r8: @r8 @r23
- r9: @r9 @r24
- r10: @r10 @r25 @r26
- r11: @r11 @r27
- r12: @r12 @r28
- r13: @r13 @r29
- r14: @r14 @r30
- r15: @r15 @r31
- r16: @r16 @r32 @r33
- r17: @r17 @r34

r3, r6, r7 keep their single tag.

## Questions

1. r2 under 0052: the brief asks that it change to 0052's rule. "Each requirement … accepted by exactly one" is
   kept as it was (r2); r19 adds that the requirements one scenario names go to one work-item, since a scenario
   is accepted whole. Choice: add r19; this is the one addition, made for 0052 — the person may drop it.
2. r5 "only the first three are reviewed alone" is `work run`'s behaviour (supervision r21), not the skill's.
   Choice: r22 states it as what the skill does with the risk (gives the first three only to work-items to be
   reviewed alone).
3. r6 "is `blocked_by` another only when its scenarios cannot pass without the other's work": read as a
   restriction (If … then shall not). Choice: Unwanted Behavior.
4. r17 was a Where line, but a question's content is no option or configuration. Choice: When (r17), with the
   routing of the answer as r34.
5. r30 "starts `work run` again" read as after the answers are recorded. Choice: When the answers are recorded.

## Consistency pass

- r2, r19, r4, r20, r21, r5: "it shall" written "`delivering-an-initiative` shall", the system named in the line.
- r24, r34: the skills `integrating-a-proposal` and `formulating-features` put in code spans, as elsewhere.
~~~~~~

## `.shop/scratch/ears/round1/map/design-model-check.md`

~~~~~~
# design-model-check: old ids to EARS lines

Highest id ever used: r67 (retired r42, r45). New ids r68 to r102. `retired:` unchanged; r70 and r72 not used (see Consistency pass). Lines 65 → 98.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1 | Event-Driven | unchanged meaning |
| r2 | r2 | Unwanted Behavior | was When; violations are a fault, so If … then |
| r3 | r3 | Unwanted Behavior | unchanged meaning |
| r4 | r4 | Unwanted Behavior | unchanged meaning |
| r5 | r5 | Unwanted Behavior | unchanged meaning |
| r6 | r6 | Unwanted Behavior | unchanged meaning |
| r7 | r7 | Unwanted Behavior | unchanged meaning; "is formulated while" folded into the condition |
| r8 | r8 | Unwanted Behavior | unchanged meaning |
| r9 | r9, r68 | Unwanted Behavior | split by condition: scenario naming an absent requirement (r9), capability resting on an absent decision (r68) |
| r10 | r10, r69 | Unwanted Behavior | split: chain reaching no initiative, v9c (r10, the case its scenario shows), no part_of, v9a (r69) |
| r11 | r11 | Event-Driven | the warnings printed, the exit status left as the other findings set it: one line |
| r12 | r12 | Unwanted Behavior | unchanged meaning (see Questions) |
| r13 | r13, r71 | Event-Driven, Ubiquitous | split: printing the facts (r13), standard library only (r71) |
| r14 | r14 | Event-Driven | unchanged meaning; response written as what `model decisions` writes |
| r15 | r15 | Unwanted Behavior | was When; a stale index is a fault. Say so and exit 1, writing nothing: one line |
| r16 | r16 | Event-Driven | unchanged meaning |
| r17 | r17 | Unwanted Behavior | unchanged meaning |
| r18 | r18 | Ubiquitous | was Where; a range is a form `model` reads, not an option |
| r19 | r19 | Ubiquitous | unchanged meaning; "and nothing else" written as "only" |
| r20 | r20 | Ubiquitous | changed to 0052's rule: each `@r<n>` tag a scenario has names a requirement, one or more, where it said "a tag" |
| r21 | r21 | Ubiquitous | unchanged meaning, as what `model` reads |
| r22 | r22, r73 | Unwanted Behavior | split by condition: reference in neither form (r22), reversed range (r73) |
| r23 | r23, r74, r75, r76, r77 | Unwanted Behavior, State-Driven | split: absent and not retired, unresolved (r23); retired id added by a proposal not merged/formulated/withdrawn, v15c (r74); retired id removed by such a proposal, unresolved (r75); while merged/formulated/withdrawn, no report for a retired id (r76); and a removed retired id read as that requirement (r77) |
| r24 | r24, r78 | Unwanted Behavior | split by condition: names nothing (r24), names the wrong kind (r78) |
| r25 | r25, r79, r80, r81, r82 | Unwanted Behavior | split, one condition each: index missing (r25), index without id (r79), capability id (r80), no Behaviour section (r81), malformed retired (r82) |
| r26 | r26, r83 | Unwanted Behavior | split: stray feature file (r26), shared title among scenarios not `@deprecated` (r83, the second sentence folded into its condition) |
| r27 | r27, r84, r85, r86, r87, r88 | Unwanted Behavior | split, one condition each: no initiative.md, naming the directory (r27), no id (r84), kind (r85), status (r86), priority (r87), date (r88) |
| r28 | r28 | Unwanted Behavior | unchanged meaning |
| r29 | r29, r89, r90, r91 | Unwanted Behavior | split, one condition each: decision without id (r29), record kind (r89), block value (r90), one id two kinds (r91) |
| r30 | r30 | Unwanted Behavior | unchanged meaning |
| r31 | r31 | Event-Driven | unchanged meaning |
| r32 | r32 | Optional | unchanged meaning |
| r33 | r33 | Optional | unchanged meaning |
| r34 | r34, r92 | Unwanted Behavior, Ubiquitous | split: v_k5 (r34), a capability-change initiative's several proposals not reported (r92) |
| r35 | r35 | Unwanted Behavior | unchanged meaning |
| r36 | r36 | Event-Driven | unchanged meaning |
| r37 | r37 | Event-Driven | unchanged meaning |
| r38 | r38, r93 | Event-Driven, Unwanted Behavior | split: prints the file (r38), a decision with no id left out (r93) |
| r39 | r39 | Unwanted Behavior | unchanged meaning |
| r40 | r40, r94 | Unwanted Behavior | split by response: says so in place of the text (r40), still lists the proposals (r94) |
| r41 | r41, r95, r96 | Event-Driven, Unwanted Behavior | split: lists proposals in date order (r41), only-removing proposals exit 1 (r95), one adding or changing proposal exits 0 (r96); the general "none adds or changes, exit 1" is r17 |
| r43 | r43, r97, r98 | Ubiquitous, Unwanted Behavior | split: full and short forms, context path and bounded context (r43); bare name in a kind-fixing field (r97); bare name where `<kind>/<name>` is needed is unresolved (r98, the reading the r43 scenario pins) |
| r44 | r44 | Ubiquitous | unchanged meaning; "tag" → "tags" for 0052 |
| r46 | r46, r99 | Unwanted Behavior | split by condition: a node's id (r46), spec/index.md's id (r99) |
| r47 | r47 | Unwanted Behavior | unchanged meaning |
| r48 | r48 | Ubiquitous | unchanged meaning, the form written as what `model` reads |
| r49 | r49 | Unwanted Behavior | unchanged meaning; "that form" → "the form r48 gives" |
| r50 | r50 | Event-Driven | unchanged meaning |
| r51 | r51 | Event-Driven | unchanged meaning |
| r52 | r52 | Unwanted Behavior | unchanged meaning |
| r53 | r53 | Unwanted Behavior | unchanged meaning |
| r54 | r54 | Unwanted Behavior | unchanged meaning |
| r55 | r55 | Unwanted Behavior | unchanged meaning; "looks … and runs again" written as one response, run again under the first found in that order |
| r56 | r56 | Unwanted Behavior | was When; "does so once" written as the fault it guards, a second failure does not run again |
| r57 | r57 | Unwanted Behavior | unchanged meaning |
| r58 | r58, r100 | Event-Driven, Ubiquitous | split: withdrawn part counted closed (r58, its scenario's title), withdrawn a status of proposal and work-item (r100) |
| r59 | r59 | Unwanted Behavior | unchanged meaning |
| r60 | r60 | Unwanted Behavior | unchanged meaning |
| r61 | r61 | Unwanted Behavior | unchanged meaning; one condition, a path of the old layout, reported for each |
| r62 | r62 | Unwanted Behavior | unchanged meaning |
| r63 | r63 | Unwanted Behavior | unchanged meaning |
| r64 | r64, r101 | Ubiquitous | split: source read as ids (r64), `by` not read (r101) |
| r65 | r65 | Event-Driven | unchanged meaning |
| r66 | r66, r102 | Ubiquitous, Unwanted Behavior | was Where; split: term reference read as the term (r66), an absent term unresolved unless a merged or formulated proposal removes it (r102) |
| r67 | r67 | Unwanted Behavior | unchanged meaning |

## Scenario tags

In features/design-model-check.feature:

- "references that name nothing are reported" (@r9): gains @r68
- "a part that reaches no initiative is refused" (@r10): gains @r69
- "facts are printed in clingo's syntax" (@r13): gains @r71
- "a reference in neither requirement form, or a reversed range, is unresolved" (@r22): gains @r73
- "a proposal adding or removing a requirement no capability has is unresolved, unless it adds a retired id" (@r23): gains @r74, @r75, @r76, @r77
- "a frontmatter reference to nothing, or to the wrong kind, is unresolved" (@r24): gains @r78
- "a malformed index or capability file is a file problem" (@r25): gains @r79, @r80, @r81, @r82
- "a feature file no capability is formulated as, or with a title twice, is a file problem" (@r26): gains @r83
- "a malformed work directory or work file is a file problem" (@r27): gains @r84, @r85, @r86, @r87, @r88
- "a malformed decision, record or frontmatter is a file problem" (@r29): gains @r89, @r90, @r91
- "only a capability-change initiative may hold several parts directly" (@r34): gains @r92
- "writing the decisions index names the file and leaves out decisions with no id" (@r38): gains @r93
- "why on a requirement no capability has still lists its proposals" (@r40): gains @r94
- "why lists every proposal naming the requirement by date, and fails when none adds or changes it" (@r41): gains @r95, @r96
- "a node may be written in short where its field allows it" (@r43): gains @r97, @r98
- "a node whose id is not in type-first form is a file problem" (@r46): gains @r99
- "a withdrawn part is closed" (@r58): gains @r100
- r64 and r66 have no scenario in the feature file yet (nor r60 to r67): when written, r64's names @r101 and r66's names @r102.

Seen, outside this brief: the feature file still has scenarios tagged @r42 and @r45, both retired, and scenarios showing `@holding` and `formulated_as` as accepted where r62 and r60 now refuse them.

## Questions

1. A message and its exit status ("say so and exit 1") are kept as one response, the command's result; a separate effect (writing nothing, still listing, leaving the exit status alone) became its own line. Choice: that reading throughout, so r1, r2, r9, r12, r17, r30, r33, r37, r39, r65 stay one line each.
2. r12 says a missing clingo exits 2 with the install command, while r55 says it first runs again elsewhere and r57 exits 2 when no interpreter has it. Choice: r12 kept as written, not narrowed to "no interpreter has clingo".
3. r11's "they alone do not change the exit status" (now in r11). Choice: the exit status is the one the other findings give, warnings counting for nothing.
4. r18, r66 were Where-lines on an input form, not an option. Choice: ubiquitous reading rules of `model`, as r19 to r21, r43 and r48.
5. r34's "a capability-change initiative may have several capability-proposals" (r92). Choice: no v_k5 for several capability-proposals directly under one; parts of other kinds under it are left as unstated as before.
6. r41's "if none adds or changes it … exits 1" repeats r17. Choice: r95 states only the case r41 added, every naming proposal only removing it; r17 has the rest.
7. r43's "need `<kind>/<name>`" said nothing of the consequence. Choice: unresolved (r98), as the r43 scenario's `part_of i1` row shows.
8. r2 and r30 (When → If): violations and file problems are faults in the repository. Choice: If … then; r1 and r11 (no fault, warnings) stay When.
9. The frontmatter `rests_on` still names design-decision/scenario-names-requirement-by-tag, which 0052 supersedes. Choice, at the consistency pass: replaced by design-decision/a-scenario-may-name-several-requirements, since the old one is superseded.

## Consistency pass

- r70 merged back into r11 and r72 into r15: a message with its exit status, or a check that changes no file, is one
  line (the shared rule). r70 and r72 are not used; they were never published, so they need no `retired:` entry.
  The scenarios of r11 and r15 no longer gain a tag. Lines 65 → 98.
- `rests_on`: `design-decision/scenario-names-requirement-by-tag` (superseded by 0052) replaced by
  `design-decision/a-scenario-may-name-several-requirements`.

## New lines (i13's check)
r103: v_e1, a line not in an EARS pattern. r104: v_e2, more than one shall or sentence. Added by the coordinator; no scenario yet (formulated with the check).
~~~~~~

## `.shop/scratch/ears/round1/map/feature-file-tools.md`

~~~~~~
# feature-file-tools: old ids to EARS lines

Highest id ever used before: r59 (`retired:` includes r50). New ids r60–r78; `retired:` unchanged. Lines 45 → 64.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r60 | Ubiquitous ×2 | split: reading the tree (core) / docstring text never a scenario, keyword or tag |
| r2 | r2 | Unwanted Behavior | unchanged meaning |
| r3 | r3, r61, r62 | Unwanted Behavior ×2, Event-Driven | the three clauses: the refusal (core) / a `Rule:` block outside a docstring makes the result invalid / the result checked for nothing else |
| r4 | r4, r63 | Event-Driven ×2 | split the two sentences: the counts (core) / the total counts every scenario, untagged ones included |
| r5 | r5 | Event-Driven | unchanged meaning |
| r6 | r6 | Event-Driven | unchanged meaning |
| r7 | r7 | Unwanted Behavior | unchanged meaning |
| r10 | r10, r64 | Unwanted Behavior ×2 | split by condition: no file has the title (core) / several files have it, each named |
| r11 | r11 | Unwanted Behavior | unchanged meaning |
| r12 | r12 | Event-Driven | "removes … and appends unchanged to the end" written as one move |
| r13 | r13 | Complex (Where, When) | unchanged meaning |
| r14 | r14 | Complex (Where, When) | unchanged meaning ("joins them to none" as "joined to none") |
| r15 | r15 | Unwanted Behavior | unchanged meaning |
| r16 | r16 | Event-Driven | unchanged meaning |
| r17 | r17 | Unwanted Behavior | unchanged meaning |
| r18 | r18 | Unwanted Behavior | unchanged meaning |
| r19 | r19, r65, r66 | Event-Driven, Complex (Where, When) ×2 | the tag and title, nothing else changed but the description line (core) / `Deprecated for: <new title>` with `--for` / `Deprecated for: removal` with `--for-removal` |
| r20 | r20 | Unwanted Behavior | unchanged meaning |
| r21 | r21, r67, r68, r69 | Event-Driven, Event-Driven, Unwanted Behavior, Event-Driven | each deprecated scenario with what it is for (core) / the replacement's file and tag / no scenario has the replacement's title / deprecated for removal |
| r22 | r22 | Complex (While, When) | "is run and no scenario is deprecated" made a state |
| r23 | r23 | Event-Driven | unchanged meaning |
| r24 | r24 | Unwanted Behavior | unchanged meaning |
| r25 | r25, r70 | Unwanted Behavior ×2 | was When; a bad binding is a fault. Split by condition: title in no feature file (core) / not in the feature the call names |
| r26 | r26 | Event-Driven | unchanged meaning |
| r27 | r27 | Unwanted Behavior | the two commands moved into the condition so the line names one system, `features` |
| r28 | r28, r71 | Event-Driven ×2 | the rewrite, nothing else changed (core) / the printed count |
| r29 | r29 | Unwanted Behavior | unchanged meaning |
| r35 | r35, r72 | Unwanted Behavior ×2 | split by condition: no file has the title (core) / several files have it, without `--file` |
| r36 | r36 | Unwanted Behavior | unchanged meaning |
| r37 | r37, r73 | Unwanted Behavior ×2 | split by condition: only in `--from`, missing (core) / only in the other tree, added |
| r38 | r38 | Event-Driven | was ubiquitous; the trigger is `features list --tag` run |
| r39 | r39 | Event-Driven | unchanged meaning |
| r40 | r40, r74 | Unwanted Behavior ×2 | was When; split by condition: no `Deprecated for:` line (core) / replacement with no `@r<n>` tag |
| r41 | r41 | Unwanted Behavior | unchanged meaning |
| r42 | r42 | Unwanted Behavior | unchanged meaning |
| r46 | r46 | Unwanted Behavior | unchanged meaning |
| r51 | r51 | Event-Driven | **changed to 0052's rule**: `features tag` adds `@r<n>` and keeps the scenario's other `@r<m>` tags, instead of making it the one requirement tag |
| r52 | r52 | Optional | unchanged meaning |
| r53 | r53 | Unwanted Behavior | unchanged meaning |
| r54 | r54 | Unwanted Behavior | unchanged meaning |
| r55 | r55 | Unwanted Behavior | unchanged meaning |
| r56 | r56, r75 | Complex (Where, When), Event-Driven | split the "; without `--file`" clause: with `--file` (core) / without it |
| r57 | r57, r76 | Event-Driven ×2 | was ubiquitous; split by what the path names: a feature file (core) / a directory |
| r58 | r58, r77, r78 | Complex (Where, When) ×2, Complex (Where, If) | feature files named after `--unbound` (core) / none named, every feature file under `--dir` / exit 1 if a scenario is bound by no call |
| r59 | r59 | Complex (Where, If) | unchanged meaning |

## Scenario tags

Of features/feature-file-tools.feature (its titles still say "hold"/"held"/"holding" where the spec says
"deprecate"; the titles are as they stand today):

- "every feature file under the directory is read, and docstring text is not" (@r1): gains @r60
- "an edit is refused only when it would leave a Rule: block outside a docstring" (@r3): gains @r61, @r62
- "counting by tag counts outline rows, inherited tags and untagged scenarios" (@r4): gains @r63
- "retagging a title that is not in exactly one file is refused" (@r10): gains @r64
- "holding a scenario marks it held and records what for" (@r19): gains @r65, @r66
- "the holding list shows each held scenario and what will retire it" (@r21): gains @r67, @r68, @r69
- "a binding that names no scenario is reported" (@r25): gains @r70
- "rebinding rewrites each binding of the old title and counts them" (@r28): gains @r71
- "moving a title that no file or several files hold is refused" (@r35): gains @r72
- "a title in only one tree is missing or added" (@r37): gains @r73
- "the holding list flags a held scenario it cannot place" (@r40): gains @r74
- "rebind --file rewrites only the bindings whose feature names that file" (@r56): gains @r75

r57, r58 have no scenario yet (`v_s3` today); when they get one, r57's names r57 and r76, r58's names r58, r77 and
r78.

**Deprecated, replaced at formulation:** "tagging with a requirement id makes it the scenario's one requirement
tag" (@r51) gains no tag but now contradicts r51 under 0052 (its Then expects the scenario's other `@r<m>` tags
removed). At formulation it is to be tagged `@deprecated`, deprecated for a new r51 scenario in which the other
`@r<m>` tags are kept, and retired by the work-item that turns that replacement green.

## Questions

1. One response. "Refuse …, naming X, and change no file" and "print X and exit N" are one line each (the shared
   rule); an "and nothing else changes" on an edit is part of that edit. Separate effects (a rewrite and a printed
   count, r28/r71) and separate conditions are split. Choice: as written.
2. r51 under 0052. Choice: `tag` adds `@r<n>` and keeps every other `@r<m>` (a scenario may name several
   requirements). The other reading, keep replacing but offer a flag to add, was not chosen.
3. r10 / r35 split by condition: "naming every file that has it" names nothing when no file has the title.
   Choice: the no-file lines (r10, r35) say only "refuse and change no file"; the several-files lines (r64, r72)
   name the files.
4. r37 / r73 "names it as missing or as added": which is which was implied. Choice, from the Implementation line
   ("missing from or added to the second tree"): only in `--from` is missing, only in the other tree is added.
5. r56 / r75: "without `--file` it rewrites every binding of the old title" repeats r28's "each binding call that
   names it". Choice: kept as its own line, so nothing is lost.
6. r58 / r78: "exits 1 when there is one" read as: when any scenario is bound by no call, whichever files
   `--unbound` reads. Choice: one line under Where `--unbound`.
7. r3 / r62: "checks nothing else of the result" written as checking the result for nothing but a `Rule:` block
   outside a docstring. Choice: its own Event-Driven line.
8. r19 / r65: "whether or not the replacement exists yet" placed on the `--for` line, the only one with a
   replacement. Choice: as written.

## Consistency pass

- No line changed. Lines already follow the shared rule (a message with its exit status, or a refusal that changes
  no file, is one line); every `**If**` has "then"; clauses in EARS order.
- Noted above: the r51 scenario is to be deprecated and replaced at formulation.
~~~~~~

## `.shop/scratch/ears/round1/map/formulation.md`

~~~~~~
# formulation: old ids to EARS lines

Highest id ever used before: r14 (`retired: []`). New ids: r15–r21. Lines 14 → 21.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r15 | Event-Driven, Ubiquitous | split: r1 where the scenarios go and their shape (core), r15 every scenario not deprecated formulates a line |
| r2 | r2 | Ubiquitous | meaning unchanged |
| r3 | r3, r16 | Unwanted Behavior, Unwanted Behavior | split: r3 the question instead of a scenario (core), r16 the rest of the capability is formulated |
| r4 | r4 | Event-Driven | "and its old scenario passes today" folded into the trigger ("a line whose old scenario passes today"), so one trigger |
| r5 | r5 | Event-Driven | as r4 |
| r6 | r6, r17 | Event-Driven, Event-Driven | split: r6 `features bindings` reports every binding names a scenario (core; the system is the script), r17 what the commit contains |
| r7 | r7 | Event-Driven | meaning unchanged |
| r8 | r8 | Ubiquitous | a form written as what the skill shall do with it |
| r9 | r9 | Ubiquitous | meaning unchanged |
| r10 | r10 | Event-Driven | trigger is the person's ruling; the response keeps its two alternatives (rewrite, or a question) as one choice |
| r11 | r11 | Ubiquitous | **changed to 0052's rule**: one `@r<n>` tag per line the scenario formulates, all of one capability, instead of the tag of the one line; "its title is free" kept as "whatever the scenario's title" |
| r12 | r12, r18 | Event-Driven, Ubiquitous | split: r12 keeps its tags (core; "tag" → "tags" for 0052), r18 it formulates no line |
| r13 | r13, r19, r20, r21 | Complex (Where, When) ×2, Optional ×2 | split by response and by option: r13 no scenario naming no line (core), r19 no line without a scenario, r20 the round says so, r21 the round checks by hand. **Changed to 0052's rule**: "names … two" became "names lines of two capabilities" |
| r14 | r14 | Event-Driven | meaning unchanged |

Lines that stated one tag per scenario: r11 (named in the brief) and r13 ("names no line or two"), both changed
to 0052's rule; r12's "the `@r<n>` tag" became "tags".

Implementation, may change: "its line's condition … the `@r<n>` tag is what names the line" changed to the
plural, so it does not contradict r11.

## Scenario tags

There is no `features/formulation.feature`, so no scenario gains tags now. When the capability is formulated,
the scenario of each old id names its new ids too:

- r1's scenario: @r1 @r15
- r3's scenario: @r3 @r16
- r6's scenario: @r6 @r17
- r12's scenario: @r12 @r18
- r13's scenario: @r13 @r19 @r20 @r21 (r20 and r21 need the case where `model check` cannot run; 0052 keeps
  it one scenario, so it is an outline or the old scenario covers both cases)

## Questions

1. r13: the old "names no line or two" contradicts 0052 once scenarios may name several lines. Choice: a
   scenario whose lines are of two capabilities, which is what 0052 still forbids.
2. r15: "every scenario that is not deprecated formulates a line" written as what the skill shall not commit;
   read as "at least one line" under 0052.
3. r18: "formulates no line" for a deprecated scenario written as the skill counting it as formulating none;
   the observable is `model check`'s coverage, which the line does not name. Kept without naming it.
4. r20/r21: "the round says so" — to whom is not stated; kept unstated. The system is named the
   `initiative-round` that formulates, as "the round" was.
5. r10: one response with two alternatives (rewrite, or a question with two readings) kept as one line; the
   choice between them is not a second condition the old line stated.

## Consistency pass

- r12, r17: "it shall" written "`formulating-features` shall", the system named in the line.
~~~~~~

## `.shop/scratch/ears/round1/map/migration-tools.md`

~~~~~~
# migration-tools: old ids to EARS lines

Highest id ever used: r45 (`retired: []`); new ids start at r46. 45 lines become 69; r47 and r70 are not used (see Consistency pass).

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1 | ubiquitous | unchanged meaning |
| r2 | r2, r46 | When; When | the print kept on r2; the exit 1 split off as r46 (two responses) |
| r3 | r3 | When | the message with its exit 0: one line |
| r4 | r4 | If … then | both commands in one condition (one rule for two subcommands) |
| r5 | r5 | If … then | the two facts are one joint condition, kept on one line |
| r6 | r6, r48 | If … then; If … then | two conditions: the form (r6), not the id `spec/index.md` has (r48) |
| r7 | r7 | Where | "changes no file" kept as "without changing any file" |
| r8 | r8 | When | the count printed with the changes, one print response |
| r9 | r9 | If … then | |
| r10 | r10 | When | "changes no file" as "without changing any file" |
| r11 | r11 | When | a data shape ("frontmatter has the id") written as what `migrate` writes |
| r12 | r12 | When | |
| r13 | r13, r49 | When; When | two responses: `retired: []` (r13), the `id` rewritten (r49) |
| r14 | r14, r50, r51, r52, r53 | When ×5 | one line per kind of reference found; "nothing else in a reference changes" is r53 |
| r15 | r15 | When | |
| r16 | r16 | If … then | |
| r17 | r17 | When | one response: the moves, as a list |
| r18 | r18 | If … then | |
| r19 | r19, r54 | When; When | "any frontmatter it had is kept" split off as r54 (it was a second sentence) |
| r20 | r20, r55 | When; When | the rewrite (r20), the listing of non-Markdown files (r55) |
| r21 | r21, r56 | When; When | two conditions: a `.superpowers/` line (r21), neither line (r56) |
| r22 | r22, r57 | When; When | the decision files (r22), the removal of `spec/decisions.md` (r57) |
| r23 | r23, r58 | ubiquitous → When; When | a form written as what `migrate run` writes: frontmatter (r23), body (r58) |
| r24 | r24, r59 | If … then; If … then | two conditions: another property line (r24), no `date:` (r59) |
| r25 | r25, r60, r61 | When ×3 | three treatments of a source's parts: moved path (r25), node id (r60), the rest to `by` (r61) |
| r26 | r26 | When | |
| r27 | r27 | When | one rewrite of one scenario, its three parts listed; "nothing else" as "changing nothing else in it" |
| r28 | r28 | When | |
| r29 | r29, r62 | If … then; If … then | two conditions: does not parse (r29), old title over several lines (r62) |
| r30 | r30, r63 | ubiquitous → When; Where | the default plan (r30), the `--plan` option (r63) |
| r31 | r31, r64 | If … then; If … then | two conditions: no plan (r31), several (r64) |
| r32 | r32 | If … then | |
| r33 | r33 | When | |
| r34 | r34 | When | **changed to 0052's rule**: `accepts` each `@r<n>` tag of the scenario, not "the requirement tag" |
| r35 | r35, r65 | If … then; If … then | two conditions: no such title (r35), a scenario with no tag (r65) |
| r36 | r36 | When | |
| r37 | r37 | Where → When | not an option but a fact of the plan, so event-driven |
| r38 | r38 | When | |
| r39 | r39, r66, r67 | When ×3 | the initiative (r39), its source observation appended (r66), one proposal per capability (r67) |
| r40 | r40 | If … then | |
| r41 | r41, r68 | When; When | "says so, writing nothing" (r41), "still writes the observations" (r68) |
| r42 | r42 | When | the response is what `migrate` writes, as `model check` sees it |
| r43 | r43 | When → Where | `--dry-run` is an option, as in r7 |
| r44 | r44, r69 | If … then; If … then | two conditions: `--drop` (r44), `--leave` (r69) |
| r45 | r45, r71 | If … then ×2 | why on stderr and exit 1 without changing any file (r45), bad usage exit 2 (r71) |

## Scenario tags

`features/migration-tools.feature` does not exist yet (the capability has no feature file), so no scenario
gains tags now. When it is formulated, the scenario for each old id names every new id of its row above,
e.g. the scenario of r14 is tagged `@r14 @r50 @r51 @r52 @r53`.

## Questions

1. **"changes no file" with a refusal or a dry run** (r5, r6, r48, r7, r10, r40, r41, r45): taken as the
   extent of the one response ("refuse without changing any file"), not a second response. Choice: kept on
   the same line. Splitting them would add eight lines.
2. **One rule for two subcommands** (r4, r7, r8, r9: `migrate run` or `migrate plan`): taken as one trigger.
   Choice: one line each; not split per subcommand.
3. **r11**: "`spec/index.md`'s frontmatter has the context's `id`, written when it had none" becomes "when
   `spec/index.md` has no `id`, write it". The case where it already has one is covered by r48 (refusal on a
   different id). Choice: the case of an id equal to `--context` needs no line.
4. **r34 under 0052**: a scenario with several tags; does the work-item accept all of them or one? Choice:
   all of its `@r<n>` tags, since the slice accepted the scenario as a whole.
5. **r31**: with no living plan, "naming those it found" names nothing. Choice: r31 "refuse, saying so";
   r64 names the plans found.
6. **r30**: read as "the default when `--plan` is not given". Choice: r30 is When with no `--plan`; r63 is
   Where `--plan`.
7. **r37**: was Where; the condition is a fact about the plan, not an option. Choice: When.
8. **r45**: "changes no file" kept with the stderr message and the exit 1, one line (see Consistency pass).

## Consistency pass

- r47 merged back into r3 and r70 into r45: a message with its exit status is one line (the shared rule). r47 and
  r70 are not used; they were never published, so they need no `retired:` entry. The scenarios of r3 and r45, when
  formulated, do not name them. Lines 45 → 69.
~~~~~~

## `.shop/scratch/ears/round1/map/planning.md`

~~~~~~
# planning: old ids to EARS lines

Highest id ever used before: r14 (retired: none). New ids r15–r21. Lines 14 → 21.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r15, r16 | Event-Driven ×3 | split by response: the plan in the plan file (core) / the result file's contents / the checkout unchanged |
| r2 | r2, r17 | Event-Driven ×2 | was ubiquitous on "the plan"; the trigger is the planner writing it. Why each scenario is red (core) / a reason the notes mark `read` marked unverified |
| r3 | r3 | Event-Driven | trigger and system made explicit; meaning unchanged |
| r4 | r4, r18 | Event-Driven ×2 | the list with what becomes of each test (core) / an empty list says what was checked |
| r5 | r5 | Event-Driven | trigger and system made explicit; one response naming three things |
| r6 | r6 | Event-Driven | "has no" written as "shall put in it no" |
| r7 | r7 | Unwanted Behavior | unchanged meaning; one two-part condition |
| r8 | r8 | Unwanted Behavior | system named: the planner gives it as a question |
| r9 | r9 | Event-Driven | trigger made explicit: the planner giving the final file set |
| r10 | r10, r19 | Event-Driven ×2 | the old "when … and otherwise": a wrong answer or lost data on the path planned as a fix here (core) / any other defect given as an observation |
| r11 | r11 | Event-Driven | system named: the planner says it in the plan's decisions |
| r12 | r12, r20 | Optional, Complex (Where, When) | the randomized test named (core) / writing it made part of the plan when none exists |
| r13 | r13 | State-Driven | was ubiquitous; reading is for the period of planning. "and no other code" kept in the line |
| r14 | r14, r21 | Event-Driven ×2 | split by response: the status (core) / the summary under fifteen lines |

## Scenario tags

`features/planning.feature` does not exist yet, so no scenario gains tags now. When it is formulated, the scenario
for each old id names its new ids too: r1 + r15, r16; r2 + r17; r4 + r18; r10 + r19; r12 + r20; r14 + r21.

## Questions

1. r2–r6, r9: the old lines described the plan ("The plan says …"). Choice: Event-Driven, "When the planner
   writes the plan, the planner shall …", the planner being the named system; "shall have" for what holds when
   planning ends (r1, r14–r16, r21).
2. r10 / r19: "the plan fixes it in this work-item" written as the planner planning its fix in this work-item;
   "otherwise" written out as its complement, a defect that is neither a wrong answer nor lost data on the
   work-item's path. Choice: two lines.
3. r12 / r20: "and the work-item writes it when none exists" is a condition of absence. Choice: Where + When no
   such test exists, the planner making its writing part of the work-item's plan.
4. r13: "and no other code" read as no code beyond the files of the file set (`spec/`, `features/`, `CLAUDE.md`
   and the notes are not the code the line restricts). Choice: one State-Driven line.
5. r12 / r20 "the system" is the system the work-item changes, as in the old line, not the line's named system
   (the planner). Choice: kept.

## Consistency pass

- No line changed.
~~~~~~

## `.shop/scratch/ears/round1/map/red-green.md`

~~~~~~
# red-green: old ids to EARS lines

Highest id ever used: r19 (retired: none). New ids from r20.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r20 | Event-Driven | split by response: r1 the accepted scenarios pass (core), r20 the suite record's passes still pass; trigger made the implementer's report (Q1) |
| r2 | r2 | Ubiquitous | unchanged meaning ("No commit … changes" as "shall not commit a change") |
| r3 | r3, r21, r22 | Unwanted Behavior | the approved example: one condition per line |
| r4 | r4, r23 | Unwanted Behavior | split by condition: r4 Then line, r23 setup-only failure |
| r5 | r5 | Unwanted Behavior | unchanged meaning; the two-part condition is one condition (both must hold) |
| r6 | r6, r24 | Event-Driven | split by trigger: r6 setup change, r24 rewrite of a test committed after the base |
| r7 | r7, r25 | Event-Driven | split by response: r7 the `HAND-BACK` result (core), r25 the commit of the work so far |
| r8 | r8, r26 | Event-Driven | split by response: r8 the report, r26 the commits in the result |
| r9 | r27, r28, r9, r29 | Unwanted Behavior | four responses, four lines; r9 keeps the `PARTIAL` stop, the line's core (Q2) |
| r10 | r10, r30 | Event-Driven | split by response: r10 the code chooses nothing (core), r30 the open question |
| r11 | r11, r31 | Event-Driven | split by response: r11 no paste (core), r31 says so |
| r12 | r12 | Unwanted Behavior | unchanged meaning |
| r13 | r13 | Unwanted Behavior | unchanged meaning; one two-part condition |
| r14 | r14, r32 | Unwanted Behavior | split by condition: r14 open decision, r32 size limit with no rule |
| r15 | r15, r33, r34 | Unwanted Behavior | split by condition: no scripts directory, no result file, `bdd-red-green` missing |
| r16 | r16, r35 | Ubiquitous | split by response: r16 the status set, r35 the summary length |
| r17 | r17, r36, r37 | Unwanted Behavior | the old line's two sentences; the refusal's two responses (commit, stop) split into r36 and r37 |
| r18 | r18, r38 | Ubiquitous | split by response: r18 worktree and branch, r38 no push, merge, rebase or reset |
| r19 | r19 | Ubiquitous | unchanged meaning |

Lines: 19 before, 38 after.

## Scenario tags

features/red-green.feature does not exist yet. When it is formulated, the scenario for each old id names
its new ids too: r1 + r20; r3 + r21, r22; r4 + r23; r6 + r24; r7 + r25; r8 + r26; r9 + r27, r28, r29;
r10 + r30; r11 + r31; r14 + r32; r15 + r33, r34; r16 + r35; r17 + r36, r37; r18 + r38.

## Questions

1. r1/r20: "When a work-item is done" has no actor. Choice: the trigger is the implementer reporting the
   work-item done (the result `DONE` or `DONE_WITH_CONCERNS`), so the implementer is the system; the
   alternative, a work-item moved to done by `work run`, would make it a line of supervision.
2. r9: which of the four responses is the core. Choice: the `PARTIAL` stop at a green commit keeps r9; the
   other three (name the files first, touch only those, a report to continue from) take r27, r28, r29.
3. r10: "the code does not choose its behaviour" written as the implementer not having the code choose it,
   so that the named system is the implementer.

## Consistency pass

- No line changed.
~~~~~~

## `.shop/scratch/ears/round1/map/review.md`

~~~~~~
# review: old ids to EARS lines

Highest id ever used: r14 (retired: none). New ids from r15.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r15 | Event-Driven | split by response: r1 the findings and result files (core), r15 the checkout left as it was |
| r2 | r2, r16 | Event-Driven | split by response: r2 the grade (core), r16 what each finding gives |
| r3 | r3, r17 | Event-Driven, Unwanted Behavior | r3 lists the removed or weakened test; r17 the Important grade of one the plan did not list |
| r4 | r4, r18 | Event-Driven | split by trigger: r4 setup-only change, r18 rewrite of a test this initiative wrote |
| r5 | r5 | Unwanted Behavior | was ubiquitous; a contradiction found is a fault, so If … then (Q1) |
| r6 | r6, r19 | Unwanted Behavior | the old line's two clauses: r6 branch reviewer fails the review, r19 task reviewer lists separately |
| r7 | r7, r20, r21 | Event-Driven | split by response: r7 wall time, r20 shape against `CLAUDE.md`, r21 coupling |
| r8 | r8 | Event-Driven | unchanged meaning |
| r9 | r9 | Optional | unchanged meaning; "the system" written "the system reviewed", since the named system is now the branch reviewer |
| r10 | r10 | Unwanted Behavior | unchanged meaning |
| r11 | r11 | Event-Driven | unchanged meaning; one report listing three kinds |
| r12 | r22, r12, r23, r24, r25 | Ubiquitous, Event-Driven | r22 names the work-item; r12 names the triage (core); the triage's three cases, one line each (Q2) |
| r13 | r13, r26 | Ubiquitous | the old line's two clauses: r13 task review, r26 branch review |
| r14 | r14, r27 | Event-Driven | split by response: r14 observation with a check (core), r27 the work-item it would unblock ("if any" becomes the trigger) |

Lines: 14 before, 27 after.

## Scenario tags

features/review.feature does not exist yet. When it is formulated, the scenario for each old id names its new
ids too: r1 + r15; r2 + r16; r3 + r17; r4 + r18; r6 + r19; r7 + r20, r21; r12 + r22, r23, r24, r25;
r13 + r26; r14 + r27.

## Questions

1. r5: the old line states a grading rule with no trigger. Choice: unwanted behaviour, "If the commits reviewed
   show behaviour that contradicts …", since what starts it is a fault found; "whether or not a scenario covers
   it" stays in the response.
2. r12: the triage was a colon list of three cases. Choice: r12 keeps "names its triage, one of fix now,
   observation or drop" and each case is its own event-driven line (r23 fix now, r24 observation with its
   reproduction, r25 drop), the trigger being what the reviewer finds; "hardening" is written "something to
   harden".
3. r1, r2, r16, r20, r21: "When a review ends, … are/is" written as what the reviewer "shall have" done by then,
   keeping the trigger at the end of the review rather than moving it to its start.

## Consistency pass

- No line changed.
~~~~~~

## `.shop/scratch/ears/round1/map/role-boundaries.md`

~~~~~~
# role-boundaries: old ids to EARS lines

Highest id ever used: r6 (retired: none). New ids from r7. Every line is ubiquitous: an agent definition holds
with no trigger. The named system is the plugin's agent definitions, as the Purpose names them.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1 | Ubiquitous | unchanged meaning |
| r2 | r2 | Ubiquitous | unchanged meaning |
| r3 | r3 | Ubiquitous | unchanged meaning; one response, a tool list without edit or shell |
| r4 | r4, r7, r8, r9 | Ubiquitous | split by response: r4 only the listed skills (core), r7 `bdd-red-green` among them, r8 no Skill tool, r9 the skill listing kept out of its context (Q1) |
| r5 | r5, r10, r11, r12 | Ubiquitous | split by response: r5 each names its model (core), r10 Opus, r11 Sonnet, r12 Haiku |
| r6 | r6 | Ubiquitous | unchanged meaning |

Lines: 6 before, 12 after.

## Scenario tags

None: role-boundaries is guarantees, checked against `agents/*.md` by `tests/scripts/test_agents.py`, not by
scenarios, and features/role-boundaries.feature does not exist. That test's check of r4 covers r7, r8, r9, and
its check of r5 covers r10, r11, r12.

## Questions

1. r4/r9: "so the listing of every installed skill never enters its context" is the consequence of having no
   Skill tool. Choice: kept as its own line, r9, so nothing is dropped; the alternative is to treat it as
   rationale and leave it to r8, which would drop it from Behaviour.

## Consistency pass

- r5: "Each of the plugin's agent definitions shall name its model" written "The plugin's agent definitions shall
  name each agent's model", the same system as every other line.
~~~~~~

## `.shop/scratch/ears/round1/map/spec-consistency.md`

~~~~~~
# spec-consistency: old ids to EARS lines

Highest id ever used before: r11 (`retired: []`). New ids: r12–r20. Lines 11 → 20.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r12 | Event-Driven, Event-Driven | split: r1 runs `model check` first (core), r12 reports its `v_t` rows as findings |
| r2 | r2 | Event-Driven | meaning unchanged |
| r3 | r3, r13, r14 | Event-Driven ×3 | three responses split, the system named the `spec-checker`: r3 reads only `spec/` and `features/` (core), r13 findings to a file, r14 short reply |
| r4 | r4, r15 | Complex (Where, When), Optional | "in report mode" is an option, so Where. Split: r4 the findings file (core), r15 changes nothing else |
| r5 | r5, r16 | Optional, Complex (Where, When) | split: r5 proposes entries first (core), r16 on yes, one gate pass |
| r6 | r6 | Complex (Where, When) | meaning unchanged |
| r7 | r7, r17 | Complex (Where, When) ×2 | split: r7 asks one question (core), r17 the answer goes through the question path |
| r8 | r8 | Complex (Where, When) | meaning unchanged |
| r9 | r9, r18 | Complex (Where, When) ×2 | split: r9 runs `model check` (core), r18 reports before the next step |
| r10 | r10, r19 | Event-Driven ×2 | split: r10 fix mode ends (core), r19 `model check` reports no `v_t` row (system: the script) |
| r11 | r11, r20 | State-Driven, Ubiquitous | was Where; a round running is a period, so While. Split: r11 a round does not run it (core), r20 it runs only when the person asks |

No line here stated one tag per scenario.

## Scenario tags

The frontmatter names `features/spec-consistency.feature`, but the file does not exist, so no scenario gains
tags now. When the capability is formulated, the scenario of each old id names its new ids too:

- r1's scenario: @r1 @r12
- r3's scenario: @r3 @r13 @r14
- r4's scenario: @r4 @r15
- r5's scenario: @r5 @r16
- r7's scenario: @r7 @r17
- r9's scenario: @r9 @r18
- r10's scenario: @r10 @r19
- r11's scenario: @r11 @r20

## Questions

1. r4/r15: "report mode" is not defined elsewhere in the lines; read as an option (Where), the counterpart of
   fix mode, rather than the default when fix mode is not asked for.
2. r14: "replies with a short summary" given the trigger of having written its findings, since the old line
   ordered write then reply.
3. r10/r19: the old line has no "Where fix mode"; kept without it, as the trigger only arises in fix mode.
4. r20: "the check runs when the person asks for it" read as "only when", the contrast the old line drew with
   rounds.

## Consistency pass

- r11: "the round shall not run" written "the `initiative-round` running it shall not run", naming the agent that
  runs integration and formulation rounds, as formulation r20/r21 do.
~~~~~~

## `.shop/scratch/ears/round1/map/spec-integration.md`

~~~~~~
# spec-integration: old ids to EARS lines

Highest id ever used before: r22 (`retired: []`). New ids: r23–r32. Lines 22 → 32.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r23 | Event-Driven, Event-Driven | two responses split: r1 shows the lines (core), r23 shows the questions |
| r2 | r2 | Unwanted Behavior | was Where; "comes from a note" is not an option, so the condition moves to If … then |
| r3 | r3 | State-Driven | "shall not change"; meaning unchanged |
| r4 | r4, r24 | Event-Driven, Event-Driven | split: r4 drafts the answer as a round (core), r24 shows the changed lines again |
| r5 | r5 | Unwanted Behavior | meaning unchanged |
| r6 | r6, r25 | Event-Driven, Event-Driven | split: r6 applies as approved (core), r25 commits alone with approval and date |
| r7 | r7 | Unwanted Behavior | was When; starting a second spec is a fault, so If … then |
| r8 | r8, r26 | Event-Driven, Event-Driven | was Where; the size of the change is the trigger, not an option. Split: r8 writes the lines itself (core), r26 still stops at the gate |
| r9 | r9, r27 | Complex (Where, When), Complex (Where, When) | split by where it is said: r9 the commit (core), r27 a decision's `by` |
| r10 | r10 | Event-Driven | "says so and recommends" folded into one response (recommend, saying why) |
| r11 | r11 | Event-Driven | meaning unchanged |
| r12 | r12 | Event-Driven | meaning unchanged |
| r13 | r13 | Event-Driven | meaning unchanged |
| r14 | r14, r28 | Event-Driven, Ubiquitous | split: r14 adds to `retired` (core), r28 no later line takes a retired id |
| r15 | r15 | Event-Driven | meaning unchanged |
| r16 | r16, r29 | Complex (Where, If … then), Complex (Where, When) | split: r16 any other new problem stops the commit (core, the refusal), r29 formulation clears the three allowed problems |
| r17 | r17 | Complex (Where, When) | "rides with" written as what the session shall do with the change |
| r18 | r18 | Event-Driven | meaning unchanged |
| r19 | r19, r30 | Complex (Where, When), Complex (Where, While) | split: r19 shows it like a line (core), r30 writes nothing to `spec/` before yes |
| r20 | r20, r31 | Event-Driven, Unwanted Behavior | split: r20 the file and its sections (core), r31 no Context or Alternatives unless options were weighed |
| r21 | r21, r32 | Event-Driven, Event-Driven | split: r21 `source` by id (core), r32 what goes in `by` |
| r22 | r22 | Event-Driven | meaning unchanged |

No line here stated one tag per scenario.

## Scenario tags

There is no `features/spec-integration.feature` (and no `formulated_as`), so no scenario gains tags now. When
the capability is formulated, the scenario of each old id names its new ids too:

- r1's scenario: @r1 @r23
- r4's scenario: @r4 @r24
- r6's scenario: @r6 @r25
- r8's scenario: @r8 @r26
- r9's scenario: @r9 @r27
- r14's scenario: @r14 @r28
- r16's scenario: @r16 @r29
- r19's scenario: @r19 @r30
- r20's scenario: @r20 @r31
- r21's scenario: @r21 @r32

## Questions

1. r8: "writes the lines itself … and still stops at the gate before writing them" uses "write" twice. Choice:
   r8 "write the lines itself from `spec/` alone" (drafting them), r26 "stop at the gate before writing them
   to `spec/`".
2. r29: "formulation clears all three" is an obligation on formulation stated in this capability. Choice:
   kept here as its own line, the system named `formulating-features` (the consistency pass; the old line
   said "formulation"); it could move to capability/formulation instead.
3. r28: "no later line takes it" is written as what `integrating-a-proposal` shall not do; it overlaps r12
   (a new id is above every retired one) but is kept, since dropping it would drop a sentence.
4. r30: "writes nothing to `spec/`" kept as nothing at all, not only the glossary change.
5. r10: the trigger "this session is the one that brainstormed the note" read as starting an integration in
   that session; the recommendation comes before the integration starts, as before.

## Consistency pass

- r26: "it shall" written "`integrating-a-proposal` shall", the system named in the line.
- r29: "formulation shall clear it" written "`formulating-features` shall clear it", the skill named.
~~~~~~

## `.shop/scratch/ears/round1/map/spec-migration.md`

~~~~~~
# spec-migration: old ids to EARS lines

Highest id ever used before: r23 (`retired: []`). New ids r24–r40. Lines 23 → 40.

"When migration is done, X is Y" lines are written as what `migrating-to-capabilities` shall have done
("shall have …"), the trigger kept; lines that had "migration" or the person as their subject now name the skill.

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r24, r25 | Unwanted Behavior ×3 | three conditions split as in the approved red-green example: the working tree not clean (core) / a work-item `claimed` / the suite not running cleanly; "says which" written as each line saying its own condition |
| r2 | r2, r26 | Event-Driven, State-Driven | what the person is shown (core) / nothing under `spec/` changed while the person has not said yes |
| r3 | r3 | Unwanted Behavior | system named; meaning unchanged |
| r4 | r4, r27 | Event-Driven ×2 | one feature file per capability (core) / each scenario as it was, the new tags aside |
| r5 | r5 | Event-Driven | meaning unchanged |
| r6 | r6 | Unwanted Behavior | "any of those … beyond what they set aside" written out with r5's terms; "stop and report" one response |
| r7 | r7 | Ubiquitous | meaning unchanged |
| r8 | r8 | Event-Driven | meaning unchanged |
| r9 | r9, r28, r29 | Complex (Where, When) ×3 | split by response: `[r<n>]` on each line (core) / `retired: []` / the capability's id |
| r10 | r10, r30 | Event-Driven ×2 | the context's id (core) / the context path from the person when `spec/index.md` does not name it |
| r11 | r11 | Event-Driven | **changed to 0052's rule**: the `@r<n>` tag of each line the scenario formulates, not of the one line; "nothing else in a scenario changes" kept in the line |
| r12 | r12, r31 | Unwanted Behavior, State-Driven | **changed to 0052's rule**: "no line or more than one" became "no line". The question at the gate (core) / nothing tagged while it is unanswered |
| r13 | r13 | Event-Driven | meaning unchanged |
| r14 | r14, r32, r33 | Event-Driven ×3 | `decision/` references, nothing else in a reference changed (core) / frontmatter ids in full / observation headings |
| r15 | r15 | Event-Driven | meaning unchanged; `migrate status` saying nothing is left kept inside the final layout |
| r16 | r16, r34 | Event-Driven, State-Driven | what is shown at the gate (core) / nothing committed after the mechanical move while the person has not answered |
| r17 | r17, r35, r36, r37 | Event-Driven ×4 | kept slices become work-items (core) / dropped slices only in the archived plan / entries become observations / the plan and its archives become records |
| r18 | r18, r38 | Event-Driven ×2 | retag and retitle (core) / still bound by its test |
| r19 | r19, r39 | Event-Driven ×2 | a decision file per ledger entry (core) / its `source` by id |
| r20 | r20 | Event-Driven | system is the skill, with what `model check` would report as the result; meaning unchanged |
| r21 | r21 | Event-Driven | meaning unchanged |
| r22 | r22, r40 | Event-Driven ×2 | the mechanical move one commit before the gate (core) / the gate's tags, work-items and observations in the commit after it |
| r23 | r23 | Event-Driven | system named; meaning unchanged |

Lines that stated one tag per scenario: r11 (named in the brief) and r12, both changed to 0052's rule.

## Scenario tags

There is no `features/spec-migration.feature`, so no scenario gains tags now. When the capability is formulated,
the scenario of each old id names its new ids too:

- r1's scenario: @r1 @r24 @r25
- r2's scenario: @r2 @r26
- r4's scenario: @r4 @r27
- r9's scenario: @r9 @r28 @r29
- r10's scenario: @r10 @r30
- r12's scenario: @r12 @r31
- r14's scenario: @r14 @r32 @r33
- r16's scenario: @r16 @r34
- r17's scenario: @r17 @r35 @r36 @r37
- r18's scenario: @r18 @r38
- r19's scenario: @r19 @r39
- r22's scenario: @r22 @r40

## Questions

1. r12 under 0052: "formulates no line or more than one" contradicts 0052 once r11 changes. Choice: only "no
   line" is a question now; a scenario naming lines of more than one capability, which 0052 still forbids, is
   left to `model check` and formulation (it is not stated here).
2. r1 / r24 / r25: "says which" written as each split line saying its own condition. Choice: as written.
3. r10 / r30: "the person gives at the gate, unless `spec/index.md` already names them" read as: the person is
   asked only when `spec/index.md` does not name them (r30). Choice: two lines.
4. r31: "tags nothing before the answer" kept as no scenario tagged at all, not only the one in question.
5. r40: "the tags, work-items and observations the gate allowed are the next" read as the next commit, one
   commit. Choice: as written.
6. r6: "stops and reports the difference" kept as one response, a stop that names its reason (the shared rule).
7. r38: "its test still binds it" written as the skill having left the scenario bound by its test.
8. r9 / r28 / r29 keep the old Where ("Where a repository has capability files whose Behaviour lines have no
   ids"), while r30 puts a like fact about the repository (`spec/index.md` naming no owner) in a When. Choice:
   kept as written, Where being a repository's configuration as in spec-integration r17/r19; the person may
   make r9, r28, r29 When.

## Consistency pass

- No line changed.
~~~~~~

## `.shop/scratch/ears/round1/map/supervision.md`

~~~~~~
# supervision: map

35 lines → 84. New ids r36–r85 (highest used before: r35, nothing retired); r62 is not used (see Consistency pass).

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r36, r37, r38, r39, r40 | Event-Driven ×6 | r1 pulls the work-items through their stages (core); one line per stage's worker: `drafted` → `code-scout` (r36), `researched` → `bdd-planner` (r37), `ready` → `bdd-implementer` (r38), `done` with a named risk → `bdd-task-reviewer` (r39), every work-item `done`, `green` or `withdrawn` → `bdd-branch-reviewer` (r40) |
| r2 | r2, r41 | Event-Driven, Ubiquitous | the new session and its brief (core) / no worker is resumed |
| r3 | r3, r42, r43 | Ubiquitous, Unwanted Behavior ×2 | outcome only from the result file (core) / no result file / result file not in its stage's form |
| r4 | r4, r44 | Unwanted Behavior ×2 | a new worker once more (core) / the second failure to `awaiting-ruling` |
| r5 | r5, r45, r46 | Unwanted Behavior ×3 | the file put back (core) / the stage failed / the file logged |
| r6 | r6, r47, r48 | Event-Driven ×2, Unwanted Behavior | file set and notes written (core) / moved to `researched` / an empty file set fails the stage |
| r7 | r7, r49, r50 | Event-Driven ×3 | `DONE`: fields written (core) / `DONE`: moved to `planned` / `QUESTION`: to `planned`, then `awaiting-ruling` |
| r8 | r8, r51 | Event-Driven ×2 | `planned` → `ready` when the guard allows (core) / a `ready` one claimed when an implementer's place is free |
| r9 | r9, r52 | Event-Driven, Ubiquitous | own worktree on a branch from the initiative branch's head (core) / no more implementers at once than `delivery.toml` allows, 2 when it says nothing |
| r10 | r10, r53, r54, r55, r56 | Event-Driven ×3, Unwanted Behavior, Event-Driven | rebase (core) / run the scenarios or check and the suite / merge fast-forward when they pass / no merge if anything that passed in the last suite record fails / moved to `done` on the merge |
| r11 | r11 | Unwanted Behavior | unchanged meaning; "does not merge them" kept in the line as "without merging the commits" |
| r12 | r12, r57 | Unwanted Behavior ×2 | split by condition: the rebase conflicts (core) / the scenarios or the suite fail; "leaving the initiative branch as it was" in each |
| r13 | r13, r58 | Event-Driven, Unwanted Behavior | first to third `PARTIAL` in a row: a continuation (core) / the fourth: `awaiting-ruling` |
| r14 | r14, r59 | Event-Driven ×2 | `awaiting-ruling`, worktree and branch kept (core) / claim released |
| r15 | r15, r60, r61 | Event-Driven, State-Driven, Event-Driven | back to `ready` (core) / kept at `ready` while the other claim is `claimed` / the next implementer continues on the same branch |
| r16 | r16 | State-Driven | unchanged meaning |
| r17 | r17 | Event-Driven | unchanged meaning: the exit with its printout is one line |
| r18 | r18, r63, r64, r65 | Event-Driven ×2, Unwanted Behavior ×2 | one exit status per line: 0 (core) / 3 / 4 on a budget / 1 for any other reason |
| r19 | r19, r66, r67, r68 | Ubiquitous, Unwanted Behavior ×3 | within the role's limits (core) / time reached: ended / spending reached: ended / ended at a limit: the stage failed |
| r20 | r20, r69, r70 | Unwanted Behavior ×3 | was When; reaching the budget stops the run. No further worker (core) / wait for the running ones / exit saying what was spent |
| r21 | r21, r71 | Event-Driven ×2 | task review started (core) / nothing to fix now: `green` once its scenarios pass at the head |
| r22 | r22, r72 | Event-Driven, State-Driven | fix work-items added (core) / not `green` while a fix work-item is not `green` |
| r23 | r23, r73 | Event-Driven ×2 | split by trigger: a review of a work-item, about its capability (core) / a branch review, about the bounded context |
| r24 | r24 | Event-Driven | unchanged meaning |
| r25 | r25, r74 | Event-Driven ×2 | branch review started (core) / nothing to fix now: each `done` work-item whose scenarios pass to `green` |
| r26 | r26, r75, r76, r77 | Event-Driven ×4 | scoped re-review started (core) / a further fix work-item for the three kinds of finding / any other an observation / nothing that gets a further fix: the fix work-item `green` |
| r27 | r27, r78 | Event-Driven ×2 | split by trigger: the line at a worker's start (core) / at its end |
| r28 | r28, r79 | Event-Driven ×2 | suite record appended (core) / the implementer's brief gives the last one |
| r29 | r29 | Event-Driven | unchanged meaning |
| r30 | r30 | Unwanted Behavior | unchanged meaning |
| r31 | r31, r80 | Unwanted Behavior ×2 | split by condition: the default branch (core) / changes outside `.shop/`; "says which" as "saying so" in each |
| r32 | r32, r81, r82 | Event-Driven ×3 | workers ended (core) / each logged as interrupted / the next `work run` continues each `claimed` work-item |
| r33 | r33 | Event-Driven | unchanged meaning; "and changes no … status" kept in the line as "changing no …" |
| r34 | r34, r83 | Event-Driven ×2 | the next stage run alone (core) / `work` exits when it ends |
| r35 | r35, r84, r85 | Event-Driven ×2, Ubiquitous | the start line (core) / the end line with the result's status / nothing a worker wrote printed |

## Scenario tags

`features/supervision.feature` does not exist yet, so no scenario gains tags now. When it is formulated, under
0052 the scenario that formulates each old id names every new id of its row (35 scenarios, as today's lines):

- r1: @r1 @r36 @r37 @r38 @r39 @r40
- r2: @r2 @r41
- r3: @r3 @r42 @r43
- r4: @r4 @r44
- r5: @r5 @r45 @r46
- r6: @r6 @r47 @r48
- r7: @r7 @r49 @r50
- r8: @r8 @r51
- r9: @r9 @r52
- r10: @r10 @r53 @r54 @r55 @r56
- r12: @r12 @r57
- r13: @r13 @r58
- r14: @r14 @r59
- r15: @r15 @r60 @r61
- r18: @r18 @r63 @r64 @r65
- r19: @r19 @r66 @r67 @r68
- r20: @r20 @r69 @r70
- r21: @r21 @r71
- r22: @r22 @r72
- r23: @r23 @r73
- r25: @r25 @r74
- r26: @r26 @r75 @r76 @r77
- r27: @r27 @r78
- r28: @r28 @r79
- r31: @r31 @r80
- r32: @r32 @r81 @r82
- r34: @r34 @r83
- r35: @r35 @r84 @r85

r11, r16, r17, r24, r29, r30 and r33 keep their single tag.

## Questions

1. r1 / r40 / r25: r1 started the branch reviewer "once every work-item is `done`, `green` or `withdrawn`" (r40);
   r25 also requires none `awaiting-ruling` and commits since the last branch review. Choice: both kept as written;
   they overlap, and the person may retire r40 in favour of r25.
2. r8 / r51: "as soon as the queue's guard allows it" read as an event, the guard coming to allow the move.
   Choice: When.
3. r9 / r52: the limit and its default ("2 when it says nothing") kept in one ubiquitous line, the default being
   the setting's value, not a second behaviour. Choice: one Ubiquitous line, not an Optional one.
4. r10 / r55: "only when they pass and nothing fails that passed in the last suite record" read as two lines: the
   merge when they pass (r54) and no merge if anything that passed in the last suite record fails (r55). Choice:
   as written; r57 sends the work-item to `awaiting-ruling` when they fail.
5. r13 / r58: "at most three times in a row" read as the first, second or third `PARTIAL` in a row each getting a
   continuation, and the fourth going to `awaiting-ruling`. Choice: as written.
6. r20: written When before; reaching the run's budget is the stop the line guards against. Choice: If … then on
   all three lines (no further worker, wait, exit saying what was spent).
7. r26 / r77: "any other finding is an observation, and the fix work-item goes to `green`" read as `green` only
   when no finding gets a further fix work-item. Choice: only then.
8. r27 / r78: "and at the end the result's status, …" read as a second line at the worker's end with the start
   line's fields and these. Choice: the end line repeats the start fields.
9. r33: "changes no initiative's or capability-proposal's status" kept in r33's response ("changing no …") rather
   than made a ubiquitous line of its own; the Purpose says it of the script as a whole. Choice: kept in r33.

## Consistency pass

- r62 ("When `work run` exits because no work-item can move, `work run` shall print …") merged back into r17: a
  message with its exit is one line (the shared rule). r62 is not used; it was never published, so it needs no
  `retired:` entry. r17's scenario no longer gains @r62.
~~~~~~

## `.shop/scratch/ears/round1/map/work-queue.md`

~~~~~~
# work-queue: map

24 lines → 47. New ids r25–r48, r39 not used (see Consistency pass) (highest used before: r24, nothing retired).

| old id | new ids | pattern(s) | note |
|---|---|---|---|
| r1 | r1, r25 | Ubiquitous ×2 | reads / needs only the standard library |
| r2 | r2, r26 | Event-Driven ×2 | writes the file / prints the id |
| r3 | r3, r27, r28, r29, r30 | Unwanted Behavior ×5 | one refusal condition per line; "writes nothing" kept inside each refusal |
| r4 | r4 | Unwanted Behavior | unchanged meaning |
| r5 | r5, r31 | Event-Driven, Complex (Where + When) | `--status` is an option |
| r6 | r6 | Event-Driven | unchanged meaning ("changes nothing" kept as "without changing anything") |
| r7 | r7, r32 | Event-Driven ×2 | status written / log line appended |
| r8 | r8 | Unwanted Behavior | unchanged meaning |
| r9 | r9, r33 | Unwanted Behavior ×2 | "only when" restated as two guards that prevent the move |
| r10 | r10 | State-Driven | unchanged meaning |
| r11 | r11, r34, r35 | Event-Driven ×2, Unwanted Behavior | adds / prints / refused when another claim has a path |
| r12 | r12 | Unwanted Behavior | unchanged meaning |
| r13 | r13 | Event-Driven | unchanged meaning |
| r14 | r14, r36 | Event-Driven ×2 | ruling written / moved to planned once every question has an answer |
| r15 | r15, r37 | Unwanted Behavior ×2 | not awaiting-ruling / no such question |
| r16 | r16, r38 | Event-Driven, Unwanted Behavior | withdraw / refused when claimed or green |
| r17 | r17 | Event-Driven | unchanged meaning |
| r18 | r18, r40 | Unwanted Behavior ×2 | why on stderr with exit 1 / wrongly given exits 2 |
| r19 | r19, r41, r42, r43 | Event-Driven ×2, Complex (Where + When), Unwanted Behavior | write / print line / relative import / not a directory |
| r20 | r20 | Ubiquitous | changed to 0052's rule: accepted when one of its `@r<n>` tags is a requirement the work-item accepts (was "its `@r<n>` tag") |
| r21 | r21, r44 | Complex (Where + While + When) ×2 | failure reported as expected / pass fails the run |
| r22 | r22, r45 | Complex (Where + While) ×2 | accepted by a claimed, done or green work-item / accepted by none |
| r23 | r23, r46 | Optional, Complex (Where + If) | run only those / fails when there are none |
| r24 | r24, r47, r48 | Optional, Complex (Where + If), Optional | header names the directory / says none was found / summary counts |

## Scenario tags

`features/work-queue.feature` does not exist yet, so no scenario gains tags now. When it is written, under 0052
the scenario that formulates each old id names these tags (24 scenarios):

- r1: @r1 @r25
- r2: @r2 @r26
- r3: @r3 @r27 @r28 @r29 @r30
- r5: @r5 @r31
- r7: @r7 @r32
- r9: @r9 @r33
- r11: @r11 @r34 @r35
- r14: @r14 @r36
- r15: @r15 @r37
- r16: @r16 @r38
- r18: @r18 @r40
- r19: @r19 @r41 @r42 @r43
- r21: @r21 @r44
- r22: @r22 @r45
- r23: @r23 @r46
- r24: @r24 @r47 @r48

r4, r6, r8, r10, r12, r13, r17, r20 keep their single tag.

## Questions

1. r20 under 0052: a scenario with several tags — accepted by a work-item when any one of its tags is a
   requirement it accepts, or only when all are. Choice: any one (one of its tags). Delivery r19 keeps a
   scenario's requirements on one work-item, so the two readings agree for drafted work-items.
2. r9 "moves … only when": read as a restriction only (two guards, r9 and r33), not also as a promise to move
   when both hold. Choice: restriction only; the move itself is `work run`'s (supervision r8).
3. r3 / r12 / r15 / r44 "refuses … and writes / changes nothing": a refusal with nothing written kept as one
   response ("refuse … without writing anything"), not split. Choice: one line per condition.
4. r18 "a command given wrongly exits 2" made its own Unwanted Behavior line (r40). Choice: If.

## Consistency pass

- r39 merged back into r18: a message with its exit status is one line (the shared rule). r39 is not used; it was
  never published, so it needs no `retired:` entry. Lines 24 → 47.
- r4: system `work add` written `work`, the script, as in every other line of the capability.
~~~~~~

## `.shop/scratch/ears/tmp/analysis-tools.behaviour`

~~~~~~
- [r1] **When** `tools` needs an interpreter, `tools` shall use the first of these, in this order: the one `--python` gives, used as given; `.venv/bin/python` under the current directory, if that file exists; `venv/bin/python` under the current directory, if that file exists; `$VIRTUAL_ENV/bin/python`, if that file exists, wherever `$VIRTUAL_ENV` points; and else the interpreter running the script.
- [r36] **When** `tools probe` is run without `--log`, `tools` shall print the interpreter's path and whether it came from `--python`, from the project's virtualenv (`.venv`, `venv` or `$VIRTUAL_ENV` alike), or from neither.
- [r2] **If** `tools probe`, `tools install` or `tools check` is run in a project that is not a Python project, then `tools` shall say in one line that no analysis tools are known for its language and exit 1.
- [r3] **When** `tools probe` is run, `tools` shall print one line per tool, `<name> <version>` for an installed tool and `<name> missing: <what it is for>` for a missing one, then the interpreter.
- [r37] **If** a tool is missing when `tools probe` is run, then `tools` shall exit 1.
- [r4] **When** `tools probe --log` is run, `tools` shall print one line, `Probe: tools -> ...`, giving each tool with its version or `missing`, for a researcher's notes.
- [r5] **When** `tools install` is run, `tools` shall install each missing tool into the interpreter with pip and edit no dependency file.
- [r6] **If** `tools install` is run with an interpreter that is not a virtualenv, then `tools` shall refuse to install into it and say so.
- [r7] **If** a tool is still missing after `tools install`, then `tools` shall print the tool, what it is for, what the workflow does without it, and the command that failed with the end of its error, and exit 1.
- [r8] **When** `tools map` is run, `tools` shall run the suite once under coverage with a context per test.
- [r38] **Where** arguments are given after `--`, **when** `tools map` is run, `tools` shall pass them to pytest.
- [r39] **When** `tools map` is run, `tools` shall keep the map in `.shop/scratch/tools/coverage`.
- [r9] **When** `tools tests-of <file>[:<function, Class.method or line range>]` is run, `tools` shall print each test that executed it in the last map, one a line, and how many of the map's tests that is, with the commit the map was made at.
- [r10] **Where** `--by-file` is given, **when** `tools tests-of` is run, `tools` shall print a count for each test file instead of each test.
- [r11] **If** no test in the map executed the target of `tools tests-of`, then `tools` shall exit 1.
- [r40] **If** the file `tools tests-of` is given has no function by the name it is given, then `tools` shall exit 1.
- [r12] **If** `tools tests-of` is run when no map has been made, then `tools` shall refuse and say to make one with `tools map`.
- [r13] **When** `tools untested <file>...` is run, `tools` shall print each function in the files that no test in the last map executed.
- [r14] **When** `tools refs <name>` is run, `tools` shall print every reference to that function, class or name defined in the project as `path:line`, including uses through an import or an alias, then one summary line with the number of references, the number of production files that contain them and, as a separate number, the number of test files that contain them, and where the name is defined.
- [r15] **If** `tools refs` is given a name that nothing in the project is defined as, then `tools` shall exit 1.
- [r16] **When** `tools check` is run, `tools` shall run ruff and vulture over the paths given or the Python files changed since `--base`, each under its own heading.
- [r41] **Where** the project has import contracts, **when** `tools check` is run, `tools` shall run import-linter over the project under its own heading.
- [r42] **If** a tool `tools check` runs reports, then `tools check` shall exit 1.
- [r17] **If** a tool `tools check` would run is missing, then `tools` shall name it as missing under its heading instead of skipping it.
- [r18] **While** the interpreter is not a virtualenv, **if** a tool is missing when `tools install` is run, then `tools` shall print for each missing tool the tool, what it is for, what the workflow does without it and that the interpreter is not a virtualenv, and exit 1.
- [r48] **While** the interpreter is not a virtualenv, **if** a tool is missing when `tools install` is run, then `tools` shall install nothing.
- [r19] **When** `tools install` finds every tool present, `tools` shall say so and exit 0, whether or not the interpreter is a virtualenv.
- [r20] **When** `tools install` installs a tool, `tools` shall print that the tool is installed.
- [r21] **If** the interpreter does not run when `tools probe`, `tools install` or `tools check` is run, then `tools` shall refuse, naming the interpreter and the end of its error.
- [r22] **When** `tools probe --log` is run, `tools` shall name every tool in its line with its version or `missing`.
- [r23] **When** `tools map` is run, `tools` shall replace any earlier map.
- [r43] **When** `tools map` is run, `tools` shall print pytest's last line, where the map is and the commit it was made at, and exit 0 whether or not the tests passed.
- [r24] **If** `tools map` makes no map, then `tools` shall refuse, naming the command it ran and the end of its output.
- [r25] **When** `tools untested` is run, `tools` shall print each function as `<path>:<line> <name>`, then how many functions no test executed and the commit the map was made at, and exit 0 however many there are.
- [r26] **If** `tools untested` is run when no map has been made, then `tools` shall refuse and say to make one with `tools map`.
- [r27] **If** coverage is missing from the interpreter when `tools tests-of` or `tools untested` is run, then `tools` shall refuse, saying to run `tools install`.
- [r28] **If** jedi is missing from the interpreter when `tools refs` is run, then `tools` shall refuse, saying to run `tools install`.
- [r29] **If** the file `tools tests-of` is given does not exist, then `tools` shall refuse, naming it.
- [r30] **When** `tools refs` is run on a name the project defines, `tools` shall count no definition as a reference.
- [r44] **When** `tools refs` is run on a name the project defines, `tools` shall name where it is defined.
- [r45] **When** `tools refs` is run on a name the project defines, `tools` shall exit 0 however many references there are.
- [r31] **Where** `--base` is given, **when** `tools check` is run, `tools` shall check the Python files changed since it and not deleted, in place of any paths given.
- [r32] **If** git cannot compare the working tree with `--base`, then `tools check` shall refuse with git's error.
- [r33] **When** `tools check` has no file to check, `tools check` shall say under the ruff and vulture headings that there is nothing to check.
- [r46] **When** `tools check` has no file to check, `tools check` shall not exit 1 for ruff or vulture.
- [r34] **Where** the project states no import contracts, **when** `tools check` is run, `tools check` shall not run import-linter.
- [r47] **Where** the project states no import contracts, **when** `tools check` is run, `tools check` shall say so under the import-linter heading.
- [r35] **When** a tool `tools check` runs prints nothing, `tools check` shall say under its heading that it is clean.
~~~~~~
