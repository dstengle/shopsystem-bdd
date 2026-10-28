/tmp/work-run-i50-mge7r3r7/i50-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | from the request |
|---|---|---|---|---|
| added | supervision | r173 | **When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write one question asking the person to approve the terms the proposal adds, changes and removes. | "**When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write one question asking the person to approve the terms the proposal adds, changes and removes." (q36, line 1) |

Glossary terms: none added, changed or removed.
Decision files: none.

## Questions

1. supervision r173: the request does not say where the question is written. r117 (its capability-proposal counterpart) writes it under the proposal's `## Questions`, and no line says where a glossary-proposal gate's questions go (r85 covers capability-proposals only; r129 covers it only for a result that gives questions). If yes (under the glossary-proposal's `## Questions`): r173 reads "**When** a round of the kind `gate` that `work run` started for a glossary-proposal ends with no question, `work run` shall write under the proposal's `## Questions` one question asking the person to approve the terms the proposal adds, changes and removes." If no: r173 stays as drafted.
2. supervision r173 against r131/r132: r132 takes "a gate round's questions" as a gate round's output. So a gate round with no question gives neither a question nor its output, and r131 would also write a question naming the missing output. r117 has the same tension for capability-proposals. If yes (no question counts as a gate round's output): r132's last item becomes "a gate round's questions, or none". If no: no change, and r131 and r173 both apply.

## Cut sentences

None.
