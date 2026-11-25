---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-90/review-1
kind: review
batch: batch-90
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/113
head: 974969dd8d201577ac1c09bc9a12db03ca0e53f2
range: 744b5f0b9089c88f5d54b06b52357b2849ff8161..974969dd8d201577ac1c09bc9a12db03ca0e53f2
result: clean
---

# batch-90 review 1

## Verdict

The batch builds all eight of b348's lines (checking#r73 to r80). Each line has a scenario whose handler checks it against real files and the real output: the version kept, published ones superseded, the version or the requirement named on a refusal, requirements and own terms kept with a pack term left out, the published contract returned with nothing changed, and an older version fetched by its number. All five runs exit 0, and the change is under the size limit. The rules and module map are kept: `contract_publish.py` and `checking_handlers_publish.py` have rows, the `contract_form.py` row is updated, the commands reference documents both commands and `spec forms` lists the new form. No test is removed or weakened. The guard added to `decision_tiers_handlers_four.py` only stops a crash on a Given with no instance name. I found nothing to fix now; there are two observations and one drop.

## Findings

### f1 Minor observation: `spec publish` refuses a malformed version, which no line asks for
- item: b348
- where: scripts/contract_publish.py:434
`publish` refuses a `--version` that does not match `VERSION`, with the reason `version not a version`. No line of b348 asks for this refusal, and the model does not declare it: `specification.publish` declares only `version already published` and `requirement not in the language` (spec/model/specification.md:609). The guard does real work, though. Without it, `--version ../../x` would write `contract.toml` outside `.shop/contracts/`, because the version is joined into the path (`KEPT / version / FILE`, line 446). Removing it would be wrong, so this is recorded and does not hold the merge. Fix: give it a line and a declared reason through `work idea`, e.g. "While a version is not a version, if the person publishes a contract with the version, then the specification service shall refuse the request and name the version", and add the reason to the operation's `refused:` list.

### f2 Minor observation: the model lets a contract hold design-decisions, but nothing puts any in it
- item: b348
- where: spec/model/specification.md:621
The new relation `holds → term | design-decision (many)` lets a contract hold design-decisions. No line of b348 says so, and `contract_form.render` writes no decisions into the contract. Only model consumers see this, such as `spec prepare --contract`'s object table and the grammar's "holds" frame for contract and design-decision; it changes no output a line checks. Either take `design-decision` out of the relation, or add a line for it when a contract is meant to carry the decisions.

### f3 Minor drop: a registry handler is squeezed between `W.local` calls
- item: -
- where: tests/scenarios/checking_handlers_publish.py:899
The `@handler("ThenK_A", "contract")` fallback `untaken` sits right after `W.local("ThenK_A", "contract")(then_status)`, and `W.local("ThenPrints")` follows it with no blank line. Ruff passes and the behaviour is right. Moving the fallback below the `W.local` registrations would make the module read more easily, but that is polish.
