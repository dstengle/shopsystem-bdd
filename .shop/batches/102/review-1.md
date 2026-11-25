---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-102/review-1
kind: review
batch: batch-102
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/125
head: 0747dc91ccd73b229fe528fbcc5245c4213b1e73
range: d5467ae62b5df904227b2a82b3f2b1accd749b23..0747dc91ccd73b229fe528fbcc5245c4213b1e73
result: fix-now
---

# batch-102 review 1

## Verdict

All three items are built. b617's ten model-line moves and two term moves are laid as written, review limit now sits in execution, and b608's term moves leave shared.md with only the five base kinds. b550 builds checking#r106-r109 and has scenarios g106-g109. One finding is fix now: b550's clash check also fires on two terms of one word inside a single contract. That is the normal shape of a contract published by a context with a domain model, so r106 fails on real contracts.

## Findings

### f1 Important fix now: two terms of one word in one provider contract are reported as a clash
- item: b550
- where: scripts/adapter_provider.py:313
`_read` puts every term it reads from a contract into `taken` (`taken[t.term] = "the contract of %s" % provider`). The next term of the same contract with the same word is then counted as a clash: it is dropped from the lexicon and reported as a file problem.

The risk is real: I checked what a contract's `terms` hold. contract_form's `_terms` writes one line per term of `spec_lexicon.read(root)`. For a context with a domain model, spec_vocabulary_terms gives each attribute its own Term with the label `attribute of <kind>`, so a single contract holds `status (attribute of batch)`, `status (attribute of task)`, `status (attribute of item)` and so on. It also holds more than one sense of a verb (for example `move` twice in tracking). That is exactly what `spec publish` writes and `spec obtain` keeps. The vocabulary's own definition of clash is "spelled as another term that the adapter spec reads and names another element". Senses of the provider's own word do not meet that definition, and `renames:` cannot help, because it renames every sense of the word together.

So for an adapter spec that holds such a contract and whose line uses `status`, `spec check` fails naming `status`, where checking#r106 says it completes the request. The scenarios pass only because their contract holds one term of each word.

Fix: compare a provider's term only against terms from outside its own contract (packs, the adapter spec's own terms, earlier contracts). Keep all senses of a word from one contract, and add a unit case with two `status (attribute of …)` lines.

### f2 Minor observation: a provider pinned with no version picks the "latest" contract by string order
- item: b550
- where: scripts/adapter_provider.py:237
`contracts` sorts the paths that `place(id, "*")` matches and takes the last one. Sorting is by text, so `provider/.../1.9.0/contract.toml` comes after `.../1.10.0/`. With both kept and `providers: [<id>]` given no version, the lexicon reads 1.9.0. Today `spec obtain` keeps one version per pin, so this does not arise yet. Sorting by version number would close it.

### f3 Minor observation: r107 and r108 read "the term" as the other term, not the provider's
- item: b550
- where: spec/capabilities/checking.md:460
The corpus form of r108, laid by `work batch start`, says `rename(subject: x1, object: x4)` and `name(e3, subject: x6, object: x4)`, where x4 is "another term". By R2, "the term" binds to the latest term. The lines mean the provider's term (x3) to be renamed and named. The code renames and names the provider's word, and the scenario cannot tell the difference: the handler names both t1 and t2 `product`. Rewording the lines (for example "the adapter spec renames the term of the contract") would make what they say match what is checked. CLAUDE.md asks that the clarity of requirement lines be weighed first.

### f4 Minor observation: the move lay did not add the import that review-guarantees' lines need
- item: b608
- where: spec/model/execution.md:5
Commit e6ff4549d added `measurement` to execution's `imports:` by hand. The lines say `dispatch`, whose entry the batch moved into the measurement layer. backlog_area_move_lay's `lay` is meant to add the target area to the imports of each area whose lines say a moved word, so v_m1 stays clean, and it missed this case. The fix in the model is right. The gap in the lay is worth an item.
