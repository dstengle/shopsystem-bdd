---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-24/review-1
kind: review
batch: batch-24
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/36
head: 19df9bd1b7e43a0f5e86a9b8a750ede0c25d8f59
range: 1ef41de670df774c80192bc8bee197657b02b451..19df9bd1b7e43a0f5e86a9b8a750ede0c25d8f59
result: fix-now
---

# batch-24 review 1

## Verdict

The batch builds all three items: b129's r10–r12, b164's r74 and r75 (r72 and r73 retired, not edited) and b131's r76–r79. One finding needs a fix: a ruff error the batch adds makes `tools check` exit 1 at Head when it exits 0 at the base. Three observations follow.

## Findings

### f1 Minor fix now: `tools check` fails on a ruff alias the batch adds
- item: b129
- where: tests/scenarios/decision_tiers_handlers.py:242
`tools check` exits 1 at Head and 0 at the base. Its output:

```
tests/scenarios/decision_tiers_handlers.py:242:109: FURB167 [*] Use of regular expression alias `re.M`
```

The line comes from commit fdb7ae2f, in the new handler `work_decision_routed`:

```python
step.context.setdefault("holds", {})[done.stdout.strip()] = re.compile(r"^verified_by: \[check\]$", re.M)
```

The fix is to write `re.MULTILINE`.

### f2 Minor observation: the `features generate --check` run used the base's scripts, not the batch's
- item: b131
- where: -
The run exits 1 at Head (base: 0), refusing every `(verb, action)` and `(verb, state)` entry as "no part of speech". The command it ran is `/home/vscode/shopsystem-bdd/scripts/features`, which is main's checkout. Main's `spec_lexicon._category` has no `ASPECTS` and does not read the 4.0 label. In the tree, `scripts/spec_lexicon.py:101` reads it. So the failure says that a pre-4.0 plugin refuses this spec, not that the batch's features are stale. `model decisions --check` ran the tree's tests, and it reports that 0082's `test_the_features_are_what_features_generate_writes` holds at Head. The features diff matches generated output: g72 and g73 are gone, and g74–g79 follow the spec text. Worth knowing: until 4.0 ships, any consumer or check that runs an older plugin on this spec is refused this way.

### f3 Minor observation: the unlabelled refusal still tells people to write `(verb)`, which v_t14 now refuses
- item: b131
- where: scripts/spec_lexicon.py:247
`unlabelled` still says `write each as (noun), (proper noun), (verb), ...`. With this batch, a bare `(verb)` is read as an event with no aspect, and `model check` refuses it (v_t14, r76). Likewise, `relabel` maps plugin 2.x's `event` to `verb` (`SPEECH`), so `migrate_upgrade_frames` would still write `(verb)` entries that v_t14 then refuses. The message should name `(verb, state)` and `(verb, action)`. The upgrade step is b161's to change, but the hint is cheap to fix here.

### f4 Minor observation: `rests_on` repeats `source`, and a bare name in it is read as a universal condition
- item: b129
- where: scripts/model_work.py:74
`work decision --rests-on` adds a frontmatter field, but `--source` already exists with the help text "an id the decision rests on", so two fields now carry one meaning. The b129 notes left the builder free to choose how a decision covers a universal condition. Reading `source` would have needed no new option.

`read_routes` qualifies every bare entry with the kind `universal-condition`. I checked `model_facts.qualify`: a bare name matching NAME becomes `<kind>/<path>/<name>`. So `rests_on: [final-layout]` turns into `universal-condition/<path>/final-layout`, which `want()` reports as unresolved, though the author meant a decision.

No test drives `--rests-on` itself. Only `given_unrouted` writes the field, and the `is not unrouted` branch is not used by any generated scenario.
