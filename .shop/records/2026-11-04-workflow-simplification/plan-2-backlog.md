---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-2
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# Plan 2: Items and the Backlog — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `backlog` capability, so that all 17 of its requirements are built. That means item files in
`.shop/backlog/`, the item commands of `work`, `work backlog` printed in rank order with blockers and questions, and
every item named by its title next to its id. Each requirement's id leaves `unbuilt:` in the same commit that makes its
scenario pass.

**Architecture:**
- Four new modules behind `scripts/work`:
  - `backlog_items.py` reads and writes one item file.
  - `backlog_moves.py` holds the commands that change an item, each one commit.
  - `backlog_view.py` holds the score, rank, blockers, the tables and the JSON.
  - `backlog_cli.py` holds the argparse wiring, so `scripts/work` stays small.
- `work withdraw`, `work show` and `work answer` already exist for work-items. They go to the backlog when their
  argument has the item id form `b<n>`, and keep their old behaviour otherwise.
- The scenarios of `features/backlog.feature` get handlers in `tests/scenarios/backlog_handlers.py`, over a scenario
  world in `tests/scenarios/backlog_world.py`.
- Some steps have a registry key that another capability already claims, such as `ThenPrints` with `` `work` `` or
  `GivenR` with `on`. Those are taken through `work_queue_world`'s `local` table, so `test_backlog.py` binds with
  `bind_all`, as `test_work_queue.py` does.

**Tech Stack:** Python 3 (standard library), git, pytest, pytest-bdd and xdist; GF 3.12 with pgf and clingo for the
step vocabulary. All are installed; run `python3 scripts/tools probe` if unsure.

**Spec:** `spec/capabilities/backlog.md` (its lines are the acceptance tests) and
`.shop/records/2026-11-04-workflow-simplification/design.md` goals 1, 2 and 10. Read them beside:
- `roadmap.md` (plan 2's row);
- `plan-1-rulings.md`, "Known gaps for later plans", whose items for plan 2 are settled in "Decisions" below.

## Global Constraints

- **Base:** a new branch `plan-2-backlog` from `workflow-simplification` at `14084b2f` or later. Plan 1 is not yet
  merged to `main` (decision D1).
- **File size:** every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300`).
  `scripts/work` is at 192 lines and may grow by at most 25.
- **Module map:** every new module gets a row in `CLAUDE.md`'s module map, in the task that creates it.
- **Strict xfail:** `spec_unbuilt.mark` uses `strict=True`.
  - A scenario whose id is in `unbuilt:` and passes fails the suite as `XPASS(strict)`. So a task removes an id from
    `spec/capabilities/backlog.md`'s `unbuilt:` in the same commit that makes its scenario pass, and never before.
  - When a task's suite run shows an `XPASS(strict)` for a backlog scenario the task does not name, read that
    scenario. If it tests its point, remove its id in that commit and say so in the report. If it passes vacuously,
    fix the handler so it checks its point.
- **Spec lines:** this plan edits no requirement line, group or term of any capability. In `backlog.md` it changes only
  the frontmatter's `unbuilt:` and the prose sections `## Implementation, may change` (new) and `## Not yet` (Task 4).
  A line found wrong is reported, not changed.
- **No new scenario keys in the registry where one exists:** a handler for a (template, term) another capability
  already claims goes through `local(template, kind)`. `python3 scripts/features vocab --check` must keep printing
  `every step has one handler`, and `vocab.duplicates()` must stay empty.
- **Old behaviour kept:** `work withdraw`, `work show` and `work answer` on a work-item, an initiative or a request
  behave as before. `tests/scenarios/test_work_queue.py`, `test_requests.py` and the `tests/scripts/test_work_*.py`
  tests pass unchanged.
- **Refusals:** a refused command raises `workqueue.Refused`. `scripts/work` prints it as `work: <message>` on stderr
  and exits 1. The repository is left byte-identical, and the U3 check holds.
- **Names next to ids:** every line `work` prints about an item names it by `backlog_items.label(item)`, as
  `b3 "Fix the parser"` (design goal 10). This covers confirmations, refusals and tables.
- **Baselines** (at `14084b2f`). Every task keeps them, and none may get worse:
  - `python3 -m pytest -q`: `951 passed, 1 skipped, 54 xfailed`. Each built scenario moves from xfailed to passed. At
    the end the count is 37 xfailed and no failures.
  - `python3 scripts/model check | tail -1`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`.
  - `python3 scripts/model logic | tail -1`: `11 findings: 6 L5, 5 L6`.
  - `python3 scripts/features generate --check`: exit 0. `features/backlog.feature` is never regenerated by hand or
    edited.
  - `python3 scripts/features bindings --unbound`: `every binding names a scenario`.
  - The known flake `tests/scripts/test_revision_done.py::test_model_logic_on_the_live_spec_is_fast` may fail once
    under xdist. Rerun it alone before calling a run red.

## Decisions (decided by the planner; revisit)

The person was unavailable and asked not to be blocked. Each decision below was **decided by the planner, 2026-11-04;
revisit.**

| # | Decision |
|---|---|
| D1 | **Branch.** Plan 2 is built on `plan-2-backlog`, branched from `workflow-simplification`, so that plan 1's PR can be reviewed and merged on its own. Once plan 1 merges, rebase plan 2 onto `main`.<br>**Overridden** by the main session's ruling (2026-11-04): every plan goes on the one branch `workflow-simplification`, so plan 2 was built and committed there, with no branch `plan-2-backlog`. |
| D2 | **The item file.** It is `.shop/backlog/b<n>.md`, in the format pinned in Task 1:<br>- the frontmatter holds `id: item/<context path>/b<n>`, `kind: item`, `status`, `provenance`, `value`, `urgency`, `size` and `depends_on: [b<m>, ...]`;<br>- the title is the one `# ` heading, as a work-item's is, so no title is ever quoted in YAML;<br>- the body has optional `## Notes`, `## Question`, `## Answers` and `## Refused` sections.<br>An unrated field is written empty and reads as None. |
| D3 | **No log file.** Each change to an item is one git commit of that one file, and git history is its log. Plan 7 (telemetry) may add a log if it needs one. |
| D4 | **Numbering.** A new item is `b<highest + 1>` over `.shop/backlog/b*.md`. Two branches that each add the same `b<n>` meet as a git conflict on that path. That collision is not prevented here. |
| D5 | **The commands.**<br>- `work idea TITLE [--provenance own\|peer\|product] [--note TEXT]`<br>- `work shape B [--note TEXT]`<br>- `work rate B [--value V] [--urgency U] [--size S]`<br>- `work depend B --on B2`<br>- `work refuse B REASON`<br>- `work withdraw B`, `work answer B TEXT`, `work show B [--json]`<br>- `work backlog [--json]`<br>There is no command that removes a dependency (YAGNI; edit the file). `work answer` on an item refuses `--change` and `--accept`. |
| D6 | **Ratings.** The flags take the glossary's values only (`low-value`…`high-value`, `low-urgency`…`high-urgency`, `small`/`medium`/`large`), as P7 ruled. Any other value is refused, naming the values allowed. |
| D7 | **Rank.** The score is (value + urgency) / size, with low = small = 1, medium = 2 and high = large = 3. Within a state, items go by score from high to low, and ties go to the lower `b<n>` (the item added first). An item missing any of the three ratings has no score and ranks after the rated items of its state. |
| D8 | **The view.** `work backlog` prints every item (r6 says every item): one Markdown table per state, in the order `in-batch`, `needs-input`, `ready`, `shaped`, `idea`, `delivered`, `refused`, `withdrawn`. A state with no items is left out. |
| D9 | **Blocked.** An item is blocked when it depends on an item that is not `delivered`. The glossary's "not in the same batch" exception waits for plan 4, because no batch exists yet. A dependency on a missing, `refused` or `withdrawn` item still blocks, and it is printed with that status (`missing` for no file) so the person sees why. |
| D10 | **Risk and likelihood** (ruling P4) are not built. The design gives them no part in the rank, so they stay in `## Not yet`. |
| D11 | **How far a batch is along** waits for plan 4, which makes batches. `## Not yet` names plan 4. |
| D12 | **Rank order and tables by state** can't be said in the grammar, which has no order or grouping. So they are described under backlog's `## Implementation, may change` and pinned by script tests, not by new requirement lines. The grammar is not extended. |
| D13 | **`spec_steps` is not changed.** Once their handlers bind them, all 17 backlog scenarios test their point (checked line by line in the tasks). The generator's gaps from plan 1's rulings are left to the plan whose lines need them first (plan 4: batches r8). |
| D14 | **Instance names.** A scenario's item `i<n>` is the file `b<n>` (`backlog_world.ident`). Generator naming is unchanged (ruling M7). |
| D15 | **A scenario item no Given sets up** (ruling, "Known gaps"). Before the command runs, it is written as `idea`, `own`, rated `medium-value`, `medium-urgency`, `medium`, with the title `Title of i<n>`. The one exception is under `work idea`, where the item a Then names is the one the command wrote. |
| D16 | **A malformed item file** is refused, naming the file and the field, by every command that reads the backlog. It is never skipped and never a traceback. Malformed means an unknown status, provenance or rating, no `# ` heading, or a `depends_on` that is not a list of `b<n>`. |
| D17 | **`work answer` on an item** moves the `## Question` text and the answer under `## Answers`, as `- Q: …` / `  A: …`, and removes `## Question`. |
| D18 | **`work refuse` and `work answer` take their text as an argument.** Empty text, or text with a newline, is refused. |

## Review Focus

These are the input classes the spec implies but no generated scenario exercises, most likely to bite first. Each has
its test in the task named.

1. **One command, two kinds of thing.**
   - `work withdraw w3`, `work show i2` and `work answer w3 x --change` must behave exactly as before.
   - `work answer b1 x --change` must be refused.

   Pinned in Task 2: `test_work_withdraw_on_a_work_item_is_unchanged` and
   `test_an_item_answer_refuses_the_reviewer_flags`.
2. **A dependency cycle or self-dependency** (`work depend b1 --on b1`, or `b1 → b2` then `b2 → b1`).
   - Expected: refused, naming the cycle as labels, with nothing committed.
   - A cycle written by hand must not hang `work backlog`.

   Pinned in Task 3 (`test_depend_refuses_a_cycle`, `test_depend_refuses_itself`) and Task 4
   (`test_backlog_prints_a_hand_written_cycle`).
3. **A dependency on an item that is missing, withdrawn or refused.**
   - Expected: `work backlog` prints the blocker with its status, or `missing`, and exits 0.

   Pinned in Task 4: `test_a_dependency_on_a_missing_or_withdrawn_item_blocks_with_its_status`.
4. **Titles that break the output.**
   - An empty title or one with a newline is refused by `work idea`.
   - A `|` in a title is escaped as `\|`, so the table keeps its columns.

   Pinned in Task 1 (`test_idea_refuses_an_empty_or_multi_line_title`) and Task 4
   (`test_a_pipe_in_a_title_keeps_the_columns`).
5. **A hand-edited item file** with an unknown status or rating, or no heading.
   - Expected: `work backlog`, `work show` and every move exit 1 with `work: <file>: <field> ...`, and change nothing.

   Pinned in Task 1: `test_a_malformed_item_is_refused_naming_the_file_and_field`.

---

### Task 1: Item files, `work idea` and `work show` on an item

Builds `backlog#r1` and `backlog#r15`.

**Files:**
- Create: `scripts/backlog_items.py`, `scripts/backlog_moves.py` (with `idea` only), `scripts/backlog_cli.py`
- Modify: `scripts/work`
  - import `backlog_cli`;
  - `backlog_cli.add_parsers(sub)` after the existing parsers;
  - merge `backlog_cli.COMMANDS` into the dispatch dict;
  - `cmd_show` sends a target that `is_item` to `backlog_cli.show`;
  - a docstring sentence on the backlog.
- Create: `tests/scenarios/backlog_world.py`, `tests/scenarios/backlog_handlers.py`
- Modify:
  - `tests/scenarios/test_backlog.py`: `bind_all(globals(), ROOT)` before `scenarios(...)`, as `test_work_queue.py`
    does; the docstring names its handlers.
  - `tests/scripts/conftest.py`: the fixture `backlog_repo`.
  - `spec/capabilities/backlog.md`: `unbuilt:` loses `r1` and `r15`.
  - `CLAUDE.md`: rows for `backlog_items.py`, `backlog_moves.py`, `backlog_cli.py`, `backlog_world.py`, and `backlog` added to the
    `<capability>_handlers*.py` row.
- Test: `tests/scripts/test_backlog_items.py`

**Interfaces:**
- Produces, in `backlog_items.py`:
  - `BACKLOG = Path(".shop") / "backlog"`
  - `STATUSES = ("idea", "shaped", "ready", "in-batch", "delivered", "needs-input", "refused", "withdrawn")`
  - `PROVENANCES = ("own", "peer", "product")`
  - `RATINGS = {"value": ("low-value", "medium-value", "high-value"), "urgency": ("low-urgency", "medium-urgency",
    "high-urgency"), "size": ("small", "medium", "large")}`
  - `@dataclass class Item`, with these fields:
    - `name: str` (`b3`), `ident: str` (`item/<ctx>/b3`), `title: str`, `status: str`, `provenance: str`;
    - `value: str | None`, `urgency: str | None`, `size: str | None`;
    - `depends_on: tuple[str, ...]`;
    - `sections: dict[str, str]` (heading → text, in file order);
    - the property `question -> str | None` (`sections.get("Question")`).
  - `is_item(name: str) -> bool`: `re.fullmatch(r"b[1-9]\d*", name)`.
  - `parse(text: str, rel: str) -> Item`: raises `Refused("<rel>: <field> ...")` per D16.
  - `render(item: Item) -> str`: byte-stable, so `parse(render(i))` round-trips.
  - `items(root) -> list[Item]`: by number.
  - `find(root, name) -> Item`: `Refused("there is no item <name> in .shop/backlog/")`.
  - `next_name(root) -> str`
  - `label(item) -> str`: `'b3 "Fix the parser"'`.
  - `commit(root, item, message) -> None`: writes `render(item)` and commits that one path through
    `workqueue.committed`.
- Produces, in `backlog_moves.py`: `idea(root, title, provenance="own", note=None) -> Item`. Task 2 adds the
  other moves.
- Produces, in `backlog_cli.py`:
  - `add_parsers(sub) -> None` (here `idea`; later tasks add theirs);
  - `COMMANDS: dict[str, Callable[[Namespace], int]]`;
  - `show(args) -> int` (prints, `--json` gives `{"item": {...}}` with the keys of Task 4's JSON row).
- Produces, in `backlog_world.py` (loaded by path under the `sys.modules` name `shop_backlog_world`):
  - `ident(name) -> str` (`i3` → `b3`)
  - `write_item(step, name, **fields) -> Path` (fields override D15's defaults; it records `context["items"][name] =
    rel`)
  - `item_rel(context, name) -> str | None`
  - `ensure_items(step) -> None` (D15, over `work_queue_world.scenario_texts`)
  - `run_work(step, *args)` (calls `ensure_items` unless `args[0] == "idea"`, then `work_queue_world.init`, keeps
    `context["head"]` and `context["result"]`)
  - `row(stdout, name) -> str | None` (the table line whose item cell is `name`'s id)
- Consumes:
  - `workqueue.Refused`, `committed`, `frontmatter`, `context_path` and `read`;
  - `work_queue_world.init`, `field`, `scenario_texts` and `local`. The world is loaded under `shop_work_queue_world`
    exactly as `work_queue_handlers.shared()` loads it: reuse the module when it is already in `sys.modules`, because
    the handler glob loads `backlog_handlers.py` first.

**The item file** (`render` writes exactly this shape; an unrated field is `value:` with nothing after it):

```
---
id: item/ex.com/prod/ctx/b3
kind: item
status: shaped
provenance: own
value: high-value
urgency: low-urgency
size: small
depends_on: [b1]
---

# Fix the parser

## Notes

the note text
```

- [x] **Step 1: Write the failing script tests** in `tests/scripts/test_backlog_items.py`, using `backlog_repo` (a git
  repository with an identity, `spec/index.md` holding `id: bounded-context/ex.com/prod/ctx`, all committed):
  - `test_idea_writes_b1_and_commits_only_it`: `work idea "Fix the parser"` exits 0 and prints `b1 "Fix the parser"`.
    `.shop/backlog/b1.md` parses to `status == "idea"`, `provenance == "own"`, `value is None` and
    `depends_on == ()`. `git show --name-only HEAD` lists only `.shop/backlog/b1.md`.
  - `test_idea_numbers_one_above_the_highest`: with `b1` and `b7` present, the next `work idea` writes `b8`.
  - `test_idea_refuses_an_empty_or_multi_line_title`: `""` and `"a\nb"` each exit 1 with `work: ` on stderr. HEAD and
    `git status --porcelain` are unchanged.
  - `test_render_round_trips`: `parse(render(item), rel) == item` for an item with every field, a `## Question` and a
    `## Notes`.
  - `test_a_malformed_item_is_refused_naming_the_file_and_field`: a file with `status: doing`, then one with
    `value: huge`, then one with no heading. `work show b1` exits 1, and stderr holds `.shop/backlog/b1.md` and,
    respectively, `status`, `value` or `title`.
  - `test_show_names_the_item_by_its_title`: `work show b1` prints `b1 "Fix the parser"` on its first line.
    `work show b1 --json` prints one object whose `item.title == "Fix the parser"`.
  - `test_show_of_a_work_item_is_unchanged`: in a repository with `.shop/work/i1/w1.md`, `work show w1` gives the
    same stdout as before this task. Compare against `workqueue_list.show` called directly.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_backlog_items.py -q`
  Expected: FAIL; `work` has no `idea` command and `backlog_items` does not exist.

- [x] **Step 3: Implement `backlog_items.py`, `backlog_moves.idea` and `backlog_cli.py`, and wire `scripts/work`.**
  - `work idea` commits with the message `work idea: b<n> "<title>" idea`.
  - A note given with `--note` goes under `## Notes`.

- [x] **Step 4: Run the script tests.**
  Run: `python3 -m pytest tests/scripts/test_backlog_items.py tests/scripts/test_work_show_request.py tests/scripts/test_workqueue_list.py -q`
  Expected: all pass.

- [x] **Step 5: Write the scenario world and the handlers for r1 and r15.** In `backlog_handlers.py`:
  - **Registry handlers** (keys no capability claims):
    - `("WhenRuns", "`work idea`")`: runs `work idea "A new idea"`.
    - `("GivenK", "item")` and `("GivenK_A", "item")` call `write_item`. For "the item i1 is not `v`", the item keeps
      its status when it is already another one; otherwise it takes the first status of `STATUSES` that is not `v`.
    - `("ThenK_A", "item")` reads the frontmatter field `step.attribute` (status, value, urgency or size) of the item's
      file and compares it with the bare value, negated for " is not ".
  - **`local` handlers** (keys another capability claims; each returns `False` for a step that is not about an item,
    so the step goes on to the registry):
    - `("WhenRuns", "item")` with the command `` `work show` `` runs `work show b<n>`. Withdraw and answer come in
      Task 2.
    - `("ThenDoes", "item")`:
      - `write`: the last run changed a `.shop/backlog/b<n>.md`. An unbound name is bound to that file.
      - `commit`: HEAD moved from `context["head"]`, and the new commits hold the item's file.
    - `("ThenPrints", "title")` asserts that the stdout holds the title of an item of the scenario, and binds the
      title's name to that item.
    - `("ThenR", "title")` asserts that the bound title is the `# ` heading of the named item's file and appears in the
      stdout.

  Check each scenario against its point:
  - r1 asserts a new `idea` file, committed.
  - r15 asserts the title of `b1`, which is `Title of i1`, printed by `work show`.

- [x] **Step 6: Mark r1 and r15 built.** Remove `r1` and `r15` from `unbuilt:` in `spec/capabilities/backlog.md`.
  Run: `python3 -m pytest tests/scenarios/test_backlog.py -q | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: `2 passed, 15 xfailed`; `every step has one handler`.

- [x] **Step 7: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/features generate --check; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/backlog_items.py scripts/backlog_moves.py scripts/backlog_cli.py scripts/work tests/scenarios/backlog_world.py tests/scenarios/backlog_handlers.py`
  Expected:
  - the suite: `52 xfailed`, no failures, passed = 951 + 2 + the new script tests;
  - `model check` and `generate --check` at their baselines;
  - `size` silent;
  - `check` reports nothing for ruff, vulture or import-linter.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/backlog_items.py scripts/backlog_moves.py scripts/backlog_cli.py scripts/work tests/scenarios/backlog_world.py \
    tests/scenarios/backlog_handlers.py tests/scenarios/test_backlog.py tests/scripts/conftest.py \
    tests/scripts/test_backlog_items.py spec/capabilities/backlog.md CLAUDE.md
  git commit -m "backlog: item files, work idea and work show on an item (backlog r1, r15)"
  ```

### Task 2: The moves of an item's status

Builds `backlog#r2`, `r3`, `r9`-`r14` and `r16`.

**Files:**
- Modify:
  - `scripts/backlog_moves.py`: the moves beside Task 1's `idea`.
  - `scripts/backlog_cli.py`: parsers `shape` and `refuse`; `withdraw(args)` and `answer(args)`.
  - `scripts/work`: `cmd_withdraw` and `cmd_answer` send an `is_item` name to `backlog_cli`.
  - `tests/scenarios/backlog_handlers.py`, `tests/scenarios/backlog_world.py`.
  - `spec/capabilities/backlog.md`: `unbuilt:` loses `r2, r3, r9, r10, r11, r12, r13, r14, r16`.
- Test: `tests/scripts/test_backlog_moves.py`

**Interfaces:**
- Consumes: Task 1's `find`, `commit`, `label` and `idea`.
- Produces, in `backlog_moves.py`:
  - `TRANSITIONS = {"work shape": {"idea": "shaped"}, "work refuse": {"idea": "refused", "shaped": "refused"},
    "work withdraw": {"idea": "withdrawn", "shaped": "withdrawn", "ready": "withdrawn", "needs-input": "withdrawn"},
    "work answer": {"needs-input": "shaped"}}`
  - `shape(root, name, note=None) -> Item`
  - `refuse(root, name, reason) -> Item`
  - `withdraw(root, name) -> Item`
  - `answer(root, name, text) -> Item`

  Each move is one commit, with the message `<command>: <label> <before> -> <after>`. A move from a status that its
  command's row lacks is refused with `<command>: <label> is <status>; <command> takes an item that is <a or b>`. The
  message names the status (r3).

- [x] **Step 1: Write the failing tests** in `tests/scripts/test_backlog_moves.py`:
  - `test_each_move_follows_its_row`: parametrised over every (command, before, after) in `TRANSITIONS`. From an item
    written `before`, the command exits 0, the file reads `after`, and HEAD's commit holds only that file.
  - `test_a_move_from_another_status_is_refused_naming_it`: parametrised over every command and every status not in
    its row. The command exits 1, stderr holds the item's status and its label, and HEAD and the tree are unchanged.
  - `test_the_moves_are_the_glossary_transitions`: from `spec_lexicon.read(REPO)`, take the term `status` of kinds
    `("item",)`. The set of its transitions whose `by` is one of `TRANSITIONS`' commands in backticks equals the set
    `TRANSITIONS` gives.
  - `test_answer_moves_the_question_under_answers`: a `needs-input` item with `## Question\n\nWhich?` gets
    `work answer b1 "The first"`. The file has no `## Question`, `## Answers` holds `Which?` and `The first`, and the
    status is `shaped`.
  - `test_refuse_writes_the_reason`: `work refuse b1 "out of scope"` leaves `## Refused` holding `out of scope`.
  - `test_an_item_answer_refuses_the_reviewer_flags`: `work answer b1 x --change` exits 1 and changes nothing.
  - `test_work_withdraw_on_a_work_item_is_unchanged`: `tests/scripts/test_work_withdraw.py`'s scenario, run through
    `scripts/work withdraw w1`, is still refused with `withdrawn` on stderr.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_backlog_moves.py -q`
  Expected: FAIL; `work shape` is not a command.

- [x] **Step 3: Implement `backlog_moves.py`, the parsers and the routing.** `work answer`'s parser keeps its
  `--change` and `--accept` flags. `backlog_cli.answer` refuses them for an item.

- [x] **Step 4: Run the tests and the old `work` tests.**
  Run: `python3 -m pytest tests/scripts/test_backlog_moves.py tests/scripts/test_backlog_items.py tests/scripts/test_work_withdraw.py tests/scenarios/test_work_queue.py tests/scenarios/test_requests.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The handlers.**
  - **Registry:** `("WhenRuns", "`work shape`")` and `("WhenRuns", "`work refuse`")`. The refuse handler supplies the
    reason `out of scope`.
  - **`local`:**
    - `("WhenRuns", "item")` gains `` `work withdraw` `` and `` `work answer` ``. The answer handler supplies
      `the first reading`.
    - `("ThenExitsErr", "item")`: the run exited non-zero, and stderr holds the label of each item named. For a noun
      phrase `the status of the item i<n>`, it also holds that item's status as it was before the run.
  - **World:** `write_item` gives a `needs-input` item the section `## Question` with the text
    `Which reading holds, the first or the second?`.

  Check each scenario against its point:
  - r3 needs the item to be given a status other than `idea` before the run;
  - r16 asserts `shaped` and a commit of `b1`.

- [x] **Step 6: Mark them built.** Remove `r2, r3, r9, r10, r11, r12, r13, r14, r16` from `unbuilt:`.
  Run: `python3 -m pytest tests/scenarios/test_backlog.py -q | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: `11 passed, 6 xfailed`; `every step has one handler`.

- [x] **Step 7: The baselines,** as in Task 1, Step 7, over the files of this task.
  Expected: the suite at `43 xfailed`, no failures; every other baseline unchanged.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/backlog_moves.py scripts/backlog_cli.py scripts/work tests/scenarios/backlog_handlers.py \
    tests/scenarios/backlog_world.py tests/scripts/test_backlog_moves.py spec/capabilities/backlog.md
  git commit -m "backlog: work shape, refuse, withdraw and answer move an item (backlog r2, r3, r9-r14, r16)"
  ```

### Task 3: Ratings and dependencies

Builds `backlog#r4` and `r5`.

**Files:**
- Modify:
  - `scripts/backlog_moves.py`: `rate` and `depend`.
  - `scripts/backlog_cli.py`: the parsers `rate` and `depend`.
  - `tests/scenarios/backlog_handlers.py`, `tests/scenarios/backlog_world.py`.
  - `spec/capabilities/backlog.md`: `unbuilt:` loses `r4, r5`.
- Test: `tests/scripts/test_backlog_ratings.py`

**Interfaces:**
- Produces:
  - `rate(root, name, value=None, urgency=None, size=None) -> Item`: at least one rating is required. A value outside
    `RATINGS` is refused, naming the allowed values. An item that is `delivered`, `refused` or `withdrawn` is refused.
    The commit message is `work rate: <label> value=… urgency=… size=…`.
  - `depend(root, name, on) -> Item`: refuses an unknown `on`, a duplicate, `on == name`, and a new edge that closes a
    cycle. The cycle refusal names the path as labels joined by ` -> `. The commit message is
    `work depend: <label> on <label of on>`.
  - `cycle(root, name, on) -> list[str] | None`: the path from `on` back to `name` over `depends_on`, if there is
    one. Task 4 uses its traversal guard.

- [x] **Step 1: Write the failing tests** in `tests/scripts/test_backlog_ratings.py`:
  - `test_rate_sets_each_given_rating`: `work rate b1 --value high-value --size small` gives `value == "high-value"`,
    `size == "small"` and `urgency is None`, in one commit.
  - `test_rate_refuses_a_value_of_another_attribute`: `--value high` and `--size high-value` each exit 1. Stderr names
    `low-value, medium-value, high-value` (respectively `small, medium, large`), and nothing changes.
  - `test_rate_refuses_no_rating`: `work rate b1` exits 1.
  - `test_depend_writes_the_dependency_in_the_needing_item`: `work depend b2 --on b1` gives b2 `depends_on == ("b1",)`
    and leaves b1's file byte-identical.
  - `test_depend_refuses_itself`: `work depend b1 --on b1` exits 1 and changes nothing.
  - `test_depend_refuses_a_cycle`: after `b1 --on b2` and `b2 --on b3`, the command `work depend b3 --on b1` exits 1.
    Stderr holds `b3`, `b1` and `b2` in path order, and HEAD is unchanged.
  - `test_depend_refuses_an_unknown_item_and_a_duplicate`.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_backlog_ratings.py -q`
  Expected: FAIL; `work rate` is not a command.

- [x] **Step 3: Implement `rate`, `depend`, `cycle` and their parsers.**

- [x] **Step 4: Run the tests.**
  Run: `python3 -m pytest tests/scripts/test_backlog_ratings.py tests/scripts/test_backlog_moves.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The handlers.**
  - **Registry:**
    - `("WhenRuns", "`work rate`")` runs `work rate b<n>` with each `context["flags"]` entry split by `shlex`. The
      registry's `GivenFeat` keeps a flag string as one entry.
    - `("WhenRuns", "`work depend`")` writes the world's own item `b90` (title `an item the scenario does not name`),
      then runs `work depend b<n> --on b90`.
  - **`local`:**
    - `("ThenDoes", "dependency")` with `write`: the last run changed the file of an item whose `depends_on` gained an
      entry. It binds the dependency's name to (that item, the entry).
    - `("ThenR", "dependency")` with `of`: the bound dependency's needing item is the named item.
  - `ThenK_A` from Task 1 already reads `value`, `urgency` and `size`.

  Check each scenario against its point:
  - r4 asserts all three ratings and a commit;
  - r5 asserts a new dependency in `b1`'s file, and a commit of `b1`.

- [x] **Step 6: Mark them built.** Remove `r4, r5` from `unbuilt:`.
  Run: `python3 -m pytest tests/scenarios/test_backlog.py -q | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: `13 passed, 4 xfailed`; `every step has one handler`.

- [x] **Step 7: The baselines,** as in Task 1, Step 7.
  Expected: the suite at `41 xfailed`, no failures; everything else unchanged.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/backlog_moves.py scripts/backlog_cli.py tests/scenarios/backlog_handlers.py \
    tests/scenarios/backlog_world.py tests/scripts/test_backlog_ratings.py spec/capabilities/backlog.md
  git commit -m "backlog: work rate and work depend (backlog r4, r5)"
  ```

### Task 4: `work backlog`: rank, tables, blockers and questions

Builds `backlog#r6`, `r7`, `r8` and `r17`.

**Files:**
- Create: `scripts/backlog_view.py`
- Modify:
  - `scripts/backlog_cli.py`: the parser `backlog`. `show` reuses `backlog_view.row_json` for its JSON.
  - `tests/scenarios/backlog_handlers.py`, `tests/scenarios/backlog_world.py`.
  - `spec/capabilities/backlog.md`: `unbuilt: []`, a new `## Implementation, may change` and a rewritten
    `## Not yet` (Step 6).
  - `CLAUDE.md`: a row for `backlog_view.py`.
- Test: `tests/scripts/test_backlog_view.py`

**Interfaces:**
- Consumes: Task 1's `items` and `label`; Task 3's cycle-guarded traversal, so that a hand-written cycle never
  recurses.
- Produces, in `backlog_view.py`:
  - `WEIGHT = {"low-value": 1, "medium-value": 2, "high-value": 3, "low-urgency": 1, "medium-urgency": 2,
    "high-urgency": 3, "small": 1, "medium": 2, "large": 3}`
  - `STATE_ORDER = ("in-batch", "needs-input", "ready", "shaped", "idea", "delivered", "refused", "withdrawn")`
  - `score(item) -> float | None`
  - `blockers(item, by_name: dict[str, Item]) -> list[tuple[str, str]]`: (the name of each dependency's target, its
    status, or `missing`) for each target that is not `delivered`.
  - `ordered(items) -> list[tuple[str, list[Item]]]`: D7 and D8.
  - `row_json(item, by_name, rank) -> dict` with the keys `id`, `title`, `status`, `provenance`, `value`, `urgency`,
    `size`, `score`, `rank`, `depends_on`, `blocked_by`, `question`.
  - `tables(root) -> str`
  - `as_json(root) -> dict` (`{"items": [row_json, ...]}`, in table order).

**The table** (pinned; `tables` writes exactly this shape):

```
## needs-input (1)

| rank | item | title | provenance | value | urgency | size | score | waiting on |
|---|---|---|---|---|---|---|---|---|
| 1 | b4 | Fix the parser | own | high-value | medium-urgency | small | 5.00 | question: Which reading holds, the first or the second? |
```

- `score` is printed with two decimals, or `-` when there is none, and so is an unrated cell.
- `waiting on` holds:
  - `blocked by <label> (<status>)` for each blocker, joined by `; `;
  - then `question: <first line of the question>` for a `needs-input` item.
- A `|` in any cell is written `\|`.
- An empty backlog prints `the backlog is empty`; with `--json` it prints `{"items": []}`.

- [ ] **Step 1: Write the failing tests** in `tests/scripts/test_backlog_view.py`:
  - `test_score_is_value_plus_urgency_over_size`: `high-value, medium-urgency, small` gives `5.0`; `low-value,
    low-urgency, large` gives `2/3`; an item with no size gives `None`.
  - `test_rank_breaks_ties_by_the_item_added_first`: `b2` and `b5` with equal scores, and an unrated `b1`, all
    `shaped`, give the order `b2, b5, b1`.
  - `test_tables_come_in_state_order_and_skip_empty_states`: items `idea`, `ready` and `in-batch` give headings in
    the order `in-batch`, `ready`, `idea`, and no `## shaped`.
  - `test_a_blocked_item_names_its_blocker_in_its_row`: b2 depends on b1 (`idea`). b2's row holds
    `blocked by b1 "…" (idea)`, and b1's row has no `blocked by`. Once b1 is `delivered`, b2's row has no
    `blocked by`.
  - `test_a_dependency_on_a_missing_or_withdrawn_item_blocks_with_its_status`: `depends_on: [b9]` with no b9 gives
    `(missing)`; a withdrawn b3 gives `(withdrawn)`; the exit is 0.
  - `test_backlog_prints_a_hand_written_cycle`: b1 and b2 depend on each other. `work backlog` exits 0 within the
    test's default timeout, and each row names the other.
  - `test_a_pipe_in_a_title_keeps_the_columns`: the title `a | b` gives a row with exactly 10 unescaped `|`.
  - `test_needs_input_prints_the_first_line_of_its_question`.
  - `test_json_is_one_object_in_table_order`: `work backlog --json` parses to a dict whose `items` ids follow the
    table order, with `score` null for an unrated item.
  - `test_an_empty_backlog`: both forms, exit 0.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_backlog_view.py -q`
  Expected: FAIL; `work backlog` is not a command.

- [ ] **Step 3: Implement `backlog_view.py` and the `backlog` parser.** `work backlog` only reads, and it commits
  nothing.

- [ ] **Step 4: Run the tests.**
  Run: `python3 -m pytest tests/scripts/test_backlog_view.py tests/scripts/test_backlog_items.py -q | tail -1`
  Expected: all pass.

- [ ] **Step 5: The handlers.**
  - **Registry:**
    - `("WhenRuns", "`work backlog`")` runs `work backlog` with the scenario's flags.
    - `("GivenK", "dependency")` records the name in `context["deps"]`.
    - `("GivenR", "of")` is a dispatcher by `step.kind`: a dict `OF_GIVENS = {"dependency": ...}`, which later plans
      extend (task of batch, request line of item). It fails naming the kind when it has no entry.
    - `("GivenK_C", "item")` with `blocked` records the item as blocked. `ensure_items` then makes sure, before the
      run, that each blocked item depends on an item that is not `delivered`, writing one of the world's own if none
      does. With `not blocked`, the item has no such dependency.
  - **`local`:**
    - `("GivenR", "dependency")` with `on` records the target. A dependency is written into its needing item's
      `depends_on` once both halves are given, and `ensure_items` completes a half-given one with an item of the
      world's own.
    - `("ThenPrints", "item")`:
      - `the item i<n>`: `row(stdout, i<n>)` exists.
      - `the <attribute> of the item i<n>`: for `status`, the row lies under the heading `## <status>`; for any other
        attribute, the item file's value is a cell of the row.
    - `("ThenPrints", "dependency")`: the needing item's row holds `blocked by` and the target's id.
    - `("ThenPrints", "question")`: the first line of a `needs-input` item's `## Question` is in the stdout, and the
      name is bound to that item.
    - `("ThenR", "question")` with `on`: the bound question is the named item's, and it is in that item's row.

  Check each scenario against its point:
  - r6: every column of `b1`'s row;
  - r7: the blocker is in `b2`'s row, not just anywhere;
  - r8: the U8 check;
  - r17: the question is in `b1`'s row.

- [ ] **Step 6: The spec's prose, and every id built.** In `spec/capabilities/backlog.md`:
  - set `unbuilt: []`;
  - add `## Implementation, may change` before `## Not yet`, with one bullet each for:
    - D7's score and tie rule;
    - D8's state order and that every item is printed;
    - the `waiting on` column;
    - D9's blocked rule, with the same-batch exception left to plan 4;
  - replace `## Not yet` with two bullets: how far a batch is along (plan 4, `batches`); and bugs' risk and likelihood
    (D10: not built, because the design gives them no part in the rank).

  Run: `python3 -m pytest tests/scenarios/test_backlog.py -q | tail -1; python3 scripts/features vocab --check | tail -1; python3 scripts/features generate --check; python3 scripts/model check | tail -1`
  Expected: `17 passed`; `every step has one handler`; `generate --check` exit 0; `model check` at its baseline.

- [ ] **Step 7: The baselines,** as in Task 1, Step 7, plus `python3 scripts/model logic | tail -1`.
  Expected: the suite at `37 xfailed`, no failures; `11 findings: 6 L5, 5 L6`; everything else unchanged.

- [ ] **Step 8: Commit.**
  ```bash
  git add scripts/backlog_view.py scripts/backlog_cli.py tests/scenarios/backlog_handlers.py \
    tests/scenarios/backlog_world.py tests/scripts/test_backlog_view.py spec/capabilities/backlog.md CLAUDE.md
  git commit -m "backlog: work backlog prints the backlog by state in rank order (backlog r6-r8, r17); backlog built"
  ```

### Task 5: Whole-plan verification and records

**Files:**
- Create: `.shop/records/2026-11-04-workflow-simplification/plan-2-implementation.md` (the implementation report)
- Modify: `.shop/records/README.md` (a row for the report); this plan (every box ticked)

- [ ] **Step 1: Every backlog requirement is built.**
  Run: `python3 -c "import sys; sys.path.insert(0,'scripts'); import pathlib, spec_unbuilt as u; d=u.unbuilt(pathlib.Path('.')); print('backlog' in d, sum(map(len,d.values())), u.problems(pathlib.Path('.')))"`
  Expected: `False 37 []`.
- [ ] **Step 2: The baselines, all at once.**
  Run: `python3 -m pytest -q | tail -2; python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check | tail -1; python3 scripts/features generate --check; python3 scripts/features vocab --check | tail -1; python3 scripts/features bindings --unbound; python3 scripts/tools size --limit 300; python3 scripts/tools check $(git diff --name-only workflow-simplification...HEAD -- '*.py' scripts/work)`
  Expected:
  - the suite: `37 xfailed`, no failures, and passed = 951 + 17 + the new script tests;
  - `model check`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`;
  - `model logic`: `11 findings: 6 L5, 5 L6`;
  - the lexicon: no problems;
  - `generate --check`: exit 0;
  - `vocab --check`: `every step has one handler`;
  - `bindings --unbound`: `every binding names a scenario`;
  - `size`: silent;
  - `check`: nothing to report.
- [ ] **Step 3: A smoke run in a scratch repository.** It shows the person's view end to end:
  ```bash
  d=$(mktemp -d) && git -C "$d" init -q && git -C "$d" config user.name t && git -C "$d" config user.email t@example.com
  mkdir -p "$d/spec" && printf -- '---\nid: bounded-context/ex.com/prod/ctx\n---\n# ctx\n' > "$d/spec/index.md"
  git -C "$d" add -A && git -C "$d" commit -qm init
  W="python3 $PWD/scripts/work --root $d"
  $W idea "Parse the item lines" && $W idea "Rank | order" && $W rate b1 --value high-value --urgency medium-urgency --size small && $W depend b2 --on b1 && $W shape b1 && $W backlog
  ```
  Expected:
  - two tables, `shaped` then `idea`;
  - b1's score `5.00`;
  - b2's row reads `blocked by b1 "Parse the item lines" (shaped)` and keeps 10 unescaped `|`;
  - `git -C "$d" log --oneline | wc -l` is `6`.
- [ ] **Step 4: Write the implementation report** at
  `.shop/records/2026-11-04-workflow-simplification/plan-2-implementation.md`, with `plan-1-implementation.md`'s
  frontmatter form (`kind: report`) and sections:
  - Final state (each Step 2 figure as measured);
  - the commits, with a table of each task's commit, what was done and its verification;
  - deviations from the plan, each with its reason;
  - D1-D18, each kept or changed;
  - open problems for plan 3 and later;
  - files.
- [ ] **Step 5: Index the records.** Add a row to `.shop/records/README.md` after the row for `plan-1-rulings.md`:
  `| \`2026-11-04-workflow-simplification/plan-2-implementation.md\` | plan 2 executed: the backlog built (item files, the item commands of \`work\`, \`work backlog\` by state in rank order), its 17 requirements out of \`unbuilt:\` | report |`.
  Tick every box of this plan.
- [ ] **Step 6: Commit.**
  ```bash
  git add .shop/records/2026-11-04-workflow-simplification/plan-2-implementation.md .shop/records/README.md \
    .shop/records/2026-11-04-workflow-simplification/plan-2-backlog.md
  git commit -m "records: plan 2 verified, its implementation report"
  ```
  The end-of-branch review follows, by a separate reviewer, into `plan-2-review.md`, reading
  `workflow-simplification..plan-2-backlog` against this plan's Review Focus.
