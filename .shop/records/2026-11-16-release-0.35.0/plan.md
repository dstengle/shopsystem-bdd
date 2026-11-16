---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-16-release-0.35.0
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-16
---

# Release 0.35.0: collections, comparisons and orders

The person, 2026-11-16: "Please follow through on merging pull requests and continuing work until the comparison and collections work is released". The release ships what batches 34 to 37 delivered:

- batch-34 (PR #54): b268, b272, b273, b274, and the late fixes reviewed in .shop/records/2026-11-15-batch-34-late-fixes-review.md;
- batch-35 (PR #55): b275;
- batch-36 (PR #56): b285, b287, b288;
- batch-37: b284.

It is carried out on one branch `plan-release-0.35.0` by one fresh agent, then one fresh reviewer of the whole branch, then a pull request that the session merges, and the tag `v0.35.0` on its merge commit.

## Why 0.35.0, not 0.34.2

Design-decision 0092 and docs/upgrading.md's Versions section: y goes up for a change that needs rewording lines or `migrate upgrade`, or that removes a command. This release changes no file format and needs no upgrade step. But a consuming repository's regenerated features change in two ways that its handlers must meet:

- the Thens of a response's thing now come after the act that brings the thing in (b268);
- every, only and count lines get counter-examples (b273): Givens of a thing that fails the restriction or is one past the bound, with negated Thens.

Its step handlers can fail on both until they are updated, as about 15 of this repository's did. That is an incompatible change, so it is a y release.

## Tasks

1. **Version.** `.claude-plugin/plugin.json` `version` and `.shop/plugin-version` set to `0.35.0`. Every place that names the current release as 0.34.1 is updated: README.md, docs/getting-started.md and docs/upgrading.md (`grep -rn "0\.34\.1"` outside CHANGELOG.md, docs/history/, .shop/, spec/ and tests/; a spec line or given block naming 0.34.1 is example data and stays). The term "release (attribute of tool)" in spec/capabilities/migration-tools.md lists the plugin's release among its values. Say in the reply whether it must list `0.35.0`, and whether anything fails if it does not. Do not edit spec/ unless a test fails without the change; say so if you do.
2. **CHANGELOG.md.** A section `## 0.35.0: collections, comparisons and orders`, newest first, with a row for 0.35 in the Line table. Write it in the voice of the existing sections, one bullet per change, each with its item and PR:
   - `model logic` and `features generate` read only and a count over a relation in a response, and `model logic` names each requirement it has no translation of (`unread <id>: ...`) instead of printing `no findings` (b272).
   - Generated scenarios that can fail: counter-examples for every, only and counts, the Givens of every in a condition and of two Ks (b273).
   - Exact membership (`holds-exactly`), a collection that holds nothing (`nothing`), and membership from the member's side (`is-in`) (b274).
   - The Thens of a response's thing after the act that brings it in (b268).
   - Value order and `Type: number|time|text` on an attribute. Two things' values compared (`value-compare`, `value-same`), also across two senses of one word (b275, b287). An order, `ordered by <attribute>, in ascending order` or `in descending order`, on a collection (`order-by`) or a printed every (`order-by-every`), kept as one atom, two opposite orders an L1, and the scenario's Then checked by a sorted comparison (b275, b288). An order refused in a precondition, a trigger and under "shall not" (b285).
   - migration-tools' release lines compare the repository's release with the release of `migrate` (b284).
   - An **Upgrading** bullet pointing to docs/upgrading.md's new section.
3. **docs/upgrading.md.** A section for 0.34.1 → 0.35.0. No upgrade step. Run `features generate` and update the step handlers:
   - a Then that read a thing before the act that brings it in now runs after that act;
   - each negated counter-example Then needs a handler that brings its thing into the world and checks the output for it;
   - `model logic` may now print `unread <id>` for lines it skipped silently before.
   Also: the new `Type:` field, and that an order or a comparison on an attribute with no value order is refused. This covers backlog item b278's note, so b278 is withdrawn once the release is merged.
4. **docs/writing-requirements.md.** The user docs must show the new constructs where a writer looks for them: membership and size (holds, is in, holds exactly, holds nothing, at least/at most/exactly, the number of Ks), comparing two things' values, and an order, each with one line that parses in docs/examples/notes-cli/'s context, or in this repository's, as the docs test reads it (tests/scripts/test_docs_lines.py). Move what section 6 ("What the language cannot say yet") listed and is now sayable out of it. Read grammar/language.md and grammar/constructs.md for the exact forms. Keep the page's voice. Every requirement line and Gherkin block you add must pass the docs tests.
5. **Checks.** The whole suite passes (`python3 -m pytest -q -n auto`), `python3 scripts/tools check --base main`, `python3 scripts/tools size --limit 300`, `python3 scripts/features generate --check`, `python3 scripts/model rules --check` and `python3 scripts/model constructs --check` exit 0. Commit messages end with `Release: 0.35.0`.

## Not in this release

Position (first, last, top n), uniqueness, aggregates, a then-by key, and number words between two values. Also backlog items b277, b280-b283, b286 and b289-b293.
