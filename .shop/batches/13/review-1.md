---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-13/review-1
kind: review
batch: batch-13
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/27
head: 738313859ad6db6119a7ae01970cb1792da84818
range: a4c5c2fb08b1647977d73660edb71e42236ab038..738313859ad6db6119a7ae01970cb1792da84818
result: fix-now
---

# batch-13 review 1

## Verdict

The batch builds b82's five lines: `model parse` refuses a verb short of its object or recipient and names the verb, `model check` reports v_t11 and v_t12, and a negated relation parses. U3 → U11 and pr-review r8 → r9 follow the retire-never-edit rule. One finding to fix: `tools check` now fails, and passed at the base.

## Findings

### f1 Important fix now: `tools check` fails at Head: vulture flags test_spec_solve.py, which the batch touched
- item: b82
- where: tests/scripts/test_spec_solve.py:195
`## Runs` gives `tools check --base a4c5c2fb` as `Exit code: 1 (base: 0)`:

```
== vulture ==
tests/scripts/test_spec_solve.py:195: unused variable 'brave' (100% confidence)
tests/scripts/test_spec_solve.py:195: unused variable 'ctl' (100% confidence)
tests/scripts/test_spec_solve.py:195: unused variable 'focus' (100% confidence)
tests/scripts/test_spec_solve.py:195: unused variable 'limit' (100% confidence)
```

The batch changed only line 20 of this file (`USE` got a `Frame:`). Because the file is now in the range, the check against the base reads all of it, and it flags this existing stub: `lambda ctl, limit, brave=True, focus=None: ([], False)`. The batch's own check has gone red, and the merge should not carry that. Fix it on b82's branch: write the stub as `lambda *_args, **_kwargs: ([], False)`, or give the parameters `_` names, so that vulture passes on the file.

### f2 Minor observation: the module map row for `tests/scenarios/vocab.py` still says U3
- item: b82
- where: CLAUDE.md:139
The change renames U3 to U11 in `vocab.py`'s docstrings and in `u_problems`' message (`"U11: ..."`), and in `spec/universal.md`, `conftest.py` and the tests. The CLAUDE.md row still reads "the U3/U4/U8 checks after a generated scenario". U3 is now a retired id, and the module map is binding, so the row should say U11/U4/U8.

### f3 Minor observation: the test of the dropped "second object" guard was removed with the guard
- item: b82
- where: tests/scripts/test_spec_tree.py:71
`spec_tree._second_object` is deleted, and so is its assertion `"second object" in spec_tree.guard(tree, WORDS)`. The test is renamed `test_a_recipient_after_its_object_passes_the_guards` and now only asserts a pass. The removal looks justified: `DoTo` now reads `&lt;verb&gt; &lt;object&gt; to &lt;recipient&gt;`, so a code after a noun phrase can no longer parse as a second object. Nothing replaces the old negative case, though. A corpus line in `refused.txt` covers the double-object order (`` `work run` shall give the stage only a brief. ``), but nothing checks that "use the interpreter `python3`" still parses as one object with a name. This is noted, and does not hold the merge.

### f4 Minor observation: `SDoesI`/`SDoesINot` reuse the `ThenDoes`/`ThenDoesNot` templates, whose handlers expect an object
- item: b82
- where: scripts/features_vocab.py:388
`THEN` maps `SDoesI` to `"ThenDoes"` and `SDoesINot` to `"ThenDoesNot"`, and `rows` adds a second `then`/`ThenDoes` pattern whose arguments have no noun phrase. No requirement in the spec uses `DoI` in a response yet, so no generated scenario reaches it today. Once a line like `` `work run` shall stop. `` is written, its Then would go to a `ThenDoes` handler written for an object. That case is not tested.

### f5 Minor observation: a frame's kinds are read but never checked against the line
- item: -
- where: scripts/spec_frames.py:680
`guard` only checks whether an object or recipient is present. The frame's subject and object kinds are parsed and never compared with the line. As a result, some frames disagree with their own gloss and nothing reports it. For example, `spec/index.md`'s **merge** has the gloss "`work run` merges a work-item branch" but `Frame: the person merges pull request.`, and **show** has the gloss "shows the person a thing" but `Frame: session shows file.`. None of b82's lines asks for the kinds to be checked (b84 is the item that types them), so this is a note for b84.
