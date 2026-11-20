---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-51/review-1
kind: review
batch: batch-51
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/75
head: 3468f6c8c3a4f79fcc044c1466ce586aafbcdc07
range: 3c07e67421ec6c9b6ea1da2e8c5297b4b34f7c6a..3468f6c8c3a4f79fcc044c1466ce586aafbcdc07
result: fix-now
---

# batch-51 review 1

## Verdict

All seven items are built. The four items with lines (b354, b387, b388, b390) build their lines, and b391 does too except when spec/index.md still has the old Composition tables. Both chores (b389, b397) are in scope. Two findings need fixing now: b391 builds batches#r76 wrong for an index in the old form, which is this repository's own index, and b389's brief and skill send the agent to a step of getting-started that b397 renumbered.

## Findings

### f1 Important fix now: a new capability laid into an index with the old Composition tables leaves the index out of the index form
- item: b391
- where: scripts/backlog_capability.py:171
batches#r76 says that when a batch opens, the batches service keeps "an index file that conforms to the index form". The line puts no condition on the index as it was before. The index form's entry (spec/vocabulary/execution.md) says one `## Composition` whose table `| area | kind | capabilities |` has a row for each area. The branch in `_with` for an old table goes the other way:

```
if rows and _cells(rows[0].group(0))[0] == "capability":
    at = rows[-1].end()
    return body[:at] + "\n" + _old_row(block) + body[at:]
```

So in a context whose Composition still has the `| capability | narrator | group |` tables, the capability gets an old-form row. That row is appended to the last table in the section, whatever area or group that table belongs to. The new capability's file says `area: <name>`, but the index gets no area row, so the result does not conform to the index form. This is not hypothetical: this repository's own spec/index.md (lines 51-109 in the Tree) is all old tables, so the next `work line --capability` laid here breaks r76. The scenario of g76 does not catch it, because `batches_handlers4.new_capability` hands the lay an index with an empty `## Composition`.

Fix: when the section holds old tables, write the index in the index form. Build `| area | kind | capabilities |` from each capability file's `area:` and add the new name to its area's row. Do not append an old row. Add a test in which the index starts with an old table.

### f2 Minor fix now: the batch brief and building-a-batch point to "docs/getting-started.md step 7" for a whole bindings module, but b397 moved it to step 6
- item: b389
- where: scripts/batch_driver.py:90
After b397, getting-started's step 7 is "Review and merge" (docs/getting-started.md:375). The `test_notes.py` module is now under "## 6. The session builds it" (line 175). The brief's `FRESH` text says "docs/getting-started.md, step 7, shows a whole module", and skills/building-a-batch/SKILL.md:29 says the same. A fresh context's first task follows that pointer and lands on the wrong section.

The path is also wrong for a consumer. Its agent works in its own repository, where there is no `docs/getting-started.md`; the page is the plugin's, beside `SCRIPTS`.

Fix: name step 6 and give the plugin's path, e.g. `<SCRIPTS>/../docs/getting-started.md`. Do both in batch_driver.py and in the skill, which are both files of b389's chore.

### f3 Minor observation: the size is over the limit
- item: -
- where: -
The range changes 54 files, +1150 -454 lines, against a limit of 1000 changed lines. Most of it comes from b397 (docs/getting-started.md rewritten, plus README and three skills) and b391 (backlog_capability.py, batches_handlers_form.py, the vocabulary moves).

### f4 Minor observation: the refusal-path test's `tools` case now runs `check` instead of `probe`
- item: b388
- where: tests/scripts/test_refusal_path.py:50
This is a test rewritten to run another command. I checked why. In the test's repository, which has no Python file, `tools --python /nonexistent/python probe` now completes instead of refusing, as toolchain#r19 requires. `check` still goes through `probed` and its "no analysis tools are known" refusal (scripts/tools_env.py:81), so the one-refusal-path check on `tools` still holds. What is no longer covered by any test: `probe` with a `--python` that does not exist, in a project that has a Python file.

### f5 Minor observation: probe in a project with no Python file ignores an explicit `--python`
- item: b388
- where: scripts/tools_env.py:90
To reproduce: in a folder with no `.py` file, run `tools --python /nonexistent/python probe`. It prints the no-Python-file notice and exits 0. It does not say that the interpreter it was given does not run. No line covers an explicit `--python` in a bare project.

### f6 Minor observation: after `migrate init`, the founded context counts as a Python project and probe asks for analysis tools that were never installed
- item: b397
- where: skills/shaping-items/SKILL.md:1683
The new setup runs `tools install` (step 2) before `migrate init` (step 3). Install sees no Python file, so it installs no analysis tool. `migrate init` then writes `tests/scenarios/conftest.py`, and `is_python_project` now returns True. From then on, `tools probe` exits 1, naming each analysis tool as missing, until `tools install` runs again. Fix: run `tools install` after `migrate init`, or run it again then.

### f7 Minor observation: a `--term` with no `--model` for a new capability lays a vocabulary file whose area has no model file
- item: b354
- where: scripts/backlog_model.py:214
`backlog_model_area.made` runs only inside `if block.lines:`. If the item gives the new capability vocabulary entries but no model lines, the lay writes `spec/vocabulary/<area>.md` with no `spec/model/<area>.md`. Each entry's `→ <element>` then names nothing that is declared (v_t19). The readiness bar should catch this before a batch, so nothing is lost.

### f8 Minor observation: a new guarantees capability's `specifies:` departs from the repository's own form
- item: b391
- where: scripts/backlog_capability.py:81
`specifies()` writes `the <name> guarantees`. The capabilities in the guarantees group write `guarantees of <x>` (trials.md, review-guarantees.md, shaping-guarantees.md). Nothing checks `specifies:` today, so this is only an inconsistency.
