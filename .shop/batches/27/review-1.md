---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-27/review-1
kind: review
batch: batch-27
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/39
head: 38ac8c84c067c3517d2208b4d4f51d9683f0b7b6
range: c8258d127ddf9947545ded3236294ee52c2172c4..38ac8c84c067c3517d2208b4d4f51d9683f0b7b6
result: fix-now
---

# batch-27 review 1

## Verdict

The batch builds all six requirement lines (r101, r131, r132, r133, r134, r135), and each has its generated scenario and handler. Two kinds of problem hold the merge. First, b141 adds observable behaviour that no line of the batch asks for: the new violation v_t20, a blank cardinality read as any number, and negated scopes in `model logic`. Second, `tools check` exits 1 at Head and 0 at the base, because of four ruff errors in code this batch added.

## Findings

### f1 Important fix now: v_t20, a new violation that no line asks for
- item: b141
- where: scripts/spec_relations.py:108
Commit 66a82ccb adds `v_t20` to `spec_relations.problems`, adds its entry to `model_rules.LEXICON` and to `grammar/rules.md`, and stores the codified-2 flag as `Lexicon.four` in `spec_lexicon.read`. In a context whose `spec/index.md` says `language: codified-2`, a relation row whose word is not one of the fixed prepositions or role nouns is now a violation. That changes what `model lexicon --check` and `model check` print, and makes them exit 1.

b141's only lines are r133 (overriding) and r134 (contravening), and neither is about relation rows. No capability's Implementation section names v_t20 either. The item's Notes mention "spec_relations' fixed word set", but Notes are not requirement lines.

Fix: take v_t20 out of this branch (spec_relations, the model_rules entry and FOUR, the rules.md entry, the `four` field if nothing else uses it, and its test), and record it with `work idea` with its own line. Or, if the person wants it in this batch, give b141 a line for it before the merge.

### f2 Important fix now: two new `model logic` readings that no line asks for
- item: b141
- where: scripts/spec_logic_vocab.py:44
b141 changes two readings that alter `model logic`'s L1 findings in a codified-2 context, and neither is asked for by r133, r134 or any other line of the batch:
- **Blank cardinality** (commit 66a82ccb): `functional(row, four)` no longer treats a blank row of for/with/on/of/in as functional. `fun/1` facts therefore drop out, which changes unification ("the worktree of the session") and so which pairs clash.
- **Negated scopes** (commit f877e03c): spec_lf_facts emits `nattr`/`nrel`, and new `out`/`gap`/`pag` rules in check.lp use them. Pairs are now set aside or kept differently. A line the translation used to refuse now translates, so it is no longer in `ctx.refused`.

Neither the overriding nor the contravening fixture depends on either reading. Both are tested only in tests/scripts/test_spec_lf_facts.py.

Fix: either take both out of this branch and record them with `work idea` with their own lines, or give b141 lines for them. A line could, for example, name a capability whose clash depends on a blank-cardinality row, or on "whose T is not v".

### f3 Minor fix now: `tools check` red, B023 and ISC004 in b142's code
- item: b142
- where: scripts/spec_entail.py:52
The `tools check` run exits 1 at Head and 0 at the base:
```
scripts/spec_entail.py:52:66: B023 Function definition does not bind loop variable `L`
tests/scenarios/codified2_world.py:87:32: ISC004 Unparenthesized implicit string concatenation in collection
```
The lambda `other` in `index` is called only inside the loop iteration, so its behaviour is correct, but the check fails. Fix: pass `L` as a default argument (`lambda M, L=L: ...`) or make it a plain comparison. Wrap the first string of `REQUIREMENTS["restating"]` in parentheses, as `CAPABILITIES` does, and add the second blank line before `def context` that this commit dropped.

### f4 Minor fix now: `tools check` red, RUF100 in spec_example
- item: b149
- where: scripts/spec_example.py:23
```
scripts/spec_example.py:23:61: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
```
Fix: drop the `# noqa: E731`, or make `bare` a nested `def`.

### f5 Minor fix now: `tools check` red, SIM114 in spec_lf_facts
- item: b141
- where: scripts/spec_lf_facts.py:179
```
scripts/spec_lf_facts.py:179:13: SIM114 [*] Combine `if` branches using logical `or` operator
```
Commit f877e03c added the branch `elif item.op == "not" and not self.acting(item): self.restrict(item, own)`, which has the same body as the `elif isinstance(item, Atom)` branch above it. Fix: merge the two conditions with `or`.

### f6 Minor observation: vulture's unused `check` in model_rules predates the batch
- item: -
- where: scripts/model_rules.py:135
The `tools check` run also prints `unused variable 'check' (100% confidence)` for the parameter `catalogue(root, write=False, check=False)`. The batch did not change that signature: commit 66a82ccb only added `FOUR`, a `LEXICON` entry and the index switch in `fires`. The warning shows up because the file is now in the range that `--base` checks. It is not the batch's, so it is recorded only.

### f7 Minor observation: actors' `Kind of:` now changes codified-1 pairs too
- item: -
- where: grammar/check.lp:132
The `aterm`/`doer` rules added in commit 56fcfba0 are not guarded by `cnl4`. `Vocab.actor_kinds` is filled for a codified-1 lexicon as well. In this repository, `` `work` `` is Kind of: tool, and tool is Kind of: agent. So `domain` now emits `akind(a_work,k_tool)` and the like for the live, codified-1 spec, and a codified-1 line about "a tool" can now pair with one about `` `work` ``.

The check.lp comments promise that codified-1 findings stay as they were for `every` and for the If tag, but nothing promises it here. b140's Notes say the actors' Kind of: goes into the domain facts, so this may be intended. What I verified: index.md:106 and :112 give `work` Kind of: tool and tool Kind of: agent, and `Vocab.__init__` builds `actor_kinds` with no codified-2 condition.

Reproduction: run `model logic` on this repository at the base and at Head, and compare the L1 lists.

### f8 Minor observation: the change is over the size limit, mostly b142's frozen fixture
- item: -
- where: -
The `## Size` section gives 59 files and +5778 -56 lines, against a limit of 1000. About 4,400 of those lines are b142's frozen spec copy under tests/scripts/fixtures/entailment/. The design asks for that fixture (section 13 point 10), so it is not to be cut, but it is what puts the change over the limit.
