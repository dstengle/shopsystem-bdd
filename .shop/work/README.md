# Work

The intake backlog and the work-breakdowns of this bounded context (design model v3, sections 3 and 8).
Each directory under `.shop/work/` is one initiative: `initiative.md`, the root, with its priority and sources; every other
file is a part, with exactly one `part_of`. Only an initiative is ranked. Forms:
design-decision/work-file-forms. Check: `python3 scripts/model check`.

| id | kind | status | priority | summary |
|---|---|---|---|---|
| i10 | capability-change | proposed | 1 | Delivery on design model v3 |
| i11 | capability-change | proposed | 2 | This repository on the final layout and conventions |
| i8 | capability-change | proposed | 3 | Migrate a consuming repository to design model v3 |
| i12 | capability-change | proposed | 4 | Batch measurement on design model v3 |
| i15 | capability-change | proposed | 4 | Files within the size limit |
| i16 | capability-change | proposed | 1 | The session keeps the gate and nothing else (next release) |
| i1 | capability-change | started | — | The plugin's first spec |
| i3 | capability-change | started | 1 | Requirement ids in the format the plugin teaches |
| i9 | capability-change | started | 8 | A ubiquitous language for the bounded context |
| i2 | capability-change | done | — | Check a repository against the design model |
| i4 | capability-change | abandoned | 3 | Work-items in place of slices, tasks, steps and lanes (replaced by i10) |
| i5 | capability-change | abandoned | 4 | A pull loop in place of the LLM controller (replaced by i10) |
| i6 | capability-change | abandoned | 2 | Retire the rules whose signals fired (replaced by i10) |
| i7 | capability-change | abandoned | 5 | Superpowers no longer a dependency (replaced by i10) |

The baseline kb batch on 0.18.0 that i5 and i6 waited for (observation/2026-10-15-unmeasured-releases) is no
longer needed by them; whether i10 is measured against it is open.
