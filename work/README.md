# Work

The intake backlog and the work-breakdowns of this bounded context (design model v3, sections 3 and 8).
Each directory is one initiative: `initiative.md`, the root, with its priority and sources; every other
file is a part, with exactly one `part_of`. Only an initiative is ranked. Forms:
design-decision/work-file-forms. Check: `python3 scripts/model check`.

| id | kind | status | priority | summary |
|---|---|---|---|---|
| i1 | capability-change | started | — | The plugin's first spec |
| i2 | capability-change | started | — | Check a repository against the design model |
| i3 | capability-change | proposed | 1 | Requirement ids in the format the plugin teaches |
| i6 | capability-change | proposed | 2 | Retire the rules whose signals fired |
| i4 | capability-change | proposed | 3 | Work-items in place of slices, tasks, steps and lanes |
| i5 | capability-change | proposed | 4 | A pull loop in place of the LLM controller |
| i7 | capability-change | proposed | 5 | Superpowers no longer a dependency |
| i8 | capability-change | proposed | 6 | Initiatives and records in consuming repositories |

Before i6 or i5 starts: one kb batch run on 0.18.0 unchanged, with its facts committed, as the baseline
(observation/2026-10-15-unmeasured-releases). That run changes nothing here; it produces a measurement.
