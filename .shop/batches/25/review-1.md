---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-25/review-1
kind: review
batch: batch-25
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/37
head: 094f7cf9005143284a59e8fa833046fe2558ced5
range: 0a5bf004ebac317749acde09c65bff5620410778..094f7cf9005143284a59e8fa833046fe2558ced5
result: fix-now
---

# batch-25 review 1

## Verdict

The batch builds all twelve lines of b132–b135, and `features generate --check`, `tools check` and `tools size` pass. One finding must be fixed: b135 adds a `model check` refusal (v_t18) that no requirement line asks for. The other findings are observations.

## Findings

### f1 Important fix now: v_t18 refuses a declared compound, and no line asks for it
- item: b135
- where: scripts/model.lp:427
The change adds a new refusal to `model check`. When a noun entry (kind or resource) is spelled as a compound that a relation row whose word is `of`, or an attribute, also derives, `model check` now exits 1 with `v_t18`. For example, a context that declares `**stage status** (noun)` beside `status (attribute of stage)` is now refused.

No line of the batch asks for this. b135's lines r88–r91 only say that `model parse` passes a requirement that is genitive, denying, compound or restrictive. The capability's `## Implementation, may change` section does not name v_t18 either. The design record and b135's notes ask for v_t18, but notes are not requirements.

There is a precedent for doing this properly: the earlier lexicon checks of this kind each came with a line (v_t15 has r79, "If the person runs `model check` on a term that is overlapping…"). v_t18 has none, so it is untested as a requirement. `grammar/rules.md` itself says `Cited by: no line`.

The pieces that carry it:
- `spec_rgl_np.derived`
- the `derived` facts in `scripts/model_spec.py:83`
- the rule and `#show` in `scripts/model.lp`
- the `## v_t18` entry in `grammar/rules.md`
- `test_a_declared_compound_that_is_derived_is_refused` in `tests/scripts/test_spec_rgl_np.py`

Fix: take v_t18 out of this batch and record it with `work idea` so it returns with its own line, something like "If the person runs `model check` on a term that is derived, then `model` shall exit with an error naming the term." The grammar's compound noun phrases (`T_Cpd_K`, `r<n>_Cpd`) do not depend on the check and can stay.

### f2 Minor observation: the aspect refusal blames the trigger for a state verb in a response
- item: b134
- where: scripts/spec_grammar4.py:691
`misaspected` decides which clause a verb is in by looking back for the nearest `when`, `if` or `while`. It never stops at `,` or `shall`. A response's acts can only use action frames (`D_Act_S` exists only for subjects with an action), so a state verb in a response makes GF stop at that verb.

Reproduction in the codified-2 fixture: `When the person runs `work start`, `work` shall follow the stage.` is refused with "the verb follow is a state, and a trigger takes an action". The verb is in the response, not the trigger, so the reason is wrong. The same happens with `If …, then …`.

r86 only names the While clause and the trigger, so this is an edge no line covers. Fix: stop the look-back at `shall`, or at `then` or the `,` that closes the clause, and in a response give a reason of its own or fall through to "does not parse at".

### f3 Minor observation: the agreement refusal misses has and holds
- item: b133
- where: scripts/spec_grammar4.py:670
`disagreeing` only tries the verb entries in `vocab.verbs`. The `has` and `holds` frames that spec_rgl_np generates from relation rows are not verb entries.

Reproduction: `While sessions has no worktree, when the person runs `work start`, `work` shall exit successfully.` gets "does not parse at has", not "the verb have does not agree in number with its subject". r85's scenario uses `write`, so it passes. This is hardening for when b135's frames come into use.

### f4 Minor observation: `model lexicon --check` now reports v_t16 and v_t17 too, and the contract still says v_t4-v_t10
- item: b132
- where: scripts/model_report.py:511
r81 and r82 name only `model check`. The change also adds v_t16 and v_t17 to `model lexicon --check`, so that command now exits 1 for a misimporting or unmarked context. `model lexicon` also adds a `[pack <name>; redefines <pack>]` mark after each line.

`lexicon --check` already mirrors the lexicon codes of `model check` (spec_frames' v_t11-v_t15), so this matches what the command already does. But the contract text in `scripts/model` still says "lexicon --check prints v_t4-v_t10". Fix: update the contract wording.

### f5 Minor observation: "compound" now has two senses in design-model-check
- item: b135
- where: spec/capabilities/design-model-check.md:117
Line 64 defines **compound** as an adjective of requirement group ("more than one statement", used by r5 and v15l). The batch adds a second **compound** at line 117, an adjective of requirement ("a compound noun that … derives"). The scenario handlers tell them apart by kind, so nothing breaks. But one word now means two unrelated things in one capability, which goes against the clarity rule in CLAUDE.md. A distinct word such as "compounded" would read better the next time these lines are touched.

### f6 Minor observation: the change is over the size limit
- item: -
- where: -
`## Size` gives 29 files, +1476 −21, against a limit of 1000 changed lines. Most of it is b133 (the new `spec_rgl.py`, `spec_grammar4.py`, `spec_rgl_vocab.py`, `grammar/Base*.gf`, `test_spec_grammar4.py` and `core-4.txt`), then b135 (`spec_rgl_np.py`, its tests and the corpus lines) and b132 (`spec_packs.py`, `grammar/packs/cli.md`, the handlers).

### f7 Minor observation: `model decisions --check` fails, at the base too
- item: -
- where: -
It exits 1 at `Head:` and at the base. Decisions 0086, 0087 and 0088 each fail with `tests/scenarios/vocab.py: exit 5` ("no tests ran"). The batch did not cause this.
