---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-design-model-check
kind: capability-proposal
part_of: initiative/i11
status: approved
date: 2026-10-19
argues: [design-model-check]
adds: [design-model-check#r61, design-model-check#r64-r66]
changes: [design-model-check#r2-r8, design-model-check#r10-r11, design-model-check#r14-r15, design-model-check#r19-r20, design-model-check#r23, design-model-check#r25-r26, design-model-check#r29, design-model-check#r33-r35, design-model-check#r37, design-model-check#r51-r54, design-model-check#r59]
removes: [design-model-check#r45]
---

# Design model check: the final layout, ids for references, labels for rules

`model` reads the final layout and nothing else (design-decision/final-layout), derives a capability's feature
file from its name, reads a decision's `source` as ids (design-decision/references-are-ids), reads
`@deprecated` in place of `@holding`, and prints every rule with a plain label. The proposed file is
`capabilities/design-model-check.md` beside this one.

What the gate sees, by id:

- The layout: r19 (what is read), r14, r15, r37 (`spec/decisions/index.md`), r20 and r26 (the feature file is
  `features/<name>.feature`), r45 removed (no ledger is read), r60 (`formulated_as` is a file problem), r61
  (an old layout's paths are file problems, naming `scripts/migrate`).
- References: r64 (a decision's `source` is ids, `by` is not read). r24 is unchanged: `source` was already in
  its list, and now covers a decision's too.
- Proposals' lists: r66 reads `term/<term>` in `adds`, `changes` and `removes`, as docs/capability-format.md
  and spec-integration#r17 already tell a writer to list a term (today `model check` reports every such entry
  as "not a requirement reference"); r23 lets a merged or formulated proposal's `removes` name the id it
  retired (today a proposal that removed a line is unresolved for ever once it merges, so this proposal's own
  removal of r45 would be).
- Decisions: r63 (a decision file needs `## Decision`, design-decision/light-decisions).
- Deprecated: r26, r44, r62 (`@holding` is a file problem, not read as `@deprecated`).
- Labels: r2, r11, r33 (printed with the code; mapped in `--json`), r65 (`model rules`), and each line that
  names a rule now names its label too: r3-r8, r10, r34, r35, r52-r54, r59.
- Mentions: r51 reads no mention inside a code span, a double-quoted string or an `@` tag, so a line or step
  that names a literal (the tag `@holding` in r62 and in migration-tools, `" (held)"`) is not a use of the
  word the glossary avoids. It also says contains for holds.
- Plain words: r4 (carry → have), r34 (hold → have); Purpose likewise.

r22 and r42 (`#behaviour/r<n>`) are left as they are: design-decision/one-requirement-form retires them in
initiative i10.

The labels, one per rule `model.lp` shows, written once there:

| code | label |
|---|---|
| v1 | needs on something that is not a part |
| v2 | a standing edge touches something that is not standing |
| v3 | a scenario is on a needs edge |
| v4 | a depends_on that no using gives |
| v5 | a using against the pin |
| v6 | a crossing names no seam |
| v6b | a job-thread is mapped with a crossing that names no seam |
| v7 | a cross-context-request names no capability it comes from |
| v7b | a cross-context-request is across the wrong seam |
| v7c | an upstream names a downstream client |
| v8 | a work-item names no capability |
| v9a | a part has no part_of |
| v9b | a part has two part_of |
| v9c | a part reaches no initiative |
| v9d | a priority on something that is not an initiative |
| v9e | a source on something that is not an initiative |
| v9f | an initiative is part of something |
| v9g | a part_of cycle |
| v10a | a source that is not an origin |
| v10b | a record is about nothing |
| v10c | a record is about something that is not standing |
| v11 | a capability without exactly one narrator |
| v12a | a decision has no summary |
| v12b | a supersedes cycle |
| v13 | a revisit signal no one reads |
| v15a | a requirement has no id |
| v15b | two requirements share an id |
| v15c | a retired id is used again |
| v15d | a requirement id outside its capability |
| v15e | a proposal changes a requirement no capability has |
| v15f | a formulated proposal leaves a requirement without a scenario |
| v_k1 | a job initiative's first part is not a job-proposal |
| v_k2 | a job-path initiative's first part is not a job-thread |
| v_k3 | a capability-change initiative's first part is not a capability-proposal |
| v_k4 | a defect initiative's first part is not a work-item |
| v_k5 | an initiative has more than one first part |
| v_k6 | a capability-proposal argues more than one capability |
| v_b1 | a work-item is part of something other than a capability-proposal |
| v_b2 | a cross-context-request has a part that is not a capability-proposal |
| v_b3 | a job-thread has a part of the wrong kind |
| v_s1 | a scenario names no requirement |
| v_s2 | a scenario names two requirements |
| v_s3 | a requirement has no scenario |
| v_w1 | a blocked_by cycle |
| v_w2 | a ready work-item is blocked by one not green |
| v_w3 | two claimed work-items claim one file |
| v_w4 | a work-item has no acceptance and no check |
| v_d1 | a done initiative has a part open |
| v_d2 | an abandoned initiative has a part open |
| v_t1 | a word the glossary avoids |
| v_t2 | a term has two entries |
| v_t3 | an avoided word is a term |
| w_unserved_cap | a capability serves no job |
| w_unserved_job | a job nothing serves |
| w_seam_unused | a seam nothing crosses |
| w_uncited_obs | an observation no initiative cites |
| w_many_requests | more than five open requests across one seam |
| w_stale_intake | an initiative proposed more than 90 days ago |

Formulation follows: the scenarios of the changed lines are reworded; steps that use "holding" or "holds"
("a directory holding", "one JSON object holding") are reworded with their lines, since the new glossary
entry avoids "holding".

Re-synced 2026-10-19 to the EARS lines (initiative/i13, approved by the person): design-model-check#r60 -> r25; design-model-check#r62 -> r26; design-model-check#r63 -> r29; design-model-check#r44 -> r20. The ids in the text above are the drafted ones.
