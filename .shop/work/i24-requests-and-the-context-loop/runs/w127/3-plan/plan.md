# Plan of w127: work outcome and work turn (third plan, after the r17 answer)

Accepts requests#r7, r15, r16, r17, r18. Rests on design-decision/requests-written-through-work and
design-decision/exits-are-successful-or-errors. Planned from `runs/w127/1-research/notes.md` and the second plan
(`runs/w127/2-plan/plan.md`), checked against the branch as it is now at the base.

**The branch has moved since the research.** w126 and w128 have landed. `scripts/work` already has the `request`,
`outcome`, `turn` and `resolve` subcommands. `scripts/workqueue_request.py` exists and commits every change through
`workqueue.committed`, so requests#r12 holds and the second plan's D1 ("no commit yet") is gone. `tests/scenarios/test_requests.py`
binds the whole of `requests.feature`, and three step modules exist: `requests_steps.py`, `requests_write_steps.py`
and `requests_show_steps.py`. So the notes' "no binding, invalid choice" reasons for red are out of date. The reasons
below come from reading those files, in the few places where the notes could not give them.

The answer of 2026-10-24 (Reading A) is in place: in `features/requests.feature` the r17 outline has an Examples table
with two rows, "no line outcome" and "the line outcome question". Both rows are pinned.

## 1. What goes green

- requests#r15, "outcome in the upstream's turn writes the outcome given as the line outcome of the line named". Two
  reasons it is red:
  - The shared request Given in `requests_steps.py` only knows the singular text "that has no line outcome". The
    plural "with two lines that have no line outcome" falls through to its outcome-list branch and writes a bogus
    line outcome for line 1.
  - The Then "q1 gives line 1 no line outcome" has no step.
- requests#r16, "a side writing a part of a request in the other side's turn is refused, and nothing changes". Red
  because `workqueue_request.outcome` never checks whose turn it is, so `work outcome q1 1 accepted` in the asker's
  turn writes the outcome and exits 0. The two Thens also have no steps: "the command is refused because it is the
  asker's turn" and "q1 is as it was".
- requests#r7, "turn passes the request's turn from the <side> to the <other side>", both rows (upstream→asker,
  asker→upstream). `turn` already flips the turn, but the Then "q1's turn is the <other side>'s" has no step.
- requests#r17, "turn passing a request to its asker with a line that has <line 2> sets the request's status to
  awaiting-asker", both rows ("no line outcome", "the line outcome question"). Two reasons it is red:
  - The Given "…with two lines, line 1 with the line outcome accepted and line 2 with …" matches no step. The shared
    Given's pattern expects a space after "lines", not a comma.
  - `turn` never sets `awaiting-asker`.
- requests#r18, "turn passing a request to its upstream sets the request's status to awaiting-upstream". Its Given
  already matches the shared Given. It is red because `turn`, passing to the upstream, only flips `turn` and never
  sets `awaiting-upstream`.

No Retires section, so no deprecated scenarios are retired.

## 2. Where the change lands

- `scripts/workqueue_request.py`:
  - `outcome` refuses with `Refused` when the request's turn is the asker's, naming the asker's turn. It does the
    check inside the edit it hands to `_change`, so the refusal comes before anything is written or committed.
  - `turn`, passing to the upstream, also sets status `awaiting-upstream`.
  - `turn`, passing to the asker, sets `awaiting-asker` unless every line is settled. When every line is settled, the
    existing r8/r9 branch stays as it is.
  - Docstrings name r7, r15–r18.
- `tests/scenarios/requests_steps.py`:
  - The shared request Given also reads "that have no line outcome" (plural) as no line outcomes.
  - A new Given for the per-line form "with two lines, line 1 with the line outcome <w> and line 2 with <no line
    outcome | the line outcome <w>>".
  - The Given keeps the text it wrote (in `context`), so a Then can compare against it.
  - New Thens: "<q> gives line <n> no line outcome", "<q>'s turn is the <side>'s", "the command is refused because it
    is the asker's turn" (on stderr), and "<q> is as it was" (the file is byte for byte what the Given wrote).
  - The module is 75 lines, so it has room.

Removed from the second plan's set:
- `scripts/work`: its subparsers and dispatch already exist, and `Refused` already maps to exit 1.
- `CLAUDE.md`: the `workqueue_request.py` row is already in the module map.
- `tests/scenarios/test_requests.py`: it already binds every scenario.
- `tests/scenarios/requests_turn_steps.py`: the steps join the existing `requests_steps.py`, whose concern is the
  request file and the commands that change it. That avoids a second module with the same Given.

`scripts/model_work.py` already lists the request statuses, `awaiting-*` among them, so it is not touched.

## 3. Decisions

- **D1. `work outcome` is the upstream's command, refused in the asker's turn.** The upstream writes line outcomes
  only through `outcome` and `resolve` (requests#r5), and a part written in the other side's turn is refused, with
  nothing changed (requests#r16). The refusal goes through `Refused`, which `work` turns into exit 1 with the message
  on stderr (design-decision/exits-are-successful-or-errors). The message says it is the asker's turn.
- **D2. `work turn` is never refused on whose turn it is.** It writes neither side's part, only the turn
  (requests#r7, design-decision/requests-written-through-work). The r5 and r18 scenarios show the asker running it in
  the asker's turn.
- **D3. `work outcome` writes any word, on the named line only.** This is already so in the code (requests#r15). It
  is kept, and the other lines' outcomes and `## Lines` are left as they were (requests#r4).
- **D4. Statuses `turn` sets.**
  - Passing to the upstream always sets `awaiting-upstream` (requests#r18).
  - Passing to the asker sets `awaiting-asker` when any line has no line outcome, or an outcome other than accepted,
    refused or withdrawn (requests#r17). This holds whatever the status was before.
  - Passing to the asker when every line is settled keeps the existing accepted/refused branch (requests#r8, r9,
    w128's).
- **D5. r17's cases.** Both Examples rows are pinned, per the work-item's Answer of 2026-10-24 (Reading A). The new
  Given maps "no line outcome" to no `## Outcomes` entry for line 2, and "the line outcome question" to entry
  `2. question`.

## 4. Tests the decisions break

None. What I checked:
- A grep of `tests/` for `workqueue_request`, `"turn"`, `"outcome"` and `awaiting-asker`/`awaiting-upstream` finds
  only the binding module's docstring. No test in `tests/scripts/` drives these functions.
- In `requests.feature`, the scenarios that run `outcome` all run it in the upstream's turn: r4, r12 and r15. So D1
  refuses none of them.
- The scenarios that run `turn` with every line settled (r8, r9) keep their branch. The r5 scenario (asker→upstream)
  asserts only line outcomes and resolution, which D4 leaves alone.
- The status Givens in `requests_show_steps.py` (r13, r14) do not run `turn`.

## 5. Open cases (for the implementer to name, not to choose)

- The r8 scenario "the upstream ending its turn on a delivered request with every line accepted leaves the status
  delivered" looks red in the code as read: `turn`'s settled branch sets `accepted` whatever the prior status. It is
  w128's requirement, not w127's. D4 must not change that branch's outcome for it either way. Name what the run shows.
- The exact wording of the r16 refusal, beyond naming the asker's turn.
- Whether "q1 is as it was" also checks that no commit was made, or only the file's bytes.
- `work outcome` with a line number that is not one of the request's lines (the scenarios are silent).
- `work turn` passing to the asker on a request whose status is `delivered` with a line not settled. D4 gives
  `awaiting-asker` by r17's text, but no scenario pins it.
- That the new per-line Given and the shared Given do not both match one step text (pytest-bdd's `parsers.re`
  matches the whole text). Name which step each request Given of the feature reaches.
