---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-147/review-1
kind: review
batch: batch-147
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/170
head: 7eeb5f4f72174e05f519796e6527f04290c9f7a7
range: 4e3ab727e4c578d172bfd6025d744aeb50a67eb7..7eeb5f4f72174e05f519796e6527f04290c9f7a7
result: fix-now
---

# batch-147 review 1

## Verdict

All four items are built and their scenarios pass. One scenario is wrong, though: for checking#r149 the code returns the coupling under the area that holds the element, while the line says the area that holds the word, and the scenario passes only because its handler swaps the two areas. The `tools check` run now fails on files that b614 touched, and the change is over the size limit.

## Findings

### f1 Important fix now: r149's coupling goes to the area that holds the element, not the area that holds the word, and its scenario passes only by swapping its areas
- item: b762
- where: tests/scenarios/checking_handlers_coupling.py:27
checking#r149 asks for "a coupling of the area that holds the word". Its logical form in grammar/corpus/spec/checking.md is `of(x9, x3)`, where x3 is the area that holds the term. `_words` in scripts/spec_coupling.py:37 files the borrowed word under a different area:

```
_coupling(found, e.element.area, e.layer)["words"].add(e.term)
```

That makes the coupling's `area` the element's area (notes) and its `by` the area that borrows the word (binder). The generated scenario @g149 says "the area a2 holds the term t1" and "the area a2 has the coupling c1", so by its own Givens a2 is the area that borrows the word. But the handler maps a2 to notes for every group (`AREAS = {"a1": "binder", "a2": "notes"}`, used by `given_state` at line 131). In the r149 world, `BORROWED` puts `jotting` in binder's vocabulary and the element `object note` in notes. So the world reverses what the Givens say about a1 and a2. If the handler followed the Givens, `coupling(step, "c1")` would look for `area == "binder"`, find nothing, and the Then would fail. As it stands, the scenario passes against code that does something other than what the line says.

The code agrees with r145's convention and the docs (a coupling is of the area depended on). So the likely fault is in the line, which differs from r145 and r148, whose scenarios do put the coupling on the area that holds the element or the second entry. Fix, pick one:
- Reword r149 on b762 (`work line --reword`, then `work batch amend`) so the coupling is of the area that holds the element. Then make the handler bind a1 and a2 per group as the Givens say, so the r149 world agrees with its scenario.
- Change `_words` so a borrowed word goes into the coupling of the area that borrows it.

### f2 Minor fix now: `tools check` exits 1 at Head on files b614 rewrote
- item: b614
- where: scripts/spec_moves.py:90
In the `python3 scripts/tools check --base …` run, ruff reports 7 errors in files that b614 touched (each had an import line changed), with exit code 1 at Head and 0 at base:

```
scripts/spec_moves.py:90:62: FURB167 [*] Use of regular expression alias `re.M`
scripts/spec_moves.py:91:54: FURB167 [*] Use of regular expression alias `re.M`
scripts/spec_moves.py:108:51: FURB192 Prefer `min` over `sorted()` to compute the minimum value in a sequence
tests/scripts/test_spec_moves.py:11:20: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
tests/scripts/test_spec_moves.py:12:19: RUF100 ...
tests/scripts/test_spec_moves.py:13:44: RUF100 ...
tests/scripts/test_spec_moves.py:129:12: RUF015 Prefer `next(...)` over single element slice
```

The lint problems were already in these files, but touching them brings them into the check, which now fails on this batch. Fix: run `ruff --fix` on the two files and fix FURB192 and RUF015 by hand (both paths are in b614's chore files).

### f3 Minor observation: the change is over the review limit
- item: -
- where: -
`## Size` gives 174 files, +988 -485, against a limit of 1000 changed lines. Most of it is b614: the `.importlinter` forbidden list (287 lines) and the plumbing import rewrites across scripts/ and tests/.

### f4 Minor observation: `batch_reached.reached` misses an input deleted when it was the last of its kind
- item: b763
- where: scripts/batch_reached.py:62
The new `inputs` takes `spec_held.inputs(tree)`, which lists only the files that exist when it runs. It adds the folder of each listed file only for paths under `spec/`.
- Under `spec/`: if a lay removes the last file of `spec/packs/` or `spec/vocabulary/`, no other file of that folder is listed, so the folder is never added and the removal is not seen.
- Outside `spec/`: the old code always passed the whole folders and `:(glob)provider/**/contract.toml`. A deleted `provider/<x>/contract.toml` is no longer in either list.

`test_reached_by_an_input_taken_out` covers only the case where another vocabulary file is left. To reproduce: in a fixture whose `spec/packs/` holds one pack, delete it uncommitted, and `batch_reached.reached(root)` returns False. Lays rarely make these deletions today, so this is hardening.
