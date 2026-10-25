# w168 research: answer named by its initiative (work-queue#r30)

Method: no `tools map` in this checkout, so `tools tests-of` and `tools untested` refuse; every test list is `by search`. `tools refs` takes a dotted name; callers were found `by search` (grep over scripts/, tests/, features/, spec/).

## 1. Why each scenario is red today

Command: `python3 -m pytest -q "tests/scenarios/test_work_queue.py::test_answer_named_by_its_initiative_answers_the_kind_name_of_that_initiative[<row>]"` (run)

- `[capability-proposal-p1-...]`: `When the session runs \`work answer i2/p1 "Use the first reading"\``; Given steps pass. Then `has_answer` (tests/scenarios/work_queue_answer_steps.py:37) fails: `returncode 1`, stderr `work: there is no work-item i2/p1 under .shop/work`.
- `[work-item-w2-work-item w1]`: same, `work: there is no work-item i2/w2 under .shop/work`.

Cause: `workqueue.find(root, name)` (scripts/workqueue.py:222-227) returns no file for any name containing `/` (`if "/" not in name else []`). `scripts/workqueue_answer.py:answer` (line 29) calls it with the whole `i2/p1`. Missing: `answer` (or `find`) must split `<initiative>/<name>`, look in that initiative only, and then use the bare name for `agrees`, `move`, `committed` and the log. Nothing in the step definitions is missing; the steps already write the initiatives, the log lines and the proposal's `## Questions`.

## 2. What the system answers today

Probe file: `.shop/scratch/w168-1-research/probe_answer.py` and `probe_glob.py`. Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w168-1-research/probe_answer.py` (run; `-n 0` needed to see stdout). Each repo is built in scratch with `spec/index.md`, initiatives, work-items with `log.jsonl`, committed.

| case | today's result (run) |
|---|---|
| A1 `answer i2/p1` (p1 proposal awaiting, only in i2) | rc 1, `there is no work-item i2/p1 under .shop/work` |
| A2 `answer i1/w1` (w1 awaiting in i1) | rc 1, `there is no work-item i1/w1` |
| B1 `answer i2/w2` (w2 awaiting, log says claimed) | rc 1, `there is no work-item i2/w2` |
| B2 `answer i1/p1` (p1 only in i2) | rc 1, `there is no work-item i1/p1` (correct outcome, wrong reason) |
| C1 bare `answer p1` with p1 proposal in i1 and i2 | rc 1, `there is more than one work-item p1 under .shop/work` (the ambiguity r30 removes) |
| C2 `answer i2/p1` with p1 in both | rc 1, `no work-item i2/p1` |
| D1 bare `answer w1` (w1 awaiting, log says claimed, one initiative) | rc 0, prints `w1 ready` (the asked-from status, r14, works) |
| D2 `answer i1/w1` (same item as D1) | rc 1, `no work-item i1/w1` |
| E1 `answer i2/w2` (no such item) | rc 1, `no work-item i2/w2` |
| E2 `answer nosuch/w1` | rc 1, `no work-item nosuch/w1` |
| E3 `answer ../i1/w1` | rc 1, `no work-item ../i1/w1` (refused only by the `/` rule) |
| E4 `answer i1/` (empty name) | rc 1, `no work-item i1/` |
| E5 `answer /w1` | rc 1, `no work-item /w1` |
| E6 `answer i1/w1/extra` | rc 1, `no work-item i1/w1/extra` |
| F2 bare `answer w1` on a claimed w1 | rc 1, `w1 is not awaiting-answer; work answer answers only ...` |
| G1 bare `answer 'w*'` (w1 awaiting, one match) | rc 1, `.shop/work/i1/w*.md does not exist; there is no work-item w* to move` |
| G2 bare `answer '[w]1'` | rc 1, `.shop/work/i1/[w]1.md does not exist ...` |
| LINE_BREAKS (workqueue_answer.py) | codepoints 0xa 0xb 0xc 0xd 0x85 0x2028 0x2029 (run), so r15's set is complete |

Status after the probes: `git status --porcelain` empty; scratch is under ignored `.shop/scratch/`.

## 3. Old assumptions

The old form is a bare name: `find` (glob `*/<name>.md`) is the only resolver, and it refuses a `/` by design.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:find (222-227) | glob over every initiative; refuses any `/` name | r30 needs `i2/p1` to resolve. Changing `find` also changes `retry` and `withdraw`, which r8/r10 leave bare | by search: the two r30 scenarios (red); bare-name scenarios of work-queue.feature | grep `find(` |
| scripts/workqueue_answer.py:answer line 29 | `find(root, name)`, then `path.parent.name` as initiative | must split `<initiative>/<name>`, validate, then pass the bare name on | by search: r30 scenarios; bare `work answer w1` scenarios (work_queue_answer_steps.py) | grep `answer(` |
| scripts/workqueue_answer.py:answer lines 31-52 | `agrees`, `move`, `committed` and the log's `work-item` use `name` as file stem and log key | must receive the bare name; a prefixed name would make a path `.shop/work/i2/i2/p1.md` | by search: as above | read |
| scripts/workqueue_answer.py:asked_from (15-21) | filters log.jsonl by `work-item == name` | bare name still | by search: bare-name answer scenarios | read |
| scripts/work:cmd_answer line 50 | prints `"%s %s" % (args.name, status)` | prints `i2/p1 ready` for a prefixed name; the printed shape is not in r30 | none (grep found no assertion on the print of answer) | grep `cmd_answer` |
| scripts/workqueue.py:retry (204) and withdraw (232) | call `find` with a bare name | a `/`-accepting `find` would let `work retry i1/w1` pass silently; r8/r10 name bare | by search: retry/withdraw steps use bare names; none asserts a refusal for `/` | grep `find(` |
| scripts/supervise_answers.py:79, 110 | uses `asked_from` and `LINE_BREAKS`; moves by bare name, not `find` | not changed by a `find` change; do not route it through `find` | none found | grep `workqueue_answer` |
| scripts/workqueue_note.py:7 | imports `LINE_BREAKS` | none | by search: note scenarios | grep |
| README.md:141 | documents `work answer <work-item> <answer>` | text only, the form r30 adds is missing | none | grep `work answer` |
| spec/decisions/0064-answers-not-rulings.md:24 and spec/decisions/index.md:71 | state the command as `work answer <work-item> <answer>` | text only | none | grep `work answer` |

## 4. Tests the requirements make impossible to keep

`tools tests-of` refused (no map), so this is `by search`.

- Search for refusals of a `/` name or of "there is no work-item" in tests and features: no test asserts that `work answer`, `retry` or `withdraw` refuses `i<n>/<name>`. Verified by grep of tests/, features/ for `there is no work-item`, `more than one`, `work (withdraw|retry|answer) \S*/`: none.
- The two r30 scenario tests (tests/scenarios/test_work_queue.py) are red and are the target, not obstacles.
- The bare-name answer scenarios (features/work-queue.feature lines 275-321, tests/scenarios/work_queue_answer_steps.py) are kept by a bare-name path: they must stay green. Not run in this session (see below).
- Result: none that the requirement makes impossible, as far as search shows. Not run beyond the two r30 tests: `pytest.ini` runs `-m "not fixture"` and the file collects 2 of 67 scenarios (65 deselected; I did not trace which option deselects them). So "kept green" is unverified for the bare-name scenarios.

## 5. A step the work-item skips

The existing path for a name goes through `find`, which refuses path-shaped names (`/`, `..`, `.`, empty, `\`) and requires exactly one match. A `<initiative>/<name>` path skips both checks:

- The initiative part must pass `workqueue.entry(word, "initiative")` (scripts/workqueue.py:58-61), as `add` does for its initiative. Without it, `answer ../i1/w1` would reach `Path(root)/WORK/".."/...`. Today the `/` rule refuses it (probe E3). Marked `read`, not probed on the new path.
- The name part must pass `entry` too; a `/` in it (E6) must still be refused.
- The initiative must exist as a directory (`add` checks `directory.is_dir()`); today `find` gives `no work-item` (probe E2). Marked `read`.
- The one-match check is replaced by the file check in `agrees` (scripts/workqueue.py:190); keep the refusal text.

## 6. Defects

### D1 `work answer` takes a glob pattern as a name

Reproduction (run, probe_glob.py G1, G2): an initiative i1 with w1 `awaiting-answer` and log `claimed -> awaiting-answer`.
`python3 scripts/work --root <repo> answer 'w*' x` gives rc 1, `work: .shop/work/i1/w*.md does not exist; there is no work-item w* to move`.
`find` matched `i1/w1.md` by the glob, then `agrees` used the literal name `w*`. Nothing was written. Same for `[w]1`.
The refusal is correct, but its message says the file does not exist when a glob matched one. The name is not validated as a plain name. Reported only; not judged.

## 7. The file set

Files the change must touch (all `read`, with the probes above):

- `scripts/workqueue_answer.py` (53 lines, room 247): `answer` splits `<initiative>/<name>`, validates the initiative and the name with `workqueue.entry`, resolves the file in that initiative, and passes the bare name on (r30).
- `scripts/workqueue.py` (290 lines, room 10): only if `find` itself takes the prefix; the room is 10 lines, so a change here must be small or move the split to `workqueue_answer.py`. `retry` and `withdraw` (lines 204, 232) would then accept `/` names unless `find` stays bare. Prefer the split in `workqueue_answer.py`.
- `scripts/work` (151 lines, room 149): `cmd_answer` prints `args.name`; change only if the printed name is to be bare. Optional.

Modules on the change path, edited or not:

- `scripts/workqueue.py` 290 lines, room 10 (loaded by `workqueue_answer.py`).
- `scripts/model` 139 lines, room 161 (read by `workqueue.py` for frontmatter; not changed).
- `scripts/workqueue_answer.py` 53 lines, room 247.
- `scripts/work` 151 lines, room 149.
- `tests/scenarios/work_queue_answer_steps.py` 41 lines, room 259 (not changed; the bare-name When is kept).
- `tests/scenarios/test_work_queue.py` 288 lines, room 12 (not changed; the r30 scenarios are bound there, and it is near its limit).

Size limit: CLAUDE.md gives 300 lines (`scripts/tools size --limit 300`).

Not run here: `tools size`, `tools check`, the bare-name answer scenarios (deselected by pytest.ini, see section 4).
