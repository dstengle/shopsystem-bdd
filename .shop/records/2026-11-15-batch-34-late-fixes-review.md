---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-15-batch-34-late-fixes-review
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-15
---

# The late fixes of batch-34: an adversarial review

A fresh agent's adversarial review of two commits made on batch-34 (pull request #54) after its recorded review 2 was clean, at the person's request before the merge. The commits are a006facd9 (b268: each Then checked once, where it stands, with vocab.py's retry of a failing Then removed) and 787881926 (b273: counter-example Thens that can fail). A batch awaiting merge has no command back into the fix loop (b280), so these commits are outside the batch's recorded reviews.

## Verdict

Nothing blocks the merge. The retry is gone completely: vocab.py at 787881926 is identical to the merge-base a02d28f54. No check is weaker than at the base. 13 changes that made the program wrong each went red at the intended negated Then. All 350 scenarios passed twice. `tools size --limit 300` exits 0 and ruff passes on the changed files. No file under features/ or spec/ changed, and both commits carry their `Item:` trailers.

## Findings (all low)

1. `analysis_tools_handlers_thens.py:139-142`: when several things of its kind are printed, `prints` leaves the choice to a later Then. If none names the thing, only "something of that kind was printed" is checked. No scenario does this today. Fix: fail on a name still waiting at the scenario's end.
2. `installs` (the version branch) and `feature_file_tools_handlers.py:140-144` pick the first candidate among several, so a correct program could fail. They can only give a false failure, never a false pass. Fix: keep every candidate (`one_of`).
3. `requests_handlers_givens.py:218-219`: a `str.replace` that does not check its old text is there. If the template changes, the counter-example silently becomes empty. Fix: assert the old text is present before replacing it.
4. `readiness_handlers_givens.py:74, :96` depend on Given order. The generated order meets it, and a wrong order fails loudly.
5. Information: the counter-examples in conversation (t3 in a record heading) and batch-measurement (the row in elsewhere.md) catch only a program that reads the wrong source. That is all their lines' restrictions allow.

## Mutations

| Change to the program | Then that failed |
|---|---|
| `work show quote` prints every quote file | does not print the message m3 |
| `work backlog` shows questions whatever the status | does not print the question q3 |
| `tests-of --by-file` lists every test file | does not print the Python file p3 |
| `tools untested` reads `src/*.py` | does not print the function f3 |
| `migrate run` appends to `notes/*.md` | does not rewrite the file f3 |
| `work show` prints other requests' lines | does not print the request line r4 |
| `model facts` uses rglob | does not print the fact f3 |
| `measure show` merges other measurements | stage row s4, dispatch d3 |
| `work ready` lists the problems the spec already had | does not name the bar check b3 |
| v_t11 reported for `pay` | does not print the term t3 |
| w_value_kind reported for every attribute | the term t3 |
| `migrate upgrade` runs steps already applied | does not print the upgrade step u3 |
| `tools map --json` prints a wrong commit | the coverage map c1 has the commit c2 |

The fix agent also reported three counter-examples outside b273 that still pass when their Given is flipped. One is "a tag in a docstring is no tag of its feature file". The other two, in `work watch`, have a precondition Given rather than a counter-example.
