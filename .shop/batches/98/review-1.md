---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-98/review-1
kind: review
batch: batch-98
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/121
head: c194a1e1c098a2be7089d5471a8f1d47548cd349
range: 63ecf83f1d03ead1a08ab686e2b38481b859b1b0..c194a1e1c098a2be7089d5471a8f1d47548cd349
result: clean
---

# batch-98 review 1

## Verdict

The batch builds all three items. checking#r102: `spec obtain` now refuses a reached bounded context whose contents read fails as `bounded context failing`, naming the context. upgrades#r44: `migrate upgrade` rewrites old command lines in the instructions files in its one commit. batches#r116: a model line that restates an object is laid in place of it and put back on the unlay. No test was removed or weakened, every run exits 0 at the head, and the change (+621 -101) is under the 1000-line limit. Nothing needs fixing before the merge; the observations below are edges the lines do not exercise today.

## Findings

### f1 Minor observation: "restate an element" is built for objects only, not for services, events or actors
- item: b598
- where: scripts/backlog_model_elements.py:268
The vocabulary defines an element as "an object, an attribute, a value, a relation, a service, an operation, an event or an actor" (spec/vocabulary/specification.md:215). `restates` returns True only for a header that starts with `object `. Operations already had their own path (backlog_model_ops). A restated service still keeps every operation the line leaves out. A restated actor or event whose header text changes (for example `actor the person kind of agent` given another kind) does not match: `ELEMENT` in backlog_model.py:26 matches only `object|service`, so the line is appended as a second declaration. No item sends such a line today; b590 restates an object. Hardening: when b590's successors need it, extend `restates` and `_at` to services, events and actors.

### f2 Minor observation: repeating one member line silently replaces the whole object
- item: b598
- where: scripts/backlog_model_elements.py:265
`restates` treats an object chunk as a restatement as soon as it repeats any one member line of the declared object. An item that adds a member and repeats an existing line for context now drops every other member of the object at the lay, with no warning. Before this change it would have produced a duplicate line. This matches the definition in the vocabulary, but nothing tells the person who drafts a line, and neither `work line --model` nor the readiness bar flags it. A note in `work line --model`'s output when a chunk restates rather than adds would make it visible.

### f3 Minor observation: the unlay of a restated object fails when another item of the batch also adds to it
- item: b598
- where: scripts/backlog_model_elements.py:290
`unrestate` puts the object back only when it holds exactly the restating chunk's members. Suppose a second item of the same batch appends members to the same object, and the restating item is then parked. The members differ, `unrestate` returns False, and the fall-through in `unmerged` only removes the chunk's members when they sit at the element's end. So the restated members stay in the model after the park. This is an edge that no line names.

### f4 Minor observation: the restate relation in the model still targets only an operation
- item: b598
- where: spec/model/tracking.md:195
The new vocabulary entry (spec/vocabulary/execution.md:58) maps "restate" to `relation model line.restates` with `Frame: <model line> restates <element>`. The model declares that relation only as `restates → operation (one)`. The grammar reads the two senses apart (`restate#2` in the corpus), but the domain model does not say that a model line restates an element. A model line `relations: restates → operation | element (one)` on the item would bring the two into agreement.

### f5 Minor observation: some command lines and some output are not handled as written
- item: b632
- where: scripts/migrate_upgrade_commands.py:415
`BARE` recognises a command at the start of a line or after `&&`, `||`, `;`, `|`, `(` or `$(` only. A hook written as `bash -c 'work names --hook'`, or `env X=1 work …`, or `then work …` keeps its old name. In the other direction, `markdown` treats every line of a `console` fence as a command, so an output line such as `spec check passed` is rewritten too. One improvement would be to rewrite only the `$ ` lines of a `console` fence and to add quotes as anchors.

### f6 Minor observation: contract_obtain's module-map row does not name the new refusal
- item: b596
- where: CLAUDE.md:241
The `scripts/contract_obtain.py` row lists its refusals in order (r88, r89, r94, no contract) but does not mention `bounded context failing` (r102): a reached repository whose contents read fails. The row should add it with b596 and r102.
