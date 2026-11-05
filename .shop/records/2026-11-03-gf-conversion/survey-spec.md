# Survey: today's spec, feature files and step definitions, before the GF conversion

Date 2026-11-03, branch `gf-conversion` at 96818f71. Read-only survey; no code changed. Input: `brief.md` beside this file.

## 1. Sizes

### spec/

- `spec/index.md` 148 lines: context frontmatter, Purpose, Constraints (still says design model v3, l.27), Composition
  (19 capabilities in four tables with narrator and group, l.38-77), Testing (l.79-91), Glossary of 51 terms
  (`- **term**: definition. Not: forbidden words.`, l.93-143), Where things live.
- `spec/decisions/`: 72 decision files `0001-...` to `00xx-...` plus a generated `index.md` (`model decisions`).
- `spec/capabilities/`: 19 files, 1323 lines, **581 requirement ids** live, 196 retired.

| capability | group | lines | reqs live | of them table rows | retired | feature | scenarios (outlines) | step lines / unique |
|---|---|---|---|---|---|---|---|---|
| analysis-tools | service | 81 | 24 | 0 | 21 | yes | 45 (10) | 211 / 158 |
| batch-measurement | service | 80 | 29 | 0 | 38 | yes | 29 (4) | 152 / 103 |
| code-research | guarantees | 38 | 10 | 0 | 2 | - | - | - |
| delivery | guarantees | 40 | 14 | 0 | 8 | - | - | - |
| design-model-check | service | 127 | 66 | 39 | 23 | yes | 87 (28) | 345 / 235 |
| feature-file-tools | service | 84 | 28 | 0 | 34 | yes | 49 (17) | 243 / 189 |
| formulation | guarantees | 48 | 14 | 0 | 2 | - | - | - |
| migration-tools | service | 72 | 33 | 0 | 0 | yes | 54 (13) | 270 / 195 |
| planning | guarantees | 33 | 8 | 0 | 0 | - | - | - |
| red-green | guarantees | 47 | 13 | 0 | 7 | - | - | - |
| requests | service | 90 | 48 | 0 | 10 | yes | 49 (15) | 253 / 156 |
| review | guarantees | 52 | 20 | 0 | 1 | - | - | - |
| role-boundaries | guarantees | 34 | 7 | 0 | 0 | - | - | - |
| spec-consistency | guarantees | 55 | 18 | 0 | 1 | yes | 16 (5) | 88 / 79 |
| spec-integration | guarantees | 63 | 26 | 0 | 13 | yes | 5 (0) | 37 / 36 |
| spec-migration | guarantees | 56 | 21 | 0 | 3 | - | - | - |
| supervision | service | 224 | 164 | 0 | 23 | yes | 193 (43) | 1049 / 539 |
| trials | guarantees | 29 | 5 | 0 | 0 | - | - | - |
| work-queue | service | 70 | 33 | 0 | 10 | yes | 48 (12) | 277 / 182 |
| **total** | | 1323 | **581** | 39 | 196 | 10 files, 6337 lines | **575 (147)** | 2925 / 1872 |

Supervision alone is 28% of the requirements, a third of the feature lines (2131) and 34 of the 95 step modules.
Guarantees capabilities: 11 (226 reqs); 9 have no feature file. Service capabilities: 8 (355 reqs), all with features.

Tag coverage: every live id of a service capability has a scenario tag except requests (2 untagged), spec-consistency
(2) and spec-integration (21 untagged; guarantees). Multi-tag scenarios: 4 (design-model-check 2, feature-file-tools 2).
`@deprecated` scenarios: 43 (supervision 20, feature-file-tools 8, work-queue 7, design-model-check 6, requests 2).

### tests/

- `tests/scenarios/`: 95 modules, 13 312 lines. 9 `test_<capability>.py` binders, the rest `<capability>_*_steps.py`
  and world/given/then helpers. **1386 step definitions**: 633 `@given`, 53 `@when`, 700 `@then`; 345 use `parsers.re`,
  301 `parsers.parse`, the rest plain strings. `@when` is small because Whens are few and generic: "the session runs
  `work {args}`" (213 step lines), "the person runs" (195), "`model check` is run" (65).
- `tests/scripts/`: 36 modules, 3106 lines, `unittest`-style tests of scripts no scenario drives
  (`test_bound.py`, `test_model*.py`, `test_supervise_*.py`, `test_migrate_*.py`, `test_features*.py`, ...).

## 2. The format rules (docs/capability-format.md, 410 lines)

- Capability file: frontmatter `id, title, narrator, group, rests_on, retired`; sections Purpose, Behaviour,
  Implementation may change, Not yet (l.44-82; example `spec/capabilities/trials.md`).
- Behaviour: one EARS line each, `- [r<n>] **When** ..., the <system> shall ...` (l.84-128). Patterns ubiquitous /
  When / While / If..then / Where / complex in that clause order. One "shall", one sentence. `If` lines only for
  purpose, data safety or seen failures; a generic failure line per script ("cannot do what it was asked ... change
  nothing"). Exits in words. Response observable by the narrator. Verifier rules may be a table `| [r3] | ... |`
  led by a "shall" sentence (only design-model-check uses this: 39 rows).
- "Lines that leave nothing to infer" (l.130-152): five lessons; lifecycles written as ways in/out of each state;
  a depended-on word is a glossary term.
- Requirement ids (l.154-170): `[r<n>]` first; new id = one above every used or retired id; a changed line keeps its id
  (note: the memory note "retire, never edit" and the brief's decision 4 supersede this for the converted spec);
  removed ids go to `retired:`; qualified name `capability/<ctx>/<name>#r<n>`.
- Feature file (l.246-272): one feature per capability, header comment `# formulated from spec/capabilities/<c>.md`,
  `Narrator:` line; scenario tagged `@r<n>` (decision 0052 allows several, all of one capability, every requirement
  named by at least one scenario); Then says "exits successfully / with an error"; EARS-to-Gherkin table: Where/While
  -> Given, When -> When, If -> When with invalid input, response -> Then, ubiquitous -> property scenario or Background.
- `model check` enforces `v_e1` (not an EARS pattern) and `v_e2` (two shalls / two sentences) by regex
  (`scripts/model_parse.py`, `scripts/model.lp` 334 lines); the GF parse replaces both.

## 3. How features bind to steps and to requirement ids

- `pytest.ini`: `testpaths = tests`, `bdd_features_base_dir = features/`, `addopts = -n auto -m "not fixture"`.
- Root `conftest.py` (12 lines): puts `scripts/` on `sys.path`, loads `pytest_plugins = ["work_items"]`.
- `tests/scenarios/conftest.py`: fixtures `repo` (tmp_path), `context` (dict a When leaves for Thens), `run` (runs a
  script with `sys.executable`); `pytest_configure` registers marks `r1..r199` only (supervision has r221 -> 300+
  `PytestUnknownMarkWarning`s); shared constants `INDEX`, `full()`, `THING`, `P1`, `I1`.
- Binding is **whole-file**: each `test_<capability>.py` calls `scenarios("<capability>.feature")` once
  (e.g. `tests/scenarios/test_work_queue.py:33`) and star-imports its step modules. No per-title `@scenario` binding in
  the real suite (the three `@scenario(` hits are fixture text inside tests of `features bindings`). So **scenario
  titles are not load-bearing for binding**; only step texts are.
- `tests/scripts/test_bound.py` runs `features bindings --tests tests --unbound` on 7 feature files: each scenario bound
  by exactly one test (requests and spec-integration are not in its list).
- Requirement ids reach pytest as marks: pytest-bdd turns `@r7` into `pytest.mark.r7`. `scripts/work_items.py` (180
  lines) implements `--work-item w<n>`: reads the work-item's `accepts: [<cap>#r<n>, <cap>#r<n>-r<m>]`, selects
  scenarios of that feature with those marks, keeps non-scenario tests.
- Scripts that parse `[r<n>]`/`@r<n>`: `features_gherkin.py`, `model_parse.py` (Behaviour lines, `TABLE_ID` l.131),
  `supervise_drafts.py`, `supervise_brief.py`, `supervise_draft.py`, `migrate_spec.py`, `work_items.py`; and
  `migrate_upgrade_ids.py` (w<n> renaming, leaves `#r<n>` alone).
- `scripts/features` (148 lines + `features_gherkin` 175, `_edit` 131, `_bindings` 170, `_report` 116): count/list by
  tag, tag, move, deprecate, retire, deprecated, verify-moved, bindings/rebind. It edits hand-written Gherkin; with
  generated Gherkin, `tag`, `move`, `deprecate`, `retire`, `rebind` lose their purpose (the generator owns the file);
  `count`, `list`, `bindings --unbound` stay useful.
- `scripts/migrate*` (migrate 81, `_layout` 131, `_spec` 132, `_ledger` 123, `_write` 126, `_upgrade` 171,
  `_upgrade_ids` 128, `_upgrade_answers` 43, `_session` 54, `_prompt` 36): old system -> final layout, and plugin
  upgrade steps one module each. The GF conversion is naturally one more upgrade step (`0.30.0`/`1.0.0`).

## 4. The suite: how it runs, how long, what fails

`python3 -m pytest -q` from the root, Python 3.11 user site (pytest-bdd, xdist, coverage). xdist `-n auto` on 32 cores.

**Result at 96818f71: 1113 passed, 23 failed, 1 skipped, 56 subtests passed, 1084 warnings, 40.4 s (41 s wall).**
1137 collected tests (575 scenarios, outlines expanded, plus tests/scripts).

The 23 failures are not regressions: 22 are `StepDefinitionNotFoundError` (scenarios formulated, step definitions not
written: requests r50-r58 from commit 627b4a71, 19 tests; supervision 3), 1 is an `AssertionError` in
`requests_show_steps.py:56` (`work list` does not print whose turn a request is: a formulated, unimplemented line).
So "the suite is green" is not today's baseline; the conversion should either finish or drop those 23 (their lines
get fresh ids anyway).

Warnings: unregistered marks `r200+` and `deprecated`; pytest-bdd fixture-registration deprecations.

## 5. What converting all 19 capabilities entails for step definitions

1. **Requirements.** 581 free-English lines -> codified requirement groups that parse in the Ears grammar, fresh ids,
   `restates: [r..]` keeping the old ids. Many lines are long compound sentences (e.g. work-queue r36 `work show`
   prints eight things; r62's four-way condition): each splits into several codified statements, so expect 800-1100
   codified statements, and the Ears grammar to grow from the spike's ~12 statement funs to a few hundred
   (each distinct response shape is a fun, or a compositional fun over lexicon categories). Guarantees capabilities
   (226 reqs) need parsing only; no Gherkin is generated for them (they are measured).
2. **Gherkin.** Generated per group: title from the group, tags from its fresh ids, steps from the Steps grammar. The
   10 hand-written feature files (575 scenarios, 6337 lines) are replaced wholesale; `@deprecated` (43) disappears.
3. **Step definitions.** Today 1386 step definitions match 1872 distinct step texts by ad hoc regexes, often packing
   several facts into one step ("an initiative i1 under .shop/work/ whose work-items w1 is drafted and w2 is ready, its
   question asked by a researcher", `test_work_queue.py:68`). Generated steps will not reproduce those texts unless the
   Steps grammar is built to. Every step definition therefore needs either a new pattern or retirement. The Python
   bodies (world-building in `*_world.py`, `*_given*.py`; assertions) are largely reusable: they are the 13k lines'
   real value.
4. **Setup detail.** Today's scenarios carry concrete example data the requirement does not (question texts, file
   contents, Examples tables: 787 table rows). Generation needs a source for it: an `examples` block per group, parsed
   by the Steps grammar, or defaults in the world fixtures.
5. **Tools.** `model_parse` (Behaviour reading, v_e1/v_e2), `features` editing commands, `work_items` (accepts form),
   `supervise_draft*`/`_brief`/`_drafts` (id parsing), mark registration in conftest, `test_bound.py`'s file list, and
   tests in `tests/scripts/` that embed `[r<n>]` text all follow the new id form and file layout.

## 6. Proposal: a fixed step vocabulary from the grammar's Steps

The rule: **one Steps fun = one step definition**, as the spike's `gf-src/Steps.gf` header already says.

- **Generate the patterns, hand-write the bodies.** A script (e.g. `scripts/steps_vocab.py`) linearizes each Steps fun
  with its arguments as holes, giving a pytest-bdd `parsers.parse` pattern per fun (`GivenInitiative i s` ->
  `"an initiative {i} that is {s}"`), and writes `tests/scenarios/steps_vocab.py`: a table fun-name -> (keyword,
  pattern). Step modules decorate bodies by fun name, `@step_of("GivenInitiative")`, which looks the pattern up; no
  step text is typed in Python. Changing a fun's English changes the generated feature and the pattern together.
- **Arguments are typed by the lexicon.** Each hole has a lexicon category (IStatus, WStatus, Actor, Stage, instance
  names); the body receives the parsed value, and a converter per category (`converters=`) maps it (e.g. a backticked
  status to its bare word). Categories close the vocabulary: a step cannot ask for a value the lexicon lacks.
- **Two checks keep it fixed.** (a) every Steps fun has exactly one body and every body names an existing fun
  (replaces `features bindings --unbound`, a unit test like `test_bound.py`); (b) every generated step parses in
  Steps (by construction) and matches exactly one pattern (pytest-bdd ambiguity is impossible if lins are distinct).
- **Generation maps Ears to Steps.** For each Ears fun a fixed formulation rule gives its Steps: While/Where pre ->
  Given funs, When trigger -> one When fun, `If` condition -> Given/When with the invalid input, response -> Then funs;
  instances (i1, w1, ...) are chosen by the generator or taken from the group's examples block. Keep the When set
  small and generic, as today (`the session runs \`<cmd>\`` covers ~70% of Whens), and put the precision in Givens and
  Thens.
- **Migrating the bodies.** Harvest today's 1872 step texts per capability, cluster them by the body that matches them
  (1386 bodies), and make each surviving body a Steps fun whose linearization is close to today's text, splitting the
  packed Givens into one fact per fun. Expect roughly 400-600 funs for the 8 service capabilities (supervision ~200),
  far fewer than 1386, because the grammar composes lists ("w1 and w2") that today's regexes spell out one by one.
- **Order of work.** Convert capability by capability, smallest service ones first (batch-measurement, analysis-tools,
  work-queue, requests) to settle the vocabulary, supervision last; keep each capability's old feature and binder
  until its generated feature is green, then delete them. Whole-file `scenarios()` binding carries over unchanged.
- **Keep from v4.** `repo`/`context`/`run` fixtures, the world helpers, `work_items.py`'s selection by mark (marks
  become the fresh ids, registered from the spec, not `range(1, 200)`), xdist, `tests/scripts/` unit tests.
