# Gate, integrate round 1 (q36)

## supervision

Added:
- [r173] **When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write one question asking the person to approve the terms the proposal adds, changes and removes.
  (from q36 line 1, the same sentence)

Changed: none. Removed: none.

## Glossary
No entry added, changed or removed.

## Decisions
None.

## Questions

1. supervision r173: the request does not say where the question is written. r117 (the capability-proposal counterpart) writes it under the proposal's `## Questions`; no line says where a glossary-proposal gate's questions go (r85 covers capability-proposals only; r129 covers a result that gives questions).
   - Reading a (recommended): r173 as drafted.
   - Reading b: r173 reads "**When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write under the proposal's `## Questions` one question asking the person to approve the terms the proposal adds, changes and removes."
2. supervision r173 against r131/r132: r132 takes "a gate round's questions" as a gate round's output, so a gate round with no question gives neither question nor output, and r131 would write a question naming the missing output as well as r173 (r117 has the same tension).
   - Reading a (recommended): no change; r131 and r173 both apply.
   - Reading b: r132's last item becomes "a gate round's questions, or none" (a changed line with a new id; r132 retired).
