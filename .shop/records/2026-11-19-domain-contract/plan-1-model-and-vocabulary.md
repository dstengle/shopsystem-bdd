# Plan 1 of 7: the domain model and vocabulary readers

Implementation plan for `design.md` (this folder), phase 1. Written 2026-11-19 while the person is offline; open
choices are made by the session (directive-1) and marked **session's call**.

## The whole branch (read once, every phase)

- **One branch `domain-contract`**, made from `main` by this phase, outside the batch workflow (design §1
  Constraints). Every phase commits on it and pushes `git push origin domain-contract` (`unset GH_TOKEN` first,
  directive-3). Nothing is merged to `main` before the review.
- **One fresh implementer agent per phase, in order** (`plan-1-...` to `plan-7-...`), each reading `design.md`, its own
  plan and the commits of the phases before it (`git log main..domain-contract`). Then **one fresh reviewer of the
  whole branch** (`main..domain-contract`), then the fixes, then the merge by pull request, the tag `v0.38.0` and
  `gh release create` (design §10 "The release"; plan 7 ends with what the release step does).
- **Live directives, passed on in every brief**: directive-1 (make the calls, merge and release when needed),
  directive-2 (no Claude Code memory; no ephemera in CLAUDE.md), directive-3 (`unset GH_TOKEN`; no agent-vault),
  directive-4 (move a file with `git mv`/`mv`, never `cp` then `rm`), directive-5 (operation and parameter names in
  business terms), directive-6 (request/response words, not "run"), directive-7 (mechanisms in decisions and adapter
  contracts, not in requirements).
- **Bootstrap** (design §10): the old reading (glossary and `## Terms` as the source of kinds, the CLI pack's
  run/option/print/exit) stays beside the new one on the branch until plan 5 deletes it. No `work decision` and no
  `work record` is run before plan 6 has the tree green.
- **Size**: every tracked Python file stays at 300 lines or fewer; a module that would pass it is split by the task
  that grows it, with its row in CLAUDE.md's module map in the same commit.
- **Module map**: each new module gets its row in CLAUDE.md in the commit that adds it (CLAUDE.md: "A new concern gets
  a new module and a row here"); nothing else is added to CLAUDE.md before plan 7.
- **Commit messages** end with the two attribution lines of the session that runs the phase.
- Until plan 6 renames it, the checking command is `scripts/model` (`model check`, `model logic`, ...). **Session's
  call**: the loop's `spec examine` (design §10) is the CLI command `spec logic` (the operation
  `specification.examine`; design §1 Non-goals keeps every command name but `model`'s).

## Goal

The two new file forms are read and checked, beside the glossary: `spec/model/<area>.md` (design §4.1) into a
`Model`, `spec/vocabulary/<area>.md` and `shared.md` (§4.2) into entries naming model elements, the area layers in
`spec_packs` and `spec_rgl_vocab`, the model's own rules and the vocabulary's rules in `model check`, and the records
policy rule. A context with no `spec/model/` reads exactly as today.

## Tasks, in order

0. **Baseline** (design §10 step 0), on the branch's first commit, by hand as supporting files of this record:
   `.shop/records/2026-11-19-domain-contract/baseline-logic.txt` (`python3 scripts/model logic` on the tree as
   branched: 15 findings, all L8) and `baseline-check.txt` (`python3 scripts/model check`: 0 violations, 140 warnings,
   2 file problems). Also `baseline-pytest.txt`: the last lines of `python3 -m pytest -q` (the count passed).
1. **Split `scripts/spec_lexicon.py` first** (300 lines): its entry problems (v_t4-v_t7, v_t9) to
   `scripts/spec_lexicon_problems.py`, re-exported where callers import them; no behaviour change; the suite green.
2. **`scripts/domain_model.py`**: the EBNF of §4.1 parsed into `Model` (objects, attributes with values/type/target,
   lifecycles, relations with cardinality, services, operations, parameters with their resolved type, outcomes with
   reasons, events, actors); a line that does not read refused through `shop_refused.Refused` naming file and line;
   `load(root)` reads every `spec/model/*.md` once per state of the files. Split into `domain_model_parse.py` if it
   passes 300.
3. **`scripts/domain_model_check.py`**: v_m8 (a relation to an undeclared object, a transition over an undeclared
   value, two operations of one name in a service, an event raised by no operation).
4. **`scripts/spec_vocabulary.py`**: entries with `→ <element>` resolved against `Model` (object, attribute, value,
   relation, lifecycle value, service, operation), their forms and thin frame, the layers of an area (its own,
   `shared.md`, the areas its model file `imports:`); v_t18 (no element), v_t19 (names none), v_t20 (two entries of one
   layer naming one element, not forms of each other), v_t21 (`imports: [cli]`; dormant until plan 2 adds the request
   pack, then switched on for a context with `spec/model/`).
5. **`spec_lexicon`** reads a context's terms through `spec_vocabulary` when `spec/model/` exists, else as today
   (bootstrap); kinds, attributes, values and transitions then come from `Model`, not from `Values:`/`Transitions:`/
   `Kind of:` (§4.2: those keys leave the vocabulary).
6. **`scripts/spec_packs.py`**: `layers` gains the area layers (one namespace per area, after the packs); **
   `scripts/spec_rgl_vocab.py`**: one vocabulary over every layer; a word naming two elements in two areas yields one
   term per element, suffixed by area (`finding_specification`, `finding_analysis`), so `spec_rgl` generates one GF
   function each (§4.2, session's call: one compiled grammar per context). `spec_relations` reads relations from the
   model when it exists.
7. **`scripts/model.lp`** and `scripts/model_spec.py`'s facts: v_m1 (a line's term names no element, through the
   vocabulary of its capability's `area:`), v_m8 and v_t18-v_t21 as facts from steps 3-4, and **v_r1** (design §8:
   an item's `source:` naming `record/...`; a violation on an item created after this rule, a warning on the existing
   ones; `backlog_items` refuses such a source on a new item). Each rule with its `% fail`/`% pass` examples;
   `python3 scripts/model rules --write` regenerates `grammar/rules.md`.
8. **Fixture** `tests/scripts/fixtures/domain-model/`: a small context (`spec/index.md` codified-2, `imports: []`,
   `spec/model/notes.md` with `object note`, `service notes` with `add(text)` and `list()`, a lifecycle, a relation;
   `spec/vocabulary/notes.md`, `shared.md`) plus one capability file with `area: notes`; its lines stay in words the
   fixture's vocabulary gives (no request yet).

## Tests to write first (red before each task)

- `tests/scripts/test_domain_model.py`: each production of §4.1's EBNF read (the design-decision example of the brief
  read whole); a parameter typed by attribute, by object, else text; a malformed line refused naming file and line.
- `tests/scripts/test_domain_model_check.py`: each v_m8 case caught, the fixture clean.
- `tests/scripts/test_spec_vocabulary.py`: each element kind resolved; v_t18, v_t19, v_t20 each caught; an area's
  layers; a two-area word giving two suffixed terms; a context without `spec/model/` read as today (the codified-2
  fixture's terms unchanged).
- `tests/scripts/test_records_policy.py`: v_r1 on a new item's `source: record/...` (refused by `backlog_items`), a
  warning on an existing one. (It is the `--enforced-by` of the decision "Records are kept, never cited", plan 6.)
- `tests/scripts/test_spec_lexicon_problems.py` only if the split moves tests; otherwise the existing lexicon tests
  stay green unchanged.

## Exit check

```
python3 scripts/tools size --limit 300                       # clean
python3 scripts/model check                                  # 0 violations; file problems = baseline-check.txt; warnings = it plus v_r1's on existing items (listed in the commit)
python3 scripts/model logic                                  # = baseline-logic.txt
python3 scripts/features generate --check && python3 scripts/features vocab --check
python3 scripts/model rules --check && python3 scripts/model forms --check && python3 scripts/model constructs --check
python3 -m pytest                                            # the full suite green; nothing skipped or xfailed by this phase
```
