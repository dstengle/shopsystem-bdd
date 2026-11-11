# The version reset to 0.y.z (b264) Plan

**Goal:** the plugin's releases made as 1.0.0-4.1.0 are renumbered into the 0.y.z series of design-decision 0092
("Versions are 0.y.z until 1.0"), continuing the tagged 0.1-0.29 releases, and the next release is 0.34.1
(the person, quote-27 and quote-28; `.shop/backlog/b264.md`). Alpha: no translation of an old number in `migrate`.

**Branch:** `plan-version-reset` from `origin/main`, worktree `.shop/worktrees/plan-version-reset`; one implementer
doing every section in order, test first where a test names a version, then one fresh reviewer of the whole branch.
The main session opens the pull request, merges it once the review is clean, and adds the tags (section 7).

## The mapping

The item lists the majors; the minors between them follow decision 0092 (z for a non-breaking update):

| released as | becomes |
|---|---|
| 1.0.0 codified requirements | 0.30.0 |
| 2.0.0 the workflow simplified | 0.31.0 |
| 2.1.0 requests exchanged through GitHub issues | 0.31.1 |
| 2.2.0 decisions and records written by command | 0.31.2 |
| 2.3.0 work pushes its commits ... | 0.31.3 |
| 2.3.1 a batch runs in one fresh agent ... | 0.31.4 |
| 2.4.0 the request watch wakes on GitHub's events ... | 0.31.5 |
| 3.0.0 verb frames | 0.32.0 |
| 3.0.1 the scenario of a negated response with a recipient | 0.32.1 |
| 4.0.0 the controlled language 4 | 0.33.0 |
| 4.1.0 value kinds | 0.34.0 |
| this release: the Given fix of PR #51 and the reset | 0.34.1 |

## 1. The version

`.claude-plugin/plugin.json` and `.shop/plugin-version`: `0.34.1`.

## 2. migrate

`scripts/migrate_upgrade.py`'s `STEPS` keyed 0.30.0 (codified requirements), 0.31.0 (the workflow simplified),
0.32.0 (verb frames), 0.33.0 (the controlled language 4), 0.34.0 (value kinds); `number()` and every comparison
unchanged in kind (tuples of ints already order 0.34.0 above 0.29.0). Every other place in `scripts/` and `hooks/`
that names 1.0.0-4.1.0 (an upgrade step module's docstring, `migrate status`'s and its SessionStart hook's text, a
version check in another step) is renamed. A repository that records 1.0.0-4.1.0 now reads as above the plugin; that
is accepted (alpha): docs/upgrading.md says to rewrite `.shop/plugin-version` by hand with the table above. The
tests under `tests/scripts/` that name these versions follow.

## 3. migration-tools

`spec/capabilities/migration-tools.md`: the release values (an attribute of repository and of upgrade step, its
`Values (noun):` and `Order: by number.`) renamed; every line, given block and example data naming 1.0.0-4.1.0 (or
a version above the plugin's, such as 9.0.0, when it means "above the plugin": keep one above 0.34.1, and prefer a
0.y.z value) rewritten: a changed line gets a new id via `work line` on b264 or by the spec's own rules, the old id
into `retired:` (requirements are never edited in place); a given block or a term entry is not a requirement and
is edited. The spec corpus blocks (`grammar/corpus/spec/`) of changed lines first, then `features generate` for
the feature, then the handlers (`tests/scenarios/migration_tools_handlers*.py`, `migration_tools_world*.py`) that
read a version. Lines elsewhere in `spec/` that name a plugin version follow the same rule.

## 4. Docs

- CHANGELOG.md: each heading 1.0.0-4.1.0 renamed with its old number in brackets, e.g.
  `## 0.33.0 (released as 4.0.0): the controlled language 4`; a new top section `## 0.34.1: the version reset and
  the Givens of a trigger's referents` saying the renumbering (the table), the Given fix of PR #51 (b263's
  generator change: a Given for each referent of the trigger's event, `scripts/spec_steps4.py`), and that a
  consumer rewrites its `.shop/plugin-version` by hand and reinstalls the plugin. The body text of old sections
  that names a version (e.g. "from 3.x") reads the new numbers, with the old in brackets on first use only where
  needed for sense.
- README.md and docs/getting-started.md: install paths (`~/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/<version>/`)
  and any "plugin 4.x" wording.
- docs/upgrading.md: its sections ("From 4.0 to 4.1" ...) renamed in the new numbers; a section on versioning
  stating decision 0092 (y for a large or incompatible change, counting past .9 to .10; z for a non-breaking
  update; 1.0.0 a decision of its own) and the old-to-new table, with the hand rewrite of `.shop/plugin-version`.
- docs/reference/commands.md, how-it-works, troubleshooting, talking-with-claude, recipes, concepts, tour,
  capability-file, writing-requirements, index, capability-format, design-model, examples/notes-cli/README.md, the
  skills (shaping-items, raising-a-request, taking-in-a-request) and grammar/language.md, rules.md, constructs.md:
  only where a number names a plugin release ("plugin 4.0", "since 4.1", "upgrading from 3.x"). A version that is
  example data (a release `3.0.0` of a sketch context, an attribute's value) is left alone. `grammar/rules.md` and
  `grammar/constructs.md` are generated: change their sources and run `model rules --write`, `model constructs
  --write`.
- `docs/history/` is history: unchanged.

## 5. The release process

Where docs or skills say how to cut a release or which number to bump (grep `plugin.json`, `bump`, `major`,
`minor`, `release`), they follow decision 0092. If no place says it, docs/upgrading.md's versioning section is it.

## 6. Not changed

`.shop/records/`, `.shop/backlog/` notes, `.shop/quotes/`, `spec/decisions/` text, `docs/history/`, git history.

## 7. Tags (main session, after the merge)

Lightweight tags on main's first-parent history: each `v0.y.z` of the table on the first first-parent commit of
main whose `.claude-plugin/plugin.json` holds the old version (1.0.0 at 1fab1b29f's merge, 2.0.0, 2.1.0, 2.2.0,
2.3.0, 2.3.1, 2.4.0, 3.0.0, 3.0.1, 4.0.0, 4.1.0), and `v0.34.1` on this plan's merge; pushed.

## 8. The gate

The suite (`timeout 1500 python3 -m pytest -q -n 8`), `model check`, `model logic`, `features generate --check`,
`features vocab --check`, the corpus and docs tests, `model rules --check`, `model constructs --check`,
`tools size --limit 300` and `tools check`; a grep that finds no `[1-4]\.[0-9]+\.[0-9]+` naming a plugin release
outside sections 6's paths and CHANGELOG's bracketed old numbers.

After the merge the person reinstalls the plugin once (Claude Code keys installs by version and may not move from
4.1.0 down to 0.34.1).
