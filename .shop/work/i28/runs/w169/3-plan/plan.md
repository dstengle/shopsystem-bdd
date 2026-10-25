# Plan: w169 (spec-integration#r43, round-ids-avoided)

## 1. What goes green

- **spec-integration#r43**: when an `integrate` round is given requirement ids that other initiatives' drafts add, `initiative-round` numbers the round's added lines above every id it is given on the same capability.
  - Scenarios: none accepted, and none will be. `spec-integration` is `group: guarantees` (design-decision/workflow-capabilities-are-guarantees, 0065): `measure` checks it on real batches, so it has no Gherkin scenario. `work_items.py` (108, 114-131) passes a work-item whose requirements are all guarantees when it collects no test. Both research runs saw this: `--work-item w169` collects 0 of 178.
  - Why it is unmet today (notes §3, §6): the round's text (agents/initiative-round.md, kind `integrate`), the skill's step 2 (skills/integrating-a-proposal/SKILL.md:23), the writer's numbering rule (agents/capability-writer.md:18-21) and the format doc (docs/capability-format.md:159-163) all number an added line above the capability's own ids, its `retired` list and this initiative's earlier drafts only. Nothing tells the round to look at ids it is given from other initiatives' drafts. So a round numbers `r98` again when i25 and i26 have already drafted `supervision#r98`.
- Retired scenarios: none. The work-item has no Retires section.

## 2. Where the change lands

- `agents/initiative-round.md`: kind `integrate`. When the brief from `work run` gives the requirement ids that other initiatives' drafts add, the round passes them to the writer in its dispatch. It then checks that every id in its change list's `adds` is above every given id on the same capability, and sends the drafts back to the writer when one is not.
- `skills/integrating-a-proposal/SKILL.md`: step 2's numbering rule. Added rows also go above every id the round is given on the same capability.
- `agents/capability-writer.md`: the numbering paragraph (18-21). A new line goes above every id the capability has used or retired, and above every id its input prompt gives for that capability.
- `docs/capability-format.md`: one sentence at the id rule (159-163) for the given ids.

Removed from the researcher's set, by decision D1:
- `scripts/supervise_brief.py` (`integrate_lines`)
- `tests/scenarios/supervision_integrate_steps.py`
- `features/supervision.feature`

Giving the ids in the brief is supervision#r102, which w170 accepts. That code and its scenario belong to w170, and two work-items editing `integrate_lines` side by side would collide at merge.

## 3. Decisions

- **D1: who finds the other drafts' ids.** The researcher left two readings open: (a) `work run` gives the ids in the round's brief; (b) the round or the writer reads other initiatives' drafts itself. Taken: (a). supervision#r102 says `work run` gives the round every requirement id that another initiative's kept, unapplied drafts add, and r43 says the round acts on the ids "it is given". So w169 changes only what the round, the writer, the skill and the doc do with ids they are given. The round reads no other initiative's files, so the question of whether drafts on other branches can be seen (notes §3, last paragraph) is w170's.
- **D2: what "above" covers.** The added line's id goes above the highest of three sets: the capability's used ids, its `retired` list, and every given id on the same capability. Given ids on other capabilities do not affect its numbering. This rests on spec-integration#r12 and #r43 ("on the same capability").
- **D3: the round checks, not only the writer.** The round checks its change list's `adds` against the given ids and sends back a draft that fails, the same way it already checks the change list in both directions. This rests on spec-integration#r43, whose subject is `initiative-round`, and on the Implementation's "verifies the change list".
- **D4: no ids given.** When the brief gives no such ids, the numbering is today's (spec-integration#r12). The texts say the extra rule applies only when ids are given.

## 4. Tests the decisions break

None. The notes searched `tests/` for the integrate brief's text (`Drafts path`, `Accepted lines`, `Request:`, `integrate_lines`, `brief.md`) and found no assertion on it. Under D1 every file in this set is agent, skill or doc text, and no test reads these four files' wording. No Python file changes, so `tools size` is unaffected.

## 5. Open cases (for the implementer to name, not to choose)

- The label the round's text uses for the given ids. It must match the label w170's `integrate_lines` writes, and that label is not fixed yet. The implementer names one in the agent text and records it in their report, so w170 uses the same one or the gap shows up.
- How a given id that equals one of the capability's own `spec/` ids is handled. This can happen when the other initiative's draft was applied after the brief was written. Numbering above the highest id already covers it; the texts can say so or stay silent.
- Given ids of the form `term/<term>`. Terms carry no number, so r43 does not touch them. Whether the texts say so is left open.
- A round from round 2 on, which works from the person's answers: whether it reuses round 1's given ids or the ids in its own brief. The texts should say it uses its own brief's ids.
