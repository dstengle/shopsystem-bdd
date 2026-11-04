---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-plan-r3
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# The GF conversion, revision 3: logic and generation without the big solve — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `model logic` and `features generate` on one translation of each requirement into ground facts, read
twice: by a fixed clingo meta-encoding (`grammar/check.lp`) for conflicts, and by a solver-free reader for Gherkin. Also
fix the two suite costs that `suite-cost.md` measured.

**Architecture:** `spec_facts.translate` walks a requirement tree once and emits the facts of design-r3 §3.
`spec_context.load` reads, parses and translates a context once per state of its files. `spec_solve` runs one brave
clingo solve of facts + `check.lp` over the whole context and turns the shown atoms into the same `Finding`s and
report as before. `spec_steps` reads one group's facts into Steps trees, which `features_generate` writes. telingo,
cones, pools, witnesses and traces are deleted.

**Tech Stack:** Python 3, clingo 5.8.2 (Python API), GF 3.12 + pgf 1.1 (Steps/Req grammars), pytest + xdist.

**Spec:** `.shop/records/2026-11-03-gf-conversion/design-r3.md`. Its sources are `solver-research.md` (same directory)
and the working example in
`/tmp/claude-1000/-home-vscode-shopsystem-bdd/248cf039-6f1c-44df-97a2-339ab46c8793/scratchpad/solver-research/example/`
(`check.lp`, `reqs.lp`, `gherkin.py`, `run.py`). The suite fixes come from `suite-cost.md`. Executors read the design in
full before their task.

## Global Constraints

- **The live spec is not solved during development.** No task runs `model logic`, `spec_solve.run` or
  `spec_engine`/telingo over the live spec (`/home/vscode/shopsystem-bdd/spec`), except S11 (once) and S12. The
  new `features generate` has no solver, so it may run on the live spec from S6 on.
- **Do not run the old solver-driven tests until their rewrite has landed.** They take minutes and pegged the machine.
  - The files are `tests/scripts/test_spec_guarantees.py`, `test_spec_trace.py`, `test_revision_done.py`,
    `test_features_generate.py`, `test_spec_solve.py`, `test_spec_engine.py`, `test_spec_logic.py` and
    `tests/scenarios/test_supervision.py`.
  - Until a file is rewritten (its task is named below), every suite run passes
    `$SLOW = --ignore=tests/scripts/test_spec_guarantees.py --ignore=tests/scripts/test_spec_trace.py
    --ignore=tests/scripts/test_revision_done.py --ignore=tests/scripts/test_features_generate.py
    --ignore=tests/scripts/test_spec_solve.py --ignore=tests/scripts/test_spec_engine.py
    --ignore=tests/scripts/test_spec_logic.py --ignore=tests/scenarios/test_supervision.py`.
  - A task drops an `--ignore` only for a file it rewrote, or one an earlier task rewrote.
- **Fixtures only.** Development tests use small fixtures: `tests/scripts/fixtures/logic/cluster`,
  `tests/scripts/fixtures/generate/repo`, `tests/scripts/fixtures/glossary`, inline facts, or `tmp_path` copies of
  those.
- **Time limits.** Every pytest command runs under `timeout 600`. Any single test over 10 s is a defect to report,
  not to wait out.
- **Size.** Every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300` exits 0).
  `scripts/spec_solve.py` is at most 200 lines (design §7). A new module gets its CLAUDE.md module-map row in the
  same task. `test_revision_done.py::test_every_script_module_has_a_map_row` enforces this.
- **Frozen:** `tests/scenarios/vocab.py`, `grammar/Req.gf`, `grammar/ReqEng.gf`, the Steps grammar's wording and the
  handlers' (template, term) keys (design §2 non-goals).
- **The interfaces that stay the same** (design §6):
  - `spec_solve.run(root, capability=None, extra=None) -> list[Finding]`;
  - `spec_solve.report(findings, as_json) -> (str, int)`;
  - `spec_solve.ERRORS` and `spec_solve.Finding = namedtuple("Finding", "code ids text")`;
  - `features_generate.generate(root, path) -> str`, `features_generate.uncodified(root, paths)` and
    `features_generate.GenerateError`;
  - `model logic`'s exit 1 on an error finding.

  `run`'s `groups=` parameter goes, because it was used only by tests.
- **Determinism.** Facts, findings and feature text are pure functions of the spec files. No set or dict iteration
  order leaks into the output. Sort by the requirement order key `spec_solve._order` (kept) or by mention order.
- **One generic instance per noun phrase.** No pools, cones, horizons, retries or optimisation anywhere (design §2
  anti-goals).
- **Spec edits** happen only in S11, under design §9 call 6.
- **Commits.**
  - Each task commits on its own worktree branch off `gf-conversion`. Messages end with the line
    `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
  - Each task writes `.shop/records/2026-11-03-gf-conversion/report-S<n>.md`, using the frontmatter of the sibling
    records with `kind: report`, and commits it with its work. The report says what changed, the test runs and their
    times, and anything left open.
  - No task pushes.
- **Paths.** `$R` = `.shop/records/2026-11-03-gf-conversion`. Commands run from the repository root.

## Review Focus

1. **A tree with a fun the translation does not know** (a new lexicon entry kind, or a grammar fun added later).
   `translate` must raise `ValueError` naming the fun, never emit partial facts. S3 pins it with
   `test_an_unknown_fun_is_refused_naming_it`, beside the every-fun coverage test.
2. **A drafted file that replaces a live capability** (`extra` in `supervise_outputs`). The draft's requirements must
   replace that capability's facts, not sit beside them. Otherwise every draft clashes with its own original. S5 pins
   it with `test_a_draft_of_a_live_capability_replaces_it`.
3. **An empty or nearly empty context.** Examples: no codified capability, no triggered requirement, an attribute with
   no transitions. `check.lp` must ground with no clingo "atom does not occur" warnings on stderr, and the report is
   `no findings`, exit 0. S4 pins it with `test_no_facts_no_atoms_no_warnings`, and S5 with
   `test_a_context_with_nothing_codified_has_no_findings`.
4. **A cache that serves a stale vocabulary** after a spec edit that keeps the file size, or after a grammar `.gf`
   edit. S1 pins it with `test_an_edit_of_equal_size_reloads` and `test_a_grammar_edit_reloads`.
5. **A contrast with no failing value.** An `every` role whose restriction admits every value of the attribute, or an
   attribute with one value. The rule gives no contrast and must not crash. S6 pins it with
   `test_no_failing_value_gives_no_contrast`.

---

## Layers

| layer | tasks (side by side, disjoint files) | needs |
|---|---|---|
| 1 | S1 vocab cache · S2 batched `git add` · S3 the facts · S4 `check.lp` | — |
| 2 | S5 `model logic` on facts · S6 Gherkin from facts | S3, S4 (S5); S3 (S6) |
| 3 | S7 old solver deleted · S8 live-spec tests and the 10 s ceiling · S9 docs and skill | S5, S6 |
| 4 | S10 features regenerated, handler fallout | S7, S8 |
| 5 | S11 live clashes (design §9 call 6) | S10 |
| 6 | S12 verification and speed acceptance | S11 |

The orchestrator merges a layer with `--no-ff` onto `gf-conversion`, then runs the gate before the next layer starts:

```
timeout 600 python3 -m pytest -q $SLOW
python3 scripts/tools size --limit 300
```

`$SLOW` shrinks as files are rewritten. Between layers 2 and 3, the dead modules `spec_trace.py` and `spec_engine.py`
may fail to import; only the ignored test files import them.

---

## Layer 1

### Task S1: the step vocabulary loaded once per state of its files

**Files:**
- Modify: `scripts/features_vocab.py:85-97` (`load`), `scripts/spec_grammar.py:78-84` (`sources`)
- Test: `tests/scripts/test_features_vocab.py`

**Interfaces:**
- Produces:
  - `features_vocab.load(root) -> Vocab`, with the same contract as now. On an unchanged fingerprint it returns the
    same object without reading the lexicon or building GF sources.
  - `features_vocab._fingerprint(root) -> tuple`: `str(Path(root).resolve())`, then
    `(relative path, st_mtime_ns, st_size)` for every file under `root/spec` (sorted `rglob("*")`, files only) and
    every `spec_grammar.GRAMMARS.glob("*.gf")`.
  - `spec_grammar.sources(root, lex=None) -> dict[str, str]`, which reads the lexicon only when `lex` is None.

- [ ] **Step 1: Write the failing tests** in `tests/scripts/test_features_vocab.py` (each copies
  `tests/scripts/fixtures/generate/repo` to `tmp_path` and calls `toolchain.require()`):

```python
def test_a_second_load_reads_nothing(repo, monkeypatch):
    first = features_vocab.load(repo)
    calls = []
    monkeypatch.setattr(spec_lexicon, "read", lambda *a, **k: calls.append(a) or pytest.fail("lexicon read"))
    monkeypatch.setattr(spec_grammar, "sources", lambda *a, **k: pytest.fail("sources rebuilt"))
    assert features_vocab.load(repo) is first

def test_a_cold_load_reads_the_lexicon_once(repo, monkeypatch):
    features_vocab._by_print.clear()
    real, calls = spec_lexicon.read, []
    monkeypatch.setattr(spec_lexicon, "read", lambda *a, **k: calls.append(a) or real(*a, **k))
    features_vocab.load(repo)
    assert len(calls) == 1

def test_an_edit_of_equal_size_reloads(repo):
    first = features_vocab.load(repo)
    index = repo / "spec" / "index.md"
    text = index.read_text()
    index.write_text(text.replace("a unit of delivery", "a unit of delivers"))   # same length, new mtime
    assert features_vocab.load(repo).lex is not first.lex

def test_a_grammar_edit_reloads(repo, tmp_path, monkeypatch):   # GRAMMARS pointed at a copy; touch one .gf
    ...
    assert features_vocab._fingerprint(repo) != before
```

- [ ] **Step 2: Run the tests and see them fail.**
  `timeout 600 python3 -m pytest -q tests/scripts/test_features_vocab.py -k "load or reload"`. Expected: FAIL, with
  no `_by_print` and a lexicon read on the second load.
- [ ] **Step 3: Implement.**
  - Add the module-level `_by_print = {}` (fingerprint → Vocab). `load` checks it **before** reading the lexicon.
  - On a miss, `load` reads the lexicon once and passes it to `spec_grammar.sources(root, lex)` and to `modules(lex)`.
    It keeps the sha-keyed `_loaded`.
  - `sources(root, lex=None)` uses `lex or spec_lexicon.read(root)`.
- [ ] **Step 4: Run** `timeout 600 python3 -m pytest -q tests/scripts/test_features_vocab.py tests/scripts/test_spec_grammar.py`.
  Then run the scenario suite without supervision and time it:
  `timeout 600 python3 -m pytest -q tests/scenarios --ignore=tests/scenarios/test_supervision.py --durations=5`.
  Expected: PASS. Report the wall time against suite-cost's 26.6 s → 19.7 s.
- [ ] **Step 5: Commit** the three files and `$R/report-S1.md` with the message "features_vocab: load once per state of
  the spec and grammar files".

### Task S2: `migrate upgrade` stages its files in batches

**Files:**
- Modify: `scripts/migrate_upgrade.py:95-107` (`apply`)
- Test: `tests/scripts/test_migrate_upgrade.py`

**Interfaces:**
- Produces: `migrate_upgrade.apply(root, changes)`, with an unchanged contract. `migrate_upgrade.BATCH = 500`.

- [ ] **Step 1: Write the failing test** (unittest style, like the file):

```python
def test_apply_stages_every_text_with_one_add_per_batch(self):
    calls = []
    changes = types.SimpleNamespace(moves=[], texts={"f%04d.md" % i: "x\n" for i in range(1201)})
    with mock.patch.object(migrate_upgrade, "git", side_effect=lambda root, *a: calls.append(a)):
        migrate_upgrade.apply(self.root, changes)
    adds = [c for c in calls if c[0] == "add"]
    self.assertEqual([len(c) - 3 for c in adds], [500, 500, 201])
    self.assertTrue(all(c[:3] == ("add", "-f", "--") for c in adds))
    self.assertEqual(sorted(p for c in adds for p in c[3:]), sorted(changes.texts))
```

  Add a second test on a real git repository: three texts are written and staged
  (`git diff --cached --name-only` lists all three).
- [ ] **Step 2: Run the test and see it fail.** `timeout 600 python3 -m pytest -q tests/scripts/test_migrate_upgrade.py`.
  Expected: FAIL, 1201 adds of 1 path each.
- [ ] **Step 3: Implement.** Write every text first, then call `git(root, "add", "-f", "--", *chunk)` for each chunk
  of `BATCH` paths, in `changes.texts` order.
- [ ] **Step 4: Run** `timeout 600 python3 -m pytest -q tests/scripts/test_migrate_upgrade*.py --durations=5`.
  Expected: PASS. `test_migrate_upgrade_codified.py`'s setup takes about 3 s (it was 13.2 s).
- [ ] **Step 5: Commit** with `$R/report-S2.md` and the message "migrate upgrade: stage changed files in batches".

### Task S3: the facts (one translation per fun) and the context read once

**Files:**
- Create: `scripts/spec_facts.py` (clauses, triggers and verb phrases), `scripts/spec_facts_np.py` (noun phrases and
  their restrictions, from `spec_logic_np.Scope`), `scripts/spec_context.py`
- Modify: `scripts/spec_logic_vocab.py` (add `domain`, `Vocab.def_lits`; leave `facts`/`pools`/`guards` for S7),
  `CLAUDE.md` (rows for the three new modules)
- Test: `tests/scripts/test_spec_facts.py`

**Interfaces:**
- Consumes:
  - `spec_logic_vocab.Vocab` (`decode`, `kinds`, `attrs`, `attr_values`, `transitions`, `actors`, `subs`, `def_funs`,
    `members`);
  - `spec_grammar.parse`, `spec_read.capability`, `spec_read.universal`, `spec_tree.parts`.
- Produces:
  - `spec_facts.translate(vocab, ident: str, tree) -> list[str]`: ground facts, each ending in `.`, in a fixed
    order. They follow the schema of design §3 exactly, with the term encodings of today's `spec_logic`:
    - ids are clingo constants (`k_initiative`, `t_status`, `v_proposed`, `e_start`, `a_work`);
    - codes and quoted texts are strings (`"`work start`"`);
    - requirement ids are strings (`"s#r11"`);
    - role variables are `v1, v2, …` in order of mention;
    - an object may be a role, a string, `value(A,V)`, `number(K)`, `pair(X,Y)` or `none`;
    - D (the doer) is an actor constant, a role, or `any`.

    The decisions the design leaves open:
    - A positive `<attr>_Set` emits `set(R,I,V,A,Val)` **and** `resp(R,I,pos,set(A,Val),D,V)`. A negated one emits
      only `resp(R,I,neg,set(A,Val),D,V)`.
    - "X shall not use Y" emits `nouse(R,D,X)` beside the design's `uses(R,D,X)`.
    - `Only` emits `only(R,I,K)` and no `resp`.
    - A value list `whose A is v1 or v2` splits the requirement the way `CondOr` does: `R#1`, `R#2`, … with
      `disj(R,K)` naming the split. A negated list (`is not v1 or v2`) is one `neg` cond per value.
    - Becomes is `trig(R,becomes,set(A,Val),any,V)`.
    - IsRun is `trig(R,ran,Cmd,any,none)`.
    - A defined condition (one in `vocab.def_lits`) gives its `ccond`. When the condition is positive, its
      definition's `cond`/`crel` literals follow, on the same role, with fresh roles for the definition's other noun
      phrases.
    - An unknown fun raises `ValueError("no translation of … <fun>")`.
  - `spec_facts.define(vocab, tree) -> None`: records a `Def` tree's literals in `vocab.def_lits[cid]` (it replaces
    `spec_logic.definition`).
  - `spec_facts.split(ident) -> str`: `"s#r5#2"` → `"s#r5"`.
  - `spec_logic_vocab.domain(vocab) -> list[str]`, which gives:
    - `kind(K)`, `sub(K,K2)` and `actor(D)`;
    - `val(K,A,V)` for every value;
    - `trans(K,A,From,To)`;
    - `initial(K,A,V)` for the values no transition enters, or every value when every one is entered (today's
      `spec_solve.reachable` rule).
  - `spec_context.Statement = namedtuple("Statement", "id capability group tree")`. A U has capability and group
    `None`.
  - `spec_context.Context = namedtuple("Context", "vocab caps statements facts refused domain")`:
    - `caps` is {name: `spec_read.Capability`}. A file in `extra` replaces the capability of the same name.
    - `facts` is {statement id: [str]}.
    - `refused` is {requirement id: refusal text}, for the requirements that do not parse.
    - `domain` is `spec_logic_vocab.domain(vocab)`.
  - `spec_context.load(root, extra=()) -> Context`: cached per process by the fingerprint of `root/spec/**/*.md`, the
    files of `extra` (resolved path, mtime_ns, size) and `root`. It calls `define` for each condition whose
    definition parses as `Def` (today's `spec_solve.definitions` loop).

- [ ] **Step 1: Write the failing tests** in `tests/scripts/test_spec_facts.py`. They use the cluster fixture, a
  module-scoped `vocab` with `define`s applied, and a `tree(line)` helper like `test_spec_logic.py`'s. Port
  `test_every_fun_of_the_grammar_has_a_translation` (CLUSTER and GLOSSARY, against
  `spec_logic_vocab.Vocab(...).covers`) and `test_the_vocabulary_names_each_typed_fun_by_its_lexicon_entry` as they
  are. Then add these, one per row of design §3:

```python
START = "When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`."

def test_a_when_statement_gives_roles_condition_trigger_response_and_set(vocab):
    out = spec_facts.translate(vocab, "s#r11", tree(START))
    for f in ['role("s#r11",v1,k_initiative).', 'cond("s#r11",v1,t_status,v_proposed,pos).',
              'trig("s#r11",ran,"`work start`",a_the_person,v1).', 'set("s#r11",1,v1,t_status,v_started).',
              'resp("s#r11",1,pos,set(t_status,v_started),a_work,v1).', 'form("s#r11",when).']:
        assert f in out
    assert out == spec_facts.translate(vocab, "s#r11", tree(START))          # deterministic

def test_shall_not_set_is_a_negative_response_only(vocab): ...   # r12: resp(...,neg,set(t_status,v_started),...), no set/5
def test_a_response_object_gives_its_restrictions(vocab): ...    # "start a research stage for the initiative": oattr + orel
def test_every_gives_every_and_its_restriction_as_cond(vocab): ...  # r1/r5: every("…",vK)
def test_no_k_in_a_condition_is_none(vocab): ...                 # "no question is `open`" -> none(R,k_question,t_…,v_open)
def test_hold_at_most_is_count(vocab): ...                       # U1 -> count("U1",…,…)
def test_holds_and_is_free_are_pre_state(vocab): ...              # U2 -> holds/free facts
def test_shall_use_is_static(vocab): ...                         # uses/3, no resp
def test_a_where_feature_is_feat(vocab): ...
def test_cond_or_splits_the_requirement(vocab): ...              # ids "s#r5#1","s#r5#2" and disj/2; split() maps back
def test_a_defined_condition_expands_when_positive(vocab): ...   # c_outputless (Def) -> ccond + its literals
def test_a_prose_condition_is_opaque(vocab): ...                 # ccond only
def test_an_unknown_fun_is_refused_naming_it(vocab):
    with pytest.raises(ValueError, match="k_nothing_An"):
        spec_facts.translate(vocab, "s#r1", ("Ubiq", ("OneResp", ("Shall", ("NPSubj", ("k_nothing_An",)), ...))))

def test_domain_gives_values_transitions_and_initial_values(vocab):
    d = spec_logic_vocab.domain(vocab)
    assert "kind(k_initiative)." in d and "trans(k_initiative,t_status,v_proposed,v_started)." in d
    assert "initial(k_initiative,t_status,v_proposed)." in d

def test_the_context_is_read_once_per_state_of_its_files(tmp_path): ...
    # load twice -> same object; edit a capability -> new; an unparsed requirement is in .refused with its refusal;
    # an extra file named like a live capability replaces its statements
```

  Each test asserts exact fact strings with the cluster's ids. Read them off the fixture
  (`tests/scripts/fixtures/logic/cluster/spec`), as the START test above does.
- [ ] **Step 2: Run the tests and see them fail.** `timeout 600 python3 -m pytest -q tests/scripts/test_spec_facts.py`.
  Expected: FAIL with `No module named 'spec_facts'`.
- [ ] **Step 3: Implement** the three modules and `domain`.
  - Port the tree walk of `spec_logic.Translation`/`spec_logic_np.Scope` (`trigger`, `clause`, `atom_`, `vp`, `np`,
    `cn`, `arg`, `objects`), emitting facts instead of `&tel` formulas.
  - Keep `spec_logic.py`, `spec_logic_np.py` and `spec_solve.py` untouched: they are still live until layer 2.
- [ ] **Step 4: Run the tests and see them pass.** `timeout 600 python3 -m pytest -q tests/scripts/test_spec_facts.py
  --durations=5` and `python3 scripts/tools size --limit 300`. Expected: PASS, no test over 2 s.
- [ ] **Step 5: Commit** with `$R/report-S3.md` and the message "spec_facts: one translation per fun into facts;
  spec_context".

### Task S4: `grammar/check.lp`, the fixed meta-encoding

**Files:**
- Create: `grammar/check.lp`, starting from the example's `check.lp` and grown to the fact set of design §3 and §6
- Test: `tests/scripts/test_check_lp.py` (inline facts; runs clingo directly, so it does not depend on S3)

**Interfaces:**
- Consumes: the fact schema of design §3, with S3's decisions above: `set/5` beside `resp(…,set(A,Val),…)`,
  `nouse/3`, `only/3`, `R#n` splits. It also reads `domain`'s `kind/1`, `sub/2`, `val/3`, `trans/4`, `initial/3`
  and `actor/1`.
- Produces: under `--enum-mode=brave`, the shown atoms are the findings:
  - `clash(A,B,Why)`, with A < B (or A = B and Why = `self`) and Why ∈ {`pos_neg`, `neg_pos`, `set`, `exit`,
    `change`, `use`, `self`};
  - `bad_set(R,A,From,To)`;
  - `unreachable(R,A,V)`: the requirement R needs a value no path reaches. The design writes `unreachable(K,A,V)`;
    R is added so that a finding names its ids;
  - `lint(R,E,T)`: L5, the untriggered positive event obligation R on event E, with T a triggered requirement that
    reacts to E, or `none`.

  Given the fact `focus(A,B)`, it also shows `pre(A,B,X,Attr,Val,Pol)`: the merged pre-state of one witness, read by
  S5 in a normal (non-brave) solve.
- Rules the design fixes, all in the file:
  - Candidate pairs come from the shared-vocabulary index of §6: equal P and E, a compatible doer, and object kinds
    that are equal or `sub`. Also a triggered requirement with an untriggered one that binds one of its kinds, and a
    requirement with a U that shares an event or an attribute.
  - The `map/4` unification. Triggers must unify.
  - The pre-state must be consistent: one value per attribute, no literal both `pos` and `neg`, no `ccond` both ways,
    and no `none(K,A,Val)` against any merged role of K or a sub-kind with `cond(…,A,Val,pos)` (§3.3).
  - An untriggered requirement's conditions are checked against state 1 (A's pre-state with A's `set`s applied), and
    its responses against A's responses there (the two states of §6).
  - L3 and L4 are graph rules over `trans/4` and `initial/3`. An attribute with no `trans` gives no L4.
  - Every predicate the file reads is `#defined`.

- [ ] **Step 1: Write the failing tests.** A helper `solve(facts: str, extra="") -> set[str]` loads `grammar/check.lp`
  and the facts into `clingo.Control(["--enum-mode=brave", "--warn=none"])` and returns the shown atoms of the last
  model. The facts are the example's `reqs.lp`, rewritten in the r3 schema (trig/5, resp/6, cond/5), with small
  domains.

```python
def test_r2_and_r53_clash_on_one_trigger():   assert 'clash("r2","r53",pos_neg)' in solve(R2 + R53)
def test_r52_and_r72_clash():                 assert 'clash("r52","r72",neg_pos)' in solve(R52 + R72)
def test_a_different_status_does_not_clash(): assert not any(a.startswith("clash") for a in solve(R2 + R3))
def test_two_sets_of_one_attribute_clash():   assert 'clash("r16","r99",set)' in solve(R16 + R99)
def test_exit_ok_and_exit_error_clash(): ...           # Why exit
def test_change_nothing_and_a_set_clash(): ...         # Why change
def test_use_and_shall_not_use_clash(): ...            # Why use; and uses/3 never clashes with an event resp
def test_an_inconsistent_own_pre_state_is_self(): ...  # cond pos + neg of one value -> clash("r1","r1",self)
def test_two_sets_in_one_requirement_is_self(): ...
def test_no_k_is_v_blocks_the_unification():           # r27-like none(...) vs "a delegation is `written`": no clash
    assert not any(a.startswith("clash") for a in solve(R27 + DELEGATION))
def test_an_untriggered_prohibition_clashes_with_a_triggered_obligation(): ...
def test_a_sub_kind_object_unifies(): ...
def test_disjoint_kinds_are_never_paired(): ...        # no pair/2 atom (show it in the test via extra "#show pair/2.")
def test_a_set_with_no_transition_is_bad_set():  assert 'bad_set("r98",t_status,v_drafted,v_done)' in solve(R98 + DOM)
def test_an_unreached_value_is_unreachable(): ...
def test_an_untriggered_event_obligation_is_linted(): ... # lint("r10",e_write,none); with a reacting trigger, lint(...,"r6")
def test_focus_shows_one_merged_pre_state(): ...      # normal solve with focus("r52","r72"): pre(...) atoms present
def test_no_facts_no_atoms_no_warnings(capfd):        # without --warn=none
    assert solve("", warn=True) == set() and capfd.readouterr().err == ""
def test_the_example_grounds_small_and_fast():        # all example requirements: < 2000 rules, < 0.5 s
    ...
```

- [ ] **Step 2: Run the tests and see them fail.** `timeout 600 python3 -m pytest -q tests/scripts/test_check_lp.py`.
  Expected: FAIL, because `grammar/check.lp` is missing.
- [ ] **Step 3: Write `grammar/check.lp`.** Keep the example's structure and comments. Grow it to the rules above.
  Keep it under about 150 lines.
- [ ] **Step 4: Run the tests and see them pass.** `timeout 600 python3 -m pytest -q tests/scripts/test_check_lp.py --durations=5`.
  Expected: PASS, each under 1 s.
- [ ] **Step 5: Commit** with `$R/report-S4.md` and the message "grammar/check.lp: conflicts as witnesses, lifecycle
  and reachability as graph rules". The `grammar/` row of CLAUDE.md changes in S7.

---

## Layer 2

### Task S5: `model logic` on facts and `check.lp`

**Files:**
- Rewrite: `scripts/spec_solve.py` (at most 200 lines)
- Rewrite: `tests/scripts/test_spec_solve.py` (drop it from `$SLOW`)

**Interfaces:**
- Consumes: `spec_context.load`, `spec_facts.split`, `grammar/check.lp` and its shown atoms (S3, S4), and
  `spec_tree.normal`.
- Produces:
  - `spec_solve.run(root, capability=None, extra=None) -> list[Finding]`, sorted by code, then by `_order` of the
    first id. One solve over the whole context; `capability` filters to the findings naming that capability's ids.
  - `spec_solve.report(findings, as_json)`, unchanged.
  - `spec_solve.ERRORS = ("L0", "L1", "L3")`. `L0` is "the check did not finish in 20 s; the findings so far are
    listed" (exit 1).
  - `spec_solve.LIMIT = 20.0`.
  - `spec_solve.solve(program: str, limit: float) -> tuple[list[str], bool]`: the shown atoms of a brave solve and
    whether it finished (`ctl.solve(async_=True)` + `handle.wait(limit)`).
  - `spec_solve.l2(statements, scope)` and `_key`, `_order`, kept as they are.
- Finding ids and texts (design §6):
  - **L1:** `ids = [A, B]` (or `[A]` for `self`), mapped back through `split`. The text is
    `"<A> and #<B local> clash: on "<trigger>" with <merged pre-state>, <why>"`, where:
    - the trigger is `spec_grammar.linearise` of A's trigger subtree;
    - the merged pre-state comes from one focused normal solve per clash, with `focus(A,B)` and its `pre/6` atoms;
    - the why is one of the five phrases of §6's L1 row, worded with the lexicon terms.

    `self` is `"<A> contradicts itself"`.
  - **L2:** unchanged.
  - **L3:** `ids = [R]`, text unchanged: `"<R> sets the <attr> of <a kind> from <v> to <w>, which no transition
    allows"`.
  - **L4:** `ids = [R]`, `"<R> needs <a kind> whose <attr> is <v>, which no transition path reaches"`.
  - **L5:** warning, `ids = [R] + [T]`, `"<R> obliges <event> in every state; <T> reacts to it"` (the clause after
    `;` only when T exists).

- [ ] **Step 1: Write the failing tests** (cluster fixture, module-scoped `findings = spec_solve.run(CLUSTER)`; keep
  the `copy` helper):

```python
def test_the_restatements_of_r66_and_r95_are_an_l2_duplicate(findings):
    [dup] = of(findings, "L2"); assert dup.ids == ["supervision#r3", "supervision#r4"]
def test_two_statements_saying_opposite_things_of_one_trigger_are_an_l1_naming_both(findings):
    [l1] = of(findings, "L1")
    assert l1.ids == ["supervision#r11", "supervision#r12"]
    assert l1.text.startswith("supervision#r11 and #r12 clash: on ") and "`proposed`" in l1.text
def test_the_resource_formulation_has_no_l1(findings): ...   # no L1 id in {r2, r5, r6, r7, r8, U1, U2}
def test_a_set_off_the_transition_table_is_l3(findings):
    [l3] = of(findings, "L3"); assert l3.ids == ["supervision#r9"]
    assert l3.text == ("supervision#r9 sets the status of an initiative from `proposed` to `abandoned`, which no "
                       "transition allows")
def test_a_pre_state_value_no_path_reaches_is_l4(findings):
    [l4] = of(findings, "L4"); assert l4.ids == ["supervision#r10"] and "`awaiting-asker`" in l4.text
def test_an_untriggered_event_obligation_is_l5(findings): ...   # r10 ("shall write a question")
def test_a_requirement_that_contradicts_itself_is_l1_with_its_id_only(tmp_path): ...   # r13 two sets -> ["supervision#r13"]
@pytest.mark.parametrize("why, lines", SEEDED)   # one seeded pair per clash kind: pos_neg, set, exit, change, use
def test_a_seeded_pair_is_an_l1_naming_both(tmp_path, why, lines): ...
def test_no_k_is_v_in_a_condition_does_not_clash(tmp_path): ...  # seeded r27-like pair on the cluster's kinds
def test_a_capability_names_what_is_reported(findings):
    assert spec_solve.run(CLUSTER, "supervision") == findings and spec_solve.run(CLUSTER, "no-such") == []
def test_extra_drafted_files_are_checked_with_the_spec(tmp_path): ...  # pacing#r1 vs supervision#r11 -> one L1 naming both
def test_a_draft_of_a_live_capability_replaces_it(tmp_path): ...       # supervision.md copied as a draft: same findings
def test_a_context_with_nothing_codified_has_no_findings(tmp_path):
    assert spec_solve.report(spec_solve.run(empty), False) == ("no findings", 0)
def test_a_solve_past_its_limit_is_partial():
    atoms, done = spec_solve.solve(PIGEONHOLE_12, 0.2); assert done is False
def test_l0_is_an_error_and_its_report_exits_1(): ...
def test_the_whole_context_is_one_solve(monkeypatch, findings): ...   # clingo.Control built 1 + (number of L1) times
def test_the_cluster_is_checked_in_under_a_second(): ...
# report tests ported as they are: text, counts line, "no findings", JSON object with exit, exit 0 on warnings only
def test_no_telingo_cone_pool_or_horizon():
    text = (REPO / "scripts" / "spec_solve.py").read_text()
    assert not re.search(r"telingo|spec_engine|cone|pool|horizon|HORIZON", text)
```

- [ ] **Step 2: Run the tests and see them fail.** `timeout 600 python3 -m pytest -q tests/scripts/test_spec_solve.py`.
  Expected: FAIL. The old module has no `solve(program, limit)`, and its ids name groups.
- [ ] **Step 3: Rewrite `spec_solve.py`:**
  1. `spec_context.load(root, extra)`;
  2. the program is the domain, every statement's facts and `check.lp`;
  3. one brave `solve`;
  4. one focused solve per clash, for its text;
  5. the findings, then L2.

  Do not import `spec_engine`, `spec_logic` or `spec_trace`.
- [ ] **Step 4: Run the tests and see them pass.**
  `timeout 600 python3 -m pytest -q tests/scripts/test_spec_solve.py tests/scripts/test_model_output.py --durations=5`.
  Expected: PASS, no test over 2 s.
  - Do not run `test_e2e_codified.py`, `test_supervise_outputs.py` or `test_supervise_formulate.py` in this worktree.
    The old `features_generate` imports the removed `spec_solve.Context`. The layer-2 gate runs them after S6 is
    merged.
- [ ] **Step 5: Commit** with `$R/report-S5.md` and the message "model logic: one brave solve of facts and check.lp".

### Task S6: Gherkin from the facts

**Files:**
- Rename: `scripts/spec_trace_steps.py` → `scripts/spec_steps.py` (`git mv`, then extend)
- Rewrite: `scripts/features_generate.py`
- Modify: `CLAUDE.md` (the `spec_trace_steps.py` row becomes `spec_steps.py`; the `features_generate.py` row says
  "read off its facts by `spec_steps`")
- Test: create `tests/scripts/test_spec_steps.py`; rewrite the fixture tests of `tests/scripts/test_features_generate.py`
  (drop it from `$SLOW`)

**Interfaces:**
- Consumes: `spec_context.load`, `Context.facts`, `Context.refused`, `spec_facts.split` (S3), and
  `features_vocab.load`/`Vocab.text`/`parse`.
- Produces:
  - `spec_steps.read(facts: list[list[str]], logic, steps) -> list[tuple[str, tuple]]`: the (keyword, Steps tree)
    pairs of one group. The argument holds the facts of each of its requirements, in order; a split requirement
    contributes only its `#1`.
    - Each fact is parsed with `clingo.parse_term`.
    - Each role is turned into the instance term `o(K,vN)`.
    - Each fact is turned into the atom that `Reader`'s table already reads: `attr`, `cond`, `rel`, `given`,
      `holds`, `over` (a negated free), `ran`, `ran_any`, `does`, `done_to`, `set_to`. `Reader`, `LETTERS` and the
      naming carry over unchanged.
  - `spec_steps.TraceError` keeps its name. `Reader` and the helpers stay importable from `spec_steps`.
  - The rules, in order (design §5):
    1. Givens: `feat`, then the `cond`/`ccond`/`crel`/`holds`/`free` facts in fact order. Each role first mentioned
       here is introduced by `Reader.given`. A `none` fact gives no Given.
    2. When: the `trig`.
    3. Thens: by I, each `resp`, then its `oattr`/`orel`, then that I's `set`s. A positive set is worded once, from
       its `set` fact, not again from its `resp`.
    4. Contrast: for each `every` role with a `cond`, one more instance of its kind, introduced as a Given:
       - for a `pos` restriction, the first value in `val` order that is not among the restriction's values;
       - for a `neg` restriction, the first negated value in `val` order;
       - with no such value, no contrast.

       A `DoesNot` Then for that instance follows the role's Thens.
    5. Several requirements in one group (fixtures only; the live spec has one per group): a later requirement's
       role maps to the first requirement's role of the same kind and the same rank among that kind's roles. Givens
       and When come from the first requirement; Thens come from each, in order.
  - `features_generate.generate(root, path) -> str`, unchanged in contract and header. It has no `Context` solve and
    no multiprocessing. `scenario_text(v, ctx, cap, group) -> str | None`. A requirement in `ctx.refused` raises
    `GenerateError("<cap>#<rid>: <refusal>")`.

- [ ] **Step 1: Write the failing tests.**
  `tests/scripts/test_spec_steps.py` works on `tests/scripts/fixtures/generate/repo` copied to `tmp_path`, with
  `steps(root, gid) -> [(keyword, text)]`:

```python
def test_a_while_condition_is_a_given_that_introduces_its_role(repo):   # add "While a work-item is `drafted`, …"
    assert ("given", "a work-item w1 that is `drafted`") in steps(repo, "work-queue#g9")
def test_a_negated_restriction_is_a_kind_given_and_an_is_not(repo):
    assert steps(repo, "work-queue#g2")[:2] == [("given", "an initiative i1"), ("given", "the initiative i1 is not `proposed`")]
def test_the_trigger_is_the_when(repo): ...
def test_each_response_is_a_then_with_its_restrictions_then_its_sets(repo): ...
def test_an_every_role_gets_one_contrast_failing_its_restriction(repo):
    got = steps(repo, "supervision#g1")
    assert ("given", "an initiative i2 that is `done`") in got and ("then", "`work run` does not take the initiative i2") in got
    assert not any("i3" in t for _, t in got)
def test_no_failing_value_gives_no_contrast(repo): ...
def test_no_k_is_v_gives_no_given(repo): ...
def test_a_scenario_does_not_change_when_an_unrelated_requirement_is_added(repo): ...   # anti-goal: add a group elsewhere
def test_roles_are_named_by_kind_letter_in_order_of_first_mention(repo): ...
def test_two_requirements_of_one_group_share_their_roles(repo): ...                    # work-queue#g1: one i1
```

  In `test_features_generate.py`, keep every fixture test. Update the expected texts to the §5 rules:
  - `WORK_QUEUE`'s g2 block becomes `Given an initiative i1` / `And the initiative i1 is not \`proposed\`` / `When …
    on the initiative i1` / `Then \`work\` exits with an error naming the status of the initiative i1`.
  - g1 and g3 keep their current lines.
  - `G1` becomes `Given an initiative i1` / `And the initiative i1 is not \`done\`` / `And the initiative i1 is not
    \`abandoned\`` / `And an initiative i2 that is \`done\`` / `When the person runs \`work run\`` / `Then \`work run\`
    takes the initiative i1` / `And \`work run\` does not take the initiative i2`. The test asserts these lines in
    this order, and that no `i3` appears. If r2 adds a Then, it is allowed after them.
  - Rename `test_an_if_group_gives_an_initiative_its_restriction_excludes` to
    `test_an_if_group_states_the_restriction_it_excludes`, asserting the two g2 Givens above.
  - Add:

```python
def test_byte_stable_under_two_hash_seeds(repo): ...   # PYTHONHASHSEED=1 and 2 give equal bytes (fixture)
def test_generation_imports_no_solver():
    text = (REPO / "scripts" / "features_generate.py").read_text() + (REPO / "scripts" / "spec_steps.py").read_text()
    assert not re.search(r"spec_solve|spec_trace\b|spec_engine|telingo|clingo\.Control", text)
```

- [ ] **Step 2: Run the tests and see them fail.**
  `timeout 600 python3 -m pytest -q tests/scripts/test_spec_steps.py tests/scripts/test_features_generate.py`.
  Expected: FAIL.
- [ ] **Step 3: Implement** `spec_steps.read` and the new `features_generate`. `context()` goes from
  `features_generate`; `spec_context.load` caches instead.
- [ ] **Step 4: Run the tests and see them pass.**
  `timeout 600 python3 -m pytest -q tests/scripts/test_spec_steps.py tests/scripts/test_features_generate.py
  tests/scripts/test_supervise_formulate.py tests/scripts/test_features_vocab.py --durations=5`. Expected: PASS, no
  test over 10 s.
  - `test_check_on_the_live_repo_runs_to_its_end` has no solver now and may run. Report its time.
  - Do not run `test_e2e_codified.py` here; S8 owns it.
- [ ] **Step 5: Commit** with `$R/report-S6.md` and the message "features generate: scenarios read off each
  requirement's facts".

---

## Layer 3

### Task S7: the old solver deleted, telingo unpinned, the module map

**Files:**
- Delete: `scripts/spec_engine.py`, `scripts/spec_trace.py`, `scripts/spec_logic.py`, `scripts/spec_logic_np.py`,
  `grammar/background.lp`, `grammar/cone.lp`, `tests/scripts/test_spec_engine.py`, `tests/scripts/test_spec_trace.py`,
  `tests/scripts/test_spec_logic.py`
- Modify:
  - `scripts/spec_logic_vocab.py`: remove `facts`, `pools`, `guards`, `guard_id`, `AMOUNT` and the docstring's
    `background.lp`, unless something still uses them (`count/3`'s amount for a code count stays, if S3 used
    `AMOUNT`);
  - `scripts/tools_grammar.py`: `WHEELS = {"pgf": "1.1", "clingo": "5.8.2"}`, and `WITHOUT` without telingo;
  - `scripts/tools`: docstrings that name telingo;
  - `tests/toolchain.py`: `WHEELS = ("pgf", "clingo")`;
  - `tests/scripts/test_tools.py:80` and `tests/scripts/test_tools_grammar.py`: telingo out of the expected lists
    and pip logs;
  - `CLAUDE.md`, these rows:
    - `grammar/`: `check.lp` replaces `background.lp` and `cone.lp`;
    - `spec_logic.py` and `spec_logic_np.py` go, and the facts row stays;
    - `spec_logic_vocab.py`: "the domain facts, `initial/3`";
    - `spec_engine.py` goes;
    - `spec_solve.py`: "facts → `check.lp` → findings, L1-L5";
    - `spec_trace.py` goes;
    - `tools_grammar.py`: "pgf and clingo".

**Interfaces:**
- Consumes: nothing new.
- Produces: no module imports `telingo`, `spec_engine`, `spec_logic`, `spec_logic_np` or `spec_trace`.

- [ ] **Step 1: Write the failing test.** Add it to `tests/scripts/test_tools_grammar.py`:

```python
def test_nothing_imports_telingo_or_the_old_solver(self):
    root = pathlib.Path(__file__).resolve().parents[2]
    files = list((root / "scripts").glob("*.py")) + [root / "scripts" / n for n in ("tools", "model", "features")]
    bad = [p.name for p in files if re.search(r"^\s*(import|from)\s+(telingo|spec_engine|spec_logic\b|spec_logic_np|spec_trace\b)", p.read_text(), re.M)]
    self.assertEqual(bad, [])
    self.assertFalse((root / "grammar" / "background.lp").exists() or (root / "grammar" / "cone.lp").exists())
```

- [ ] **Step 2: Run the test and see it fail.** `timeout 600 python3 -m pytest -q tests/scripts/test_tools_grammar.py`.
  Expected: FAIL.
- [ ] **Step 3: Make the deletions and edits.** Check with
  `git grep -n "spec_engine\|spec_trace\b\|spec_logic\b\|spec_logic_np\|background.lp\|cone.lp" -- scripts tests CLAUDE.md`.
  Expected: no hit outside `.shop/`.
- [ ] **Step 4: Run** `timeout 600 python3 -m pytest -q $SLOW tests/scripts` (with the ignores of deleted files
  removed), `python3 scripts/tools check scripts tests` and `python3 scripts/tools size --limit 300`. Expected: PASS,
  and vulture finds no dead code left in `spec_logic_vocab.py`.
- [ ] **Step 5: Commit** with `$R/report-S7.md` and the message "remove telingo, the cone engine and the trace
  solver".

### Task S8: the live-spec tests share one run; the 10 s ceiling

**Files:**
- Create: `tests/scripts/conftest.py` (the session-scoped `live_logic` fixture)
- Modify:
  - `conftest.py` (root): the ceiling report;
  - `pytest.ini`: register the marker `live_logic`;
  - `tests/scripts/test_spec_guarantees.py`, `tests/scripts/test_revision_done.py`,
    `tests/scripts/test_features_generate.py` (the live tests only), `tests/scripts/test_e2e_codified.py`
- Test: `tests/scripts/test_ceiling.py`

**Interfaces:**
- Consumes: `spec_solve.run`, `spec_solve.report` (S5) and `features generate --check` (S6).
- Produces:
  - `live_logic` (session scope; one run per xdist worker): `spec_solve.run(REPO)`, the live findings. Each test that
    uses it is marked `@pytest.mark.live_logic`.
  - `EXPECTED: dict[str, str]` in `tests/scripts/conftest.py`: {finding text: why}, the live findings that are known
    and open. It starts empty, and S11 fills it.
  - In the root `conftest.py`, the ceiling. `pytest_runtest_logreport` collects each `report.duration` over
    `float(os.environ.get("SHOPSYSTEM_TEST_CEILING", "10"))`, setup, call and teardown summed per nodeid, on the
    controller. `pytest_terminal_summary` prints `tests over the 10 s ceiling:` followed by one `<seconds> <nodeid>`
    line each, or nothing when there are none. It reports and does not fail (design §7).

- [ ] **Step 1: Write the failing tests and the rewrites.**
  - `test_ceiling.py`: writes a tmp project with `def test_slow(): time.sleep(0.3)` and a copy of the root
    conftest's hooks. It runs `pytest -p no:xdist` with `SHOPSYSTEM_TEST_CEILING=0.1` and asserts
    `"tests over the" in out and "test_slow" in out`. With the ceiling at 5 it asserts that the line is absent.
  - `test_spec_guarantees.py`: `findings` becomes the `live_logic` fixture, and
    `test_the_logic_check_finds_no_error` is marked `live_logic`. It asserts
    `[f.text for f in live_logic if f.code in spec_solve.ERRORS and …cap… and f.text not in EXPECTED] == []`.
  - `test_revision_done.py`:
    - `test_model_logic_finds_no_conflict_in_the_spec` uses `live_logic`, is marked, has no subprocess and no
      `timeout=600`. It asserts no L1/L2/L3 outside `EXPECTED`.
    - `test_no_fixed_horizon`'s docstring changes to "no horizon constant".
    - Add `test_model_logic_on_the_live_spec_is_fast` (marked): `model logic` as a subprocess, in under 2 s wall time.
  - `test_features_generate.py`:
    - `test_check_on_the_live_repo_runs_to_its_end` becomes `test_check_on_the_live_repo_is_fast_and_clean`: the
      return code is in (0, 1), there is no Traceback, and it takes under 5 s.
    - Add `test_byte_stable` on a `tmp_path` copy of the live `spec/`: `features generate` under
      `PYTHONHASHSEED=1` and `=2` gives equal bytes for every service capability (design §5).
  - `test_e2e_codified.py`: adjust only what the r3 texts changed. The REFUSED draft (proposed → abandoned) is now an
    L3 named `work-queue#r2`. Assert the refusal through `supervise_outputs`, as the test already does.
- [ ] **Step 2: Run the tests and see them fail** where they are new.
  `timeout 600 python3 -m pytest -q tests/scripts/test_ceiling.py`. Expected: FAIL, because there is no ceiling hook.
- [ ] **Step 3: Implement** the hooks, the fixture and the rewrites.
- [ ] **Step 4: Run** the tests below. The `live_logic` tests are not run here: they solve the live spec, and S12
  runs them first.
  - `timeout 600 python3 -m pytest -q -m "not fixture and not live_logic" tests/scripts/test_ceiling.py
    tests/scripts/test_spec_guarantees.py tests/scripts/test_revision_done.py tests/scripts/test_features_generate.py
    tests/scripts/test_e2e_codified.py tests/scripts/test_supervise_outputs.py --durations=10`.
  - Expected: PASS, and no test over 10 s. Report `test_e2e_codified`'s time; it was 11.2 s.
  - `--collect-only -m live_logic` lists the marked tests.
- [ ] **Step 5: Commit** with `$R/report-S8.md` and the message "tests: one live model logic run, the 10 s ceiling".

### Task S9: the docs and the skill say what the check now is

**Files:**
- Modify:
  - `README.md` (lines 4, 22, 64, 153-154);
  - `docs/capability-format.md` (around lines 400-416);
  - `docs/design-model/grammar.md` (around lines 410-450);
  - `docs/design-model/design-model.md`: lines 21 and 142-145, and a new decision row after C37 that names
    design-r3 (C37 stays, as history);
  - `skills/checking-spec-consistency/SKILL.md` (lines 10 and 22).

**Interfaces:**
- Consumes: the findings L1-L5 as S5 defines them.
- Produces: text only. Each place says the following.
  - Each fun translates to facts.
  - `model logic` is one clingo solve of `grammar/check.lp` over pairs that share vocabulary: L1 a clash witness
    naming both ids, L2 duplicates, L3/L4 graph rules on the transitions, L5 an untriggered event obligation.
  - `features generate` reads each requirement's facts, with no solver.
  - The grammar tools are GF, pgf and clingo.
  - The skill's missing-tool list is "gf, clingo".

- [ ] **Step 1: Write the failing test.** Add to `tests/scripts/test_agents.py`, or the nearest docs test:
  `test_no_doc_names_telingo_as_current`. In `README.md`, `docs/capability-format.md`, `docs/design-model/grammar.md`
  and `skills/checking-spec-consistency/SKILL.md`, no line names `telingo` or `&tel`. `design-model.md` and
  `how-we-got-here.md` may keep history.
- [ ] **Step 2: Run it and see it fail.** `timeout 600 python3 -m pytest -q tests/scripts/test_agents.py`.
- [ ] **Step 3: Edit the texts.** Wrap them at the files' widths, and use the codes and wording of S5.
- [ ] **Step 4: Run it and see it pass.** `timeout 600 python3 -m pytest -q tests/scripts/test_agents.py`. Expected:
  PASS.
- [ ] **Step 5: Commit** with `$R/report-S9.md` and the message "docs: model logic and features generate after
  revision 3".

---

## Layer 4

### Task S10: features regenerated; handler fallout fixed in the world

**Files:**
- Regenerate: `features/*.feature` (all 8)
- Modify, as the failures need: `tests/scenarios/world_*.py`, `tests/scenarios/<capability>_handlers*.py`,
  `tests/scenarios/<capability>_world.py`, `supervision_build.py`, `supervision_plans.py`
- Never modify: `tests/scenarios/vocab.py`, `spec/`, `scripts/`

**Interfaces:**
- Consumes: `features generate` (S6).
- Produces: `python3 scripts/features generate --check` exits 0 on the live repository, and `tests/scenarios` passes.

- [ ] **Step 1: Regenerate.** Run `time python3 scripts/features generate` with every service capability named, then
  `python3 scripts/features generate --check`. Expected: exit 0, in under 5 s. Write the per-capability
  `git diff --stat features/` into the report.
- [ ] **Step 2: Run the scenarios and see which fail.**
  `timeout 600 python3 -m pytest -q tests/scenarios --durations=10 -x --maxfail=50`. This is the first run of
  `test_supervision.py` (drop it from `$SLOW`). If any test runs over 10 s, stop and report it, with its
  `--durations` line.
- [ ] **Step 3: Fix each failure in the world or the handler.** The new scenarios drop revision 2's extra Givens and
  gain rule contrasts (design §10), so a handler gets a default such as "a work-item has no blocker" or "a lock is
  free". **Never add a Given the requirement does not state**, and never edit a generated feature. A failure that
  needs a spec change is listed in the report for S11 and left failing; it is named in the report's table.
- [ ] **Step 4: Run** `timeout 600 python3 -m pytest -q tests/scenarios tests/scripts/test_bound.py
  tests/scripts/test_features_scenarios.py --durations=10` and `python3 scripts/features vocab --check`. Expected:
  PASS, apart from the listed S11 items, and no test over 10 s.
- [ ] **Step 5: Commit**, one commit for `features/` and one per capability's handler fixes, with
  `$R/report-S10.md`. The messages are "features: regenerated from facts (revision 3)" and "scenarios:
  <capability> handlers after revision 3".

---

## Layer 5

### Task S11: the clashes the new check finds in the live spec (design §9 call 6)

**Files:**
- Modify: `spec/capabilities/*.md` (only the requirements named by findings), `features/<cap>.feature` (regenerated
  for an edited capability), `tests/scripts/conftest.py` (`EXPECTED`)
- Create: `$R/report-S11.md`, with the findings table and the questions

**Interfaces:**
- Consumes: `model logic` (S5), `EXPECTED` (S8).
- Produces: the live findings are either cleared or named in `EXPECTED`. Each one in `EXPECTED` is a question for the
  person in the report.

- [ ] **Step 1: Run the check once on the live spec.** This is the first time, as the person instructed:
  `time timeout 120 python3 scripts/model logic --json > $R/logic-r3.json`. Record the time; the target is under 2 s.
  If it runs past 20 s, it reports L0. Stop and report rather than retry.
- [ ] **Step 2: Triage every L1 and L3** into the report's table: id, text, the reading, and the action.
  - **Edit:** one reading is plainly the intent, such as a dropped condition or a missing exception. Edit the
    requirement in place and keep its id (the codified spec is unreleased, so the edit is not retired). Then run
    `python3 scripts/model parse` on the line, `python3 scripts/features generate <cap>`, and that capability's
    scenario test. One commit each: "spec: <cap>#<rid> <what changed> (r3 clash with <other id>)".
  - **Question:** the fix needs a product decision, such as which requirement wins. Do not edit. Add
    `EXPECTED[text] = "question: <one line>"` and the question to the report.
  - L4 and L5 warnings are listed in the report and not edited.
  - Fix the S10 items that needed a spec change the same way.
- [ ] **Step 3: Re-run the check once.** `timeout 120 python3 scripts/model logic`. Expected: every L1 and L3 left is
  in `EXPECTED`. Then run `python3 scripts/features generate --check` (exit 0) and
  `timeout 600 python3 -m pytest -q tests/scenarios`. Expected: PASS.
- [ ] **Step 4: Commit** `EXPECTED`, `logic-r3.json` and `$R/report-S11.md`, with the message "records: revision 3's
  live findings".

---

## Layer 6

### Task S12: verification and speed acceptance

**Files:**
- Create: `$R/report-S12.md`
- Modify: only what a failing check below needs, reported line by line

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: Time the speed targets** (design §2 goal 6). Expected:
  - `/usr/bin/time -v python3 scripts/model logic` takes under 2 s wall time;
  - `/usr/bin/time -v python3 scripts/features generate --check` takes under 5 s and exits 0.

  Record the wall time and the max RSS of each.
- [ ] **Step 2: Run the whole suite** with no `$SLOW`, every ignore gone: `time timeout 900 python3 -m pytest -q
  --durations=25`. Expected:
  - every test passes, the `live_logic` ones included;
  - the ceiling summary prints no test over 10 s;
  - the solver-driven files (`test_spec_solve`, `test_check_lp`, `test_spec_facts`, `test_spec_steps`,
    `test_features_generate`, `test_spec_guarantees`, `test_revision_done`) sum under 15 test-seconds.

  Record the wall time against suite-cost's 26.6 s baseline (and its 18.1 s floor with both fixes).
- [ ] **Step 3: Run the repository checks.** `python3 scripts/tools size --limit 300`, then `python3 scripts/tools
  check scripts tests`, then `python3 scripts/model check --limit 100000`, then `python3 scripts/features vocab
  --check`. Expected: exit 0, with no new `model check` row against `$R/baseline-model-check.txt`.
- [ ] **Step 4: Check the design's goals one by one** in the report:
  - goals 1-6;
  - the anti-goals: no solve grows with the spec times a pool; every finding names only its ids; scenarios are
    stable when an unrelated requirement is added (S6's test);
  - the module table of §7;
  - the open questions S11 listed.
- [ ] **Step 5: Commit** with `$R/report-S12.md` and the message "records: revision 3 verified". Do not push.

---

## Self-review notes

- **Coverage of design-r3.**
  - §3 (facts) is S3. §3.1 is S3 (`uses`), S4 and S5 (L5). §3.2 is S3 (`define`, opaque `ccond`). §3.3 is S3, S4,
    S5 and S6 (`none`).
  - §4 is not built, as the design decides.
  - §5 is S6. Its byte-stable test on the live spec is S8.
  - §6 is S4 and S5. The 20 s limit is S5's `L0`.
  - §7 deletions and the module map are S6 and S7. `tools` without telingo is S7. The tests are S3-S8, and the
    ceiling is S8.
  - §9 call 6 is S11. The §10 risks are S10, S11 and S5 (the limit).
  - suite-cost's two fixes are S1 and S2.
- **Consistent names.**
  - `spec_context.load`, `Context.facts`/`.refused`/`.domain` and `spec_facts.split` are used the same way in S5 and
    S6.
  - `ERRORS` gains `L0`. `supervise_outputs` keeps filtering on `spec_solve.ERRORS`, unchanged.
- **Proportion.** Signatures, fact strings and test assertions only. The bodies are left to the executors, apart from
  the fixed copy of finding texts.
