# Plan of w142: delivery#r15, answers appended to the ledger with `work note`

## 1. What goes green

- `delivery#r15`: "When the person gives an answer, `delivering-an-initiative` shall append one line naming it to the initiative's ledger with `work note`." No scenario: delivery is a guarantees capability (design-decision/workflow-capabilities-are-guarantees) and has no feature file. The work-item's review judges it (supervision r64, r65; blocked by w125).
- It falls short today because `skills/delivering-an-initiative/SKILL.md`, section "Fixes, rulings and the ledger", has each *ruling* appended by hand to `.shop/scratch/run/ledger-<initiative>.md`, an untracked scratch path, and names no command (notes part 3). It also has the ledger moved to `.shop/records/archive/` once every work-item is `green` or `withdrawn`.
- Retired: `delivery#r16` (archiving the ledger) is in the capability's `retired:` list. The work-item says the skill must say so. No deprecated scenario is involved, since delivery has none.

## 2. Where the change lands

- `skills/delivering-an-initiative/SKILL.md`: the one file changed.
  - The ledger bullet: each answer the person gives becomes one line naming it, appended with `python3 <scripts>/work note <initiative> <line>`. That writes and commits `.shop/work/<initiative>/ledger.md`.
  - The archive bullet goes.
  - The section heading and its words say "answer", not "ruling".

Removed from the researcher's set, and why:

- `agents/initiative-round.md`: its scratch-ledger paragraph is spec-integration#r40, which work-item w144 accepts ("initiative-round appends its ledger line with work note"). It is not r15's.
- `spec/decisions/0059-the-session-keeps-the-gate.md`: an accepted decision file is not edited (design-decision/answers-not-rulings states the rule). 0059 is superseded by design-decision/the-context-runs-without-a-coordinator, and its ledger sentence is replaced by design-decision/the-ledger-is-tracked. The conflict is already settled in the records.
- `scripts/work`, `scripts/workqueue_note.py`, `scripts/workqueue.py`: read-only. `work note` already does what r15 needs, by probe (notes part 2). No change.
- `scripts/workqueue_answer.py`: not changed (decision 2).

## 3. Decisions

1. **The answer step uses `work note`, with the tracked ledger path.** The skill appends the answer's one line with `work note <initiative> <line>`, never by hand, and names the ledger `.shop/work/<initiative>/ledger.md`. The commit that `work note` makes is the skill's only commit apart from a trial's fix drafted with `work add`. The Red Flags line "committing anything but a trial's fix" is widened to allow it. Rests on delivery#r15 and design-decision/the-ledger-is-tracked.
2. **"The person gives an answer" binds the skill, not `work answer`.** r15's subject is `delivering-an-initiative`. So the line is appended by the skill when the person answers in its session: a question `work run` printed, or one the skill put under r21 or r22. `work answer` (a work-queue script that writes `## Answers` in the work-item) is not changed to write the ledger. The skill does not start running `work answer` either: "Writing answers and starting `work run` again" is in delivery's Not yet. Rests on delivery#r15 (its subject) and delivery's Not yet. This is the notes' reading (b). Reading (a) would change a script of another capability (work-queue), which r15 does not accept.
3. **The archive step goes.** The bullet moving the ledger to `.shop/records/archive/` is removed, not rewritten. Rests on the retirement of delivery#r16 and on design-decision/the-ledger-is-tracked: the ledger is "tracked and archived with the initiative", so the skill does not move it. The skill does not mention r16 by id. It just no longer archives anything.
4. **"Answer", not "ruling".** The section heading and the bullet say answer. Rests on design-decision/answers-not-rulings and on r15's wording.
5. **What the line names.** The line names the answer: the work-item or question it answers, and the answer in the person's words, on one line. `work note` refuses a line break (notes part 2), so an answer with several lines is put on one line before it is noted. Rests on delivery#r15 ("one line naming it").
6. **A refused `work note`.** If `work note` exits non-zero, the skill shows its `work: <why>` line and stops, writing the ledger by no other means. Rests on delivery#r7.
7. **The empty-note defect** (notes part 6) is work-queue's (r19-r21), not delivery's. It is not fixed here. Under decision 5 the skill's line is never empty.

## 4. Tests the decisions break

None. The researcher searched `tests/` and found no test that reads `SKILL.md`, `skills/`, the scratch ledger path or `agents/initiative-round.md` (notes part 4). The plan changes no script, so `tests/scenarios/work_queue_note_steps.py` (work-queue r19-r21) is untouched. The size limit is not involved: the plan changes no Python file.

## 5. Open cases

- The exact wording of the ledger line: a prefix such as "answer:", and how the work-item id or question is quoted. The implementer names the form in the skill.
- An answer the person gives that answers none of the printed questions, e.g. a general instruction: whether it counts as an answer under r15. The implementer names how the skill treats it; the scenarios are silent.
- Several answers in one message: one `work note` per answer, or one line naming all. The implementer names which.
- The order of the steps when an answer also leads to a fix drafted with `work add`: which commit comes first.
