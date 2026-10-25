/tmp/work-run-i35-5vwjz_3l/i35-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | note sentence |
|---|---|---|---|---|
| changed | supervision | r73 | **When** `work run` drafts a work-item, `work run` shall list under the work-item's `## Retires` each deprecated scenario whose `Deprecated for:` line names a scenario of a requirement the work-item accepts. (old: **When** `work run` drafts a work-item for a `formulated` capability-proposal, `work run` shall list under the work-item's `## Retires` each scenario tagged `@deprecated` whose `@r<n>` tag names a requirement the work-item accepts.) | "1. **When** `work run` drafts a work-item, `work run` shall list under its `## Retires` each `@deprecated` scenario whose `Deprecated for:` names a scenario of a requirement the work-item accepts." |
| added | supervision | r123 | **When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft one work-item that retires each deprecated scenario whose replacement's work-item is `green`. | "2. **When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft one work-item that retires each `@deprecated` scenario whose replacement's work-item is `green`." |

No glossary term added, changed or removed ("`@deprecated` scenario" is written with the existing term **deprecated scenario**). No decision file.

## Questions

1. supervision r73: is the old `@r<n>` criterion replaced by the `Deprecated for:` one, or kept beside it? Replaced (recommended): r73 as drafted. Kept: **When** `work run` drafts a work-item, `work run` shall list under the work-item's `## Retires` each deprecated scenario whose `Deprecated for:` line names a scenario of a requirement the work-item accepts or whose `@r<n>` tag names a requirement the work-item accepts.
2. supervision r123: when no deprecated scenario has a replacement whose work-item is `green`, is a work-item still drafted? No (recommended, a test can check): **When** every work-item of an initiative is `green` or `withdrawn` and a deprecated scenario's replacement's work-item is `green`, `work run` shall draft one work-item that retires each deprecated scenario whose replacement's work-item is `green`. Yes: r123 as drafted.
3. supervision r123: is "replacement's work-item" a work-item of that initiative, or of any initiative? That initiative (recommended): ... each deprecated scenario whose replacement's work-item is a `green` work-item of the initiative. Any: r123 as drafted.
4. supervision r123: under which capability-proposal is the retiring work-item drafted? Under the capability-proposal of the replacement's work-item drafted last: ... `work run` shall draft one work-item, under the capability-proposal of the last-drafted work-item whose replacement scenario it retires, that retires ... . Under the initiative's last formulated capability-proposal: ... `work run` shall draft one work-item, under the initiative's last `formulated` capability-proposal, that retires ... .
5. supervision r123 against r27 and r75: is the retiring work-item drafted before the branch review starts and before `measure initiative` runs? Yes (recommended): **When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft the work-item r123 names before it starts a branch review or runs `measure initiative`. No: no line.
6. supervision r73 and r123: a deprecated scenario whose `Deprecated for:` is `removal` names no replacement; is it retired by a work-item? No (recommended, as the note gives): no line. Yes: **When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall list under the `## Retires` of the work-item r123 names each deprecated scenario deprecated for removal of a requirement a capability-proposal of the initiative removes.

## Cut sentences

- "Deprecated scenarios retired with their replacements" (the note's title)
