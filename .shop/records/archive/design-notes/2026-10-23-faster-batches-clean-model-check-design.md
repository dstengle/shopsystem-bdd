# Faster batches and a clean model check (i23)

Source: the analysis of i22's batch (.shop/records/2026-10-23-i22-analysis.md, measurement
2026-10-23-i22-rulings-round-trips-query-output), the analysis of every `model check` problem (2026-10-23; 168
violations, 30 warnings, 43 file problems), and branch review 2 of i22 (its Minor observations). The person,
2026-10-23: "Set up an initiative to make all of these improvements." Drafting decisions are delegated to the
coordinator; the choice on decision 0030 (part 6) is the person's.

## 1. supervision: independent work-items side by side

i22's 47 stages ran one at a time: 111 minutes of worker time, 64 of them research and planning, which change nothing
in the checkout. `work run` starts the research and plan stages of every work-item that can make a transition at once,
up to a limit of workers set in `.shop/delivery.toml` (a default such as 4). Implementers also run side by side, each
in its own worktree; their merges into the initiative branch stay one at a time, in the order the implementers end,
each with the suite run on the merge as today. A work-item whose `blocked_by` or `depends_on` is not yet green waits,
as today. Measured on the next batch: the stages' span against their summed time.

## 2. Drafting: what stopped i22's work-items

- Retires at drafting: when the delivering-an-initiative skill drafts a work-item, it lists under `## Retires` each
  scenario tagged `@deprecated` that carries a requirement tag the work-item accepts (the formulator deprecates the old
  scenario of a changed line). In i22 a missing Retires stopped or flagged five work-items and was both Critical
  findings of branch review 1.
- Every scenario the initiative's formulation added or reworded is accepted by some work-item: i22's reworded @r4
  supervision scenario was accepted by none, and every other work-item's suite failed on it until w91 merged. The
  check: `model check` reports a scenario in a formulated proposal's feature file whose requirement no work-item of the
  initiative accepts, or the skill refuses to draft without one.
- Work merged outside `work run` gets a task review: the skill says so (every fix-now finding of i22's branch review 1
  came from work that had none). With `work answer` and kept branches (i22) the hand-merges should not recur.

## 3. batch-measurement: what i22 left that measure refused

- A stage whose `session.json` is empty (a worker killed) is measured without its session's figures, and named, not a
  refusal of the whole measurement.
- A transcript line holding U+2028 or another Unicode line break inside a JSON string is read as one line
  (`measure_read.py` splits on `\n` only).
- Branch review 1's coupling note: each stage's transcript path recorded in its `session.json` when the stage runs, so
  round trips do not depend on Claude Code's private store layout.

## 4. design-model-check: the check's own gaps

- v_w4 double count: `model_work.py` writes an `accepts` fact only where a scenario exists, so a work-item whose lines
  have no scenario reads as having no acceptance (5 rows besides its file problems). Write it from the field.
- w_unserved_cap says nothing when the context has no job nodes (18 warnings here, every capability).
- r27 leaves out a retired id accepted by a green work-item (history: w50 accepts work-queue#r2).
- model.lp:55 names capability-proposal statuses the file form refuses (built, delivered, ruled, refused): drop them.

## 5. Small defects model check and review 2 found

- v_k6: i22's proposals `answers` and `open-findings` each argue several capabilities; split them, one a capability.
- v_s2: features/migration-tools.feature's two scenarios tagged @r4 @r5 and @r9 @r5; drop @r5 and the clause of
  their title and Then it pins (r5 has its own five scenarios). Through formulating-features.
- From i22's branch review 2: an empty `.shop/plugin-version` tested again (N1); `work answer`'s one-line refusal comes
  before the status and log refusals, or the scenario says which wins (N2); U+2028 and other line breaks count as a
  newline in an answer (N3); a test for `measure_read.moment` with a "Z" time (N4).
- `tools install` pins the ruff it installs, since ruff.toml selects codes by name (review 1's coupling note).

## 6. The workflow capabilities' scenarios (the person's choice)

Decision 0030 gives the ten workflow capabilities (spec-integration, spec-migration, spec-consistency, review,
delivery, formulation, red-green, code-research, planning, trials) Gherkin scenarios run as headless `claude -p`
fixture sessions; decision 0043 puts them under pytest-bdd with `@fixture`. The harness was never built, so their 150
lines are v_s3, nine closed initiatives are v_d1, and five green i10 work-items are file problems. Either:

- A, keep 0030: bring the harness into the repository (tests/workflow/, the `fixture` marker), write the ten feature
  files, and reopen the nine initiatives or move their backlog here; or
- B, supersede 0030 with its rejected alternative: the ten are guarantees, checked by `measure` on real batches, as
  role-boundaries is; v_s3 and r27 leave guarantees capabilities out, and their proposals become `formulated`.

## Not in this initiative

- A time limit on a worker (observation 2026-10-23-hung-worker): the person deferred it ("leave that for later").
