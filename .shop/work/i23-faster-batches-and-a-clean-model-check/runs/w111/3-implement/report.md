## Budget

- skills/delivering-an-initiative/SKILL.md

## Changed

SKILL.md: new drafting step 3 (r18 check before any `work add`, stops naming the scenarios); step 5 after `work add` (r17: append `## Retires` with quoted exact titles + feature file, none if no match); "Commit them, alone" says `work add` already commits and the pathspec commit covers the Retires sections, only if there is a change.

## Runs

No scenarios: delivery is a guarantees capability (0065), no red/green run exists. Suite at start: 686 passed, 0 failed at 221be9b (brief's record). No tests touched; none run.

## Size check

`tools size --limit 300` printed nothing.

## Tests changed under an allowance

none

## Open questions

- Source for "added or reworded" scenarios: I used scenarios tagged with `@r<n>` of the proposals' adds/changes; the plan left it open.
- Deprecated scenario matching two work-items: listed under both (follows from the wording, unchosen beyond that).
- `@deprecated` scenario with no `@r<n>`: not listed anywhere.
- Re-run on existing work-items: only work-items drafted in this run get Retires.

The plan contained no code.

Commit: db77ded. Files changed: skills/delivering-an-initiative/SKILL.md.
