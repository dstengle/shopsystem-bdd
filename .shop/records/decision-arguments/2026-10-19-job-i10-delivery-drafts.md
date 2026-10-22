---
id: decision-argument/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-job-i10-delivery-drafts
kind: decision-argument
about: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-script-supervises-delivery, design-decision/missingmass.io/shopsystem/shopsystem-bdd/worker-results-are-files, design-decision/missingmass.io/shopsystem/shopsystem-bdd/work-item-lifecycle-as-run, design-decision/missingmass.io/shopsystem/shopsystem-bdd/review-of-work-items, design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-file-set-is-the-claim, design-decision/missingmass.io/shopsystem/shopsystem-bdd/superpowers-not-a-dependency, design-decision/missingmass.io/shopsystem/shopsystem-bdd/fixture-scenarios-under-pytest-bdd, design-decision/missingmass.io/shopsystem/shopsystem-bdd/plans-list-the-tests-they-break]
date: 2026-10-19
---

# i10 delivery on v3: drafts and the drafter's notes

The drafts of initiative i10 (delivery on design model v3: work-items, `scripts/work`, `work run` as a script supervisor) written on 2026-10-19 by a drafting agent under the common brief (initiative-archive/2026-10-19-job-migration-release-common-brief), with its NOTES.md: the open questions it put to the coordinator with a recommendation each, what in the repository contradicted the person's directions, the overlap with i11 and i8, and risks. They were integrated, unapproved, in commit b0231c6 (measurement/2026-10-19-job-migration-release-integration-report) and later reshaped at the EARS and release gates, so none is identical to a committed file: these are superseded drafts. Decisions 0037-0044 drafted here were accepted at the 0.21.0 release gate. Copied out of a job workspace on 2026-10-22; each file's text as it was, in the order NOTES, initiative, capability-proposals, proposed capability files, decisions, work-items.

Archived from git-ignored scratch; each file's text as it was.

## `.shop/scratch/from-job/design-drafts/i10/NOTES.md`

~~~~~~
# i10 drafts: notes for the coordinator

What is here: `initiative.md`; 14 capability-proposals `delivery-on-v3-<capability>.md` with the full proposed
files under `capabilities/` (4 new: work-queue, supervision, delivery, planning; 10 changed); 8 decisions
0037-0044 under `decisions/`; 31 work-items under `work-items/`. I ran a copy of the repository (not the repository)
with the drafts in place through `scripts/model check`: they parse; the problems are the expected ones (requirements
with no scenario yet, work-items accepting them, old scenarios of removed lines), plus the model gap in question 9.

## Open questions, each with my recommendation

1. **What builds i10?** The release builds the system it would be built with. Recommend: build work-queue-1..4 and
   supervision-1..5 with today's workflow (or plain sessions), then run every other i10 work-item through `work run`
   itself. That is the strongest evidence the supervisor works, and its `log.jsonl` is i12's first measurement.
   The removals (feature-file-tools-1, delivery-3, delivery-4) go last, since they delete the old system.
2. **How many fixture runs must pass?** Recommend 3 of 3 (decision 0043). The alternative is 2 of 3. With 3 of 3
   a step that fails one run in three counts as broken, which is how it behaves in a consuming repository. If
   verdicts flip between suite runs, 0043's revisit_when is the signal for changing it.
3. **Worktrees and parallel implementers, or one implementer in the main checkout?** Recommend worktrees, 2 at once
   by default (0041). Without them the file-set claim protects nothing. The risk is a consuming project whose
   editable install points at the main checkout: `[worktree] setup` covers it, and supervision-2's unknown probes it.
4. **After a ruling, does the planner run again?** Recommend no. The ruling goes into the work-item in the person's
   words and the next implementer reads it. Re-planning is in supervision's Not yet, with its trigger.
5. **Workers' permissions.** `claude -p` denies whatever would prompt, so a worker whose Bash commands are not
   allowed fails. Recommend `delivery.toml` `permission_mode`, default `acceptEdits`, with the README giving the
   allowlist a consuming repository needs (`Bash(python3 *)`, `Bash(git *)` and so on). Bypassed permissions only
   in a sandbox (supervision Not yet). supervision-1 probes what `--agent` with a plugin agent does.
6. **The planner's place in decisions 0020 and 0021.** Their Decision sections list the agents and models without
   `bdd-planner` (Opus, no Bash). I had no decision number left. Recommend: the coordinator gives a number for a
   light decision superseding design-decision/rules-held-by-agent-tools that lists the v3 agents. Failing that,
   role-boundaries#r2, r5 and r6 are the standing statement.
7. **The spec-integration fixture items** (spec-integration-1, -2) are `part_of` i1's
   capability-proposal/first-spec-spec-integration, because i10 does not change spec-integration and a work-item has
   to sit under a proposal. Recommend: keep them there and file them in i1's directory. The other spec-side
   capabilities have i10 proposals (formulation, spec-migration, spec-consistency), so their items sit under those.
8. **`depends_on` in the common brief.** For a work-item, the model's `depends_on` names capabilities (the
   planner's). Ordering between work-items is `blocked_by`, and that is what the drafts use.
9. **Retired ids and merged proposals (a model gap I found).** Today `model check` keeps reporting a merged
   proposal once an id it names is retired: `changes` gives v15e, `removes` stays unresolved (design-model-check#r23
   says so). Retiring design-model-check#r42 would put i3's merged proposal under v15e for good. I added a change to
   design-model-check#r6 and #r23: a merged, formulated or withdrawn proposal may name a retired id. Recommend
   approving it with 0036's change.
10. **Glossary terms in a proposal's `adds`.** spec-integration#r17 says a term rides in `adds`, but `model check`
    reports `term/<x>` there as no requirement reference. My proposals put their terms in the body. Recommend that
    i11 (or whoever owns terms) adds reading `term/` references to design-model-check.
11. **The old glossary terms.** batch-measurement (i12's, untouched) still uses slice, batch, controller and task.
    So I added no `Not:` words and removed no terms. Recommend that i12 retires them and adds `Not: slice, task` to
    work-item.
12. **Work-item names.** design-model.md gives the id `<capability>/<n>`, but the id grammar forbids `/` in a name.
    Recommend `<capability>-<n>`, numbered across the context: `design-model-check-1` already exists from i2, so
    mine is `-2`.
13. **Lifecycle extensions.** claimed → ready (a refused claim) and claimed → awaiting-ruling (an implementer's
    stop) are not in grammar.md v3, which has awaiting-ruling only from planned. Recommend accepting them as
    extensions, as `withdrawn` was (0039). The grammar text is the person's to change.
14. **Fixture cost.** About 50 cases × 3 runs × $0.3-3 a session, so roughly $100-300 for a full fixture run, and
    more for deliver-real. Runs are cached by the plugin's tree hash. Recommend running a capability's fixtures when
    its skill or agent changes, and the whole set once per release with `--fixture-record`.
15. **One commit per move.** That gives many small commits on the initiative branch. Recommend keeping it: git
    becomes the record of every transition, which i12 can read, and a run that is killed loses nothing.

## In the repository, against the directions (2026-10-19)

- `spec/index.md`: the Constraints still carry superpowers as a dependency. The Purpose still says "thin vertical
  slices", the glossary's slice entry points to the abandoned i4, and Testing says workflow scenarios are open.
  The delivery proposal's merge changes the first three; formulation-1's decision answers Testing.
- `README.md` and `.claude-plugin/plugin.json`: the superpowers dependency, slicing and per-version history of the
  old system (delivery-4).
- Not yet entries with triggers on abandoned i5: code-research, red-green, review, and design-model-check's
  work-queue view. All four are dropped in the drafts.
- `docs/capability-format.md` still says `#r<n>` is short for `#behaviour/r<n>`, against 0036 (design-model-check-2).
- `agents/code-scout.md` and the skills formulating-features, integrating-a-proposal, migrating-to-capabilities,
  checking-spec-consistency and initiative-round still speak of slicing, writing-plans, slice tags and the plan
  (delivery-3). Their `.superpowers/` paths are i11's.
- Decisions 0005, 0006 and 0007 are written in task and slice terms. 0007 is superseded by 0044. 0005 and 0006 are
  left standing, since their rule holds for work-items.
- The `slice_expectations` lines and `features plugin` in feature-file-tools (removed; work_expectations replaces them).

## Overlap with i11 (and i8)

- feature-file-tools#r21, r40 and formulation#r4: I change only their slice clause and leave the hold/holding
  words for i11's rename to deprecated. In the capabilities I rewrite whole (red-green, review, delivery, planning)
  I write "deprecated" already. Both proposals change these files, so merge them per file.
- design-model-check: i11's rule labels and `.shop/` paths (r19) and my r6, r22-r24, r43, r60 touch the same file.
- `.shop/delivery.toml`, `.shop/worktrees/` and `.shop/scratch/` (git-ignored) are new paths under i11's `.shop/`.
- Every binding work-item needs i11's pytest-bdd conversion and `pytest.ini`. formulation-1 adds the `fixture`
  marker and `addopts = -m "not fixture"` to it. The coordinator should link i11's work-item into the
  `blocked_by` of work-queue-1, design-model-check-2 and formulation-1.
- i8 migrates living slice plans to work-items. It needs this initiative's work-item form (work-queue's
  Implementation and decision 0026 plus `risk`, `plan`, `notes`, `fixes`, `findings`) and `work add`.

## What i12 will need from supervision

`log.jsonl` per initiative: the base commit; every move; every worker start and end with the agent, model, session
id, attempt, result status, exit, duration, cost and tokens; the suite records. It also needs the run directories
with `session.json`, the review-finding records, and a commit per move. Session ids are preassigned
(`--session-id`), so a transcript is found without any description parsing. Transcripts still expire after
`cleanupPeriodDays`, so i12's measurement should run soon after the release.

## Risks

- A Haiku scout's file set will often be incomplete. Each miss costs a `work claim`, or a BLOCKED and a wait. That
  shows up in the log (claims per item) and is i12's to measure.
- The stub `claude` can drift from real `claude -p` JSON. supervision-1 records the real output's shape.
- 3-of-3 fixture verdicts may be flaky on spec-side cases that passed 2 of 3 before (B-migrate-2,
  A-formulate in the scratch scores).
- The drafted work-items cannot be pulled before i10's proposals are approved, merged and formulated: until then
  `model check` reports their `accepts` as naming no scenario (design-model-check#r28).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/initiative.md`

~~~~~~
---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i10
title: Delivery on design model v3
summary: Work-items pulled through their stages by a script supervisor, with a claude -p worker for each stage and only the supervisor writing status.
kind: capability-change
owner-level: shopsystem-bdd
status: proposed
priority: 1
source: [review-finding/2026-10-13-kb-and-bdd-assessment, measurement/kb-batches-32-35]
date: 2026-10-19
---

The final state of delivery, in place of i4, i5, i6 and i7 (abandoned 2026-10-19). No intermediate stage:
the person's direction of 2026-10-19 (observation/2026-10-19-final-state-only).

## Why

The assessment of 13 October and kb batches 32-35: the controller session read 23-55% of a batch's cache and its
own turns were the span the agents did not use; rules asked of it (models, review by risk, fresh agents, one
batch a session) did not hold; Lands was exceeded in 15 of 23 slices for 790k tokens of sizing scouts; nothing in
the build layer named a capability, and reports, findings and notes were git-ignored and lost. The design model's
answer is the work-item, the work-queue and a supervising script. This initiative builds that, and removes what it
replaces.

## The final state

An initiative's capability-proposals are approved, merged and formulated as before. Then:

1. **The person asks to deliver it.** `delivering-an-initiative` (capability/delivery) drafts work-items from the
   formulated proposals with `work add`, reading only `spec/`, `features/` and `.shop/work/`: each added or changed
   requirement accepted by one work-item, one unknown each, a risk (`contract`, `concurrency`, `data`, `none`),
   `blocked_by` only where scenarios need another's work, deprecated scenarios under Retires. It commits them, shows
   one table, and starts `work run` in the background. It reads nothing workers write.
2. **`work run <initiative>` supervises** (capability/supervision, design-decision/a-script-supervises-delivery).
   Stage by stage it starts a fresh `claude -p --agent shopsystem-bdd:<agent>` worker with one brief file:

   | status | worker | result → status |
   |---|---|---|
   | drafted | `code-scout` (researcher) | DONE with a file set → researched |
   | researched | `bdd-planner` (new) | DONE → planned; QUESTION → awaiting-ruling |
   | planned | none: the guard | blockers green, no claimed file set overlapping → ready |
   | ready | `bdd-implementer`, in `.shop/worktrees/<item>/` | claimed; DONE → rebased, tested, merged → done; PARTIAL → continuation; BLOCKED, HAND-BACK, NEEDS_CONTEXT → awaiting-ruling; a refused `work claim` → ready |
   | done, risk named | `bdd-task-reviewer` | nothing to fix now → green |
   | all done | `bdd-branch-reviewer` from the initiative's base | nothing to fix now → each done item green |

   A worker's outcome is only its `result.json` (design-decision/worker-results-are-files); a missing or malformed
   one is a failed stage, retried once, then a question. Findings to fix now become fix work-items (`fixes:`,
   `findings:`), followed by a scoped re-review; other findings become observations; every review is a
   review-finding record. Each worker has a time and dollar limit by role, and the run has a budget
   (`.shop/delivery.toml`). Only `work run` writes status: a worker that touches `.shop/work/` has its change put
   back and its stage failed.
3. **The person is asked only at the end.** When nothing can move, `work run` exits (0 all green, 3 a question, 4
   a budget) printing each question with its readings and the `work rule` command. The session shows them, records
   the person's answers in their words with `work rule`, and starts `work run` again. A question about a scenario
   goes to formulation or integration first.

`scripts/work` (capability/work-queue) is the queue the supervisor runs on: `add`, `show`, `next`, `claim`,
`questions`, `rule`, `withdraw`, `log`, `step`, `run` and `plugin`, which writes `work_expectations.py`: a
scenario of a work-item not yet claimed is a strict expected failure, so the suite is green between work-items.

**What it records, for i12.** Per initiative, `.shop/work/<initiative>/log.jsonl`: the base commit; every move
(time, item, before, after, by whom, why); every worker start and end (item, stage, attempt, agent, model, session
id, result status, exit, duration, cost, tokens from `claude`'s JSON); every suite record. Per stage, a run
directory `runs/<item>/<k>-<stage>/` with the brief, the result, `session.json` and the notes, plan, report or
findings. Each move is its own commit (`work: <item> <before> -> <after>`). The session ids name the transcripts
i12's `measure` reads; nothing in it needs a dispatch description to be parsed.

## Removed

- `skills/slicing-into-increments`, `scripts/plan`, `scripts/slice_expectations.py`, `features plugin`, slice tags,
  Lands, Steps, lanes, batch plans, the living plan and its archive, the HAND-BACK log entry and the checkpoint
  entry, the plan's Backlog (now observations).
- `superpowers:writing-plans`, `superpowers:subagent-driven-development` and `superpowers:executing-plans` as the
  delivery pipeline, and `superpowers@claude-plugins-official` as a dependency
  (design-decision/superpowers-not-a-dependency supersedes design-decision/superpowers-dependency).
- Decisions superseded: one-batch-one-session, fresh-agents-short-replies, suite-record-holds, review-by-risk,
  slice-budget-refused-by-plan, tests-the-decisions-break (0037-0041, 0044).
- `model check` reading `#behaviour/r<n>` (design-decision/one-requirement-form).

Kept for i12 as they are: `scripts/measure`, `spec/capabilities/batch-measurement.md`, `skills/analyzing-a-batch`.

## Capabilities

New: work-queue, supervision, delivery, planning. Rewritten in work-item terms: code-research, red-green, review,
role-boundaries. Changed by the removal: design-model-check, feature-file-tools, formulation, spec-migration,
spec-consistency, analysis-tools. One capability-proposal each, `capability-proposal/delivery-on-v3-<capability>`.

## The workflow scenarios as fixture sessions

design-decision/fixture-scenarios-under-pytest-bdd: the feature files of the workflow capabilities carry `@fixture`,
deselected from `python3 -m pytest` and run by `python3 -m pytest -m fixture`. The harness moves into
`tests/workflow/` from `/home/vscode/scratch/shopsystem-bdd/ids/` (formulation-1). A Given binds a fixture case of
the shelf repository, a When runs its prompt headless three times (cached by the plugin's tree hash), a Then checks
every run. The stage capabilities run through `work step <item>`; delivery's session runs `work run` with a stub
`claude`. Which case each requirement's scenario binds:

| capability | cases (requirements) |
|---|---|
| spec-integration | integrate (r1, r3), integrate-question (r1, r2), answer (r4), apply-reject (r5, r6), integrate-second-spec (r7), brainstormed-here (r10), apply (r11-r16, r18), small-change (r8), apply-delegated (r9), apply-with-work (r17), glossary-no-work (r19) |
| formulation | formulate (r1, r2, r4-r8, r11-r13), noclingo (r13), formulate-two-readings (r3), formulate-every-call (r9), formulate-hand-back (r10), formulate-avoided-word (r14) |
| spec-migration | migrate-notes (r2-r5, r7, r8), migrate-unclean ×3 (r1), migrate-drift (r6), migrate (r9-r11, r13, r14), migrate-ambiguous (r12) |
| spec-consistency | consistency-report (r1-r4), consistency-fix (r5-r10), formulate and apply transcripts (r11) |
| code-research | research (r1, r4, r5, r7, r9-r12), research-changed-line (r3), research-defect (r8), research-skipped-stage (r6) |
| planning | plan (r1-r6, r9, r13, r14), plan-question (r7, r8), plan-defect (r10), plan-import (r11, r12) |
| red-green | implement (r1, r2, r6, r8, r10, r11, r16, r18, r19), implement-big (r9), implement-no-context (r15), implement-passes-early (r3, r7), implement-contradiction (r4, r7), implement-breaks-test (r5), implement-unnamed-work (r12), implement-meaning (r13), implement-open-decision (r14), implement-claim-refused (r17) |
| review | task-review (r1-r5, r10, r12, r13), re-review (r8), branch-review (r6, r7, r9, r11), architecture-review (r14) |
| delivery | deliver (r1-r8, r10, r12, r15), deliver-unclean ×2 (r11), deliver-two-readings (r9), deliver-question (r13, r14), deliver-budget (r16), deliver-scenario-wrong (r17) |

role-boundaries is guarantees, checked by `tests/scripts/test_agents.py`. One end-to-end case, deliver-real, has
real workers deliver the lending initiative (delivery-5). The script capabilities (work-queue, supervision and the
others) are ordinary pytest-bdd scenarios, `work run`'s with the stub.

## Order

work-queue-1..4 → supervision-1..5 → the agents and skills with their fixture scenarios (code-research-1,
planning-1, red-green-1..2, review-1..2, delivery-1..2) → the removals (feature-file-tools-1, delivery-3, delivery-4)
→ delivery-5. The harness (formulation-1) and the spec side's fixture scenarios run beside them. Every binding item
waits for i11's pytest-bdd conversion of this repository's suite.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-analysis-tools.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-analysis-tools
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [analysis-tools]
adds: []
changes: [analysis-tools#r4]
removes: []
---

# Analysis tools: the probe line for a researcher's notes

What the gate approves: changed `analysis-tools#r4`: `tools probe --log` gives its line for a researcher's notes,
as `plan log` is gone.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-code-research.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-code-research
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [code-research]
adds: [code-research#r10-r12]
changes: [code-research#r1, code-research#r3, code-research#r4, code-research#r5, code-research#r6]
removes: [code-research#r2]
---

# Code research: the researcher stage

What the gate approves: added `code-research#r10-r12`, changed `#r1` and `#r3-r6`, removed `#r2`, and the narrator
"the supervisor that started the researcher" (was "the session that plans a batch").

The scout researches one drafted work-item for `work run` and its result gives the file set that becomes the
claim (r10). The Lands probe (r2) goes with slicing's budget (design-decision/the-file-set-is-the-claim supersedes
design-decision/slice-budget-refused-by-plan). The consequence sweep (r3) is done for the work-item whose requirement
replaces an assumption, not for a batch. The module sizes (r11) move from Implementation into Behaviour, as the
planner relies on them. The Not yet entry (pull drafted work-items) is done.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-delivery.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-delivery
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [delivery]
adds: [delivery#r1-r17]
changes: []
removes: []
---

# Delivery: a new capability

What the gate approves: `delivery#r1-r17`, a new capability, as written in `capabilities/delivery.md`.

`delivering-an-initiative` is the session's part of delivery: formulated capability-proposals become drafted
work-items, `work run` is started, and the person is asked only the questions it ends with. It replaces
`slicing-into-increments` and its hand-off to `superpowers:writing-plans`; what slicing kept that still holds (one
unknown, thin, observable, refusals routed to the spec, deprecated scenarios retired by the work that replaces
them) is in its lines, and the rest (Lands, Steps, lanes, batch plans, the living plan and its archive) goes with it.

Decision: design-decision/superpowers-not-a-dependency (supersedes design-decision/superpowers-dependency).

Glossary, added:
- **ruling**: the person's answer to a work-item's question, recorded with `work rule` in their words.

With this proposal `spec/index.md` changes: the Purpose says work-items for thin vertical slices; the
superpowers constraint goes; the build side of Composition lists delivery, code-research, planning, red-green,
review and role-boundaries with their new narrators, and the tools work-queue and supervision; Testing says the
workflow capabilities run as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-design-model-check.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-design-model-check
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [design-model-check]
adds: [design-model-check#r60]
changes: [design-model-check#r6, design-model-check#r22, design-model-check#r23, design-model-check#r24, design-model-check#r43]
removes: [design-model-check#r42]
---

# Design model check: one requirement form, and fix work-items

What the gate approves: added `design-model-check#r60`, changed `#r6`, `#r22`, `#r23`, `#r24`, `#r43`, removed `#r42`.

`model check` accepts a requirement only as `capability/<name>#r<n>` and its short forms
(design-decision/one-requirement-form): `#behaviour/r<n>` is unresolved (r22, r60), and the line that read it as the
same requirement goes (r42). A fix work-item's `fixes` and `findings` are checked like `blocked_by` (r24, r43). A proposal that has been merged keeps naming the ids it added, changed or removed after a later
proposal retires them, without a report (r6, r23): retiring r42 here would otherwise leave i3's merged proposal under
v15e, and every removal unresolved once merged. The
Not yet entry for a work-queue view is done by `work show` and `work next` (work-queue).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-feature-file-tools.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-feature-file-tools
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [feature-file-tools]
adds: []
changes: [feature-file-tools#r11, feature-file-tools#r21, feature-file-tools#r40]
removes: [feature-file-tools#r8, feature-file-tools#r9, feature-file-tools#r30-r34, feature-file-tools#r43-r45, feature-file-tools#r47-r50]
---

# Feature file tools: no slices

What the gate approves: changed `feature-file-tools#r11`, `#r21`, `#r40`; removed `#r8`, `#r9`, `#r30-r34`,
`#r43-r45`, `#r47-r50`.

Slice tags and `slice_expectations.py` go with slicing: `features tag` sets only `@r<n>` (r11), `features holding`
no longer reports a replacement's slice tag (r21, r40), and `features plugin` with the plugin's lines goes, replaced
by `work plugin` and `work_expectations.py` (work-queue#r19-r24). The words held and holding in r21 and r40 are
left for initiative i11's rename to deprecated.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-formulation.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-formulation
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [formulation]
adds: []
changes: [formulation#r4, formulation#r10]
removes: []
---

# Formulation: work-items in place of slices

What the gate approves: changed `formulation#r4` (a work-item, not a slice, retires a held scenario) and `#r10`
(a hand-back reaches formulation through a ruling on a work-item, not through slicing). The words held and holding
in r4 are left for initiative i11's rename.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-planning.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-planning
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [planning]
adds: [planning#r1-r14]
changes: []
removes: []
---

# Planning: a new capability

What the gate approves: `planning#r1-r14`, a new capability, as written in `capabilities/planning.md`.

The planner stage, researched to planned, was the planning session under `superpowers:writing-plans` with the
constraints slicing handed it. It becomes an agent, `bdd-planner`, that plans one work-item from its researcher's
notes and writes a plan file, and asks a question where a client-visible decision is open. The rules that held
(no code in a plan; tests the decisions break; a stage left out; a dry run that agrees) are its lines.

Decisions: design-decision/plans-carry-intent-not-code (stands), design-decision/plans-list-the-tests-they-break
(supersedes design-decision/tests-the-decisions-break).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-red-green.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-red-green
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [red-green]
adds: [red-green#r17-r19]
changes: [red-green#r1-r3, red-green#r5-r16]
removes: []
---

# Red-green: the implementer stage

What the gate approves: added `red-green#r17-r19`, changed `#r1-r3` and `#r5-r16` (r4 stands), and the narrator
"the supervisor that started the implementer" (was "the controller that dispatched the implementer").

The implementer takes a ready work-item in its worktree in place of a task brief, reports through its result file in
place of the plan's log (HAND-BACK becomes a result status, the checkpoint a report section), claims a file outside
its set or stops (r17), and leaves branches and `.shop/work/` to `work run` (r18, r19). Steps go; the 15-file
budget and `PARTIAL` stay (r9). A test's allowance is measured from the initiative's base (r6). The Not yet entry is
done. Decisions: design-decision/plans-list-the-tests-they-break, design-decision/the-file-set-is-the-claim.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-review.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-review
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [review]
adds: [review#r12-r14]
changes: [review#r1, review#r3, review#r4, review#r6, review#r8, review#r10, review#r11]
removes: []
---

# Review: work-items and initiatives

What the gate approves: added `review#r12-r14`, changed `#r1`, `#r3`, `#r4`, `#r6`, `#r8`, `#r10`, `#r11`, and the
narrator "the supervisor closing a work-item or an initiative" (was "the controller closing a task or a batch").

A task review covers one work-item's commits, a branch review the initiative branch (r13); each finding names its
work-item and its triage (r12), from which `work run` makes fix work-items and observations; the backlog is gone
(r8). The architecture reviewer gives a refactor as an observation with a check, not a slice (r14). The Not yet
entry is done. Decision: design-decision/review-of-work-items (supersedes design-decision/review-by-risk).

Glossary, added:
- **fix work-item**: a work-item `work run` adds for a review's findings to fix now, naming the work-item it fixes.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-role-boundaries.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-role-boundaries
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [role-boundaries]
adds: [role-boundaries#r6]
changes: [role-boundaries#r2, role-boundaries#r5]
removes: []
---

# Role boundaries: the planner

What the gate approves: added `role-boundaries#r6`, changed `#r2` and `#r5`.

`bdd-planner` joins the agents: no Edit (r2), Opus (r5), no shell (r6), so a planner cannot build what it plans.
The Purpose no longer says no script checks the lines: `tests/scripts/test_agents.py` does.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-spec-consistency.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-spec-consistency
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [spec-consistency]
adds: []
changes: [spec-consistency#r10]
removes: []
---

# Spec consistency: an observation in place of the backlog

What the gate approves: changed `spec-consistency#r10`: a finding not applied is recorded as an observation, as the
plan's backlog is gone. The Not yet entry's trigger reads a measured initiative in place of a batch.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-spec-migration.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-spec-migration
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [spec-migration]
adds: []
changes: [spec-migration#r1]
removes: []
---

# Spec migration: a claimed work-item in place of a slice in progress

What the gate approves: changed `spec-migration#r1`: migration stops while a work-item is claimed, not while a
slice is in progress.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-supervision.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-supervision
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [supervision]
adds: [supervision#r1-r35]
changes: []
removes: []
---

# Supervision: a new capability

What the gate approves: `supervision#r1-r35`, a new capability, as written in `capabilities/supervision.md`.

`work run` is the supervisor the design model names ("workers; a script supervises"). It replaces the controller
session of subagent-driven-development and the plan's execution rules: fresh agents, paths in and results out,
review by risk, fresh fix rounds, further rounds only for the severe, and one session per batch become what a
script does rather than what a controller is asked. Lanes go: implementers with disjoint file sets work at once,
each in its own worktree. What it records (`log.jsonl`, run directories, review-finding records) is what
initiative i12's `measure` reads.

Decisions: design-decision/a-script-supervises-delivery (supersedes design-decision/one-batch-one-session),
design-decision/worker-results-are-files (supersedes design-decision/fresh-agents-short-replies),
design-decision/work-item-lifecycle-as-run (supersedes design-decision/suite-record-holds),
design-decision/review-of-work-items (supersedes design-decision/review-by-risk),
design-decision/the-file-set-is-the-claim (supersedes design-decision/slice-budget-refused-by-plan).

Glossary, added:
- **supervisor**: `work run`, the script that starts the workers and alone writes a work-item's status.
- **worker**: a new `claude -p` session of one agent, started by the supervisor for one stage of one work-item.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/delivery-on-v3-work-queue.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-work-queue
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [work-queue]
adds: [work-queue#r1-r24]
changes: []
removes: []
---

# Work queue: a new capability

What the gate approves: `work-queue#r1-r24`, a new capability, as written in `capabilities/work-queue.md`.

The design model's work-queue (design-model.md v3, section 3, "Three structures") as a script, `scripts/work`,
over `.shop/work/`: drafting, the queue view, the guards of the lifecycle, claims, rulings and the move log. It
replaces `scripts/plan` (the living slice plan) and, through `work plugin`, `slice_expectations.py`: a scenario of
a work-item not yet claimed is a strict expected failure, as a scenario of a planned slice was, so the suite stays
green between work-items.

Decisions: design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim.

Glossary (`spec/index.md`), added with this proposal:
- **work-item**: the unit of delivery under a capability-proposal, done when the scenarios it accepts or its check pass, moved through its stages by `work run`.
- **file set**: the paths a work-item's work changes, found by its researcher and made final by its planner.
- **claim**: a claimed work-item's hold on its file set, which no other claimed work-item's file set shares.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/analysis-tools.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
title: Analysis tools
narrator: an agent researching or reviewing a project's code
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs]
formulated_as: features/analysis-tools.feature
retired: []
---

# Analysis tools

## Purpose
`scripts/tools` finds and installs a project's analysis tools in the project's own interpreter, and gives one
interface to them: a coverage map of which tests execute which code, the functions no test executed, the
references to a name, and a lint check. It is not a test runner for the fast suite and edits no dependency
file; it reports what the tools found and names a tool that is missing rather than skipping it.

## Behaviour
- [r1] **When** `tools` needs an interpreter, it uses the first of these, in this order: the one `--python` gives, used as given; `.venv/bin/python` under the current directory, if that file exists; `venv/bin/python` under the current directory, if that file exists; `$VIRTUAL_ENV/bin/python`, if that file exists, wherever `$VIRTUAL_ENV` points; and else the interpreter running the script. Unless `--log` is given, `tools probe` prints that interpreter's path and whether it came from `--python`, from the project's virtualenv (`.venv`, `venv` or `$VIRTUAL_ENV` alike), or from neither.
- [r2] **If** the project is not a Python project, `tools probe`, `tools install` and `tools check` say in one line that no analysis tools are known for its language and exit 1.
- [r3] **When** `tools probe` is run, `tools` prints one line per tool, `<name> <version>` for an installed tool and `<name> missing: <what it is for>` for a missing one, then the interpreter, and exits 1 when any tool is missing.
- [r4] **When** `tools probe --log` is run, `tools` prints one line, `Probe: tools -> ...`, giving each tool with its version or `missing`, for a researcher's notes.
- [r5] **When** `tools install` is run, `tools` installs each missing tool into the interpreter with pip and edits no dependency file.
- [r6] **If** the interpreter is not a virtualenv, `tools install` refuses to install into it and says so.
- [r7] **If** a tool is still missing after `tools install`, `tools` prints the tool, what it is for, what the workflow does without it, and the command that failed with the end of its error, and exits 1.
- [r8] **When** `tools map` is run, `tools` runs the suite once under coverage with a context per test, passing arguments after `--` to pytest, and keeps the map in `.superpowers/tools/coverage`.
- [r9] **When** `tools tests-of <file>[:<function, Class.method or line range>]` is run, `tools` prints each test that executed it in the last map, one a line, and how many of the map's tests that is, with the commit the map was made at.
- [r10] **Where** `--by-file` is given, `tools tests-of` prints a count for each test file instead of each test.
- [r11] **If** no test in the map executed the target, or the file has no function by that name, `tools tests-of` exits 1.
- [r12] **If** no map has been made, `tools tests-of` refuses and says to make one with `tools map`.
- [r13] **When** `tools untested <file>...` is run, `tools` prints each function in the files that no test in the last map executed.
- [r14] **When** `tools refs <name>` is run, `tools` prints every reference to that function, class or name defined in the project as `path:line`, including uses through an import or an alias, then one summary line with the number of references, the number of production files holding them and, as a separate number, the number of test files holding them, and where the name is defined.
- [r15] **If** nothing in the project is defined as `<name>`, `tools refs` exits 1.
- [r16] **When** `tools check` is run, `tools` runs ruff and vulture over the paths given or the Python files changed since `--base` and, where the project has import contracts, import-linter over the project, each under its own heading, and exits 1 when any reports.
- [r17] **If** a tool `tools check` would run is missing, `tools` names it as missing under its heading instead of skipping it.
- [r18] **If** the interpreter is not a virtualenv and a tool is missing, `tools install` installs nothing, prints for each missing tool the tool, what it is for, what the workflow does without it and that the interpreter is not a virtualenv, and exits 1.
- [r19] **When** `tools install` finds every tool present, `tools` says so and exits 0, whether or not the interpreter is a virtualenv.
- [r20] **When** `tools install` installs a tool, `tools` prints that the tool is installed.
- [r21] **If** the interpreter does not run, `tools probe`, `tools install` and `tools check` refuse, naming it and the end of its error.
- [r22] **When** `tools probe --log` is run, the line names every tool with its version or `missing`.
- [r23] **When** `tools map` is run, `tools` replaces any earlier map, prints pytest's last line, where the map is and the commit it was made at, and exits 0 whether or not the tests passed.
- [r24] **If** `tools map` makes no map, `tools` refuses, naming the command it ran and the end of its output.
- [r25] **When** `tools untested` is run, `tools` prints each function as `<path>:<line> <name>`, then how many functions no test executed and the commit the map was made at, and exits 0 however many there are.
- [r26] **If** no map has been made, `tools untested` refuses and says to make one with `tools map`.
- [r27] **If** coverage is missing from the interpreter, `tools tests-of` and `tools untested` refuse, saying to run `tools install`.
- [r28] **If** jedi is missing from the interpreter, `tools refs` refuses, saying to run `tools install`.
- [r29] **If** the file `tools tests-of` is given does not exist, `tools` refuses, naming it.
- [r30] **When** `tools refs` is run on a name the project defines, `tools` names where it is defined, counts no definition as a reference, and exits 0 however many references there are.
- [r31] **Where** `--base` is given, `tools check` checks the Python files changed since it and not deleted, in place of any paths given.
- [r32] **If** git cannot compare the working tree with `--base`, `tools check` refuses with git's error.
- [r33] **Where** `tools check` has no file to check, it says under the ruff and vulture headings that there is nothing to check, and those two do not make it exit 1.
- [r34] **Where** the project states no import contracts, `tools check` says so under the import-linter heading and does not run it.
- [r35] **When** a tool `tools check` runs prints nothing, `tools check` says under its heading that it is clean.

## Implementation, may change
- The tools probed are coverage, pytest-cov, jedi, ast-grep, ruff, vulture, import-linter and hypothesis.
- A Python project is one with `pyproject.toml`, `setup.py`, `setup.cfg`, `pytest.ini`, `requirements.txt`,
  `tox.ini` or any `.py` file under the current directory.
- `install` runs `<interpreter> -m pip install <package>` per missing tool.
- `map` runs `pytest -q --cov=. --cov-context=test`, writes the commit it was made at beside the data, and is
  its own command, never part of the fast suite. Code on the path of every call is executed by most of the
  suite, so the map narrows a search only for code off that path; a test that ran and failed counts.
- When the interpreter is not the one running the script, the script re-runs itself under it.
- `refs` uses jedi, so it reads the code as the interpreter would and does not find a name built from a
  string. A test file is under a tests or test directory or named `test_*` or `*_test.*`.
- `check` treats `.importlinter` or a `[tool.importlinter` table in `pyproject.toml` as the project's import
  contracts, and says so under the import-linter heading when there are none; headings are `== <tool> ==`.
- Exit status: 0 success, 1 something is missing, refused or reported, 2 bad usage.

## Not yet
- Only Python projects are known; in any other, agents search by text and say that they did — trigger: a project in another language asks for its analysis tools.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/code-research.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/code-research
title: Code research
narrator: the supervisor that started the researcher
group: service
rests_on: [design-decision/scout-on-haiku-at-low-effort, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim]
formulated_as: features/code-research.feature
retired: [r2]
---

# Code research

## Purpose
Reads the code and runs the system for one drafted work-item, so that its planner does not have to: why each
accepted scenario is red today, what the system answers today, the tests the change would break, and the file set
that becomes the work-item's claim. It is `code-scout`, started by `work run` on a `drafted` work-item. It builds
nothing and changes nothing in the checkout.

## Behaviour
- [r1] **When** research ends, its notes are in the notes file the brief names, its result file gives the file set, and the checkout is unchanged.
- [r3] **When** a requirement the work-item accepts changes or replaces one that existing code relies on, the notes list every place that still holds the old assumption, with the tests that execute it.
- [r4] **When** a work-item is researched, the notes say why each scenario it accepts is red today from a run of it, and each probe of today's behaviour with its command and what came back, marked `run`; what was concluded from reading is marked `read`.
- [r5] **When** a work-item is researched, the notes list the existing tests its accepted requirements make impossible to keep, starting from the tests that execute the code those requirements change.
- [r6] **When** a work-item adds a path that skips a stage, the notes list every refusal and effect only that stage produces.
- [r7] Each count in the notes says whether it came from `refs`, `tests-of` or a text search.
- [r8] **When** a probe finds a defect in today's behaviour, the notes report it with its reproduction.
- [r9] Probes run in a scratch directory, never on the checkout's data.
- [r10] The result's file set names every production and test file the work-item must change for its scenarios to pass and for everything that passes today to keep passing, each one a search or a read showed.
- [r11] The notes give each module on the change's path its line count and its room under the size limit `CLAUDE.md` states.
- [r12] The result's status is `DONE` or `NEEDS_CONTEXT`, and its summary is under fifteen lines.

## Implementation, may change
- Haiku at low effort; the notes are `notes.md` in the stage's run directory; probe files under `.shop/scratch/<run>/`.
- `tools refs`, `tests-of` and `untested` first, a text search for what is not a name.

## Not yet
- None.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/delivery.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/delivery
title: Delivery
narrator: the person delivering an initiative
group: service
rests_on: [design-decision/a-script-supervises-delivery, design-decision/gate-on-behaviour-lines, design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/review-of-work-items]
formulated_as: features/delivery.feature
retired: []
---

# Delivery

## Purpose
Turns an initiative's formulated capability-proposals into drafted work-items and has `work run` deliver them,
with the person asked only what nobody else may decide. It is `delivering-an-initiative`, run by the session the
person talks to. The session drafts from the spec and the feature files, never the code; it starts `work run`
and reads what it ends with, never what its workers write. It does not change a Behaviour line or a scenario: a
question about one goes to integration or formulation.

## Behaviour
- [r1] **When** the person asks to deliver an initiative, the session drafts work-items for each of its capability-proposals that is `formulated`, and names each one it leaves out with its status.
- [r2] **When** work-items are drafted, each requirement a formulated proposal adds or changes, and that has a scenario, is accepted by exactly one of them.
- [r3] **When** a proposal changes or removes a requirement whose old scenario is deprecated, one drafted work-item lists that scenario under Retires: the one that accepts its replacement, or the one that removes what it tests.
- [r4] Each drafted work-item accepts requirements of one capability or carries a check, and has one observable sentence and one unknown or none.
- [r5] Each drafted work-item's risk is `contract`, `concurrency`, `data` or `none`, and only the first three are reviewed alone.
- [r6] A drafted work-item is `blocked_by` another only when its scenarios cannot pass without the other's work.
- [r7] **Where** a capability is guarantees, its work-items carry a check against the requirement's bound in place of scenarios.
- [r8] The session drafts from `spec/`, `features/` and `.shop/work/` alone and reads no code.
- [r9] **If** drafting finds a requirement that admits two readings, the session drafts no work-item for it and shows the person the question with its readings, to be answered through integrating-a-proposal.
- [r10] **When** the work-items are drafted, the session commits them alone, shows the person one table of them (name, accepts, blocked by, risk) and starts `work run` without waiting for approval.
- [r11] **If** the working tree has changes, or the branch is the repository's default branch, the session stops before drafting and says which.
- [r12] **While** `work run` runs, the session reads nothing its workers write and waits for it to exit.
- [r13] **When** `work run` exits with questions, the session shows the person each question with its readings, as `work run` printed them, and asks nothing else.
- [r14] **When** the person answers, the session records each answer with `work rule` in the person's words and starts `work run` again.
- [r15] **When** `work run` exits with every work-item green or withdrawn, the session tells the person, names the initiative's capability-proposals, and says that closing the initiative is the owner's.
- [r16] **When** `work run` exits on a budget, the session tells the person what was spent and asks whether to raise the budget, and changes nothing before the answer.
- [r17] **Where** a question says a scenario the implementer was given is wrong, the session shows it as a formulation question, and the answer goes through formulating-features or integrating-a-proposal before it is recorded with `work rule`.

## Implementation, may change
- `skills/delivering-an-initiative/SKILL.md`. Drafting uses `work add`; the session runs `work run` as a
  background command and is woken when it exits; it reads `work run`'s last lines and `work questions`.
- Thin, by one unknown: a work-item with an unknown is usually one scenario; scenarios with none that share step
  definitions go together. A refactor a review asks for is an enabling work-item `for:` the one it unblocks.

## Not yet
- Drafting work-items for a cross-context-request's upstream proposal — trigger: a request between two bounded contexts on design model v3 is accepted.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/design-model-check.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check
title: Design model check
narrator: a person or agent checking a repository against the design model
group: service
rests_on: [design-decision/plugin-adopts-the-design-model, design-decision/model-check-solves-with-clingo, design-decision/scenario-names-requirement-by-tag, design-decision/retired-ids-in-capability-frontmatter, design-decision/work-file-forms, design-decision/capability-ids-are-context-scoped, design-decision/one-requirement-form, design-decision/review-of-work-items]
formulated_as: features/design-model-check.feature
retired: [r42]
---

# Design model check

## Purpose
`scripts/model` reads a bounded context's files — spec, feature files, decisions, work and records — as the
facts of `docs/design-model/grammar.md`, and reports what the grammar refuses. It also writes the generated
decisions index and traces a requirement to why it exists. It does not edit the spec, the work or the
records, and it checks one bounded context: product-level artifacts are read only where the files hold them.

## Behaviour
- [r1] **When** `model check` finds no violation, unresolved reference or file problem, it says so with the counts and exits 0.
- [r2] **When** `model check` finds violations, it prints each violated relation by its grammar.md name, with its rows, and exits 1.
- [r3] **If** a requirement bullet in a capability's Behaviour has no `[r<n>]`, `model check` reports it under v15a.
- [r4] **If** two requirements of one capability carry the same id, `model check` reports them under v15b.
- [r5] **If** a capability uses an id it lists as retired, `model check` reports it under v15c.
- [r6] **If** a capability-proposal that is `drafted` or `approved` changes a requirement no capability has, `model check` reports it under v15e.
- [r7] **If** a capability-proposal is `formulated` while a requirement it adds or changes has no scenario, and the capability is not guarantees, `model check` reports it under v15f.
- [r8] **If** a requirement of a capability that is not guarantees has no scenario naming it, `model check` reports it under v_s3.
- [r9] **If** a scenario names a requirement its capability does not have, or a capability rests on a decision that does not exist, `model check` reports the unresolved reference and exits 1.
- [r10] **If** a part has no `part_of`, or its `part_of` chain does not reach an initiative, `model check` reports it under v9a or v9c.
- [r11] **When** `model check` finds warnings, it prints each warning relation with its count and they alone do not change the exit status.
- [r12] **If** the clingo package is missing, `model check` says so with the command that installs it and exits 2.
- [r13] **When** `model facts` is run, it prints the facts read, one a line in clingo's syntax, using only the standard library.
- [r14] **When** `model decisions` is run, `spec/decisions.md` lists every decision under `decisions/` with its summary, status, what it supersedes and when to revisit it.
- [r15] **When** `model decisions --check` is run and `spec/decisions.md` is not what `model decisions` would write, it says so, exits 1 and writes nothing.
- [r16] **When** `model why <capability>#r<n>` is run, it prints the requirement, each capability-proposal that adds or changes it, the `part_of` chain to its initiative and the initiative's sources.
- [r17] **If** no capability-proposal adds or changes the requirement, `model why` says so and exits 1.
- [r18] **Where** a proposal's or work-item's list names `<capability>#r<a>-r<b>`, `model` reads it as every id from a to b.
- [r19] `model` reads, under `--root` (default the current directory), `spec/index.md`, `spec/capabilities/*.md`, every `*.feature` under `features/`, `decisions/*.md`, `work/<initiative>/*.md`, `records/observations.md` and any other Markdown under `records/` whose frontmatter has an `id`.
- [r20] A scenario names a requirement by a tag `@r<n>`, its own or its feature's, in the feature file its capability is `formulated_as`, or `features/<capability name>.feature` when it gives none.
- [r21] A reference written `<name>#r<n>` or `capability/<name>#r<n>` is read as a requirement of the capability `capability/<context path>/<name>` in the bounded context, the field fixing the kind where it is written `<name>`.
- [r22] **If** a list names a reference that is not `<capability>#r<n>`, with the capability written `capability/<context path>/<name>`, `capability/<name>` or `<name>`, or a range `#r<a>-r<b>` with a greater than b, `model check` reports it as unresolved.
- [r23] **If** a capability-proposal adds or removes a requirement no capability has, `model check` reports it as unresolved, except that adding an id the capability lists as retired is reported under v15c, and that a proposal that is `merged`, `formulated` or `withdrawn` may name an id its capability lists as retired, in `adds`, `changes` or `removes`, without a report.
- [r24] **If** a `supersedes`, `source`, `part_of`, `argues`, `under`, `for`, `blocked_by`, `depends_on`, `fixes` or `findings` names nothing in the repository, or names a node of the wrong kind (`supersedes` needs a design-decision, `under` and `depends_on` a capability, `for`, `blocked_by` and `fixes` a work-item, `findings` a review-finding), `model check` reports it as unresolved.
- [r25] **If** `spec/index.md` is missing or has no `id`, a capability's `id` is not `capability/<context path>/<file name>`, a capability has no `## Behaviour` section, or its `retired` lists an entry that is neither `r<n>` nor a number, `model check` reports a file problem naming the file.
- [r26] **If** a feature file is not the `formulated_as` of any capability, where a capability that gives none has `features/<its name>.feature`, or two of its scenarios share a title, `model check` reports a file problem naming the file. A scenario tagged `@holding` is not counted in the title check.
- [r27] **If** a work directory has no `initiative.md`, an initiative or part has no `id`, a part's kind is not a part kind, a status is missing or not in its kind's lifecycle, an initiative's priority is not a number or its date is not `YYYY-MM-DD`, `model check` reports a file problem naming the file; for a work directory with no `initiative.md` it names the directory, not the missing file.
- [r28] **If** a work-item accepts a requirement no scenario names yet, `model check` reports a file problem naming the work-item's file.
- [r29] **If** a decision has no `id`, a record with an `id` has a kind that is not a record kind, a frontmatter value is written as a folded or literal block, or one id names nodes of two kinds, `model check` reports a file problem.
- [r30] **If** `model check` finds a file problem, it prints each and exits 1.
- [r31] **When** `model check` ends without `--json`, it prints the counts of violations, warnings, unresolved references and file problems.
- [r32] **Where** `--limit <n>` is given, default 10, `model check` prints at most n rows of each violated relation and how many more there are.
- [r33] **Where** `--json` is given, `model check` prints the violations, warnings, unresolved references and file problems as one JSON object, with the same exit status.
- [r34] **If** an initiative that is not a capability-change has more than one part directly under it, `model check` reports it under v_k5, while a capability-change initiative may hold several capability-proposals.
- [r35] **If** a capability-proposal argues more than one capability, `model check` reports it under v_k6.
- [r36] A capability-proposal at `formulated` counts as closed when `model check` decides whether an initiative may be done.
- [r37] **When** `model decisions --check` finds `spec/decisions.md` is what `model decisions` would write, it says the file is current and exits 0.
- [r38] **When** `model decisions` is run, it prints the file it wrote, and a decision file with no `id` is left out of the index.
- [r39] **If** `model why` is given an argument that is not a requirement reference, it says why and exits 2.
- [r40] **If** no capability has the requirement `model why` names, it says so in place of the requirement's text and still lists the proposals that name it.
- [r41] **When** `model why` is run, it lists each capability-proposal that adds, changes or removes the requirement, in date order with its status and date. **If** no capability-proposal adds or changes it, including when every one that names it only removes it, `model why` exits 1; one proposal that adds or changes it is enough for exit 0.
- [r43] A node is written `<kind>/<context path>/<name>`, or in short `<kind>/<name>`, and a field that fixes the kind (`rests_on`, `supersedes`, `argues`, `under`, `depends_on`) and the capability part of a `#r<n>` reference may write the bare `<name>`; `part_of`, `for`, `blocked_by`, `fixes` and `findings` need `<kind>/<name>`; the context path is `<owner>/<product>/<context name>` and the bounded context is `bounded-context/<context path>`.
- [r44] A scenario tagged `@holding` is not read as an acceptance-scenario, whatever `@r<n>` tag it carries.
- [r45] **Where** a repository has no `decisions/` directory, `model` reads each `## design-decision/<slug>` heading of `spec/decisions.md` as a design-decision, and the entry's text up to a blank line, a heading or a property line (`date:`, `revisit_when:`, `supersedes:` or `source:`) as its summary.
- [r46] **If** a node's `id` is not `<kind>/<context path>/<name>` with its own kind, or spec/index.md's `id` is not `bounded-context/<context path>`, `model check` reports a file problem naming the file.
- [r47] **If** a reference is written `<context name>/<name>`, `decision/<name>` or `obs/<name>`, `model check` reports it as unresolved.
- [r48] A glossary entry is a bullet of `spec/index.md`'s `## Glossary` written `- **<term>**: <one-sentence definition>. Not: <word>, <word>.`, the `Not:` part optional, and `model` reads it as a term of the bounded context, with the id `term/<context path>/<term>`, the term lowercased with spaces as hyphens.
- [r49] **If** a bullet in `spec/index.md`'s `## Glossary` is not of that form, `model check` reports a file problem naming the file.
- [r50] **When** `model facts` is run, it prints for each glossary entry a `node` fact of kind `term`, a `term_of` fact naming the bounded context, and an `avoid` fact for each word after its `Not:`.
- [r51] **When** `model facts` is run, it prints a `mentions` fact for each requirement and each scenario and each term or avoided word it holds, matching a whole word, whatever its case, with a plural "s" allowed, so that "restore" is no mention of "store".
- [r52] **If** a requirement or a scenario mentions a word that its context's glossary lists after `Not:`, `model check` reports it under v_t1, naming the requirement or scenario, the word and the term.
- [r53] **If** two glossary entries have one term, `model check` reports it under v_t2.
- [r54] **If** a word one term lists after `Not:` is another term of the context, or the term itself, `model check` reports it under v_t3.
- [r55] **If** `import clingo` fails, `model check` looks for an interpreter that has clingo in this order: `$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH` outside the active virtualenv's `bin/`, `/usr/local/bin/python3`, `/usr/bin/python3`, and runs again under the first that has it.
- [r56] **When** `model check` has run again under another interpreter, it does so once, and a second failure to import clingo does not run it again.
- [r57] **If** no interpreter has clingo, `model check` exits 2 with its message naming each interpreter it tried.
- [r58] A capability-proposal or a work-item may have the status `withdrawn`, and `model check` counts a withdrawn part as closed when it decides whether an initiative may be done.
- [r59] **If** an initiative is `abandoned` while a part of it, at any depth, is neither closed nor `withdrawn`, `model check` reports the initiative under v_d2.
- [r60] **If** a reference is written `<capability>#behaviour/r<n>`, `model check` reports it as unresolved, as it does any reference that is not a requirement's.

## Implementation, may change
- `scripts/model.lp` is grammar.md v3 sections 1, 3 and 4 in clingo, with FIX notes where grammar.md does not
  compile as written; facts use grammar.md's relation names.
- Node ids: the bounded-context is spec/index.md's `id`; a requirement without an id is `<capability>#line<k>`;
  a scenario is `<feature path>:<title>`.
- The frontmatter reader is a YAML subset: scalars, `[a, b]` lists and `- x` block lists.

## Not yet
- Product-level artifacts (jobs, the context-map, seams, pins) read from a product repository — trigger: a second bounded context is checked together with this one.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/feature-file-tools.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools
title: Feature file tools
narrator: an agent or session editing feature files
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/held-scenarios]
formulated_as: features/feature-file-tools.feature
retired: [r8, r9, r30, r31, r32, r33, r34, r43, r44, r45, r47, r48, r49, r50]
---

# Feature file tools

## Purpose
`scripts/features` reads and edits Gherkin feature files without the test runner: it counts and lists
scenarios by tag or title, sets a scenario's requirement tag, moves a scenario between files and verifies the
move, holds and retires scenarios kept while they still pass, and checks and rewrites the titles test modules
bind. It is not a Gherkin runner and does not run
any test; it edits only the feature files, test modules and directory it is pointed at.

## Behaviour
- [r1] `features` reads every `*.feature` under `--dir` (default `features`), recursively, and text inside a docstring is never taken as a scenario, keyword or tag.
- [r2] **If** a feature file holds a `Rule:` block, `features` refuses, naming the file.
- [r3] **If** an edit would leave a file that `features` cannot read, `features` refuses the edit and leaves every file as it was. `features` reads a file as invalid when it holds a `Rule:` block outside a docstring, and checks nothing else of the result.
- [r4] **When** `features count --by-tag` is run, `features` prints the number of scenarios carrying each tag and a total, counting a Scenario Outline once per Examples row and giving each scenario its feature's tags and its Examples table's tags. The total counts every scenario, those carrying no tag included.
- [r5] **When** `features list --tag <tag>` is run, `features` prints the file and title of each scenario whose tags, its feature's and its Examples' included, hold that tag.
- [r6] **When** `features list --title <text>` is run, `features` prints the file and title of each scenario whose title contains the text.
- [r7] **If** `features list` matches no scenario, `features` prints nothing and exits 1.
- [r10] **If** `features tag` is given a title no file holds, or one several files hold, `features` refuses, naming every file that holds it, and changes no file.
- [r11] **If** `features tag` is given a tag not written `r<n>`, `features` exits 2 as bad usage and changes no file.
- [r12] **When** `features move <title> --to <file>` is run, `features` removes the scenario's block from its file and appends it unchanged to the end of the destination file.
- [r13] **Where** `--inline-background` is given, **when** `features move` is run, `features` puts the source Background's steps before the moved scenario's first step.
- [r14] **Where** `--keep-feature-tags` is given, **when** `features move` is run, `features` puts the source's feature tags that the destination's feature tags lack on a tag line of their own immediately above the moved scenario's `Scenario:` line, after any tag line the scenario already has, and joins them to none.
- [r15] **If** the destination of `features move` does not exist, `features` refuses and changes no file.
- [r16] **When** `features verify-moved --from <dir>` finds every scenario in the two trees alike by title in its effective tags, description, and Background and own steps, `features` prints how many scenarios match and exits 0.
- [r17] **If** a scenario's effective tags, description or steps differ between the two trees, `features verify-moved` names the scenario and which of them changed, and exits 1.
- [r18] **If** a title is held by more than one scenario in either tree, `features verify-moved` names the title as a duplicate and exits 1.
- [r19] **When** `features hold <title> --for <new title>` or `--for-removal` is run, `features` gives the scenario the tag `@holding`, " (held)" at the end of its title and a description line naming what it is held for, and changes nothing else in it, whether or not the replacement exists yet.
- [r20] **If** `features hold` is given a scenario already tagged `@holding`, `features` refuses it.
- [r21] **When** `features holding` is run, `features` lists each held scenario with what it is held for, or says that no scenario has the replacement's title.
- [r22] **When** `features holding` is run and no scenario is held, `features` says none is held.
- [r23] **When** `features retire <title>` is run on a scenario tagged `@holding`, `features` removes that scenario's block and leaves the rest of the file as it was.
- [r24] **If** `features retire` is given a scenario not tagged `@holding`, `features` refuses because it is not held, and leaves the file as it was.
- [r25] **When** `features bindings` finds a `scenario(<feature>, "<title>")` call under `--tests` (default `tests`) whose title no feature file has, or not the feature it names, `features` reports the module, line, title and feature of each, and exits 1.
- [r26] **When** `features bindings` finds every binding names a scenario, `features` says so and exits 0.
- [r27] **If** a test module under `--tests` does not parse, `features bindings` and `features rebind` refuse, naming the module.
- [r28] **When** `features rebind <old> <new>` is run, `features` rewrites `<old>` to `<new>` in each binding call that names it, changes nothing else in the module, and prints how many bindings it rebound, zero included.
- [r29] **If** `features rebind` is given a new title that is no scenario in a feature file, `features` refuses and changes no test module.
- [r35] **If** `features move`, `features hold` or `features retire` is given a title no file holds, or, without `--file`, one several files hold, `features` refuses, naming every file that holds it, and changes no file.
- [r36] **If** the destination of `features move` is the scenario's own file, `features` refuses and changes no file.
- [r37] **If** a title is in the `--from` tree and not the other, or in the other tree and not `--from`, `features verify-moved` names it as missing or as added, and exits 1.
- [r38] `features list --tag` finds the tag whether it is given with its leading `@` or without.
- [r39] **When** `features hold` has held a scenario, `features` prints its file and its new title.
- [r40] **When** `features holding` finds a held scenario with no `Held for:` line, `features` says so on that scenario's line.
- [r41] **If** `features rebind` is given a new title that several feature files hold, `features` refuses and changes no test module.
- [r42] **If** a binding call names the old title of `features rebind` in a string written over several lines, `features` refuses, naming the module and line, and changes no test module.
- [r46] **If** `features` refuses a command or an edit, it says why on stderr and exits 1.
- [r51] **When** `features tag <title> r<n>` is run on a title exactly one file holds, `features` makes `@r<n>` the scenario's one requirement tag, removing any other `@r<m>` tag it has, and leaves its other tags and every other line unchanged.
- [r52] **Where** `--file <path>` is given, the `features` script looks for the scenario's title in that file only, whatever the command.
- [r53] **If** `--file` names a file that does not hold the title, `features` refuses, naming the file, and changes no file.
- [r54] **If** `--file` names a file that holds the title twice, `features` refuses, naming the file, and changes no file.
- [r55] **If** `--file` names a file outside `--dir`, `features` refuses and changes no file.
- [r56] **Where** `--file <feature path>` is given, **when** `features rebind` is run, `features` rewrites only the bindings whose feature argument names that file, the feature argument resolved against `--dir`; without `--file` it rewrites every binding of the old title.

## Implementation, may change
- Gherkin is parsed line by line, not by a Gherkin library. A docstring opens and closes on `"""` or three
  backticks. A scenario's block is its tag lines, its `Scenario:` line and everything up to the next
  scenario's tag lines; `move` drops the block's trailing blank lines.
- `tag` replaces the scenario's first `@r<n>` tag or adds one to its last tag line; `hold` adds to the last tag line; a new tag line takes the scenario's indentation. Background steps
  inlined by `move` take the scenario's step indentation; kept feature tags take the `Scenario:` line's.
- `verify-moved` compares lines stripped of indentation, blank lines and comments, and also reports titles
  missing from or added to the second tree.
- `move` also refuses a destination that is the scenario's own file.
- `hold` writes the description line as `Held for: <title>` or `Held for: removal`, indented like the
  scenario's first following line.
- `bindings` reads only a title written as a plain string in the call; a feature given as a name is looked up
  among the module's own top-level assignments. `rebind` refuses a title written over several lines.
- Output lines: `list` prints `<path>: <title>`; `holding` prints `<path>: <title> | for: <what>`
  or `none held`; `bindings` prints `<path>:<line>: no scenario titled "<title>" in <feature>`.
- Exit status: 0 success, 1 a check failed or an edit was refused, 2 bad usage.

## Not yet
- `Rule:` blocks are refused rather than parsed — trigger: a feature file needs a `Rule:`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/formulation.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/formulation
title: Formulation
narrator: the person who approved the lines
group: service
rests_on: [design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/held-scenarios, design-decision/controller-per-spec-round]
formulated_as: features/formulation.feature
retired: []
---

# Formulation

## Purpose
Writes the acceptance-scenarios for approved Behaviour lines, one feature file per capability, from the
narrator's side and without sight of the code. It is `formulating-features`, run in a `initiative-round` that
dispatches `feature-formulator`s. It decides nothing: a line with two readings comes back as a question.

## Behaviour
- [r1] **When** lines are approved, each added or changed line with one reading has its scenarios in its capability's feature file `features/<name>.feature`: one scenario or one outline, or one scenario per reason for a line every call must keep (r9); every scenario that is not held formulates a line.
- [r2] Formulated scenarios are committed without being shown to the person for approval.
- [r3] **If** a line admits two readings, it gets no scenario and the person is shown the question with its two readings; the rest of the capability is formulated.
- [r4] **When** a line is changed or removed and its old scenario passes today, the old scenario stays in the suite tagged `@holding`, with " (held)" on its title and what it is held for, until a work-item retires it.
- [r5] **When** a line is changed or removed and its old scenario does not pass today, the old scenario is replaced or removed.
- [r6] **When** feature files are committed, `features bindings` reports that every binding names a scenario, and the commit holds only the feature files and the test files `features rebind` changed.
- [r7] **When** an existing feature file is changed, every scenario not added, changed or removed is byte for byte as it was, tags included.
- [r8] A feature file begins `# formulated from spec/capabilities/<name>.md`, then `Feature: <title>`, then `Narrator: <narrator>`.
- [r9] A line every call must keep is formulated as one scenario per reason the line gives, each with one representative call.
- [r10] **When** a work-item's implementer hands back a scenario with evidence and the person rules it a formulation question, the scenario is rewritten to fit its line and the evidence, or a question with two readings goes to the person.
- [r11] Each scenario carries the tag `@r<n>` of the one line it formulates, on the scenario's tag line, and its title is free.
- [r12] A scenario tagged `@holding` keeps the `@r<n>` tag it had and formulates no line.
- [r13] **Where** `model check` can run, **when** feature files are committed, it reports no scenario that names no line or two, and no added or changed line without a scenario; **where** it cannot, the round says so and checks coverage by hand.
- [r14] **When** a scenario uses a word its context's glossary avoids, the scenario is reworded to its line through the small-change path, without a further gate.

## Implementation, may change
- The workflow scenarios of this capability run as fixture sessions (design-decision/fixture-scenarios-under-pytest-bdd).
- The session dispatches `initiative-round` with the job `formulate`; the round dispatches one `feature-formulator`
  a capability with the brief in the skill, checks coverage one to one, runs each old scenario alone before
  replacing it, uses `features hold`, `features rebind` and `features bindings`, splices and commits.
- A scenario's title usually restates its line's condition, though the `@r<n>` tag is what names the line; Then lines name a refusal's reason, never message text.

## Not yet
None.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/planning.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/planning
title: Planning
narrator: the supervisor that started the planner
group: service
rests_on: [design-decision/plans-carry-intent-not-code, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim]
formulated_as: features/planning.feature
retired: []
---

# Planning

## Purpose
Turns one researched work-item into a plan an implementer can follow alone: the decisions the spec leaves open,
the tests those decisions break and what becomes of each, the final file set, what to reuse and how to verify. It
is `bdd-planner`, started by `work run` on a `researched` work-item. It plans from the researcher's notes and
carries intent, never code. A decision a client would observe that nothing settles is a question, not a plan.

## Behaviour
- [r1] **When** planning ends, the plan is in the plan file the brief names, the result file gives the final file set, the capabilities the work depends on and the questions, and the checkout is unchanged.
- [r2] The plan says, for each scenario the work-item accepts or for its check, why it is red today from the researcher's notes, marking as unverified each reason the notes mark `read`.
- [r3] The plan states each decision the capability's Behaviour leaves open, with the requirement or design-decision it rests on.
- [r4] The plan lists under Tests the decisions break every test the researcher's notes name and every test in the file set that a decision of the plan changes, each with what becomes of it: rewritten, and to assert what, or a question; an empty list says what was checked.
- [r5] The plan names the step definitions and fixtures to reuse, the commands that verify the work with the number of scenarios each runs, and the deprecated scenarios the work-item retires.
- [r6] The plan has no code block, file contents, diff or step-definition body.
- [r7] **If** a decision would change what the capability's narrator observes and no requirement or design-decision settles it, the result is `QUESTION`, giving the question, its readings and what the plan becomes under each.
- [r8] **If** what becomes of a broken test would change what a client observes, it is a question, not a rewrite.
- [r9] The final file set is the researcher's, with each file the plan's decisions add, each named.
- [r10] **When** the researcher's notes report a defect a probe found, the plan fixes it in this work-item when it is a wrong answer or lost data on the work-item's path, and otherwise the result gives it as an observation with its reproduction.
- [r11] **When** the notes list refusals and effects that only a skipped stage produces, the plan's decisions say for each what the new path does about it.
- [r12] **Where** the system has a dry run and a real run of an operation the work-item touches, the plan names the randomized test that they agree, and the work-item writes it when none exists.
- [r13] The planner reads the work-item, the researcher's notes, `spec/`, `features/`, `CLAUDE.md` and the files of the file set, and no other code.
- [r14] The result's status is `DONE`, `QUESTION` or `NEEDS_CONTEXT`, and its summary is under fifteen lines.

## Implementation, may change
- `agents/bdd-planner.md`: tools Read, Glob, Grep, Write; Opus. The plan is `plan.md` in the stage's run directory.
- A ruled work-item is not planned again: the ruling is under its `## Rulings`, for the implementer.

## Not yet
- None.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/red-green.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/red-green
title: Red-green
narrator: the supervisor that started the implementer
group: service
rests_on: [design-decision/feature-files-read-only-in-red-green, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim, design-decision/work-item-lifecycle-as-run]
formulated_as: features/red-green.feature
retired: []
---

# Red-green

## Purpose
Implements one ready work-item, one scenario at a time, under `bdd-red-green`, by the `bdd-implementer` that
`work run` starts in the work-item's worktree; or continues one, or carries out one fix work-item. The scenarios are
the contract; the implementer satisfies them and stops when one cannot be satisfied honestly. It never decides what
a scenario should have said, and it never moves a work-item: `work run` reads its result.

## Behaviour
- [r1] **When** a work-item is done, every scenario it accepts passes, and so does everything that passed in the suite record its brief gives.
- [r2] No commit of an implementer changes a `.feature` file, except removing, with `features retire`, a deprecated scenario the work-item lists under Retires.
- [r3] **If** a scenario the work-item accepts passes before any code is written for it, its check passes before any work, or a scenario of a work-item not yet claimed passes early, the implementer hands back.
- [r4] **If** a Then line can only pass through code that contradicts it, or a scenario can only fail on setup, the implementer hands back.
- [r5] **If** an existing test could stay green only by being removed, loosened, skipped or rewritten to assert something else, and the work-item's plan does not list it, the implementer stops `BLOCKED` naming the test.
- [r6] **When** the implementer changes a test's setup without touching what it asserts, or rewrites a test first committed after the initiative's base, its report names each such test.
- [r7] **When** the implementer hands back, its result is `HAND-BACK` with the stop condition, the evidence verbatim and which scenarios are green and red, and the work so far is committed on the work-item's branch.
- [r8] **When** a work-item's scenarios are green, the report says what someone can now do, what was surprising and the open questions, and the result gives the commits.
- [r9] **If** the work needs more than 15 files touched, the implementer names in its report, before any edit, the files this worker will touch, touches only those, stops at a green commit with the result `PARTIAL`, and a new implementer can continue from the report.
- [r10] **When** the scenarios are silent about a case, the code does not choose its behaviour and the report names it as an open question.
- [r11] **When** the plan carries code, the implementer does not paste it and says so in the report.
- [r12] **If** going green needs work that no scenario of the work-item describes and its plan does not name, beyond a trivial helper, the implementer hands back.
- [r13] **If** a previously green scenario breaks and fixing it would change what a step means, the implementer stops `BLOCKED`.
- [r14] **If** the work needs a decision the plan, its rulings and the capability's Behaviour leave open, or a file would cross the repository's size limit with no rule in `CLAUDE.md` saying where the code goes, the implementer stops `BLOCKED` with the specifics.
- [r15] **If** the brief names no scripts directory or no result file, or `bdd-red-green` is not in the implementer's context, the implementer stops `NEEDS_CONTEXT`.
- [r16] Every result's status is one of `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `NEEDS_CONTEXT`, and its summary is under fifteen lines.
- [r17] **If** the work needs a file outside the work-item's file set, the implementer claims it with `work claim` before editing it. **If** the claim is refused, it commits what is green and stops `BLOCKED`, naming the file and the work-item that holds it.
- [r18] The implementer works only in the worktree and on the branch its brief names, and never pushes, merges, rebases or resets.
- [r19] No commit of an implementer changes a file under `.shop/work/`.

## Implementation, may change
- The cycle: run one scenario red, write the step definitions it needs, the least code, run the work-item's
  scenarios (`--work-item <name>` where `work_expectations.py` is registered) and the scenario's module, refactor,
  commit; the whole suite once before the last commit, its record in the report.
- The implementer has no Skill tool; `bdd-red-green` is loaded through its `skills` field. Sonnet by default.
- A continuation reads the report first and takes the next part it names; a fix work-item reads its findings and
  fixes those and nothing else.

## Not yet
- None.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/review.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/review
title: Review
narrator: the supervisor closing a work-item or an initiative
group: service
rests_on: [design-decision/review-of-work-items, design-decision/rules-held-by-agent-tools, design-decision/worker-results-are-files]
formulated_as: features/review.feature
retired: []
---

# Review

## Purpose
Finds defects in one work-item's commits or in an initiative's whole branch, against the work-item's plan, the
spec and the repository's rules, and triages them. The reviewers are `bdd-task-reviewer` and `bdd-branch-reviewer`,
started by `work run`, and, when the person asks, `architecture-reviewer`. A reviewer changes nothing: what is to be
fixed now becomes a fix work-item, and the rest an observation.

## Behaviour
- [r1] **When** a review ends, its findings are in the findings file and the result file the brief names, and the working tree, index, HEAD and branches are as they were.
- [r2] **When** a task or branch review ends, every finding is graded Critical, Important or Minor and gives its file and line, what is wrong, why it matters and the fix.
- [r3] **When** a test was removed or weakened in the commits reviewed, the review lists it, and one the work-item's plan did not list is Important.
- [r4] **When** the implementer reported a setup-only change or a rewrite of a test this initiative wrote, the review checks each against the commits.
- [r5] Behaviour that contradicts a Behaviour line or a capability's Purpose is Important, whether or not a scenario covers it.
- [r6] **If** the branch reviewer cannot verify a check a work-item states, the review fails; a task reviewer lists what it cannot verify from the commits separately.
- [r7] **When** a branch review ends, it reports the suite's wall time and checks the code's shape against `CLAUDE.md` and its coupling to the projects it depends on.
- [r8] **When** the re-review of a fix work-item finds something other than data left invalid, the system's own fault on input, or a write that lands where a refusal belongs, it is triaged as an observation.
- [r9] **Where** the system has a dry run and a real run of one operation, the branch review runs the randomized test that they agree.
- [r10] **If** the commits reviewed change anything under `features/` other than removing a deprecated scenario the work-item lists under Retires, the review grades it Critical.
- [r11] **When** a branch review ends, it reports each deprecated scenario whose replacement's work-item is green, each scenario removed that was not deprecated, and each binding that names no scenario.
- [r12] Each finding names the work-item whose commits hold it and its triage: fix now for a wrong answer, a crash where a refusal belongs or lost data; observation for hardening, with its reproduction; or drop for polish that is not cheap.
- [r13] A task review reads the commits of one work-item and its plan; a branch review reads the initiative branch from its base and every work-item of the initiative.
- [r14] **When** the architecture reviewer finds a refactor to call for, it gives it as an observation with a check that would show it done, and names the work-item it would unblock, if any.

## Implementation, may change
- Opus; a work-item's commits over 8 production or 4 test files are reviewed by area, one reviewer each, in parallel.
- Probes go in the scratch directory the brief names; another revision is checked out as a worktree there.
- `tools check` runs the lint, dead-code and import-contract tools.

## Not yet
- None.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/role-boundaries.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/role-boundaries
title: Role boundaries
narrator: the person running the workflow
group: guarantees
rests_on: [design-decision/rules-held-by-agent-tools, design-decision/model-pinned-in-agent-definitions, design-decision/spec-writers-blind-to-code]
formulated_as: features/role-boundaries.feature
retired: []
---

# Role boundaries

## Purpose
What the plugin's agent definitions guarantee about each role, whatever a brief asks. Each is checked by reading
the definitions under `agents/`, not by a scenario. Tool lists bound what an agent can do directly: an agent with
Bash can still write files through the shell, which is why `work run` checks the files a worker leaves.

## Behaviour
- [r1] Only `initiative-round` can start another agent.
- [r2] No reviewer, no scout and no planner has the Edit tool.
- [r3] The `capability-writer` and the `feature-formulator` have no edit and no shell tool.
- [r4] The implementer's skills are the ones its definition lists under `skills:`, `bdd-red-green` always among them; it has no Skill tool, so the listing of every installed skill never enters its context.
- [r5] Each agent names its model: Opus for the spec writers, the planner and the reviewers, Sonnet for the implementer and `initiative-round`, Haiku for the scout.
- [r6] The `bdd-planner` has no shell tool.

## Implementation, may change
- Tool lists and `model:` in `agents/*.md`; `skills:` preloads a skill. `tests/scripts/test_agents.py` reads the
  definitions and checks each line.
- What a tool list cannot hold (no push, one write path) is asked, or `permissions.deny` in the consuming
  repository's settings.

## Not yet
- None.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/spec-consistency.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency
title: Spec consistency
narrator: the person keeping a spec
group: service
rests_on: [design-decision/glossary-terms-are-standing, design-decision/consistency-check-on-demand, design-decision/spec-writers-blind-to-code]
formulated_as: features/spec-consistency.feature
retired: []
---

# Spec consistency

## Purpose
Checks a bounded context's spec against itself: that one word means one thing, that one thing has one word,
that a line has one reading and that a scenario says what its line says. It is `checking-spec-consistency`,
run on demand by the session the person talks to, with a blind `spec-checker` agent for each judgment of
meaning. It reads nothing but `spec/` and `features/`, and it is not run by integration or formulation.

## Behaviour
- [r1] **When** the person asks for a consistency check, the session runs `model check` first and reports its `v_t1`, `v_t2` and `v_t3` rows as findings.
- [r2] **When** the check starts, the session states how many `spec-checker` dispatches it will make, one for each capability and one for the whole context, before it dispatches any.
- [r3] **When** a `spec-checker` is dispatched, it reads only `spec/` and `features/`, never the source, and writes its findings to a file under the drafts path and replies with a short summary.
- [r4] **When** the check ends in report mode, the session writes one findings file grouped by term cluster, then lines with two readings, then other drift, each finding naming its ids, and changes nothing else.
- [r5] **Where** fix mode is asked for, the session first proposes, for each term cluster, a glossary entry with its `Not:` words, and on the person's yes puts the entry and the line changes that apply it, ids kept, through one gate pass for the term.
- [r6] **Where** fix mode is asked for, **when** the terms are settled, a scenario that uses an avoided word is reworded to its line through formulation's small-change path, with no further approval.
- [r7] **Where** fix mode is asked for, **when** a line has two readings, the session asks the person one question with its readings, and has the answer integrated through the question path of integrating-a-proposal.
- [r8] **Where** fix mode is asked for, **when** a finding is drift other than a term or a line with two readings, the session asks the person which side is right, one finding at a time.
- [r9] **Where** fix mode is asked for, **when** a step is done, the session runs `model check` and reports what it found before the next step.
- [r10] **When** every finding is applied, rejected or recorded as an observation, fix mode ends and `model check` reports no `v_t1`, `v_t2` or `v_t3` row.
- [r11] **Where** an integration or formulation round runs, it does not run the consistency check; the check runs when the person asks for it.

## Implementation, may change
- The skill is `skills/checking-spec-consistency/SKILL.md`; the agent is `agents/spec-checker.md`
  (tools Read, Glob, Grep, Write; model sonnet).
- One dispatch for each capability judges its lines against its scenarios; one for the context judges every
  Behaviour line and the glossary, with no scenarios.

## Not yet
- The check runs in integration and formulation rounds — trigger: a measured initiative shows drift the on-demand check would have caught.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/spec-migration.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration
title: Spec migration
narrator: the person migrating a repository onto spec/
group: service
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines]
formulated_as: features/spec-migration.feature
retired: []
---

# Spec migration

## Purpose
Moves a repository that has design notes and approved feature files, but no `spec/`, onto capability files
paired with feature files. It is `migrating-to-capabilities`: the first integration, plus re-pairing the
existing scenarios. It changes the meaning of no approved scenario.

## Behaviour
- [r1] **If** the working tree is not clean, a work-item is `claimed`, or the suite does not run cleanly, migration stops before any change and says which.
- [r2] **When** migration drafts the spec, the person is shown the capabilities, which old features' scenarios each receives, every line no scenario backs, and every question, and nothing under `spec/` changes before their yes.
- [r3] **If** two scenarios with one title would land in one capability, the person is asked to retitle one at the gate.
- [r4] **When** migration is done, each capability has one feature file named for it, holding the scenarios mapped to it; each scenario's effective tags, title, description and tables, and its Background steps followed by its own steps, are as they were, the new `@r<n>` tags aside.
- [r5] **When** migration is done, the suite's summary, its passing scenarios by title and its count of scenarios per tag equal those before it, retitles approved at the gate and the new `@r<n>` tags aside.
- [r6] **If** any of those differ beyond what they set aside, migration stops and reports the difference without editing a scenario.
- [r7] No step definition's body changes in a migration.
- [r8] **When** migration is done, each note is headed as a proposal integrated into `spec/` on its date.
- [r9] **Where** a repository has capability files whose Behaviour lines carry no ids, **when** it is migrated to ids, each line gets `[r<n>]` in its order from r1 with its text unchanged, each capability gets `retired: []`, and each capability's id becomes `capability/<context path>/<name>`.
- [r10] **When** a repository is migrated to ids, its context's id is `bounded-context/<context path>`, the context path being the owner's domain, product and context name the person gives at the gate, unless `spec/index.md` already names them.
- [r11] **When** a repository is migrated onto `spec/` or to ids, each scenario that is not held gets the `@r<n>` tag of the line it formulates, and nothing else in a scenario changes but the holds the gate led to.
- [r12] **If** a scenario formulates no line or more than one, migration to ids shows it to the person at the gate as a question and tags nothing before the answer.
- [r13] **When** migration onto `spec/` or to ids is done, the suite's summary, its passing scenarios by title and its count of scenarios per tag equal those before it, the new `@r<n>` tags, the holds the gate led to and their " (held)" titles aside.
- [r14] **When** a repository is migrated to ids, its `decision/<name>` references and ledger headings become `design-decision/<name>`, every frontmatter `id` outside `spec/` is written in full, its observation headings `## obs/<x>` become `## observation/<context path>/<x>`, and nothing else in a reference changes.

## Implementation, may change
- A baseline under the scratch directory: the summary line, the passing tests (`-q -rA`), a copy of
  `features/`, and `features count --by-tag`.
- `capability-writer` drafts with the migration brief; `features move` (with `--keep-feature-tags`,
  `--inline-background`) moves scenarios; `features verify-moved` compares them.
- Bindings follow step definitions: `scenarios(...)` per capability where every step has one body, otherwise
  `@scenario(<file>, <title>)` from the old modules.

## Not yet
None.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/supervision.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
title: Supervision
narrator: the person who started work run
group: service
rests_on: [design-decision/a-script-supervises-delivery, design-decision/worker-results-are-files, design-decision/work-item-lifecycle-as-run, design-decision/review-of-work-items, design-decision/the-file-set-is-the-claim, design-decision/model-pinned-in-agent-definitions]
formulated_as: features/supervision.feature
retired: []
---

# Supervision

## Purpose
`work run <initiative>` delivers an initiative's work-items: it pulls each through its stages, starting a fresh
`claude -p` worker for each stage, reads each worker's result file, checks the guards, writes the status, merges
the implementers' work, runs the reviews, and logs every worker and every move for measurement. It is a script and
takes no judgment: what a worker decides comes back in its result, and what nobody may decide goes to the person as
a question. It never changes an initiative's or a capability-proposal's status.

## Behaviour
- [r1] **When** `work run <initiative>` is started, it pulls the initiative's work-items through their stages until none can move: a `drafted` one to a `code-scout` worker, a `researched` one to a `bdd-planner`, a `ready` one to a `bdd-implementer`, a `done` one with a named risk to a `bdd-task-reviewer`, and the initiative's branch to a `bdd-branch-reviewer` once every work-item is `done`, `green` or `withdrawn`.
- [r2] Each worker is a new `claude -p` session of its stage's agent, given one brief file that names the work-item, the stage, the files to read, the run directory to write in and the result file; no worker is resumed.
- [r3] `work run` takes a worker's outcome only from its result file. **If** the worker ends without one, or with one not in its stage's form, the stage has failed.
- [r4] **If** a stage fails, `work run` starts a new worker for it once more. **If** that one fails too, the work-item goes to `awaiting-ruling` with the failure as its question.
- [r5] **If** a worker changes a file under `.shop/work/` outside its run directory, `work run` puts the file back as it was, fails the stage and logs the file.
- [r6] **When** a researcher's result is `DONE` with a file set, `work run` writes the file set and the notes' path into the work-item and moves it to `researched`. **If** the file set is empty, the stage has failed.
- [r7] **When** a planner's result is `DONE`, `work run` writes the plan's path, the final file set and the capabilities the work depends on into the work-item and moves it to `planned`. **When** it is `QUESTION`, the work-item goes to `planned` and then `awaiting-ruling`, with each question and its readings.
- [r8] `work run` moves a `planned` work-item to `ready` as soon as the queue's guard allows it, and claims a `ready` one as it starts its implementer, when an implementer's place is free.
- [r9] Each implementer works in its own git worktree under `.shop/worktrees/<work-item>/`, on a branch made from the initiative branch's head, and no more implementers work at once than `delivery.toml` allows, 2 when it says nothing.
- [r10] **When** an implementer's result is `DONE` or `DONE_WITH_CONCERNS`, `work run` rebases its branch onto the initiative branch, runs the work-item's accepted scenarios, or its check, and the whole suite in its worktree, and only when they pass and nothing fails that passed in the last suite record merges the branch fast-forward and moves the work-item to `done`.
- [r11] **If** the work-item's commits change a file outside its file set, `work run` does not merge them, and the work-item goes to `awaiting-ruling` naming the files.
- [r12] **If** the rebase conflicts or the scenarios or the suite fail in the worktree, `work run` leaves the initiative branch as it was, and the work-item goes to `awaiting-ruling` with the conflict or the failing tests.
- [r13] **When** an implementer's result is `PARTIAL`, `work run` starts a new implementer on the same worktree and report as a continuation, at most three times in a row; at a fourth `PARTIAL` the work-item goes to `awaiting-ruling`.
- [r14] **When** an implementer's result is `BLOCKED`, `HAND-BACK` or `NEEDS_CONTEXT`, the work-item goes to `awaiting-ruling` with the result's questions and evidence, its claim released and its worktree and branch kept.
- [r15] **When** an implementer stops because `work claim` refused a path, `work run` moves its work-item back to `ready`, where it waits until the work-item holding the path is no longer `claimed`, and the next implementer continues on the same branch.
- [r16] **While** a work-item is `awaiting-ruling`, `work run` goes on with every work-item that is not blocked by it.
- [r17] **When** no work-item can move and no worker is running, `work run` exits, printing the number of work-items in each status, and each open question with its readings and the `work rule` command that answers it.
- [r18] `work run` exits 0 when every work-item is `green` or `withdrawn`, 3 when one is `awaiting-ruling`, 4 when a budget stopped it, and 1 when it stopped for any other reason.
- [r19] Each worker runs within the time and the spending `delivery.toml` gives its role. **If** it reaches either, `work run` ends it and the stage has failed.
- [r20] **When** the spending of the workers `work run` has started reaches the run's budget in `delivery.toml`, it starts no further worker, waits for the running ones, and exits saying what was spent.
- [r21] **When** a work-item whose risk is `contract`, `concurrency` or `data` is `done`, `work run` starts a task review of its commits. **When** the review finds nothing to fix now, the work-item goes to `green` once its accepted scenarios pass at the initiative branch's head.
- [r22] **When** a review triages findings as fix now, `work run` adds for each work-item they name a fix work-item at `planned`, with `fixes:` naming that work-item, `findings:` naming the review-finding, the files the findings name as its file set, and the requirements that work-item accepts; the work-item fixed goes to `green` only once every fix work-item for it is `green`.
- [r23] **When** a review ends, `work run` writes its findings as a review-finding record under `.shop/records/review-findings/`, about the reviewed work-item's capability, or about the bounded context for a branch review.
- [r24] **When** a review triages a finding as an observation, `work run` appends it to `.shop/records/observations.md`, about the work-item's capability, with its reproduction and the review-finding it came from.
- [r25] **When** every work-item of the initiative is `done`, `green` or `withdrawn`, none is `awaiting-ruling`, and the initiative branch has commits since its last branch review, `work run` starts a branch review from the initiative's base. **When** it finds nothing to fix now, each `done` work-item whose scenarios pass goes to `green`.
- [r26] **When** a fix work-item is `done`, `work run` starts a scoped re-review of its commits. A finding that is data left invalid, the system's own fault on input, or a write that lands where a refusal belongs gets a further fix work-item; any other finding is an observation, and the fix work-item goes to `green`.
- [r27] **When** `work run` starts or ends a worker, it appends a line to `log.jsonl` with the time, the work-item, the stage, the attempt, the agent, the model and the session id, and at the end the result's status, the exit, and the duration, cost and token counts the session reported.
- [r28] **When** `work run` has run the whole suite, it appends a suite record to `log.jsonl` (passed, failed, expected, the commit, the seconds), and each implementer's brief gives the last one.
- [r29] **When** `work run` moves a work-item, it commits the work-item's file, its run directory and `log.jsonl` on the initiative branch, and nothing else, with the message `work: <work-item> <before> -> <after>`.
- [r30] **If** another `work run` is running in the repository, `work run` refuses, naming its process id.
- [r31] **If** `work run` is started on the repository's default branch, or with changes in the working tree outside `.shop/`, it refuses before starting any worker and says which.
- [r32] **When** `work run` is interrupted, it ends its running workers and logs each as interrupted; the next `work run` continues each `claimed` work-item from its worktree and report as a continuation.
- [r33] **When** every work-item of the initiative is `green` or `withdrawn` and the last branch review found nothing to fix now, `work run` says the initiative's work-items are done, and changes no initiative's or capability-proposal's status.
- [r34] **When** `work step <work-item>` is run, `work` runs that work-item's next stage alone, under the rules of `work run`, and exits when it ends.
- [r35] **When** `work run` starts a worker, it prints one line naming the work-item, the stage and the agent, and one line when the worker ends with its result's status; it prints nothing a worker wrote.

## Implementation, may change
- A worker is `claude -p "<the brief's path and the result file>" --agent shopsystem-bdd:<agent> --session-id <uuid>
  --output-format json --max-budget-usd <n> --permission-mode <delivery.toml, default acceptEdits>`, with `--model`
  only where `delivery.toml` overrides the agent definition's. The executable is `$SHOPSYSTEM_WORK_CLAUDE`, else
  `claude`; the plugin's tests set it to a stub that follows a script.
- Run directory `.shop/work/<initiative>/runs/<work-item>/<k>-<stage>/`: `brief.md`, `result.json`, `session.json`
  (claude's JSON output), and the worker's `notes.md`, `plan.md`, `report.md` or `findings.md`.
- `.shop/delivery.toml`: `[tests] scenarios` (default `python3 -m pytest -q --work-item {item}`) and `suite`
  (default `python3 -m pytest -q`); `[workers] implementers = 2`, `researchers = 3`; `[limits]` minutes and dollars
  per role (scout 10/1, planner 20/3, implementer 45/8, task reviewer 20/3, branch reviewer 45/8) and `run_dollars`
  (default 60); `[worktree] setup`; `[models]` overrides.
- The initiative's base is the merge-base of the initiative branch with the default branch when `work run` first
  starts; it is the first line of `log.jsonl`. `.shop/worktrees/` and `.shop/scratch/` are git-ignored.
- One process, a lock file `.shop/work/.lock` holding its pid; workers run as child processes polled for exit.

## Not yet
- Re-planning after a ruling (the planner run again on the ruled work-item) — trigger: a ruled work-item's implementer stops on what the ruling changed.
- Workers in a sandbox the supervisor starts (a container per worker) — trigger: a consuming repository asks to run `work run` with bypassed permissions.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/capabilities/work-queue.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue
title: Work queue
narrator: a person, agent or script reading or moving work-items
group: service
rests_on: [design-decision/work-file-forms, design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim, design-decision/plugin-takes-the-dependencies-it-needs]
formulated_as: features/work-queue.feature
retired: []
---

# Work queue

## Purpose
`scripts/work` keeps the work-queue of a bounded context in `.shop/work/`: it drafts work-items, shows them and
what can move, moves them through their lifecycle checking each transition's guard, takes claims and rulings, and
logs every move. It is the only writer of a work-item's status. It also writes `work_expectations.py`, the pytest
plugin that expects the scenarios of work-items not yet claimed to fail. `work run`, the supervisor, is the
supervision capability; this one is the queue it runs on. It judges nothing and starts no worker.

## Behaviour
- [r1] `work` reads the work-items of every initiative under `.shop/work/`, each `.shop/work/<initiative>/<name>.md` whose frontmatter `kind` is `work-item`, and the scenarios under `features/`, and needs nothing beyond the standard library.
- [r2] **When** `work add <initiative> <name>` is run with `--part-of`, `--under` and either `--accepts` or `--check`, `work` writes `.shop/work/<initiative>/<name>.md` with the status `drafted`, the fields given, and the sections Observable, Unknown and Risk from `--observable`, `--unknown` and `--risk`, and prints the work-item's id.
- [r3] **If** `work add` names an initiative with no `initiative.md`, a `--part-of` that is not a capability-proposal of that initiative, a `--blocked-by` that is no work-item, a `--risk` other than `contract`, `concurrency`, `data` or `none`, or a requirement in `--accepts` that no scenario names, `work` refuses, naming it, and writes nothing.
- [r4] **If** the work-item's file already exists, `work add` refuses and leaves it as it was.
- [r5] **When** `work show` is run, `work` prints each work-item, one a line, with its status, its capability, what it waits on and the number of paths in its file set, grouped by initiative; `--status <status>` keeps only those with that status.
- [r6] **When** `work next` is run, `work` prints each move that can be made now, as the work-item, its status before and after and the worker that would make it, and changes nothing.
- [r7] **When** `work` moves a work-item, it writes the new status into the work-item's file and appends one line to `.shop/work/<initiative>/log.jsonl` giving the time, the work-item, the status before and after, who moved it (a worker's session id, `person` or `work`) and why.
- [r8] **If** a work-item's status in its file is not the last status `log.jsonl` gives it, `work` refuses to move it and names the file and both statuses.
- [r9] `work` moves a work-item from `planned` to `ready` only when every work-item it is `blocked_by` is `green` and no `claimed` work-item's file set has a path in its file set.
- [r10] **While** two `ready` work-items' file sets share a path, `work` lets at most one of them be claimed.
- [r11] **When** `work claim <work-item> <path>...` is run on a `claimed` work-item, `work` adds each path to its file set and prints them. **If** another `claimed` work-item's file set has one of the paths, `work` refuses, naming that work-item and the path, and adds none.
- [r12] **If** `work claim` names a work-item that is not `claimed`, `work` refuses and changes nothing.
- [r13] **When** `work questions` is run, `work` prints each `awaiting-ruling` work-item with each open question, numbered, its readings, and the `work rule` command that answers it.
- [r14] **When** `work rule <work-item> <n> "<answer>"` is run on an `awaiting-ruling` work-item, `work` writes the answer, its date and the question it answers under the work-item's `## Rulings`, and moves the work-item to `planned` once every open question has an answer.
- [r15] **If** `work rule` names a work-item that is not `awaiting-ruling`, or a question it does not have, `work` refuses and changes nothing.
- [r16] **When** `work withdraw <work-item> "<why>"` is run, `work` moves the work-item to `withdrawn` with the reason. **If** the work-item is `claimed` or `green`, `work` refuses.
- [r17] **When** `work log <work-item>` is run, `work` prints the work-item's lines of `log.jsonl` in order.
- [r18] **If** `work` refuses a command, it says why on stderr and exits 1; a command given wrongly exits 2.
- [r19] **When** `work plugin <directory>` is run, `work` writes `work_expectations.py` into the directory, over any there, and prints the line that registers it in the `conftest.py` beside it, importing it relative to the package where the directory holds an `__init__.py`. **If** the path is not a directory, `work` refuses and writes nothing.
- [r20] A scenario is accepted by a work-item when it is in the feature file of the work-item's capability and its `@r<n>` tag is a requirement the work-item `accepts`.
- [r21] **Where** `work_expectations.py` is registered, a scenario that some work-item accepts, while none of the work-items that accept it has reached `claimed`, is expected to fail: its failure is reported as expected and its pass fails the run.
- [r22] **Where** `work_expectations.py` is registered, a scenario that a `claimed`, `done` or `green` work-item accepts, or that no work-item accepts, runs as it is.
- [r23] **Where** `--work-item <name>` is given to pytest, only the scenarios that work-item accepts are run, each as it is, and the run fails when there are none.
- [r24] **Where** `work_expectations.py` is registered, the run's header names the `.shop/work` directory it read, or says none was found and nothing is expected to fail, and its summary says how many scenarios of which work-items were expected to fail.

## Implementation, may change
- `scripts/work` with its library `scripts/workqueue.py`; the frontmatter subset `scripts/model` reads. A work-item's
  fields are `design-decision/work-file-forms`', plus `risk`, `plan`, `notes`, `fixes` and `findings`; its body
  sections are Observable, Unknown, Risk, Retires, Rulings, and the paths of its notes, plan, report and findings.
- `work_expectations.py` reads pytest-bdd's scenario object for the feature file and the tags, and marks a waiting
  scenario `xfail(strict=True)`.
- `log.jsonl` is one JSON object a line; a move and its file are written together, the log line last.

## Not yet
- A work-queue across bounded contexts (an upstream's items for a cross-context-request) — trigger: a second bounded context is delivered by `work run`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/decisions/0037-a-script-supervises-delivery.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-script-supervises-delivery
summary: "scripts/work run pulls an initiative's work-items through their stages, starting a fresh claude -p worker for each stage, and is the only writer of a work-item's status; no language-model session controls delivery."
date: 2026-10-19
status: proposed
supersedes: design-decision/one-batch-one-session
source: "initiative/i10; review-finding/2026-10-13-kb-and-bdd-assessment, sections 3 and 4; measurement/kb-batches-32-35"
---

# 0037. A script supervises delivery

## Decision

Delivery is a loop in a script: `work run <initiative>` reads the work-queue under `.shop/work/`, starts one
`claude -p` session per stage of a work-item (researcher `code-scout`, planner `bdd-planner`, implementer
`bdd-implementer`, `bdd-task-reviewer`, `bdd-branch-reviewer`), checks each transition's guard itself and
writes the status. The session the person talks to drafts the work-items, starts `work run`, relays the
questions it ends with and records the person's rulings with `work rule`. It reads no worker's output.

## Context

In kb batches 32-35 the controller session read 23-55% of a batch's cache tokens and its own turns were the
gap between span and agent-minutes; "one batch, one session" was asked of it, not enforced. Rules a controller
was given (models, review by risk, fresh agents) were broken in the batches measured.

## Alternatives

A controller agent per batch (the assessment's recommendation 11); a shell loop with the guards in
`model check` (initiative i5). The first keeps a language model in the loop that decides nothing; the second
splits the guards from the loop that needs them.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/decisions/0038-worker-results-are-files.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/worker-results-are-files
summary: "A worker is a fresh session given one brief file, and its outcome is a JSON result file of its stage's form that work run reads; work run never parses a worker's prose and never resumes a worker."
date: 2026-10-19
status: proposed
supersedes: design-decision/fresh-agents-short-replies
source: "initiative/i10; design-decision/fresh-agents-short-replies; records/measurements/fixture-runs/2026-10-12-spec-round-test-log.md (reply files)"
---

# 0038. Worker results are files

## Decision

`work run` writes a brief file into the stage's run directory, `.shop/work/<initiative>/runs/<work-item>/<k>-<stage>/`,
and starts the worker with a prompt that names it. The worker writes its notes, plan, report or findings there and,
last, `result.json`: `status` (DONE, DONE_WITH_CONCERNS, PARTIAL, BLOCKED, NEEDS_CONTEXT, HAND-BACK or QUESTION, as
its stage allows), `summary` (under fifteen lines), `questions` (each with its readings), and the stage's own fields
(the researcher's and planner's `fileset`, the planner's `depends_on` and `plan`, the implementer's `commits` and
`report`, a reviewer's `findings`). A missing or malformed result is a failed stage. `claude -p --output-format json`
is written beside it, so cost, turns and the session id are read from a file too. No worker is resumed: a
continuation, a fix or a re-review is a fresh worker given the files.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/decisions/0039-work-item-lifecycle-as-run.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/work-item-lifecycle-as-run
summary: "work run moves work-items drafted → researched → planned → ready → claimed → done → green, with awaiting-ruling for every question to the person, and runs the suite itself before an item is done; a stopped or refused implementer releases its claim."
date: 2026-10-19
status: proposed
supersedes: design-decision/suite-record-holds
source: "initiative/i10; docs/design-model/grammar.md v3 section 5"
---

# 0039. The work-item lifecycle as work run runs it

## Decision

Transitions and their guards:

| from → to | made by | guard |
|---|---|---|
| drafted → researched | researcher's result | DONE, a non-empty file set, the notes file present |
| researched → planned | planner's result | DONE, the plan file present, a final file set |
| planned → awaiting-ruling | planner's result | QUESTION, each question with its readings |
| planned → ready | work | every `blocked_by` green; no claimed item's file set shares a path |
| ready → claimed | work, as it starts an implementer | the same, at that moment |
| claimed → done | implementer's result | DONE; rebased on the initiative branch; commits inside the file set; accepted scenarios (or check) pass; the suite fails nothing the last record passed |
| claimed → ready | work, on a refused `work claim` | the holder is claimed (EXTENSION: release) |
| claimed → awaiting-ruling | implementer's result | BLOCKED, HAND-BACK, NEEDS_CONTEXT, a fourth PARTIAL, a second failed stage, a conflict (EXTENSION) |
| awaiting-ruling → planned | the person, `work rule` | every open question answered |
| done → green | review | no finding to fix now, every fix work-item for it green, its scenarios pass at the head |
| any but claimed, green → withdrawn | the person, `work withdraw` | — |

A ruling is written into the work-item under `## Rulings` in the person's words; the next implementer reads it, and
no planner runs again. The suite record is `work run`'s own run after each rebase, logged in `log.jsonl` and given
in each implementer's brief; implementers do not log suite records.

## Consequences

Two transitions are extensions against grammar.md v3, which has awaiting-ruling only from planned: a claimed item
goes back to ready or to awaiting-ruling, so that a claim is never held by a stopped worker.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/decisions/0040-review-of-work-items.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/review-of-work-items
summary: "A done work-item with a named risk (contract, concurrency, data) gets a task review of its commits; every other is reviewed once by the initiative's branch review; findings to fix now become fix work-items, the rest observations, and every review is a review-finding record."
date: 2026-10-19
status: proposed
supersedes: design-decision/review-by-risk
revisit_when: "more than half of a measured initiative's task reviews find nothing to fix now"
revisit_signal: requests
source: "initiative/i10; design-decision/review-by-risk; measurement/kb-batches-32-35 (7 of 17 task reviews clean)"
---

# 0040. Review of work-items

## Decision

Risk is set when a work-item is drafted: `contract`, `concurrency`, `data` or `none`. `work run` starts
`bdd-task-reviewer` on a done item with one of the first three, and `bdd-branch-reviewer` over the initiative
branch from its base once every item is done, green or withdrawn. Each finding is graded, names its work-item and is
triaged fix now (correctness, data loss), observation (hardening, with its reproduction) or drop. Fix now becomes a
fix work-item (`fixes:`, `findings:`), planned, whose done is followed by a scoped re-review; after it only data
left invalid, the system's own fault on input, or a write where a refusal belongs gets another round. Observations
are appended to `.shop/records/observations.md`. Models are the agent definitions'; a work-item names none.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/decisions/0041-the-file-set-is-the-claim.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-file-set-is-the-claim
summary: "A work-item's file set, found by its researcher and finalised by its planner, is its claim: implementers whose sets are disjoint work at once, each in its own worktree; no count of modules is refused, and a dispatch still touches at most 15 files."
date: 2026-10-19
status: proposed
supersedes: design-decision/slice-budget-refused-by-plan
source: "initiative/i10; docs/design-model/design-model.md v3 section 3, the work-item; measurement/kb-batches-32-35 (Lands exceeded in 15 of 23 slices)"
---

# 0041. The file set is the claim

## Decision

The file set names every file the work-item changes. `work run` never runs two implementers whose sets share a
path. Each implementer works in `.shop/worktrees/<work-item>/` on a branch from the initiative branch's head; `work
run` rebases it, tests it there and merges it fast-forward. A file the implementer finds it needs is claimed with
`work claim`, which refuses one a claimed item holds; the implementer then stops, and the item waits. Where a
worktree needs its own environment, `delivery.toml`'s `[worktree] setup` command makes it. Sizing scouts and the
Lands line go; the implementer's 15-file dispatch budget and `PARTIAL` stay.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/decisions/0042-superpowers-not-a-dependency.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/superpowers-not-a-dependency
summary: "The plugin declares no dependency on superpowers and invokes none of its skills; a brainstorming note stays one possible source of a proposal."
date: 2026-10-19
status: proposed
supersedes: design-decision/superpowers-dependency
source: "initiative/i10; the person, 2026-10-19"
---

# 0042. Superpowers is not a dependency

## Decision

`.claude-plugin/plugin.json` has no `dependencies`. No skill, agent or script of the plugin names a superpowers
skill or a superpowers path; delivery is `delivering-an-initiative` and `work run`. The README names clingo,
pytest and pytest-bdd as the plugin's dependencies (design-decision/plugin-takes-the-dependencies-it-needs).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/decisions/0043-fixture-scenarios-under-pytest-bdd.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/fixture-scenarios-under-pytest-bdd
summary: "A workflow capability's scenarios are pytest-bdd scenarios tagged @fixture, deselected from the unit suite, whose When runs a fixture case headless three times and whose Then passes only when every run passes."
date: 2026-10-19
status: proposed
revisit_when: "a fixture scenario's verdict changes between two suite runs on one plugin tree"
revisit_signal: requests
source: "design-decision/workflow-scenarios-run-as-fixture-sessions (its open question); /home/vscode/scratch/shopsystem-bdd/ids/ (make_ids.py, score.py, run.sh)"
---

# 0043. Fixture scenarios run under pytest-bdd

## Decision

A workflow capability's feature file carries the feature tag `@fixture`; pytest-bdd makes it the marker
`fixture`, and the repository's `pytest.ini` has `addopts = -m "not fixture"`, so `python3 -m pytest` runs the
unit suite only. `python3 -m pytest -m fixture [path]` runs them. The harness is test code under `tests/workflow/`:
fixture cases (a builder that makes a throwaway repository and the prompt the session is given), the run (`claude
-p <prompt> --plugin-dir <this checkout> --model sonnet --output-format stream-json --dangerously-skip-permissions`
in that repository), and the checks over what a run left. A Given binds a case, a When runs it, a Then checks every
run. Each case runs `--fixture-runs` times (default 3), once for all the scenarios bound to it, and a Then passes
when `--fixture-pass` runs (default all) pass. Runs are kept under `--fixture-dir` (default
`~/.cache/shopsystem-bdd/fixture-runs/`) by the plugin's tree hash and reused, so a rerun after a change to a check
costs nothing. `--fixture-record <label>` writes the verdicts, costs and times as a measurement record under
`.shop/records/measurements/fixture-runs/`.

## Alternatives

Two of three runs; one run per scenario. A contract that one run in three breaks is broken that often in a consuming
repository.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/decisions/0044-plans-list-the-tests-they-break.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/plans-list-the-tests-they-break
summary: "A work-item's plan lists every existing test its decisions make impossible to keep and what becomes of each; any other test an implementer would weaken is BLOCKED, with two reported allowances measured from the initiative's base."
date: 2026-10-19
status: proposed
supersedes: design-decision/tests-the-decisions-break
source: "initiative/i10; design-decision/tests-the-decisions-break"
---

# 0044. Plans list the tests they break

## Decision

The planner writes, under "Tests the decisions break", each test the researcher's notes name and each test in the
file set that a decision of the plan changes: the test, the decisions, and whether it is rewritten (to assert what)
or a question for the person. An implementer changes what a test asserts only when it is listed. Two allowances stay:
a test's setup changed with no assertion touched, and a test first committed after the initiative's base (the
commit `work run` logged when it first started) rewritten to a decision of the plan; each is named in the report and
checked by the review. Deferral to a later slice goes: a work-item's scenarios are expected to fail until it is
claimed, and a test is never skipped to wait for one.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/analysis-tools-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-analysis-tools
status: drafted
wkind: capability
under: analysis-tools
accepts: [analysis-tools#r4]
blocked_by: []
risk: none
---

# analysis-tools-1

## Observable
`tools probe --log` and its `--help` no longer speak of the plan's log.

## Unknown
none

## What goes green
analysis-tools#r4: the output is as it is; the `--help` text says the line is for a researcher's notes.

## Files, roughly
`scripts/tools` (help text), its step definitions.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/code-research-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/code-research-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-code-research
status: drafted
wkind: capability
under: code-research
accepts: [code-research#r1, code-research#r3-r12]
blocked_by: [work-item/formulation-1, work-item/supervision-1]
risk: none
---

# code-research-1

## Observable
`code-scout` researches a drafted work-item from a brief and writes its notes and a result with the file set; its
scenarios pass in every run of `work step`.

## Unknown
Whether Haiku at low effort finds the whole file set on the shelf fixture (it found most of Lands' files, never all,
in kb).

## What changes
`agents/code-scout.md` rewritten for the researcher stage: the brief and result file, the notes' five parts in
work-item terms, the file set, module sizes; the Lands probe and the batch consequence sweep go (r2 retired); notes
and probes under the run directory and `.shop/scratch/`. Its description says it is started by `work run`.

## Fixture cases
Each runs `work step <item>` on a drafted lend-items work-item, the real `claude`.
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r4, r5, r7, r9, r10, r11, r12 | research | lend-items formulated, its work-items drafted |
| r3 | research-changed-line | an item accepting the changed keep-items#r3 |
| r8 | research-defect | a store that crashes on a title of spaces |
| r6 | research-skipped-stage | an item adding an import that skips the duplicate check |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`agents/code-scout.md`, `tests/workflow/test_code_research.py`, `tests/workflow/checks/code_research.py`, fixtures.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/delivery-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/delivery-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-delivery
status: drafted
wkind: capability
under: delivery
accepts: [delivery#r1-r12, delivery#r15]
blocked_by: [work-item/formulation-1, work-item/supervision-5]
risk: none
---

# delivery-1

## Observable
`delivering-an-initiative` drafts the work-items of an initiative's formulated proposals, commits them, shows them
and runs `work run` to the end; its scenarios pass in every run.

## Unknown
Whether a session waits on a background `work run` without reading its output (the reply-file wait of
initiative-round is the pattern), and how thin its drafted items come out on the lending fixture.

## What changes
New `skills/delivering-an-initiative/SKILL.md`: drafting by `work add` (one unknown, thin, risk, blocked_by,
Retires), routing a two-reading requirement to integration, the table, `work run` in the background, the end.

## Fixture cases
The session's `work run` uses the stub claude, whose script turns every item green.
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4, r5, r6, r7, r8, r10, r12, r15 | deliver | an initiative with two formulated proposals (lend-items, keep-items' changes with a held scenario), one merged proposal not formulated, a guarantees capability with a bound |
| r11 | deliver-unclean (two rows) | an uncommitted change; on the default branch |
| r9 | deliver-two-readings | a formulated requirement with two readings |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`skills/delivering-an-initiative/SKILL.md`, `tests/workflow/test_delivery.py`, `tests/workflow/checks/delivery.py`, fixtures.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/delivery-2.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/delivery-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-delivery
status: drafted
wkind: capability
under: delivery
accepts: [delivery#r13, delivery#r14, delivery#r16, delivery#r17]
blocked_by: [work-item/delivery-1, work-item/supervision-4]
risk: none
---

# delivery-2

## Observable
The session relays `work run`'s questions, records the person's answers with `work rule` and runs again, and
handles a budget stop and a wrong-scenario question as the lines say; in every run.

## Unknown
How a headless fixture gives the person's answer before the question is asked (the prompt gives answers in
advance, as consistency-fix did).

## Fixture cases
Stub claude as in delivery-1.
| requirements | case | what the fixture holds |
|---|---|---|
| r13, r14 | deliver-question | the stub planner returns QUESTION on one item; the prompt gives the answer |
| r16 | deliver-budget | the stub reports costs that reach the run's budget |
| r17 | deliver-scenario-wrong | the stub implementer hands back saying a scenario is wrong |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`skills/delivering-an-initiative/SKILL.md`, `tests/workflow/test_delivery.py`, `tests/workflow/checks/delivery.py`, fixtures.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/delivery-3.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/delivery-3
kind: work-item
part_of: capability-proposal/delivery-on-v3-delivery
status: drafted
wkind: enabling
under: delivery
check: "test ! -e scripts/plan && test ! -e skills/slicing-into-increments && ! grep -rniE 'slic(e|es|ed|ing)|writing-plans|subagent-driven|executing-plans|scripts/plan|plan (log|show|status|archive|add-slice)|\blanes?\b|batch plan' skills agents --exclude-dir=analyzing-a-batch, and python3 -m pytest -q passes"
for: work-item/delivery-1
blocked_by: [work-item/delivery-2, work-item/red-green-2, work-item/review-2, work-item/planning-1, work-item/code-research-1, work-item/feature-file-tools-1]
risk: none
---

# delivery-3

## Observable
Nothing of slicing is left in the plugin: no skill, script, agent text or test.

## Unknown
none

## What the check covers
Deleted: `skills/slicing-into-increments/`, `scripts/plan`, `tests/scripts/test_plan.py`. Reworded in work-item
terms: `skills/formulating-features` (slicing hands back, hands to slicing), `skills/integrating-a-proposal` (the
hand-off to writing-plans, QUESTION FOR THE SPEC from slicing), `skills/migrating-to-capabilities` (a slice in
progress, slice-tag counts), `skills/checking-spec-consistency` (the backlog), `agents/initiative-round.md` (reads the
plan), `agents/capability-writer.md`, `agents/spec-checker.md`, `agents/feature-formulator.md` where they speak of
slices. `skills/analyzing-a-batch/` and `scripts/measure` are i12's and are left as they are.

## Files, roughly
The files above (about 12).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/delivery-4.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/delivery-4
kind: work-item
part_of: capability-proposal/delivery-on-v3-delivery
status: drafted
wkind: enabling
under: delivery
check: "! grep -q dependencies .claude-plugin/plugin.json && ! grep -rn 'superpowers' README.md .claude-plugin skills agents scripts/work scripts/supervise.py scripts/model scripts/features scripts/tools --exclude-dir=analyzing-a-batch"
for: work-item/delivery-1
blocked_by: [work-item/delivery-3]
risk: none
---

# delivery-4

## Observable
The plugin declares no superpowers dependency, and its README describes the plugin as it is: spec side, delivery
by work-items and `work run`, its agents, scripts and dependencies.

## Unknown
none

## What the check covers
`.claude-plugin/plugin.json`: `dependencies` removed, the description and keywords without slicing or superpowers,
the version the release's. `README.md` rewritten to the final state (design-decision/superpowers-not-a-dependency):
what the plugin does, the skills and agents tables, the scripts (`model`, `features`, `tools`, `work`, `measure`), the
dependencies clingo, pytest and pytest-bdd and the `claude` CLI for `work run`, `delivery.toml`, and how to run the
unit suite and the fixture scenarios; the per-version sections of the old system go (git keeps them).
Superpowers paths in skills and agents (`.superpowers/spec-drafts/`) are moved by i11's layout work; if i11 has
not landed, this item is blocked on it.

## Files, roughly
`.claude-plugin/plugin.json`, `README.md`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/delivery-5.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/delivery-5
kind: work-item
part_of: capability-proposal/delivery-on-v3-delivery
status: drafted
wkind: enabling
under: delivery
check: "python3 -m pytest -m fixture tests/workflow/test_end_to_end.py passes in every run: the lending initiative delivered by delivering-an-initiative with real workers to every work-item green"
for: work-item/delivery-1
blocked_by: [work-item/delivery-4]
risk: none
---

# delivery-5

## Observable
One initiative goes from formulated proposals to every work-item green with real workers, on the shelf fixture.

## Unknown
The cost and time of one real delivery (it is i12's baseline material; the run's `log.jsonl` is kept with the
measurement record).

## What the check covers
Case deliver-real: as delivery-1's deliver case, with `claude` itself. Checks: every work-item green; the lend-items
and keep-items scenarios pass at the head; `log.jsonl` has a start and an end line for each stage of each item with a
session id and cost; at least one review-finding record (the branch review's); no file under `.shop/work/` changed
by a worker; the session read no worker output (its transcript). `--fixture-record` keeps the figures.

## Files, roughly
New `tests/workflow/test_end_to_end.py`, `tests/workflow/checks/delivery.py`, fixtures.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/design-model-check-2.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/design-model-check-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r6, design-model-check#r22-r24, design-model-check#r43, design-model-check#r60]
blocked_by: []
risk: none
---

# design-model-check-2

## Observable
`model check` reports `<capability>#behaviour/r<n>` as unresolved, checks a work-item's `fixes` and `findings`, and lets a
merged proposal name an id retired after it.

## Unknown
none

## What goes green
design-model-check#r6, r22, r23, r24, r43, r60. v15e in `scripts/model.lp` and the unresolved check of `removes` read the
proposal's status: a merged, formulated or withdrawn proposal may name a retired id. The scenario of the retired r42 is removed by formulation; its code (the
`(?:behaviour/)?` in `scripts/model`'s `REF`) and the `--help` sentence that reads both forms go, and
`docs/capability-format.md`'s sentence on `#behaviour/r<n>` with them. Any reference this repository's own files
write as `#behaviour/r<n>` is rewritten (a search first; none is expected).

## Files, roughly
`scripts/model`, `scripts/model.lp`, `docs/capability-format.md`, the model check step definitions, `tests/scripts/test_model.py`.

## Notes
Needs this repository's scenarios bound as pytest-bdd step definitions and the `.shop/` layout, both from initiative i11; the coordinator links i11's work-item into `blocked_by`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/feature-file-tools-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-feature-file-tools
status: drafted
wkind: capability
under: feature-file-tools
accepts: [feature-file-tools#r11, feature-file-tools#r21, feature-file-tools#r40]
blocked_by: [work-item/work-queue-4]
risk: none
---

# feature-file-tools-1

## Observable
`features` knows no slice: `tag` takes only `r<n>`, `holding` reports no slice tag, and `features plugin` and
`slice_expectations.py` are gone.

## Unknown
none

## What goes green
feature-file-tools#r11, r21, r40. Removed with their tests and scenarios: `features plugin` (r30, r43-r45),
`scripts/slice_expectations.py` (r31-r34, r47-r50), slice tags in `tag` (r8, r9).

## Files, roughly
`scripts/features`, delete `scripts/slice_expectations.py`, `tests/scripts/test_features.py` (the plugin and slice
tests go), the feature-file-tools step definitions.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/formulation-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/formulation-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-formulation
status: drafted
wkind: enabling
under: formulation
check: "python3 -m pytest -q collects no test marked fixture; python3 -m pytest -m fixture tests/workflow/test_harness.py --fixture-runs 1 passes, scoring the seven cases moved from the scratch harness as score.py scored them"
for: work-item/formulation-2
blocked_by: []
risk: none
---

# formulation-1

## Observable
The fixture harness is in the repository: a case can be built, run headless and scored by `python3 -m pytest -m
fixture`, and the unit suite runs none of it.

## Unknown
Whether pytest-bdd's feature tag `@fixture` becomes a marker that `addopts = -m "not fixture"` deselects in this
repository's configuration from i11, and how the run cache is keyed (the plugin's tree hash with the working tree's
diff).

## What the check covers
Moved from `/home/vscode/scratch/shopsystem-bdd/ids/` (outside git): `make_ids.py` and the older `make_shelf.py` become
`tests/workflow/fixtures/shelf.py` (one builder per case, the shelf repository written in the final layout:
`.shop/work/`, `spec/decisions/`); `run.sh`'s prompts and `claude -p` call become `tests/workflow/harness.py`;
`score.py`'s readers and checks become `tests/workflow/checks/` (one module per capability; `model_check`, `suite`,
`scenarios`, the transcript readers shared); `tests/workflow/conftest.py` adds `--fixture-runs` (3),
`--fixture-pass` (all), `--fixture-dir` (`~/.cache/shopsystem-bdd/fixture-runs/`), `--fixture-record <label>`,
and the session-scoped run cache. `tests/workflow/test_harness.py` runs the seven existing cases (integrate, apply,
formulate, noclingo, migrate, consistency-report, consistency-fix) through the moved checks. The slice-plan parts of
the old fixtures (`plan add-slice`, `@slice-<n>` tags) are dropped.

## Files, roughly
New `tests/workflow/` (conftest.py, harness.py, fixtures/shelf.py, checks/*.py, test_harness.py); `pytest.ini`
(marker, addopts); `.gitignore`.

## Notes
Needs this repository's scenarios bound as pytest-bdd step definitions and the `.shop/` layout, both from initiative i11; the coordinator links i11's work-item into `blocked_by`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/formulation-2.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/formulation-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-formulation
status: drafted
wkind: capability
under: formulation
accepts: [formulation#r1-r14]
blocked_by: [work-item/formulation-1]
risk: none
---

# formulation-2

## Observable
Formulation's scenarios run as fixture sessions and pass in every run.

## Unknown
Whether a hand-back reaching formulation through a ruling (r10) can be set up as a fixture without a real
`work run` (an awaiting-ruling work-item written by the fixture with its evidence).

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r4, r5, r6, r7, r8, r11, r12, r13 | formulate | the lending lines applied, nothing formulated; the count scenario and removed r4's pass today |
| r13 (where it cannot) | noclingo | as formulate, clingo unimportable |
| r3 | formulate-two-readings | as formulate, one lend-items line with two readings |
| r9 | formulate-every-call | a line every call must keep, giving two reasons |
| r10 | formulate-hand-back | an awaiting-ruling work-item whose ruling sends a scenario back with its evidence |
| r14 | formulate-avoided-word | a scenario using a word the glossary avoids |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_formulation.py`, `tests/workflow/checks/formulation.py`, `tests/workflow/fixtures/shelf.py`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/planning-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/planning-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-planning
status: drafted
wkind: capability
under: planning
accepts: [planning#r1-r14]
blocked_by: [work-item/formulation-1, work-item/supervision-1]
risk: none
---

# planning-1

## Observable
`bdd-planner` plans a researched work-item from its notes; its scenarios pass in every run of `work step`.

## Unknown
Whether a planner limited to the notes and the file set writes the tests-the-decisions-break list as completely as
the planning session did with a scout re-run.

## What changes
New `agents/bdd-planner.md` (Read, Glob, Grep, Write; opus): the plan's sections, the question form with readings
and the plan under each, no code, the file set; the constraints of slicing's hand-off to writing-plans that still
hold, in work-item terms.

## Fixture cases
Each runs `work step <item>` on a researched work-item with prepared notes.
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4, r5, r6, r9, r13, r14 | plan | a researched lend-items item, notes with one `read` line and one broken test |
| r7, r8 | plan-question | notes where a broken test's fate is a contract decision |
| r10 | plan-defect | notes reporting a probe's defect, one on the item's path and one not |
| r11, r12 | plan-import | an import path that skips a stage, with a dry run beside it |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`agents/bdd-planner.md`, `tests/workflow/test_planning.py`, `tests/workflow/checks/planning.py`, fixtures.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/red-green-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/red-green-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-red-green
status: drafted
wkind: capability
under: red-green
accepts: [red-green#r1, red-green#r2, red-green#r6, red-green#r8-r11, red-green#r15, red-green#r16, red-green#r18, red-green#r19]
blocked_by: [work-item/formulation-1, work-item/supervision-2]
risk: none
---

# red-green-1

## Observable
The implementer takes a ready work-item in its worktree, goes green one scenario at a time and reports through its
result file; its scenarios pass in every run.

## Unknown
How much of `bdd-red-green` and `bdd-implementer.md` remains once plans, steps, lanes and the plan's log go (the
assessment counted 29k tokens of starting context against a 900-token brief).

## What changes
`skills/bdd-red-green/SKILL.md` and its `example/` rewritten: the cycle with `--work-item`, the suite record from the
brief, HAND-BACK as a result, the report's sections, `work claim`, Retires with `features retire`; no slice tags,
`plan log`, Steps or lanes. `agents/bdd-implementer.md` rewritten to match (brief, result file, worktree,
continuation, fix work-item; the 15-file budget kept). Rationalization and red-flag tables are cut to what a stop
condition needs.

## Fixture cases
Each runs `work step <item>` on a ready work-item with a plan.
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r6, r8, r10, r11, r16, r18, r19 | implement | lend-items-1 ready, its plan (one silent case, one code block in it), a held scenario to retire |
| r9 | implement-big | a plan whose file set has 18 files |
| r15 | implement-no-context | a brief with no scripts directory |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`skills/bdd-red-green/SKILL.md`, `skills/bdd-red-green/example/`, `agents/bdd-implementer.md`,
`tests/workflow/test_red_green.py`, `tests/workflow/checks/red_green.py`, fixtures.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/red-green-2.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/red-green-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-red-green
status: drafted
wkind: capability
under: red-green
accepts: [red-green#r3-r5, red-green#r7, red-green#r12-r14, red-green#r17]
blocked_by: [work-item/red-green-1]
risk: none
---

# red-green-2

## Observable
Each stop condition of red-green stops the implementer with the right status and evidence, in every run.

## Unknown
Whether one fixture can plant each stop without the others firing first.

## Fixture cases
Each runs `work step <item>` on a ready work-item.
| requirements | case | what the fixture holds |
|---|---|---|
| r3, r7 | implement-passes-early | a scenario the code already satisfies |
| r4, r7 | implement-contradiction | a Then that only code contradicting it can pass |
| r5 | implement-breaks-test | a decision that breaks a test the plan does not list (and a setup-only change that is allowed) |
| r12 | implement-unnamed-work | going green needs a module the plan does not name |
| r13 | implement-meaning | a green scenario breaks unless a step's meaning changes |
| r14 | implement-open-decision | a case the plan, rulings and Behaviour leave open |
| r17 | implement-claim-refused | the work needs a file a claimed item holds |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_red_green.py`, `tests/workflow/checks/red_green.py`, fixtures; `skills/bdd-red-green/SKILL.md`
only where a run shows a stop is not followed.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/review-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/review-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-review
status: drafted
wkind: capability
under: review
accepts: [review#r1-r5, review#r8, review#r10, review#r12, review#r13]
blocked_by: [work-item/formulation-1, work-item/supervision-5]
risk: none
---

# review-1

## Observable
`bdd-task-reviewer` reviews one work-item's commits from a brief and writes graded, triaged findings to its result;
its scenarios pass in every run.

## Unknown
none

## What changes
`agents/bdd-task-reviewer.md` rewritten: the brief (the item, its plan, its commits), the findings and result files,
the triage, the scoped re-review of a fix work-item; no Review:/Model: lines, no backlog, no lanes.

## Fixture cases
Each runs `work step <item>` on a done work-item with planted defects.
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4, r5, r10, r12, r13 | task-review | commits that remove an unlisted test, contradict a line, edit a feature file, and report a setup-only change |
| r8 | re-review | a fix work-item's commits leaving one hardening issue |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`agents/bdd-task-reviewer.md`, `tests/workflow/test_review.py`, `tests/workflow/checks/review.py`, fixtures.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/review-2.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/review-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-review
status: drafted
wkind: capability
under: review
accepts: [review#r6, review#r7, review#r9, review#r11, review#r14]
blocked_by: [work-item/review-1]
risk: none
---

# review-2

## Observable
`bdd-branch-reviewer` reviews an initiative branch and `architecture-reviewer` gives refactors as observations; their
scenarios pass in every run.

## Unknown
none

## What changes
`agents/bdd-branch-reviewer.md` (Write added for its result and findings; no Edit) and `agents/architecture-reviewer.md`
rewritten in work-item terms: the initiative branch from its base, the work-items' checks, deprecated scenarios and
their replacements' items; a refactor as an observation with a check.

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r6, r7, r9, r11 | branch-review | an initiative branch with an unverifiable check, a dry-run pair, a deprecated scenario whose replacement is green, a removed scenario that was not deprecated, a dangling binding |
| r14 | architecture-review | a module past `CLAUDE.md`'s size limit |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`agents/bdd-branch-reviewer.md`, `agents/architecture-reviewer.md`, `tests/workflow/test_review.py`,
`tests/workflow/checks/review.py`, fixtures.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/role-boundaries-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/role-boundaries-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-role-boundaries
status: drafted
wkind: guarantee
under: role-boundaries
check: "python3 -m pytest -q tests/scripts/test_agents.py passes: each line of role-boundaries#r1-r6 checked against agents/*.md"
blocked_by: [work-item/planning-1, work-item/review-2, work-item/red-green-1, work-item/code-research-1]
risk: none
---

# role-boundaries-1

## Observable
A test reads every agent definition and fails when a tool list or model breaks role-boundaries.

## Unknown
none

## What the check covers
r1 (only initiative-round has Agent), r2 (no Edit for reviewers, the scout and the planner), r3, r4 (the
implementer's `skills:` holds bdd-red-green and its tools no Skill), r5 (models by role, bdd-planner opus), r6 (no
Bash for the planner).

## Files, roughly
New `tests/scripts/test_agents.py`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/spec-consistency-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/spec-consistency-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-spec-consistency
status: drafted
wkind: capability
under: spec-consistency
accepts: [spec-consistency#r1-r11]
blocked_by: [work-item/formulation-1]
risk: none
---

# spec-consistency-1

## Observable
The consistency check's scenarios run as fixture sessions and pass in every run.

## Unknown
none

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r2, r3, r4 | consistency-report | the lending lines formulated, a glossary, three planted problems |
| r5, r6, r7, r8, r9, r10 | consistency-fix | as consistency-report; the prompt gives the answers |
| r11 | formulate, apply | their transcripts: no `spec-checker` is dispatched |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_spec_consistency.py`, `tests/workflow/checks/spec_consistency.py`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/spec-integration-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/spec-integration-1
kind: work-item
part_of: capability-proposal/first-spec-spec-integration
status: drafted
wkind: capability
under: spec-integration
accepts: [spec-integration#r1-r7, spec-integration#r10]
blocked_by: [work-item/formulation-1]
risk: none
---

# spec-integration-1

## Observable
Spec integration's gate scenarios run as fixture sessions and pass in every run.

## Unknown
How to run r10's "this session brainstormed the note" headless: a first `claude -p` turn that brainstorms, then
`--resume` with the integration request.

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r3 | integrate | keep-items r1-r4, the approved lending note |
| r1 (questions), r2 | integrate-question | the note leaves "too many books" open and has a sentence no line can quote |
| r4 | answer | round-1 drafts and a gate with one question; the prompt answers it |
| r5, r6 | apply-reject | round-1 drafts; the answer approves all but one line |
| r7 | integrate-second-spec | a note that asks for a second spec |
| r10 | brainstormed-here | two turns in one session: brainstorm, then integrate |

Placed under i1's proposal: these requirements came from it, and i10 brings only their scenarios' harness.

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_spec_integration.py`, `tests/workflow/checks/spec_integration.py`, `tests/workflow/fixtures/shelf.py`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/spec-integration-2.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/spec-integration-2
kind: work-item
part_of: capability-proposal/first-spec-spec-integration
status: drafted
wkind: capability
under: spec-integration
accepts: [spec-integration#r8, spec-integration#r9, spec-integration#r11-r19]
blocked_by: [work-item/spec-integration-1]
risk: none
---

# spec-integration-2

## Observable
Spec integration's apply, small-change and glossary scenarios run as fixture sessions and pass in every run.

## Unknown
none

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r11, r12, r13, r14, r15, r16, r18 | apply | round-1 drafts, the gate, the person's yes; a glossary entry added |
| r8 | small-change | a request to add one keep-items line, no note |
| r9 | apply-delegated | as apply, approved under the person's delegation |
| r17 | apply-with-work | as apply, in a repository with `.shop/work/` and a capability-proposal |
| r19 | glossary-no-work | a glossary change, no `.shop/work/` |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_spec_integration.py`, `tests/workflow/checks/spec_integration.py`, `tests/workflow/fixtures/shelf.py`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/spec-migration-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/spec-migration-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-spec-migration
status: drafted
wkind: capability
under: spec-migration
accepts: [spec-migration#r1-r8]
blocked_by: [work-item/formulation-1]
risk: none
---

# spec-migration-1

## Observable
Migration onto `spec/` runs as fixture sessions and passes in every run.

## Unknown
What planted difference makes r6's stop observable without the migration being wrong otherwise (a test module that
binds a scenario by a title the move would change).

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r2, r3, r4, r5, r7, r8 | migrate-notes | notes and approved features, no `spec/`; two scenarios with one title bound for one capability |
| r1 | migrate-unclean (three rows) | an uncommitted change; a claimed work-item; a failing suite |
| r6 | migrate-drift | as migrate-notes, with the planted difference |

`make_shelf.py` (scratch root) is the older generator these start from.

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_spec_migration.py`, `tests/workflow/checks/spec_migration.py`, `tests/workflow/fixtures/shelf.py`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/spec-migration-2.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/spec-migration-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-spec-migration
status: drafted
wkind: capability
under: spec-migration
accepts: [spec-migration#r9-r14]
blocked_by: [work-item/spec-migration-1]
risk: none
---

# spec-migration-2

## Observable
Migration to ids runs as fixture sessions and passes in every run.

## Unknown
none

## Fixture cases
| requirements | case | what the fixture holds |
|---|---|---|
| r9, r10, r11, r13, r14 | migrate | keep-items with no ids, the old `decision/` and `obs/` forms, a held scenario, an outline |
| r12 | migrate-ambiguous | as migrate, one scenario formulating two lines |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`tests/workflow/test_spec_migration.py`, `tests/workflow/checks/spec_migration.py`, `tests/workflow/fixtures/shelf.py`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/supervision-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/supervision-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-supervision
status: drafted
wkind: capability
under: supervision
accepts: [supervision#r2-r7, supervision#r27, supervision#r34, supervision#r35]
blocked_by: [work-item/work-queue-2, work-item/work-queue-3]
risk: data
---

# supervision-1

## Observable
`work step <item>` runs a drafted item's researcher or a researched item's planner as a fresh worker, reads its
result file, and moves the item, retries, or puts it to awaiting-ruling, with every start and end logged.

## Unknown
What `claude -p --agent shopsystem-bdd:<agent> --output-format json` gives for a plugin agent's session (session id,
cost, usage), and whether `--agent` loads the agent's `skills:` and `effort:` (a probe against the installed claude,
recorded in the notes).

## What goes green
supervision#r2-r7, r27, r34, r35: the brief file, the run directory `runs/<item>/<k>-<stage>/`, the result's form per
stage (design-decision/worker-results-are-files), a failed stage and its one retry, the restore of a work file a
worker changed, writing the file set, notes, plan and depends_on into the item, QUESTION to awaiting-ruling, the
log lines with the session's figures, and the two printed lines.

## Files, roughly
`scripts/work` (`step`), new `scripts/supervise.py` (stages, briefs, result schemas, the worker process), new
`tests/scripts/stub_claude.py` (a stand-in `claude` that reads its brief and writes the result a script tells it to,
with a `session.json` like claude's), step definitions for `features/supervision.feature`.

## Notes
Driven with `$SHOPSYSTEM_WORK_CLAUDE` pointing at `tests/scripts/stub_claude.py` (from supervision-1), so no model runs.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/supervision-2.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/supervision-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-supervision
status: drafted
wkind: capability
under: supervision
accepts: [supervision#r8-r15, supervision#r28]
blocked_by: [work-item/supervision-1]
risk: concurrency
---

# supervision-2

## Observable
A ready item's implementer works in its own worktree; on DONE the branch is rebased, tested there and merged
fast-forward, or the item goes to awaiting-ruling; PARTIAL continues; a refused claim sends the item back to ready.

## Unknown
How a worktree gets a working environment in a consuming Python project (`[worktree] setup`), and whether the
suite's interpreter resolves the worktree's sources rather than the main checkout's (an editable install points at
the main checkout).

## What goes green
supervision#r8-r15, r28, in a fixture git repository with a small pytest project, the stub claude committing in the
worktree as its script says.

## Files, roughly
`scripts/supervise.py` (implementer stage, worktrees, rebase, test, merge, suite record), `scripts/work`,
`.gitignore` (`.shop/worktrees/`, `.shop/scratch/`), step definitions; delivery.toml reading (the `[tests]` and
`[worktree]` tables) in `scripts/workqueue.py` or a small `scripts/delivery_config.py`.

## Notes
Driven with `$SHOPSYSTEM_WORK_CLAUDE` pointing at `tests/scripts/stub_claude.py` (from supervision-1), so no model runs.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/supervision-3.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/supervision-3
kind: work-item
part_of: capability-proposal/delivery-on-v3-supervision
status: drafted
wkind: capability
under: supervision
accepts: [supervision#r1, supervision#r16-r18, supervision#r29-r32]
blocked_by: [work-item/supervision-2]
risk: concurrency
---

# supervision-3

## Observable
`work run <initiative>` pulls every item through its stages to green or to a question, several workers at once,
and exits with the summary and the exit status the lines give.

## Unknown
How the loop waits on several child processes and a signal without threads (poll with a short sleep, or
`os.waitpid` on any child).

## What goes green
supervision#r1, r16-r18, r29-r32: the pull order, going on past an awaiting-ruling item, the exit summary and
statuses, the commit per move, the lock, the refusal on the default branch or a dirty tree, and the continuation
after an interrupt.

## Files, roughly
`scripts/supervise.py` (the loop), `scripts/work` (`run`), step definitions.

## Notes
Driven with `$SHOPSYSTEM_WORK_CLAUDE` pointing at `tests/scripts/stub_claude.py` (from supervision-1), so no model runs.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/supervision-4.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/supervision-4
kind: work-item
part_of: capability-proposal/delivery-on-v3-supervision
status: drafted
wkind: capability
under: supervision
accepts: [supervision#r19, supervision#r20]
blocked_by: [work-item/supervision-3]
risk: none
---

# supervision-4

## Observable
A worker is ended at its role's time or spending limit, and the run stops starting workers at its budget and exits 4.

## Unknown
Whether `--max-budget-usd` ends a session cleanly enough to leave its `session.json`, or the supervisor must read
the cost from the transcript.

## What goes green
supervision#r19, r20.

## Files, roughly
`scripts/supervise.py`, the `[limits]` table, step definitions.

## Notes
Driven with `$SHOPSYSTEM_WORK_CLAUDE` pointing at `tests/scripts/stub_claude.py` (from supervision-1), so no model runs.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/supervision-5.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/supervision-5
kind: work-item
part_of: capability-proposal/delivery-on-v3-supervision
status: drafted
wkind: capability
under: supervision
accepts: [supervision#r21-r26, supervision#r33]
blocked_by: [work-item/supervision-3]
risk: data
---

# supervision-5

## Observable
Done items with a named risk get a task review; once all are done a branch review runs; findings become fix
work-items, observations and review-finding records; items go green as the lines say.

## Unknown
none

## What goes green
supervision#r21-r26, r33: the task review, fix work-items (planned, `fixes:`, `findings:`, the findings' files),
the review-finding record (frontmatter id, kind, about; `scripts/model check` reads it), observations appended
under `.shop/records/observations.md` in its `## <id>` form, the branch review from the base, the scoped
re-review, and the closing message.

## Files, roughly
`scripts/supervise.py` (review stages, fix items, records), `scripts/workqueue.py`, step definitions.

## Notes
Driven with `$SHOPSYSTEM_WORK_CLAUDE` pointing at `tests/scripts/stub_claude.py` (from supervision-1), so no model runs.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/work-queue-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/work-queue-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-work-queue
status: drafted
wkind: capability
under: work-queue
accepts: [work-queue#r1-r8, work-queue#r17, work-queue#r18]
blocked_by: []
risk: data
---

# work-queue-1

## Observable
`work add`, `work show`, `work next` and `work log` work over `.shop/work/`, and every move is in `log.jsonl`.

## Unknown
Whether `scripts/model`'s frontmatter reader and feature reader can be shared with `work` without either changing behaviour.

## What goes green
The scenarios of work-queue#r1-r8, r17, r18: reading the queue, `add` and its refusals, `show` (with `--status`),
`next` (read-only), the move with its log line, the refusal on a status the log disagrees with, `log`, and exit
statuses. Moves are made by an internal function the later items and `work run` use; no `move` command is exposed.

## Files, roughly
New `scripts/work` and `scripts/workqueue.py` (stdlib); `tests/` step definitions for `features/work-queue.feature`
in i11's pytest-bdd form; possibly a shared reader factored out of `scripts/model` (then `tests/scripts/test_model.py`
must stay green as it is).

## Notes
Needs this repository's scenarios bound as pytest-bdd step definitions and the `.shop/` layout, both from initiative i11; the coordinator links i11's work-item into `blocked_by`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/work-queue-2.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/work-queue-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-work-queue
status: drafted
wkind: capability
under: work-queue
accepts: [work-queue#r9-r12, work-queue#r16]
blocked_by: [work-item/work-queue-1]
risk: concurrency
---

# work-queue-2

## Observable
A planned work-item becomes ready only when its blockers are green and no claimed item shares a path; `work claim`
and `work withdraw` work and refuse as the lines say.

## Unknown
How paths are compared for overlap (normalised relative paths; a directory claimed as a prefix of the paths under it, or not).

## What goes green
work-queue#r9-r12, r16.

## Files, roughly
`scripts/workqueue.py` (guards), `scripts/work` (claim, withdraw), their step definitions.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/work-queue-3.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/work-queue-3
kind: work-item
part_of: capability-proposal/delivery-on-v3-work-queue
status: drafted
wkind: capability
under: work-queue
accepts: [work-queue#r13-r15]
blocked_by: [work-item/work-queue-1]
risk: none
---

# work-queue-3

## Observable
`work questions` lists every open question with its readings and the command that answers it; `work rule` records
the person's answer and moves the item to planned when none is open.

## Unknown
none

## What goes green
work-queue#r13-r15. A question's form (number, text, readings, asked by, asked at) is the one `work run` writes
from a result's `questions` (design-decision/worker-results-are-files); write it here once, under `## Questions` in
the work-item, so supervision-1 only fills it.

## Files, roughly
`scripts/workqueue.py`, `scripts/work`, step definitions.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i10/work-items/work-queue-4.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/work-queue-4
kind: work-item
part_of: capability-proposal/delivery-on-v3-work-queue
status: drafted
wkind: capability
under: work-queue
accepts: [work-queue#r19-r24]
blocked_by: [work-item/work-queue-1]
risk: none
---

# work-queue-4

## Observable
With `work_expectations.py` registered, the suite is green between work-items: the scenarios of items not yet
claimed fail as expected, and `--work-item <name>` runs one item's scenarios as they are.

## Unknown
How a pytest-bdd item gives its feature file and tags across the pytest-bdd versions in use (the scenario object, or
the markers and the test module's feature).

## What goes green
work-queue#r19-r24, with a fixture project in a temporary directory (two feature files, three work-items at drafted,
claimed and green). This repository's own `tests/conftest.py` registers the plugin, so i10's formulated and unbuilt
scenarios are expected failures here too.

## Files, roughly
New `scripts/work_expectations.py`; `scripts/work` (plugin command); `tests/conftest.py`; step definitions.
~~~~~~
