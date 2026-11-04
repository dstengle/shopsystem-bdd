---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-answers
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Q_STAGE, Q_CLOSED, Q_LINES and Q_RELEASE answered

Branch `gfr3/answers` from 42ee3f26, head 97328e92, merged as 0acac0b0. The person approved all four answers (and the
fifth, "If" precedence, written separately in 5e6a427c). Ids kept.

## Counts

| | L1 | L5 | L6 |
|---|---|---|---|
| before | 9 | 6 | 8 |
| after | 0 | 6 | 5 |

No new finding. `model check` output identical before and after.

## 1. Q_STAGE: "include" is per stage (batch-measurement)

- **Grammar:** new fun `QuotedFor : Quoted -> NP -> NP` ("include "turns" for the logged stage").
  - It translates as `resp(…, for(e_include,"turns"), measure, stage)`, so the stage unifies like any role.
  - It is read back as the existing `SDoes`/`SDoesNot` steps, with a corpus line and tests.
- **Relations:**
  - new rows `logged stage | has | transcript | one` and `logged stage | has | session file | one`;
  - `spec_typed`'s plural of "has" fixed.
- **Lines:**
  - r8/r14: "While a logged stage has a transcript that is `found`/`lost`, … include "round_trips" for the logged
    stage".
  - r13: "While a logged stage has a session file that is `empty`, …".
  - The "shall not include" Thens are kept.
- **r12 gained a condition:** "and the logged stage has a session file that is `filled`".
  - Without it, an unended stage with an empty `session.json` is a genuine clash.
  - The capability's implementation notes already said so.
- Cleared 2 L1.

## 2. Q_CLOSED: r26 means every work-item (supervision)

- **r26:** "While an initiative is `started` and a work-item kept in the initiative is closed and every work-item kept
  in the initiative is closed and no request is `asker` and no remote is unpushable, when … on the initiative, …".
  - Its Thens are unchanged.
  - The existential keeps a work-item in the scenario.
- **r27 and r28** are tied to the initiative ("a work-item kept in the initiative is …"). Otherwise a work-item of
  another initiative still fired both.
- Cleared 4 L1.

## 3. Q_LINES: every line (requests)

- All three use the relation "proposed in", tied to the trigger's request:
  - r20: "a request line proposed in the request is not settled";
  - r21: "every … is settled and a … is `accepted`";
  - r22: "a … is `refused` and every … is `refused`".
- **Checker bug fixed** (`hasu` in `grammar/check.lp`): a value given by "every K … is v" was not used when reading a
  negated defined condition. A test beside it shows a real clash of the same shape is still found.
- Cleared 3 L1.

## 4. Prose conditions defined (migration-tools)

- **New attribute** `release` of repository, with values `0.23.1`, `0.24.0`, `0.29.0`, `own` and `newer`.
- **New condition** `codified` of capability. It stays prose.
- **Def sentences:**

  | condition | defined as |
  |---|---|
  | behind | `0.23.1` |
  | outdated | `0.24.0` |
  | uncodified | `0.29.0` and a capability is not codified |
  | current | `own` |
  | ahead | `newer` |
  | idle | `own` and no initiative is open |

- Cleared 3 L6.

## Left as prose (5 L6, in `EXPECTED`)

| condition | what it lacks | question |
|---|---|---|
| codified / uncodified (change list) | a relation `capability named in change list` | Q_CODIFIED |
| fixing | a relation from a question to a review finding | Q_RESULT |
| strange | a relation from a change list to a capability | Q_RESULT |
| unparsing | a relation from a draft to a requirement | Q_RESULT |
| unheld | a relation from a result or draft to an answer | Q_RESULT |

## Verification

| check | result |
|---|---|
| `pytest -n 8 -q` | 941 passed, 1 skipped |
| `features generate --check` | exit 0 |
| `tools size --limit 300` | exit 0 |
| `tools check scripts tests` | clean |

`features generate` changed batch-measurement g8 and g12–g14, requests g20–g22, and supervision g26–g28.
