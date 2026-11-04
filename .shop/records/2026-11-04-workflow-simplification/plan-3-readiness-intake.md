---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-3
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# Plan 3: Readiness and Intake — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `readiness` and `intake` capabilities, so that all 4 of readiness's and all 6 of intake's
requirements are built, and meet `brainstorming` r1 and r2 with a skill. That means requirement lines kept on an item,
`work line` to write them, `work ready` checking the mechanical bar, `work intake` taking a peer's request in as an
item, and `work outcome` answering a line of it (accept into a capability, refuse with a reason, counter-propose).
Each requirement's id leaves `unbuilt:` in the same commit that makes its scenario (or, for brainstorming, its check)
pass.

**Architecture:**
- Three new modules behind `scripts/work`:
  - `backlog_lines.py` reads and writes an item's `## Requirements` block, gives new lines their ids, and lays the
    block over a copy of `spec/`.
  - `readiness_bar.py` is the bar: an item's request lines settled, and its lines well-formed (they parse, `model
    logic` finds no L0 or L1 naming them, `features generate` writes their scenarios), checked on a temporary copy of
    `spec/` with the item's lines laid in. `spec/` itself is never written.
  - `intake_moves.py` holds `work intake` and the item side of `work outcome`, over the request files
    `workqueue_request.py` keeps.
- `backlog_moves.ready` is the move `shaped` → `ready`, refused with every reason the bar gives.
- `backlog_cli.py` gains the parsers `line`, `ready` and `intake`. `scripts/work`'s `outcome` parser gains four
  options and routes to `intake_moves` when one is given or the request is taken in as an item; otherwise `work
  outcome` is exactly as before.
- The scenarios of `features/readiness.feature` and `features/intake.feature` get their own handlers
  (`readiness_handlers.py`, `intake_handlers.py`) over a world `readiness_world.py` that writes a codified spec, an
  item's lines and an item's request. Both test modules bind with `bind_all`, as `test_backlog.py` does (plan 2's open
  problem: readiness's item steps get their own `local` handlers).
- Two new skills: `skills/shaping-items/` (the brainstorming session's, for brainstorming r1 and r2) and
  `skills/taking-in-a-request/` (the intake session's).

**Tech Stack:** Python 3 (standard library), git, pytest, pytest-bdd and xdist; GF 3.12 with pgf and clingo for the
bar and the step vocabulary. All are installed; run `python3 scripts/tools probe` if unsure.

**Spec:** `spec/capabilities/readiness.md`, `spec/capabilities/intake.md` and `spec/capabilities/brainstorming.md`
(their lines are the acceptance tests), the glossary entries of `spec/index.md` they use (`item`, `request line`,
`line outcome`, `side`, `settled`, `well-formed`, `passing`, `item asked by bounded context`, `request line of item`,
`item proposes requirement`), and `.shop/records/2026-11-04-workflow-simplification/design.md` goals 3 and 4, with
"Who writes the lines" and "Where a ready item's lines live". Read them beside:
- `roadmap.md` (plan 3's row);
- `plan-1-rulings.md` (S3: settled request lines are part of `passing`; M3: readiness r4 and intake r5 are weak lines
  the handlers strengthen; the generator's dropped preconditions);
- `plan-2-implementation.md`, "Open problems for plan 3 and later", and `plan-2-rulings.md` (Q2: a negated Then
  requires only that the command exists).

## Global Constraints

- **Branch:** `workflow-simplification`, from `3d9e2a91` or later (the main session's ruling: every plan on this one
  branch). No new branch.
- **File size:** every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300`).
  - `scripts/work` is at 202 lines and may grow by at most 20.
  - `scripts/workqueue_request.py` is at 252 and is not changed (the new request writes live in `intake_moves.py`).
  - `tests/scenarios/backlog_handlers.py` is at 262 and may only shrink (Task 3 moves `OF_GIVENS` out of it).
- **Module map:** every new module gets a row in `CLAUDE.md`'s module map, in the task that creates it; the new
  handler modules join the `<capability>_handlers*.py` row, and `readiness_world.py` the `<capability>_world.py` row.
- **Strict xfail:** `spec_unbuilt.mark` uses `strict=True`.
  - A task removes an id from its capability's `unbuilt:` in the same commit that makes its scenario pass, and never
    before.
  - When a task's suite run shows an `XPASS(strict)` the task does not name, read that scenario. If it tests its point,
    remove its id in that commit and say so in the report. If it passes vacuously, fix the handler so it checks its
    point.
- **Spec lines:** this plan edits no requirement line, group or term. In `readiness.md` and `intake.md` it changes only
  the frontmatter's `unbuilt:` and the prose sections `## Implementation, may change` (new) and `## Not yet`; in
  `brainstorming.md` only `unbuilt:` and `## Not yet`. A line found wrong is reported, not changed.
- **No new scenario keys where one exists:** a handler for a (template, term) another capability already claims goes
  through `local(template, kind)`. `python3 scripts/features vocab --check` must keep printing
  `every step has one handler`, and `vocab.duplicates()` must stay empty.
- **Old behaviour kept:** `work outcome`, `ask`, `reply`, `turn`, `resolve` and `request` on a request that no item
  was taken in from, and given none of `--into`, `--group`, `--reason` or `--line`, behave byte for byte as before.
  `tests/scenarios/test_requests.py`, `test_work_queue.py`, `test_backlog.py` and the `tests/scripts/test_work_*.py`
  and `test_backlog_*.py` tests pass unchanged.
- **`spec/` is read, never written,** by `work line`, `work ready`, `work intake` and `work outcome`. The bar works on
  a copy under `tempfile.mkdtemp()`, removed afterwards whatever happens.
- **Refusals:** a refused command raises `workqueue.Refused`; `scripts/work` prints it as `work: <message>` on stderr
  and exits 1; the repository is left byte-identical, and the U3 check holds.
- **Names next to ids:** every line `work` prints about an item names it by `backlog_items.label(item)`; a request is
  named `q<n> "<its title>"`, and a request line as `line <n> of request q<m>` (design goal 10).
- **Baselines** (measured at `3d9e2a91`). Every task keeps them, and none may get worse:
  - `python3 -m pytest -q`: `1067 passed, 1 skipped, 37 xfailed, 129 subtests passed`. Each built scenario moves from
    xfailed to passed; at the end the count is `27 xfailed` and no failures.
  - Unbuilt ids (`spec_unbuilt.unbuilt`): 48, with no problems; at the end 36 (`brainstorming` keeps `r3`).
  - `python3 scripts/model check | tail -1`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`.
  - `python3 scripts/model logic | tail -1`: `11 findings: 6 L5, 5 L6`.
  - `python3 scripts/model lexicon --check | tail -1`: `401 terms, 0 problems`.
  - `python3 scripts/features generate --check`: exit 0. No feature file is regenerated by hand or edited.
  - `python3 scripts/features vocab --check | tail -1`: `every step has one handler`.
  - `python3 scripts/features bindings --unbound`: `every binding names a scenario`.
  - `python3 scripts/tools size --limit 300`: silent, exit 0.
  - The known flake `tests/scripts/test_revision_done.py::test_model_logic_on_the_live_spec_is_fast` may fail once
    under xdist. Rerun it alone before calling a run red.
- **Smoke steps** run `work` through a shell function, which bash and zsh both run (plan 2 review M10):
  `r=$PWD; W() { python3 "$r/scripts/work" --root "$d" "$@"; }`.

## Decisions (decided by the planner; revisit)

The person was unavailable and asked not to be blocked. Each decision below was **decided by the planner, 2026-11-04;
revisit.**

| # | Decision |
|---|---|
| D1 | **Branch.** Built and committed on `workflow-simplification`, as the main session ruled for every plan. |
| D2 | **Where an item's lines live.** In the item file's `## Requirements` section, one `### <capability>` block for each capability the lines go into, in the capability file's own syntax one heading level down: optional term bullets first (`- **frobnicate** (event): ...`), then `#### [g<n>] <title>` groups of `- [r<n>] <statement>` bullets, one line each. The design's "they stay on the item until its batch merges" is this section; plan 4 moves it into `spec/` at the merge. |
| D3 | **Ids.** A new group or requirement takes the next number free in its capability: one above the highest over the capability file's groups, requirements and `retired:` ids and the item's own block for it. Two items given the same id are not caught here; plan 4's pick lays every item of a batch over `spec/` together, where the duplicate is a file problem, and renumbers there. |
| D4 | **What lines may go into.** Only a capability that has a codified file in `spec/capabilities/`. A new capability, and a term for the glossary of `spec/index.md`, are not built (`## Not yet` of readiness); a term the lines need goes into the capability's own `## Terms` through the block's term bullets. |
| D5 | **`work line B --into CAP [--group TITLE \| --in g<n>] (TEXT \| --term BULLET)`.** It writes one requirement (or one term bullet) into the item's block and commits; it parses nothing, because `work ready` is the check. A new group is titled `--group`, else the item's title. It takes an item that is `idea` or `shaped`. |
| D6 | **The bar's logic check** refuses an L0, and an L1 whose ids name one of the item's requirements, as the glossary's `well-formed` says. An L1 elsewhere in `spec/` is not the item's. An L3 naming the item is printed on stderr as a warning and does not refuse, because the glossary leaves it out; adding it to the bar means retiring `well-formed` for a new one. |
| D7 | **An item with no requirement lines is not passing.** `well-formed` reads vacuously true for one, but a ready item with nothing to build defeats the bar; the reason says to give it a line with `work line`. |
| D8 | **`work ready` names every reason at once,** one per line after `work ready: <label> is not passing:`, in this order: its request lines not settled, then the well-formed reasons. A status other than `shaped` is refused first, by the move's own message (r3), with no check run. |
| D9 | **`features generate` in the bar** runs only on a `service` capability. Each of the item's groups must come out as a scenario unless it is logic-only (`spec_tree.logic_only`); a group with a fact no step words is a reason (`<cap>#g<n> has no scenario: <why>`). A `guarantees` capability has no scenarios, and is not generated. |
| D10 | **`work intake Q`** writes an item and changes nothing in the request. The item is `shaped`, titled by the request's `# ` heading, with the new frontmatter fields `request: q<n>` and `asked_by: <the request's asker>`, its provenance read off the asker (`internal` or this context's own id: `own`; an id starting `product/`: `product`; anything else: `peer`), and the note `taken in from request q<n> "<title>"`. It takes a request in the upstream's turn (`open` or `awaiting-upstream`), and refuses one another item was already taken in from, naming that item. |
| D11 | **The request lines of an item** are the lines of its request whose line outcome is not `rewritten`: a rewritten line is no longer the item's, its counter-proposal is. So `passing` (every request line of the item is settled) holds once each line is `accepted`, `refused` or `withdrawn`, and a rewritten line's counter-proposal is. |
| D12 | **`work outcome Q N WORD [--into CAP] [--group TITLE] [--reason TEXT] [--line TEXT]`.** With none of the four and no item taken in from Q, it is the old `work outcome`. Otherwise `intake_moves.outcome` writes it, keeping the old refusals (the asker's turn, the upstream's part):<br>- `accepted` on a taken-in request needs `--into`, and writes the line into the item's block (D2, D3);<br>- `refused` on a taken-in request needs `--reason`;<br>- `rewritten` with `--line` checks the counter-proposal in the context's grammar (`workqueue_lines.check`), appends it to the request's `## Lines` as the next number, and passes the turn to the asker as `work turn` would (status `awaiting-asker`, `turn: asker`);<br>- a reason (`--reason`, or `rewritten as line <m>`) goes under the request's new `## Reasons` section as `<n>. <text>`;<br>- on a taken-in request, the item gains a `## Notes` line (`line <n> of request q<m> <word>` and its detail), and the request and the item are one commit. |
| D13 | **`## Reasons`** joins the request sections `model check` accepts (`model_requests.SECTIONS`). |
| D14 | **The intake session** is not started by `work backlog` in this plan: the design's call ("a session started when the backlog command runs intake") needs `claude -p` plumbing that plan 4's batches build. `skills/taking-in-a-request/` is that session's instructions, run by any session now; intake's `## Not yet` names the start for plan 4. |
| D15 | **Brainstorming** is met by `skills/shaping-items/SKILL.md`, checked by `tests/scripts/test_skill_shaping_items.py`, which reads the skill as `test_agents.py` reads the agents (role-boundaries). r3 (`work quote`) stays in `unbuilt:` until plan 8 builds `work quote`; the skill says to cite the person's words in the item's notes until then. |
| D16 | **"Does not ask a question"** (readiness r4, intake r5; plan 1's M3 weak lines) is checked, not assumed: the handler runs `work` with stdin at `/dev/null` and a 120 s timeout; the Then needs the command to exist (exit code not 2), no file the run changed to gain a `## Question` or a `## Questions` entry or to move to `needs-input` or `awaiting-asker`, and no line of its stdout or stderr to end with `?`. |
| D17 | **The scenario world's codified spec** is `tests/scripts/fixtures/generate/repo/spec/` without `capabilities/legacy.md` (which is not codified, so `workqueue_lines.check` would refuse every line), its index's `id` rewritten to `bounded-context/ex.com/prod/ctx`. A passing line is the fixture's `ABANDON` statement as `work-queue#r5`; a line that is not passing is its `FROBNICATE` statement. |
| D18 | **`OF_GIVENS`** (`the x is of the y`, by the kind of x) moves from `backlog_handlers.py` to `backlog_world.py`, so `intake_handlers.py` adds `"request line"` to it; plan 4 adds `"task"`. |
| D19 | **A peer's request in the tests** is written by hand (`backlog_testing.write_request`, the smoke run's `printf`), because `work request`'s gate (requests r32) takes only this repository's own asker; how a peer writes its request into this repository is left as it is. |

## Review Focus

These are the input classes the spec implies but no generated scenario exercises, most likely to bite first. Each has
its test in the task named.

1. **The live spec must not move.** `work ready` on a passing and on a failing item leaves `spec/` byte-identical, the
   tree clean but for what the command commits, and no `readiness-*` directory in the temporary directory.
   Pinned in Task 2: `test_ready_never_writes_spec_and_cleans_up`.
2. **An L1 that is not the item's.** A finding elsewhere in `spec/` must not keep an item from `ready`; an L1 naming
   the item's line must; an L3 naming it is a warning only (D6).
   Pinned in Task 2: `test_only_the_items_l0_and_l1_refuse` (with `spec_solve.run` stubbed) and
   `test_an_l3_is_a_warning` (the fixture's `DONE` statement).
3. **Lines into something that is not a codified service capability:** a capability with no file, an uncodified one,
   and a `guarantees` one. Expected: the first two refused by `work line`, naming the capability; the third accepted,
   and readied without generating.
   Pinned in Task 1 (`test_line_refuses_a_capability_that_is_not_codified`) and Task 2
   (`test_a_guarantees_line_is_not_generated`).
4. **The old `work outcome`.** On a request no item was taken in from, with no new option, the commit (its files,
   message and the request's bytes) is what `workqueue_request.outcome` makes on a copy.
   Pinned in Task 4: `test_old_outcome_is_unchanged`.
5. **Taking a request in twice, or out of turn.** A second `work intake q1`, and one on an `awaiting-asker` or
   `delivered` request, are refused naming the item or the status, with nothing committed.
   Pinned in Task 3: `test_intake_refuses_a_request_taken_in` and `test_intake_refuses_a_request_out_of_turn`.

---

### Task 1: An item's requirement lines and `work line`

Builds no requirement on its own; Task 2's bar and Task 4's accepted outcome stand on it.

**Files:**
- Create: `scripts/backlog_lines.py`
- Modify:
  - `scripts/backlog_cli.py`: the parser `line` and `cmd_line`.
  - `CLAUDE.md`: a row for `backlog_lines.py`.
- Test: `tests/scripts/test_backlog_lines.py`; `tests/scripts/conftest.py` gains the fixture `ready_repo`.

**Interfaces:**
- Consumes: `backlog_items.find`, `commit`, `label`, `text_line` (from `backlog_moves`), `Refused`; `spec_read.capability`,
  `spec_read.codified`; `spec_lexicon.entry`.
- Produces, in `backlog_lines.py`:
  - `SECTION = "Requirements"`
  - `Group = namedtuple("Group", "id title requirements")`, `requirements` a list of `(r<n>, text)`
  - `Block = namedtuple("Block", "capability terms groups")`, `terms` a list of bullet strings
  - `read(item, rel) -> list[Block]`: the blocks of `item.sections.get(SECTION, "")`, in file order; malformed text is
    refused as `<rel>: Requirements: <what>` (a line that is neither a `### `, `#### [g<n>] ` heading, a `- [r<n>] `
    bullet nor a `- **` term bullet; a requirement or term before its heading; a group or requirement id twice).
  - `render(blocks) -> str`: byte-stable, `read` of it round-trips.
  - `ids(blocks) -> list[str]`: `["work-queue#r5", ...]`, in file order.
  - `capability_file(root, capability) -> Path`: refused as `there is no codified capability <cap> in spec/capabilities/`.
  - `next_ids(root, capability, blocks) -> tuple[str, str]`: D3's next `g<n>` and `r<n>`.
  - `add_line(root, name, capability, text, group=None, in_group=None) -> tuple[Item, str]` (D5; the second value is
    `<cap>#r<n>`); `add_line_to(root, item, ...)` the same on an item already loaded, without committing, for Task 4.
  - `add_term(root, name, capability, bullet) -> Item`: a bullet `spec_lexicon.entry` cannot read is refused, naming
    it.
  - `lay(root, item, into) -> list[str]`: `spec/` of `root` copied to `into/spec`; for each block, its term bullets
    appended to the capability file's `## Terms` (the section made before `## Behaviour` when missing) and its groups,
    headings raised to `### `, appended at the end of `## Behaviour`; returns the capability names laid.
- Produces, in `backlog_cli.py`: `cmd_line(args) -> int`, printing `<label>: <cap>#r<n>` (or `<label>: a term of
  <cap>`); the commit message is `work line: <label> <cap>#r<n>` (or `... a term of <cap>`).

**The block** (`render` writes exactly this shape; a blank line between term bullets and the first group, and
between groups):

```
## Requirements

### work-queue

- **frobnicate** (event): Forms: frobnicates, frobnicated.

#### [g4] An initiative is abandoned
- [r5] When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to `abandoned`.
```

- [x] **Step 1: Write the fixture and the failing tests.**
  - `ready_repo` in `tests/scripts/conftest.py`: `backlog_repo`, with `tests/scripts/fixtures/generate/repo/spec/`
    copied over its `spec/` less `capabilities/legacy.md`, the index's `id:` line made
    `id: bounded-context/ex.com/prod/ctx` (D17), all committed.
  - In `tests/scripts/test_backlog_lines.py`, with `ABANDON`, `FROBNICATE`, `DONE` and `TERM` copied from
    `test_supervise_outputs.py` without their `- [r5] ` prefix:
    - `test_line_writes_the_next_ids_and_commits_only_the_item`: on a `shaped` b1, `work line b1 --into work-queue
      "<ABANDON>"` exits 0 and prints `b1 "Fix the parser": work-queue#r5`. The block reads
      `[Block("work-queue", [], [Group("g4", "Fix the parser", [("r5", ABANDON)])])]`; HEAD's commit holds only
      `.shop/backlog/b1.md`.
    - `test_a_second_line_in_the_group_takes_the_next_requirement_id`: then `--in g4` gives `r6` in `g4`, and
      `--group "Another"` then gives `g5` holding `r7`.
    - `test_ids_skip_the_retired`: with `retired: [r9]` written into the fixture's `work-queue.md` and an `r8` added to
      its `g3`, the next line is `r10`.
    - `test_line_refuses_a_capability_that_is_not_codified`: `--into nothing` and `--into legacy` (the fixture's
      uncodified file copied back in) exit 1, stderr naming the capability; HEAD and the tree unchanged.
    - `test_line_refuses_an_item_that_is_not_idea_or_shaped`: a `ready` and a `withdrawn` b1, refused naming the
      status.
    - `test_line_refuses_an_unknown_group_and_text_with_a_line_break`.
    - `test_term_writes_a_term_bullet`: `work line b1 --into work-queue --term "<TERM>"` puts it under the block's
      terms; a bullet `- frobnicate` is refused naming it.
    - `test_render_round_trips_and_malformed_blocks_are_refused`: `read(render(b))` equals `b`; a block with a
      requirement before any group, and one with `r5` twice, are refused naming `Requirements`.
    - `test_lay_puts_the_block_into_a_copy_of_spec`: `lay(root, item, tmp)` returns `["work-queue"]`; `tmp`'s
      `work-queue.md` reads (`spec_read.capability`) with a `g4` holding `r5`, no problems, and its `## Terms` holds
      the term; `root/spec` is byte-identical.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_backlog_lines.py -q`
  Expected: FAIL; `backlog_lines` does not exist and `work` has no `line` command.

- [x] **Step 3: Implement `backlog_lines.py` and the `line` parser.** `TEXT` and `--term` are mutually exclusive and
  one is required; `--group` and `--in` are mutually exclusive.

- [x] **Step 4: Run the tests and the backlog's.**
  Run: `python3 -m pytest tests/scripts/test_backlog_lines.py tests/scripts/test_backlog_items.py tests/scripts/test_backlog_moves.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/features generate --check; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/backlog_lines.py scripts/backlog_cli.py tests/scripts/test_backlog_lines.py tests/scripts/conftest.py`
  Expected: the suite at `37 xfailed`, no failures, passed = 1067 + the new tests; `model check` and `generate
  --check` at their baselines; `size` silent; `check` clean.

- [x] **Step 6: Commit.**
  ```bash
  git add scripts/backlog_lines.py scripts/backlog_cli.py tests/scripts/test_backlog_lines.py tests/scripts/conftest.py CLAUDE.md
  git commit -m "backlog: an item's requirement lines and work line"
  ```

### Task 2: The bar and `work ready`

Builds `readiness#r1`-`r4`.

**Files:**
- Create: `scripts/readiness_bar.py`; `tests/scenarios/readiness_world.py`, `tests/scenarios/readiness_handlers.py`
- Modify:
  - `scripts/backlog_moves.py`: `"work ready": {"shaped": "ready"}` in `TRANSITIONS`; `ready`.
  - `scripts/backlog_cli.py`: the parser `ready` and `cmd_ready`.
  - `tests/scenarios/backlog_world.py`: `write_item` keeps a `sections` field (heading → text, written after the
    `## Question`) and a `request` field (a frontmatter line `request: q<n>` when set); `run_work(step, *args,
    **kwargs)` passes `kwargs` to `step.run`.
  - `tests/scenarios/test_readiness.py`: `bind_all(globals(), ROOT)` before `scenarios(...)`; the docstring names its
    handlers.
  - `spec/capabilities/readiness.md`: `unbuilt: []`, `## Implementation, may change` (new) and `## Not yet` (Step 7).
  - `CLAUDE.md`: a row for `readiness_bar.py`; `readiness` in the handlers row; `readiness_world.py` in the world row.
- Test: `tests/scripts/test_readiness_bar.py`

**Interfaces:**
- Consumes: Task 1's `read`, `ids`, `lay`, `capability_file`; `spec_grammar.parse`, `spec_grammar.hint`,
  `spec_solve.run`, `features_generate.generate`, `features_generate.GenerateError`, `spec_context.load`,
  `spec_tree.logic_only`, `workqueue_request.sections`, `workqueue_request.SETTLED`.
- Produces, in `readiness_bar.py`:
  - `request_lines(root, item) -> list[tuple[int, str, str | None]]`: (number, text, line outcome or None) of each line
    of the item's request whose outcome is not `rewritten` (D11); `[]` for an item with no `request`. Task 3 adds the
    field `Item.request`; until then the function reads `getattr(item, "request", None)`, which is None.
  - `unsettled(root, item) -> list[str]`: `line <n> of request q<m> is <outcome or "unanswered">, not settled: <text>`
    for each request line not in `SETTLED`.
  - `well_formed(root, item) -> tuple[list[str], list[str]]`: (reasons, warnings), per D6, D7 and D9. A parse refusal
    reads `<cap>#r<n>: <refusal>; parsed up to: <prefix>; nearest words: <words>`; a finding reads `<code> <text>`;
    a capability problem `<cap>.md: <problem>`.
  - `check(root, item) -> tuple[list[str], list[str]]`: `unsettled` + `well_formed`'s reasons, and its warnings.
- Produces, in `backlog_moves.py`: `ready(root, name) -> tuple[Item, list[str]]`, through `move(root, name, "work
  ready", change)`, where `change` raises `Refused("work ready: <label> is not passing:\n  <reason>\n  ...")` when
  `check` gives a reason, so nothing is committed; the commit message is `work ready: <label> shaped -> ready`.
  `cmd_ready` prints `<label> ready` and each warning on stderr as `work ready: warning: <text>`.
- Produces, in `readiness_world.py` (loaded by path as `shop_readiness_world`):
  - `codify(step) -> None`: D17's spec written over the repository's `spec/` once.
  - `PASSING`, `FAILING`: the fixture's `ABANDON` and `FROBNICATE` statements.
  - `give_lines(step, name, text) -> None`: `codify`, then the item `name` rewritten through `backlog_world.write_item`
    with `sections={"Requirements": <a work-queue block: g4 holding r5 text>}`.
  - `NO_INPUT = {"stdin": subprocess.DEVNULL, "timeout": 120}`.
- Produces, in `readiness_handlers.py`:
  - registry `("WhenRuns", "`work ready`")`: `B.run_work(step, "ready", B.ident(name), **NO_INPUT)`;
  - `local("GivenK_C", "item")`: `passing` gives the item `PASSING`, `not passing` gives it `FAILING` and keeps in
    `context["reason"]` the words its refusal must name (`work-queue#r5`, `frobnicate`); any other condition returns
    `False`, so `blocked` still reaches the backlog's handler;
  - `local("ThenExitsErr", "reason")`: exit 1 (not 2), and stderr holds the item's label and every word of
    `context["reason"]`;
  - registry `("ThenDoesNot", "ask")`: D16, written so intake r5 uses it as it is.

- [x] **Step 1: Write the failing script tests** in `tests/scripts/test_readiness_bar.py`, on `ready_repo` with a
  `shaped` b1 (`toolchain.require()` first):
  - `test_ready_readies_a_passing_item`: with `ABANDON` written by `work line`, `work ready b1` exits 0, prints
    `b1 "Fix the parser" ready`, and HEAD's commit holds only b1, now `ready`.
  - `test_a_line_that_does_not_parse_is_the_reason`: with `FROBNICATE`, exit 1; stderr holds `is not passing`,
    `work-queue#r5`, `frobnicate` and `parsed up to:`; HEAD and the tree unchanged.
  - `test_an_item_with_no_lines_is_not_passing`: stderr names `work line`.
  - `test_ready_refuses_an_item_that_is_not_shaped_before_checking`: an `idea` b1 with `FROBNICATE` is refused naming
    `idea` and not `frobnicate`.
  - `test_every_reason_is_named`: two groups, both `FROBNICATE`-like, give two reason lines.
  - `test_only_the_items_l0_and_l1_refuse`: with `spec_solve.run` stubbed (call `readiness_bar.well_formed`
    in-process with `monkeypatch`) to return an L1 naming `supervision#r1`, no reason; an L1 naming `work-queue#r5`,
    one; an L0 with no ids, one.
  - `test_an_l3_is_a_warning`: with `DONE`, `work ready` exits 0 and stderr holds `warning:` and `L3`.
  - `test_a_guarantees_line_is_not_generated`: a line into the fixture's `review` (a `guarantees` capability)
    `` `work run` shall hold at most `workers` worker slots at a time. `` readies.
  - `test_ready_never_writes_spec_and_cleans_up`: for a passing and a failing item, `git status --porcelain -- spec`
    is empty after the run, and `tempfile.gettempdir()` (pointed at a `tmp_path` dir through `TMPDIR`) holds nothing
    after it.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_readiness_bar.py -q`
  Expected: FAIL; `work` has no `ready` command.

- [x] **Step 3: Implement `readiness_bar.py`, `backlog_moves.ready` and the parser.** The copy of `spec/` is made with
  `tempfile.mkdtemp(prefix="readiness-")` and removed in a `finally`. Parse each of the item's requirements in the
  copy; run `spec_solve.run(copy, cap)` and `features_generate.generate(copy, path)` only when every requirement
  parses.

- [x] **Step 4: Run the tests.**
  Run: `python3 -m pytest tests/scripts/test_readiness_bar.py tests/scripts/test_backlog_moves.py tests/scripts/test_backlog_lines.py -q | tail -1`
  Expected: all pass (`test_the_moves_are_the_glossary_transitions` now includes `shaped -> ready: work ready`).

- [x] **Step 5: The world and the handlers**, as in Interfaces. Check each scenario against its point:
  - r1: the item is `ready`, and the run committed it (`ThenK_A` reads the file after a real check of `PASSING`).
  - r2: the refusal names `work-queue#r5` and `frobnicate`, not merely a non-zero exit; nothing changed.
  - r3: the backlog's `local("ThenExitsErr", "item")` reads the label and the status `idea` (D15 of plan 2).
  - r4: the item is `idea` (D15), so `work ready` refuses, and D16's Then holds: the command exists, nothing asks.
    Mutate once by hand: make `cmd_ready` print `Ready it anyway?`, see r4 fail, revert.

- [x] **Step 6: Run the readiness scenarios.** Remove `r1, r2, r3, r4` from `readiness.md`'s `unbuilt:`.
  Run: `python3 -m pytest tests/scenarios/test_readiness.py -q | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: `4 passed`; `every step has one handler`.

- [x] **Step 7: The spec's prose.** In `spec/capabilities/readiness.md`, add `## Implementation, may change` with one
  bullet each for D2 (where the lines live, `work line`), D6, D7, D8 and D9, and a `## Not yet` with two bullets: a
  new capability or a glossary term an item proposes (D4); the bar checked again when a batch picks the item (plan 4).
  Run: `python3 scripts/model check | tail -1; python3 scripts/features generate --check`
  Expected: at their baselines.

- [x] **Step 8: The baselines,** as in Task 1, Step 5, over this task's files, plus `python3 scripts/model logic |
  tail -1`.
  Expected: the suite at `33 xfailed`, no failures; `11 findings: 6 L5, 5 L6`; everything else unchanged.

- [x] **Step 9: Commit.**
  ```bash
  git add scripts/readiness_bar.py scripts/backlog_moves.py scripts/backlog_cli.py tests/scenarios/readiness_world.py \
    tests/scenarios/readiness_handlers.py tests/scenarios/backlog_world.py tests/scenarios/test_readiness.py \
    tests/scripts/test_readiness_bar.py spec/capabilities/readiness.md CLAUDE.md
  git commit -m "readiness: work ready checks the bar on a copy of spec/ (readiness r1-r4); readiness built"
  ```

### Task 3: `work intake`, and an item's request lines in the bar

Builds `intake#r1`, `r5` and `r6`.

**Files:**
- Create: `scripts/intake_moves.py` (with `intake` and `linked`); `tests/scenarios/intake_handlers.py`
- Modify:
  - `scripts/backlog_items.py`: `Item` gains `request: str | None = None` and `asked_by: str | None = None`, read and
    rendered as frontmatter lines after `depends_on` only when set, so every existing item file renders as before;
    `request` must match `q[1-9]\d*` (else refused as D16 of plan 2: `<rel>: request ...`); `as_dict` gains both keys.
  - `scripts/backlog_cli.py`: the parser `intake` and `cmd_intake` (prints `<label> shaped`).
  - `tests/scenarios/backlog_world.py`: `OF_GIVENS` moved here from `backlog_handlers.py` (D18); `run_work` skips
    `ensure_items` for `intake` as for `idea` (the item a Then names is the one the command writes).
  - `tests/scenarios/backlog_handlers.py`: `given_of` reads `B.OF_GIVENS`.
  - `tests/scenarios/readiness_world.py`: `link_request(step, line, item)` (below).
  - `tests/scenarios/test_intake.py`: `bind_all`, as Task 2.
  - `spec/capabilities/intake.md`: `unbuilt:` loses `r1, r5, r6`.
  - `CLAUDE.md`: a row for `intake_moves.py`; `intake` in the handlers row.
- Test: `tests/scripts/test_intake_moves.py`; `tests/scripts/backlog_testing.py` gains `write_request(repo, name="q1",
  asker="bounded-context/ex.com/prod/peer", status="open", turn="upstream", lines=(...), outcomes=(), commit=True)`,
  writing the file in the form `workqueue_request.request` writes (with `part_of: job-thread/ex.com/prod/t1`). The
  tests write requests by hand because `work request`'s gate (requests r32) takes only this repository's own asker.

**Interfaces:**
- Consumes: `workqueue_request.path_of`, `field`, `own_askers`, `sections`; `backlog_items` as in Task 1;
  `backlog_moves.idea`'s numbering (`next_name`) and `commit`.
- Produces, in `intake_moves.py`:
  - `provenance_of(root, asker) -> str` (D10).
  - `linked(root, request) -> Item | None`: the item whose `request` is `request`.
  - `intake(root, request) -> Item`: D10, one commit of the item file alone, message
    `work intake: q<n> "<title>" -> <label> shaped`. Refusals: no such request (`path_of`'s); a status that is not
    `open` or `awaiting-upstream`, naming it; a request already taken in, naming the item's label.
- Produces, in `readiness_world.py`: `link_request(step, line, item)`: writes the world's own request `q9`
  (`asker: bounded-context/ex.com/prod/peer`, `status: open`, `turn: upstream`, `## Lines` with `1. <PASSING>`, and
  under `## Outcomes` the line outcome a Given gave the line, if any), gives the item `request="q9"`, and keeps
  `context["line_of"][line] = ("q9", 1)` and `says[line] = "line 1 of request q9"`.
- Produces, in `intake_handlers.py`:
  - registry `("WhenRuns", "`work intake`")`: `work intake q<n>` with `NO_INPUT`;
  - `B.OF_GIVENS["request line"] = lambda step: R.link_request(step, *step.names)`;
  - `local("GivenK_C", "request line")`: `settled` writes the outcome `accepted`, `not settled` none (a line with no
    outcome); any other condition returns `False` (requests' `unparsed`);
  - registry `("ThenR", "asked by")`: the item's `asked_by` is the asker of the request the run took in, and is not
    this context's own (`own_askers`);
  - `local("ThenExitsErr", "request line")`: exit 1, and stderr holds `says[line]`.
  - The backlog's handlers already read `writes the item`, `is `shaped``, `is `peer`` (the attribute `provenance`) and
    `commits the item`.

- [x] **Step 1: Write the failing tests** in `tests/scripts/test_intake_moves.py`, on `ready_repo` with a request
  `q1` titled `Archive old items`, written by `write_request` with the one line `ABANDON`:
  - `test_intake_writes_a_shaped_peer_item_and_commits_only_it`: `work intake q1` exits 0 and prints
    `b1 "Archive old items" shaped`; b1 has `provenance: peer`, `request: q1`, `asked_by:
    bounded-context/ex.com/prod/peer`, the note naming `q1`; HEAD's commit holds only `.shop/backlog/b1.md`; `q1.md`
    is byte-identical.
  - `test_provenance_is_read_off_the_asker`: `internal` → `own`, `product/ex.com/prod` → `product`, a peer → `peer`
    (`provenance_of` directly).
  - `test_intake_refuses_a_request_taken_in`: a second `work intake q1` exits 1 naming `b1 "Archive old items"`.
  - `test_intake_refuses_a_request_out_of_turn`: `awaiting-asker` and `delivered` (edited into `q1.md` and committed)
    are refused naming the status; `awaiting-upstream` is taken in.
  - `test_an_item_without_request_fields_renders_as_before`: every item file plan 2's tests write round-trips
    byte for byte; `request: 7` is refused naming `request`.
  - `test_ready_names_an_unsettled_line_of_the_items_request`: after intake, `work ready b1` exits 1 naming
    `line 1 of request q1` and `work line`.
  - `test_unsettled_names_each_line`: an item taken in from a request with lines 1-3 and outcomes `1. accepted`,
    `2. question`, `3. rewritten` gives `readiness_bar.unsettled` exactly one reason, naming `line 2 of request q1`.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_intake_moves.py -q`
  Expected: FAIL; `work` has no `intake` command.

- [x] **Step 3: Implement the item fields, `intake_moves.intake` and `linked`, and the parser.**

- [x] **Step 4: Run the tests and the backlog's.**
  Run: `python3 -m pytest tests/scripts/test_intake_moves.py tests/scripts/test_readiness_bar.py tests/scripts/test_backlog_items.py tests/scenarios/test_backlog.py tests/scenarios/test_requests.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The handlers**, as in Interfaces. Check each scenario against its point:
  - r1: the item is the file the run wrote (not one `ensure_items` wrote), `shaped`, `peer`, asked by the request's
    asker (`other`, which world_nodes writes), and committed.
  - r5: the request is `awaiting-upstream`; D16's Then.
  - r6: the refusal names `line 1 of request q9`, the item is `shaped`, nothing changed.

- [x] **Step 6: Mark them built.** Remove `r1, r5, r6` from `intake.md`'s `unbuilt:`.
  Run: `python3 -m pytest tests/scenarios/test_intake.py -q | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: `3 passed, 3 xfailed`; `every step has one handler`.

- [x] **Step 7: The baselines,** as in Task 2, Step 8.
  Expected: the suite at `30 xfailed`, no failures; everything else unchanged.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/intake_moves.py scripts/backlog_items.py scripts/backlog_cli.py tests/scenarios/intake_handlers.py \
    tests/scenarios/backlog_world.py tests/scenarios/backlog_handlers.py tests/scenarios/readiness_world.py \
    tests/scenarios/test_intake.py tests/scripts/test_intake_moves.py tests/scripts/test_readiness_bar.py \
    spec/capabilities/intake.md CLAUDE.md
  git commit -m "intake: work intake takes a peer's request in as a shaped item (intake r1, r5, r6)"
  ```

### Task 4: `work outcome` on a taken-in request: accept, refuse, counter-propose

Builds `intake#r2`, `r3` and `r4`.

**Files:**
- Modify:
  - `scripts/intake_moves.py`: `handles` and `outcome`.
  - `scripts/work`: the `outcome` parser gains `--into`, `--group`, `--reason` and `--line`; `cmd_outcome` sends the
    command to `intake_moves.outcome` when `intake_moves.handles(args)`, else to `workqueue_request.outcome` as now.
  - `scripts/model_requests.py`: `SECTIONS` gains `"Reasons"` (D13).
  - `tests/scenarios/intake_handlers.py`, `tests/scenarios/readiness_world.py`.
  - `spec/capabilities/intake.md`: `unbuilt: []`, `## Implementation, may change` (new) and `## Not yet` (Step 6).
- Test: `tests/scripts/test_intake_outcome.py`

**Interfaces:**
- Consumes: Task 1's `add_line_to`; Task 3's `linked`; `workqueue_request`'s `path_of`, `field`, `_entries`,
  `_with_entries`, `_with_field`, `_numbered`, `_refuse_upstream_part` and `turn`'s rule (call its edit on the text;
  do not copy it); `workqueue_lines.check`; `workqueue.committed`.
- Produces, in `intake_moves.py`:
  - `handles(args) -> bool`: any of `into`, `group`, `reason`, `line` given, or `linked(root, request)`.
  - `outcome(root, request, number, word, into=None, group=None, reason=None, line=None) -> None`: D12. Refusals, each
    before anything is written: a number with no line; `--into` or `--group` on a request no item was taken in from,
    or with a word other than `accepted`; `accepted` on a taken-in request with no `--into`; `refused` on a taken-in
    request with no `--reason`; `--line` with a word other than `rewritten`; a counter-proposal that does not parse
    (`workqueue_lines.check`'s refusal); a linked item that is `delivered`, `refused` or `withdrawn`. The commit
    message is `work outcome: q<n> line <k> <word>` (`... -> <label>` when an item is written).

- [x] **Step 1: Write the failing tests** in `tests/scripts/test_intake_outcome.py`, on Task 3's `q1` taken in as b1:
  - `test_accepted_writes_the_line_into_the_item`: `work outcome q1 1 accepted --into work-queue` exits 0; q1's
    `## Outcomes` holds `1. accepted`; b1's block holds `g4`/`r5` with the line's text, and its notes
    `line 1 of request q1 accepted into work-queue#r5`; HEAD's one commit holds both files. Then `work ready b1` exits 0.
  - `test_accepted_without_into_is_refused`.
  - `test_refused_writes_the_reason`: `--reason "out of scope"` gives `## Outcomes` `1. refused`, `## Reasons`
    `1. out of scope`, the note in b1, one commit of both. Without `--reason`, refused.
  - `test_rewritten_with_a_line_passes_the_turn`: a request q2 (`write_request`, not taken in) with one line; `work outcome q2 1
    rewritten --line "<ABANDON with the status started>"` gives `## Lines` `2. ...`, `## Outcomes` `1. rewritten`,
    `## Reasons` `1. rewritten as line 2`, `status: awaiting-asker`, `turn: asker`, one commit of q2 alone.
  - `test_a_counter_proposal_that_does_not_parse_is_refused`: `FROBNICATE` as `--line`; stderr has `parsed up to:`.
  - `test_the_rewritten_line_is_not_the_items`: on the taken-in q1, `rewritten --line ...` and then (after `work turn
    q1` twice, as the asker and back) `work outcome q1 2 accepted --into work-queue`: `readiness_bar.request_lines`
    gives line 2 only, and `work ready b1` exits 0.
  - `test_the_asker_turn_still_refuses`: in the asker's turn, any word with `--reason` is refused as today.
  - `test_old_outcome_is_unchanged`: on a request no item was taken in from, `work outcome q2 1 accepted` gives the
    commit's files, message and q2's bytes that `workqueue_request.outcome` gives on a copy of the repository.
  - `test_model_check_accepts_reasons`: `model check --root` on the repository after the refused outcome reports no
    request-form problem for q1.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_intake_outcome.py -q`
  Expected: FAIL; `work outcome` has no `--into`.

- [x] **Step 3: Implement `handles`, `outcome`, the options and `SECTIONS`.** Read the request once, build its new
  text by the old helpers, and commit it with the item in one `workqueue.committed` call.

- [x] **Step 4: Run the tests and the old requests'.**
  Run: `python3 -m pytest tests/scripts/test_intake_outcome.py tests/scripts/test_intake_moves.py tests/scenarios/test_requests.py tests/scripts/test_work_show_request.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The handlers.**
  - **Registry:** `("WhenRuns", "`work outcome accepted`")`, `` `work outcome refused` `` and `` `work outcome
    rewritten` ``. Each takes the request and number from `context["line_of"][line]`, records
    `context["before"] = {"status": ..., "side": ...}` of that request (read by requests' `ThenDoes change`), and runs
    `work outcome q<n> <k> <word>` with, by word: `--into work-queue`; `--reason "out of scope"` (kept as
    `context["reason_text"]`); `--line <COUNTER>` (`readiness_world.COUNTER`: the fixture's `ABANDON` with `started`
    for `proposed`), after `codify(step)` so the line parses.
  - **`local`:**
    - `("GivenR", "request line")` with `proposed in`: records `context["line_of"][line] = (request, 1)` and returns
      `False`, so the requests' handler still runs.
    - `("ThenK_A", "request line")`: the request's `## Outcomes` entry for the line's number is (is not) the value.
    - `("ThenDoes", "reason")` with `write`: a file the run changed holds `context["reason_text"]`.
    - `("ThenDoes", "request line")` with `write`: the request's `## Lines` gained an entry; the name is bound to it.
  Check each scenario against its point:
  - r2: `1. accepted` in the request and the item in the commit;
  - r3: `1. refused`, the reason in a changed file, the item in the commit;
  - r4: `1. rewritten`, line 2 written, and the side moved from `upstream` to `asker`.

- [x] **Step 6: Mark them built, and the spec's prose.** In `intake.md`: `unbuilt: []`; `## Implementation, may
  change` with one bullet each for D10, D11, D12 and D13; `## Not yet` keeps its bullet and gains one for D14 (the
  intake session started by `work backlog`, plan 4).
  Run: `python3 -m pytest tests/scenarios/test_intake.py -q | tail -1; python3 scripts/features vocab --check | tail -1; python3 scripts/model check | tail -1; python3 scripts/features generate --check`
  Expected: `6 passed`; `every step has one handler`; `model check` and `generate --check` at their baselines.

- [x] **Step 7: The baselines,** as in Task 2, Step 8, with `scripts/work` and `scripts/model_requests.py` in the
  `tools check` list.
  Expected: the suite at `27 xfailed`, no failures; `scripts/work` at most 222 lines; everything else unchanged.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/intake_moves.py scripts/work scripts/model_requests.py tests/scenarios/intake_handlers.py \
    tests/scenarios/readiness_world.py tests/scripts/test_intake_outcome.py spec/capabilities/intake.md
  git commit -m "intake: work outcome accepts a line into the item, refuses with a reason, counter-proposes (intake r2-r4); intake built"
  ```

### Task 5: The skills: shaping items in a brainstorming, taking in a request

Meets `brainstorming#r1` and `r2`; `r3` stays unbuilt (D15).

**Files:**
- Create: `skills/shaping-items/SKILL.md`, `skills/taking-in-a-request/SKILL.md`
- Modify: `spec/capabilities/brainstorming.md`: `unbuilt: [r3]`, and a `## Not yet` bullet: r3 waits for `work quote`
  (plan 8).
- Test: `tests/scripts/test_skill_shaping_items.py`

**What each skill says** (the implementer writes the prose, in `raising-a-request`'s form: frontmatter `name` and a
`description` that starts "Use when", Overview, Process, Red Flags):
- `shaping-items`: use when a brainstorming with the person settles work to do, in a repository with a codified
  `spec/`, before any design document or plan is written. Process:
  1. `work idea "<title>"`, then `work shape <b> --note "<the context to work from>"`;
  2. for each behaviour, find the words and write the line as `raising-a-request` steps 1-5 say (`model lexicon`,
     `model parse`, a missing word as a term bullet with `work line --term`), then `work line <b> --into <capability>
     "<line>"` (`--in g<n>` for a line of the same scenario);
  3. `work rate <b> --value ... --urgency ... --size ...`, with a reason for each in the note;
  4. `work ready <b>`; on a refusal, reword from its reasons and run it again;
  5. tell the person the items and their lines afterwards, in the backlog's words (`work backlog`).
  It holds the sentence **"Do not ask the person to approve the lines: nothing waits on their reading."** and, until
  `work quote` exists, says to cite the person's words in the item's note with the date.
  Red Flags include: a design document in place of items; asking the person before `work ready`; a line bent onto a
  nearby word.
- `taking-in-a-request`: use when a request is open or awaiting the upstream in this repository's
  `.shop/work/requests/`. Process: `work intake q<n>`; for each line, judge it against `spec/` and answer with `work
  outcome q<n> <k> accepted --into <capability>`, `refused --reason "<why>"` or `rewritten --line "<counter>"`;
  `work turn q<n>` when every line has an answer; `work ready <b>` once every line is settled. It asks no person; when
  the two sides cannot agree after a counter-proposal is itself rewritten, it stops and names the request to the
  person in its last message.

- [ ] **Step 1: Write the failing test** `tests/scripts/test_skill_shaping_items.py`:
  - `test_r1_the_session_writes_lines_and_readies`: in `skills/shaping-items/SKILL.md`, the Process names
    `work idea`, `work line` and `work ready`, and `work line` comes before `work ready`.
  - `test_r2_nothing_waits_on_the_person`: the skill holds the pinned sentence, and no Process step after the one
    naming `work ready` holds "ask the person" or "wait".
  - `test_the_skills_name_only_commands_work_has`: every `` `work <sub>` `` in the two skills is a subcommand of
    `scripts/work` (read from `work --help`'s choices), and every `` `model <sub>` `` one of `scripts/model`'s.
  - `test_each_skill_has_a_use_when_description`: both frontmatters have `name` equal to the directory and a
    `description` starting `Use when`.

- [ ] **Step 2: Run it to verify it fails.**
  Run: `python3 -m pytest tests/scripts/test_skill_shaping_items.py -q`
  Expected: FAIL; the skills do not exist.

- [ ] **Step 3: Write the two skills.**

- [ ] **Step 4: Run the test.** Then set `brainstorming.md`'s `unbuilt: [r3]` and its `## Not yet` bullet.
  Run: `python3 -m pytest tests/scripts/test_skill_shaping_items.py tests/scripts/test_agents.py -q | tail -1; python3 scripts/model check | tail -1`
  Expected: all pass; `model check` at its baseline.

- [ ] **Step 5: Commit.**
  ```bash
  git add skills/shaping-items/SKILL.md skills/taking-in-a-request/SKILL.md tests/scripts/test_skill_shaping_items.py \
    spec/capabilities/brainstorming.md
  git commit -m "skills: shaping-items writes and readies an item's lines (brainstorming r1, r2), taking-in-a-request answers a peer"
  ```

### Task 6: Whole-plan verification and records

**Files:**
- Create: `.shop/records/2026-11-04-workflow-simplification/plan-3-implementation.md`
- Modify: `.shop/records/README.md` (a row for the report); this plan (every box ticked)

- [ ] **Step 1: Every requirement of the plan is built.**
  Run: `python3 -c "import sys; sys.path.insert(0,'scripts'); import pathlib, spec_unbuilt as u; d=u.unbuilt(pathlib.Path('.')); print('readiness' in d, 'intake' in d, sorted(d.get('brainstorming', ())), sum(map(len,d.values())), u.problems(pathlib.Path('.')))"`
  Expected: `False False ['r3'] 36 []`.
  (36 = 48 − 4 readiness − 6 intake − 2 brainstorming.)
- [ ] **Step 2: The baselines, all at once.**
  Run: `python3 -m pytest -q | tail -2; python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check | tail -1; python3 scripts/features generate --check; python3 scripts/features vocab --check | tail -1; python3 scripts/features bindings --unbound; python3 scripts/tools size --limit 300; python3 scripts/tools check $(git diff --name-only 3d9e2a91...HEAD -- '*.py' scripts/work)`
  Expected:
  - the suite: `27 xfailed`, no failures, passed = 1067 + 10 + the new script tests;
  - `model check`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`;
  - `model logic`: `11 findings: 6 L5, 5 L6`;
  - the lexicon: `401 terms, 0 problems`;
  - `generate --check`: exit 0; `vocab --check`: `every step has one handler`; `bindings --unbound`: `every binding
    names a scenario`; `size`: silent; `check`: nothing to report.
- [ ] **Step 3: A smoke run in a scratch repository,** both ways in:
  ```bash
  d=$(mktemp -d) && git -C "$d" init -q -b main && git -C "$d" config user.name t && git -C "$d" config user.email t@example.com
  cp -r tests/scripts/fixtures/generate/repo/spec "$d/" && rm "$d/spec/capabilities/legacy.md"
  sed -i 's#^id: bounded-context/.*#id: bounded-context/ex.com/prod/ctx#' "$d/spec/index.md"
  git -C "$d" add -A && git -C "$d" commit -qm init
  r=$PWD; W() { python3 "$r/scripts/work" --root "$d" "$@"; }
  W idea "Abandon a started initiative" && W shape b1 --note "from the smoke run"
  W line b1 --into work-queue 'When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to `abandoned`.'
  time W ready b1
  mkdir -p "$d/.shop/work/requests" && printf '%s\n' '---' 'id: request/ex.com/prod/ctx/q1' 'kind: request' \
    'asker: bounded-context/ex.com/prod/peer' 'part_of: job-thread/ex.com/prod/t1' 'status: open' 'turn: upstream' '---' '' \
    '# Print a started initiative' '' '## Lines' \
    '1. When the person runs `work start` on an initiative that is `proposed`, `work` shall print the initiative.' '' \
    '## Questions' '' '## Answers' '' '## Outcomes' '' '## Resolution' > "$d/.shop/work/requests/q1.md"
  git -C "$d" add -A && git -C "$d" commit -qm "a peer's request"
  W intake q1 && W ready b2; W outcome q1 1 accepted --into work-queue && W turn q1 && W ready b2 && W backlog
  ```
  Expected:
  - `b1 "Abandon a started initiative" ready`, and the time `work ready` took (record it);
  - the first `W ready b2` refused naming `line 1 of request q1`; the second readies b2;
  - `work backlog`'s `ready` table holds b1 and b2, b2 with provenance `peer`;
  - `git -C "$d" status --porcelain` empty, and `git -C "$d" diff --stat "$(git -C "$d" rev-list --max-parents=0 HEAD)" HEAD -- spec` empty.
- [ ] **Step 4: Write the implementation report** at
  `.shop/records/2026-11-04-workflow-simplification/plan-3-implementation.md`, in `plan-2-implementation.md`'s form
  (no frontmatter): Final state (each Step 2 figure as measured, and the smoke run's `work ready` time); the commits,
  a table of each task's commit, what was done and its verification; deviations, each with its reason; D1-D19, each
  kept or changed; open problems for plan 4 and later; files.
- [ ] **Step 5: Index the records.** Add a row to `.shop/records/README.md` after the row for `plan-2-rulings.md`:
  `| \`2026-11-04-workflow-simplification/plan-3-implementation.md\` | plan 3 executed: readiness and intake built (an item's requirement lines and \`work line\`, \`work ready\` checking the bar on a copy of \`spec/\`, \`work intake\`, \`work outcome\` accepting into the item, refusing with a reason and counter-proposing), the shaping-items and taking-in-a-request skills, 12 requirements out of \`unbuilt:\` | report |`.
  Tick every box of this plan.
- [ ] **Step 6: Commit.**
  ```bash
  git add .shop/records/2026-11-04-workflow-simplification/plan-3-implementation.md .shop/records/README.md \
    .shop/records/2026-11-04-workflow-simplification/plan-3-readiness-intake.md
  git commit -m "records: plan 3 verified, its implementation report"
  ```
  The end-of-branch review follows, by a separate reviewer, into `plan-3-review.md`, reading `<this plan's commit>..HEAD`
  on `workflow-simplification` against this plan's Review Focus.
