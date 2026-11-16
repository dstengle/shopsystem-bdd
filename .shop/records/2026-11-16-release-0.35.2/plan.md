# Release 0.35.2: migrate records the version, orders after any act, and line commands

The person, 2026-11-16: "You can merge when you need to. Do releases when you need to." (quote-42). The release ships batch-39 (PR #61) and batch-40 (PR #62), and what the session did on main after them:

- b303: `migrate upgrade` writes, commits and pushes the plugin's version when the repository is behind it and no upgrade step is pending (feed's feedback item 8);
- b310: `model logic` and `features generate` no longer crash on "every K is not v" in a precondition;
- b14: `work line --reword` and `work line --remove` on an item's own lines;
- b203: laying an item's universal conditions with no `spec/universal.md` writes it as `codified-2`;
- b179: `work decision --supersedes`; on main, decisions 0094-0096 supersede 0086-0088, so `model decisions --check` exits 0;
- b271: `work line --retires <id> --no-line` retires a live requirement with nothing in its place;
- b300: "every K, ordered by ..." after any act whose verb's frame names the member's kind (feed's feedback item 5);
- `.shop/delivery.toml` (b173, this repository only): a batch review's checks run the batch tree's own scripts.

It is carried out on one branch `plan-release-0.35.2` by one fresh agent, then one fresh reviewer of the whole branch, then a pull request that the session merges, and the tag `v0.35.2` on its merge commit.

## Why 0.35.2

Design-decision 0092: z for a release with no upgrade step and no line reworded. Task 1 checks it: if any scenario `features generate` wrote at v0.35.1 for a line that still reads the same changes (b310 or b300 may touch the steps of existing lines), stop and say so in the reply, since that makes it 0.36.0.

## Tasks

1. **Check the bump.** `git diff v0.35.1 main -- features/` and read each changed scenario: only the new ids' scenarios may be new or changed. Name any other.
2. **Version.** `.claude-plugin/plugin.json` `version` and `.shop/plugin-version` set to `0.35.2`; every place that names the current release as 0.35.1 updated (`grep -rn "0\.35\.1"` outside CHANGELOG.md, docs/history/, .shop/, spec/ and tests/). Do not edit spec/ unless a test fails without it; say so if you do.
3. **CHANGELOG.md.** A section `## 0.35.2: migrate records the version, orders after any act, and line commands`, newest first, its link in the 0.35 row of the Line table. In the voice of the existing sections, one bullet per item with its PR (#61, #62); `.shop/delivery.toml` is this repository's own and not in the notes. An **Upgrading** bullet: no upgrade step; `migrate upgrade` now records the release even when nothing is pending.
4. **docs/upgrading.md.** A short section "From 0.35.1 to 0.35.2".
5. **Docs of the new commands.** `docs/reference/commands.md` names `work line --reword`, `--remove`, `--no-line` and `work decision --supersedes` where `work line` and `work decision` are described; `docs/writing-requirements.md` section 3's order paragraph no longer limits "every K, ordered by" to a verb whose frame takes `thing` (0.35.1's wording); `docs/recipes.md`'s "change a delivered line" names `--no-line` for a line retired with nothing in its place. Every line and Gherkin block you add or change passes the docs tests.
6. **Checks.** The whole suite passes (`python3 -m pytest -q -n auto`; a test known flaky under load, such as test_check_on_the_live_repo_is_fast_and_clean or test_byte_stable, rerun alone and named in the reply), `python3 scripts/tools check --base main`, `python3 scripts/tools size --limit 300`, `python3 scripts/features generate --check`, `python3 scripts/model rules --check`, `python3 scripts/model constructs --check`, `python3 scripts/model decisions --check` exit 0. Commit messages end with `Release: 0.35.2`.

## Not in this release

The ready items not yet built (b20, b316, b318, b317, b77, b65, b286, b309, b6, b315, b305, b296) and everything in the backlog.
