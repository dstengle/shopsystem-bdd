# Plan of w103: delivery#r17, delivery#r18

## 1. What goes green

Delivery is a guarantees capability (`group: guarantees`; design-decision/workflow-capabilities-are-guarantees, 0065): it is checked by `measure` on real batches, and its scenarios are not run as fixture sessions. `features/` has no `delivery.feature` (notes, "Accepted scenarios"), and none is needed. This answers the notes' first question with reading A, by decision 0065.

- **delivery#r17** (Retires listed when drafting). No scenario. Not met today: the skill's Drafting steps 1-3 call only `work add`, which writes front matter and a title, so no `## Retires` section is ever written (notes §3, rows SKILL.md and workqueue.py:add).
- **delivery#r18** (stop on a formulated scenario no drafted work-item accepts). No scenario. Not met today: the drafting path goes from `work add` to the commit with no such check, and `model check` is not run on that path either (notes §5).

The work-item retires no deprecated scenario.

The work is done when `skills/delivering-an-initiative/SKILL.md` gives both steps. No test reads the skill (notes §3; I searched `tests/` for `delivering-an-initiative` and `SKILL.md` and found nothing), so the implementer has no red to see. The suite and `tools size --limit 300` must stay as they are.

## 2. Where the change lands

- `skills/delivering-an-initiative/SKILL.md`: Drafting gets two new steps:
  - after each `work add`, the skill writes the work-item's `## Retires` section (r17);
  - after all the work-items are drafted and before "Commit them, alone", the skill checks the formulated scenarios and stops if one names a requirement no drafted work-item accepts (r18).
  
  Two Red Flags lines are added: a work-item drafted without its Retires, and a commit made after an unaccepted scenario was found.

Removed from the researcher's set, because of decision D1 below: `scripts/workqueue.py`, `scripts/work`, `scripts/features_report.py`, and the `work add` tests (`tests/scripts/test_work_add_title.py`, `tests/scripts/test_work_item_ids.py`, `tests/scenarios/test_work_queue.py`). Not edited, as the notes say: `scripts/model_work.py`, `scripts/work_items.py`, `scripts/supervise_brief.py`, `scripts/model.lp`, `spec/capabilities/delivery.md`.

## 3. Decisions

- **D1. The skill writes the Retires section itself; `work add` gains no option.** After `work add` prints the id, the skill appends the section to the new work-item file. This rests on delivery#r17, which puts the listing on `delivering-an-initiative`, and on delivery#r2, which already has the skill read `features/` and write under `.shop/work/`. The capability's "Implementation, may change" names only the skill. The narrator sees the same section either way. This answers the notes' second question.
- **D2. Which deprecated scenarios.** They are the scenarios tagged `@deprecated` in the feature file of the work-item's `under:` capability (`features/<capability>.feature`, the pairing by name), whose `@r<n>` tag names a requirement the work-item accepts. A range in `accepts:` counts as each id in the range. The skill reads the tags in the feature file itself and does not use `features deprecated --json`, which does not carry a scenario's own tags (notes P1). This rests on delivery#r17, delivery#r2 and design-decision/scenario-names-requirement-by-tag (0023).
- **D3. What a Retires entry says.** One bullet for each scenario, giving its full title as `features retire` takes it, with " (deprecated)" in it. This rests on delivery#r17 and on red-green#r2, which makes the implementer remove exactly the scenarios listed under Retires with `features retire`. When no scenario qualifies, the work-item gets no `## Retires` section, since r17 asks for a list of each such scenario and here there are none.
- **D4. Which scenarios the r18 check covers.** They are the scenarios that the initiative's `formulated` capability-proposals' formulation added, or whose wording it changed, in `features/`. The skill finds them from the git history of `features/` alone, through the formulation commit that each proposal's body records ("formulated in <commit>"). For each such scenario it takes its `@r<n>` tags, read as `<capability>#r<n>` with the capability paired to the feature file by name. It checks them against the `accepts:` of the drafted work-items and of the initiative's work-items that are not `withdrawn` (as in Drafting step 1). This rests on delivery#r18, and on delivery#r2, because the git history is read only for `features/`.
- **D5. How the r18 stop happens.** The check runs after drafting and before the commit. When it finds a scenario that no work-item accepts, the skill deletes the work-item files this session drafted, names each such scenario (its feature file and title) and the requirement it names, and stops without committing or starting `work run`. This is the same as the existing refusal path for `work add`. It rests on delivery#r18 ("commit no work-item") and delivery#r7 ("change nothing").

## 4. Tests the decisions break

None. D1 to D5 change only `SKILL.md`, and no test reads it. I searched `tests/` for `delivering-an-initiative` and `SKILL.md` and found no match; the notes' search agrees (notes §3, §4). Because D1 leaves `work add` unchanged, the `work add` tests the notes list stay as they are.

## 5. Open cases

- A `formulated` proposal whose body records no formulation commit, or names a commit that cannot be found: the implementer must name what the skill does then (r7's stop is the nearest line).
- The case where every requirement is already accepted (step 1 goes straight to `work run`): whether the r18 check still runs when nothing is drafted is not stated.
- A deprecated scenario whose `@r<n>` names a requirement that a work-item from an earlier initiative accepts.
- A scenario with no `@r<n>` tag, or whose feature file pairs with no capability.
- Out of this work-item, for the implementer to log as an observation and not fix: notes defect D1, where `--work-item` with no scenario collected passes on unrelated tests. Also, `model check` flags w103 itself (an accepts with no scenario, and v_w4) even though delivery is a guarantee.
