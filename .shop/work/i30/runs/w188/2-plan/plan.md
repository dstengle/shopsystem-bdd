# Plan of w188: fix the findings of branch review 1 of i30

Work-item `.shop/work/i30/w188.md`, under `supervision`, accepts supervision#r110, #r117, #r19. Its findings file is `.shop/work/i30/runs/branch-review/1/findings.md`; one finding there is triaged fix now (finding 1). Planned from the research notes `.shop/work/i30/runs/w188/1-research/notes.md`.

## 1. What goes green

None of the three accepted scenarios is red today. The researcher ran all three and they pass (notes §1, "3 passed"). This work-item exists to fix the branch review's fix-now finding, and that finding does not show up as a red scenario.

- **supervision#r19**: "a researcher is given the work-item's file set and accepted scenarios and a limit of 80 turns". Green today: `supervise_worker.py` gives `--max-turns 80`. The defect is in what the researcher is *told*: `agents/code-scout.md:24` still says 40 turns (finding 1, notes D2). No scenario reads the agent text, so the fix shows up in no scenario.
- **supervision#r117**: the scenario where a gate that gives no question gets the approval question written under `## Questions`. Green today (notes §1 and probe case a).
- **supervision#r110**: the scenario where a green fix work-item from a kept branch review starts the next branch review. Green today (notes §1).

Deprecated scenarios retired: none. The work-item has no Retires section. The r19 "40 turns (deprecated)" scenario was already retired by w184 (`cd134f29`).

The check stays `python3 -m pytest -q -p work_items --work-item w188`: all three scenarios stay green.

## 2. Where the change lands

- `agents/code-scout.md`: the sentence at line 24 that tells the researcher how many turns `work run` gives it now states 80 turns (`--max-turns 80`) instead of 40. This is the fix finding 1 names. Nothing else in the file changes.

That is the whole set, the same as the researcher's. Files left out on purpose:
- `README.md:174`: the 0.24.0 release note. It is history, and the findings file says it is fine.
- `scripts/supervise.py`: the r110 loop has no bound (D3, finding 2). Finding 2 is an observation, not a fix-now finding, and no line asks for a bound.
- `scripts/supervise_rounds.py`: an empty-string question gets written as an empty question (D1). The review did not raise it, and changing it changes what the narrator sees (see §5).

## 3. Decisions

1. **The agent text states the limit `work run` gives.** The researcher's instruction file must state the limit r19 sets: 80 turns, given as `--max-turns 80`. Rests on supervision#r19 and on branch review 1's finding 1 (fix now). Only the number and the flag value in that sentence change. The sentence's advice to write notes well before the last turn stays.
2. **Findings 2 to 4 are not fixed here.** Finding 2 is triaged "observation", finding 3 "drop", and finding 4 "observation" (and finding 4 is w180's, under formulation, not this capability). The work-item's findings link marks only finding 1 as fix now. Rests on the findings file's triage.

## 4. Tests the decisions break

None. What I checked (from the notes, §3 and §4):
- No test reads the turn text in `agents/code-scout.md`. `tests/scripts/test_agents.py` checks the agent files' shape (lines 26-83) and asserts no turn text. It keeps passing.
- No test or scenario asserts "40 turns" or `--max-turns 40`. The only matches anywhere are `agents/code-scout.md:24` and `README.md:174`.
- No code changes, so no scenario's steps are affected.

## 5. Open cases

Left for the implementer to name in the report, not to settle here:
- **D1:** a gate result whose `questions` is an empty string, or a list holding one empty string, writes an empty question `- ` instead of r117's approval question (probe cases c and d). Whether "gives no question" in r117 covers an empty or whitespace-only question is unsettled. Under one reading the narrator sees the approval question; under the other they see an empty question line. No requirement or ruling decides it, and this work-item does not touch it. Name it as a candidate for a requirement line.
- **D3 / finding 2:** the r110 review-and-fix loop in `supervise.py` has no bound. No line names one.
- Not probed by the researcher: whether `workqueue.add` commits the fix work-item it drafts before `supervise.py` pushes (notes §5).
