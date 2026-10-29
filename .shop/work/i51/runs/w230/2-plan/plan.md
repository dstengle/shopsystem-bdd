# Plan of w230: supervision r209, r210

## 1. What goes green

- **supervision#r209**: "under a delegation, a question of the initiative's glossary-proposal is left for the person and given to no session, whatever words it uses, here <words>" (features/supervision.feature:1353). There are two examples: "naming the term "ledger"" and "naming no term of the glossary". Both are red today because the Given "i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with "<q>" and no answer" is undefined. The Then "g1's question "<q>" has no answer" is undefined too. The code already holds r209: `Answers.asking` in scripts/supervise_answers.py lists only work-items and capability-proposals. So r209 needs only step definitions.
- **supervision#r210**: "under a delegation, each question of the initiative that is not a question of a glossary-proposal goes to a session of its own, … even when it names a term of the glossary or a glossary-proposal, that <reply>" (features/supervision.feature:1370). There are two examples: "answers it" and "leaves it for the person". Both are red today because the Given for w2 with two unanswered questions is undefined (the existing step hard-codes w1). The two After texts are undefined too (the existing ones name only w1 and p1). The code is also red: `Answers.answers` uses `supervise_glossary.names_one` to give any question that names a term or a glossary-proposal to no session, so w2's questions are never asked.
- **Deprecated scenarios retired.** The work-item has no `## Retires` section. Decision D2 below retires the r162 @deprecated outline ("under a delegation, a question of the initiative that names <named> is left for the person and given to no session (deprecated)", features:1334-1351).

## 2. Where the change lands

- `scripts/supervise_answers.py`: every open question that `asking` gives is asked, with no `names_one` test. Remove the `supervise_glossary` import. Reword the module docstring so it no longer cites r162/r163 and cites r209/r210 instead.
- `scripts/supervise_glossary.py`: delete `names_one`, `proposals_of` and `terms_of`. Each fed only the retired rule. Reword the module docstring so it no longer says a question naming a term is left for the person.
- `tests/scripts/test_supervise_answers.py`: delete the test of `names_one` (see part 4).
- `tests/scenarios/supervision_delegation_steps.py`, step definitions:
  - a Given for a glossary-proposal awaiting-answer with one unanswered question in its ## Questions;
  - the "awaiting-answer with two questions, each with no answer" Given widened from w1 to any work-item name;
  - a Then saying a glossary-proposal's question has no answer;
  - Thens for the two r210 After texts: w1, p1 and each of w2's questions answered; none answered, with w1, w2 and p1 awaiting-answer.
  
  The file is at 224 lines, so it must stay at 300 or under. Widen the existing steps rather than add near-copies.
- `features/supervision.feature`: retire the r162 @deprecated outline with the `features retire` command (D2).

This is the researcher's file set, unchanged.

## 3. Decisions

- **D1. What "a question of a glossary-proposal" means.** It is a question written in a glossary-proposal's own ## Questions section, whatever its words name. Any question elsewhere goes to a session, even one that names a term or a glossary-proposal. This rests on supervision#r209 and #r210 ("whatever words it uses"). The i51 ledger records the person's approval of reading (a) on 2026-10-29, and the r210 scenario's w2 question "Does scripts/queue.py wait for g1 to be applied?" requires it. With this reading the word-matching helpers have no requirement left, so they are deleted, not kept dead.
- **D2. Retire the r162 @deprecated outline in this work-item.** It asserts r162, which the spec lists as retired and the person approved retiring on 2026-10-29. After D1 its Then "was given to no session" fails. Neither r43 nor r122 counts that failure as expected, so the whole-suite gate of supervision#r4 would stop w230 from merging, and r123 would never fire. This choice rests on r4 and on the retirement of r162 (the capability's `retired:` list).
- **D2a. Leave the r163 @deprecated outline in the feature.** It still passes under D1 because its questions name no term. supervision#r123 retires it once w230 is green. This keeps the change minimal.
- **D3. Leave the r77 @deprecated scenario alone.** It names no term and stays green.

## 4. Tests the decisions break

- **features/supervision.feature:1334, the r162 outline (both examples).** D1 breaks it: the w1 question reaches a session. D2 removes it through `features retire`, because it asserts a retired requirement.
- **tests/scripts/test_supervise_answers.py:59, `test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case`.** D1 deletes `names_one`, which this test asserts. Delete the test, not rewrite it, because the behaviour it pins is r162, which is retired. The r209 and r210 scenarios cover the new rule.
- **Verified kept (from the notes):**
  - test_supervise_answers.py:46-56 (no ask for an answered question);
  - the r163 outline (features:1315);
  - the r77 scenario (features:1301).
  
  These give the same results under D1.

## 5. Open cases

- A glossary-proposal question that also names files: the scenarios do not say whether anything about it is recorded beyond "given to no session". The implementer names this case and does not choose.
- A glossary-proposal question that has already been answered: the scenarios are silent on it.
- Whether the run's exit status differs when only glossary-proposal questions remain open: the r209 scenario asserts no exit status.
