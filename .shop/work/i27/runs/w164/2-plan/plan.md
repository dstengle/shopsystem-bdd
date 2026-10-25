# plan of w164: integrate rounds carried (supervision r91-r97, r66)

From the research notes (`.shop/work/i27/runs/w164/1-research/notes.md`); code read only in `supervise_rounds.py` and
`supervise_brief.py` (where the drafts are and what the integrate brief gives), and in `supervision_rounds_steps.py`
for the r84 step that a decision breaks.

## 1. What goes green

- **supervision#r93**: "a started initiative with neither a capability-proposal nor a work-item is given to an integrate
  round with the accepted lines of the request it fulfils". Red: its Given is undefined, and `due` gives an integrate
  round only to a `proposed` initiative (probe c7: no round, exit 0).
- **supervision#r96**: "an integrate round that ends DONE without a change list ends `work run` with an error naming the
  round". Red: Given, the "gives DONE with no change list" step and the Then are undefined, and `round` takes any DONE
  integrate (probe c3: exit 0).
- **supervision#r91**: "the drafts of an integrate round that <ending> are kept on the initiative branch" (both rows: DONE
  with a change list naming thing; ends at its turn limit). Red: the drafts step, "every other round ends" and the Then
  are undefined, and the drafts are in no commit on either ending (probes c5, c6).
- **supervision#r92**: "an integrate round's change list gives one drafted capability-proposal for each capability it
  names, with what it adds, changes and removes on that capability". Red: the change-list Given, "every other round
  ends" and the Then are undefined, and no code writes a capability-proposal (probe c4).
- **supervision#r94**: "an initiative with no work-item gets no branch review, though its branch holds a commit no kept
  branch review has read". Red: its two Givens are undefined, and `pull_through`'s all-green test is true over no
  work-items, so a review starts (probes c1, c2).
- **supervision#r97**: "an initiative with no work-item is not measured". Red: the Given (r94's) and the Then are
  undefined, and `analyse` runs on the same empty test (probe c1).
- **supervision#r95**: "`work run` started with no initiative runs the integrate, apply and formulate rounds of different
  initiatives one at a time". Red: the i2/i3 Givens, the slow-rounds Given and both Thens are undefined, and nothing
  serialises rounds across initiatives (`run_all` threads, only the worker semaphore).
- **supervision#r66** (changed): "`work run` started with no initiative takes every initiative that is neither done nor
  abandoned through its transitions, ...". Passes today and must stay green: its gate rounds stay side by side.
- Retired: none (the work-item has no `Retires` section).

## 2. Where the change lands

- `scripts/supervise_rounds.py`: `due` also gives the integrate round to a `started` initiative with no
  capability-proposal and no work-item that fulfils a request (r93); the integrate round's start skips the
  proposed-to-started transition when the initiative is already started; on every ending the round's drafts are
  copied from its worktree into its stage directory before the worktree goes, and committed with it (r91); a DONE
  integrate's change list is read, refused when missing (r96), and handed to the new module (r92); the r95 lock is
  held over integrate, apply and formulate rounds.
- `scripts/supervise_change.py` (new): the change list read from the integrate result, checked for its form, split by
  capability, and written as one `drafted` capability-proposal a capability (r92). A new concern, so a new module.
- `CLAUDE.md`: the module map's row for `scripts/supervise_change.py` (the file's own rule: a new concern gets a row).
- `scripts/supervise.py`: `pull_through` starts no branch review and no `measure initiative` when the initiative has no
  work-item (r94, r97); `Run` takes the cross-initiative round lock it is given, or makes its own (r95).
- `scripts/supervise_all.py`: `run_all` makes one round lock and gives it to every initiative's `Run` (r95, r66).
- `scripts/supervise_brief.py`: `integrate_lines` also names the round's drafts path and the change-list form the
  result gives (r91, r92).
- `agents/initiative-round.md`: the `integrate` kind writes its drafts under the drafts path its brief names and gives
  its change list in its result (r92, r96).
- `tests/scenarios/supervision_integrate_steps.py` (new): the integrate-round steps of r91, r92, r93, r96 ("has
  neither ...", "gives DONE with no change list", "writes spec/capabilities/thing.md under its drafts path and
  <ending>", "gives DONE with a change list that ...", "every other round ends", "names the integrate round of i1",
  the drafts and proposals Thens). New because `supervision_rounds_steps.py` has 42 lines of room.
- `tests/scenarios/test_supervision.py`: imports the new step module.
- `tests/scenarios/supervision_rounds_steps.py`: the r84 Then rewritten (part 4).
- `tests/scenarios/supervision_given.py`: r94's and r97's Given (started, p1 awaiting-answer with its question, no
  work-item).
- `tests/scenarios/supervision_review_steps.py`: "the initiative branch holds a commit of notes.txt that no kept branch
  review has read".
- `tests/scenarios/supervision_analysis_steps.py`: "`work run` ran no `measure initiative` on i1".
- `tests/scenarios/supervision_all_steps.py`: r95's i2 and i3 Givens, the slow-rounds Given and both Thens.

Removed from the researcher's set: `scripts/supervise_review.py` (the r94 guard goes in `pull_through`, beside r97's,
one condition for both); `scripts/supervise_worker.py` (the drafts are copied by the round, not by `keep_named`, and
the round lock is separate from the worker semaphore); `skills/integrating-a-proposal/SKILL.md` (the result form
belongs to the agent's `integrate` kind, which work run starts); `tests/scenarios/supervision_world.py` (helpers go
in the new step module).

## 3. Decisions

1. **The drafts path and where the drafts are kept.** The integrate brief names a drafts path, a `drafts/` directory in
   the round's run directory in its worktree. Whenever the round ends (DONE, any other outcome, an error, the turn
   limit, no result), before its worktree is removed, `work run` copies that tree into the stage directory's `drafts/`,
   each file at the same path relative to the drafts root, and commits it with the stage directory: in the round's
   closing commit on DONE, in `keep_round`'s commit otherwise. The drafts go under `.shop/work/`, never into `spec/`
   (the gate is not passed). Rests on supervision#r91, r15 and design-decision/worker-results-are-files (the worker
   writes into its stage's directory).
2. **The change list's form.** It is the result field `changes`: a list with one entry for each capability, each entry
   naming the `capability` and its `adds`, `changes` and `removes`, each a list of ids in the proposal's frontmatter
   form (`<capability>#r<n>`, `term/<term>`). Rests on design-decision/worker-results-are-files (a stage's own result
   fields) and design-decision/work-file-forms (the proposal's `adds`, `changes`, `removes`).
3. **"Without a change list."** A DONE integrate result whose `changes` is missing or empty ends without a change list
   (r96's scenario: "an integration that names no capability to change"). A `changes` that is not of decision 2's form
   is a result `work run` cannot read: an error naming the round and how it ended, the status kept, nothing written
   (supervision#r86-r88, design-decision/worker-results-are-files: "a malformed result is a failed stage").
4. **The r96 ending.** The round's commits are merged as for any DONE; the stage directory and drafts are committed
   (decision 1), no capability-proposal is written, the initiative keeps its status, and `work run` exits with an error
   naming the round by its stage directory, as the other round errors do. Rests on supervision#r96, r91,
   design-decision/exits-are-successful-or-errors.
5. **The proposals written.** For each entry, one file in the initiative's directory named after the capability, with
   the id `capability-proposal/<the initiative id's prefix>/<capability>`, `kind: capability-proposal`, `part_of` the
   initiative, `status: drafted`, the day's `date`, `argues: [<capability>]`, and the entry's `adds`, `changes` and
   `removes` (empty lists where it gives none), its body a title naming the capability and the stage directory that
   holds the drafts. All of one round's proposals are written in one commit: the round's closing commit. Rests on
   supervision#r92, design-decision/one-capability-per-proposal, design-decision/work-file-forms.
6. **The r93 round.** `due` gives the integrate round to a `started` initiative with no capability-proposal and no
   work-item whose request is in the queue, the same accepted lines as r79. Its start writes no status, logs no
   transition and makes no commit (r84 is for a `proposed` initiative only); its ending is r91/r92/r96's. Rests on
   supervision#r93, r84.
7. **No work-item, no review, no measure.** `pull_through` tests that the initiative has a work-item before both the
   branch review and `analyse`. Rests on supervision#r94, r97.
8. **The round lock.** One lock across the initiatives of a `work run`, taken by a round of the kind `integrate`, `apply`
   or `formulate` before its session starts and released after its last commit; `gate`, `intake` and answering
   sessions do not take it. It is always taken before the initiative's own git lock and before a worker slot, never
   while holding either, so no two waits cross. Rests on supervision#r95, r66 (the gate rounds stay side by side).

## 4. Tests the decisions break

- `tests/scenarios/supervision_rounds_steps.py`, `second_not_refused` (the r84 scenario "when the integrate round `work
  run` started for a proposed initiative ends DONE, ..."): its Given gives the integrate round DONE with no change list.
  Under decisions 4 and 6 the first run ends in r96's error, and the second run, the initiative now started with neither
  node, starts an integrate round again (r93) and ends in r96's error too, so its asserted exit 0 cannot hold. Rewritten
  to assert what the scenario pins: the second run was not refused over anything left uncommitted under
  `.shop/work/` (r10's refusal) and got as far as starting a round. Its Given stays as it is; the other Thens of the
  scenario hold (decision 4 commits the stage directory, and `initiative.md` is already `started` there).
- Verified sound (from the notes, part 4, and the scenarios read): the r79 and r84 scenarios on "every round ends" assert
  no exit; the r81 example with p1 awaiting-answer and no work-item still exits with an error and prints the statuses;
  r66 passes under decision 8; the review, analysis and delegation scenarios all have work-items; `no_integrate_started`
  serves proposed initiatives only.

## 5. Open cases

- A `proposed` initiative that already has a file named after a capability its change list names (or a capability named
  like `initiative`, `ledger` or a work-item).
- A change list entry naming a capability that is not in `spec/capabilities/`, or an id of another capability.
- A request in the queue whose accepted lines are none, for the r93 round.
- The r95 scenario's i1 integrate round ending DONE with no change list: whether its step gives it a change list, and
  that i1's r96 error does not stop i2's and i3's rounds.
- The gate and apply briefs naming the drafts kept in the integrate round's stage directory.
- An integrate round's drafts path left empty, or holding nothing.
