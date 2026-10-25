# Plan of w193: fix the findings of branch review 1 of i31

w193 accepts supervision r111 to r116, r70 and r83. Its findings file
(`.shop/work/i31/runs/branch-review/1/findings.md`) has one finding to fix now: **Finding 1**. r114 is met only against
the stand-in, because the real apply round never gives a change list. Findings 2 to 10 are observations or drops, and
this plan does not take them (see part 5).

## 1. What goes green

The research notes (§1) ran every accepted node by id, and all of them pass today. They are:

- supervision#r111: "an initiative that a work-item's transition leaves able to be done is set done before work run ends"
- supervision#r70: "a capability-proposal whose every question has an answer is given to an apply round with its answers"
- supervision#r116: "a capability-proposal whose every question from its formulate round has an answer is given to a formulate round with the answers"
- supervision#r114: "when the apply round `work run` started for a capability-proposal ends, the proposal's adds, changes and removes are written from the change list the round applied"
- supervision#r83: "when the formulate round … ends without giving a question, the proposal is formulated"
- supervision#r112: "when the formulate round … gives questions, each is written under the proposal's ## Questions"
- supervision#r113: "when the formulate round … gives a question, the proposal is awaiting-answer"
- supervision#r115: "when the gate round of a capability-proposal ends …", all four Examples (BLOCKED, an error, the turn limit, no result file)

The r114 scenario passes only because its Given hands the stand-in a `changes` field
(`supervision_formulate_steps.py`, `apply_change_list`). No real apply round gives that field. The agent's apply
text does not ask for it, and neither does `work run`'s apply brief (notes §3 rows `supervise_brief.py`,
`agents/initiative-round.md`; D1, reproduced as P1). Decision 2 below strengthens the r114 Then. With it, the r114
node goes **red today** and turns green only when the apply brief asks for the change list. The other ten nodes stay
green throughout.

The work-item has no Retires section and retires no deprecated scenarios. The old r83 was already removed in
`ce5c1bfb`, under w185.

## 2. Where the change lands

- `scripts/supervise_brief.py`: the apply round's brief also asks for the change list the round applied, in the
  result's `changes`. The form is the one `integrate_lines` names: one entry for each capability, with adds, changes and
  removes as ids. Where to put the shared wording is the implementer's choice (167 lines, so there is room).
- `agents/initiative-round.md`: the `apply` kind's text says to give, in the result's `changes`, the change list of
  what was applied after the answers. This is the form the brief names, as the integrate kind already does (its reply
  paragraph, around lines 32-33).
- `tests/scenarios/supervision_formulate_steps.py`: the r114 Then `lists_written` also asserts that p1's apply round
  was started with a brief asking for its change list in the result's `changes` (Decision 2).

The researcher's set has ten other files. This plan drops them all, and why:

- `scripts/supervise_rounds.py`: its apply branch already reads `changes` and calls `rewrite_lists` (notes §3). Once
  the round gives the field, no code change is needed. Whether a DONE apply with no list is an error is not taken here
  (part 5).
- `scripts/supervise_change.py`: D2 and F3 are minor observations, not fix-now findings, and are not taken (part 5).
- `scripts/supervise.py`, `scripts/supervise_all.py`, `scripts/supervise_worker.py`, `scripts/supervise_draft.py`,
  `scripts/supervise_done.py`: these are on the path but nothing changes in them. They cover D3 and F6, which are not
  taken.
- `features/supervision.feature`: a planner and an implementer write no scenario. The fix is pinned through the
  existing r114 scenario's step (Decision 2).
- `tests/scenarios/test_supervision.py` and `tests/scenarios/supervision_rounds_steps.py`: no change. The latter is
  at 288 lines, so it has no room anyway.

## 3. Decisions

1. **The apply round gives the change list it applied in its result's `changes`, in the integrate form, and both the
   apply brief and the agent's apply text ask for it.** This rests on supervision#r114 ("from the change list the round
   applied") and design-decision/worker-results-are-files (0038: `work run` reads stage fields, never prose). It does
   not change what the narrator observes beyond what r114 already states. spec-integration's Implementation section
   already has the apply round's writer reply with a change list, so this is how that list reaches `work run`, not a
   new line. `work run`'s reading of the list is unchanged: the same `entries` and `rewrite_lists`, and the same r107
   check on unknown capabilities.
2. **The r114 Then pins that the real brief asks for the list.** The stand-in cannot tell whether a real round would
   give `changes`. The only thing `work run` controls is that it asks for the list. So `lists_written` also checks
   that p1's apply brief, as recorded by the stand-in, names the change list in the result's `changes`. The check is
   on wording that marks the request, not on the whole text. This rests on supervision#r114 and finding 1's "met only
   against the stand-in". A new `tests/scripts` test of the brief was the other option. It is not chosen, because it
   would need a whole briefs fixture outside the scenarios the brief is already recorded in.

## 4. Tests the decisions break

None. What was verified:

- Notes §4 found no test asserting the old behaviour, and all eleven accepted nodes pass today.
- Decision 1 only adds lines to the apply brief. The steps that read apply briefs check that a string is contained,
  never that the brief equals something:
  - `apply_started` in `supervision_rounds_steps.py` checks `"Answer: …" in brief`.
  - The r108 drafts-path step in `supervision_proposal_steps.py` checks the `Drafts path:` line.
  - `supervision_review_steps.py:61` compares a kept brief only for the branch reviewer.
- Decision 2 strengthens one Then. It weakens nothing and removes nothing.
- The stand-in's `fields.changes` in `apply_change_list` stays as it is. It now stands for what the real round is
  asked to give.

## 5. Open cases (for the implementer to name, not to choose)

- **A DONE apply round that gives no `changes`**: today the lists are kept as drafted and the proposal goes on to
  `approved` (notes D1, review F1's last point). Making it an error, as r96 does for integrate, would change what the
  narrator sees. No line settles it, so it stays as it is and is named in the report as needing a line.
- **An apply list with no entry for the proposal's `argues`** empties all three lists (D2, review F2). This becomes
  reachable once the real round gives lists naming several capabilities, as i33's 7-apply did. It is left as it is
  and named.
- **The proposal stays `awaiting-answer` while `work run` exits 0**: this happens when the only waiting node is a
  proposal (D3). The spec is silent (r9 counts work-items only), so it is not taken.
- **A proposal that is `awaiting-answer` with no question** goes to apply (D4). It can only be reached by hand-editing.
- **Review F3, F4, F6 and F7** are minor observations. **F8** (stale `supervise_rounds.py` docstring) and the stale
  CLAUDE.md row for `supervise_change.py` are "drop". None of these files is in the file set.
- **Whether the apply text should say the list covers every capability the round applied, or only the proposal's**:
  the integrate form is one entry for each capability, and `rewrite_lists` keeps only the `argues` entry. The
  implementer names the wording it chose.
