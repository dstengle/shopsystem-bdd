---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-125/review-1
kind: review
batch: batch-125
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/148
head: 6e7a3baf0c1fcf42bb2011d1cb160f9274f57363
range: 6c7d67a8d76b07931b31b481a7b800242ac36e98..6e7a3baf0c1fcf42bb2011d1cb160f9274f57363
result: fix-now
---

# batch-125 review 1

## Verdict

The batch builds b636's six lines: publish deposits, fetch and obtain retrieve through `contract_registry`, and the shop-folder adapter completes, returns and refuses as r1-r3 say. The checks in `## Runs` all exit 0, and no test is removed or weakened. One finding is to fix now: the new port's outcomes reach no core line, so `spec check` has error-severity v_pb2 violations at Head. That goes against decision 0127. The other findings are observations.

## Findings

### f1 Important fix now: the registry port's three outcomes reach no core line (v_pb2, decision 0127)
- item: b636
- where: spec/model/registry.md:16
The implementer's concern holds, and it belongs to this batch. The batch adds the driven port `contract registry` with three outcomes:

```model
operation deposit(contract, version)  outcomes: done → the contract
operation retrieve(contract, bounded context, version)  outcomes: returned → the contract | refused: version not deposited
```

None of `deposit done`, `retrieve returned` or `retrieve refused: version not deposited` is handled by a core line or excluded by a port line. checking r125-r127 only request the operation. checking r79 and r82 refuse on the person's own request, not on the port's outcome. `grammar/rules.md` lists v_pb2 at severity `error`, with the purpose "Every outcome the upstream may give reaches a core line or is excluded by a port line" (decisions 0116, 0127). Decision 0127, a judgement decision in force, says the same. The base has no registry area, so these violations are new. The batch-start check let them through only because v_pb2 names an outcome, not a requirement. Merged as it is, `spec check` on main reports three errors.

Fix: on b636, use `work line` and then `work batch amend b636 --finding <this finding>` to add core lines in checking for each outcome. For example, a line on the registry's refusal of a retrieve under which the specification service refuses the request and names the version, and lines on a completed deposit and a returned retrieve. Alternatively, add port lines that exclude an outcome. Then confirm `spec check` shows no v_pb2.

### f2 Minor observation: the shop-folder adapter is wired in with no technical decision, and 0139 and 0137 are not superseded (decisions 0125, 0139)
- item: b636
- where: scripts/contract_registry.py:1
Decision 0125 says a context records which adapter of a port it runs as a technical architecture decision. b636's shaping note also says the batch writes that decision and, with `work decision --supersedes`, the requirement-tier successors of 0139 and 0137. The change holds no new file under `spec/decisions/`. The docstrings of `contract_registry.py` and `contract_registry_folder.py` cite "decision 0125" as the wiring decision, but 0125 is only the general rule. These decisions are committed on the base, not on the item's branch, so this cannot be a fix on b636's branch. Write them before or with the merge.

### f3 Minor observation: obtain still names the provider/ location in core code and reaches the adapter around the port (decision 0139)
- item: b636
- where: scripts/contract_obtain.py:18
Decision 0139 says "no line or core code names a file location". The module map calls `contract_registry` "the one module the contract commands reach it through". Yet `contract_obtain` imports `from contract_registry_folder import place` directly and writes `provider/<id>/<version>/contract.toml` itself through `shop_files.committed`. `model_adapter`, `adapter_provider` and `checking_handlers_pinned` read `place` back through it. So keeping an obtained contract still goes through the shop-folder adapter's layout, whichever adapter `$SHOPSYSTEM_CONTRACT_REGISTRY` names. No line of b636 asks for this keeping to move behind the port, so this does not hold the merge. It is a gap against 0139 for the follow-up that supersedes it.

### f4 Minor observation: the default publish version is now counted from the published contract, not the highest kept one
- item: b636
- where: scripts/contract_publish.py:60
Before, `_next` took the highest version of every contract kept. Now it takes the version of the published one (`_published`). The two differ once a lower version is published explicitly after a higher one.

Reproduction:
1. `spec publish --version 1.0.1`
2. `spec publish --version 1.0.0` (1.0.1 is now superseded, 1.0.0 published)
3. `spec publish`

The new code picks `1.0.1`, which `_deposited` refuses as "a contract is kept at the version 1.0.1 already". The base picked `1.0.2`. No line names the default version, so this is hardening only. Fix: have the adapter give the highest deposited version, or keep the max-of-kept rule behind the port.

### f5 Minor observation: obtain with no adapter spec now asks the upstream after the provider check, and reports an upstream with no `github:` differently
- item: b636
- where: scripts/contract_obtain.py:50
`obtain` used to call `reached` before `holders`. Now it calls `holders` first and, when none hold the provider, `_reach` runs `contract_registry.retrieve(root, context, None)`. `_reach` re-raises only `bounded context unreachable`. So `request_gh.repo_of`'s refusal of an upstream with no `github:` is swallowed, and `no adapter spec has the provider` is reported in its place, where the base reported the missing `github:`. The probe also does a full retrieve of the published contract (a listing and one `gh api` read per version folder), only to check reachability. r89 and r103 still hold: r103 is conditioned on an `available` provider. This is an edge no line names.

### f6 Minor observation: the change is over the review size limit
- item: b636
- where: -
`## Size` gives 24 files, +850 -172, against a limit of 1000 changed lines. b636 is the batch's only item. Most of the change is the new port, its adapter split in two (`contract_registry_folder.py`, `contract_registry_github.py`), their two handler modules and the CLAUDE.md rows.
