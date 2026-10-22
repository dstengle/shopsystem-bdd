---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-i13-ears-skeleton-notes
kind: initiative-archive
about: [capability/missingmass.io/shopsystem/shopsystem-bdd/supervision, capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue, capability/missingmass.io/shopsystem/shopsystem-bdd/delivery, capability/missingmass.io/shopsystem/shopsystem-bdd/planning, capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools]
date: 2026-10-19
---

# 0.21.0 EARS restructure (i13): skeleton notes, lines cut from round 1

Written under brief-skeleton.md when supervision, work-queue, delivery and planning (i10) and migration-tools (i8) were cut to walking skeletons (decision 0051): the round-1 lines left out, as ideas to test once each skeleton runs, and which drafted work-items of i10 and i8 the skeletons still need, defer or drop.

Archived from `.shop/scratch/ears/skeleton-notes.md` (git-ignored scratch), text as it was.

---

# Skeleton notes: what the round-1 drafts said that the skeletons leave out

Decision 0051: a capability not yet built is a walking skeleton. These are the round-1 lines cut from
supervision, work-queue, delivery, planning (i10) and migration-tools (i8), as ideas to test once the skeleton
runs: notes for the initiatives, not requirements. Round-1 ids (in .shop/scratch/ears/round1/ and
spec/capabilities/ on the branch) are in brackets; none was ever published.

## Supervision

Kept in the skeleton: the stage-by-stage pull (r1, r36-r38), a fresh `claude -p` per stage with one brief
(r2), outcome only from the result file (r3, r42, r43), merge only when the tests pass (r10, r53-r55), worker
changes under `.shop/work/` put back (r5), one commit per move (r29), session ids logged (r27), exit with the
statuses and questions (r17).

Ideas to test once the skeleton runs:
- A failed stage gets one more fresh worker before it becomes a question (r4, r44).
- A worker that touches `.shop/work/` also fails its stage and is logged by file (r45, r46).
- A researcher's `DONE` with an empty file set fails the stage; the file set and notes' path go into the work-item (r6, r47, r48).
- The planner's plan path, final file set and dependencies go into the work-item; a `QUESTION` goes through `planned` to `awaiting-ruling` (r7, r49, r50).
- The queue's guard decides when `planned` becomes `ready`; claiming happens when an implementer's place is free (r8, r51).
- Several implementers at once, as many as `delivery.toml` allows, 2 by default (r52).
- Commits outside the file set, rebase conflicts and failing tests each stop the merge with their own question (r11, r12, r57).
- `PARTIAL` continues on the same worktree up to three times, then a question (r13, r58).
- `BLOCKED`, `HAND-BACK` and `NEEDS_CONTEXT` keep the worktree and branch and release the claim (r14, r59).
- A refused `work claim` sends the work-item back to `ready`, waiting for the other claim, then continuing its branch (r15, r60, r61).
- Work-items not blocked by an `awaiting-ruling` one go on (r16).
- Separate exit codes for green, a question, a budget and anything else (r18, r63-r65).
- Time and spending limits per role, ending the worker and failing its stage (r19, r66-r68).
- A run budget: no new worker, wait for the running ones, say what was spent (r20, r69, r70).
- Task review only for risk `contract`, `concurrency` or `data`; green once accepted scenarios pass at the branch head (r21, r39, r71).
- Fix-now findings become fix work-items with `fixes:` and `findings:`, holding the original back from green (r22, r72).
- Every review's findings as a review-finding record; observations appended to `observations.md` (r23, r24, r73).
- A branch review from the initiative's base when all are done, turning done items green (r25, r40, r74).
- Scoped re-review of a fix: severe findings get another fix, the rest observations (r26, r75-r77).
- A worker's end logged with result, exit, duration, cost and tokens; suite records logged and given to the implementer (r28, r78, r79).
- Refuse a second `work run`, the default branch, a dirty working tree (r30, r31, r80).
- Interruption ends and logs the workers; the next run continues each claimed work-item (r32, r81, r82).
- Say the initiative's work-items are done without touching the initiative's status (r33).
- `work step <work-item>` runs one stage alone (r34, r83).
- One printed line per worker start and end, nothing a worker wrote (r35, r84, r85).

## Work queue

Kept: `work add` (r2, partly), refusing to overwrite (r4), `work show` (r5, partly), the move writing the status
(r7) and the log line (r32), refusing a status the log does not agree with (r8).

Ideas to test once the skeleton runs:
- `work` reads every work-item by `kind` and every scenario under `features/`; standard library only (r1, r25: kept as implementation).
- `work add` with `--check`, the Observable, Unknown and Risk sections, printing the id (r2, r26).
- `work add` refusing an unknown initiative, `--part-of`, `--blocked-by`, risk, or an accepted requirement with no scenario (r3, r27-r30).
- `work show` grouped by initiative with capability, what it waits on and file-set size; `--status` filter (r5, r31).
- `work next`: the moves that can be made now, changing nothing (r6).
- Guards: blockers green, no overlap with a claimed file set, one of two overlapping ready items claimed (r9, r10, r33).
- `work claim` adding paths to a claimed item's file set, refusing a path another holds (r11, r12, r34, r35).
- `work questions` and `work rule`, moving an item back to `planned` once every question is answered (r13-r15, r36, r37).
- `work withdraw`, refused for claimed or green items (r16, r38).
- `work log <work-item>` (r17).
- Refusals on stderr exit 1, bad usage exit 2 (r18, r40: covered by the general line).
- `work plugin` and `work_expectations.py`: unclaimed accepted scenarios as strict expected failures, `--work-item` runs, header and summary lines (r19-r24, r41-r48).

## Delivery

Kept: drafting from formulated proposals with `work add` (r1, r2), drafting from the spec alone (r8, r23),
committing alone (r10), starting `work run` (r26), reading nothing workers write (r12), showing what `work run`
printed (r13).

Ideas to test once the skeleton runs:
- Name each capability-proposal left out, with its status (r18).
- Exactly one work-item accepts each requirement; all requirements of one scenario in the same work-item (r2, r19).
- Deprecated scenarios listed under Retires in the work-item that replaces or removes them (r3).
- One capability or a check per work-item; one observable sentence; one unknown or none (r4, r20, r21).
- Risk `contract`, `concurrency`, `data` or `none`, a named risk only for an item reviewed alone (r5, r22).
- `blocked_by` only where scenarios need another's work (r6).
- Guarantees capabilities get a check against the bound (r7).
- A requirement with two readings gets no work-item and goes to the person through integration (r9, r24).
- One table of the drafted work-items (r25: kept as implementation).
- Stop on a dirty working tree or the default branch (r11, r27: covered by the general line).
- Wait for `work run`; ask nothing but its questions (r28, r29).
- Record answers with `work rule` in the person's words and run again (r14, r30).
- On all green, name the proposals and say closing the initiative is the owner's (r15, r31).
- On a budget, say what was spent, ask about raising it, change nothing meanwhile (r16, r32, r33).
- A question that a scenario is wrong goes through formulation or integration before `work rule` (r17, r34).

## Planning

Kept: the plan written to the brief's file (r1), the result file with status and file set (r14, r15), the
checkout unchanged (r16), open decisions with what they rest on (r3), tests the decisions break (r4), no code
(r6), a question when nothing settles a decision (r7).

Ideas to test once the skeleton runs:
- Why each accepted scenario is red today, unverified where the notes only `read` it (r2, r17).
- Tests the decisions break: every test the notes name, and what was checked when the list is empty (r4, r18).
- Step definitions and fixtures to reuse, verify commands with scenario counts, deprecated scenarios retired (r5).
- A broken test whose fate a client would see is a question (r8).
- The final file set is the researcher's plus each file the plan adds, named (r9).
- Probe defects: wrong answers or lost data fixed here, the rest observations (r10, r19).
- Skipped-stage refusals and effects addressed in the decisions (r11).
- A randomized test that a dry run and a real run agree, written if missing (r12, r20).
- Reading only the work-item, notes, `spec/`, `features/`, `CLAUDE.md` and the file set (r13).
- Summary under fifteen lines (r21).

## Migration tools

Kept: the moves (r17), the ledger to decision files (r22, r57, r23, r58, r26 in implementation), `@holding` to
`@deprecated` with bindings (r27, r28), the ids (r11, r12, r49, r52, r19), path and reference rewrites (r14,
r20, r50, r51), `model check` passing (r42, for `run`), all-or-nothing refusal (r9, r18, r45).

Ideas to test once the skeleton runs:
- Only files under `--root` (r1).
- `migrate status`: what is left of the old system, exit 1 or 0 (r2, r3, r46).
- Refusals: not a git working tree, no or malformed `--context`, a context differing from `spec/index.md` (r4-r6, r48: covered by the general line).
- `--dry-run` and the per-step printed changes (r7, r8, r43).
- Nothing to migrate on a repository on the final layout (r10).
- `retired: []` added; `formulated_as` removed when it names its own feature file, refused otherwise (r13, r15, r16).
- A rewritten reference changes nothing else (r53); record frontmatter kept (r54).
- Moved paths in non-Markdown files listed with the line (r55).
- `.gitignore`'s `.superpowers/` to `.shop/scratch/` (r21, r56).
- Ledger entries with unknown property lines or no `date:` refused (r24, r59).
- A decision's `source` split into record ids, node ids and `by` (r25, r60, r61).
- Retitling `(held)` to `(deprecated)` and `Held for:` to `Deprecated for:`; unparsable modules or multi-line titles refused (r27, r29, r62).
- `migrate plan`: the living plan's open slices to work-items under `migrated-plan`, enabling slices to checks, backlog and log entries to observations, `--plan`, `--drop`, `--leave`, refusals for in-progress slices, unknown titles, untagged scenarios, an existing `migrated-plan` (r30-r41, r44, r63-r69).
- Bad usage exit 2 (r71).

## Drafted work-items

Needed, rewritten to the skeleton's lines:
- `work/i10-delivery-on-v3/work-queue-1` (merging work-queue-1's add, show and moves; accepts work-queue#r1-r7).
- `work/i10-delivery-on-v3/supervision-1` (merging what supervision-1, -2 and -3 had of the skeleton; accepts supervision#r1-r10, against the stub `claude`).
- `work/i10-delivery-on-v3/planning-1` (accepts planning#r1-r8), `delivery-1` (accepts delivery#r1-r7).
- `code-research-1`, `red-green-1` and `review-1`: needed for the stages, rewritten to those capabilities' skeleton or trimmed lines (other capabilities' files; their writers decide the ids).
- `work/i10-delivery-on-v3/delivery-5` as the skeleton's proof: one person-approved, formulated work-item on a fixture repository through every stage with real workers, ending green or `awaiting-ruling`.
- `work/i8-model-in-consumers/migrate-layout`, `migrate-decisions`, `migrate-deprecated`, `migrate-status-and-ids` folded into one or two work-items accepting migration-tools#r1-r7 (status leaves; ids stay).
- `work/i8-model-in-consumers/kb-trial` as the i8 proof, rewritten: a fresh clone, `migrate run` alone, `model check` passing (no skill, no gate; kb's ten lines with no scenario may still give `v_s3`).

Deferred, until the skeleton has run:
- i10: work-queue-2, -3, -4; supervision-4 (budgets), supervision-5 (fix work-items, branch review); delivery-2 (questions, rulings, budget); red-green-2; review-2; role-boundaries-1; formulation-1 (the harness move: the proof runs from the scratch harness), formulation-2.
- i10, the removals: delivery-3 (slicing, `scripts/plan`) and delivery-4 (superpowers dependency), done once the skeleton has delivered for real.
- i10, the other capabilities' changes: feature-file-tools-1, analysis-tools-1, design-model-check-2, spec-consistency-1, spec-migration-1, -2 (not on the skeleton's path).
- i8: migrate-plan; migration-skill (the skill's fixture case T-migrate-final).
- `work/i1-first-spec/spec-integration-1`, `-2`: spec-integration's fixture scenarios, not on the skeleton's path.

Dropped: none outright; every deferred item waits for evidence from the skeleton's runs.
