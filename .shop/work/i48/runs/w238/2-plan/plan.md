# Plan of w238 (supervision r188, r189)

## 1. What goes green

- **supervision#r188**: "an integrate round started for a capability-proposal that redrafts some of its lines leaves the proposal with the requirement ids its change list does not name" (features/supervision.feature:1168). Red today because its first Given (line 1171, the `adds/changes/removes naming` form with `for thing`) has no step. Behind that, `Changes.write_proposals` in its own-proposal branch calls `rewrite_lists`. That call replaces all three lists, so p1 would lose thing#r4, thing#r2 and thing#r3.
- **supervision#r189**: "an integrate round started for a glossary-proposal that redrafts some of its terms leaves the proposal with the terms its change list does not name" (features/supervision.feature:1180). Red today because the Given at 1184 has no step: the existing glossary-proposal step at supervision_proposal_steps.py:133 needs a `## Questions` clause. The steps at 1186 ("a round of the kind integrate is started for g1, redrafts the term …") and the Then at 1189 are not defined either. Behind that, the glossary branch of `write_proposals` writes `glossary.md` fresh from the change list's terms and never reads the held g1.
- The Thens at 1177 and 1189 never ran, so nobody knows yet whether steps exist for them.
- Retired scenarios: none. The work-item has no Retires section.

## 2. Where the change lands

- `scripts/supervise_change.py`: in `write_proposals`, the own capability-proposal branch keeps the held ids that the change list does not name and still rewrites the drafts-path sentence. The glossary branch writes into the glossary-proposal the round was started for, when `own` is one, and keeps its unnamed terms. `rewrite_lists` stays as it is for the apply round. The docstrings and the module header name r188 and r189.
- `tests/scripts/test_supervise_change.py`: rewrite the p1 assertion (see part 4). Add a unit test for a glossary-proposal that keeps its terms.
- `tests/scenarios/supervision_integrate_steps.py`: new steps for the Givens at 1171 and 1184, the glossary round at 1186, and the Thens at 1177 and 1189 where they are missing. It has 48 lines of room. If it would go over 300 lines, the new steps go into `tests/scenarios/supervision_reintegrate_steps.py` (125 lines of room).
- `tests/scenarios/supervision_reintegrate_steps.py`: its p1 integrate step (near line 56) may already serve line 1174. Extend it only if "redrafts thing#r5 and" does not match. It also takes any steps that do not fit above.

Removed from the researcher's set: `scripts/supervise_rounds.py`. The decisions below need no round kind passed in. Apply already calls `rewrite_lists` (line 175, r145). Integrate already passes `own` (line 206), and that is enough to pick the own glossary-proposal. At 275 lines, it is also the file with the least room.

## 3. Decisions

1. **Integrate merges into its own capability-proposal; apply still replaces.** In the own branch of `write_proposals`, every held id the change list does not name stays in the list it was in. Rests on supervision#r188. The apply round's `rewrite_lists` path is not touched (supervision#r145, pinned by features/supervision.feature:1129).
2. **A named id goes where the change list puts it.** If the change list names an id the proposal already holds, the id sits in the list (adds, changes or removes) the change list gives, and in no other. Rests on supervision#r188, which keeps only ids the change list does not name, and supervision#r148, under which the proposal is rewritten from the round's drafts. This is unlike `merge_lists` (r187), which only appends. So the own branch does not simply call `merge_lists` unchanged.
3. **The glossary-proposal the round was started for is the one rewritten.** When `own` names a held glossary-proposal (found by `kind: glossary-proposal`, not by the file name `glossary.md`), the round's glossary terms are written into that file. Its unnamed terms are kept, as in decision 2, and its drafts-path sentence names the round's kept drafts. No `glossary.md` is written beside it. Rests on supervision#r189 ("a glossary-proposal it was started for"), with supervision#r148 by analogy (no second proposal), and design-decision/the-glossary-is-a-target-of-spec-work. This also settles the researcher's naming conflict: the scenario's g1.md is found by its kind.
4. **Every other glossary case keeps today's behaviour.** When the round was not started for a glossary-proposal, the glossary branch still writes a fresh drafted `glossary.md` (supervision#r171, pinned by features/supervision.feature:1575-1578). That covers a round started for a capability-proposal or for the initiative. Neither r189 nor r187 covers merging into a glossary-proposal the round was not started for, so this work does not change that case (see part 5).
5. **The status move is unchanged.** `supervise_rounds.py:208` still moves the started proposal (p1 or g1) from awaiting-answer to drafted (supervision#r142).

## 4. Tests the decisions break

- `tests/scripts/test_supervise_change.py::test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal`, line 37. It asserts that p1, the own proposal, ends with only `adds: [thing#r5]`, which drops its held thing#r1. Decision 1 breaks it. Rewrite it to assert that p1's adds are thing#r1 then thing#r5, and keep its p2 assertions (lines 38-41) as they are, because the r187 merge path does not change. The test name stays true.
- The research notes found the other tests sound under these decisions: the other unit tests in that file (lines 44-63), and features/supervision.feature at 1129 (r145, apply), 1157 (r148), 1559-1568 (r187) and 1575-1578 (r171, fresh glossary write). Decision 4 keeps 1575 as it is. Decision 1 leaves the apply path alone, so 1129 is kept.

## 5. Open cases

- An integrate round started for a capability-proposal or for the initiative, whose change list names the glossary while the initiative already holds a glossary-proposal. Decision 4 keeps today's fresh write, which overwrites `glossary.md` if that is the held file. The scenarios are silent on this, and the implementer should name it in the report.
- A change list that names the same id in two of its own lists. Under decision 2 it ends up in both, as the change list gives it.
- An own capability-proposal whose change list names a held id under a different capability's entry. This is not reachable through `argues` matching, but the implementer should name it if seen.
- r189's scenario has no apply-round step before the integrate round. Whether "every other round ends" covers the apply round that an awaiting-answer proposal with Answers starts is for the step author to confirm once the scenario is red.
