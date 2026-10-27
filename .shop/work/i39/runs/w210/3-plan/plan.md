# Plan of w210: supervision r135, r136 (second plan, after the answers of 2026-10-27)

From the research notes (`.shop/work/i39/runs/w210/1-research/notes.md`), the first plan
(`.shop/work/i39/runs/w210/2-plan/plan.md`), the capability, the proposal `.shop/work/i39/supervision.md` (its
Answers are the rulings cited below), and the work-item's own Answers of 2026-10-27, which settle the first plan's two
questions. This plan keeps the first plan's decisions 1–7, changes decision 8 (the order of the integrate round's
end) to fit the r135 answer, and adds decisions 9 and 10.

## 1. What goes green

- **supervision#r135**, "the lines an integrate round gives into an upstream are raised with `work request`, raised for
  the request the initiative fulfils and with its delegation" (features/supervision.feature:1445). It is red today
  because the step at line 1448 has no definition, and nor do lines 1451 and 1452. In the code, the integrate branch of
  `Rounds.run_round` never reads the result's `requests`, and `work request` has no `--raised-for`: it is refused with
  exit 2 (notes, probe row 1, defect D1).
- **supervision#r136**, "a formulated capability-proposal whose integrate round raised the lines of a request into an
  upstream gets no work-item while that request is not delivered" (features/supervision.feature:1163). It is red today
  because the Given at 1165 (two formulated proposals) has no definition, and nor do 1166, 1167 or the Then at 1170. In
  the code, `Drafts.draft_proposals` drafts every formulated proposal, and nothing writes or reads a record of raised
  requests for it.
- Retires: none. The work-item has no `## Retires`.

## 2. Where the change lands

- `scripts/supervise_raise.py` (new). It does the raising: for each `requests` entry of an integrate round's result,
  it finds the upstream's repository, writes the lines file, runs `work request` there and gives back the request id
  or work's reason for refusing. It writes this context's record lines, and it reads whether a proposal is held under
  r136. It is a new module because this is a new concern (CLAUDE.md).
- `scripts/supervise_rounds.py`. In the integrate branch of `run_round`, the raise comes after the r96 and r107 checks
  and before any proposal is written or committed (decision 8). A failed raise ends the run as decision 9 says. The
  record goes into the round's commit through the existing `also` list.
- `scripts/supervise_draft.py`. `draft_proposals` skips a formulated proposal that r136 holds (decisions 6, 7, 10).
- `scripts/supervise.py`. `Run.commit` and its call site change only if the record cannot travel through `also`. The
  file has 16 lines of room.
- `scripts/workqueue_request.py`. `request()` takes a raised-for. It is written as `raised_for` in the upstream's
  request (requests r29) and, like `--thread`, counts as naming where the request comes from (requests r31, r44).
- `scripts/work`. Adds `--raised-for` to the request subparser, passed through by `cmd_request`.
- `CLAUDE.md`. Adds a module-map row for `scripts/supervise_raise.py`.
- `tests/scenarios/supervision_raise_steps.py` (new). Holds the Givens at 1165–1167 and 1448 and the Thens at
  1451–1452 and 1170.
- `tests/scenarios/supervision_proposal_steps.py`, `supervision_integrate_steps.py`, `supervision_request_steps.py`.
  Each step that sits better beside an existing one goes there instead: the two-proposal Given beside `formulated`,
  the integrate Given with `requests` reusing `entry`, and the "q2 in catalogue … raised by i1" Given.
- `tests/scenarios/test_supervision.py`. Imports the new step module (34 lines of room).
- `tests/scenarios/spec_integration_steps.py`. Added to the researcher's set; see part 4.

Removed from the researcher's set, as in the first plan:
- `scripts/workqueue_list.py`. The record keeps the fields `waiting` reads and gains one, which `waiting` ignores.
- `scripts/model.lp` and `scripts/model_requests.py`. The model check of a raised-for request (v17) is
  design-model-check r120, which belongs to w209.

## 3. Decisions

1. **w210 builds `--raised-for` (requests r29).** The Then at 1452 cannot pass without it, and no other work-item
   accepts requests#r29. Its behaviour comes from requests r29, r31 and r44. The value is written as `work run` gives
   it.
2. **Where the lines come from.** They come from the integrate result's `requests`: one entry per upstream, with an
   `upstream` id and its `lines`, in the form `supervise_brief.REQUEST_LINES` asks for (spec-integration r44). An
   entry whose lines list is empty raises nothing. A result with no `requests` raises nothing and runs as it does
   today.
3. **The upstream's repository** is the directory above the upstream's published spec, as `Briefs.upstreams` reads it
   from `## Upstreams` in `spec/index.md`. `work request` runs there with `--root`. This rests on r135 ("with
   `work request`") and on design-decision requests-written-through-work. The lines file is passed as an absolute
   path, because `--lines` is resolved against the process's working directory (notes, probe row 8). It is kept in
   the integrate round's stage directory beside its result (design-decision worker-results-are-files).
4. **The arguments of the raise.**
   - `--from` is this context's id from `spec/index.md`.
   - `--raised-for` is the request the initiative fulfils, as `fulfils` in `initiative.md` gives it (r135).
   - `--delegation` is that request's delegation, read the way `Answers.delegation` reads it, and left out when the
     request gives none. This rests on the proposal's ruling of 2026-10-27, "a delegation always passes upstream as a
     flag".
   - The title names the initiative and the upstream. The wording is the implementer's; no scenario reads it.
5. **This context's record.** Each request raised adds one line to `.shop/work/<initiative>/raised.jsonl`. The line
   has the fields `waiting` reads for work-queue r39: the upstream, the request id from `work request`'s output, the
   initiative, and status `open`. It also has the integrate round's stage directory, which ties the request to the
   proposals that round wrote. This rests on the proposal's ruling of 2026-10-27, "r135 ties the raised lines to the
   proposal whose integrate round gave them". The record is committed on the initiative branch in the round's one
   commit with its proposals (r91). An uncommitted file under `.shop/work/` would make the next run refuse (r46).
6. **Which proposal r136 holds.** A formulated proposal is held when the integrate round that wrote it has a record
   line whose request is not `delivered`. The round is found through the drafts path that r108 already reads from the
   proposal. This rests on r136 and on the proposal's ruling of 2026-10-27, reading 2. In the scenario at 1165–1171,
   p2 is drafted and p1 is not.
7. **"Not delivered" is read from the request itself**, meaning its status in the upstream, read with `work`'s own
   reader at the upstream's root. It is not read from the record's last line, which nothing updates (notes §5). This
   rests on r136, which names the request's status, and on requests r29, which puts the request in the upstream. The
   gate does not write to the record.
8. **Order at the end of the integrate round (changed).** First the r96 and r107 checks on the change list. Then the
   raise of every `requests` entry. Only when every raise has succeeded are the proposals written and committed with
   the record (r92, r91). A round that r96 or r107 ends in an error therefore raises nothing. The raise also comes
   before anything of the round is committed or pushed, which decision 9 needs. This rests on the work-item's answer
   of 2026-10-27 to r135, reading C.
   Today the round's branch is merged (supervise_rounds.py:129) before the result is read, and that merge is a commit
   that is not yet pushed. The implementer may either move the raise and its checks ahead of the merge, or keep the
   merge and undo it when the raise fails. Either way, a failed raise leaves the initiative branch at the head it had
   before the round.
9. **A failed raise.** A raise fails when `work request` refuses or errors: no repository that keeps requests at the
   Upstreams path, a line not in strict form, a blank delegation, or any other non-zero exit. Then `work run`:
   - writes no capability-proposal, records nothing, and commits and pushes nothing from the round;
   - leaves the initiative branch at its head before the round, with the round's worktree and branch removed;
   - leaves `.shop/work/` as its last commit has it, so the round's stage directory and its `log.jsonl` lines are not
     left behind uncommitted, which r46 would otherwise refuse on the next run;
   - keeps the initiative's or proposal's status (r86, r143);
   - exits with an error that names the round, the upstream and work's reason, as r10 does.
   On the next `work run` the round runs again: the initiative is still `started` with neither a proposal nor a
   work-item (r93). This rests on the work-item's answer of 2026-10-27 to r135, reading C.
10. **An upstream request that cannot be read is held.** If the request a record line names cannot be read when r136
    is checked, the proposal is held and gets no work-item. That covers no checkout at the Upstreams path, no request
    file there, and a file `work` cannot read. This rests on the work-item's answer of 2026-10-27 to r136, reading A.
    No question is written and no error is raised, so the proposal stays `formulated` and the run's other transitions
    go on.

## 4. Tests the decisions break

- `tests/scenarios/spec_integration_steps.py`, `approved_note` and `names_upstream` (spec-integration @r44, feature
  line 6). Its round gives `requests` into billing at `../billing-ctx/spec`, a directory that holds only a spec, with no
  git and no `.shop/work/`. Under decisions 3 and 9 the raise there fails, so that `work run` would now write no
  proposal and exit with an error. Rewrite: its Givens make `../billing-ctx` a repository that keeps requests, meaning
  a git repository with its spec committed and a `spec/index.md` that gives billing's id. The lines it gives are in
  strict form, so the raise succeeds. Its Thens are unchanged, because they read the brief and the kept result. This
  is not verified by a run: the scenario cannot be collected under `--work-item w210`.
- `supervision_proposal_steps.py` `two_drafted` (feature line 1155, r72): kept. There is no record, so nothing is
  held (checked by reading; notes §4).
- `supervision_integrate_steps.py` `proposals_written`: kept. It counts only the `.md` files added, and the record is
  `.jsonl`.
- The integrate scenarios whose round gives no `requests` (r92, r96, r107, r140–r148): kept, by decision 2. A round
  with no `requests` raises nothing, so their order and commits are unchanged.
- `tests/scripts/test_workqueue_list.py`: kept. The record gains a field that `waiting` ignores.
- `features/requests.feature` raised-for rows (@r29, @r31, @r44) may go green as a side effect of decision 1; see
  part 5.

## 5. Open cases

- One integrate round that gives lines into an upstream and writes several proposals. Decision 6 holds all of them;
  no scenario pins this.
- One round giving lines into two upstreams where the second raise fails after the first has succeeded. The first
  request is already written and committed in its upstream, and decision 9 commits nothing here. The next round
  raises it again.
- The same upstream named twice in one result's `requests`.
- A proposal drafted anew by a later integrate round (r140–r142): which round's raised requests hold it then, and
  whether a failed raise in such a round is retried on the next run, since that round is started by r140 and not by
  r93.
- What happens to the failed round's session transcript and stage directory, which decision 9 leaves uncommitted.
- requests @r29 and @r31 passing under `--whole-suite` while r122 counts them as expected to fail, if xfail is strict.
- The raise's commit lands in the upstream's checkout and is never pushed (notes §5). r35 covers only this context's
  branch.
