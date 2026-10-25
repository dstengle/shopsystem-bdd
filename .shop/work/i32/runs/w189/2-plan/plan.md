# Plan of w189: review#r31

## 1. What goes green

- **review#r31**: when a branch review ends, the branch reviewer gives in its result's `questions` only the findings it triages fix now.
  - Scenarios: none. review is `group: guarantees` (design-decision 0065, workflow-capabilities-are-guarantees). It has no feature file and no `@r31` tag for review, so no scenario has to run red (notes §1). The work is checked by `measure` on real batches, not by a scenario.
  - What is wrong today (notes §2, §3, §6 D1): `agents/bdd-branch-reviewer.md` line 74 tells the reviewer to list each fix-now **or Critical** finding **and each check it could not verify** in `questions`. The probe shows `fix_work_item` drafting a fix work-item for a Critical line that is not fix now, and also for an unverified-check line. r31 rules out both.
- Retires: none. The work-item has no Retires section and no Rulings.

## 2. Where the change lands

- `agents/bdd-branch-reviewer.md`: the only file that changes.
  - The `questions` rule in "The result" becomes "each finding triaged fix now, one line each (grade, work-item, file:line, what is wrong), else empty".
  - The `NEEDS_CONTEXT` stop paragraph changes as decision 3 says.
  - The `status` rule and "What you run"'s line "a check you cannot verify fails the review" stay as they are.

No Python file and no test file changes. `scripts/supervise_draft.py` `fix_work_item`, `scripts/supervise_analysis.py` `lists_nothing`, and `pull_through` in `scripts/supervise.py` read `questions` as it comes. Narrowing what goes into `questions` fixes defect D1 without touching them (notes §3, §7). This is the researcher's file set, with nothing added or removed.

## 3. Decisions

1. **Critical findings not triaged fix now, and checks the reviewer could not verify, leave `questions`.**
   - Where they stay: they are still written in `findings.md`, under `Findings` and `Cannot verify`, and they still make the result's `status` `DONE_WITH_CONCERNS`.
   - Rests on review#r31: its "only" admits no other line.
   - Rests on review#r6: "fail the review" stays, carried by the status rather than by `questions`.
   - Rests on review#r10 and review#r2: they set the grade, not the triage.
   - Of the notes' two readings (§5), reading B, where the unverified check still reaches `questions`, contradicts r31's text. So this is not a choice between two readings of a requirement, and no question is needed.
2. **The `status` rule is unchanged.**
   - `DONE` still requires that no finding is fix now, none is Critical and every check was verified. `DONE_WITH_CONCERNS` covers the rest.
   - This keeps `lists_nothing` (`DONE` with empty `questions`) meaning "nothing to fix now".
   - Rests on review#r6 and on design-decision 0040 (review-of-work-items): fix-now findings become fix work-items, and the rest are observations.
3. **On the `NEEDS_CONTEXT` stop, the reason goes in `summary` alone, and `questions` is empty.**
   - A stop ends the branch review, and it has no finding triaged fix now. So r31 leaves `questions` empty.
   - review#r28's "stop, saying why" is met by the summary.
   - Rests on review#r31 and review#r28.
   - Narrator effect: `fix_work_item` drafts only for a line naming a work-item of the initiative, and `lists_nothing` needs `DONE`. So `work run` drafts nothing either way. The only change is that the reason is no longer duplicated in `questions`.

## 4. Tests the decisions break

None. The notes (§4) searched `tests/scenarios/supervision*.py` and `tests/scripts/*.py` for `Critical`, `cannot verify` and `unverif`. No test asserts a Critical or unverified-check line, or a stop reason, in a branch review's `questions`.
- The tests that stub a branch reviewer's result use only `Important` fix-now lines or `[]`. These are `FIX_NOW` in `supervision_proposal_steps.py` and the `[]` and `PARTIAL` results in `supervision_analysis_steps.py`, and they stay valid under decisions 1 to 3.
- `tests/scripts/test_agents.py` checks the agent files' frontmatter only. The frontmatter is unchanged (the `description` does not mention `questions`).
- After the edit, run the three supervision scenarios the notes name, with `test_agents.py`. They should still pass.

## 5. Open cases

- A finding that is both Critical and triaged fix now appears once in `questions`, as a fix-now line. The implementer names whether its grade field reads `Critical`.
- A fix-now finding in a commit that belongs to no work-item. "The branch" section makes that commit a finding, but the line names no work-item of the initiative, so `fix_work_item` drafts nothing for it. The implementer names what the line gives as its work-item.
- `measure` of a later initiative is the check on r31, since no scenario covers it. The implementer names nothing here and does not add a test for the prompt text.
