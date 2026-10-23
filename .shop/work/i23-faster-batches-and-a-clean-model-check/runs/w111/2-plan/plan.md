# Plan of w111 (delivery#r17, delivery#r18)

## 1. What goes green

- **delivery#r17** (list each `@deprecated` scenario whose `@r<n>` names an accepted requirement under the work-item's `## Retires`): no scenario. Delivery is a guarantees capability (design-decision/workflow-capabilities-are-guarantees, 0065): its scenarios do not run, it is checked by `measure` on real batches. The notes confirm no `features/delivery.feature` and no `@r17` scenario under delivery. Today the skill writes no Retires list (notes §3).
- **delivery#r18** (stop, naming the scenario, and commit no work-item, when an added or reworded scenario names a requirement no drafted work-item accepts): no scenario, for the same reason. Today the skill has no such check (notes §3, SKILL.md "Before anything"/"Drafting").
- Deprecated scenarios retired by this work-item: none (it has no `## Retires` section).

Nothing runs red. The implementer's red is the skill text read against r17 and r18. The researcher's open question ("formulate scenarios first, or work from the requirements only") is settled by 0065: work from the requirements only.

## 2. Where the change lands

- `skills/delivering-an-initiative/SKILL.md`: add the r18 check before any `work add`; add the r17 Retires step after each `work add`; rewrite the "Commit them, alone" step, because `work add` already commits each work-item (notes §2, §5).

That is the whole file set. Removed from the researcher's set, and why:
- `scripts/work`, `scripts/workqueue.py`, `tests/scripts/test_work_add_title.py`, `tests/scenarios/test_work_queue.py`, `tests/scenarios/work_queue_add_steps.py`: no `--retires` option (decision 2).
- `scripts/features_report.py`: `deprecated --json` keeps its shape (decision 3).
- `features/delivery.feature`: no scenarios, because delivery is a guarantee (0065).

## 3. Decisions

1. **No scenarios and no step definitions for r17/r18.** Rests on design-decision/workflow-capabilities-are-guarantees: delivery is a guarantee checked by `measure`, and its scenarios are not run.
2. **The Retires list is written by the skill, not by a new `work add --retires` option.** After `work add` has written and committed a work-item, the skill appends a `## Retires` section to that work-item file. Once every work-item of the draft is written, it commits those work-item files alone, in the skill's existing `work: draft <initiative>` commit, and only when there is a change to commit. Rests on delivery#r3 (commit the drafted work-items alone) and on the work-item's `accepts` scope: it accepts only delivery requirements, and a new `work` CLI option would change work-queue behaviour that no accepted requirement asks for. The narrator sees the same work-items with the same Retires list under either path; the only difference is one extra commit.
3. **The skill finds the deprecated scenarios by reading `features/` itself**, taking each `@deprecated` scenario's own `@r<n>` tags. It does not use the replacement tags from `features deprecated --json`. Rests on delivery#r2 (draft from `spec/`, `features/`, `.shop/work/`) and delivery#r17 (the deprecated scenario's own `@r<n>`). Notes §2 show that `deprecated --json` gives the replacement's tags, so it cannot be relied on for this.
4. **Shape of each Retires entry:** the scenario's exact title as it stands in the file, including its " (deprecated)" suffix, quoted, one per line, with its feature file. Rests on delivery#r17, red-green#r2 and review#r10: the implementer removes those scenarios with `features retire <title>`, which matches the exact title, and the readers named in notes §3 (bdd-red-green, bdd-implementer, the reviewers, code-scout) read a list of quoted titles, as in w110.
5. **The r18 check runs before the first `work add`.** It covers every added or reworded scenario of the initiative's `formulated` capability-proposals against the full set of planned work-items. On a miss, the skill stops, names each such scenario (file and title), and runs no `work add`. Rests on delivery#r18 ("commit no work-item"): `work add` commits as it goes (notes §2), so a check after drafting would already have committed work-items. It also rests on delivery#r7: stop, say why, change nothing.

## 4. Tests the decisions break

None. Verified from the notes: no test reads the delivering skill (§3, §4), no test asserts that a work-item has no `## Retires` section (§4), and decisions 2 and 3 leave `scripts/work`, `scripts/workqueue.py` and `scripts/features_report.py` unchanged, so the tests that run them (test_work_add_title.py, work_queue_add_steps.py, test_work_queue.py, test_features_scenarios.py, test_features_deprecating.py) are untouched.

## 5. Open cases (for the implementer to name, not choose)

- How the skill tells which scenarios "the initiative's formulation added or reworded" (for example, the formulation commits of its capability-proposals, or the proposal's own record). The skill text must name its source.
- A deprecated scenario whose `@r<n>` tags name requirements accepted by two different work-items: whether it is listed under both.
- A work-item with no matching deprecated scenario: whether the skill writes an empty `## Retires` section or none at all.
- An `@deprecated` scenario that carries no `@r<n>` tag.
- A re-run of the skill (delivery#r8) on an initiative whose work-items already exist: whether r17 adds Retires to work-items it did not draft in this run.
