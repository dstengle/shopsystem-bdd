---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-tie-nouns
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Q_ONE and Q_RELEASE: each condition's noun tied to the trigger's thing

Branch `gfr3/tie-nouns` from ef4c5610, head ec1e0d5d, merged as 1f0261a1.

The person approved rewording the lines behind the 13 Q_ONE findings and the 3 Q_RELEASE findings. The cause was the
same in each: a condition's indefinite noun phrase was not tied to the trigger's thing, so two different instances
could make both lines fire.

Ids are kept. The grammar, the lexicon and `## Terms` are unchanged.

## Lines changed

### work-queue r20–r24

- **Before:** "While a question is `X`, when the person runs `work answer` on a work-item that is `awaiting-answer`"
- **After:** "While a work-item is `awaiting-answer` and the question on the work-item is `X`, when the person runs
  `work answer` on the work-item"
- In r23 and r24, "an answer" became "the answer".

Why:
- The question is the one the work-item waits on, tied through the relation `question on node`.
- "a question on the work-item" was not enough. A work-item can have two questions, so the pair still clashed.
- "the answer" is the one answer `work answer` is given.

Cleared 9 L1.

### supervision r39, r40, r41

- **r39 after:** "While an initiative is `started` and a work-item kept in the initiative is `green` and no remote is
  unpushable and the initiative branch is not reviewed, when the person runs `work run` on the initiative"
- **r40:** "an initiative branch" became "the initiative branch".
- **r41:** "a `started` initiative is itemless" became "an initiative is `started` and no work-item is kept in the
  initiative".

Why:
- The lexicon has no relation from an initiative branch to an initiative, so the branch is "the" one branch.
- The green work-item is tied to the initiative through `work-item kept in initiative`.
- `itemless` is defined only in prose, which gave an L6. r41 now spells out its meaning with the same relation.
- The `itemless` entry is kept, though no line uses it any more.

Cleared 2 L1.

### supervision r71

- **Change:** "a question on the glossary-proposal is answered" became "the question on the glossary-proposal is
  answered".
- **Why:** r69's gate asks one question. "every question …" also cleared the finding, but it was dropped because the
  generated scenario lost its question.

Cleared 1 L1.

### supervision r76, r77

- **Before:** "While a change list is (un)codified, when … with a result that is `DONE`"
- **After:** "While a result that is `DONE` gives the change list and the change list is (un)codified, when … with
  the result"

Why:
- The list is the one the round's result gives. "a change list" alone still clashed, because one result could have
  two lists.
- The pair is now an L6, because `codified` and `uncodified` are defined only in prose.
- Writing "not codified" would have dropped "service" from the meaning of `uncodified`, so it was not used.

New question: Q_CODIFIED.

### migration-tools r13–r16

- **Change:** "a repository is …" became "the repository is …".
- **Why:** the repository is the one `migrate` runs in. The trigger has no object to tie it to.
- Three L6 remain, on the release conditions, which are defined only in prose. Q_RELEASE was reworded.

## Counts

| | L1 | L5 | L6 |
|---|---|---|---|
| before | 25 | 6 | 4 |
| after | 9 | 6 | 8 |

All 16 L1 are cleared. The 4 new L6 are in `EXPECTED`.

## Fallout and checks

- **Features:** the generated scenarios changed for work-queue r20–r24 and supervision r39, r41, r76 and r77.
- **Handler:** supervision_handlers.py gained a `GivenR gives` handler, which only records the relation.
- **Results:**

  | check | result |
  |---|---|
  | `pytest -n 8` | 938 passed, 1 skipped |
  | `features generate --check` | exit 0 |
  | `tools size` | exit 0 |
  | `tools check` | clean |
  | `model check` | unchanged |
