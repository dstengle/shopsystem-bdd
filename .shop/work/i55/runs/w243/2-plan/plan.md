# Plan of w243 (supervision r184, r185, r186)

From the research notes (`.shop/work/i55/runs/w243/1-research/notes.md`). The notes find the production code for all three requirements already present. The four red scenarios are red only because of step definitions. `python3 -m pytest -q --work-item w243`: 4 failed, all `StepDefinitionNotFoundError`.

## 1. What goes green

- **supervision#r184**: Scenario Outline "when `work run` ends with <node> awaiting-answer, it exits with an error, printing <node> with its open questions", examples p1 and w2. Why it is red: the Givens "... its Answers section answering only ... with ..." (for p1, "given by its gate round", and for w2) have no step. Its Thens are not reached yet, and two of them have no step either: "`work run` prints <node> with the question "..."" (test_supervision.py:195 needs "and the question") and "it prints neither ... nor ... with <node>" (the `$` anchor at test_supervision.py:255 forbids "with <node>"). "it exits with an error" exists (test_supervision.py:119).
- **supervision#r185**: Scenario "a researcher's result that gives an empty file set is taken as the researcher's file set". Why it is red: the Then "`work run` wrote no question naming the researcher's file set as missing" has no step. The Given "the researcher's result gives no question and an empty file set, ..." does match supervision_outputs_steps.py:23, but its parsing (:37-42) knows only "no file set" and "file set of X". So the stand-in gives the default `scripts/thing.py`, not an empty file set.
- **supervision#r186**: Scenario "a formulate round that formulates nothing because the proposal's answers change lines not in spec/ is followed by a new integrate round for the proposal". Why it is red: the Then reads "... after the formulate round for p1 had ended", but the step at supervision_reintegrate_steps.py:76 has no "for p1".
- Retired scenarios: the work-item has no Retires section, so none. Deprecated r149 (features/supervision.feature:1610-1619) shares the r186 Then step in its old wording, and it must keep passing.

## 2. Where the change lands

- `tests/scenarios/supervision_outputs_steps.py`: the researcher-result Given learns "an empty file set", which gives the stand-in an empty `fileset` list. A new Then (or a widened pattern of the Then at :131) asserts that no question naming the researcher's file set as missing was written.
- `tests/scenarios/supervision_reintegrate_steps.py`: the Then at :76 takes an optional "for <proposal>". When it is given, the step checks the formulate round of that proposal.
- `tests/scenarios/supervision_awaiting_steps.py` (new, under the existing `tests/scenarios/` row of CLAUDE.md, so no new row is needed): the r184 Givens for a capability-proposal (with the round that gave the questions) and for a work-item, both awaiting-answer with an answer to only one question. Also the Thens "`work run` prints <node> with the question "..."" and "it prints neither "..." nor "..." with <node>".
- `tests/scenarios/test_supervision.py`: one import of the new module (269 lines, room 31).

This is the researcher's set, unchanged. No production file is added: the decisions below change no code.

## 3. Decisions

1. **"Exits with an error" is any nonzero exit, and the existing exit 3 for awaiting-answer stands.** This rests on design-decision exits-are-successful-or-errors (0055): Behaviour names no exit code, codes live in Implementation, and a command waiting on the person exits with an error. It also rests on supervision's Implementation section ("3 awaiting an answer"). This settles the notes' reading A. Reading B (exit 1) is excluded, so `Run.show`, `asked`, `supervise_all` and test_supervise_show.py stay as they are.
2. **The r184 Givens write the two sections by the positional rule the capability keeps.** The rule is that the n-th bullet of `## Answers` answers the n-th of `## Questions` (supervision Implementation; `Run.questions` reads it this way). So "answering only "Is the old reader kept?"" is written with that question as the first bullet of `## Questions`, "Which unit is the limit in?" as the second, and one answer bullet "Yes." The open question is then "Which unit is the limit in?", as r184 requires. The Given's wording does not fix the order of the bullets in the file, and no production change is needed. Rests on supervision#r184 and the Implementation line.
3. **For p1, "given by its gate round" records the gate round as the source of the questions**, the same way supervision_reintegrate_steps.py:46 records "given by its formulate round". The proposal stays awaiting-answer because it has fewer answers than questions (the routing in supervise_rounds.py:56). Rests on supervision#r184.
4. **"it prints neither A nor B with <node>"** reads the output that `work run` prints for that node: its status line and the indented lines under it, up to the next node's line. Neither text may appear there. "prints <node> with the question Q" requires Q among those indented lines. Rests on supervision#r184 ("printing each with its open questions").
5. **The r186 Then accepts both wordings.** The phrase "for <proposal>" is optional, so deprecated r149's line and r186's line both bind to one step. Rests on supervision#r186. Changing the feature line is not the planner's to do.
6. **r185 needs no production change.** supervise_outputs.py:17 already takes `[]` as given. The work is the stand-in giving `[]` and the Then. Rests on supervision#r185 and design-decision the-file-set-is-the-claim.

## 4. Tests the decisions break

None. Checked from the notes, which found tests by search because there was no map:
- Decision 1 keeps exit 3, so tests/scripts/test_supervise_show.py:29-31 (`== 3`) stays sound.
- Decision 5 keeps deprecated r149 (:1610-1619) passing, because the step accepts its wording.
- r83, r152 and r153 (:1602, :1622, :1633) do not forbid the integrate round r186 starts. The "no round of the kind integrate was started for i1" step (supervision_rounds_steps.py:180) concerns i1, not p1.
- Decisions 2-4 add steps and change no existing one. The existing Thens at test_supervision.py:195 and :255 are left as they are; the new Thens are new patterns that must not collide with them.

## 5. Open cases

- What the "with <node>" Thens do when a node is printed twice in one run, for example once in the initiative's statuses and once by `asked` or a fault list.
- Whether the r185 Then has to tell a question naming the file set apart from any other missing-output question. The scenario only says that none naming the file set is written.
- How the r184 run treats the proposal's gate round (it is not started again, because the proposal is awaiting-answer with an open question). The implementer should name it if the stand-in round setup needs "every other round ends".
- Size: test_supervision.py has room for 31 more lines. supervision_delegation_steps.py (258) is not touched. The new module starts small.
