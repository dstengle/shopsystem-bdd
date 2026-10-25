# Gate: i35, round 1 (supervision)

Draft: .shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## supervision

### Changed
- [r73] **When** `work run` drafts a work-item, `work run` shall list under the work-item's `## Retires` each deprecated scenario whose `Deprecated for:` line names a scenario of a requirement the work-item accepts.
  - was: **When** `work run` drafts a work-item for a `formulated` capability-proposal, `work run` shall list under the work-item's `## Retires` each scenario tagged `@deprecated` whose `@r<n>` tag names a requirement the work-item accepts.

### Added
- [r123] **When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft one work-item that retires each deprecated scenario whose replacement's work-item is `green`.

No glossary entry, no decision, no removal.

## Questions
1. r73: is the old `@r<n>` criterion replaced by `Deprecated for:`, or kept beside it? Replaced (recommended): r73 as drafted. Kept: r73 reads "... each deprecated scenario whose `Deprecated for:` line names a scenario of a requirement the work-item accepts or whose `@r<n>` tag names a requirement the work-item accepts."
2. r123: when no deprecated scenario has a replacement whose work-item is `green`, is a work-item still drafted? No (recommended): r123 gains "and a deprecated scenario's replacement's work-item is `green`" after its condition. Yes: r123 as drafted.
3. r123: is "replacement's work-item" a work-item of that initiative, or of any? That initiative (recommended): "... whose replacement's work-item is a `green` work-item of the initiative". Any: r123 as drafted.
4. r123: under which capability-proposal is the retiring work-item drafted? Under the capability-proposal of the last-drafted work-item whose replacement it retires; or under the initiative's last `formulated` capability-proposal.
5. r123 against r27 and r75: is the retiring work-item drafted before the branch review starts and `measure initiative` runs? Yes (recommended): add a line "**When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft the work-item r123 names before it starts a branch review or runs `measure initiative`." No: no line.
6. r73/r123: a scenario deprecated with `Deprecated for: removal` names no replacement; is it retired by a work-item? No (recommended, as the note gives): no line. Yes: a line listing it under the r123 work-item's `## Retires` when a capability-proposal of the initiative removes its requirement.

## Cut sentences
- "Deprecated scenarios retired with their replacements" (the note's title)
