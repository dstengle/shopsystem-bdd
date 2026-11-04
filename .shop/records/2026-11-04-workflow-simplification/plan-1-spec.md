---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-1
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# Plan 1: The New Workflow Codified — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write the simplified workflow's requirements in the codified language: its lexicon, nine new capabilities
and their generated scenarios. Every requirement is marked unbuilt, so its scenarios are expected failures until a
later plan builds it.

**Architecture:**
- The lexicon goes into `spec/index.md`'s Glossary and Relations.
- Each capability is one file under `spec/capabilities/`, whose lines parse in the context's grammar and pass
  `model logic`.
- `features generate` writes each service capability's feature, and a test module binds it.
- A new frontmatter field `unbuilt: [r<n>, ...]`, read by `scripts/spec_unbuilt.py`, makes the plugin's pytest plugin
  mark those requirements' scenarios xfail.
- No workflow code is written in this plan.

**Tech Stack:** Python 3 (standard library), GF 3.12 with pgf, clingo, pytest and pytest-bdd. All are already
installed; run `python3 scripts/tools probe` if unsure.

**Spec:** `.shop/records/2026-11-04-workflow-simplification/design.md`, with `roadmap.md` beside it (which plan builds
which capability).

## Global Constraints

- **Base:** the branch `workflow-simplification`, which sits on `gf-conversion`.
- **File size:** every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300`).
- **Module map:** a new module gets a row in `CLAUDE.md`'s module map.
- **Retire, never edit:** spec lines are never edited, only retired and replaced. This plan adds lines and terms only.
  It changes no existing requirement, group or term.
- **New capability files:** each one's frontmatter has `language: codified-1`, `retired: []`, one `narrator`, one
  `group` (`service` or `guarantees`) and `unbuilt:` listing every one of its requirement ids.
- **Baselines:** every task keeps these, and none may rise.
  - `model check`: 53 violations, 16 warnings, 29 unresolved references, 0 file problems.
  - `model logic`: `11 findings: 6 L5, 5 L6`. New lines add no L0, L1, L2, L3 or L4. An L5 or L6 on a new line is fixed by rewording the line or by defining its
    condition in the controlled language.
  - The suite: `python3 -m pytest -q` passes (941 passed and 1 skipped today, plus the new xfails).
  - `features generate --check` passes for every existing capability.
- **Wording:** lines use the names the design uses for the person: item, backlog, batch, pull request, decision.
  A line that names a command writes it in backticks.
- **Refused lines:** when the grammar refuses a line, reword it keeping its meaning. Use the hint `model parse` prints
  ("parsed up to", "nearest words"). If a meaning cannot be said in the grammar, write that line as a group of its
  capability's `## Not yet` section with the refusal, and go on. Do not extend the grammar in this plan.

## Review Focus

1. **Collisions with existing words.** A new term may change how an existing line parses: "turn" is already a
   resource, "open" is already a condition, "batch" appears in batch-measurement's prose, and "status" exists for other
   kinds. Expected: every existing capability's feature is byte-identical after the lexicon changes. Pinned in Task 2,
   Step 4.
2. **One command, two kinds of thing.** New lines on `work withdraw` and `work answer` for an item sit beside old lines
   on the same commands for a work-item. Expected: `model logic` reports no L1 between an old line and a new one.
   Pinned in each capability task's logic step.
3. **An `unbuilt:` id that names nothing.** For example a typo `r99` in a capability with 12 requirements. Expected: it
   is reported as a problem and marks nothing. Pinned in Task 1's test
   `test_an_unbuilt_id_the_capability_lacks_is_a_problem`.
4. **Hiding a built scenario.** The xfail mark must touch only the scenarios of the listed ids in that capability, and
   must be non-strict, so that a scenario that starts passing shows as XPASS and is not hidden. Pinned in Task 1's test
   `test_a_capability_without_unbuilt_marks_nothing`.
5. **Bindings.** Every new feature is bound by exactly one test module, and `features bindings --unbound` stays clean.
   Pinned in Task 11.

---

### Task 1: The `unbuilt:` mark

**Files:**
- Create: `scripts/spec_unbuilt.py`
- Modify: `scripts/work_items.py` (add one call in its `pytest_collection_modifyitems`; it is at 245 lines)
- Modify: `CLAUDE.md` (a module-map row)
- Test: `tests/scripts/test_spec_unbuilt.py`

**Interfaces:**
- Produces:
  - `unbuilt(root: pathlib.Path) -> dict[str, set[str]]`: capability name → the requirement ids (`"r3"`) its
    `unbuilt:` lists, for codified capabilities only.
  - `problems(root: pathlib.Path) -> list[str]`: one line for each listed id the capability has no requirement for,
    `"<cap>: unbuilt r<n> is no requirement of the capability"`.
  - `mark(items, root) -> None`: adds `pytest.mark.xfail(strict=False, reason="unbuilt: <cap>#r<n>")` to each
    pytest-bdd scenario item whose feature stem is a capability with an `unbuilt:` id among the item's `r<n>` marks.
- Consumes: `spec_read.capability(path)` for the requirement ids and `model_parse.frontmatter`.

- [x] **Step 1: Write the failing tests** in `tests/scripts/test_spec_unbuilt.py`. They use `unittest` with a
  temporary root holding `spec/capabilities/demo.md` (codified, two groups g1 = r1 and g2 = r2), in the style of
  `tests/scripts/test_spec_read.py`.
  - `test_unbuilt_reads_the_listed_ids`: with `unbuilt: [r2]`, assert `unbuilt(root) == {"demo": {"r2"}}`.
  - `test_a_capability_without_unbuilt_marks_nothing`: with no field, assert `unbuilt(root) == {}`, and that `mark`
    on a fake item with marks `g1` and `r1` from `demo.feature` adds no marker.
  - `test_an_unbuilt_id_the_capability_lacks_is_a_problem`: with `unbuilt: [r9]`, assert
    `problems(root) == ["demo: unbuilt r9 is no requirement of the capability"]` and `unbuilt(root) == {}`.
  - `test_mark_adds_a_non_strict_xfail`: with `unbuilt: [r2]`, an item with marks `g2` and `r2` from `demo.feature`
    gets exactly one xfail marker, with `strict=False` and the reason `"unbuilt: demo#r2"`.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_spec_unbuilt.py -q`
  Expected: FAIL with `ModuleNotFoundError: spec_unbuilt`.

- [x] **Step 3: Implement `spec_unbuilt.py`** (standard library and pytest only). Then call
  `spec_unbuilt.mark(items, root)` from `work_items.py`'s collection hook on every run, not only under
  `--whole-suite`. Give `root` the same way that hook finds the spec.

- [x] **Step 4: Run the tests and the suite.**
  Run: `python3 -m pytest tests/scripts/test_spec_unbuilt.py -q && python3 -m pytest -q`
  Expected: 4 passed; the suite 945 passed, 1 skipped.

- [x] **Step 5: Check that `model check` takes the field.** Add `unbuilt: []` to `spec/capabilities/trials.md`'s
  frontmatter as a probe. Run `python3 scripts/model check | tail -1`.
  Expected: `53 violations, 16 warnings, 29 unresolved references, 0 file problems`. If a file problem appears, add
  `unbuilt` to the frontmatter keys `scripts/model_spec.py` accepts. Then remove the probe.

- [x] **Step 6: Commit.** Add the CLAUDE.md row first:
  `| scripts/spec_unbuilt.py | a capability's unbuilt: ids, their problems, and the xfail mark the pytest plugin puts on their scenarios |`.
  ```bash
  git add scripts/spec_unbuilt.py scripts/work_items.py tests/scripts/test_spec_unbuilt.py CLAUDE.md
  git commit -m "spec_unbuilt: a capability's unbuilt requirements run as expected failures"
  ```

### Task 2: The lexicon and the decision

**Files:**
- Modify: `spec/index.md`: a new block at the end of `## Glossary`, rows at the end of `## Relations`, and a sentence
  in "Where it stands".
- Create: `spec/decisions/0074-the-workflow-simplified.md`, in the frontmatter form of `0073`, with `status: accepted`,
  `source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design]` and
  `by: "the person, 2026-11-04, in the brainstorming of the workflow simplification"`. Its decision paragraph
  summarises the design's goals 1-10 in one paragraph.
- Regenerate: `spec/decisions/index.md` (`python3 scripts/model decisions`).

**Terms to add**, in the glossary's own form. The definitions are fixed here; the wording around them may be adjusted
for the grammar:
- **item** (kind): one entry of the backlog: work this bounded context may do, with its requirement lines, its origin
  and its ratings, named by its id `b<n>` and its title.
- **backlog** (kind): every item of a bounded context, kept in `.shop/backlog/`.
- **batch** (kind): ready items built together on one branch and closed by its pull request, named `batch-<n>`.
  Plural: batches.
- **batch plan** (kind): the file `.shop/batches/<n>/plan.md`, with a batch's tasks and their statuses.
- **task** (kind): one unit of a batch plan, built in its own worktree.
- **pull request** (kind): the GitHub pull request of a batch's branch.
- **quote** (kind): the person's words cited by a file, with its session, its message and the messages around it.
- **message** (kind): one turn of the person or of a session in a transcript, without its tool uses.
- **status** (attribute of item): Values: `idea`, `shaped`, `ready`, `in-batch`, `delivered`, `needs-input`,
  `refused`, `withdrawn`. Transitions:
  - `idea` → `shaped`: `work shape`;
  - `shaped` → `ready`: `work ready`;
  - `ready` → `shaped`: pick;
  - `ready` → `in-batch`: pick;
  - `in-batch` → `delivered`: merge;
  - `in-batch` → `needs-input`: park;
  - `needs-input` → `shaped`: `work answer`;
  - `idea` → `refused` and `shaped` → `refused`: `work refuse`;
  - `idea`, `shaped`, `ready` and `needs-input` → `withdrawn`: `work withdraw`.
- **origin** (attribute of item): Values: `own`, `peer`, `product`.
- **value** (attribute of item): Values: `low`, `medium`, `high`.
- **urgency** (attribute of item): Values: `low`, `medium`, `high`.
- **size** (attribute of item): Values: `low`, `medium`, `high`.
- **status** (attribute of batch): Values: `building`, `in-review`, `awaiting-merge`, `merged`, `abandoned`.
  Transitions:
  - `building` → `in-review`: `work batch review`;
  - `in-review` → `building`: a fix-now finding;
  - `in-review` → `awaiting-merge`: a clean review;
  - `awaiting-merge` → `merged`: merge;
  - `building` → `abandoned` and `in-review` → `abandoned`: `work batch abandon`.
- **status** (attribute of task): Values: `pending`, `running`, `done`, `failed`.
- **tier** (attribute of design-decision): Values: `check`, `requirement`, `judgement`.
- **blocked** (condition of item): an item that depends on an item that is not `delivered` and is not in the same
  batch.
- **passing** (condition of item): an item whose every requirement parses, has no L0 or L1 finding of `model logic`
  with the item's lines laid over `spec/`, and has its scenarios written by `features generate`.
- **clean** (condition of pull request): a pull request whose review lists no review finding to fix now.
- **pick** (event): `work batch start` takes a ready item into a batch, or returns it to `shaped` when it is no longer
  passing. Forms: picks, picked.
- **park** (event): a batch sets an item it cannot finish without an answer to `needs-input`. Forms: parks, parked.
- **publish** (event): `work` puts a batch's branch on GitHub as a pull request. Forms: publishes, published.

**Relations to add:** each row is from, word, to, then cardinality (blank where none).

| from | word | to | cardinality |
|---|---|---|---|
| item | depends on | item | |
| item | proposes | requirement | |
| item | in | batch | one |
| item | asked by | bounded context | |
| task | of | batch | one |
| pull request | of | batch | one |
| review finding | on | pull request | |
| quote | from | session | one |
| quote | cites | message | |
| design-decision | enforced by | test | |

- [x] **Step 1: Save the baseline.** Copy `features/` to a scratch directory (`<saved-dir>`), then write the terms
  and the relations.
- [x] **Step 2: Check the lexicon.**
  Run: `python3 scripts/model lexicon --check`
  Expected: no problem lines.
- [x] **Step 3: Probe that the new terms parse.** Each must print a tree:
  - `python3 scripts/model parse "When the person runs \`work backlog\`, \`work\` shall print every item and the status of the item."`
  - `python3 scripts/model parse "When the person runs \`work batch abandon\` on a batch that is \`building\`, \`work\` shall set the status of the batch to \`abandoned\`."`
- [x] **Step 4: Check that existing features are unchanged.**
  Run: `python3 scripts/features generate --check && diff -r <saved-dir> features/`
  Expected: `--check` passes and the diff is empty.
- [x] **Step 5: Check logic, the model and the suite.**
  Run: `python3 scripts/model logic | tail -1; python3 scripts/model check | tail -1; python3 -m pytest -q | tail -1`
  Expected: the three baselines unchanged (`11 findings: 6 L5, 5 L6`; `53 violations, ...`; all passed).
- [x] **Step 6: Commit.**
  ```bash
  git add spec/index.md spec/decisions/
  git commit -m "spec: the simplified workflow's lexicon and decision 0074"
  ```

### Tasks 3-10: one capability each

Every capability task has the same steps. Its own section below gives the file, the frontmatter, the groups and the
test module.

- [ ] **Step 1: Write the capability file**, with its frontmatter, `# <Title>`, `## Purpose` (two to four sentences
  from the design goal it serves), `## Terms` (only where its section names some) and `## Behaviour`. Each group is
  `### [g<n>] <title>` followed by its `- [r<n>] <line>`. There is no `Restates:`. List every `r<n>` in `unbuilt:`.
- [ ] **Step 2: Parse it.**
  Run: `python3 scripts/model parse --file spec/capabilities/<cap>.md`
  Expected: a tree for every line. Reword any refused line, as the Global Constraints say.
- [ ] **Step 3: Check its logic.**
  Run: `python3 scripts/model logic | grep '<cap>#'; python3 scripts/model logic | tail -1`
  Expected: no finding naming the capability, and the total unchanged at `11 findings: 6 L5, 5 L6`.
- [ ] **Step 4: Generate its feature** (service capabilities only).
  Run: `python3 scripts/features generate <cap> && python3 scripts/features generate --check`
  Expected: `features/<cap>.feature` is written, with one scenario a group, and `--check` passes.
- [ ] **Step 5: Bind it** (service capabilities only). Create `tests/scenarios/test_<cap_underscored>.py`. Its
  docstring names the feature and says its scenarios are unbuilt (plan 1); its body is `scenarios("<cap>.feature")`,
  as in `tests/scenarios/test_analysis_tools.py`. Write no handlers.
  Run: `python3 -m pytest tests/scenarios/test_<cap_underscored>.py -q | tail -1`
  Expected: every scenario `xfailed`, none failed and none errored.
- [ ] **Step 6: Add its row** to `spec/index.md`'s Composition table: a new sub-table headed "The simplified
  workflow (plan 1, unbuilt):". Then check the model and the suite.
  Run: `python3 scripts/model check | tail -1; python3 -m pytest -q | tail -1`
  Expected: the model check baseline unchanged, apart from a `w_unserved_cap` warning, which is accepted. The suite
  passes.
- [ ] **Step 7: Commit:** `git commit -m "spec: <cap>, codified and unbuilt"`.

The lines each section gives are target lines. Where the grammar takes one as written, use it as written.

#### Task 3: `backlog` (service)

- **Frontmatter:** narrator `a person or session keeping the backlog`; `rests_on:
  [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]`.
- **Groups:**
  1. **`work idea` writes an item:** When the person runs `work idea`, `work` shall write an item that is `idea` and
     commit the item.
  2. **`work shape` shapes an idea:** When the person runs `work shape` on an item that is `idea`, `work` shall set the
     status of the item to `shaped`.
  3. **`work shape` refuses an item that is not an idea:** the refusal names the status and changes nothing.
  4. **`work rate` sets an item's ratings:** its value, urgency and size.
  5. **`work depend` records a dependency:** of an item on an item.
  6. **`work backlog` prints the backlog:** every item with its status, origin and ratings.
  7. **`work backlog` marks a blocked item:** prints the items it depends on.
  8. **`work backlog --json` prints one JSON object:** exits successfully.
  9. **`work withdraw` on an item:** an `idea`, `shaped`, `ready` or `needs-input` item becomes `withdrawn`.
  10. **`work refuse` on an item:** an `idea` or `shaped` item becomes `refused`.
  11. **Names beside ids:** every item `work` prints is printed with its title.
- **Test module:** `tests/scenarios/test_backlog.py`.

#### Task 4: `readiness` (service)

- **Groups:**
  1. **`work ready` readies a passing item:** While an item is `shaped` and the item is passing, when the person runs
     `work ready` on the item, `work` shall set the status of the item to `ready`.
  2. **`work ready` refuses an item that is not passing:** it names the first failing check and changes nothing.
  3. **`work ready` refuses an item that is not shaped.**
  4. **`work ready` reads no answer from the person:** a Ubiquitous line that `work ready` asks no question.
- **Test module:** `tests/scenarios/test_readiness.py`.

#### Task 5: `intake` (service)

- **Groups:**
  1. **A peer's request becomes an item:** When a session runs `work intake` on a request whose upstream is this
     bounded context, `work` shall write an item that is `shaped`, whose origin is `peer`, asked by the asker of the
     request.
  2. **Accept:** `work outcome` with `accepted` on a request line keeps the line on the item.
  3. **Refuse with a reason:** `work outcome` with `refused` writes the reason, and the item drops the line.
  4. **Counter-propose:** `work outcome` with `rewritten` writes the counter line and passes the turn to the asker.
  5. **No person in the loop:** intake starts no question to the person while the turn is the upstream's.
  6. **An item whose every line is settled and passing:** it may be readied.
- **Note:** the brainstorming route of design goal 4 is a skill. It goes in Task 9 as a guarantees line, not here.
- **Test module:** `tests/scenarios/test_intake.py`.

#### Task 6: `batches` (service)

- **Groups:**
  1. **`work batch start` picks ready items:** in rank order, unblocked, up to `batch_size` of `.shop/delivery.toml` (a new key, default 4).
     It writes a batch that is `building` and a batch plan, and sets each picked item `in-batch`.
  2. **A ready item that is no longer passing is returned:** `shaped`, not picked.
  3. **A blocked item is not picked.**
  4. **`work batch status` prints where the batch stands:** every item of the batch, every task and its status.
  5. **`work batch resume` carries on:** a batch that is `building`, from the batch plan, without a person.
  6. **A park leaves the rest building:** when a task needs an answer, the batch parks its item to `needs-input`; the
     other items stay `in-batch`.
  7. **A parked item's commits stay out of the pull request.**
  8. **`work batch review` publishes:** when every task of a `building` batch is `done`, `work batch review` publishes
     a pull request and sets the batch `in-review`.
  9. **The merge delivers:** when the person merges the pull request of a batch, every item of the batch that is
     `in-batch` becomes `delivered`.
  10. **`work batch abandon`:** the batch becomes `abandoned`, and its items return to `ready`.
- **Test module:** `tests/scenarios/test_batches.py`.

#### Task 7: `pr-review` and `brainstorming` (guarantees)

- **Frontmatter:** narrator `the person who merges a batch's pull request`; no feature and no test module.
- **Groups:**
  1. **One review a batch:** a pull request is reviewed once by the `pr-reviewer`, not after each task.
  2. **Correctness against the items' requirements.**
  3. **Engineering quality:** the repository's rules, the `judgement` decisions, and the change's size.
  4. **Only the batch's commits are read:** from the branch's base to its head.
  5. **A fix-now finding:** it sets the batch back to `building`, and the next review reads only what the fix
     changed.
  6. **A clean pull request:** it sets the batch `awaiting-merge`, and asks the person to merge.
  7. **Findings recorded with their grade:** under `.shop/batches/<n>/`.
- **A second file, `brainstorming`** (guarantees, design goal 4):
  - **Frontmatter:** narrator `the person shaping work in a conversation`; no feature.
  - **Groups:**
    1. **Lines are written:** a brainstorming that ends in items writes each item's requirement lines and runs
       `work ready` on each.
    2. **Nothing waits on the person's reading:** the person may skim the lines in the backlog and in the pull
       request.
    3. **A quote keeps its turns:** each of the person's words an item cites is written with `work quote`.

#### Task 8: `decision-tiers` (service)

- **Groups:**
  1. **Each decision has a tier:** `model check` reports a design-decision with no tier, as a warning while plan 6
     sorts them.
  2. **A `check` decision names its test:** one that names no test it is enforced by is a violation.
  3. **A `requirement` decision names its requirement.**
  4. **`model decisions --check` runs the tests:** it runs the tests the `check` decisions are enforced by, and exits
     with an error naming each failing decision.
  5. **A superseded decision is `superseded`:** a design-decision that another supersedes, but whose status is
     `accepted`, is a violation.
- **Test module:** `tests/scenarios/test_decision_tiers.py`.

#### Task 9: `telemetry` (service)

- **Groups:**
  1. **`measure batch` writes a measurement:** for a batch that is `merged`, with its wall time, session time, tokens
     and cost by role.
  2. **Review findings counted:** by grade.
  3. **A defect after merge traced:** `measure defect` on a delivered item records the defect against the item and
     its batch.
  4. **`measure compare` on two batches:** prints each figure side by side.
- **Test module:** `tests/scenarios/test_telemetry.py`.

#### Task 10: `conversation` (service)

- **Groups:**
  1. **`work quote` keeps the turns:** When a session runs `work quote` with the person's words, `work` shall write a
     quote with its session, its message and the two messages before it and after it, without tool uses, and commit
     the quote.
  2. **The prompt hook gives the session and transcript:** the UserPromptSubmit hook passes them to `work quote`.
  3. **`work show` on a quote prints its messages.**
  4. **The names table at SessionStart:** the SessionStart hook prints the title of every item and batch it names.
- **Test module:** `tests/scenarios/test_conversation.py`.

### Task 11: Whole-plan verification and records

**Files:** `.shop/records/README.md` (rows for `roadmap.md` and `plan-1-spec.md`).

- [ ] **Step 1: Bindings.**
  Run: `python3 scripts/features bindings --unbound`
  Expected: no output, exit 0.
- [ ] **Step 2: The baselines.**
  Run: `python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check; python3 scripts/tools size --limit 300; python3 -m pytest -q | tail -2`
  Expected:
  - `model check` at 53 violations or fewer, 0 file problems;
  - `model logic` at `11 findings: 6 L5, 5 L6`;
  - no lexicon problems;
  - `tools size` silent;
  - the suite passed, with the new scenarios xfailed.
- [ ] **Step 3: Count.**
  Run: `python3 -c "import sys; sys.path.insert(0,'scripts'); import pathlib, spec_unbuilt as u; d=u.unbuilt(pathlib.Path('.')); print(sum(map(len,d.values())), sorted(d))"`
  Expected: all nine capabilities, and a count equal to the number of `[r<n>]` lines in their files.
- [ ] **Step 4: Commit the records rows.**
  ```bash
  git add .shop/records/README.md
  git commit -m "records: the roadmap and plan 1 of the workflow simplification"
  ```
