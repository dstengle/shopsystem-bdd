# Release 0.37.0: whole-spec faults caught before a batch, chores, new capabilities by command, and model logic's precision

The person, 2026-11-17: "It doesn't seem worth cutting a release with a large bug. Continue with batch-46 and then do a release" (b333 was the large bug); standing direction directive-1 ("You can merge when you need to. Do releases when you need to."). The release ships batch-43 (PR #66), batch-44 (PR #67), batch-45 (PR #68) and batch-46 (PR #69), and what the session did on main after v0.36.0:

- batch-43: b175 (a state verb in a response refused with its own reason), b296 (a count that restricts a written thing gets a counter-example), b305 (`work ready` names every failing line in one run), b314 (no false L1 between acts on objects whose restrictions exclude each other);
- batch-44: b20 (directives: `work directive`, `work directives`, `work promote`, `work drop`, the SessionStart hook), b315 (holds-exactly on a response's object with a relative clause reaching a second thing), b316 (a chore item: `work chore`, ready without requirement lines), b317 (every file form scaffolded by a command: `work line --capability`, `model forms --check`);
- batch-45: b289 was parked here and shipped in batch-46; b301 (the order phrase takes a comma before what follows), b323 (`work line --remove` reads which id a line retires from the item), b232 (model logic finds the clash of a negated restriction with a value it rules in);
- batch-46: b346 (shaping several items at once from the shipped `skills/shaping-items/parallel-brief.md`), b289 (no `git stash` in a batch's subagents), b324 (a park takes out an item's lines as they were laid), b333 (the readiness bar refuses every model check violation the lay brings; `work batch start` writes the corpus blocks and the catalogues).

It is carried out on one branch `plan-release-0.37.0` by one fresh agent, then one fresh reviewer of the whole branch, then a pull request that the session merges, and the tag `v0.37.0` on its merge commit.

## Why 0.37.0

Design-decision 0092: y for a release that rewords a delivered line or changes what a consumer must do; b333 retires readiness#r49 for a general line and changes what `work ready` refuses, b316/b317 add commands and a new item form, b20 adds hooks. Task 1 checks whether any upgrade step is needed (none is expected: no file form of a consumer changes shape); if one is, stop and say so in the reply.

## Tasks

1. **Check the bump.** `git diff v0.36.0 main -- features/ spec/capabilities/` and read each change: name each delivered line retired or reworded, and any scenario of a line that still reads the same that changed. Say whether a consumer needs an upgrade step (`migrate status` logic, `scripts/migrate_upgrade*.py`).
2. **Version.** `.claude-plugin/plugin.json` `version` and `.shop/plugin-version` set to `0.37.0`; every place that names the current release as 0.36.0 updated (`grep -rn "0\.36\.0"` outside CHANGELOG.md, docs/history/, .shop/, spec/ and tests/). Do not edit spec/ unless a test fails without it; say so if you do.
3. **CHANGELOG.md.** A section `## 0.37.0: whole-spec faults caught before a batch, chores, new capabilities by command, and model logic's precision`, newest first, a 0.37 row in the Line table. In the voice of the existing sections, one bullet per item with its PR (#66-#69), grouped as the section above groups them. `.shop/delivery.toml` and this repository's own records are not in the notes. An **Upgrading** bullet: what `work ready` now refuses that it did not (b333, b77's general form), the new commands, and the pins a consumer's tests need (`pytest==9.1.1`, `pytest-bdd==8.1.0`, as docs/getting-started.md already says; b256 is open).
4. **README.md.** Its requirements name the pytest and pytest-bdd versions above (b256's interim note).
5. **docs/upgrading.md.** A short section "From 0.36.0 to 0.37.0".
6. **Docs of the new commands.** `docs/reference/commands.md` covers `work directive`, `work directives`, `work promote`, `work drop`, `work chore`, `work line --capability` and `model forms --check` where their tools are described (the docs test requires every subcommand a heading); `docs/recipes.md` gains short recipes for a chore item and a new capability if none exists. Every line and Gherkin block you add or change passes the docs tests.
7. **Checks.** The whole suite passes (`python3 -m pytest -q -n auto`; a test known flaky under load, such as test_check_on_the_live_repo_is_fast_and_clean or test_byte_stable, rerun alone and named in the reply), `python3 scripts/tools check --base main`, `python3 scripts/tools size --limit 300`, `python3 scripts/features generate --check`, `python3 scripts/model rules --check`, `python3 scripts/model constructs --check`, `python3 scripts/model forms --check`, `python3 scripts/model decisions --check` exit 0 (name any that fails on main already, with its output, rather than fixing it outside this plan's scope). Commit messages end with `Release: 0.37.0`.

## Not in this release

The ready and shaped items not yet built (b318, b309, b334 and the rest), b347 and b349 (from batch-46's review), and the REST contract design (`.shop/records/2026-11-17-rest-contract/design.md`), not yet approved.
