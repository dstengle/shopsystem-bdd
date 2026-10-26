# Plan of w201: fix branch review 2's fix-now finding (i38, supervision)

Sources: the work-item, `spec/capabilities/supervision.md`, the research notes and result (`runs/w201/1-research/`), the findings of branch review 2 (`runs/branch-review/2/findings.md`), design-decision 0065 (workflow-capabilities-are-guarantees, which supervision `rests_on`), and `features/supervision.feature` (the r83 and r132 scenarios). I also read `scripts/work_items.py:guarantees`, for decision 2.

## 1. What goes green

**Nothing is red today.** The researcher ran `tests/scenarios/test_supervision.py` and got 64 passed. That run covers every accepted scenario of the 20 requirements w201 accepts:
- r4, r31, r32, r36, r37, r45, r61;
- r86 to r90, r115;
- r128 to r134.

They stay green. Those to watch are:
- the r132 outline, whose formulate row is "a scenario for thing#r4 and no question";
- the r131 outline, whose formulate round row is "the formulate round's scenario for thing#r4";
- the r83 scenario, "when the formulate round `work run` started for a capability-proposal ends without giving a question, the proposal is formulated".

**What the work fixes.** Review 2's Important finding 1 (fix now). A formulate round on a proposal whose `adds` or `changes` names a requirement of a guarantees capability never reaches `formulated`, because `supervise_outputs.unformulated` counts that id as lacking. Research probe P1 reproduces it: `planning#r1`, `review#r1` and `formulation#r1` come back lacking. No accepted scenario pins this case, so it is not red. Before any code changes, the implementer needs a scenario that is red today. It is a new row of the r132 outline (or a scenario tagged `@r132`/`@r83`), and it comes through a feature-formulator hand-back: the implementer asks for it as its question. The plan describes the row and does not write it:
- **Given:** i1's capability-proposal p1 is awaiting-answer and has answered formulate-round questions, as in the existing formulate row. Its `adds` names a requirement of a capability whose frontmatter has `group: guarantees`.
- **When:** the formulate round gives no scenario and no question.
- **Then:** p1's transition to formulated was made once the formulate round had ended.

Today this row is red: p1 goes to `awaiting-answer`, with "the formulate round's scenario for <cap>#r<n> is missing" under its `## Questions`.

**Retires:** none. The work-item has no Retires section, and no scenario changes meaning.

## 2. Where the change lands

- `scripts/supervise_outputs.py`: `unformulated` skips every id whose capability is guarantees (decision 1). It gains the root-taking reader of a capability's `group: guarantees` (decision 2).
- `scripts/work_items.py`: `guarantees` keeps its own path resolution from the pytest config and reads the group through the reader of decision 2, so the frontmatter is read in one place.
- `scripts/supervise_rounds.py`: there is no change to the formulate branch (lines 148-154). The only change is the import order at line 7, which fixes ruff I001 (review finding 3, decision 4).
- `features/supervision.feature`: the new guarantees row of section 1. It comes through the feature-formulator hand-back, not written by the implementer.
- `tests/scenarios/supervision_formulate_steps.py` and `tests/scenarios/supervision_session_faults_steps.py`: the Given that writes a guarantees capability file in the test repository. The formulate stand-in for that row commits no scenario, because `stage_gives` must not commit one for a guarantees id.
- `tests/scenarios/test_supervision.py` (265 lines, room 35): this changes only if a new steps module or step import must be bound there. The binding is `scenarios("supervision.feature")`.

This is the researcher's file set, unchanged.

## 3. Decisions

1. **The formulate round's output leaves out guarantees requirements.** A requirement of a capability whose frontmatter has `group: guarantees` asks the formulate round for no scenario. A formulate round that gives no question on a proposal naming only such ids, or such ids together with formulated ones, therefore transitions the proposal to `formulated`. This rests on:
   - design-decision 0065 (workflow-capabilities-are-guarantees): guarantees capabilities have no scenarios and are checked by `measure`;
   - supervision#r83: a formulate round ending without a question gives `formulated`;
   - supervision#r132, read with 0065: the scenario output has nothing to give for a guarantees requirement.

   The rest of the system already reads it this way: `model.lp` v15f excepts `group(C, "guarantees")`, and r56, r64 and r65 excuse guarantees work-items. The Implementation line for r56, r64 and r65 defines "guarantees" as `group: guarantees` in the frontmatter, and this plan uses the same definition.
2. **One reader of a capability's guarantees group.** It takes the repository root and a capability name. It does not take a pytest config, so `work run` does not import pytest through `work_items`. It lives in `supervise_outputs.py`, and `work_items.guarantees` calls it after resolving the root as it does today. A capability with no spec file is not guarantees: its ids stay lacking, as today. This follows the `supervise_outputs.py` module-map row (the reading of a stage's output) and the CLAUDE.md rule against a duplicated concern.
3. **No change to how the question is asked.** `supervise_rounds.py` still makes one question of whatever ids `unformulated` returns (supervision#r131).
4. **Ruff I001 at `supervise_rounds.py:7` is fixed** by putting the imports in order. This changes no behaviour, and the file is already in the set (review finding 3).
5. **Not taken in this work** (they are observations, not fix-now):
   - review finding 2, ranges and the keyword synonyms `Scenario Template:` and `Example:`. Reading ranges would change what the narrator sees for a range id;
   - finding 4, a changed requirement's old scenario still counting;
   - findings 5 to 9.

## 4. Tests the decisions break

None. I verified this from the notes, section 4, and from the review:
- no test asserts that a guarantees id is lacking;
- the r131 and r132 formulate rows use `thing`, which has a feature file and no `group: guarantees`, so decision 1 leaves them as they are;
- the `steady` guarantees fixture in `supervision_tests_steps.py` (r56, r64, r65) goes through `work_items.guarantees`. Under decision 2 that function returns the same answer for the same file, so those scenarios keep passing.

## 5. Open cases

These are for the implementer to name, not to choose:
- A proposal whose `adds` mixes guarantees ids with lacking ordinary ids. Decision 1 says only the ordinary ids are asked for. No scenario pins the mix.
- A guarantees capability's spec file with `group: guarantees` written differently, for example quoted or with trailing spaces. The reader matches the exact line, as `work_items` does today.
- A range id (`planning#r1-r3`) of a guarantees capability. It is skipped by capability whatever its range form. The range reading for ordinary capabilities stays as it is (finding 2).
- Whether the hand-back puts the new row in the r132 outline's Examples or makes it its own `@r83` scenario. That is the formulator's choice.
