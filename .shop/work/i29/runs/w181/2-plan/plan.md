# Plan of w181: an initiative done, its records committed, change lists checked, kept drafts given to gate and apply

Work-item: .shop/work/i29/w181.md, under supervision, accepts supervision#r105-r109. No `## Retires`, no `## Rulings`.

## 1. What goes green

All in features/supervision.feature, bound by tests/scenarios/test_supervision.py. Each is red today at an undefined step (notes §1); the code gaps behind them are below.

- **supervision#r107**, "a change list naming a capability that neither spec/capabilities/ nor the round's drafts have gives no capability-proposal for it, and `work run` exits with an error naming it" (line 1315). Red: no step for "spec/capabilities/ holds no capability nowhere", for the integrate Given "… having written no draft of nowhere under its drafts path", or for the three Thens. In code, `supervise_change.write_proposals` writes a drafted proposal for any name, with no error (probe P1).
- **supervision#r108**, Outline "the <kind> round of a capability-proposal is given the path of the kept drafts of the integrate round that wrote the proposal", examples gate and apply (line 1327). Red: no step for "p1 was written from the change list of i1's integrate round, whose drafts are kept at …", and none for the Then "the <kind> round for p1 was given the path …". In code, `supervise_brief.brief` gives gate and apply rounds no drafts path. The proposal's body names the integrate stage directory, not its `drafts/round-<m>/`.
- **supervision#r106**, "once the initiative's measurement and analysis record are written, they are committed on the initiative branch" (line 1342). Red: no step for the Then "the initiative branch has a commit of i1's measurement and i1's analysis record" or for "nothing under .shop/records/ is left uncommitted". In code, `Analyses.analyse` copies the record into `.shop/records/` and commits nothing.
- **supervision#r105**, "an initiative whose work-items are green or withdrawn, whose branch review lists nothing to fix now, whose measurement and analysis record are committed and whose requests are delivered is set done" (line 1351). Red: no step for "i1 is started and its work-items w1 is green and w2 is withdrawn", for the q2 Given, or for "i1 is done". In code, `pull_through` never sets the initiative done.
- **supervision#r109**, "an initiative set done is committed on the initiative branch" (line 1360). Red: the same Givens as r105, and no step for its two Thens. In code, nothing on the run path commits a done.

No deprecated scenario is retired.

## 2. Where the change lands

Production:
- `scripts/supervise_change.py`: the check of each named capability against `spec/capabilities/` and the integrate round's kept drafts (r107). The proposal's sentence naming its drafts now names the round's kept `drafts/round-<m>/` directory, not the stage directory (r108).
- `scripts/supervise_rounds.py`: `run_round` for integrate runs the check before any proposal is written. It writes the known capabilities' proposals and refuses naming each unknown one (decision 2). It hands `write_proposals` the drafts directory (decision 4).
- `scripts/supervise_brief.py`: gate and apply briefs get a "Drafts path:" line with the proposal's kept drafts path, and that path joins the brief's Read list (r108).
- `scripts/supervise_analysis.py`: `analyse` commits the measurement and the record it copied, then pushes (r106, r38). It reports which files it committed (decision 5).
- `scripts/supervise_done.py` (**new**): the run path's done. It holds the condition of r105 and the transition and its commit (r105, r109). It is a part of `supervise.Run`, like `Analyses`. It is a new module because `supervise.py` has 40 lines of room (notes §7) and the initiative's being done on a run is a concern of its own (CLAUDE.md: a new concern gets a new module).
- `scripts/supervise.py`: `Run` takes the new part. `pull_through` calls the done step after the analysis branch (only a few lines).
- `scripts/workqueue_done.py`: the existing condition (work-items and requests) gets a public name that `supervise_done` calls. What it decides does not change, so the command path (work-queue r23) is untouched (decision 1).
- `CLAUDE.md`: a module-map row for `scripts/supervise_done.py`. This file is added to the researcher's set because of decision 7.

Tests (tests/scenarios/):
- `supervision_integrate_steps.py`: the r107 Givens and Thens.
- `supervision_proposal_steps.py`: the r108 Given that writes p1's drafts sentence and its kept drafts directory, and the Then that reads the round's brief for the path.
- `supervision_given.py`: the r108 apply-example status Given, only if the existing awaiting-answer Given (the r83 one, line 1209, same text) does not already match it. The implementer checks this first.
- `supervision_analysis_steps.py`: the r106 Thens (the commit of measurement and record, and nothing left uncommitted under `.shop/records/`).
- `supervision_done_steps.py` (**new**): the r105 and r109 Givens and Thens: "i1 is started and its work-items …", the q2 request Given, "i1 is done", the commit of i1 with its status done, and i1's file not left uncommitted. It is a new module because `supervision_given.py` has 41 lines of room.
- `test_supervision.py`: one star-import line for the new steps module.

Read only: `scripts/supervise_drafts.py` (the glob of kept drafts), `scripts/workqueue.py`, `scripts/workqueue_request.py`, `scripts/measure_write.py` (the measurement lands at `.shop/records/measurements/<date>-<initiative>.md`).

## 3. Decisions

1. **The run path's done condition is separate from the command's.** The new condition is the existing one in `workqueue_done` (at least one work-item, each green or withdrawn, every request asked by this context that names the initiative delivered), plus two more. The two are: the kept branch review lists nothing to fix now, as `lists_nothing` reads it, and the measurement and analysis record are committed (decision 6). `_holds`, `becomes` and `mark` keep what they do. Rests on supervision#r105 (its two extra conditions are `work run`'s), and on work-queue r23, whose command path and scenarios (features/work-queue.feature :57, :75) do not have them (notes §3, §4).
2. **A change list naming an unknown capability.** `work run` checks every named capability first. It writes no proposal for an unknown one (r107). It writes a drafted proposal for each known one, as before (supervision#r92, which still holds for every other capability the list names). It then exits with an error naming each unknown capability (r107). When every named capability is unknown, the round is kept as the r96 refusal keeps it: its stage directory and drafts are committed with no proposal, so r93 starts integrate again on the next run (supervision#r91, r93, r96). When some are known, their proposals are committed with the stage directory as today, and then the run is refused. The initiative keeps `started`, which r84 already made it. Rests on supervision#r107, r92, r91.
3. **"Have" for r107.** A capability is had when `spec/capabilities/<name>.md` exists in the checkout `work run` runs on, or when any `drafts/round-<m>/spec/capabilities/<name>.md` exists under that integrate round's stage directory. This uses the same layout `supervise_drafts` globs. Rests on supervision#r107 ("the round's drafts", every round of them).
4. **The kept drafts path a proposal comes from.** It is the integrate stage directory's `drafts/round-<m>/` with the highest `<m>`, at the time `work run` writes the proposals. It is relative to the repository, with a trailing slash, as the scenario names it. The proposal's existing body sentence ("The drafts of this proposal are in …") records it. The frontmatter is not used, so the design model's checks of a capability-proposal's frontmatter are not touched. The gate and apply briefs read the path back from that sentence and give it as a "Drafts path:" line, and add it to the Read list. Rests on supervision#r108 and r91.
5. **The commit of measurement and record.** It is one commit on the initiative branch of the measurement file `measure initiative` printed and the analysis record copied into `.shop/records/`, followed by the push. It works the way `Run.commit` does (`git add`, `git commit` of those paths only, then `push`), with a message naming the initiative, its measurement and its analysis. When the analysis session wrote no record, `analyse` commits nothing; that case is in part 5. Rests on supervision#r106 and r38.
6. **"Measurement and analysis record work run has committed".** This is read from git, not from the checkout. Both an analysis record `.shop/records/*-<initiative>-analysis.md` and a measurement `.shop/records/measurements/*-<initiative>.md` must be tracked at HEAD and unmodified. Rests on supervision#r105 and notes §5 (the done step reads the commit, not the file).
7. **The done transition and its commit.** It mirrors `start_initiative`. `workqueue_done.mark` sets `done`, a log line records the initiative's move from its status to `done` by `work run`, and `Run.commit` for the initiative commits `initiative.md` and `log.jsonl` (message `work: <initiative> <before> -> done`), then pushes. It runs only after the analysis branch of `pull_through`, when the condition of decision 1 holds. Rests on supervision#r105, r109, r38.

## 4. Tests the decisions break

None, verified as follows:
- Decision 1 leaves `_holds` and `becomes` deciding as they do, so the work-queue done scenarios (features/work-queue.feature :57, :75) keep their footing. They are not run here: the shell's `--work-item w181` refuses them (notes §4).
- The r75/r76 steps in `supervision_analysis_steps.py` (`measured_after_review`, `analyst_started`, `analysis_there`, `analysis_not_there`, `measured_not`, `measured_never`) assert only whether the measurement, the record and the analyst session are there. A commit (decision 5) and a done (decision 7) change none of that.
- The scenarios naming `thing` read as having it held (notes §4). The r92 scenario at feature line 1173 names `other#r1 on other`, and whether its Givens hold `other` in spec or drafts is unverified (notes §4). Under decisions 2 and 3 that scenario breaks if they do not. If it does, the fix is in its Given step in `supervision_integrate_steps.py`, which then also writes a draft of `other` under the round's drafts path. What it asserts stays as it is: r107 makes a capability that exists nowhere an error, and the scenario's intent is two existing capabilities. The implementer runs it red/green with the r107 work.

## 5. Open cases (for the implementer to name, not to choose)

- An integrate round that kept no `drafts/round-<m>/` at all: which drafts path, if any, its proposals name, and what the gate and apply briefs then say.
- Proposals written before this change, whose sentence names the stage directory and not a `round-<m>/`.
- The analysis session cut short or writing no record. The measurement is then written but uncommitted under `.shop/records/`, which the start-of-run check (`supervise.check`, `.shop/work/` only) does not refuse (notes §6).
- A later run of an initiative whose analysis was committed earlier but whose request was not yet delivered. Whether `measure initiative` is refused (the measurement exists for the date) or writes a second one, and how the done check reads that.
- The push after the records' commit or the done's commit failing. `Run.commit`'s push is the path to follow.
- `work run` with no initiative printing an initiative it has just set done (r82 prints the initiatives it took).
