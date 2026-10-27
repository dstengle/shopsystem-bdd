# Plan of w210: supervision r135, r136

From the research notes (`.shop/work/i39/runs/w210/1-research/notes.md`), the capability, the proposal
`.shop/work/i39/supervision.md` (its Answers are the rulings cited below), requests r29/r31/r44, spec-integration r44,
work-queue r39 and design-decisions 0067 (requests-written-through-work) and 0055.

## 1. What goes green

- **supervision#r135**, "the lines an integrate round gives into an upstream are raised with `work request`, raised for
  the request the initiative fulfils and with its delegation" (features/supervision.feature:1445). Red today because the
  step at line 1448 is undefined, and lines 1451 and 1452 after it are too. In the code, `Rounds.run_round`'s integrate
  branch never reads the result's `requests`, and `work request` has no `--raised-for`: the probe shows it is refused
  with exit 2 (defect D1).
- **supervision#r136**, "a formulated capability-proposal whose integrate round raised the lines of a request into an
  upstream gets no work-item while that request is not delivered" (features/supervision.feature:1163). Red today because
  the Given at 1165 (two formulated proposals) is undefined, and so are 1166, 1167 and the Then at 1170. In the code,
  `Drafts.draft_proposals` drafts every formulated proposal and reads no record of raised requests, and nothing writes
  `raised.jsonl`.
- Retires: none. The work-item has no `## Retires`.

## 2. Where the change lands

- `scripts/supervise_raise.py` (new): the raising. For each `requests` entry of an integrate round's result it finds the
  upstream's repository, writes the lines file, runs `work request` there and appends this context's record line. It also
  holds the r136 reading of whether a proposal's raised requests are all delivered. It is a new module because this is a
  new concern (CLAUDE.md).
- `scripts/supervise_rounds.py`: the integrate branch of `run_round` calls the raising once the change list has been
  read, and puts the record into the round's commit.
- `scripts/supervise_draft.py`: `draft_proposals` skips a formulated proposal that the r136 reading holds.
- `scripts/supervise.py`: `Run.commit` and its call site, only if the record has to go through `also`. It has 16 lines
  of room.
- `scripts/workqueue_request.py`: `request()` takes a raised-for. It writes it as `raised_for` in the upstream's request
  (requests r29) and counts it, like `--thread`, as naming where the request comes from (r31, r44).
- `scripts/work`: `--raised-for` on the request subparser, passed through by `cmd_request`.
- `CLAUDE.md`: a module-map row for `scripts/supervise_raise.py`.
- `tests/scenarios/supervision_raise_steps.py` (new): the Givens at 1165–1167 and 1448, and the Thens at 1451–1452 and
  1170.
- `tests/scenarios/supervision_proposal_steps.py`: the two-proposal Given, if it fits better beside the existing
  `formulated` step.
- `tests/scenarios/supervision_integrate_steps.py`: the integrate-round Given that adds `requests`, if it reuses `entry`
  there.
- `tests/scenarios/supervision_request_steps.py`: the step "q2 in catalogue … raised by i1 for q1, awaiting-upstream",
  if it fits there.
- `tests/scenarios/test_supervision.py`: the import of the new step module.
- `tests/scenarios/spec_integration_steps.py`: added. See part 4.

Removed from the researcher's set:
- `scripts/workqueue_list.py`. The record keeps the fields `waiting` reads and only gains one more, which `waiting`
  ignores.
- `scripts/model.lp` and `scripts/model_requests.py`. v17 for raised-for is design-model-check r120, which is w209's.

## 3. Decisions

1. **w210 builds `--raised-for` (requests r29).** r135's Then at 1452 cannot pass without it, and no other work-item
   accepts requests#r29. Its behaviour is given by requests r29, r31 and r44. Nothing is chosen here, only the order of
   work. The value is written as `work run` gives it.
2. **Where the lines come from.** They come from the integrate result's `requests`: one entry per upstream, an
   `upstream` id and its `lines`, the form `supervise_brief.REQUEST_LINES` asks for (spec-integration r44). An entry
   whose lines list is empty raises nothing.
3. **The upstream's repository** is the directory above the upstream's published spec, as `Briefs.upstreams` reads it
   from `spec/index.md`'s `## Upstreams`. `work request` runs there with `--root` (r135 says "with `work request`";
   0067 says a request is written only through `work`). The lines file is passed as an absolute path (probe row 8) and
   kept in the integrate round's stage directory beside its result (design-decision/worker-results-are-files).
4. **The arguments of the raise:**
   - `--from` is this context's id from `spec/index.md`.
   - `--raised-for` is the id of the request the initiative fulfils, as `initiative.md`'s `fulfils` gives it (r135).
   - `--delegation` is that request's delegation, read as `Answers.delegation` reads it. If the request gives none, the
     option is not passed. Basis: the ruling of 2026-10-27 in the proposal's Answers, "a delegation always passes
     upstream as a flag". Where there is none, none passes.
   - The title names the initiative and the upstream. Its wording is the implementer's; no scenario reads it.
5. **This context's record.** For each request raised, one line goes into `.shop/work/<initiative>/raised.jsonl`. It
   has the fields work-queue r39's `waiting` reads (upstream, request id from `work request`'s output, initiative,
   status `open`), plus the integrate round's stage directory. That last field ties the request to the proposals the
   round wrote. Basis: the ruling of 2026-10-27, "r135 ties the raised lines to the proposal whose integrate round gave
   them". The record is committed on the initiative branch in the integrate round's commit. r7 governs only work-item
   transitions, and an uncommitted `.shop/work/` file would make the next start refuse (r46).
6. **Which proposal r136 holds.** A formulated proposal is held when the integrate round that wrote it has a record line
   whose request is not `delivered`. The round is found through the drafts path r108 already reads from the proposal.
   Basis: r136 and the ruling of 2026-10-27, reading 2: only the proposal the raised lines belong to. In 1165–1171, p2
   is drafted and p1 is not.
7. **"Not delivered" is read from the request itself,** that is, its status in the upstream, read through `work`'s own
   reader at the upstream's root. It is not read from the record's last line, which nothing updates (notes §5). Basis:
   r136 speaks of the request's status, and requests r29 puts the request in the upstream. The record stays as work-queue
   r39 describes it. The gate does not write to the record.
8. **Order inside the integrate round's end.** The merge comes first, then the change list and the proposals (r92,
   r107), then the raise, then one commit (r91). The raise therefore never runs for a round that r96 or r107 ends in an
   error.

The case of a raise that fails is not decided here. It is the first question in the result.

## 4. Tests the decisions break

- `tests/scenarios/spec_integration_steps.py`, `approved_note` and `names_upstream` (spec-integration @r44, feature line
  6). Its round gives `requests` into billing at `../billing-ctx/spec`. That directory holds only a spec: no git and no
  `.shop/work/`. Under decisions 3 and 5, `work run` now raises into it, and the raise fails. The fix is to rewrite the
  Givens so that `../billing-ctx` is a repository that keeps requests: a git repository with its spec committed, and
  `spec/index.md` giving billing's id. The raise then succeeds. The Thens stay as they are, because they read the brief
  and the kept result. Unverified by run: the scenario is not collectable under `--work-item w210`.
- `supervision_proposal_steps.py` `two_drafted` (feature line 1155, r72): kept. There is no record, so nothing is held
  (checked by reading, notes §4).
- `supervision_integrate_steps.py` `proposals_written`: kept. It counts only added `.md` files, and the record is
  `.jsonl`.
- `tests/scripts/test_workqueue_list.py`: kept. The record gains a field that `waiting` ignores.
- `features/requests.feature` @r29, @r31, @r44 raised-for rows: they may go green as a side effect of decision 1. See
  part 5.

## 5. Open cases

- One integrate round that gives lines into an upstream and writes several proposals: decision 6 holds them all. No
  scenario pins this.
- A proposal drafted anew by a later integrate round (r140–r142): which round's raised requests then hold it.
- The same upstream named twice in one result's `requests`.
- The upstream's request cannot be read when r136 is checked: no checkout at the Upstreams path, or no request file.
  This is the second question in the result.
- requests @r29 and @r31 passing under `--whole-suite` while r122 counts them as expected to fail, if xfail is strict.
- The raise's commit lands in the upstream's checkout with no push (notes §5). r35 covers only this context's branch.
- A line the round gives that is not in strict form: `work request` refuses it (probe row 6), which leads into the first
  question.
