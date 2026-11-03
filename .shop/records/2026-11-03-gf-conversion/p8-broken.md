---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-p8-broken
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# P8: the supervision scenarios the new flow breaks

P8 makes the formulate round a script with no session and removes the formulation-question paths (design §13.1).
Eleven scenarios of `tests/scenarios/test_supervision.py` fail because of that, beyond the 23 of
`baseline-failures.txt`. Each tests a 0.29 supervision line that P12 retires or restates when it converts supervision.
No other test fails outside the baseline.

| scenario (test name) | 0.29 lines | why it fails now |
|---|---|---|
| `test_when_the_apply_round_work_run_started_for_a_capabilityproposal_ends_having_applied_its_drafts_a_formulate_round_is_started_for_the_proposal` | r83 | expects a `claude` session for the formulate round; it is now `features generate`, and the fixture's capability is not codified, so the script stops naming `migrate upgrade` |
| `test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_ends_without_giving_a_question_the_proposal_is_formulated` | r83 | the same: the round is a script, refused on an uncodified capability |
| `test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_gives_a_question_the_proposal_is_awaitinganswer_deprecated` | r112 | a formulate round gives no question |
| `test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_gives_questions_each_is_written_under_the_proposals__questions_deprecated` | r113 | the same |
| `test_a_capabilityproposal_whose_every_question_from_its_formulate_round_has_an_answer_is_given_to_a_formulate_round_with_the_answers` | r116 | the route back from formulate is removed: an answered question goes to the gate's next round (apply) |
| `test_a_formulate_round_that_formulates_nothing_because_the_proposals_answers_change_lines_not_in_spec_leaves_the_proposals_status_as_it_was` | r149, r152 | `nothing_formulated` is removed |
| `test_a_formulate_round_that_formulates_nothing_because_the_proposals_answers_change_lines_not_in_spec_is_followed_by_a_new_integrate_round_for_the_proposal_deprecated` | r149, r153 | the same |
| `test_a_stages_result_giving_output_is_taken_as_its_stages_output[formulate round-…thing#r4…]` | r132 | the formulate round's output is the generated feature, not a session's scenario |
| `test_a_stages_result_giving_output_is_taken_as_its_stages_output[formulate round-…steady…guarantees…]` | r132, design-decision 0065 | the same (the route after the answered formulate question now runs apply) |
| `test_a_who_whose_result_gives_neither_a_question_nor_missing_puts_a_question_naming_it_under_nodes__questions_and_makes_node_awaitinganswer[formulate round-…]` | r131, r132 | `unformulated` and its question are removed: `features generate --check` is the guard |
| `test_the_questions_a_whos_result_gives_go_where_and_node_makes_its_transition_from_from_to_to[formulate round-…]` | r112, r113 | a formulate round gives no question |

The baseline's `test_a_formulate_round_that_formulates_nothing_…_is_followed_by_a_new_integrate_round_for_the_proposal`
(no `_deprecated`) still fails, as it did, for its missing step definition.

For P12: the lines formulation lists `moved to supervision` and supervision's own formulate lines (r83, r112, r113,
r116, r131, r132 for formulate, r149, r152, r153) are restated by groups that say the new flow: an approved proposal's
formulate round runs `features generate` for its service capabilities, checks with `--check` and `model check`, commits
`features/` and sets the proposal `formulated`; an uncodified capability or a failed generation is the round's fault.
The integrate round's check (`uncodified`, two send-backs, then the question whose answer goes back to integration)
needs groups of its own too.
