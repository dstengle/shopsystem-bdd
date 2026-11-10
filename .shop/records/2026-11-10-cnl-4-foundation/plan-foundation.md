# CNL 4 foundation (b198, b145, b199, b151) Implementation Plan

> **For agentic workers:** carried out as CLAUDE.md says a plan is: **one fresh agent implements every task in order
> on one branch, then one fresh reviewer reviews the whole branch.** Not an implementer and a reviewer per task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** four backlog items on one branch, `plan-cnl4-foundation`, in this order: b198 (the batch test run imports
the tree's `spec_read`), b145 (one refusal path, CNL 4's I14b), b199 (`model check`'s v_t13 on a codified-2 index)
and b151 (this repository's glossary in 4.0, CNL 4's I20), so the rewords b152-b159 can recodify one capability at a
time.

**Architecture:** b198, b145 and b199 are small code fixes, each with its test first. b151 starts with two code fixes
the switch needs (found by a probe of this plan, below), then edits `spec/index.md` and the capabilities' `## Terms`
in steps, each kept green by the same gate. No requirement line is added, changed or retired.

**Tech stack:** Python 3 (standard library), pytest with xdist, GF 3.12 with pgf, clingo. The project's own commands
`scripts/model`, `scripts/features`, `scripts/tools`, `scripts/work`.

**Spec:** `.shop/records/2026-11-09-cnl-4/design.md` (sections 5, 9, 10.3 I14b and I20, 11, 13 points 2 and 8, 14),
and the items' notes in `.shop/backlog/b198.md`, `b145.md`, `b199.md`, `b151.md`. Phase 3's vocabulary share,
`.shop/records/2026-11-08-cnl-research-phase-3/terms.md`, for b151's senses and dead terms. The items name
`plan-i14b.md` and `plan-i20.md`; the session carried the four as this one plan instead.

## Global Constraints

- main's checkout is the reference. Never read leftover worktrees under `.shop/worktrees/` to learn the code; do not
  read other repositories.
- Every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300` exits 0).
- A new module gets a row in CLAUDE.md's module map; a module whose concern changes gets its row rewritten, in the
  same task.
- **No requirement line is added, edited or retired** by this plan. Term entries, relation rows and `language:` /
  `imports:` frontmatter are not requirement lines. If a task seems to need a line changed, stop (below).
- A design-decision is written by `work decision`, never by hand. A record by `work record` (its supporting files by
  hand).
- Push with the wrapper the session gives (it unsets `GH_TOKEN` and uses gh's credential helper), e.g.
  `<wrapper> git push -u origin plan-cnl4-foundation`; run gh as `env -u GH_TOKEN gh ...`.
- Commit messages cite the item: a line `Item: b198` (b145, b199, b151) as the message's last paragraph, and end with
  the session's attribution lines.
- The items' statuses are not changed by this plan; the main session closes them after the merge.

## The gate

Every task ends with the whole gate green. It is what "keep the whole suite and `model check` passing" means here.

| # | Command (from the branch's checkout) | Passes when |
|---|---|---|
| G1 | `python3 -m pytest -q` | no failure and no error (xfails and skips as on main) |
| G2 | `python3 scripts/model check` | its last line starts `0 violations` |
| G3 | `python3 scripts/features generate --check` | exit 0: every feature file byte-identical |
| G4 | `python3 scripts/features vocab --check` | prints `every step has one handler` |
| G5 | `python3 scripts/tools size --limit 300` | exit 0 |
| G6 | `python3 scripts/tools check <each .py file the task changed>` | ruff and vulture print `clean` |
| G7 | `python3 scripts/model logic --json > $SCRATCH/logic-<task>.json` then `diff $SCRATCH/logic-base.json $SCRATCH/logic-<task>.json` | no difference (tasks 4-9 only; tasks 1-3 do not touch the logic) |
| G8 | `python3 scripts/model decisions --check` | the same three `failing` lines as on main (0086, 0087, 0088: their `enforced_by` names `tests/scenarios/vocab.py`, which collects no test, exit 5) and every other decision `holds` |

`$SCRATCH` is the executing agent's scratchpad directory.

## When a task proves bigger than expected

Stop and report; do not improvise. Concretely, stop when any of these holds, commit nothing more, push what is
committed, and reply with the task, the command, its output's last 30 lines and what you would need decided:

- a gate command fails and the fix is not inside the files the task lists;
- a fix would change a requirement line, a feature file by hand, a handler's behaviour, or `grammar/*.gf`;
- G7 shows a difference the task does not predict;
- a file would go over 300 lines and the split is not the obvious one named in the task;
- in b151 (tasks 4-9), more than the bound a task names is affected.

## The probe (done while writing this plan, on a copy of main at 9e6506ba)

Setting `spec/index.md` to `language: codified-2` and `imports: [cli]` and nothing else gave:

- `model check`: 12 violations: v_t16 on `change`, `command`, `reason`, `refuse`, `tool` (spec/index.md), `name`
  (role-boundaries) and `output` (supervision); v_p1 on U4, U5, U7, U8 and U11, because a universal condition is read
  in the grammar `spec/index.md`'s marker names (`spec_language.four`, `spec_context._translate`), though
  `spec/universal.md` says `language: codified-1` itself.
- `model logic` and `features generate`: a traceback, `ValueError: no translation of the clause c_present_2_Is`
  (spec_facts_np.decode). With a codified-2 index, `spec_context._vocab` gives the codified-1 lines the layered
  lexicon's Vocab, whose condition funs are numbered differently (`c_present_2` ...) from the old grammar's; 23
  codified-1 lines that use a condition word with two entries fail this way.
- The test suite: errors at the first `live_logic` test, the same traceback.

Tasks 4 and 5 fix the two causes; task 6 then makes the switch.

## Review Focus

1. **Import order of the refusal base.** `shop_files` loads `scripts/model` at import, which imports
   `model_decisions` -> `tools_env` -> `tools_grammar`. If those import `shop_files`, the cycle fails on whichever is
   imported first. Task 2 puts the base in a module that imports nothing of the project and tests each importer
   imported alone in a fresh interpreter.
2. **A refusal raised under another tool's catch.** Today `tools` catches only `tools_env.Refused`, so
   `tools_grammar.Refused` ends in a traceback; `measure` catches only `transcripts.Refused`, so a `shop_files.Refused`
   from `measure_cost` or `measure_defect` does too; `work quote` (conversation_quote) catches nothing of
   `transcripts`. Task 2 makes each CLI catch the base and tests a refusal of another module's class under each.
3. **The batch test run with a stale plugin.** `work batch done` runs the suite with the plugin's scripts on
   PYTHONPATH; a tree whose `spec_read` differs must have its own used. Task 1's test puts a decoy `spec_read` in the
   plugin's place.
4. **A codified-1 line's facts under a codified-2 index.** Tasks 5 and 6 must leave every codified-1 line's facts and
   every finding unchanged (G7), not only "no traceback".
5. **Senses and the old grammar's first sense.** The old grammar reads a verb's first frame of its first sense, and
   `spec/index.md`'s entries come before the capabilities'. A sense added in the index ahead of a capability's entry of
   the same word changes what every codified-1 line with that word parses to. Task 9 adds a sense only when G1-G7 stay
   green and drops it otherwise.

---

### Task 0: Branch and baseline

- [ ] **Step 1:** `git -C /home/vscode/shopsystem-bdd switch -c plan-cnl4-foundation main`
- [ ] **Step 2:** run G1-G6 and G8 on the fresh branch; every one must pass as the table says. Save
      `python3 scripts/model logic --json > $SCRATCH/logic-base.json` and the last line of G2 (`0 violations, <n>
      warnings, ...`) for later comparison. If anything fails on main, stop and report.

### Task 1: b198, `work_items` imports `spec_unbuilt` only when it marks

**Files:**
- Modify: `scripts/work_items.py` (the `import spec_unbuilt` moves from the top into `pytest_collection_modifyitems`;
  the docstring says why)
- Modify: `conftest.py` (its comment above the `sys.path` lines: the plugin is loaded by `-p work_items` before this
  file runs, so `work_items` imports the spec modules only at collection, after this file has put the tree's scripts
  first)
- Test: `tests/scripts/test_work_items.py`
- Modify: CLAUDE.md, the `scripts/work_items.py` row (add: "its spec modules imported at collection, after a tree's
  conftest has put the tree's scripts first (b198)")

**Interfaces:** Produces nothing others use. `work_items.pytest_collection_modifyitems(config, items)` keeps its
signature.

- [ ] **Step 1: Write the failing test** `test_a_tree_whose_conftest_puts_its_scripts_first_is_marked_by_its_own_spec_read`
      in `tests/scripts/test_work_items.py`:
  - `plugin = tmp_path / "plugin"`: a copy of every `*.py` of `SCRIPTS` (shutil.copy2 each), then
    `(plugin / "spec_read.py").write_text("raise ImportError('the plugin\\'s spec_read was imported')\n")`.
  - `tree = tmp_path / "tree"`: `tree/scripts/` a copy of every `*.py` of `SCRIPTS`; `tree/conftest.py`:
    ```python
    import pathlib, sys
    SCRIPTS = str(pathlib.Path(__file__).parent / "scripts")
    if SCRIPTS in sys.path:
        sys.path.remove(SCRIPTS)
    sys.path.insert(0, SCRIPTS)
    ```
    and `tree/tests/test_one.py` with `def test_one(): import spec_read; assert "tree" in spec_read.__file__`.
  - Run `python3 -m pytest -q -p no:cacheprovider -p work_items` in `tree` with `PYTHONPATH=str(plugin)`
    (`PYTEST_PLUGINS`, `PYTEST_ADDOPTS` removed from the environment, as `pytest()` there does).
  - Assert `returncode == 0` and `"1 passed" in stdout`.
- [ ] **Step 2:** `python3 -m pytest tests/scripts/test_work_items.py -q -n 0` — the new test FAILS (an ImportError
      naming "the plugin's spec_read" while loading `work_items`); the old tests pass.
- [ ] **Step 3:** move the import into the hook in `scripts/work_items.py`; `spec_root` unchanged.
- [ ] **Step 4:** the same command: all pass.
- [ ] **Step 5:** gate G1-G6, G8. Commit `work_items.py`, `conftest.py`, the test and CLAUDE.md:
      `work_items: the spec modules imported at collection, after a tree's conftest (b198)` with `Item: b198`.

### Task 2: b145, one refusal path

**Files:**
- Create: `scripts/shop_refused.py` (standard library only, imports nothing of the project): `class
  Refused(Exception)` with the docstring of today's `shop_files.Refused` ("What was asked cannot be done; the message
  says why, and nothing was changed.") and a module docstring naming the decision.
- Modify: `scripts/shop_files.py`: `from shop_refused import Refused  # noqa: F401` in place of its class, above
  `_load_model()`; `shop_files.Refused is shop_refused.Refused`.
- Modify: `scripts/tools_env.py`, `scripts/tools_grammar.py`, `scripts/features_gherkin.py`, `scripts/transcripts.py`:
  each `class Refused(shop_refused.Refused)` (keeps its name and docstring, so every `raise Refused(...)` and every
  `except <module>.Refused` stays as it is). Their docstrings' "Standard library only" become "Standard library and
  shop_refused".
- Modify the CLIs' one catch each, to the base: `scripts/tools` (`except shop_refused.Refused`), `scripts/features`,
  `scripts/measure` (`from shop_refused import Refused` in place of `from transcripts import Refused`), `scripts/work`
  (unchanged: `shop_files.Refused` is the base). Each keeps its message form (`tools: <reason>`, `features: <reason>`,
  `measure <command>: <reason>`, `work: <reason>`) and exit 1. `scripts/model` and `scripts/migrate` are out of scope
  (design 13 point 8: one task, not a sweep).
- Test: `tests/scripts/test_refusal_path.py` (new)
- Modify: CLAUDE.md: a row for `scripts/shop_refused.py` ("the one refusal (b145, design-decision one-refusal-path):
  `Refused`, the base every command's refusal reaches, standard library only so that any module can import it");
  the `scripts/shop_files.py` row's `Refused` becomes "`Refused` (shop_refused's, re-exported)".
- Decision: `spec/decisions/<next>-one-refusal-path.md` and the index, written by `work decision` (Step 6).

**Interfaces:**
- Produces: `shop_refused.Refused(Exception)`; `shop_files.Refused`, `tools_env.Refused`, `tools_grammar.Refused`,
  `features_gherkin.Refused`, `transcripts.Refused`, `batch_git.GitFailed` all subclasses of it (the first the class
  itself).

- [ ] **Step 1: Write the failing tests** in `tests/scripts/test_refusal_path.py` (SCRIPTS on `sys.path` as the other
      script tests do):
  - `test_every_refusal_class_reaches_the_one_base`: for each of `shop_files.Refused`, `tools_env.Refused`,
    `tools_grammar.Refused`, `features_gherkin.Refused`, `transcripts.Refused`, `batch_git.GitFailed`:
    `assert issubclass(cls, shop_refused.Refused)`; and `assert shop_files.Refused is shop_refused.Refused`.
  - `test_each_importer_imports_alone` parametrized over `shop_files`, `tools_env`, `tools_grammar`,
    `features_gherkin`, `transcripts`, `shop_refused`: `subprocess.run([sys.executable, "-I", "-c", "import sys;
    sys.path.insert(0, %r); import %s" % (SCRIPTS, name)])` returns 0 (Review Focus 1).
  - `test_a_refused_command_exits_1_naming_the_reason_and_changes_nothing`, parametrized over four cases, each run in
    a fresh git repository in `tmp_path` (one empty commit, user name and email set with `-c`), recording
    `git rev-parse HEAD` and `git status --porcelain --untracked-files=all` before and after:
    | tool | argv | stderr holds |
    |---|---|---|
    | work | `scripts/work show b9` | `work: there is no item b9` |
    | tools | `scripts/tools --python /nonexistent/python probe` | `tools: no analysis tools are known` |
    | features | `scripts/features count --by-tag` with `features/a.feature` = `Feature: a\n  Rule: r\n` written and committed first | `features: ` and `Rule: blocks are not supported` |
    | measure | `scripts/measure show nothing` | `measure show: no measurement at nothing` |
    Assert returncode 1, the stderr text, no `Traceback` in stderr, HEAD and status unchanged.
  - `test_a_refusal_of_another_modules_class_is_caught_by_each_tool` (Review Focus 2): for `tools`, `features` and
    `measure`, load the script with `importlib.machinery.SourceFileLoader`, monkeypatch the function its main
    dispatches to (`tools`: the parsed `args.run`, via monkeypatching `tools_size.cmd_size` and calling main with
    argv `["size"]`; `features`: `cmd_count`; `measure`: `COMMANDS["show"]`) to raise `tools_grammar.Refused("x")`,
    `shop_files.Refused("x")` and `transcripts.Refused("x")` in turn; assert main returns 1 and stderr (capsys) ends
    with `: x\n`. Set `sys.argv` where the script's main reads it rather than taking `argv`.
- [ ] **Step 2:** `python3 -m pytest tests/scripts/test_refusal_path.py -q -n 0` — FAIL: `shop_refused` does not exist.
- [ ] **Step 3:** implement as Files says.
- [ ] **Step 4:** the same command: all pass. Then
      `python3 -m pytest tests/scripts/test_tools.py tests/scripts/test_features.py tests/scripts/test_measure_show_old.py tests/scripts/test_conversation_quote.py -q`: pass.
- [ ] **Step 5:** gate G1-G6. Commit code, test and CLAUDE.md: `One refusal path: every Refused a subclass of
      shop_refused.Refused, caught once by each tool (b145)` with `Item: b145`.
- [ ] **Step 6: the decision.** Write the decision text to `$SCRATCH/refusal-decision.md`:
      > Every refusal of every command is a `shop_refused.Refused` (re-exported as `shop_files.Refused`): the four
      > other `Refused` classes (`tools_env`, `tools_grammar`, `features_gherkin`, `transcripts`) and
      > `batch_git.GitFailed` are its subclasses, and each tool (`work`, `tools`, `features`, `measure`) catches the
      > base once, prints `<tool>: <reason>` and exits 1. A refusal is raised before anything is written, or what was
      > written is put back (U11). The path is tested once, by tests/scripts/test_refusal_path.py; after every
      > generated scenario tests/scenarios/vocab.py checks that a refused run changed nothing (decision 0088). No
      > scenario states U11 again.
      Then run:
      ```
      python3 scripts/work decision "One refusal path" --tier check \
        --summary "Every refusal of every command reaches one base exception, shop_refused.Refused, and leaves through one catch a tool that exits 1 naming the reason and changes nothing." \
        --decision @$SCRATCH/refusal-decision.md \
        --context "CNL 4's I14b (design 10.3, 13 point 8): five Refused classes, each tool catching only its own; an entailed consequence guaranteed by one code path and tested once (b112, b125)." \
        --enforced-by tests/scripts/test_refusal_path.py::test_every_refusal_class_reaches_the_one_base \
        --enforced-by tests/scripts/test_refusal_path.py::test_a_refused_command_exits_1_naming_the_reason_and_changes_nothing \
        --verified-by check --rests-on U11 \
        --by "the plan for b145, 2026-11-10"
      ```
      It writes, commits and pushes the decision and the index (on this branch). Then G2 and G8: the new decision
      `holds`. If `work decision` refuses `--rests-on U11` in that spelling, use the one decision 0088 shows
      (`rests_on: [U11]`) — it is that one.

### Task 3: b199, the old lexicon reader sees grammar 4's base kinds and the imported packs

**Files:**
- Modify: `scripts/spec_rgl_vocab.py`: `outer(root) -> frozenset[str]`: when `spec_grammar4.marked(root)`, the keys of
  `BASE_KINDS` and the term of every kind and actor (category `kind`, `actor`) of each pack `spec_packs.imports(root)`
  names (read with `spec_packs.path_of` and `spec_packs.terms`); else `frozenset()`.
- Modify: `scripts/spec_frames.py`: `names(lexicon, outer=frozenset())` returns today's set `| outer`;
  `problems(lexicon, outer=frozenset())` passes `outer` to `names`, and to the kinds its v_t4 of an actor's `Kind of:`
  checks against.
- Modify: `scripts/spec_lexicon.py`: `problems(lexicon, outer=frozenset())` passes it to `spec_frames.problems`.
- Modify the callers to pass `spec_rgl_vocab.outer(root)`: `scripts/model_spec.py` (`read_lexicon`: `known =
  spec_frames.names(lexicon, outer)`; `overlapping` unchanged), `scripts/model_report.py:163`,
  `scripts/model_rules.py:67`, `scripts/readiness_bar.py:129,134` (the copy's root),
  `scripts/migrate_upgrade_frames.py:44`.
- Test: `tests/scripts/test_spec_packs.py` (add), `tests/scripts/test_model_spec_terms.py` (add)
- Modify: CLAUDE.md rows of `spec_rgl_vocab.py` (add "`outer`, the base kinds and the imported packs' kinds and actors
  that the old lexicon reader's frames may name in a codified-2 context (b199)") and `spec_frames.py` (`names` with
  `outer`).

**Interfaces:**
- Produces: `spec_rgl_vocab.outer(root) -> frozenset[str]`; `spec_frames.names(lexicon, outer=frozenset())`;
  `spec_lexicon.problems(lexicon, outer=frozenset())`.

- [ ] **Step 1: Write the failing tests:**
  - in `test_spec_packs.py`: `test_outer_names_the_base_kinds_and_the_cli_packs_kinds` —
    `spec_rgl_vocab.outer(FIXTURES / "codified-2")` contains `thing`, `agent`, `tool`, `command`, `option`, `reason`,
    `output`; `outer(FIXTURES / "glossary")` (its index says codified-1) is empty.
  - in `test_model_spec_terms.py`: `test_a_codified_2_index_has_no_v_t13_for_a_frame_naming_agent` — copy
    `tests/scripts/fixtures/codified-2` to `tmp_path`, run `scripts/model check` there; stdout has no `v_t13` and
    its last line starts `0 violations`. And `test_a_codified_1_index_still_reads_agent_as_unknown` — the same copy
    with `language: codified-2` replaced by `language: codified-1` and the `imports:` line removed: stdout has `v_t13`
    naming `write`.
- [ ] **Step 2:** run both files with `-n 0`: the new tests FAIL (4 v_t13 today, as the item says).
- [ ] **Step 3:** implement as Files says.
- [ ] **Step 4:** pass.
- [ ] **Step 5:** gate G1-G6, G8. Commit: `model check over a codified-2 index: frames may name grammar 4's base kinds
      and the imported packs' (b199)` with `Item: b199`.

### Task 4: b151 (1/6), a universal condition read in `spec/universal.md`'s own grammar

**Files:**
- Modify: `scripts/spec_language.py`: `four(root, capability=None, universal=False)`: with `universal`, true when
  `spec/universal.md` says `language: codified-2` (`spec_read.codified(path, (spec_read.MARKER4,))`), whatever the
  index says; a line of no capability and not universal keeps the index's marker (`model parse` alone).
- Modify: `scripts/spec_context.py` `_translate`: a universal condition goes to `four.facts` only when
  `spec_language.four(root, universal=True)`; otherwise through `spec_grammar.parse` as a codified-1 line.
- Modify: every other caller that parses universal conditions by the index's marker — find them with
  `grep -n "universal" scripts/model_spec.py scripts/model_check.py scripts/readiness_bar.py scripts/features_generate.py scripts/spec_steps*.py`
  — to pass `universal=True`. If more than three callers need it, stop and report.
- Test: `tests/scripts/test_spec_language.py` (new, or the existing test file of spec_language if one exists:
  `grep -ln spec_language tests/scripts/`)
- Fixture: `tests/scripts/fixtures/mixed-index/spec/` — `index.md` a copy of `tests/scripts/fixtures/codified-2`'s
  plus `universal.md` with `language: codified-1` and one condition of today's grammar using the fixture's own words,
  and one capability `capabilities/shelf.md` with `language: codified-1` and one group (copy the shape of an existing
  codified-1 fixture capability under `tests/scripts/fixtures/entailment/spec/capabilities/`). Its words must parse in the old
  grammar over that glossary; check with `python3 scripts/model parse --capability shelf "<line>"` from the fixture.
- Modify: CLAUDE.md rows of `spec_language.py` and `spec_context.py` ("a universal condition in `spec/universal.md`'s
  own marker").

**Interfaces:** Produces `spec_language.four(root, capability=None, universal=False) -> bool`.

- [ ] **Step 1: failing tests:** `test_a_universal_condition_is_read_in_its_own_files_grammar`:
      `spec_language.four(MIXED, universal=True) is False` and `spec_language.four(MIXED) is True`;
      `test_a_codified_2_index_loads_a_codified_1_universal_condition`: `spec_context.load(MIXED).refused == {}`.
- [ ] **Step 2:** FAIL (the condition is parsed in grammar 4).
- [ ] **Step 3:** implement.
- [ ] **Step 4:** pass; then gate G1-G8 (G7 identical: the live index still says codified-1).
- [ ] **Step 5:** commit with `Item: b151`.

### Task 5: b151 (2/6), codified-1 lines translated with the old vocabulary under a codified-2 index

**Files:**
- Modify: `scripts/spec_context.py`: `_vocab(root, four)` returns two Vocabs when `four.marked`: the layered one
  (as today: `spec_logic_vocab.Vocab(spec_rgl_vocab.lexicon(root), spec_rgl_vocab.read(root).kinds)`) and the old one
  (`spec_logic_vocab.Vocab(spec_lexicon.read(root))` with `_define` run on it); when not marked, the old one twice.
  `_translate` translates every codified-1 line (and a codified-1 universal condition) with the old one; `domain` is
  `spec_logic_vocab.domain(<layered>) + spec_facts.def_facts(<old>)`; `Context.vocab` stays the layered one when
  marked (what `model_explain`, `spec_entail` and `features_generate4` read today). If the file passes 300 lines, move
  `_Four` and `_vocab` to `scripts/spec_context_four.py` (a module map row).
- Test: in the Task 4 test file, using the `mixed-index` fixture with a condition word given two entries (e.g.
  `open (adjective of stage)` and `open (adjective of file)`) and the capability's line using the second:
  `test_a_codified_1_lines_facts_do_not_depend_on_the_index_marker`: `spec_context.load(MIXED).facts[<id>]` equals the
  facts of a `tmp_path` copy whose `index.md` says `codified-1` (imports line removed).

**Interfaces:** `spec_context.load(root, extra=())` unchanged.

- [ ] **Step 1:** the failing test; **Step 2:** it fails with `no translation of the clause c_open_2_Is` (or the
      fixture's word); **Step 3:** implement; **Step 4:** pass.
- [ ] **Step 5: the live probe.** On a scratch copy of the branch (`git archive HEAD | tar -x -C $SCRATCH/probe`, a
      fresh `git init` and commit there), set `spec/index.md` to `language: codified-2` plus `imports: [cli]`. Then
      in the probe: `python3 scripts/model logic --json > $SCRATCH/logic-probe.json`; `diff` against
      `$SCRATCH/logic-base.json` must show no difference, and `python3 scripts/features generate --check` must exit 0.
      If either does not hold, stop and report (the difference and the lines it names).
- [ ] **Step 6:** gate G1-G8 on the branch; commit with `Item: b151`.

### Task 6: b151 (3/6), the switch: `spec/index.md` codified-2 with the CLI pack

**Files:**
- Modify: `spec/index.md` frontmatter: `language: codified-2` and a line `imports: [cli]` after it. (Not `time`: no
  line of this repository uses the time pack's words yet; the reword that needs them adds it. If the gate shows a
  line needs it, add `time` and say so in the report.)
- Modify: the seven entries v_t16 names, each by adding `Redefines: cli.` at the end of its entry text (they stay:
  the old pipeline reads no pack, and codified-1 lines use them): `change`, `command`, `reason`, `refuse`, `tool` in
  `spec/index.md`; `name` in `spec/capabilities/role-boundaries.md`; `output` in `spec/capabilities/supervision.md`.
  Each one's removal, once no codified-1 line uses it, belongs to the reword that frees it or to I28: file one idea,
  `python3 scripts/work idea "The glossary's copies of the CLI pack's words removed once no codified-1 line uses them"`
  with a note naming the seven, in this task.
- Modify: the prose in `spec/index.md`'s opening paragraph that says what the glossary is (one sentence: the index
  says codified-2 and imports the CLI pack; codified-1 capabilities keep parsing through the old pipeline over it).

- [ ] **Step 1:** make the edits.
- [ ] **Step 2:** gate G1-G8. G2's warning count may move only by `w_example`; any new violation code, stop.
- [ ] **Step 3: `model parse` alone now reads grammar 4.** `grep -rn "model parse" skills/ agents/ tests/scenarios/`:
      where a skill tells a session to check a line of a codified-1 capability with `model parse "<line>"`, that now
      needs `--capability <cap>`. Do not edit the skills here (I30, the authoring skills, is their plan); file one
      `work idea "Skills: model parse --capability for a line of a codified-1 capability"` naming the places, unless
      such an idea already exists (`python3 scripts/work backlog`).
- [ ] **Step 4:** commit `spec/index.md`, the two capability files: `spec/index.md: codified-2 with the CLI pack
      imported; the glossary's copies of the pack's words marked Redefines: cli (b151)` with `Item: b151`.

### Task 7: b151 (4/6), relation rows to one reading of a blank cardinality

**Files:** `spec/index.md` `## Relations` (and any capability's `## Relations` table).

- [ ] **Step 1: explicit `one`.** For every row with a blank cardinality whose word `spec_logic_vocab.functional(row)`
      reads as functional (the word in `spec_logic_vocab.PREPOSITIONS`), write `one` in its cardinality cell. The old
      check reads them the same; grammar 4's check (blank = any number, call 14) then reads them as the old one did.
      List them with a one-off script in `$SCRATCH` (not committed) over `spec_relations.read(".")`.
- [ ] **Step 2: rows whose word is a verb or a noun.** Rows whose word is `adds`, `changes`, `removes`, `deletes`
      (proposal and commit rows) and the noun rows `asker`, `upstream`: remove each that no live requirement uses
      (a row is used when a fun of it, `spec_logic_vocab.Vocab(...).rels`, appears in a tree of
      `spec_context.load(".").statements`, or a condition's definition names it); keep each one used and list it in
      the report. Unused rows inherited from 1.x (`file | of | initiative`, `file | changed by | work-item`,
      `file | outside | file set`, `stage | needs | resource`, and like rows of kinds no line uses) go the same way.
- [ ] **Step 3:** gate G1-G8 (G7 identical). If a removed row breaks a definition or a handler, put it back and list
      it.
- [ ] **Step 4:** commit with `Item: b151`.

### Task 8: b151 (5/6), dead terms and unneeded prose conditions removed

A term is **live** when any of these uses it: a tree of a live requirement or universal condition
(`spec_context.load(".")`: each statement's funs decoded by `ctx.vocab.decode`, plus the old Vocab's for codified-1
lines), a relation row kept by Task 7, another live term's `Frame:`, `Kind of:`, `This:` or definition, a group's given
block, a step handler key under `tests/scenarios/` (`features vocab --check` sees it), or a pack's `Redefines:`
target. Every other term in `spec/index.md`'s `## Glossary` and in each capability's `## Terms` is dead (phase 3
counted 66 adjectives, 94 of 166 kinds, 18 of 43 verbs and all 9 resources as unused).

- [ ] **Step 1:** compute the dead set with a one-off script in `$SCRATCH` (not committed); save its list to
      `$SCRATCH/dead.txt`, grouped by file.
- [ ] **Step 2:** remove the dead entries from their files, in one pass. A prose-defined condition that is live stays
      (its replacement is the reword's, call 13); one that is dead goes with the rest (b10, withdrawn, folds in here).
- [ ] **Step 3:** gate G1-G8. On a failure, put back the entries the failure names (a refusal's word, a handler's
      key) and run the gate again; if more than 10 entries come back this way, or G7 differs, stop and report.
- [ ] **Step 4:** commit with `Item: b151`; the message gives the counts removed by category.

### Task 9: b151 (6/6), `This:` and the senses the rewords need

**Files:** `spec/index.md` `## Glossary`; `spec/capabilities/migration-tools.md` (`repository`).

- [ ] **Step 1: `This:`.** Add to the end of the entry text:
  - `bounded context`: `This: the bounded context whose repository the command runs in.`
  - `session`: `This: the session that runs the command.`
  - `repository` (in migration-tools' `## Terms`, where it stands): `This: the repository the command runs in.`
- [ ] **Step 2: the senses** (design I20, phase 3's SENSE: name, list, use, hold, include, keep against record). Add
      each entry below at the end of `spec/index.md`'s `## Glossary`, one at a time, running G2, G3 and G7 after each;
      keep it when they stay green, and remove it and list it in the report otherwise (Review Focus 5). Do not change
      an existing entry's frame.
  - `- **name** (verb, state): a text says which thing it means, as a scenario names a requirement. Forms: names, named. Frame: text names thing.`
  - `- **use** (verb, state): a text holds a word or a thing, as a requirement uses a term. Forms: uses, used. Frame: text uses thing.`
  - `- **list** (verb, state): a text holds each of some things, as a glossary lists a term. Forms: lists, listed. Frame: text lists thing.`
  - `- **record** (verb, action): an agent writes a thing into a file to keep it. Forms: records, recorded. Frame: agent records thing in file.`
  If `name`'s new sense is refused by v_t15 against role-boundaries' `name` or the CLI pack's, drop it and list it.
  `hold` and `include` are left to the rewords that need them (requests, batch-measurement): their subjects are those
  shares' kinds.
- [ ] **Step 3:** gate G1-G8.
- [ ] **Step 4:** commit with `Item: b151`.

### Task 10: CLAUDE.md, the report, the branch

- [ ] **Step 1:** check CLAUDE.md's module map against the branch's diff (`git diff main --stat -- scripts/`): every
      new module has a row, every changed concern its row rewritten.
- [ ] **Step 2: the report.** Write `$SCRATCH/foundation-report.md`: per task what was done; Task 6's seven
      entries; Task 7's rows made `one`, removed and kept (each kept one with the line that uses it); Task 8's counts
      by category and the entries put back with why; Task 9's senses kept and dropped. Then
      `python3 scripts/work record "CNL 4 foundation: what the plan did" --kind analysis --summary "b198, b145, b199 and b151 carried by plan-foundation: the refusal base, the codified-2 index over codified-1 capabilities, and the glossary's rows, dead terms and senses" --body $SCRATCH/foundation-report.md`.
- [ ] **Step 3:** the whole gate G1-G8 once more; then `<wrapper> git push -u origin plan-cnl4-foundation`.
- [ ] **Step 4:** reply with the branch, its head, the gate's results and the report's path. The main session then
      dispatches one fresh reviewer of the whole branch (`git diff main...plan-cnl4-foundation`) with this plan and the
      design.
