---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-113/review-1
kind: review
batch: batch-113
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/136
head: ce7866d87ae28aa619e4241a75e45fd0ed9677ab
range: dcd33c7be6f0abebab8f38c7f3db4f666e928036..ce7866d87ae28aa619e4241a75e45fd0ed9677ab
result: fix-now
---

# batch-113 review 1

## Verdict

The batch builds all nine lines of b672. One refusal no line asks for contradicts drafting#r73 and needs a fix. The change is also over the size limit. The three runs given are clean at `Head:`.

## Findings

### f1 Important fix now: `--import` of a pack spec/index.md already imports is refused, against r73
- item: b672
- where: scripts/backlog_import.py:419
drafting#r73 obliges the drafting service to keep the item that imports the pack whenever the person imports a pack into an item. It sets no condition about what spec/index.md imports already. drafting#r74 is the only refusal the lines ask for: a pack that does not exist. `write` also refuses this case:

```
    if pack in spec_packs.imports(root):
        raise Refused("work line: spec/index.md imports the pack %s already" % pack)
```

So a plugin pack that exists and is already in `imports:` is refused, where r73 says the item is kept. That refusal is observable behaviour no line of the batch asks for and no Implementation section gives. It also protects nothing:
- The lay goes through `backlog_pack._imports`, which returns the text unchanged when the name is already listed. I read this at scripts/backlog_pack.py:112.
- `backlog_import.unlay` keeps an import the index held at the batch's base.

`tests/scripts/test_backlog_retire.py:321` pins the refusal with `["--import", "request"]`. Fix: drop the index check in `write`, keep the import in the item, and take `["--import", "request"]` out of that test's refused list. Better, assert that it is kept.

### f2 Minor observation: a second import or retirement of one thing in the same item is refused, which no line names
- item: b672
- where: scripts/backlog_retire.py:608
`_kept` refuses a retirement the item holds already. `backlog_import.write` does the same for an import (scripts/backlog_import.py:421). r75 and r77 ("shall keep the model line / term in the item") set no such condition. The block reader rejects duplicates, so a no-op is needed in place of a duplicate append. Making it a refusal is a choice no line makes. This follows the moves block's existing pattern, so I record it rather than hold the merge. Reproduction: run `work line b1 --retire-term low` twice. The second run exits 1.

### f3 Minor observation: `--retire-model` looks only at the area of the `--into` capability, not the whole domain model
- item: b672
- where: scripts/backlog_retire.py:576
r76 refuses only when "the domain model does not hold" the model line. `retire_model` searches only `model_path(root, area_of(root, into, blocks))`. An element that another area declares is refused with reason `model line not in the domain model`, though the domain model holds it. The person can avoid this by naming a capability of the right area, and `--into` is `cli-only` in spec/adapters/cli.toml. Reproduction: retire an element of `shared`'s model with `--into notebook`. It is refused although the domain model declares it.

### f4 Minor observation: the unlay of a model-line retirement lists the model file as changed when it put nothing back
- item: b672
- where: scripts/backlog_retire_lay.py:731
`put_element` returns without writing when neither the base nor `chunk` gives the element's lines, because `chunk` is `None` there. `unlay` still appends the model file to `files`. The commit step would then name a file that did not change. In every case I read this does nothing harmful. It is noted for accuracy only.

### f5 Minor observation: the change is over the review size limit
- item: b672
- where: -
`## Size` gives 23 files, +978 -31: 1009 changed lines against a limit of 1000. All of it is b672's, the batch's only item. Most of it is the three new modules (backlog_import, backlog_retire, backlog_retire_lay), their two scenario handler files and the corpus blocks.
