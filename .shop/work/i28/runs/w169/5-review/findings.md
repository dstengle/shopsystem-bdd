# Review of w169 (spec-integration#r43, round-ids-avoided)

Verdict: DONE. No Critical finding, none triaged fix now. One Minor observation.

## Commits reviewed

The branch `work/w169` is gone; the commits are those between `24bbf163 work: w169 ready -> claimed` and `89c19d88 work: w169 claimed -> done`, less `work run`'s `work:` commits:

- `50788670` round-ids-avoided: integrate rounds number above ids given from other initiatives' drafts (spec-integration r43). Four files, +7 −4: `agents/capability-writer.md`, `agents/initiative-round.md`, `docs/capability-format.md`, `skills/integrating-a-proposal/SKILL.md`.

The implementer's result gives `4e17518d`. That commit exists, with the same message, author time and stat, and `git diff 4e17518d 50788670 -- agents skills docs` is empty. `50788670` is the same change carried onto the line by the merge, so this is not a finding. Every file is inside the work-item's fileset. No Python, no `features/` and no `tests/` file changed.

## Removed and weakened tests

None. The commits touch no file under `tests/` or `features/`. I checked with `git diff --stat 24bbf163 89c19d88`.

## Allowances

The report's `## Tests changed under an allowance` says "none", and the commits agree.

## Cannot verify

- spec-integration#r43 is a guarantee (design-decision/workflow-capabilities-are-guarantees), so no scenario covers it. Whether a real integrate round now numbers above the ids it is given can only be judged by `measure` on a real batch.
- The label "Ids drafted elsewhere" appears nowhere under `scripts/`, `tests/` or `features/` (grep). The brief that gives these ids is w170's (supervision#r102), so this work-item cannot show whether the round text's label matches what `integrate_lines` will write. The report flags this for w170.

## Findings

### 1. Minor, observation: the writer's dispatch templates have no slot for the given ids
- File: `skills/integrating-a-proposal/SKILL.md:37-64` (The Template, The Question Template); `agents/initiative-round.md:27`.
- What: the round's text says to give the listed ids "to the writer in the dispatch". `capability-writer.md:20` says to number above "every id your input prompt gives for that capability". Neither template has a place to put those ids, so the round has to add them freehand.
- Why it matters: little. If a writer misses the ids, its numbering is caught by the round's check in step 2 and sent back, so no wrong id reaches the gate. The cost is an extra writer round.
- Reproduction: Read `SKILL.md` lines 37-64. Neither template mentions ids from elsewhere.
- Fix: add an optional line to both templates, for example `Ids drafted elsewhere (number above them on the same capability): <IDS>`.

### Checked and found sound
- Behaviour against r43 and r12: the added text applies the "above" rule only to ids on the same capability, leaves numbering unchanged when no ids are given (r12 still holds), and makes the round itself check (r43's subject is `initiative-round`). This matches plan decisions D1-D4.
- No code was added that no Behaviour line asks for. The change is text only.
- Purpose: no contradiction.

## Commands run

- `git log --format=%H -1 --grep="^work: w169 ready -> claimed$"` gives 24bbf163
- `git log --oneline 24bbf163^..HEAD`; `git log --format=%H -1 --grep="^work: w169 claimed -> done$"` gives 89c19d88
- `git show 50788670`; `git show --stat 4e17518d`; `git diff 4e17518d 50788670 --stat -- agents skills docs` (empty)
- `git diff --stat 24bbf163 89c19d88`
- grep for `r43]`, `r12]` in spec-integration.md; `r102]` in supervision.md; "drafted elsewhere" in scripts/tests/features (no match)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 24bbf163`:
  - ruff: 4 FURB167 in `tests/scenarios/supervision_integrate_steps.py` and `tests/scripts/stub_claude.py`. These commits did not touch either file, so the errors are not w169's.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing, so no file is over the limit.
