---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-close-r3
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Revision 3 closed: where the branch stands and what is open

## Where it stands

- **The check and the generator:** `model logic` and `features generate` run on per-requirement facts and one clingo
  check (design-r3, plan-r3, gate-r3-L1..L6). The telingo whole-system solve is gone.
- **Findings on the live spec:**
  - `model logic` finds 0 L1, 6 L5 and 5 L6, in about 1.3 s;
  - `features generate --check` takes about 1.1 s.
- **The suite:** 941 passed and 1 skipped in about 16 s wall, down from about 5 minutes.
- **Since S12:**
  - the checker's gaps (report-checker-gaps);
  - nouns tied to their triggers (report-tie-nouns);
  - Q_STAGE, Q_CLOSED, Q_LINES and Q_RELEASE answered (report-answers);
  - "If" precedence written in `spec/universal.md` and design-r3 §6.

## Open, recommended, not started

1. **Glossary relations** that would define the last prose conditions and clear the 5 L6:
   - `capability named in change list`, for codified and uncodified;
   - the relations fixing, strange, unparsing and unheld need (report-answers, "Left as prose").
2. **The 6 L5:** reword the untriggered event obligations U4 (twice), U7, U8, review r5 and spec-migration r10 so
   each has a trigger or states a state.
3. **`model check`:** 53 violations, 16 warnings and 29 unresolved references. This count is unchanged by revision 3
   and should be looked at before any merge.
4. **Carried from earlier:**
   - 115 prose condition definitions;
   - 17 unmerged ubiquitous statements;
   - call 16;
   - q47;
   - the 25 open proposals in 0.29 lines;
   - leftover workflow worktrees under `.claude/worktrees/`.
5. **Merging `gf-conversion` to main is the person's call.**
