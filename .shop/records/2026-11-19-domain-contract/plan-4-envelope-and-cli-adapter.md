# Plan 4 of 7: the response envelope, the CLI adapter contract, the protocol driver, the lay into the model

Implementation plan for `design.md` (this folder), phase 4. Read plan 1's "The whole branch" first.

## Goal

Every operation answers with one envelope (design §5.4); refusals name business references; the commands a scenario
requests print the envelope under `--json`, their core functions callable by business-named keyword parameters
(§6.3); the CLI adapter contract is read and checked both ways against argparse (§6.1); `driver_cli` turns a request
into argv and the envelope back (§6.2); `work line` and the readiness bar lay model lines and vocabulary entries into
`spec/model/` and `spec/vocabulary/` (§10 build tasks). All of it is proved on fixtures; this repository's own
`spec/adapters/cli.toml` is written in plan 5 with its model.

## Tasks, in order

1. **`scripts/domain_envelope.py`**: `Response(outcome, content, errors, notices)`; outcomes `done`, `returned`,
   `refused`, `passed`, `failed`, and `broken` outside the domain; `errors` each `{reason, names}` by business
   reference (`parameter:tier`, `item:b12`, `rule:v_d6`); `errors` non-empty iff refused or failed; JSON rendering.
2. **`scripts/shop_refused.py`**: `Refused` gains `reason` and `names` beside its message (standard library only, as
   today); every existing raise keeps working (defaults).
3. **The list of operations a scenario requests**: read off today's handlers keyed on `WhenRuns` and the command
   codes the live features run (`grep -rn "WhenRuns" tests/scenarios`, the features' "runs \`...\`" steps); written as
   the supporting file `.shop/records/2026-11-19-domain-contract/driven-commands.txt` (one command a line), the scope
   of tasks 4-5 (session's call (person offline) §6.3: only these).
4. **Core functions by business name** for each command of that list: argv → `Request(operation, params)` → the core
   function with keyword parameters by business name → `Response` → rendering (human table as today; `--json` the
   envelope, the old payload whole under `content`). E.g. `scripts/decision_write.py`'s `write(args)` becomes
   `write(root, title, summary, tier, wording, ...)`, its refusals naming `parameter:summary`. An `as_namespace` shim
   is allowed only where the conversion would push a file over 300 lines; each use is listed in
   `.shop/records/2026-11-19-domain-contract/shims.txt` for the reviewer. Tests reading the old `--json` shapes
   (`test_decision_checks`, the `features list --json`, `work backlog --json`, `work batch status --json` tests, ...)
   read `content`.
5. **`scripts/adapter_cli.py`** (read `spec/adapters/cli.toml` with `tomllib`: `[outcomes]`, `[operations."S.O"]`
   with `command` or `hook`, `parameters` (positional, option, repeat, example), `cli-only`, `[unexposed]`,
   `[environment]`; translate business references to CLI spellings for human messages) and
   **`scripts/adapter_cli_check.py`** (v_a1 an operation with no table and not unexposed; v_a2 a table naming no real
   operation or parameter; v_a3 a command or option argparse lacks, the parsers caught as `tests/scripts/
   docs_testing.py` catches them; v_a4 an argparse subcommand or option no table names and not `cli-only`: `--root`,
   `--json`, `--hook`, `--every`). Wired into `model check` (facts in `scripts/model_spec.py`, rules in
   `scripts/model.lp`), active only when `spec/adapters/cli.toml` exists.
6. **`tests/scenarios/driver_cli.py`**: from an operation and a step's params, argv by `cli.toml` (the examples for
   required parameters a step leaves out), the command run with `--json`, the `Response` returned; a helper for the
   Thens (`refused` with the named references, `returned` content, `kept` through the store check of task 7).
7. **`scripts/store_git.py`**: the store adapter's checks used by the driver's `ThenKeeps` and by the decision "Git is
   the store and the isolation": a thing kept is one commit of its named files on the branch checked out; shared when
   that commit is on the upstream remote (U13's check, moved out of `tests/scenarios/vocab.py` in plan 6).
8. **The lay into the model and the vocabulary**: `scripts/backlog_section.py` (an item's `### <area> model` block
   lines and vocabulary entries read and written byte-stable), `scripts/backlog_lines.py`, `scripts/backlog_forms.py`
   (`work line --relation` writes a model relation line into the item, laid into `spec/model/<area>.md`; a vocabulary
   entry laid into `spec/vocabulary/<area>.md`), `scripts/readiness_bar.py`'s lay and unlay, same discipline as today.
   `scripts/model_forms.py` `FORMS`: domain model area, vocabulary term, adapter contract, capability moves (§4.5),
   minus glossary term, glossary relation row, relation row; each new form names its writer (the `work idea` items
   are raised in plan 6, named here by title).
9. **Fixture** `tests/scripts/fixtures/domain-model/` gains `spec/adapters/cli.toml` for a tiny stand-in program
   (`tests/scripts/fixtures/domain-model/notes_cli.py`, argparse, `--json` envelope) and request-word lines.

## Tests to write first

- `tests/scripts/test_domain_envelope.py`: the four fields; errors iff refused/failed; `broken` never a domain
  outcome; JSON shape. (The `--enforced-by` of the decision "The response envelope", plan 6.)
- `tests/scripts/test_adapter_cli_check.py`: v_a1-v_a4 each caught on a broken copy of the fixture's `cli.toml` or
  stand-in parser; the fixture clean; a business reference rendered as its option. (The `--enforced-by` of "The CLI is
  an adapter".)
- `tests/scripts/test_driver_cli.py`: argv built from a request (positional, option, repeat, example filled in); the
  envelope read back for done, returned, refused.
- `tests/scripts/test_store_git.py`: kept and shared, kept not shared, nothing kept on a refusal. (The `--enforced-by`
  of "Git is the store and the isolation".)
- `tests/scripts/test_decision_write.py` gains `write(...)` by keyword and a refusal naming `parameter:summary`; one
  `--json` envelope test per converted command.
- `tests/scripts/test_readiness_lay_model.py`: an item with a model line, a vocabulary entry and a requirement line on
  the domain-model fixture passes `work ready`; unlay leaves the fixture byte-identical.

## Exit check

```
python3 scripts/tools size --limit 300
python3 scripts/model check                      # as at plan 1's exit
python3 scripts/model logic                      # = baseline-logic.txt
python3 scripts/features generate --check && python3 scripts/features vocab --check
python3 scripts/model rules --check && python3 scripts/model forms --check && python3 scripts/model constructs --check
python3 -m pytest                                # the full suite green (old --json readers moved to `content`)
```
