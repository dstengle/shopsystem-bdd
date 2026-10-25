# Plan of w170: initiatives side by side in the loop

Work-item `.shop/work/i28/w170.md`, under `supervision`, accepts supervision#r102, #r103, #r104. Planned from
`.shop/work/i28/runs/w170/1-research/notes.md` (notes) and the scenarios in `features/supervision.feature`.
No `## Retires`, no `## Rulings`.

## 1. What goes green

- **supervision#r103**: "an accepted request this context is the upstream of, that no initiative fulfils, has its
  initiative started with `work start`" (feature line 1230). Red: `StepDefinitionNotFoundError` at its first Given (the
  existing intake Given needs "its turn the upstream's, with two lines"). Behind that, `supervise_all.run_all` never
  starts an initiative: probe R103-a shows `work run` with q1 accepted and no initiative leaves `.shop/work/` with no
  initiative (notes 1, 2).
- **supervision#r102**: "an integrate round is given every requirement id another initiative's kept drafts add that
  spec/ on the branch it starts from does not hold, whatever that initiative's capability-proposal's status" (line
  1240). Red: undefined Given at the spec/capabilities/thing.md step. Behind that, `supervise_brief.integrate_lines`
  gives only the request's accepted lines, the drafts path and the change-list form; probe R102 shows the brief names
  none of the ids (notes 1, 2).
- **supervision#r104**: "the gate round of a capability-proposal is asked only for the questions on the lines and terms
  that proposal adds, changes or removes" (line 1252). Red: undefined Given "the capability thing holds ...". Behind
  that, the gate branch of `supervise_brief.brief` writes one fixed sentence and no id of the proposal; probe R104
  (notes 1, 2).

No deprecated scenario is retired.

## 2. Where the change lands

- `scripts/supervise_all.py`: `run_all` starts, with `workqueue_start.start`, the initiative of each accepted request
  this context is the upstream of that no initiative fulfils. It does this after every check has passed and before the
  initiatives are taken, so the run takes the new initiative too (r103).
- `scripts/supervise_drafts.py` (new): the requirement ids that other initiatives' kept drafts add and that spec/ on
  the round's branch does not hold (r102). This is a new concern, so it gets its own module (CLAUDE.md).
- `CLAUDE.md`: a row in the module map for `scripts/supervise_drafts.py`.
- `scripts/supervise_brief.py`:
  - `integrate_lines` adds a line that gives the round those ids (r102).
  - The gate branch of `brief` names the proposal's adds, changes, removes and terms, and asks for questions on those
    alone. It keeps the r68 sentence (r104).
- `tests/scenarios/supervision_intake_steps.py`: the r103 Givens (an accepted request no initiative fulfils, and one
  that i1 fulfils) and its two Thens.
- `tests/scenarios/supervision_integrate_steps.py`: the r102 Givens (spec on the branch; i2's and i3's kept drafts with
  their proposals) and its two Thens.
- `tests/scenarios/supervision_proposal_steps.py`: the r104 Givens (the capability's ids; p1 and p2 drafted) and its two
  Thens on p1's gate brief.

Removed from the researcher's set, with why:
- `scripts/supervise_rounds.py`: the brief works out the ids itself (decision 4), so `run_round` passes nothing new.
- `scripts/workqueue_start.py`: `work start` is not changed. D1 to D3 are met on `work run`'s path by decisions 1 and
  2, not in `start`.

A step module that would go over 300 lines is split into a new `supervision_*_steps.py` instead.

## 3. Decisions

1. **When the start happens (r103, r10).** `work run` with no initiative makes every check it makes today (each open
   initiative's `Run.check`, each intake's `check`) and only then starts the new initiatives. The new initiatives join
   the runs taken in this same `work run`, each checked like the others, before anything moves. It rests on
   supervision#r10: a refusal changes nothing. Probe R103-c shows that an initiative started by hand is taken through
   integrate onward, and the one `work run` started is taken the same way (supervision#r79, #r84).
2. **Refusals when no initiative is open (r10).** When there is no open initiative, `work run`'s path to the start still
   refuses what `Run.check` refuses, before starting anything: a worker's marker (`SHOPSYSTEM_WORK_RUN_WORKER`), a
   detached HEAD, and loose changes under `.shop/work/`. This keeps D1 (a start inside a worker) and D3 (a commit on a
   detached HEAD) out of `work run`. It rests on supervision#r10. `work start` by hand keeps its behaviour today; this
   work-item does not cover it.
3. **What "no initiative fulfils it" means (r103).** It means no initiative under `.shop/work/`, of any status, has a
   `fulfils` that names the request. The id is matched the way `supervise_rounds.due` matches it (the last path
   segment). This is r103's literal wording, and it keeps D2 (a second initiative for one request) out of `work run`.
   The push is the one `push_unpushed` already makes later in `run_all`; no push is added.
4. **Where the ids of r102 come from (supervision#r102, #r91).** "Kept drafts" means the drafts r91 keeps: the
   capability files under each other initiative's integrate stage directories (`runs/<initiative>/<k>-integrate/
   drafts/spec/capabilities/<capability>.md`). The capability-proposal's `adds` is not the source, which is why the
   proposal's status does not matter, as the scenario's title says.
   - Only the drafts of the initiative's last integrate stage directory count, because those are the drafts its
     proposals were written from (r92).
   - An id "added" by a draft is a `[r<n>]` requirement id the draft holds that `spec/capabilities/<capability>.md` on
     the branch the round starts from does not hold. That branch is the checkout the brief is written from, which is
     the tree the round's worktree is made from. This is "not yet applied" as the scenario's title reads it: an id i2
     applied on its own branch still counts when i1's branch lacks it.
   - Terms are not given; r102 names requirement ids only.
   - The round's own initiative is skipped.
   - The brief gives the ids as `<capability>#r<n>`, in a line of their own that says they are taken by other drafts.
     When there are none, the line says so or is left out (the implementer chooses).
5. **What the gate brief names (supervision#r104, #r92).** The ids come from the proposal's frontmatter `adds`,
   `changes` and `removes`, as `supervise_change.write_proposals` writes them: `<capability>#r<n>` and `term/<term>`.
   - The brief lists them under adds, changes and removes, and asks for questions on those ids and terms only.
   - The read list stays as it is: the proposal file and its stage directories. No capability file is added, so the
     brief itself names no other id of the capability and no other proposal's id. This settles the researcher's open
     reading (notes 3, read-list row) toward "the brief lists the ids". r104 only constrains what the round is asked
     for, and adding a read is not needed for that.
6. **How `work start` is seen to have run (r103 Then).** The scenario's Then observes the effects only `work start`
   produces (notes 5): its commit "work: start i<n>, fulfilling q<n>" and an `initiative.md` whose `fulfils` names the
   request. The step reads those, not a call record.

## 4. Tests the decisions break

None. What was verified:
- Notes 4 lists the tests that drive `work run` with no initiative. None has an accepted request that no initiative
  fulfils, except r103's own.
- I read the two scenarios the researcher had not read:
  - Line 1049 (r66): its initiatives fulfil no accepted request left open.
  - Line 1142 (r92): q1 and q2 are each fulfilled by i1 and i2, so decision 3 starts nothing. Its Then asserts the
    proposals' `adds`, which decision 4 does not touch. Only i2's integrate brief may gain a line, and only when the stub
    leaves drafts.
- `supervision_rounds_steps.py` `gate_brief_asks` checks "questions", "readings" and "recommended". These stay, because
  decision 5 keeps the r68 sentence.
- `integrate_started` asserts "Line 2 text." is absent. Decision 4 adds ids only.
- `supervision_integrate_steps.py` `proposals_written` is unchanged, since the proposal form does not change.
- `work_queue_start_steps.py` is unchanged, since `work start` does not change.

## 5. Open cases

- An accepted request whose only initiative is `abandoned`: by decision 3 it gets no new start. The scenario is silent,
  so the implementer names it in the report.
- A request that an intake round in the same `work run` turns `accepted`: it is started on the next `work run`, or once
  the intakes are taken. The scenarios are silent.
- `work start` refusing inside `work run` (no `spec/index.md`, no bounded-context id, a bad name): how that refusal is
  told and what the exit is, under r10.
- Several accepted requests with no initiative: the order they are started in and the initiative numbers they get.
- An initiative that is done or abandoned but has kept drafts whose ids spec/ on this branch does not hold: decision 4
  counts them. Whether that is wanted goes in the report.
- A draft capability file that matches no `spec/capabilities/` file (a new capability): every id in it counts as added.
- An initiative whose drafts are kept on a branch other than the checkout's.
