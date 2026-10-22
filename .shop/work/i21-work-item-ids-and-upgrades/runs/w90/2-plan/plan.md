# Plan: work-queue-5 (work-queue#r1, work-queue#r12)

From the research notes (`runs/work-queue-5/1-research/notes.md`), the work-item's ruling (formulation round f1), design-decision/work-items-named-by-ids and `features/work-queue.feature`.

## 1. What goes green

- **work-queue#r1**
  - `add with a title, --part-of, --under and --accepts writes a drafted work-item named by its id and prints the id`: red today. Its first Given (`an initiative i1 under .shop/work/`) has no step. `work prints one id w<n>, and nothing else` falls into `prints_statuses`, which fails. The `w<n>.md ... whose id is that w<n>` and `` its `# ` heading is `` steps do not exist. Behind the steps, `workqueue.add` writes `<title>.md` with the title as its id, and `cmd_add` prints nothing (probe P1).
  - `add with --part-of, --under and --accepts writes a drafted work-item with the fields given (deprecated)`: passes today and must still pass. Under the ruling, `w1` is the title. In an empty store the new work-item is `w1`, so `w1.md` with the id `w1` comes out as before.
- **work-queue#r12**: `add numbers the new work-item one above the highest work-item under .shop/work/, in any initiative and any status`: red today. `with_items` splits `w2 is green and whose work-item w4 is withdrawn` wrongly. `work prints w5` raises in `prints_statuses`. `whose id is w5` and `no other work-item's file has changed` have no step. `add` numbers nothing (P3).
- **Retires:** the work-item has no Retires section, so it retires nothing. See the question in part 3 about the deprecated r2 and r7 `add when the work-item's file already exists ...` scenarios.

## 2. Where the change lands

- `scripts/workqueue.py`: `add` takes the title. It numbers the new work-item `w<n>`, with `<n>` one above the highest `<n>` among the work-items under `.shop/work/`. It writes `.shop/work/<initiative>/w<n>.md` with the id `work-item/<context>/w<n>` and the title as its `# ` heading, and returns the id. It needs a small helper that gives the highest `<n>`, read from the `w<n>.md` file names of the work-items `items()` yields. Room is 57 lines.
- `scripts/work`: `cmd_add` prints the id `add` returns, and nothing else.
- `tests/scenarios/test_work_queue.py` (room 17):
  - narrow `prints_statuses` so it no longer matches `one id w<n>, ...` or a bare `w5`;
  - `with_items` takes a repeated `and whose work-item <w> is <status>`;
  - `given_fields` reads the file of the work-item the scenario wrote: the printed id's file, or `w1.md` for the deprecated r1 scenario;
  - add the import of the new step module.
- `tests/scenarios/work_queue_add_steps.py` (new, following the `<capability>_*_steps.py` row of CLAUDE.md): the steps for
  - the bare `an initiative i1 under .shop/work/` Given;
  - `work prints one id w<n>, and nothing else`;
  - `work prints <id>`;
  - `.shop/work/i1/w<n>.md is a drafted work-item whose id is that w<n>` and `... whose id is w5`;
  - `` its `# ` heading is ... ``;
  - `no other work-item's file has changed`.

No file is added to or removed from the researcher's set.

## 3. Decisions

- **D1. The title still passes the one-directory-entry check** (`entry` on the name). The refusal `the name ../../w1 is not a file name` stays for a title that is a path. The notes suggested dropping the check. This rests on the work-item's ruling: the unchanged scenarios that call `work add i1 <name> ...` take the name as the title and must pass, among them the `@r7` outline row `i1 | ../../w1`.
- **D2. Which files count toward `<n>`.** Only work-items count: files with `kind: work-item`, the files `work show` lists (`items()`). A `w<n>.md` of another kind, or one with no frontmatter, does not count (P4's `w50`, `w70`), and neither does a file not named `w<n>.md` (a typed name from before the upgrade). `<n>` is read from the file name `w<n>.md`. Rests on work-queue#r12 ("any work-item"), work-queue#r3 (what a work-item of the queue is), and the work-item's ruling on where `<n>` is read from.
- **D3. A file under `.shop/work/` that `add` cannot read while numbering is refused.** `add` exits with an error, names the file (`... is not UTF-8 text`, as `show` says it) and writes nothing. Rests on work-queue#r7: `add` cannot number without reading every work-item, and r12 requires it to. Before this change `add` read no other file (P9).
- **D4. The "already exists" check.** Under r12, `w<n>.md` is new by construction, so the path guard can only trip in a race. It stays as a guard, and the refusal names the `w<n>` path. Rests on work-queue#r7.
- **Q1 (open, the plan's question). The deprecated scenarios `add when the work-item's file already exists leaves the file as it was (deprecated)` (@r2) and `... is refused, saying so, with an error (deprecated)` (@r7).** Under r1 and r12, `work add i1 w1 ...` beside an existing `w1` writes `w2.md` titled `w1`, so both scenarios break: r2 through the whole-repository snapshot in `as_it_was`, r7 through the refusal.
  - The scenarios are marked `Deprecated for: removal`, and the proposal ids-work-queue removes work-queue#r2.
  - This work-item has no Retires section, so the implementer may not `features retire` them (bdd-red-green).
  - Nothing under `--whole-suite` marks them expected-red, since no open work-item accepts @r2, and @r7's other acceptors are not known.
  - The ruling says the unchanged scenarios calling `work add i1 w1` must pass, but these two are deprecated, not unchanged.
  - Which way this goes changes what the narrator sees, and no line settles it. See the result's `questions`.

## 4. Tests the decisions break

- `features/work-queue.feature` @r2 deprecated `add when the work-item's file already exists leaves the file as it was (deprecated)`: broken by r1 and r12. Reading A of Q1: retired with `features retire`, together with `as_it_was` if nothing else uses it. Reading B: kept, and it passes because `add` refuses.
- `features/work-queue.feature` @r7 deprecated `add when the work-item's file already exists is refused, saying so, with an error (deprecated)`: broken by r1 and r12. Same two fates as above.
- `prints_statuses`, `given_fields` and `with_items` in `test_work_queue.py`: rewritten as part 2 says. The r3 and r11 `work prints w1 with drafted, ...` steps keep asserting what they assert today.
- None of these break: `tests/scripts/test_work_withdraw.py`, `tests/scripts/test_work_items.py` and `work_queue_withdraw_steps.py`. They write `w1` files directly and do not call `add` (notes part 4, by search).
- The r9 outline row `add` (`add i1 w1`, empty store → `w1.md` as work left it) and the r7 outline rows (missing initiative, missing or short `spec/index.md`, newline, `../../spec`, `../../w1`) keep passing, provided:
  - the existing refusals still run before numbering reads anything;
  - the order stays the same: the entry checks, then the newline check, then the initiative's existence and `context_path`;
  - D1 keeps the title check.

## 5. Open cases

- Two `work add` runs at once can number the same `w<n>`. There is no lock (notes part 5).
- A store not yet upgraded (0.23.1 typed names): `add` numbers from 1 next to typed work-items. The 0.24.0 upgrade (`migrate_upgrade_ids.py`) then numbers the existing work-items from 1 as well and may collide (notes question 4). This is migration's concern, not settled here.
- A `w<n>.md` whose stem has leading zeros or extra characters (`w05`, `w5a`).
- A title that is empty, or that holds characters a `# ` heading cannot carry (a newline in the title itself).
- D1 in `show` (notes part 6): a partial listing printed before the refusal of a non-UTF-8 file. Not this work-item's.
