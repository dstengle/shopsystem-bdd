# Plan: design-model-check-3 (design-model-check#r110)

## 1. What goes green

- **design-model-check#r110**: the file problem when a work-item's file name is not `w<n>.md`, or when two work-items have one id.
  - Scenario Outline "a work-item not named w<n>.md, or two work-items with one id, is a file problem", in `features/design-model-check.feature`, with four rows:
    1. `.shop/work/i1/fix-login.md` with the id w3: prints a file problem
    2. `.shop/work/i1/w3.md` with the id w3: does not print one
    3. `i1/w3.md` and `i2/w3.md`, each with the id w3: prints a file problem
    4. `i1/w3.md` with the id w3 and `i2/w4.md` with the id w4: does not print one
  - Why all four are red today (notes §1): each fails at the Given. `malformed_record` in `tests/scenarios/design_model_check_problems.py` has no branch for the four case strings, so it falls to its `else` assertion. The helper `World.work_item` writes only into `i1`, and always names the file after the id. The bare Then "it does not print a file problem" has no step. Behind the steps, the probe (notes §2) shows `model check` printing no file problem for row 1 or row 3: the file stem is never read, and a second work-item with the same id is registered without any problem.
- Retires: none. The work-item has no Retires section.

## 2. Where the change lands

- `scripts/model_work.py`: two new checks, for work-items only (frontmatter `kind: work-item`):
  - In `read_part`: a work-item whose file stem is not `w<n>` gets a file problem naming its file.
  - A registry of work-item ids across every initiative: a second work-item file with an id already held gets a file problem naming both files.
  - The registry starts empty in `read_work`, before the initiative loop, so `model_facts.py` is not touched.
- `tests/scenarios/design_model_check_problems.py`: `malformed_record` gets the four case branches. Rows 3 and 4 also write the second initiative `i2` (its `initiative.md`, through `World.initiative`).
- `tests/scenarios/conftest.py`: `World.work_item` takes the initiative (default `i1`, which also sets `part_of`) and the file name (default the id), so a row can write `fix-login.md` with the id w3, or a file in `i2`.
- `tests/scenarios/design_model_check_then.py`: the bare Then "it does not print a file problem". It goes here because this file has 85 lines of room and `design_model_check_problems.py` has 22, which the four branches need. Its pattern must not collide with the existing "it does not print a file problem naming {named}" step.

Removed from the researcher's set: `scripts/model_facts.py` (35 lines of room). With the registry in `model_work.py`, it needs no change.

## 3. Decisions

1. **A work-item's id for r110 is the `w<n>` of its file name.** The duplicate check compares file stems across all of `.shop/work/`; the frontmatter id does not enter it. This rests on the work-item's ruling (formulation round f1) and on design-decision/work-items-named-by-ids.
2. **Only nodes of kind `work-item` are checked.** Capability-proposal parts such as `p1.md` stay as they are. This rests on r110 ("a work-item's file name") and on design-decision/work-file-forms, which keeps `<part>.md` for other part kinds.
3. **The duplicate check spans every initiative and every status, `withdrawn` included.** Rests on design-decision/work-items-named-by-ids: "in any initiative and any status ... never repeated".
4. **Two work-items with one id give one file problem.** It names the later file read and the file that already holds the id. A file whose stem is not `w<n>` gives one problem and does not enter the registry. Rests on r110 (one case: "two work-items have one id") and on the capability's sentence "a file problem names the file". The scenario's "it prints a file problem" step expects one problem per case.
5. **The new problems go in the file problems.** They are not a `model.lp` rule. Rests on r110's code, "file problem". `model_check.py` and `model.lp` stay unchanged.

## 4. Tests the decisions break

None. I verified this from the notes' search (§4): every `model check` test in `tests/scripts/test_model*.py` and `tests/scenarios/design_model_check_*` writes its work-items through `World.work_item` or `work_item` with the default `w1`, so the file is `w1.md`, and none writes two work-items with one id. The parts written as `.shop/work/i1/p1.md` (`design_model_check_problems.py`, `design_model_check_reading.py`) are capability-proposals, which decision 2 leaves alone. The work-queue and supervision tests name work-items by other names but never run `model check`. The old-layout test in `migration_spec_steps.py` reads `work/`, not `.shop/work/`. The default arguments in the `World.work_item` change keep every existing caller as it is. This was found by search only: `tools tests-of` has no map. The implementer runs the `design_model_check` scenarios and `tests/scripts/test_model*.py` to confirm.

## 5. Open cases

The implementer names these in a test or a note; they are not chosen here.
- A work-item named `w4.md` whose frontmatter id is w3 (defect D3). r110 and the ruling are silent on whether the frontmatter id has to agree with the stem.
- What `w<n>` admits: `w0`, leading zeros (`w03`), an upper-case `W3`.
- Two work-items in one initiative whose stems are not `w<n>` but whose frontmatter ids are the same (defect D4). Under decision 1 they have no r110 id, so only the stem problem is printed for each.
- The order in which the two files of a duplicate are named, given that initiatives and files are read in sorted order.
