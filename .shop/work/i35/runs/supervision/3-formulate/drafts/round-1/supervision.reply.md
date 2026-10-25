## Coverage

| id | line | scenario |
|---|---|---|
| r73 | "When `work run` drafts a work-item, `work run` shall list under the work-item's `## Retires` each deprecated scenario whose `Deprecated for:` line names a scenario of a requirement the work-item accepts." | a work-item lists under its Retires each deprecated scenario whose Deprecated for line names a scenario of a requirement it accepts |
| r73 | (same line, range case) | a work-item that accepts a range lists under its Retires each deprecated scenario whose Deprecated for line names a scenario of a requirement in the range |
| r123 | "When every work-item of an initiative is `green` or `withdrawn` and a deprecated scenario's replacement's work-item, of any initiative, is `green`, `work run` shall draft one work-item, under the capability-proposal of the last-drafted work-item whose replacement it retires, that retires each deprecated scenario whose replacement's work-item is `green`." | when every work-item is green or withdrawn, one work-item is drafted retiring each deprecated scenario whose replacement's work-item is green |
| r124 | "When every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft the work-item r123 names before it starts a branch review or runs `measure initiative`." | the work-item retiring deprecated scenarios is drafted before the branch review starts and before measure initiative runs |

The two r73 scenarios replace the two existing @r73 scenarios (plain case and range). Each new one gives the deprecated scenario an `@r<n>` tag different from its replacement's, so it shows the work-item is found through the `Deprecated for:` line, not through the deprecated scenario's own tag.

## Questions

None.

## Cases no line mentions

- r123, "of any initiative": when the last-drafted work-item whose replacement is retired belongs to another initiative's capability-proposal, no line says whether the drafted work-item sits in that initiative or in the one being run. The r123 scenario keeps every green replacement in i1 and does not exercise this.
- r123: when several work-items accept the replacement's requirement, for example a line changed in two initiatives, no line says which of them is "the replacement's work-item".
- r123: no line says whether a deprecated scenario that a green work-item already lists under `## Retires` (r73) but that is still in its feature file is retired again by the r123 work-item.
- r123: the drafted work-item can retire deprecated scenarios of several capabilities while sitting under one capability-proposal, which is of one capability. No line says that is intended.
- r123: no line covers a deprecated scenario with `Deprecated for: removal`, a line with no replacement and so no replacement's work-item.
- r73: no line says whether a work-item drafted for a branch review's findings (r74), which accepts no requirement, lists anything under `## Retires`.
- r124: no line says what happens when the r123 work-item turns `green`, for example whether the branch review then starts at once.

## Drafts

- /tmp/work-run-i35-geaeg_4d/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/supervision.feature
- /tmp/work-run-i35-geaeg_4d/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/supervision.reply.md
