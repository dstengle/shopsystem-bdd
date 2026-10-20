# Small Slices and Steps (0.11.0) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** size is measured before the work and held during it, and every agent's context stays small: a Small test and a `Lands:` count at slicing, expand/migrate/contract, tasks with research and Steps, a `code-scout` agent, an implementer with step mode, fix mode, `PARTIAL` and a rule against removing tests, reviewers that scope and write findings to a file, and a thin controller with lanes.

**Architecture:** prose changes to one skill's rules and hand-off, three agents and one new agent, plus one validated line in `scripts/plan`. Each prose change is tested as this repository tests skills: a headless baseline on a fixture before the edit, the same prompt after.

**Tech Stack:** Markdown skills and agents; Python 3 standard library (`scripts/plan`, `unittest`); `claude -p --plugin-dir` for headless runs.

**Spec:** `docs/superpowers/specs/2026-10-10-small-slices-and-steps-design.md`. Executors read it; each task below names the change number it implements, and the spec's wording of a rule is the rule.

## Global Constraints

- Budgets, verbatim from the spec: a slice lands in at most **8 production modules and 4 test modules**; a task landing in more than **about 5 files** is written as Steps; an implementer that has touched more than **about 15 files** replies `PARTIAL`.
- Line formats, exact: `- Lands: <p> production, <t> test`; `Probe: <search> -> <p> production, <t> test`; `Lane: <letter>`; the task part is titled **Tests the decisions break**.
- Statuses the implementer may reply: `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `NEEDS_CONTEXT`.
- The scout writes only under `.superpowers/scout/<run>/`; its model is `haiku`.
- House style of the skills and agents: short declarative sentences, no em dashes, British spelling ("behaviour"), rationalization tables as `| Excuse | Reality |`.
- No file of a consuming repository's `CLAUDE.md` is asked to carry a rule.
- Script tests: `python3 -m unittest discover -s tests/scripts` passes after every task.
- Fixtures and transcripts live in the session scratchpad, never in this repository. Only the test log is committed.
- Branch `0.11.0-small-slices-and-steps`. Commits end with the `Co-Authored-By` trailer.

## Review Focus

1. **A plan written before 0.11.0** (no `Lands:` line) still loads, edits and archives. Owner: Task 2, `test_a_slice_without_lands_stays_valid`.
2. **A `Lands:` exactly at the budget** (8 and 4) is accepted; 9 or 5 is refused. Owner: Task 2.
3. **`plan status` on a plan holding an over-budget slice** is refused like any other invalid plan, and the message names the slice and the budget, so the person knows why an unrelated edit failed. Owner: Task 2.
4. **An implementer in step mode whose report file does not exist yet** (the first step) creates it and does not report `NEEDS_CONTEXT`. Owner: Task 5's wording, pinned by Task 1's step-mode fixture.
5. **A test the brief lists under "Tests the decisions break"** is changed without a stop, so the new rule does not block the work the plan decided. Owner: Task 5's wording, pinned by a second run of the breaking-test fixture with the test listed.

---

### Task 1: Fixtures and baselines (RED), before any edit

**Files:** scratchpad only: `fixtures/make_shelf.py` and the transcripts. Nothing in this repository changes.

One generated fixture project, `shelf`, serves every case: a pytest-bdd project whose ids are spelled `"<kind>/<slug>"`, with 12 small production modules and 8 test modules that spell the form, a `CLAUDE.md` with a module map, `spec/` with two capability files, `features/`, a living slice plan with a suite record, and a `.venv`. Variants are commits or briefs on top of it.

- [ ] **Step 1:** write `make_shelf.py`; generate the fixture; run its suite; commit inside the fixture.
- [ ] **Step 2:** write the briefs and packages for each case:
  - `slicing`: an approved capability change, "an id is an https IRI the client chooses", with its scenarios formulated and untagged. Prompt: invoke `shopsystem-bdd:slicing-into-increments`, stop before writing-plans.
  - `breaking-test`: a brief with two decisions that together make one unlisted plain test fail. Prompt: dispatch `bdd-implementer`.
  - `breaking-test-listed`: the same, the test listed under "Tests the decisions break" as "rewritten to ...".
  - `steps`: a brief with three Steps. Prompt: dispatch `bdd-implementer` naming step 1, then 2, then 3, the same report file.
  - `partial`: a brief for the whole migration (20 files) as one task.
  - `fix`: a finished task, its report, a findings file with two findings. Prompt: dispatch `bdd-implementer` in fix mode.
  - `review-deleted`: a diff that removes one parametrize case the brief does not list. Prompt: dispatch `bdd-task-reviewer`, findings file named.
  - `review-scoped`: the same package with a dispatch that gives `tests/` as its paths.
- [ ] **Step 3:** run each prompt headless against the unedited plugin (`claude -p --model opus --plugin-dir <checkout at 34279e8>`, stream-json to a transcript). Cases that depend on text that does not exist yet (`steps`, `fix`, `review-scoped`, `breaking-test-listed`) get no baseline: say so in the log.
- [ ] **Step 4:** record for each baseline what the agent did, quoted, in the test log draft (scratchpad).

### Task 2: `plan` holds and checks `Lands:` (spec change 8)

**Files:** Modify `scripts/plan`; Test `tests/scripts/test_plan.py`.

**Interfaces:** Produces `plan add-slice ... --lands "<p> production, <t> test"` (optional) and validation of any `- Lands:` line; constants `LANDS_PRODUCTION = 8`, `LANDS_TEST = 4`.

- [ ] **Step 1: failing tests**

```python
    def lands(self, text):
        self.plan.write_text(PLAN.replace("- Status: planned", "- Lands: %s\n- Status: planned" % text))
        return self.run_script("check")

    def test_a_slice_without_lands_stays_valid(self):
        self.assertEqual(self.run_script("check").returncode, 0)
        self.assertEqual(self.run_script("status", "2", "green").returncode, 0)

    def test_lands_at_the_budget_is_accepted(self):
        self.assertEqual(self.lands("8 production, 4 test").returncode, 0)

    def test_lands_over_the_budget_is_refused_naming_slice_and_budget(self):
        for text in ("9 production, 4 test", "8 production, 5 test"):
            done = self.lands(text)
            self.assertEqual(done.returncode, 1)
            self.assertIn("slice 2: Lands %s is over the budget of 8 production, 4 test" % text, done.stderr)

    def test_a_malformed_lands_is_refused(self):
        done = self.lands("about twenty files")
        self.assertEqual(done.returncode, 1)
        self.assertIn("slice 2: Lands must be '<p> production, <t> test'", done.stderr)

    def test_an_edit_is_refused_while_a_slice_is_over_budget(self):
        self.lands("30 production, 20 test")
        done = self.run_script("status", "2", "in progress")
        self.assertEqual(done.returncode, 1)
        self.assertIn("over the budget", done.stderr)

    def test_add_slice_writes_lands_before_status(self):
        done = self.run_script("add-slice", "3", "Remove", "--kind", "capability", "--scenarios", "cart / Removing",
                               "--observable", "gone", "--lands", "2 production, 1 test")
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("- Needs: none\n- Lands: 2 production, 1 test\n- Status: planned\n", self.plan.read_text())

    def test_add_slice_refuses_lands_over_the_budget(self):
        done = self.run_script("add-slice", "3", "Remove", "--kind", "capability", "--scenarios", "cart / Removing",
                               "--observable", "gone", "--lands", "12 production, 1 test")
        self.assertEqual(done.returncode, 1)
        self.assertNotIn("Slice 3", self.plan.read_text())

    def test_archive_keeps_a_green_slices_lands(self):
        self.plan.write_text(PLAN.replace("- Status: green", "- Lands: 3 production, 2 test\n- Status: green"))
        self.assertEqual(self.run_script("archive", "b1").returncode, 0)
        archived = (self.plan.parent / "archive" / "cart-slices-b1.md").read_text()
        self.assertIn("- Lands: 3 production, 2 test", archived)
```

- [ ] **Step 2:** run `python3 -m unittest discover -s tests/scripts`; the new tests fail (unknown `--lands`; over-budget accepted).
- [ ] **Step 3: implement.** A `LANDS = re.compile(r"(\d+) production, (\d+) test$")` beside `STATUS`; in `_slice_problems`, when `b.field("Lands")` is not None: no match gives `"%s: Lands must be '<p> production, <t> test'"`; over either constant gives `"%s: Lands %s is over the budget of 8 production, 4 test"` (numbers from the constants). `add-slice` gains `--lands` and writes the line between Needs and Status when given. The `CONTRACT` text gains one bullet stating the line, the budget, and that a slice without it is valid.
- [ ] **Step 4:** run the tests; all pass. Commit.

### Task 3: `agents/code-scout.md` (spec change 4)

**Files:** Create `agents/code-scout.md`.

- [ ] Frontmatter: `name: code-scout`; a description ending "Dispatched by slicing-into-increments and by the planner under writing-plans; not for general use."; `tools: Read, Glob, Grep, Bash, Write`; `model: haiku`.
- [ ] Body, in the order of the other agents: what it is and may not do (reads the named repository, changes nothing in it, one notes file under `.superpowers/scout/<run>/`, no whole-suite run, builds nothing, no other agents); **Lands probe** (inputs, method: search for the old form, read `CLAUDE.md`'s map, count files not matches, generated files included, say what a search cannot see); **Task research** (the four parts with their exact titles: Why it is red today, Where the change lands, Steps and helpers to reuse, Tests the decisions break; "none found" only with what was checked; it finds conflicts and never decides them); the reply (counts, one line per conflict, the path, under ten lines).
- [ ] Commit.

### Task 4: `skills/slicing-into-increments` (spec changes 1, 2, 3, 7)

**Files:** Modify `skills/slicing-into-increments/SKILL.md`.

- [ ] "What a Slice Is": "Four tests"; add **Small** with the budget and "counting the migration of existing code and tests it forces".
- [ ] Process step 2: add **Count where it lands** (the scout's Lands probe for a slice that changes a form existing code depends on, the `Probe:` log line, an estimate for a slice that only adds, the hard budget, "Steps are not a way to keep an over-budget slice") and **Cut a breaking change expand, migrate, contract** with the four parts and the shortened slice-156 example.
- [ ] Process step 3: the walking skeleton is the first capability slice after expand.
- [ ] Process step 4: `add-slice --lands`.
- [ ] The Hand-off: bullets for research by scout (notes file read, not the source), **Tests the decisions break**, **Steps** (over about 5 files; each step's what, check, where it lands; not slices, no number, no tag), the re-count and the return to slicing for a task over budget, `Lane:`, and the execution rules the Global Constraints carry (spec change 7, as a quoted block the planner copies).
- [ ] The Plan File: the `- Lands:` line in the template and the `Probe:` form for a count in the Log.
- [ ] Rationalizations: the request's row, plus rows the baseline's own words give. Red flags: the three from the spec, plus "a migrate slice whose check has no search".
- [ ] Commit.

### Task 5: `agents/bdd-implementer.md` and `skills/bdd-red-green` (spec change 5)

**Files:** Modify `agents/bdd-implementer.md`, `skills/bdd-red-green/SKILL.md`.

- [ ] Implementer: a "Modes" section (whole task, one step, fix); step mode reads the report first and creates it when the step is the first; a step ends green with one whole-suite run and its record in the report; only the last step, and never an implementer in a lane, makes the checkpoint commit; **PARTIAL** with the 15-file measure and how to count it; the removed-test stop condition with what counts as weakening and the exception for tests the brief lists; statuses listed; the "If resumed with review findings" bullet replaced by fix mode.
- [ ] bdd-red-green: a stop-condition row ("An existing test can only stay green by being removed, loosened, skipped or xfailed, and the brief does not list it"), a rationalization row, a red flag; "Run Discipline" or its equal says a step of a task runs the whole suite once before its commit.
- [ ] Commit.

### Task 6: reviewers (spec change 6)

**Files:** Modify `agents/bdd-task-reviewer.md`, `agents/bdd-branch-reviewer.md`.

- [ ] Task reviewer: `tools:` gains `Write`, and the opening paragraph says its one write is the findings file the dispatch names; Inputs gain optional paths and the findings file; a "Scoped by area" section (`git diff <base> <head> -- <paths>`, say what was not reviewed); a "Removed and weakened tests" section; Output: the full review goes to the findings file, the reply is the verdict, one line per issue with grade, the backlog lines and the path.
- [ ] Branch reviewer: the removed-and-weakened-tests bullet under "How you review" and a line in Output.
- [ ] Commit.

### Task 7: green runs, test log, README, version (spec change 9)

**Files:** Create `docs/superpowers/testing/2026-10-10-small-slices-and-steps-test-log.md`; Modify `README.md`, `.claude-plugin/plugin.json`.

- [ ] Run every Task 1 prompt against the edited checkout. A case that fails gets a wording fix and a re-run, each iteration logged, as the earlier logs do.
- [ ] The scout comparison: the two dispatches of the spec's Evidence on kb at `bd159cd^`, through `shopsystem-bdd:code-scout`, three runs on Haiku and three on Sonnet each, scored against the commit's files and the report's removed tests. Haiku stays the default unless it misses what Sonnet finds in most runs.
- [ ] Write the test log: fixtures, prompts, baselines quoted, edits, green runs, the comparison table.
- [ ] README: the 0.11.0 section; `code-scout` in the agents line and table; the task reviewer's row and the "what stays a request" note on Write; the subagent-driven-development note points to the plan's Global Constraints; the `plan` script line mentions `Lands:`.
- [ ] `plugin.json` to `0.11.0`.
- [ ] `python3 -m unittest discover -s tests/scripts`; commit.
