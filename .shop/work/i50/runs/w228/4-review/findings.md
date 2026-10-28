# Review of w228 (supervision#r173)

**Verdict: DONE.** Nothing is Critical and nothing is to be fixed now. There are two Minor observations.

## Commits reviewed

- `a807b5b7` "work run: a glossary gate with no question asks for approval of the terms (r173)". It touches `scripts/supervise_glossary.py` (+12), `scripts/supervise_rounds.py` (+2/-1) and `tests/scenarios/supervision_proposal_steps.py` (+10/-1).
- The implementer's result lists `4f878184`. `git diff 4f878184 a807b5b7 -- scripts tests features` is empty, so the merged commit is the same change and the two lists agree. All three files are in the work-item's file set.

## Removed and weakened tests

None. I looked for deleted test functions, dropped parametrize cases, and removed or loosened asserts, skips and xfails. The test diff adds one Then step, `g1_one_question`, and adds `bullets` to an existing import. No existing step is changed. Nothing under `features/` changed.

## Allowances

The report gives "none", and the commit changes no existing test.

## Cannot verify

- The report says the work-item's scenarios gave "182 passed, 1 skipped". I did not rerun them. The brief's suite record has 1060 passed and 0 failed at a807b5b7, and the r173 scenario is not among the expected failures, so it passed.

## Checks

- `tools check --base 2c461ed7`:
  - ruff: 9 findings, none in lines this commit touched. Six are in `.shop/.../splice.py` scratch files, one is `supervision_integrate_steps.py:87`, and two are `RUF100` at `supervision_proposal_steps.py:102` and `:137`. Those two lines are not in the diff, so they were there before.
  - vulture: clean.
  - import-linter: the project states no contracts.
- `tools size --limit 300`: no file is over the limit.

## Findings

1. **Minor, observation**: `scripts/supervise_glossary.py:52-55`. If a glossary-proposal's `adds`, `changes` and `removes` are all empty, `named` is `[]` and the question reads "Are the terms of g1 approved as drafted? It ." That text makes no sense to the person reading it.
   - The implementer's report names this case as left open ("unchosen"). r173 names no such proposal, and none of today's scenarios writes one.
   - Reproduction: by reading the code. `", ".join([])` is `""`, so the format gives `"It ."`. I could not run a Python probe here.
   - Fix: when `named` is empty, leave out the second sentence.
2. **Minor, observation**: `scripts/supervise_glossary.py:53`. `i[len("term/"):]` cuts the first five characters off every id, whether or not it starts with `term/`, so an id in another form shows up cut short.
   - `withheld` reads ids with the same assumption, and every client writes `term/<term>`.
   - Fix: strip the prefix only when the id starts with it, for example with `removeprefix("term/")`.

Things I checked and found sound:

- The default from r117 (a capability gate with no question) is unchanged: `approval_question` returns None unless `kind` is `glossary-proposal`.
- `supervise_glossary` is already imported in `supervise_rounds.py` (line 11).
- The question is written through the existing `asked` → `move` path, so it lands under `## Questions` just as r117's question does.
- No behaviour beyond r173 was added.

## Commands run

- `git show --stat a807b5b7`, `git show a807b5b7`, `git show 4f878184 --stat`, `git diff 4f878184 a807b5b7 -- scripts tests features`
- `git diff 2c461ed7 a807b5b7 --stat`, `git log --oneline -1 a807b5b7^`
- `grep -n "r173\|r117\|r164" spec/capabilities/supervision.md`, `grep -n "import\|supervise_glossary" scripts/supervise_rounds.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 2c461ed7…`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
