# Plan of w172: fix the findings of branch review 1 of i28

Work-item `.shop/work/i28/w172.md` accepts supervision#r102, r103 and r104, under supervision. It names the findings file `.shop/work/i28/runs/branch-review/1/findings.md`. It has no `## Retires` and no `## Rulings`.

The review triaged one finding as fix now: finding 1, the label of the integrate brief. Findings 2 and 3 are observations, and findings 4 and 5 are drops. This plan does the fix-now finding. It also does the ruff part of finding 4, but only on the lines of the two files the fix touches anyway.

## 1. What goes green

- **supervision#r102:**
  - "an integrate round is given every requirement id another initiative's kept drafts add that spec/ on the branch it starts from does not hold, whatever that initiative's capability-proposal's status"
  - its `@deprecated` twin, which stays in place.
  - Both pass today (notes part 1, run: 4 passed). They go red once the step `integrate_given_ids` also asserts the label the round reads (decision D2).
  - Today's brief line is "Requirement ids other initiatives' kept drafts add, which spec/ does not hold yet; take none of them: …" (`scripts/supervise_brief.py:79`). The label the round is told to look for is "Ids drafted elsewhere" (`agents/initiative-round.md:27`, `skills/integrating-a-proposal/SKILL.md:23`). So the label assertion fails until D1 is made.
- **supervision#r103:** "an accepted request this context is the upstream of, that no initiative fulfils, has its initiative started with `work start`". It passes today. This plan does not change it, and it stays green.
- **supervision#r104:** "the gate round of a capability-proposal is asked only for the questions on the lines and terms that proposal adds, changes or removes". It passes today. This plan does not change it, and it stays green.
- **Deprecated scenarios retired:** none. The work-item has no `## Retires`. So the deprecated r102 scenario (`features/supervision.feature:1239-1250`) and its step `other_initiative` stay (finding 3 is an observation and is left for later).

## 2. Where the change lands

- `scripts/supervise_brief.py`, in `Briefs.integrate_lines`:
  - The line for the other initiatives' ids carries the label "Ids drafted elsewhere".
  - Its wording asks the round to number added lines above each listed id on the same capability, instead of "take none of them".
  - It also clears the ruff errors on line 3 (I001) and line 82 (ISC004) of this file.
- `tests/scenarios/supervision_integrate_steps.py`:
  - The step `integrate_given_ids` also asserts that the brief carries the "Ids drafted elsewhere" label and that the given ids are on that line.
  - It also clears FURB167 on lines 107 and 112.

The researcher's set had more files. These are left out, and why:

- `features/supervision.feature` and `tests/scenarios/test_supervision.py`: retiring the deprecated scenario needs a `## Retires` section, which this work-item does not have.
- `tests/scenarios/supervision_intake_steps.py`, `tests/scenarios/supervision_proposal_steps.py` and `tests/scripts/stub_claude.py`: their only change would be ruff, which finding 4 triaged as drop. The stub does not read the label: a grep for the old wording in `scripts/`, `tests/`, `agents/` and `skills/` hits only `supervise_brief.py:79` and a step regex that does not touch the brief.
- `CLAUDE.md`: finding 2 is an observation.

## 3. Decisions

- **D1. The label is fixed on the code side.**
  - The brief takes over the words the instructions already use. `agents/initiative-round.md` and `skills/integrating-a-proposal/SKILL.md` stay as they are.
  - The line reads as an instruction to number above every listed id on the same capability, not "take none of them".
  - When there are no ids, the line still appears and lists none. The instructions say "A brief that lists none leaves the numbering as it was".
  - Rests on: spec-integration#r43 (the round numbers its added lines "above every id it is given on the same capability") and supervision#r102 (`work run` gives the round those ids).
  - Why the code side: the instruction text is w169's delivered guarantee for r43 (design-decision/workflow-capabilities-are-guarantees). One line of code changes, and no guarantee text is reopened.
  - This does not change what the narrator observes: the ids given and not given are the same, and only the brief's wording to the round changes.
- **D2. The r102 scenario checks the label.**
  - `integrate_given_ids` asserts that the brief has the "Ids drafted elsewhere" label with the given ids on it.
  - Rests on: supervision#r102 ("give the round" the ids, which counts only when the ids are given where the round reads them, under r43). The branch review's fix also asks for this step to assert the label.

## 4. Tests the decisions break

None. What I checked:

- No test asserts the old wording: the notes' grep for "take none" and "drafted elsewhere" in `tests/` found nothing, and my own grep for the brief's old wording found only `supervise_brief.py:79`.
- `integrate_not_given` checks only that thing#r1, thing#r2 and thing#r5 are absent, so it is unaffected.
- `integrate_given_ids` gains one assertion. Both r102 scenarios, the current one and the deprecated one, reach it, and both pass with D1.
- The r103 and r104 steps do not read the integrate brief.

## 5. Open cases

- How the line is laid out when there are no ids: the label followed by "none", or something else. The scenarios do not say.
- The order and separator of the listed ids on the line.
- How strictly the new assertion matches: the exact label, or the label with the ids following on the same line.
