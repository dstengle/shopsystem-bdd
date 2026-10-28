# Plan of w223: the delegation leaves glossary questions for the person

Accepts supervision#r162, supervision#r163. Under: supervision. From the research notes `.shop/work/i46/runs/w223/1-research/notes.md`.

## 1. What goes green

- **supervision#r163**: Scenario Outline "under a delegation, each question of the initiative that names neither a term of the glossary nor a glossary-proposal goes to a session of its own, given only the delegation and the files it names, that <reply>" (`features/supervision.feature` line 1334, rows "answers it" and "leaves it for the person"). Red today: its first Given, `spec/index.md's Glossary holds the term "ledger"`, has no step definition. Once that step exists the rest should pass on today's code, because neither question names "ledger". The scenario guards against the filter catching too much.
- **supervision#r162**: Scenario Outline "under a delegation, a question of the initiative that names <named> is left for the person and given to no session" (line 1352, rows `the term "ledger"` and `the glossary-proposal g1`). Red today for three reasons. The Glossary Given has no step. The Given `i1's glossary-proposal g1 is awaiting-answer` has no step. The Then `"<question>" was given to no session` has no step. The code is also missing: `Answers.answers` in `scripts/supervise_answers.py` gives every open question to `ask`, and nothing reads glossary terms or glossary-proposal ids.
- **Retires**: the work-item has no `## Retires` section, so nothing is retired by this work. The deprecated r77 outline at line 1302 names the r163 outline in its `Deprecated for:`, so r73 would list it. The deprecated r77 scenario at line 1320 has "Deprecated for: removal", which r73 does not cover. Both still pass after this change (no term is named in their questions), and they are left as they are. This plan cannot add the missing Retires line, because the planner writes only this plan. It is noted in the summary for the coordinator.

## 2. Where the change lands

- `scripts/supervise_glossary.py`: new module-level readers, kept beside `withheld`:
  - the terms of `spec/index.md`'s `## Glossary` (the bold name of each bullet);
  - the ids of every glossary-proposal under `.shop/work/*/`, as file stem and full `id`;
  - a predicate that says whether a question names one of them (see the Decisions for how matching works).
  The module docstring gets r162's purpose, and CLAUDE.md's module-map row for it gets the same addition (see below).
- `scripts/supervise_answers.py`: in `Answers.answers`, before `ask`, an open question that the predicate flags is not given to a session. It counts as a question left for the person, so the existing `left` flag is set. Later questions of the same item that the predicate does not flag still get their own sessions. The docstring names r162 and r163.
- `tests/scenarios/supervision_delegation_steps.py`: three new steps:
  - the Given that writes a `## Glossary` bullet for the term into the fixture's `spec/index.md`;
  - the Given that writes `.shop/work/i1/g1.md` with kind `glossary-proposal` and status `awaiting-answer`;
  - the Then that no `delegation-answerer` session's brief holds the question.
- `tests/scripts/test_supervise_answers.py`: a unit test of the predicate covering a term, a glossary-proposal id, a question naming neither, a different case ("Ledger"), and a word that only contains the term ("pledger"). `Stubbed` keeps working because the predicate is a module function, not a method on `self`.
- `CLAUDE.md`: the `scripts/supervise_glossary.py` row also names the questions left for the person (r162). CLAUDE.md requires a row per concern. This file is not in the researcher's set; it is added for that reason.

Not edited: `scripts/model_parse.py`. `glossary_entry` and `bullets` may be imported for reading the Glossary, and that is the implementer's choice of means. Its observable result is the same either way. `scripts/supervise.py` (7 lines of room) is not touched.

## 3. Decisions

1. **Which terms count**: only the terms of `spec/index.md`'s `## Glossary`. The terms a glossary-proposal adds but that are not yet applied do not count, and neither do the words after a bullet's `Not:`. Rests on supervision#r162 ("a term of the glossary"). It also rests on supervision#r163, which gives every other question a session, and on design-decision/the-glossary-is-a-target-of-spec-work: a term stands once it is in `spec/index.md`.
2. **Which glossary-proposals count**: every glossary-proposal under `.shop/work/` of any initiative and any status. A question names one by its file stem (`g1`) or its full `id`. Rests on supervision#r162 ("a glossary-proposal", not limited to the initiative's own or to open ones).
3. **What "names" means**: the term or id appears in the question as a whole word, or as a whole phrase for a multi-word term. Matching ignores case. A longer word that merely contains it does not count ("pledger" does not name "ledger"; `g10` does not name `g1`). Rests on supervision#r162: a question names a term by using it, not by containing its letters. The researcher's substring reading does not fit "names".
4. **Questions after one left for the person**: a flagged question is never given to a session, and it sets `left`. Every later question that is not flagged is still given to its own session (supervision#r163: "each question ... to a session of its own"). Its answer is written only while no earlier question of the item is unanswered. This follows the implementation line of supervision that the n-th bullet of `## Answers` answers the n-th of `## Questions`. It is the same handling today's code already gives a question left by a session. The researcher's reading A would stop the sessions at the first left question, and that breaks r163.
5. **Status after a left question**: an item with a flagged question keeps no move and stays `awaiting-answer`. Rests on supervision#r162 ("leave the question for the person"), through the existing `left` and `open_questions` check.
6. **Reviewer questions**: a reviewer's question that names a term or a glossary-proposal is also given to no session, so it gets no verdict from this run. Rests on supervision#r162, which makes no exception.

## 4. Tests the decisions break

None. Verified from the notes and by reading `features/supervision.feature` lines 1301-1368:
- The r77 deprecated outline (line 1302) and scenario (line 1320) have questions that name no glossary term or glossary-proposal, and their fixtures write no Glossary, so they still pass.
- `tests/scripts/test_supervise_answers.py::test_a_reviewers_item_with_every_question_answered_and_no_verdict_from_this_run_is_not_moved` has no open question, so the new check is not reached. `Stubbed` lacks no method, because the predicate is a module function (decision 4 changes no stub).
- By the notes' search, no test in `tests/` asserts that a glossary question goes to a session.
- The r78 scenario (line 1370) asks "Which module owns the log?" with no Glossary written, so it is unaffected.

## 5. Open cases

These are cases the scenarios do not cover, for the implementer to name in a test or a note, not to decide:
- An item whose first question is flagged and whose second is not. Its second question gets a session, and the answer is not written (decision 4). No scenario covers this mix.
- A fixture with no `spec/index.md`, or one with no `## Glossary`, has no terms. Every r77/r78 fixture is like this today.
- How today's `work run` treats an `awaiting-answer` glossary-proposal in `i1` (the r162 Given). Its gate and apply rounds are w225's work (r164-r172), not yet built. The implementer names what happens there if the r162 scenario meets it, for example an apply round started for it. This work does not build those rounds.
- A question that names a term only through a plural or other inflected form ("ledgers"). It is not flagged under decision 3.
