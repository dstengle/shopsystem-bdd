---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-181/review-1
kind: review
batch: batch-181
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/203
head: a7be7d89d92739da45740ae330a6d4a27b0744c7
range: f69bd074ecc97e188ecd8de8f647a38af3d2b709..a7be7d89d92739da45740ae330a6d4a27b0744c7
result: clean
---

# batch-181 review 1

## Verdict

The batch builds both items. b861 retires and rewrites the seven glosses its lines name (preview, model line, readiness bar, amend, amendment, opening time, opening phase), each with the same word and element. b898 builds drafting r114-r118 with `work line --retire-area` and applying r48-r50 with backlog_retire_area's `lay`. The model, vocabulary, cli.toml operation table and module-map rows are in step. Every run exits 0 at `Head:`. The change is under the size limit, and no test is removed or weakened. The `retire#4` to `retire#5` changes in the corpus come from the new sense of retire and were written by the generator. No finding is fix now; there are two observations.

## Findings

### f1 Minor observation: a capability named after the area stays in the area once its `area:` is taken out
- item: b898
- where: scripts/backlog_retire_area.py:22
`capabilities` reads a capability's area as its `area:`, else its file name. spec_composition (`_field(text, "area") or path.stem`, scripts/spec_composition.py:35) reads it the same way. `lay` takes `area:` out of each capability of the area. But a capability whose file name is the area's name, such as `spec/capabilities/laying.md` for the area `laying` that b899 will retire, falls back to its file name and is still read as in the area after the lay. That is against r50's "keep no capability in the area".

The scenario does not catch it, because its capabilities are `shelves` and `racks` and the area is `shelving`. I checked whether it shows anywhere today: spec_composition lists only capabilities that hold a requirement, and r118 refuses those, so no Composition row comes back. The harm is in the reading, not in an output. The fix fits b899 or a follow-up: write the capability in no area in a way the file-name fallback cannot reach, or have the fallback skip a name that has no model file.

### f2 Minor observation: `specifies:` is taken out even when it names another area's service
- item: b898
- where: scripts/backlog_retire_area.py:462
`FIELD` takes `specifies:` out of each capability of the area, as well as `area:`. r50 asks only that the capability be kept in no area. In the scenario's own world, `specifies: service notes` names the service of another area (notes) and is still taken out. The item's Notes ask for this, and applying r25 ties `specifies:` to the area's service, so it is defensible. Still, no line of the batch asks for that change to the file. Reproduction: apply the scenario's item. `racks.md` loses `specifies: service notes`, although notes is still in the domain model.
