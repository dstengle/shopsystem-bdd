# Plan of w129: work show prints requests; work status prints uncited observations

## 1. What goes green

- **requests#r13**: "show prints each request with its status and whose turn it is" (features/requests.feature:148).
  It is red today because no step module binds requests.feature (StepDefinitionNotFoundError on the first Given). Under
  that, `work show` prints work-items only: `scripts/work:cmd_show` prints `workqueue.items()`, which yields
  `kind: work-item` files only (probe P1).
- **requests#r14**: "status with no initiative prints, with its date, each observation no initiative's or request's
  source names" (requests.feature:157). It is red today for the same missing steps. Under that,
  `workqueue_status.status()` reads only initiative directories and prints no observation (probes P2 to P4), and no
  `workqueue*` module reads `.shop/records/observations.md`.

The work-item retires nothing.

## 2. Where the change lands

- `scripts/workqueue.py`: a reader of the requests under `.shop/work/requests/`. For each request it gives its name
  (`q<n>`), status, turn and `source`, and it reads each file through `workqueue.read`, which refuses a file that is
  not UTF-8. `items()` and `highest()` keep skipping files that are not work-items. The file has room for 38 more lines.
- `scripts/work`: `cmd_show` prints a line for each request after the work-items, and its `--json` object gains a
  requests key next to the unchanged `work-items` key.
- `scripts/workqueue_status.py`: a reader of observations (id and `date:`) from `.shop/records/observations.md`. With
  no initiative, `status()` prints the uncited observations after the initiative blocks, and its `--json` object gains
  an observations key. `open_text` keeps printing only the initiative blocks (decision D3).
- `tests/scenarios/test_requests.py`: binds `features/requests.feature` with `scenarios(...)`. w126 and w128 name the
  same file, so if it already exists when this lands, leave it as it is.
- `tests/scenarios/requests_show_steps.py` (new): the Givens of requests with a status and a turn, of requests with an
  origin, of dated observations and of an initiative with a source, and the Thens of both scenarios. It reuses the
  conftest's `repo`, `run` and `context` and the work-queue step that makes an initiative under `.shop/work/`. It gets
  its own module, not w126's and w128's `requests_steps.py`, under CLAUDE.md's rule of one step module per concern.

Removed from the researcher's set:
- `scripts/model_work.py`: w131 ("model reads requests") owns how `model` reads `.shop/work/requests/` and request
  `source` lines. Neither r13 nor r14 asks anything of `model check`.
- `scripts/migrate_session.py`: it calls `workqueue_status.open_text`. Under D3 that function keeps giving only the
  initiative blocks, so this file does not change.
- `CLAUDE.md`: no new script module is added, and the module map's `tests/scenarios/` row already covers the new step
  module.

## 3. Decisions

- **D1. The observations are added to `work status`'s output; they do not replace the initiative blocks.** This
  settles the researcher's first question, and requirements settle it, not a reading. requests#r14 and work-queue#r17
  both say what `work status` with no initiative "shall print", and neither is retired. Only output that holds both is
  allowed: the r16 blocks of each initiative that is neither done nor abandoned, then the uncited observations. When
  there are no open initiatives, only the observations are printed. When there is nothing to print, the output is
  empty and the command exits successfully (design-decision/query-commands-answer-in-their-output).
- **D2. With `--json`, the new parts appear under new keys of the same JSON object.** `work show --json` adds the
  requests (name, status, turn) and `work status --json` with no initiative adds the observations (id, date). The
  existing `work-items` and `initiatives` keys stay as they are. This rests on
  design-decision/query-commands-answer-in-their-output ("prints its whole result as one JSON object"; "the keys …
  are Implementation"), work-queue#r11, work-queue#r18, and requests#r13 and #r14, which apply whenever the command is
  run.
- **D3. The SessionStart hook's text stays per initiative.** `open_text` prints only the initiative blocks, not the
  observation lines. migration-tools#r32 asks the hook for "what `work status` prints for each such initiative", which
  means the r16 blocks and not the r14 observations. The narrator of requests is not the hook's audience. Splitting
  `status()` into the initiative part, which `open_text` uses, and the observation part, which only the
  no-initiative `status` command adds, satisfies both lines.
- **D4. A request file that is not UTF-8 makes `work show` refuse, naming the file.** The same goes for `work status`
  with no initiative, because that command reads request sources. This settles the researcher's second question. It
  rests on work-queue#r7 and on design-decision/query-commands-answer-in-their-output: the command cannot answer
  without reading the file. It is the same refusal work-queue's "show refuses a file … not UTF-8 text" scenario pins
  for work-items, and probe P6 shows `show` already does it. A `.shop/records/observations.md` that is not UTF-8
  likewise makes `work status` with no initiative refuse. `open_text` reads neither file, so the hook is unaffected.
- **D5. Which sources count as naming an observation.** An observation is named when the `source` of any initiative
  under `.shop/work/`, of any status including done and abandoned, or of any request, of any status, gives its id.
  That id may be the full `observation/<context path>/<slug>` or the short `observation/<slug>` that the decisions'
  `source` lines use. This rests on requests#r14 ("the `source` of no initiative and of no request"). A request with
  `part_of` and no `source` names no observation.
- **D6. Each request line of `show` names the request, its status and whose turn it is (`asker` or `upstream`), from
  the request's frontmatter.** This rests on requests#r13 and the capability's Implementation section (the file's
  `status` and `turn`).

## 4. Tests the decisions break

None. What I checked:
- `test_work_queue.py::test_status_with_no_initiative_prints_each_initiative_that_is_neither_done_nor_abandoned`: its
  step `prints_each_status` (work_queue_status_steps.py:135-140) looks for each `work status <id>` output as a run of
  consecutive lines, and `nothing_about_either` matches whole words `i2`/`i3`. Under D1 the initiative blocks stay
  together and the observation lines come after them, so both checks still hold.
- The status JSON step reads `json["initiatives"]` (line 151), which D2 leaves unchanged.
- `test_migration_tools.py` r32 scenario: under D3 `open_text` is unchanged.
- The work-queue show scenarios, including the non-UTF-8 refusal: work-item lines and the `work-items` JSON key are
  unchanged. Their fixtures write no `.shop/work/requests/` directory (the notes' search).
- `scripts/work_items.py:acceptors` reading a non-UTF-8 request file is outside this work. No test writes one.

## 5. Open cases (for the implementer to name, not to choose)

- The order of request lines in `show` (for example by request number, natural order) and of observation lines in
  `status` (for example in file order or by date).
- `work show` or `work status` when `.shop/work/requests/` or `.shop/records/observations.md` does not exist. By D1
  this is an empty part, not a refusal, but the scenarios do not pin it.
- A request file whose frontmatter has no closing `---` (probe P7: skipped silently today, as work-item files are), or
  one with no `status` or `turn`.
- An observation heading with no `date:` line.
- Whether `show` and `status` mark the request and observation parts with a heading line, and what the text line of
  each looks like, provided each line holds the words the scenarios assert (`q1`, `open`, `upstream`; `o3` and its date).
