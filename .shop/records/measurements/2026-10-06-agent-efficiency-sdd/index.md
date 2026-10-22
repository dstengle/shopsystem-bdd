---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-06-agent-efficiency-sdd
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-06
---

# Agent efficiency (0.10.0): subagent-driven run ledger

The controller's ledger of the subagent-driven run that built the 2026-10-06 agent-efficiency plan (release 0.10.0: scripts/features and scripts/plan, suite records, probes at the pin, spec agents drafting to files), on branch agent-efficiency from 41ccb37 to 34279e8, finished 2026-10-07. It holds the preflight scan, every ruling, each task's dispatch, review rounds and deferred minors, and the final review. The plan is .shop/records/archive/plans/2026-10-06-agent-efficiency.md; its Global Constraints were copied to the run's global-constraints.md, identical but for the SCRATCH line, which this ledger also carries, so that file is not kept. One record per task (its report; the task brief is the plan's own section) and the final fix wave's report sit beside this index.

Archived from `.superpowers/sdd/2026-10-06-agent-efficiency/progress.md` (git-ignored scratch), text as it was.

---

# SDD ledger — plan: docs/superpowers/plans/2026-10-06-agent-efficiency.md

Branch: agent-efficiency (created in place from main 41ccb37; not a worktree, because the plan's headless runs and script paths hardcode /home/vscode/shopsystem-bdd as --plugin-dir).
SCRATCH: /tmp/claude-1000/-home-vscode-shopsystem-bdd/fc94dcb8-3a7e-4e90-920d-bc0abed97f22/scratchpad
Spec: docs/superpowers/specs/2026-10-06-agent-efficiency-design.md (read).

## Preflight scan
| Rows | Produces / consumes | Found |
|---|---|---|
| T1 self | 15 tests vs contract; count expectation (cart 5, slice-2 3, slow 1, wip 3, total 5) checked by hand against CART | agrees |
| T2 self | 18 tests vs contract; archive / backlog / add-slice expectations checked by hand | agrees |
| T1→T3/T4/T5 | features count/list/tag/move/verify-moved consumed by slicing (T4), migrating (T5) | agrees |
| T2→T3/T4 | plan show --last-suite [--current], log, add-slice, status, archive consumed by red-green, implementer, slicing | agrees |
| T3→T4 | suite record convention cited by slicing step 1 | agrees |
| T3 self | edits bdd-red-green + 3 agents; fixtures impl/review | agrees |
| T4 self | slicing edits; hand-off phrase "(`pytest --collect-only -q -m slice-N`)" exists at slicing SKILL.md:66 | agrees |
| T5 self | spec agents + 3 skills; migrating baseline line exists at migrating SKILL.md:17 | agrees |
| T3,T4,T5→T6 | T6 grep expects removed phrases (implementer.md:21, slicing:66, capability-writer:10, feature-formulator:14) | agrees, each phrase removed by T3/T4/T5 |
| T2 Step 5 vs T6 Step 3 | T2 may add tests for real plan shapes; T6 expects exactly 33 | conflict (conditional) |
| Spec vs plan | spec lists formulating-features as a user of `features`; plan's T5 gives formulating-features no `features` use | gap |
| Spec vs T3 | spec: controller names last record in dispatch; plan: implementer reads plan show --last-suite | compatible |

Ruling: T6's "33 tests" means "every test OK, 33 plus any T2 Step 5 added" — the plan's own Step 5 mandates adding a test for each real shape — costs if wrong: none beyond a count.
Ruling: formulating-features gets no `features` script use in this batch (plan's task list governs; no baseline evidence for it) — costs if wrong: one skill misses a script reference the spec lists; a later small change.
Ruling: implementers are general-purpose agents (this plugin's bdd-* agents serve consuming repos, not the plugin's own skill/script work) — costs if wrong: none.

## Progress
Task 1: dispatched (base 41ccb37, implementer sonnet, agent a447df95c7c127de1)
Task 1: minor (deferred): CRLF/encoding not preserved (text mode, no newline="") — scripts/features:183-185,234-235
Task 1: minor (deferred): --inline-background flattens Background docstring indentation; Background description inserted as a step — :136-139,172-174
Task 1: minor (deferred): missing --dir/--from is silent (total 0 / all "added") — :177-188
Task 1: minor (deferred): malformed slice returns 1 not 2 when repo has a Rule: file (validation after load) — :239-241
Task 1: minor (deferred): tag appended after a trailing "# comment" on the last tag line is lost — :265
Task 1: minor (deferred): built in one pass, not test by test; Rule: refusal, move-refusal branches, write_checked refusal untested; move refusals go beyond the contract
Task 1: minor (deferred): move writes source then destination, no rollback — :293-298
Task 1: complete (commits 41ccb37..8382992, review clean)
Task 2: dispatched (base 8382992, implementer sonnet, agent ad587dbcdb5d5118d)
Task 2: review 1 (8382992..4ee1350): spec ❌ (--help missing 2 contract bullets; --current without --last-suite ignored), Important: archive drops continuation lines of log entries. Fix round 1 sent to implementer.
Task 2: minor (deferred): add-slice "" for --check/--scenarios writes "None"; non-numeric n tracebacks (exit 1 not 2); "02" vs "2" duplicates — scripts/plan:228,232
Task 2: minor (deferred): malformed "## Slice 3 - foo" heading treated as unknown section, passes check
Task 2: minor (deferred): log text with embedded newline writes extra lines
Task 2: minor (deferred): staleness ignores git diff failure; git missing uncaught; porcelain quoted paths; show --last-suite with no record exits 0 silently
Task 2: minor (deferred): archive writes archive file before plan; failed second write blocks retry
Task 2: minor (deferred): unknown-section test asserts no success and covers only status/log; no tests for show --backlog, archive without Suite, duplicate-number/slice-after-section checks
Ruling: tests added in fix rounds also extend Task 6's "33 tests" count — the fix needs test-first evidence — costs if wrong: none beyond a count.
Task 2: fix round 1/5 (3 addressed, 0 open; commits 4ee1350..db66c75)
Task 2: minor (deferred): bullets() drops an indented line after a blank line, and a non-bullet line before the first bullet
Task 2: minor (deferred): real shopsystem-knowledge plan's suite record lacks "at <hash>", so --current says stale until a template-format record is logged
Task 2: complete (commits 8382992..db66c75, review clean after round 1)
Task 3: dispatched (base db66c75, implementer opus)
Task 3: implementer DONE_WITH_CONCERNS fff6163 (impl, impl-norecord, review green). Concern noted for final review: `plan show --last-suite` with no record exits 0 silently (Task 2 minor) — implementer compensated with a sentence in bdd-implementer.md; headless controller re-ran the suite after the implementer (not governed by Task 3).
Task 3: review 1 (db66c75..fff6163): spec ✅; Important: (1) where the suite record goes in the log is ambiguous — agents folded it into the checkpoint entry 2/2; (2) plan-mandated: Red Flags footer "stop, undo the edit, hand back" applies to the new start-of-slice-run flag.
Ruling: Red Flags footer gets an exception for the suite-run flag (skip the run and continue) — spec §4 is about fewer round trips and binds over the plan's placement — costs if wrong: one sentence of wording.
Task 3: minor (deferred): stale record at slice start not covered (implementer reads --last-suite without --current) — spec §2 says run again
Task 3: minor (deferred): fix round does not refresh the suite record (bdd-implementer.md fix-round bullet)
Task 3: minor (deferred): "holds" in bdd-red-green omits the working tree (SKILL.md:44)
Task 3: minor (deferred): branch-reviewer names `plan show` bare, not `python3 <Scripts>/plan`
Task 3: minor (deferred): "is Important" reads as fixed grade; "at least Important" clearer (task-reviewer, branch-reviewer)
Note: user went offline 'continue through to completion' — finish on branch, no merge/push (outward actions held for the user).
Task 3: fix round 1/5 (2 addressed, 0 open; commits fff6163..d07a1a5)
Task 3: minor (deferred): implementer set slice Status with sed instead of `plan status` in a green run (bdd-implementer names only `plan log`)
Task 3: minor (deferred): branch-reviewer edits have no green run (brief prescribes none)
Task 3: complete (commits db66c75..d07a1a5, review clean after round 1)
Task 4: dispatched (base d07a1a5, implementer opus)
Task 4: implementer DONE 840aedf (green iteration 1, all criteria)
Task 4: review 1 (d07a1a5..840aedf): spec ✅; Important (plan-mandated): (1) fast-suite trigger's "or" lets the subprocess arm fire without the 60 s bound; (2) hand-off still lets writing-plans run the suite.
Ruling: fix both to the spec (§1: over 60 s AND failing either property; §2: a record that holds is used, not re-run) — spec binds over the plan's wording — costs if wrong: two clauses.
Ruling: no headless re-run for these two clause edits; the green run already behaved as the corrected wording says — costs if wrong: the corrected clauses are untested by a run.
Task 4: minor (deferred): scripts named bare after the Overview; full python3 form only once (SKILL.md:12)
Task 4: minor (deferred): "Check: the suite -> …" uses "the suite" as placeholder for a command (SKILL.md:39)
Task 4: minor (deferred): one green run, variance unmeasured; plan archive and second fast-suite arm not exercised
Task 4: fix round 1/5 (2 addressed, 0 open; commits 840aedf..34010f5)
Task 4: minor (deferred): fast-suite clause grouping of "and CLAUDE.md gives no reason" could be read as attaching to one arm only (SKILL.md:49)
Task 4: complete (commits d07a1a5..34010f5, review clean after round 1)
Task 5: dispatched (base 34010f5, implementer opus)
Task 5: implementer DONE_WITH_CONCERNS e6ec51f (spec, spec-form, legacy green). README.md:77 'read-only' capability-writer → carry into Task 6.
Task 5: review 1 (34010f5..e6ec51f): spec ✅; Important: a question round's drafts on the same drafts path overwrite the first round's (approved lines lost); no rule for rounds.
Ruling: fix by giving each round its own subdirectory under the drafts path, applied in order — smallest change, keeps the writer's read limits — costs if wrong: the controller applies a stale earlier round section over a later one.
Ruling: no headless re-run for the round-subdirectory fix (the question round is untested by any run already; a run costs ~15 min and the user flagged duration) — costs if wrong: the fix is unexercised until a real integration with questions.
Task 5: minor (deferred): migrating-to-capabilities names `features …` without the python3 <base>/../../scripts/ form (:17,:25,:29)
Task 5: minor (deferred): capability-writer "nothing else" vs migration mapping table (:55 vs ~:64)
Task 5: minor (deferred): no draft rule for frontmatter changes or a changed index.md (capability-writer:49; integrating step 4)
Task 5: minor (deferred): .gitignore/drafts-path sentence comes after "Dispatch" in integrating :16 and formulating :16
Task 5: minor (deferred): porcelain check assumes a clean tree before dispatch; integrating has no clean-tree precondition
Task 5: minor (deferred): "structural" overstates what tools enforce (formulating :99, integrating :63)
Task 5: minor (deferred): ledger instruction repeated (capability-writer:51)
Task 5: minor (deferred): Question Brief, Hand-back Brief and Review Focus 5's send-back path never exercised by a run
Task 5: fix round 1/5 (1 addressed, 0 open; commits e6ec51f..28bb4d2)
Task 5: minor (deferred): Migration Brief hardcoded to round-1/, no earlier-rounds read for a migration re-dispatch
Task 5: minor (deferred): "a line the person rejects is dropped from the drafts" doesn't say which round (integrating step 3)
Task 5: complete (commits 34010f5..28bb4d2, review clean after round 1)
Task 6: dispatched (base 28bb4d2, implementer sonnet)
Task 6: minor (deferred): README "What the tools make structural" doesn't mention spec agents' Write (README.md:101)
Task 6: complete (commits 28bb4d2..72d33af, review clean)
Final review (41ccb37..72d33af): With fixes. Important: (1) archive hides the record it keeps from --last-suite; (2) plan-mandated: archive moves RE-FORMULATE/QUESTION FOR THE SPEC entries out; (3) features move drops source feature tags so migration stops; (4) Scripts: doesn't reach implementer via SDD task-brief; implementer reads a failure as "no record"; (5) spec §2 fix-wave whole run missing. Fix-before-merge minors: fix round refreshes record (=5); Status via `plan status` in Checkpoint; porcelain noted before dispatch.
Ruling: archive keeps RE-FORMULATE and QUESTION FOR THE SPEC entries in the living log beside REQUEST — spec: the script keeps the plan valid, and slicing step 7 / formulating's hand-back read those entries from the living plan — costs if wrong: a few extra lines kept in the living log.
Ruling: final reviewer says the formulating-features ruling put plan over spec, inconsistent with later rulings; outcome stands as backlog (no baseline evidence for the edit), reasoning corrected — costs if wrong: formulating-features lacks verify-moved for its byte-for-byte check until a later change.
Ruling: final fix wave is tested by unittest only; no headless re-runs for its prose — costs if wrong: prose fixes unexercised until the next real batch.
Final fix wave: dispatched (base 72d33af, opus)
Final fix wave: re-review clean (72d33af..34279e8), 7 addressed, 0 open.
Final: minor (backlog): plan reader at scripts/plan:311 lists only REQUEST entries; open RE-FORMULATE/QUESTION entries not shown
Final: minor (backlog): --carry-feature-tags doesn't detect a destination with a differing feature tag set
