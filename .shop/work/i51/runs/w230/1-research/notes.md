# w230 research: supervision r209, r210

Method: no coverage map exists (`tools tests-of` answers "no map"), so every test list is `by search`. `tools refs` shows `names_one` with 0 references, though `supervise_answers.py:75` calls it as a module attribute; caller counts below are by search.

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q --work-item w230`. Result: 4 failed, 181 passed, 1 skipped. All four failures are Outline examples, each stopped at its first Given (StepDefinitionNotFound); their Thens were not reached.

- r209, features/supervision.feature:1353, both examples (run): Given `i1's glossary-proposal g1 is awaiting-answer, its ## Questions section with "<q>" and no answer` is undefined. tests/scenarios/supervision_delegation_steps.py:29 matches g1 with no questions; supervision_proposal_steps.py:133 needs an Answers section. The Then `g1's question "<q>" has no answer` (line 1362) is undefined too: supervision_delegation_steps.py:130 is w1-only. Code (read): r209 already holds, since supervise_answers.py:57 `asking` lists only work-item and capability-proposal kinds. So r209 needs steps, no code.
- r210, features/supervision.feature:1370, both examples (run): Given `i1's work-item w2 is awaiting-answer, its ## Questions section with "A" and "B", each with no answer` is undefined: supervision_delegation_steps.py:69 hard-codes w1. The two After texts (lines 1385, 1390) are undefined too: have_answer (:200) and have_none (:206) name w1 and p1 only. Code (read): supervise_answers.py:75, in `Answers.answers`, gives any question naming a term or glossary-proposal to no session (`supervise_glossary.names_one`), so w2's two questions are never asked. This needs a code change.

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_answers.py:Answers.answers (line 75) | a question naming a term or glossary-proposal is not asked: answer None, left for the person | r210: asked, each in a session of its own; the test is only the glossary-proposal's own ## Questions (r209) | by search: test_supervision.py r162 outline (features:1334); r209, r210 outlines (red) | grep `names_one`; read |
| scripts/supervise_glossary.py:names_one (102-106) | whole-word, any-case match of a question against terms_of and proposals_of: the retired r162 rule | no requirement keeps it (r162 retired; r209, r210 replace it) | by search: tests/scripts/test_supervise_answers.py:59 (direct) | grep: one caller, supervise_answers.py:75 |
| scripts/supervise_glossary.py:proposals_of (92-99) | reads each glossary-proposal's file stem and id under .shop/work/ | feeds only names_one | by search: test_supervise_answers.py:59, through names_one | grep; refs (one caller, names_one) |
| scripts/supervise_glossary.py:terms_of (58-61) | reads the term names of spec/index.md's Glossary | feeds only names_one | by search: test_supervise_answers.py:59, through names_one | grep; refs (production use only at names_one) |
| scripts/supervise_answers.py module docstring (lines 1-5) | says a question naming a term is left for the person (r162, r163) | text must change | none (text only) | read |
| scripts/supervise_glossary.py module docstring (lines 1-4) and names_one docstring | says a question naming a term is left for the person (supervision r162) | text must change | none (text only) | read |
| scripts/supervise_answers.py import of supervise_glossary (line 10) | imported only for names_one | goes with it | none | grep |
| scripts/supervise_answers.py:Answers.asking (52-59) | lists awaiting-answer work-items and capability-proposals; glossary-proposals excluded | already the r209 rule; no change | by search: test_supervise_answers.py:21 stubs it; r209 outline (red at steps) | read |

Reading (a) is the one i51's ledger records as approved (grep of .shop/work/i51/supervision.md): only a glossary-proposal's own ## Questions goes to no session. Reading (b) would be any question about a glossary-proposal, wherever written. Under (b), r210's `Does scripts/queue.py wait for g1 to be applied?` on w2 would go to the person, which contradicts the scenario at features:1384. The scenarios therefore require (a).

## 3. Tests the requirements make impossible to keep

Method: by search (no map). Read only; the single run in part 1 is the only run.

- features/supervision.feature:1334-1346, r162 @deprecated outline, both examples: Then `"<q>" was given to no session` (supervision_delegation_steps.py:36) fails once names_one is gone, since "Does scripts/log.py write the ledger?" and "Does scripts/log.py wait for g1 to be applied?" then reach a session. Mechanism: supervise_answers.py:75.
- tests/scripts/test_supervise_answers.py:59-71, `test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case`: asserts names_one, the retired rule. It fails by ImportError once names_one is removed; kept, it would assert the retired rule. Mechanism: supervise_glossary.py:102.

Kept, found sound (read):
- test_supervise_answers.py:46-56: stubs asking and held; no ask is made for an answered question; unaffected.
- features/supervision.feature:1315-1332, r163 @deprecated outline: its questions name neither a term nor a glossary-proposal; same answers under the new rule.
- features/supervision.feature:1301-1313, r77 @deprecated: no term named; same result.
- No test or plugin code skips @deprecated (search of tests/ and scripts/work_items.py), so the r162 outline runs in the whole suite. Once changed it is red and counted expected by neither r43 (no accepted requirement) nor r122 (supervision is formulated, and r162 is not added or changed). So w230's whole-suite gate (r4) fails unless the outline is retired.

Retire reading: w230 has no ## Retires. r73 lists a deprecated scenario whose `Deprecated for:` names a scenario of an accepted requirement. The r162 and r163 outlines say `Deprecated for: r209 and r210`, which names requirements, not scenario titles.
- Reading (a), requirement level: w230 accepts r209 and r210, so list the r162 outline (and r163, optional) under ## Retires.
- Reading (b), literal: no scenario is named, so w230 lists nothing. The r162 outline then stays red in the suite. r123 retires a deprecated scenario only once its replacement's work-item is green, so w230 cannot reach green and r123 never fires.

## 4. The file set

Production files to change:
- scripts/supervise_answers.py (148 lines): drop the names_one test at line 75 so every open question is asked; drop the import at line 10 and the docstring lines 1-5 (r162, r163). Found: grep, one caller.
- scripts/supervise_glossary.py (115 lines): delete names_one, proposals_of and terms_of (lines 58-61, 92-106); reword docstring lines 1-4 (r162). Found: grep; refs.

Test files to change:
- tests/scripts/test_supervise_answers.py (72 lines): delete the test at lines 59-71. Found: read.
- tests/scenarios/supervision_delegation_steps.py (224 lines): a Given for g1 with ## Questions and no answer (widen line 29); widen two_unanswered (lines 69-74) from w1 to any name; a Then for g1's question has no answer (widen line 130); Thens for the two r210 After texts (lines 1385, 1390). Found: read; the run's undefined steps.
- features/supervision.feature (1981 lines): retire the r162 @deprecated outline (lines 1334-1352) and, under reading (a), the r163 outline (1315-1332), with `features retire`, which removes only @deprecated scenarios (tests/scripts/test_features_deprecating.py). Found: grep `@r162`, `@deprecated`.

Modules on the change's path, edited or not (line count, room under 300 per CLAUDE.md; counted with wc):
- scripts/supervise.py: 295 lines, room 5. Run mixes in Answers (line 19). Not edited.
- scripts/supervise_answers.py: 148 lines, room 152. Edited.
- scripts/supervise_glossary.py: 115 lines, room 185. Edited.
- scripts/supervise_worker.py: 259 lines, room 41. Supplies git, SCRIPTS and GitFailed to the answering path. Not edited.
- tests/scripts/test_supervise_answers.py: 72 lines, room 228. Edited.
- tests/scenarios/supervision_delegation_steps.py: 224 lines, room 76. Edited.

Other facts (read): the answering brief gives only the question, the delegation and the named files (supervise_answers.py:131-148), which the r210 Thens' `spec/` and `.shop/work/` checks rely on.

Worktree: the status was empty at start. The shell wrote nothing but the stage directory.
