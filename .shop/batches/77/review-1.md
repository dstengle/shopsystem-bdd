---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-77/review-1
kind: review
batch: batch-77
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/101
head: c932476890b0d641c840e78d1557e188e04dc14c
range: c536816646451ca300213b85b3eae729f3e2e532..c932476890b0d641c840e78d1557e188e04dc14c
result: clean
---

# batch-77 review 1

## Verdict

The batch builds all five lines. b544 (consistency#r35) makes two layers' terms of one actor one referent in the logical form (`spec_lf_core.State.constant`) and one thing in the check's facts (`spec_lf_ids.Ids.actors`). b547 (checking#r64-r67) adds `spec prepare --contract <version>`, which prints a `contract.toml` in the contract form. The contract holds each operation's governing requirements and properties, and `spec check` fails a property that refers to an undeclared operation (v_m8). No test is removed or weakened. The size (845 changed lines) is under the limit. Every run exits 0. The new modules and test handlers have rows in `CLAUDE.md`'s module map. There is nothing to fix now; three observations follow.

## Findings

### f1 Minor observation: v_m8 now also fails a property's parameter or event, and an event line's stray segment is refused; checking#r67 asks only for an operation
- item: b547
- where: scripts/domain_model_props.py:77
checking#r67 asks the check to fail a property that refers to an operation that does not exist. `_declared` also fails two other cases under v_m8:

- `idempotent by <parameter>` naming no parameter of the operation;
- `followed by <event>` naming no declared event.

Separately, `domain_model_parse.Reader.event` (scripts/domain_model_parse.py:185) now refuses any `;` segment of an event line that is not `delivery:` or `when:`. No line of the batch asks for these failures or this refusal. The model's `object property` declares only `refers to → operation`. They do fit v_m8's catalogued purpose ("the domain model is internally consistent"), and removing them would let dangling references through silently, so this is not graded fix now. Fix: state them in a line, for example a property that refers to a parameter or an event that does not exist fails the check, so that the scenarios hold them.

### f2 Minor observation: the property pattern also reads the `outcomes:` part of an operation line
- item: b547
- where: scripts/domain_model_props.py:34
`PROPERTY.finditer(text)` runs over the whole logical line, including the text after `outcomes:`. A value ends at `\soutcomes:`, but nothing stops a key from matching after it. Reproduction: the line below would lose part of its refusal reason, and then fail v_m8 because `a reader` is no declared event.

```
operation lend(book)  outcomes: done → the book | refused: not followed by a reader
```

I searched every `spec/model/*.md` in the tree: no model line holds `idempotent by`, `compensated by` or `followed by` today, so nothing reads differently now. Fix: match properties only in the text before `outcomes:`.

### f3 Minor observation: the CLI table gives the version option the parameter `contract`, with example `contract-1`
- item: b547
- where: spec/adapters/cli.toml:1382
The model declares `operation prepare(contract)`, so the parameter is the contract object. The CLI table maps it to `--contract`, which `scripts/spec` reads as the version (`metavar="VERSION"`). Its example, `contract-1`, is not a version. The contract this produces would print `version = "contract-1"`. Nothing fails today. A version parameter, or an example such as `1.0.0`, would make the table say what the option means.
