---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-i13-ears-round2-maps
kind: initiative-archive
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-19
---

# 0.21.0 EARS restructure (i13), round 2: compaction maps

Round 2 of initiative i13-ears (release 0.21.0), under brief-2.md after decision 0051 changed (commit 26e0dd2): for each built or spec-side capability, original id -> surviving id, 'retired -> rN' or 'dropped: general line rN', the scenario tags that move to the surviving line, and the questions still open. The capability files these maps describe are committed as they were drafted (a844763, identical to .shop/scratch/ears/capabilities/), so only the maps are archived here. Not included: the maps of delivery, migration-tools, planning, supervision and work-queue, identical to round 1's (see the round-1 maps record).

Archived from git-ignored scratch; each file's text as it was.

## `.shop/scratch/ears/map/analysis-tools.md`

~~~~~~
# analysis-tools: original ids to compacted EARS lines (round 2)

Lines: original 35 → round 1 45 → now 15. Highest id ever published: r35. Round-1 ids r36–r48 are unused (never
published); r49 is new, the general line. `retired:` gains r2, r12, r15 and r18 to r35.

`If` lines kept: a missing tool named rather than skipped (r17, r7, the purpose), the refusal to install outside
a virtualenv (r6, protects the person's interpreter), and `tests-of` finding nothing executed (r11, its answer).
Every other refusal is under the general line r49 and listed in Implementation.

| original id | now | note |
|---|---|---|
| r1 | r1 | the interpreter's source printed by `probe` moved into r3 |
| r2 | dropped: general line r49 | "not a Python project" wording in Implementation |
| r3 | r3 | takes r1's second sentence (the interpreter and where it came from) |
| r4 | r4 | takes r22 (names every tool) |
| r5 | r5 | r19 (all present, exit 0) and r20 (prints what it installed) in Implementation |
| r6 | r6 | takes r18 (installs nothing, says so for each missing tool, exit 1); only when there is a tool to install |
| r7 | r7 | unchanged meaning |
| r8 | r8 | takes r23 (replaces the earlier map, exit 0 whether or not tests pass); its printout in Implementation |
| r9 | r9 | unchanged meaning |
| r10 | r10 | unchanged meaning |
| r11 | r11 | unchanged meaning |
| r12 | dropped: general line r49 | |
| r13 | r13 | takes r25 (count, commit, exit 0); the line format in Implementation |
| r14 | r14 | takes r30 (no definition counted); exit 0 in Implementation |
| r15 | dropped: general line r49 | |
| r16 | r16 | takes r31 (`--base`), r33 (nothing to check), r34 (no import contracts), r35 (clean); their wording in Implementation |
| r17 | r17 | takes r27 (coverage) and r28 (jedi): a missing tool named for `check`, `tests-of`, `untested`, `refs` |
| r18 | retired → r6 | |
| r19 | retired → r5 | |
| r20 | retired → r5 | |
| r21 | dropped: general line r49 | |
| r22 | retired → r4 | |
| r23 | retired → r8 | |
| r24 | dropped: general line r49 | |
| r25 | retired → r13 | |
| r26 | dropped: general line r49 | |
| r27 | retired → r17 | |
| r28 | retired → r17 | |
| r29 | dropped: general line r49 | |
| r30 | retired → r14 | |
| r31 | retired → r16 | |
| r32 | dropped: general line r49 | |
| r33 | retired → r16 | |
| r34 | retired → r16 | |
| r35 | retired → r16 | |
| (new) | r49 | the general line for `tools` |

## Scenario tags

In features/analysis-tools.feature, the scenarios whose tag is retired or dropped take the surviving line's tag
instead (none removed, 0052):

- "the interpreter is the first of --python, .venv, venv, $VIRTUAL_ENV and the running one": keeps @r1, gains @r3 (its "says where it came from" is now r3's)
- "a project that is not a Python project has no known analysis tools": @r2 → @r49
- "tests-of without a map says to make one": @r12 → @r49
- "refs fails for a name the project does not define": @r15 → @r49
- "install outside a virtualenv explains each missing tool and installs nothing": @r18 → @r6
- "install with every tool present says so and succeeds": @r19 → @r5
- "install says each tool it installed": @r20 → @r5
- "an interpreter that does not run is refused": @r21 → @r49
- "the probe log line names every tool with its version or missing": @r22 → @r4
- "map replaces the earlier map and succeeds whether or not the tests pass": @r23 → @r8
- "map that makes no map is refused": @r24 → @r49
- "untested prints each function with its place, the count and the commit": @r25 → @r13
- "untested without a map says to make one": @r26 → @r49
- "without coverage tests-of and untested say to install it": @r27 → @r17
- "without jedi refs says to install it": @r28 → @r17
- "tests-of on a file that does not exist is refused": @r29 → @r49
- "refs on a defined name gives its definition apart from its references": @r30 → @r14
- "check with --base checks the changed Python files that remain, in place of the paths given": @r31 → @r16
- "check with a base git cannot compare is refused with git's error": @r32 → @r49
- "check with no file to check says so under ruff and vulture and does not fail for them": @r33 → @r16
- "check without import contracts does not run import-linter": @r34 → @r16
- "a tool that prints nothing is reported clean": @r35 → @r16

## Questions

1. r49 says "change nothing". `tools map` that makes no map (r24, now under r49): does a failed map leave the
   earlier map in place? r8 replaces it; the old r24 did not say. Choice: left as r49 reads; to confirm against
   `scripts/tools` (records/observations.md notes two ways it removes the old map).
2. r17 now covers `check`, `tests-of`, `untested` and `refs` alike ("name it as missing"); for the last three that
   naming is a refusal (exit 1). Choice: the refusal and its "run `tools install`" wording in Implementation.
~~~~~~

## `.shop/scratch/ears/map/batch-measurement.md`

~~~~~~
# batch-measurement: original ids to compacted EARS lines (round 2)

Lines: original 38 → round 1 62 → now 23. Highest id ever published: r38. Round-1 ids r39–r66 are unused (never
published); no new id. `retired:` gains r5, r8, r20, r21, r22, r23, r24, r25, r26, r27, r28, r30, r35, r36, r37.

`If` lines kept: an unknown transcript shape or no dispatch (r6, the purpose "refuses rather than guesses",
decision 0018), an existing facts file not written over (r7, protects a file the transcripts cannot rebuild),
tasks left uncounted rather than guessed (r29). Every other refusal is under the general line, r38, and listed
in Implementation. The facts' counting rules are the purpose and stay, joined where they share a subject.

| original id | now | note |
|---|---|---|
| r1 | r1 | its one-line report (r30) in Implementation |
| r2 | r2 | takes r26 (the open batch's start) and r25's name; Where → When, as round 1 |
| r3 | r3 | unchanged meaning |
| r4 | r4 | takes r25's path for the open batch |
| r5 | dropped: general line r38 | |
| r6 | r6 | takes r8 (no dispatch inside the batch) |
| r7 | r7 | unchanged meaning |
| r8 | retired → r6 | |
| r9 | r9 | unchanged meaning, as what `measure batch` counts |
| r10 | r10 | unchanged meaning |
| r11 | r11 | unchanged meaning |
| r12 | r12 | unchanged meaning |
| r13 | r13 | unchanged meaning |
| r14 | r14 | takes r28 (ambiguous commits) |
| r15 | r15 | takes r27 (which slices the facts hold) |
| r16 | r16 | unchanged meaning |
| r17 | r17 | unchanged meaning |
| r18 | r18 | what `show` prints (r35) in Implementation |
| r19 | r19 | takes r36's per-slice figures and ratio; the rest of r36 in Implementation |
| r20 | dropped: general line r38 | |
| r21 | dropped: general line r38 | its hint (`--plan`) in Implementation |
| r22 | dropped: general line r38 | its hint (`--from`) in Implementation |
| r23 | dropped: general line r38 | |
| r24 | dropped: general line r38 | |
| r25 | retired → r2, r4 | |
| r26 | retired → r2 | |
| r27 | retired → r15 | |
| r28 | retired → r14 | |
| r29 | r29 | the note on stderr in Implementation |
| r30 | retired → r1 | |
| r31 | r31 | unchanged meaning |
| r32 | r32 | unchanged meaning |
| r33 | r33 | unchanged meaning |
| r34 | r34 | unchanged meaning |
| r35 | retired → r18 | |
| r36 | retired → r19 | |
| r37 | dropped: general line r38 | |
| r38 | r38 | now the general line ("exit non-zero, say why on stderr, change nothing") |

## Scenario tags

In features/batch-measurement.feature, the scenarios whose tag is retired or dropped take the surviving line's tag
instead (none removed, 0052):

- "an archive file no commit added is refused": @r5 → @r38
- "a batch with no dispatch inside it is refused": @r8 → @r6
- "show refuses a file measure did not write as facts": @r20 → @r38
- "the open batch needs --plan when the living plan cannot be found": @r21 → @r38
- "a batch with no archive before it needs --from": @r22 → @r38
- "a --<option> that is neither a commit nor an ISO time is refused": @r23 → @r38
- "git's failures are refused with git's error": @r24 → @r38
- "the open batch is named by --name, default open": @r25 → @r2, @r4
- "the open batch starts at the last commit that added a file under the archive directory": @r26 → @r2
- "the facts hold the slices the batch planned and the slices dispatches were attributed to": @r27 → @r15
- "a commit made while two implementers ran is counted as ambiguous": @r28 → @r14
- "a written batch is reported in one line": @r30 → @r1
- "show prints the header, the tables, the exceptions, the hand-backs and the notes": @r35 → @r18
- "compare prints both files' figures with the ratio of the second to the first": @r36 → @r19
- "a file measure cannot read as its facts is refused": @r37 → @r38

## Questions

1. r8 (no dispatch inside the batch) kept as an `If` line, joined to r6: a facts file of zeros would be a guessed
   number (0018). Choice: as written; say if it is a minor refusal for r38.
~~~~~~

## `.shop/scratch/ears/map/code-research.md`

~~~~~~
# code-research: original ids, round 2

Lines: 11 original → 18 round 1 → 10 now. Highest id ever used: r19 (round 1; r13–r19 were never published and
are unused). `retired:` gains r7.

| original id | now | note |
|---|---|---|
| r1 | r1 | one response, the state research leaves (r13, r14 unused) |
| r2 | (retired before round 1) | |
| r3 | r3 | "changes or replaces" one trigger again (r15 unused) |
| r4 | r4 | why each scenario is red, from a run; the `run`/`read` marking of probes and conclusions moved to Implementation as the notes' form (r16, r17 unused) |
| r5 | r5 | unchanged meaning |
| r6 | r6 | unchanged meaning |
| r7 | retired: output format, to "Implementation, may change" | where each count came from |
| r8 | r8 | unchanged meaning |
| r9 | r9 | one line (r18 unused); protects the checkout's data |
| r10 | r10 | unchanged meaning |
| r11 | r11 | unchanged meaning |
| r12 | r12 | now the general line for the researcher; the status set and the summary length moved to Implementation (r19 unused) |

## Scenario tags

`features/code-research.feature` does not exist yet; no scenario changes. No scenario is written for r7.

## Questions

None open.
~~~~~~

## `.shop/scratch/ears/map/design-model-check.md`

~~~~~~
# design-model-check: original ids to compacted EARS lines (round 2)

Lines: original 65 → round 1 100 (98 + r103, r104) → now 50 (23 lines + 27 rows of the reports table).
Highest id ever published: r67. Round-1 ids r68–r102 are unused (never published). r103, r104 (i13's
EARS check) survive; r105 is new (the general line). `retired:` gains r28, r30, r31, r32, r38, r39, r40, r41,
r44, r47, r50, r56, r57, r58, r60, r62, r63, r67 (r42, r45 were already retired).

The reports (violations, unresolved references, file problems) are the capability's purpose: they stay, as rows
of one table (id | code | what is reported), conditions with one code joined in a row.

| original id | now | note |
|---|---|---|
| r1 | r1 | "with the counts" moved to Implementation |
| r2 | r2 | now any violation, unresolved reference or file problem: print each, exit 1 |
| r3 | r3 | table row, v15a |
| r4 | r4 | table row, v15b |
| r5 | r5 | table row, v15c; takes r23's "adding a retired id is v15c" |
| r6 | r6 | table row, v15e |
| r7 | r7 | table row, v15f |
| r8 | r8 | table row, v_s3 |
| r9 | r9 | table row, unresolved; its "exits 1" is r2 |
| r10 | r10 | table row, v9a and v9c |
| r11 | r11 | unchanged meaning |
| r12 | r12 | now the case no interpreter has clingo (takes r57); exit 2 naming each tried and the install command |
| r13 | r13 | unchanged meaning |
| r14 | r14 | takes r38's "a decision with no id is left out" |
| r15 | r15 | unchanged meaning |
| r16 | r16 | takes r41's listing (adds, changes or removes, date order, status and date) and r40's "says no capability has it" |
| r17 | r17 | takes r41's exit 1 when none adds or changes it |
| r18 | r18 | unchanged meaning |
| r19 | r19 | unchanged meaning |
| r20 | r20 | 0052's rule (each `@r<n>` tag a requirement); takes r44 (`@deprecated` not read) |
| r21 | r21 | unchanged meaning |
| r22 | r22 | table row, unresolved; takes r67 (`#behaviour/r<n>`) |
| r23 | r23 | table row, unresolved; its v15c exception is in r5 |
| r24 | r24 | table row, unresolved; takes r47 (refused forms) |
| r25 | r25 | table row, file problem; takes r60 (`formulated_as`) |
| r26 | r26 | table row, file problem; takes r62 (`@holding`) |
| r27 | r27 | table row, file problem; takes r28 (work-item accepting an unnamed requirement) |
| r28 | retired → r27 | |
| r29 | r29 | table row, file problem; takes r63 (no `## Decision`) |
| r30 | retired → r2 | |
| r31 | retired → r2 | the counts summary moved to Implementation |
| r32 | retired → r2 | `--limit` moved to Implementation (an output format) |
| r33 | r33 | unchanged meaning |
| r34 | r34 | table row, v_k5 |
| r35 | r35 | table row, v_k6 |
| r36 | r36 | takes r58 (a `withdrawn` part closed) |
| r37 | r37 | unchanged meaning |
| r38 | retired → r14 | "prints the file it wrote" moved to Implementation |
| r39 | dropped: general line r105 | a minor refusal; exit 2 moved to Implementation |
| r40 | retired → r16 | |
| r41 | retired → r16, r17 | |
| r42 | (already retired) | |
| r43 | r43 | one reading line; a bare name elsewhere is not read as a node, hence unresolved (r24) |
| r44 | retired → r20 | |
| r45 | (already retired) | |
| r46 | r46 | table row, file problem |
| r47 | retired → r24 | |
| r48 | r48 | takes r50's avoided words; the facts it prints moved to Implementation |
| r49 | r49 | table row, file problem |
| r50 | retired → r48 | |
| r51 | r51 | written as what `model` reads as a mention; the `mentions` fact moved to Implementation |
| r52 | r52 | table row, v_t1 |
| r53 | r53 | table row, v_t2 |
| r54 | r54 | table row, v_t3 |
| r55 | r55 | takes r56 ("once") |
| r56 | retired → r55 | |
| r57 | retired → r12 | |
| r58 | retired → r36 | "`withdrawn` is a status of proposal and work-item" moved to Implementation |
| r59 | r59 | table row, v_d2 |
| r60 | retired → r25 | |
| r61 | r61 | table row, file problem |
| r62 | retired → r26 | naming the title moved to Implementation |
| r63 | retired → r29 | |
| r64 | r64 | takes "does not read its `by`" into one line |
| r65 | r65 | unchanged meaning |
| r66 | r66 | table row, unresolved; reading `term/<term>` as the term is implied |
| r67 | retired → r22 | |
| (new) | r103, r104 | table rows, v_e1 and v_e2 (i13's check); no scenario yet |
| (new) | r105 | the general line for `model` |

## Scenario tags

In features/design-model-check.feature, the scenarios whose tag is retired take the surviving line's tag instead
(no scenario removed, 0052):

- "a work-item accepting a requirement no scenario names is a file problem": @r28 → @r27
- "file problems are each printed and fail the check": @r30 → @r2
- "the check ends with the four counts": @r31 → @r2
- "rows of a violated relation are limited, saying how many more there are": @r32 → @r2
- "writing the decisions index names the file and leaves out decisions with no id": @r38 → @r14
- "why refuses an argument that is not a requirement reference": @r39 → @r105
- "why on a requirement no capability has still lists its proposals": @r40 → @r16
- "why lists every proposal naming the requirement by date, and fails when none adds or changes it": @r41 → @r16, @r17
- "a held scenario names no requirement": @r44 → @r20
- "a reference in a refused form is unresolved": @r47 → @r24
- "facts give each term its kind, its context and its avoided words": @r50 → @r48
- "the check runs again only once": @r56 → @r55
- "with no interpreter that has clingo the check names each one it tried": @r57 → @r12
- "a withdrawn part is closed": @r58 → @r36

No other scenario changes. r60 to r67 had no scenario; r64, r66, r103, r104 still have none.

Seen, outside this brief: scenarios still tagged @r42 and @r45 (retired before this round), and scenarios that show
`@holding` (r26 example, r44) and `formulated_as` (r20, r26) as accepted where r26 and r25 now refuse them.

## Questions

1. The reports table: rows carry ids and count as lines (0051), introduced by one un-numbered sentence, and
   Behaviour has `###` sub-headings. Does `model check` (v15a, v_e1, v_e2) read table rows and skip the
   sentence and headings? Choice: drafted so; the check must learn the table before this file is published.
2. "Withdrawn as a status" (r58's first half) and r39's exit 2 moved to Implementation. Choice: kept, as lifecycle
   detail and a minor refusal.
~~~~~~

## `.shop/scratch/ears/map/feature-file-tools.md`

~~~~~~
# feature-file-tools: original ids to compacted EARS lines (round 2)

Lines: original 45 → round 1 64 → now 25. Highest id ever published: r59. Round-1 ids r60–r78 are unused
(never published); no new id. `retired:` gains r3, r6, r10, r11, r15, r18, r20, r22, r27, r36, r37, r38, r39,
r40, r41, r42, r53, r54, r55, r59.

`If` lines kept: the checks' findings (`verify-moved`, `bindings`, the purpose), and refusals that keep an edit
from damaging the wrong scenario, a file `features` cannot read, a scenario not deprecated, or test modules
(r2, r35, r24, r29). Every other refusal is under the general line r46.

| original id | now | note |
|---|---|---|
| r1 | r1 | unchanged meaning |
| r2 | r2 | takes r3 (an edit that would leave a `Rule:` block); the response is r3's, every file left as it was |
| r3 | retired → r2 | "checks nothing else of the result" moved to Implementation |
| r4 | r4 | unchanged meaning, the two sentences in one |
| r5 | r5 | takes r6 (`--title`); r38's leading `@` moved to Implementation |
| r6 | retired → r5 | |
| r7 | r7 | If → When: no match is a result, not a fault |
| r10 | retired → r35 | |
| r11 | dropped: general line r46 | exit 2 as bad usage in Implementation |
| r12 | r12 | unchanged meaning |
| r13 | r13 | unchanged meaning |
| r14 | r14 | unchanged meaning |
| r15 | dropped: general line r46 | a minor refusal, listed in Implementation |
| r16 | r16 | unchanged meaning |
| r17 | r17 | takes r18 (duplicate) and r37 (missing or added) |
| r18 | retired → r17 | |
| r19 | r19 | unchanged meaning |
| r20 | dropped: general line r46 | a minor refusal, listed in Implementation |
| r21 | r21 | takes r40 (flagged on its line); r22's empty list wording in Implementation |
| r22 | retired → r21 | |
| r23 | r23 | unchanged meaning |
| r24 | r24 | kept: `retire` removes a block |
| r25 | r25 | unchanged meaning |
| r26 | r26 | unchanged meaning |
| r27 | dropped: general line r46 | a minor refusal, listed in Implementation |
| r28 | r28 | the printed count moved to Implementation |
| r29 | r29 | takes r41 (several feature files) and r42 (title over several lines) |
| r35 | r35 | takes r10 (`tag`), r53, r54, r55 (`--file`) |
| r36 | dropped: general line r46 | a minor refusal, listed in Implementation |
| r37 | retired → r17 | |
| r38 | retired → r5 | |
| r39 | retired → r19 | the printed file and title moved to Implementation |
| r40 | retired → r21 | |
| r41 | retired → r29 | |
| r42 | retired → r29 | naming the module and line moved to Implementation |
| r46 | r46 | now the general line ("exit non-zero, say why on stderr, change nothing") |
| r51 | r51 | 0052's rule: adds `@r<n>`, keeps other `@r<m>` tags (as round 1) |
| r52 | r52 | unchanged meaning |
| r53 | retired → r35 | |
| r54 | retired → r35 | |
| r55 | retired → r35 | |
| r56 | r56 | "without `--file` every binding" moved to Implementation (r28 says it) |
| r57 | r57 | unchanged meaning |
| r58 | r58 | takes r59 (bound more than once) |
| r59 | retired → r58 | |

## Scenario tags

In features/feature-file-tools.feature (titles as they stand, still saying "hold"/"held"), the scenarios whose
tag is retired or dropped take the surviving line's tag instead (none removed, 0052):

- "an edit is refused only when it would leave a Rule: block outside a docstring": @r3 → @r2
- "listing by title finds every scenario whose title contains the text": @r6 → @r5
- "retagging a title that is not in exactly one file is refused": @r10 → @r35
- "retagging with a tag that is neither a slice nor a requirement tag is bad usage": @r11 → @r46
- "moving to a destination that does not exist is refused": @r15 → @r46
- "a title held twice in either tree is a duplicate": @r18 → @r17
- "holding a scenario already held is refused": @r20 → @r46
- "the holding list says when nothing is held": @r22 → @r21
- "a test module that does not parse is refused": @r27 → @r46
- "moving a scenario to its own file is refused": @r36 → @r46
- "a title in only one tree is missing or added": @r37 → @r17
- "a tag is found with or without its leading @": @r38 → @r5
- "holding a scenario prints its file and new title": @r39 → @r19
- "the holding list flags a held scenario it cannot place": @r40 → @r21
- "rebinding to a title several feature files hold is refused": @r41 → @r29
- "rebinding a title written over several lines is refused": @r42 → @r29
- "--file naming a file that does not hold the title is refused": @r53 → @r35
- "--file naming a file that holds the title twice is refused": @r54 → @r35
- "--file naming a file outside --dir is refused": @r55 → @r35

r57 and r58 still have no scenario. Scenarios tagged with ids retired before this round (r8, r9, r30–r34, r43–r45,
r47–r50) are as they were.

**Deprecated, replaced at formulation** (from round 1, still open): "tagging with a requirement id makes it the
scenario's one requirement tag" (@r51) contradicts r51 under 0052; it is to be deprecated for a new r51 scenario
in which the other `@r<m>` tags are kept.

## Questions

1. r7 is When, not If (a list that matches nothing is a result scripts read). Choice: kept as a line, not moved to
   Implementation, since its exit 1 is what callers test.
2. r15, r36 (move to a missing destination or to its own file) went to the general line: neither loses a
   scenario. Choice: as written; say if either was a seen failure.
~~~~~~

## `.shop/scratch/ears/map/formulation.md`

~~~~~~
# formulation: original ids, round 2

Lines: 14 original → 21 round 1 → 13 now. Highest id ever used: r22 (r15–r21 from round 1 were never published
and are unused; r22 is new, the general line). `retired:` gains r8, r12.

| original id | now | note |
|---|---|---|
| r1 | r1 | "every scenario that is not deprecated formulates a line" left to r13, where `model check` shows it (r15 unused) |
| r2 | r2 | unchanged meaning |
| r3 | r3 | the question and the rest formulated in one response (r16 unused). Kept: the capability's purpose |
| r4 | r4 | joined with r12 (the deprecated scenario keeps its `@r<n>` tags); the deprecation's marks (tag, title suffix, `Deprecated for:`) moved to Implementation |
| r5 | r5 | unchanged meaning |
| r6 | r6 | one response, the commit, with what `features bindings` reports as its state (r17 unused); protects the person's files |
| r7 | r7 | unchanged meaning; seen: a formulator in the kb run dropped a scenario (records/measurements/fixture-runs/2026-09-30-migrating-to-capabilities-test-log.md) |
| r8 | retired: output format, to "Implementation, may change" | the feature file's first three lines |
| r9 | r9 | unchanged meaning |
| r10 | r10 | unchanged meaning |
| r11 | r11 | as round 1: decision 0052's rule, several `@r<n>` tags, all of one capability |
| r12 | retired → r4 | "formulates no line" is `model check`'s reading of a deprecated scenario (r13, design-model-check), r18 unused |
| r13 | r13 | the two reports joined (r19 unused); the fallback where `model check` cannot run moved to Implementation (r20, r21 unused) |
| r14 | r14 | unchanged meaning |
| — | r22 | new: the general line for the skill (decision 0051) |

## Scenario tags

No `features/formulation.feature` exists (the capability has no `formulated_as`); no scenario changes. No scenario
is written for r8 or r12.

## Questions

1. r3: "formulating the rest of the capability" is written as the manner of the one response. Choice: as written.
~~~~~~

## `.shop/scratch/ears/map/red-green.md`

~~~~~~
# red-green: original ids, round 2

Lines: 19 original → 38 round 1 → 14 now. Highest id ever used: r38 (round 1; r20–r38 were never published).
Round-1 ids kept: r37. Unused: r20–r36, r38.

| original id | now | note |
|---|---|---|
| r1 | r1 | the two passing conditions are one response again (r20 unused) |
| r2 | r2 | joined with r19: one "shall not commit a change to" for both kinds of file |
| r3 | r3 | every hand-back condition in one line (same response): r3's three, r4's two, r12's. Kept: the capability's purpose (stops when a scenario cannot be satisfied honestly); an early pass was seen suite-wide (records/archive/design-notes/2026-10-11-green-suite-design.md) |
| r4 | retired → r3 | |
| r5 | r5 | every `BLOCKED` stop with the same response joined: r5's, r13's, r14's; "naming the test" widened to the test, step, decision or file. Kept: four hand-backs for an unlisted test in kb batches 33–35, and slice 156 removing tests to stay green (records/archive/design-notes/2026-10-11-rules-adjusted-design.md, 2026-10-10-small-slices-and-steps-design.md) |
| r6 | r6 | the two triggers joined (r24 unused) |
| r7 | r7 | the commit of the work so far is the result's state, not a second response (r25 unused); "which scenarios are green and red" moved to Implementation |
| r8 | retired: output format, to "Implementation, may change" | the report's contents and the commits in the result |
| r9 | r9 | one response, the `PARTIAL` stop, with the files named before the first edit as its state; "a new implementer can continue" is the continuation in Implementation (r27–r29 unused). Kept: slice 156 of kb touched 72 files in one dispatch (2026-10-10-small-slices-and-steps-design.md) |
| r10 | r10 | one response (r30 unused) |
| r11 | r11 | "says so in the report" moved to Implementation (r31 unused) |
| r12 | retired → r3 | |
| r13 | retired → r5 | |
| r14 | retired → r5 | |
| r15 | r15 | now the general line for the implementer; its three cases (no scripts directory, no result file, `bdd-red-green` missing) moved to Implementation as the cases seen (r33, r34 unused) |
| r16 | r16 | the summary under fifteen lines moved to Implementation (r35 unused) |
| r17 | r17, r37 | the claim is event-driven (r17); its refusal keeps round 1's r37: it protects another work-item's claimed files. "Commits what is green" is the stop's state, "at a green commit" (r36 unused) |
| r18 | r18 | one response (r38 unused) |
| r19 | retired → r2 | |

## Scenario tags

`features/red-green.feature` does not exist yet; no scenario changes. When it is formulated, a scenario for a
retired id is not written: the lines r3, r5 and r2 cover r4, r12; r13, r14; r19.

## Questions

1. r3 and r5 each join many conditions into one line, as the rule for one response asks. Choice: as written; the
   alternative is a table of stop conditions (condition | result), which decision 0051 allows only for a check.
2. r7, r9, r37: a state the response leaves ("the work so far committed", "at a green commit") is written in the
   response rather than as a second "shall". Choice: as written.
~~~~~~

## `.shop/scratch/ears/map/review.md`

~~~~~~
# review: original ids, round 2

Lines: 14 original → 27 round 1 → 15 now (six of them rows of one table). Highest id ever used: r28 (r15–r27 from
round 1 were never published and are unused; r28 is new, the general line).

| original id | now | note |
|---|---|---|
| r1 | r1 | one response, the state the review leaves (r15 unused) |
| r2 | r2 | the grade only; a finding's file and line, what, why and fix moved to Implementation (r16 unused) |
| r3 | r3 | table row; "list it" and "Important if unlisted" one response (r17 unused) |
| r4 | r4 | table row; both allowances in one row (r18 unused) |
| r5 | r5 | table row |
| r6 | r6 | table row; the branch and task halves in one row (r19 unused) |
| r7 | r7 | one "report" of the three (r20, r21 unused) |
| r8 | r8 | unchanged meaning |
| r9 | r9 | unchanged meaning |
| r10 | r10 | table row |
| r11 | r11 | table row, branch review only |
| r12 | r12 | the triage and its three cases in one line again (r22–r25 unused) |
| r13 | r13 | both kinds of review in one line (r26 unused) |
| r14 | r14 | "names the work-item it would unblock" as the response's manner (r27 unused) |
| — | r28 | new: the general line for a reviewer (decision 0051) |

The table's rows are the review's purpose, a check that reports problems; r10 also protects the feature files.

## Scenario tags

`features/review.feature` does not exist yet; no scenario changes. When it is formulated, each table row is a
requirement like any line.

## Questions

1. The table's lead sentence carries no id; only its rows are requirements. Choice: as written.
~~~~~~

## `.shop/scratch/ears/map/role-boundaries.md`

~~~~~~
# role-boundaries: original ids, round 2

Lines: 6 original → 12 round 1 → 6 now. Highest id ever used: r12 (r7–r12 from round 1 were never published and
are unused). `retired:` unchanged. Every line is ubiquitous, a guarantee the agent definitions hold; none is a
failure, so there is no general line (nothing here runs).

| original id | now | note |
|---|---|---|
| r1 | r1 | unchanged meaning |
| r2 | r2 | unchanged meaning |
| r3 | r3 | unchanged meaning |
| r4 | r4 | the implementer's skill set in one response (r7, r8 unused); "so the listing of every installed skill never enters its context" is the consequence, moved to Implementation (r9 unused) |
| r5 | r5 | the models in one response (r10–r12 unused) |
| r6 | r6 | unchanged meaning |

## Scenario tags

`features/role-boundaries.feature` does not exist yet; no scenario changes.

## Questions

None open.
~~~~~~

## `.shop/scratch/ears/map/spec-consistency.md`

~~~~~~
# spec-consistency: original ids, round 2

Lines: 11 original → 20 round 1 → 12 now. Highest id ever used: r21 (r12–r20 from round 1 were never published
and are unused; r21 is new, the general line). `retired:` unchanged.

| original id | now | note |
|---|---|---|
| r1 | r1 | run and report in one response (r12 unused) |
| r2 | r2 | unchanged meaning |
| r3 | r3 | the blind reading only; writing the findings file and the short reply moved to Implementation (r13, r14 unused) |
| r4 | r4 | one response, the state report mode leaves (r15 unused); the findings file's grouping moved to Implementation |
| r5 | r5 | proposal and its gate pass in one response (r16 unused) |
| r6 | r6 | unchanged meaning |
| r7 | r7 | the question and its integration in one response (r17 unused) |
| r8 | r8 | unchanged meaning |
| r9 | r9 | "runs `model check` and reports" as one report of what it finds (r18 unused) |
| r10 | r10 | one response, fix mode ending in that state (r19 unused) |
| r11 | r11 | one ubiquitous line: only on demand, never in a round (r20 unused) |
| — | r21 | new: the general line for the skill (decision 0051) |

## Scenario tags

`features/spec-consistency.feature` does not exist yet; no scenario changes.

## Questions

1. r4: "report mode" is not defined elsewhere in the lines; read as an option (Where), the counterpart of fix
   mode. Choice: as written (open since round 1).
~~~~~~

## `.shop/scratch/ears/map/spec-integration.md`

~~~~~~
# spec-integration: original ids, round 2

Lines: 22 original → 32 round 1 → 20 now. Highest id ever used: r33 (r23–r32 from round 1 were never published
and are unused; r33 is new, the general line). `retired:` gains r5, r9, r18.

| original id | now | note |
|---|---|---|
| r1 | r1 | lines and questions in one "show" (r23 unused) |
| r2 | r2 | When again, not If: drafting a line no sentence backs is the writer's draft, not a fault of the skill; "Where the change comes from a note" is in the trigger |
| r3 | r3 | unchanged meaning; protects `spec/` |
| r4 | r4 | one response, the changed lines shown again (r24 unused) |
| r5 | retired → r6 | a rejected line is not approved, and r6 writes the lines exactly as approved |
| r6 | r6 | apply and commit alone, one response; the commit message's contents moved to r15 (r25 unused) |
| r7 | r7 | When again, not If: integrating into the one spec is the normal path |
| r8 | r8 | "still stops at the gate" is r3 (r26 unused) |
| r9 | retired → r15 | the delegation named in the commit message (r15) and in the decision's `by` (r21); r27 unused |
| r10 | r10 | unchanged meaning |
| r11 | r11 | unchanged meaning |
| r12 | r12 | unchanged meaning; "no later line takes it" (r28 unused) is r12's "one above every id … retired" |
| r13 | r13 | unchanged meaning |
| r14 | r14 | as r12 says |
| r15 | r15 | joined with r9's commit half and r18: one line for what the commit message names |
| r16 | r16 | as round 1: protects `spec/` from a commit that breaks the model. "formulation clears all three" (r29 unused) is formulation's work, not this capability's |
| r17 | r17 | unchanged meaning |
| r18 | retired → r15 | |
| r19 | r19 | one response, the gate (r30 unused) |
| r20 | r20 | the decision's sections moved to Implementation (r31 unused), as decision 0046 states them |
| r21 | r21 | `source` and `by` in one line again (r32 unused) |
| r22 | r22 | unchanged meaning |
| — | r33 | new: the general line for the skill (decision 0051) |

## Scenario tags

No `features/spec-integration.feature` exists (the capability has no `formulated_as`); no scenario changes. No
scenario is written for r5, r9 or r18.

## Questions

None open.
~~~~~~

## `.shop/scratch/ears/map/spec-migration.md`

~~~~~~
# spec-migration: original ids, round 2

Lines: 23 original → 40 round 1 → 21 now. Highest id ever used: r40 (round 1; r24–r40 were never published).
Round-1 ids kept: r26. Unused: r24, r25, r27–r40. `retired:` gains r3, r12, r13.

| original id | now | note |
|---|---|---|
| r1 | r1 | the three conditions joined again (r24, r25 unused) and made the skill's general line ("cannot otherwise do what it was asked"); protects the person's uncommitted work |
| r2 | r2, r26 | what the gate shows of the spec, with r3's and r12's questions (r2); nothing beyond the mechanical move changed before the answers, joined with r16's half (r26, round 1's id) |
| r3 | retired → r2 | the retitle is asked at the gate. Seen: the cart fixture's two "An empty cart" scenarios (records/measurements/fixture-runs/2026-09-30-migrating-to-capabilities-test-log.md) |
| r4 | r4 | one response, each scenario put in its file as it was (r27 unused) |
| r5 | r5 | joined with r13, which sets aside more and covers migration to ids too |
| r6 | r6 | unchanged meaning; protects the suite from silent damage |
| r7 | r7 | unchanged meaning |
| r8 | r8 | unchanged meaning |
| r9 | r9 | one "give" (r28, r29 unused) |
| r10 | r10 | the context path from `spec/index.md` or the person in one line (r30 unused) |
| r11 | r11 | as round 1: decision 0052's rule, the tag of each line the scenario formulates |
| r12 | retired → r2 | a scenario that formulates no line is a question at the gate; "tags nothing before the answer" is r26 (r31 unused) |
| r13 | retired → r5 | |
| r14 | r14 | one "rewrite" (r32, r33 unused) |
| r15 | r15 | unchanged meaning |
| r16 | r16, r26 | what the gate shows of the work and the glossary (r16); its "nothing committed before the answers" joined into r26 (r34 unused) |
| r17 | r17 | the living plan's conversion in one response (r35–r37 unused) |
| r18 | r18 | "still bound by its test" as the response's state (r38 unused) |
| r19 | r19 | the `source` as the response's state (r39 unused) |
| r20 | r20 | unchanged meaning |
| r21 | r21 | unchanged meaning |
| r22 | r22 | "the tags, work-items and observations … are the next [commit]" moved to Implementation (r40 unused) |
| r23 | r23 | unchanged meaning; protects the person's files from a silent path rewrite |

## Scenario tags

No `features/spec-migration.feature` exists yet; no scenario changes. No scenario is written for r3, r12 or r13.

## Questions

1. r1 as the general line keeps "before any change": a failure found after the mechanical move cannot stop before
   it. Choice: as written, since r26 and r6 cover what follows the move; the alternative is a separate general
   line "stop, saying why, and change nothing further".
2. r26 "change nothing beyond the mechanical move" replaces r2's "nothing under `spec/` changes before their yes"
   and r16's "nothing after the mechanical move is committed": nothing written, not only nothing committed.
   Choice: as written.
~~~~~~
