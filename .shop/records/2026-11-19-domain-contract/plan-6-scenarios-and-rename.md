# Plan 6 of 7: the scenarios driven through the CLI adapter, `model` renamed `spec`, the decisions

Implementation plan for `design.md` (this folder), phase 6. Read plan 1's "The whole branch" first.

## Goal

Every generated scenario of the 22 new capabilities runs: its Whens through `driver_cli`, handlers keyed on the
operation, Thens checking the envelope (design §6.2, §9.4); the U17 check after a scenario; `model` renamed `spec`
with a one-release alias (§10 step 6); then, with the tree green, the design-decisions of §7 and the follow-up items
by `work decision` and `work idea`.

## Tasks, in order

1. **`tests/scenarios/vocab4.py`, `tests/scenarios/vocab.py`**: step definitions for `WhenRequests` and the new Then
   templates; the U12/U13/U16 checks after a scenario become U17 (the envelope's errors carry a reason; the store
   changed nothing), U13's check now `scripts/store_git.py`'s (plan 4).
2. **Scenario modules moved** (§9.4, directive-4): each `tests/scenarios/test_<old>.py` and its
   `<old>_handlers*.py`/`<old>_world.py` moved with `git mv` to the new capability that takes most of it, the rest cut
   out by editing into the other new capabilities' files (never `cp` then `rm`); a `test_<capability>.py` for each
   of the 22 features. Handlers keyed on `("WhenRuns", "<command code>")` re-keyed on `("WhenRequests",
   "<service>.<operation>")` through `cli.toml`, driving through `driver_cli`; Givens that build the world unchanged;
   `tests/scenarios/world_four.py`'s chains keyed on the operation id; `world_run.py`, `world_refusal.py`,
   `world_cli.py`, `world_fallbacks.py` adapted (the CLI pack's acts become the request pack's).
3. **Trace marks**: the 19 `@pytest.mark.requirement("cap#rN")` marks remapped through `spec/moves.json`
   (`tests/scripts/test_pr_review_trace.py` follows).
4. **Inline lines in tests**: every remaining "runs \`" line under `tests/scripts` and `tests/scenarios` rewritten in
   request words (`grep -rln 'runs `' tests` empty but the upgrade-step tests of plan 7 and the frozen fixtures).
5. **`model` renamed `spec`**: `git mv scripts/model scripts/spec`; a new two-line `scripts/model` alias printing a
   deprecation notice on stderr and calling `scripts/spec`; every caller updated: `hooks/hooks.json`, skills and agents
   (the name only; their grammar is plan 7's), `docs/` command names (plan 7 rewrites the prose), CLAUDE.md's rules
   naming `model`, `scripts/migrate_layout.py:127`, `.shop/delivery.toml`'s `[review] checks`,
   `tests/scripts/docs_testing.py`'s `TOOLS`, `tests/scripts/conftest.py`'s `run("model", ...)`, the 42 test files
   naming it. `grep -rn "scripts/model\b\|\"model\"" scripts tests .shop/delivery.toml hooks skills agents` clean
   but the alias and its test. The `model_*.py` module names stay (imports, not the command).
6. **`python3 scripts/features vocab --check`** clean: every step of every feature has a handler.
7. **Once the full suite is green** (and not before: bootstrap rule), the decisions of §7 by `work decision` with the
   tiers and `--enforced-by` the table gives: "The CLI is an adapter" (check, `tests/scripts/test_adapter_cli_check.py`),
   "GitHub issues carry context requests", "Pull requests carry a batch's change to review", "Git is the store and the
   isolation" (check, `tests/scripts/test_store_git.py`; U13 retires into it), "Files under spec/ and .shop/ are the
   storage", "Hooks are a driving adapter", "The response envelope" (check, `tests/scripts/test_domain_envelope.py`;
   U16 retires into it), "Domain words for the store's acts", "Records are kept, never cited" (check,
   `tests/scripts/test_records_policy.py`), "The specification has four parts" (rests on final-layout), "One reword
   for the domain contract" (judgement). Then by `work idea`: "the envelope on every command" (§6.1), "spec model
   commands" (the writer of the domain model form), "adapter contract commands", each named where `model_forms.FORMS`
   (now `spec forms`) cites it.

## Tests to write first

- `tests/scripts/test_spec_alias.py`: `scripts/model check` prints the deprecation notice on stderr and the same
  stdout and exit as `scripts/spec check`.
- A scenario test per new capability is the generated feature itself: run `python3 -m pytest tests/scenarios/
  test_decisions.py` red first, then re-key; repeat capability by capability.
- `tests/scripts/test_vocab_u17.py`: the after-scenario check fails a refusal with no reason and a refusal that changed
  the store.

## Exit check

```
python3 scripts/tools size --limit 300
python3 scripts/spec check                       # 0 violations (the decisions' --enforced-by tests exist)
python3 scripts/spec logic                       # no finding not in baseline-logic.txt (mapped by moves.json)
python3 scripts/features generate --check && python3 scripts/features vocab --check
python3 scripts/spec forms --check && python3 scripts/spec rules --check && python3 scripts/spec constructs --check
python3 scripts/spec decisions --check
python3 -m pytest --ignore=tests/scripts/test_docs.py --ignore=tests/scripts/test_docs_lines.py \
  --ignore=tests/scripts/test_agents.py --ignore=tests/scripts/test_skill_shaping_items.py
```

Left for plan 7 only: the four ignored test files, each only if it fails.
