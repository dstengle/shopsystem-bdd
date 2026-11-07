---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-18/review-1
kind: review
batch: batch-18
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/31
head: bc468091afb0a35281da620b02a162bc41d6423c
range: 6aa87f27c92af309c8978fd69c2bce577a51c770..bc468091afb0a35281da620b02a162bc41d6423c
result: clean
---

# batch-18 review 1

## Verdict

The batch builds b87's one line, migration-tools#r25, and I found nothing that needs fixing now. When the repository's version is after 1.0.0 and before 3.0.0, `migrate upgrade` runs the new 3.0.0 step "verb frames". That step rewrites `spec/index.md`, printing "verb frames" in its summary, and prints a `verb frames: v_t11 …` note for each verb that has no `Frame:`.

The plugin version goes to 3.0.0 in `.claude-plugin/plugin.json`, the README has its 3.0.0 section, and `CLAUDE.md` has a module-map row for `scripts/migrate_upgrade_frames.py`. Every check in the brief exits 0 at the head, as it did at the base. The feature changes are what `features generate --check` expects. No test is removed or weakened: the `spec/index.md` check in `tests/scenarios/migration_tools_handlers.py` still does its old test for `migrate run`, and only an upgrade scenario gets the stricter test that each category became its part of speech.

The given blocks of g14 and g19 now say "3.0.0" where they said "2.4.0". Only the example data changed, not the requirement lines, and the item's notes ask for it, so design-decision 0085 is met. The change is 239 lines against a limit of 1000.

## Findings

### f1 Minor observation: a term entry whose bullet wraps before its label is not relabelled
- item: b87
- where: scripts/migrate_upgrade_frames.py:160
`LABEL` checks one physical line at a time. `spec_lexicon._bullets` joins a bullet's indented continuation lines before it reads an entry. So an entry like this keeps its 2.x category:

```
- **work
  item** (kind): ...
```

`spec_lexicon` then reads that term as having no part of speech. Its v_t4 is not one of the codes the step prints. `spec_grammar.Unlabelled` makes `unparsed` print one line, "the requirements could not be parsed: …", instead of naming each line that no longer parses. The upgrade does not crash (`Unlabelled` is a subclass of `GrammarError`, which is caught at line 206), and the refusal names the term with the label it is to carry. No consumer spec is known to wrap a term's name today, so this is hardening only. To reproduce: write a `## Glossary` bullet whose `**term**` spans two lines and run `plan`; the entry keeps its old category.
