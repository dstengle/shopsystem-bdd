# Review of w141: delivering-an-initiative only starts work run

**Verdict: DONE.** No Critical finding, none triaged fix now. Two Minor observations, two Minor drops.

## Commits reviewed

The branch `work/w141` is gone (`git log ... work/w141`: unknown revision), so the commits are those on the checked-out
history between `a102fce work: w141 ready -> claimed` and `337f609 work: w141 claimed -> done`, less `work:` commits:

- `36ecb74 delivering-an-initiative: only start work run and put what it cannot deliver to the person`
  (skills/delivering-an-initiative/SKILL.md, +14 -26).

The implementer's result lists exactly `36ecb74`: they match. `337f609` is work run's own transition commit.

## Removed and weakened tests

None. `git diff --stat a102fce 36ecb74 -- features/ tests/` is empty; the only file changed is SKILL.md (markdown,
no test reads it; research notes §4 searched tests/ for `SKILL`, `skills/`, `delivering`). Plan §4 lists none.

## Allowances

The report's `## Tests changed under an allowance` says "none"; no test changed, so nothing to verify.

## Cannot verify

- delivery#r21 (put a refused tool to the person, naming the stage): the skill text (SKILL.md:42) acts on work run's
  printout, but work run prints no refused tool today (research D3; a refusal becomes a `failed` work-item with a
  fault). The line is written but cannot fire until supervision prints it. Not a defect of these commits; it is a
  supervision gap (the plan's Open cases, the report's Open questions).
- The report's `pytest --work-item w141`: 142 passed, 1 skipped. Not rerun (work run ran the suite before merging).
- Whether the skill behaves as written in a real session: guarantees capability, judged by `measure` on real batches
  (decision 0065), not by these commits.

## Accepted lines against the text

- r4: SKILL.md:30 starts `work run` on the ask; the formulated-proposal precondition and the Drafting / Commit
  sections are gone (retired r1-r3, r8, r9, r17, r18). Holds.
- r10: SKILL.md:47 drafts only a trial's fix with `work add`; review fixes left to work run (decision 0068). Holds.
- r19, r20: SKILL.md:12 and Red Flag at :58. Holds.
- r21: SKILL.md:42. Holds as text (see Cannot verify).
- r22: SKILL.md:43, a `failed` work-item or a `work: <why>` stop put as a question, nothing retried or edited. Holds.
- r5, r6, r7, r11 (not accepted, kept): unchanged or consistent; `awaiting-ruling` corrected to `awaiting-answer`
  (SKILL.md:36), matching what work run prints.
- No code no line asks for: the diff is skill text only; each added sentence maps to r4, r10, r19-r22 or r6.

## Findings

### F1 Minor, observation: the skill may no longer read spec/ or features/, yet r10 and r12 need them
SKILL.md:26 restricts reading to `.shop/work/` (initiative, proposals, work-items). SKILL.md:47 (r10) needs
`--under <capability> --accepts <id>` for a trial's fix, and :48 (r12) needs to judge whether a fix needs a new
scenario or examples row, which the feature files tell. Requirement ids are reachable through a proposal's
`adds:`/`changes:` in `.shop/work/`, so the trial's fix is draftable when its requirement is in a proposal; a trial
finding a fix against a requirement no proposal of this initiative names leaves the session with no permitted source
for the id. No client hits this today. Reproduction: `grep -n "What you read" -A2 SKILL.md` (line 26: `.shop/work/`
alone) against `scripts/work:99-100` (`--under`, `--accepts` required). Fix: allow `spec/` (and `features/` for
r12) in "What you read", as the old text did (decision 0004 forbids code, not spec).

### F2 Minor, observation: `--part-of capability-proposal/<...>` for a trial's fix names no proposal
SKILL.md:47 keeps the drafting invocation's placeholder; a trial's fix belongs to no particular proposal, and the
text does not say which to give. The report names it as an open question. Fix: say which proposal (the one whose
requirement the fix accepts), when a line asks for it.

### F3 Minor, drop: exit 0 explained as "every work-item green"
SKILL.md:36. supervise.py exits 0 when every work-item is green *or withdrawn*, and also over an empty list (research
§2, D1). Pre-existing wording, unchanged by these commits; r6 asks to show the printout, which the skill does.

### F4 Minor, drop: the work-item's title promises the ledger with `work note`, the text still writes it by hand
w141's title says "writes the ledger with work note", but it accepts no r15; SKILL.md:50-51 still give
`.shop/scratch/run/ledger-<initiative>.md` and an archive move, contrary to decision 0066. w142 (accepts delivery#r15,
`researched`) owns that change; it should take :51 (the archive move) along with :50. Not this work-item's to fix.

Also outside the file set: README.md lines 57, 149, 206, 229, 250 still describe the drafting skill (report names them).

## Tools

- `tools check --base a102fce`: ruff "nothing to check"; vulture "nothing to check"; import-linter "the project
  states no import contracts".
- `tools size --limit 300`: printed nothing; no tracked Python file over the limit.

## Commands run

- `git log --format=%H -1 --grep="^work: w141 ready -> claimed$" work/w141` (refused: no such branch)
- `git log --oneline -25 --grep=w141`, `git log --oneline -15`
- `git log --stat a102fce..337f609`, `git diff a102fce 36ecb74`
- `git diff --stat a102fce 36ecb74 -- features/ tests/` (empty)
- `grep -l` over spec/decisions for the rests_on ids; `cat` of decisions 0065, 0066, 0068
- `head .shop/work/i24-requests-and-the-context-loop/w142.md`; `grep -n ledger SKILL.md`
- `grep -n "accepts|under|part-of|required" scripts/work`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base a102fce`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
