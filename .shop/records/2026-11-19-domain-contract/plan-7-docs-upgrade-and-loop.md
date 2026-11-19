# Plan 7 of 7: docs, skills, the upgrade step, the release's files, and the loop until clean

Implementation plan for `design.md` (this folder), phase 7, the last implementation phase. Read plan 1's "The whole
branch" first.

## Goal

The docs, the notes-cli example, the skills and agents speak the new words; CLAUDE.md states the records policy;
consuming bounded contexts get the `migrate upgrade` step from 0.37.0 (design §9.6), proved on frozen 0.37 copies;
the release's files say 0.38.0; then the full check loop is run and fixed until every check is clean in one pass.

## Tasks, in order

1. **Frozen 0.37 inputs first** (§9.4): `tests/scripts/fixtures/upgrade-0.37/notes-cli/` and `.../docs-shop/` written
   from `git show main:docs/examples/notes-cli/...` and `git show main:tests/scripts/fixtures/docs-shop/...` (main is
   untouched by the branch), before task 4 migrates the originals.
2. **`scripts/migrate_upgrade_domain.py`** with **`scripts/migrate_upgrade_domain_report.py`**, step `("0.38.0", "the
   domain contract", ...)` registered beside the earlier `migrate_upgrade_*` steps. Mechanical: `spec/model/<context>.md`
   scaffolded from the glossary, `## Terms` and `## Relations` (nouns objects, attributes with values and
   `Transitions:` lifecycles, rows relations, one `service <tool>` per tool code the lines run, one operation per
   command code named the command minus the tool, parameters the options the lines give); `spec/vocabulary/<context>.md`
   and `shared.md` with each entry's `→ element`; `spec/adapters/cli.toml`; `imports: [cli]` → `[request]`; `##
   Glossary`, `## Terms`, `## Relations` emptied; `spec/moves.json` empty (`{}`). Reported by file and id (no line
   reworded, no new id): each line naming a command or an option (with the operation and parameters scaffolded), each
   `--json`/print/exit line, each `Kind of: tool` entry, each verb that should name an operation, each line naming git
   or GitHub acts. Reads `grammar/packs/cli.md` (deprecated) for the old words.
3. **This repository's `.shop/plugin-version`** 0.37.0 → 0.38.0; `.claude-plugin/plugin.json` version 0.38.0
   (marketplace.json has no version field).
4. **`docs/examples/notes-cli/`** migrated by the new step then reworded by hand (§9.5: `object note`, `service notes`
   with add, list; "When the person adds a note with the text `x`, the notes service shall keep the note"; its
   `cli.toml`; its feature regenerated); `tests/scripts/fixtures/docs-shop/` and `docs-labels/` likewise.
5. **Docs** (§9.5): README, `docs/concepts.md`, `how-it-works.md`, `writing-requirements.md`, `capability-format.md`,
   `getting-started.md`, `tour.md`, `recipes.md`, `troubleshooting.md`, `upgrading.md` (the 0.38.0 step: what it
   scaffolds, what a session rewords, that `spec check` refuses unreworded lines with v_m1 and `imports: [cli]` with
   v_t21), `docs/reference/commands.md` (`spec` for `model`, the alias, each converted command's `--json` envelope),
   new `docs/reference/domain-model.md` (§4.1's syntax, §4.2's vocabulary entries) and `docs/reference/adapters.md`
   (§6.1). Every requirement line and Gherkin block in the docs reads in its context (test_docs_lines).
6. **Skills and agents** (§9.5): `skills/raising-a-request`, `building-a-batch`, `shaping-items` (and its parallel
   brief), `taking-in-a-request`, `analyzing-a-batch`, `agents/pr-reviewer.md`, `agents/trial-runner.md`: every
   CLI-pack line rewritten in request words; `tests/scripts/test_agents.py`, `test_skill_shaping_items.py` follow.
7. **CLAUDE.md** (§8; directive-2: nothing ephemeral): the design/plan rule becomes "A design is reported as a
   record; its decisions are written as design-decisions, model changes and item lines. A plan is a batch's tasks; a
   plan file is a report."; add "No artifact of the system cites a record."; `model forms` → `spec forms` and every
   rule naming `model`; the module map checked whole against `scripts/` (rows of every module added on the branch,
   removed modules' rows dropped).
8. **CHANGELOG.md** `## 0.38.0: the domain contract` with its table row: the model, the vocabulary, operations with
   parameters, the request pack (cli retired from lines), the envelope, the CLI adapter contract and check, `spec` for
   `model` (alias for one release), the upgrade step; a **Breaking** heading naming each command whose `--json` shape
   changed and that its old payload is under `content` (from `driven-commands.txt`), `imports: [cli]` refused, the
   alias.
9. **The loop until clean** (below), fixing what each check finds, repeated until one full pass is clean; then push.

## Tests to write first

- `tests/scripts/test_migrate_upgrade_domain.py`: on copies of `fixtures/upgrade-0.37/notes-cli` and `docs-shop`,
  `migrate upgrade` writes the scaffold (model, vocabulary, cli.toml, imports) and the report naming each line to
  reword by file and id; a second run changes nothing; then a hand-reworded copy (kept as
  `tests/scripts/fixtures/upgrade-0.37/notes-cli-reworded/`) passes `spec check`, `features generate --check` and
  `spec logic` with no finding (design §10 Definition of done).
- `tests/scripts/test_docs.py` and `test_docs_lines.py` run red on the old docs first, then green.

## Exit check: the full loop, every check clean in one pass

```
python3 scripts/spec check                       # 0 violations (v_p*, v_m*, v_a*, v_t18-21, v_r1)
python3 scripts/spec logic                       # no finding not in baseline-logic.txt (ids mapped by spec/moves.json)
python3 scripts/features generate --check        # every group of every capability has its scenario
python3 scripts/features vocab --check           # every step has a handler
python3 -m pytest                                # the full suite, docs test included; nothing ignored, no xfail of this branch
python3 scripts/tools size --limit 300           # no file over the limit
python3 scripts/spec forms --check; python3 scripts/spec rules --check; python3 scripts/spec constructs --check
python3 scripts/spec decisions --check
python3 scripts/migrate status                   # this repository at 0.38.0, nothing pending
```

## After this phase (not the implementer's)

One fresh reviewer of the whole branch (`git diff main...domain-contract`), given `design.md`, these plans,
`shims.txt` and the live directives; its report kept by `work record` as `.shop/records/<date>-release-0.38.0-reviewed.md`
once the fixes are in. Then a fresh fixer for its findings with the loop above re-run clean; then the merge by a pull
request (`gh pr create`, `GH_TOKEN` unset, merged by the session per directive-1), the tag `v0.38.0` pushed, `gh
release create v0.38.0` with the CHANGELOG section as its note; then the contract artifact (design §10 "Then").
