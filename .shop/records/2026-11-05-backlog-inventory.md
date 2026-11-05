---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-05-backlog-inventory
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# What of the old system still needs to become backlog items

This is a read-only sweep made after the 2.0.0 upgrade on branch `workflow-simplification`. Its sources:
- the frozen `.shop/work/`;
- the spec's `## Not yet` sections;
- the open problems and rulings in `2026-11-04-workflow-simplification/`;
- `2026-11-03-gf-conversion/close-r3.md`.

Plan 9 Task 10 entered only b1-b4.

**State at the sweep:**
- `model check`: 0 violations, 16 warnings (all `w_uncited_obs`), 0 unresolved.
- `model logic`: 4 L5 (U4 twice, U7, U8), 0 L6.
- Lexicon: 114 of its 139 conditions are prose.
- Frozen queue:
  - 12 initiatives `started`: i39, i45, i47, i49, i52, i53, i55, i56, i58, i59, i60, i61;
  - about 30 proposals not applied;
  - 27 internal requests `accepted` and 2 `open` (q46, q47).

## Proposed backlog items

| # | Title | Sources | Why still live | Prov. | Value / urgency / size |
|---|---|---|---|---|---|
| b1 | *(exists)* Requests between repositories over GitHub issues | q14 lines 2-3, 13-22; i39 w212; q21 lines 2-9; i55 `requests-deda9fa6.md`; requests `## Not yet` (r50-r54) | Not built. **Gap:** q14 line 4 (an asker works from its own repository, with no checkout of the upstream's) is accepted, but b1's note leaves it out. | product | H / M / L |
| b2 | *(exists)* Request lines in the downstream's own terms | q17; i53 `spec-integration.md`; the 2.0 form of q14 line 23 | Wanted | own | – |
| b3 | *(exists)* JSON from every command, exit 0 except on a crash | q25; i59's 11 drafted proposals | The title leaves out q25's second half: every agent returns structured JSON (i59 `role-boundaries.md`). | own | – |
| b4 | *(exists)* Requirement quality | q26; i45's 4 proposals | – | own | – |
| 5 | A request withdrawn whole, and the asker's own withdrawals | q33 line 3 (i47); requests `## Not yet` | No line sets a request `withdrawn` when all its lines are | own | M / L / S |
| 6 | Resolve the delivered item's request at the merge | batches `## Not yet` | b1's merge is meant to resolve q14, but no command does it | own | M / M / S |
| 7 | Generator gaps in `spec_steps` | plan-1-rulings "Known gaps" S2; plan-1-impl #1, #4 (batches g7, backlog g4/g6/g15) | Lines were reworded around the gaps instead of the generator being fixed (plan-2 D13) | own | H / M / M |
| 8 | Strengthen the weak lines | plan-1-rulings M3: telemetry r4, conversation r2, readiness r4, batches r5, intake r5 | Each needs retire-and-replace | own | L / L / S |
| 9 | Reword the L5 lines | close-r3 #2; plan-9 Q1 | 4 L5 left; U7 waits for a line about a batch's task subagent | own | M / L / S |
| 10 | Define prose conditions in the controlled language, with glossary relations | close-r3 #1, #4; plan-1-impl #3 (`blocked`) | 114 of 139 conditions are prose; count the live ones first | own | M / L / L |
| 11 | Merge the repeated ubiquitous statements | close-r3 #4; verify-r2 point 2 | Not measured since the retirement | own | L / L / S |
| 12 | Remove the dead terms from the lexicon | plan-9 open row 26 | Needs an unused-term check first | own | L / L / M |
| 13 | An item proposes a new capability or glossary term | readiness `## Not yet`; q30 lines 1, 4, 6 | 2.0 can't add a capability or an index term through an item | own | M / M / M |
| 14 | Reword or remove an item's line by command | plan-3-impl open problems | `work line` only adds lines | own | M / M / S |
| 15 | Id collisions across branches | plan-2 D4; plan-3 D3; q46 line 3 | Check what `work batch start` already prevents first | own | M / L / S |
| 16 | Tie an intake item to its asker | intake `## Not yet`; plan-1 P8 | The grammar can't yet say who asked | own | M / L / M |
| 17 | The names table expands `q<n>` and `r<n>` | plan-9 open row 21; plan-8 open #2 | Needs a `conversation` line | own | L / L / S |
| 18 | Small CLI hygiene | plan-9 M1 (`work`'s commits with no git identity); observation `2026-10-16-release-0-19-0-defects`; `2026-10-24-i23-open-cases`; plan-6 (no `--json` on `model decisions --check`) | Small; check each first | own | L / L / S |
| 19 | Telemetry and PR review tuned on real batches | telemetry and pr-review `## Not yet`; plan-7 #2-#4; plan-5 duplicate comment | Waits for real batch figures | own | L / L / M |
| 20 | Log of temporary rules | observation `2026-10-30-log-of-temporary-rules`; board design | Named as its own item, never entered | own | ? / L / M |
| 21 | Browser board, or a TUI | board design non-goals | Named as its own item, never entered | own | L / L / L |
| 22 | Bugs' risk and likelihood | backlog `## Not yet`; plan-1 P4 | Decided, not built | own | L / L / S |
| 23 | Design model v6: items in place of initiatives | plan-9 open row 27 | `docs/design-model/` v5 still describes initiatives | own | M / L / L |
| 24 | The design model's ownership moves to shopsystem-knowledge | observation `2026-10-16-model-owned-by-knowledge`; i14; design-model-check `## Not yet` | A request to shopsystem-knowledge, not code here | peer (outgoing) | M / L / ? |
| 25 | Drop `_LineParser` once the floor is Python 3.12 | plan-9 open row 2; plan-4 D25 | Waits for that floor | own | L / L / S |

## Obsolete under 2.0 (no item)

- **Initiatives on `work run` and its gates:** i49, i52, i58, i60, i61, i47 lines 1-2, and the rest of i55. Branches `work/w174`, `work/w182` and `work/w243` are each 1 commit ahead and can go.
- **Internal requests on `work run`, rounds, proposals and delegations:** q18-q24, q34-q40, q42-q44, q47, and q46 lines 1, 2, 4.
- **Already settled:** q41, q45, q46.
- **Met by `work idea`:** q27 and i56.
- **q30, q36, q37:** their 1.x side is obsolete; what survives is row 13.
- **Uncited observations about the old machinery:** 10 of the 16 warnings. Citing or closing them clears the warnings.
- **`## Not yet` entries that already have a trigger:** analysis-tools, feature-file-tools, migration-tools, and the intake session.
- **close-r3 #3** (`model check`, now 0) and **r52 vs r5** (ruled by the "If" precedence).

## Needs the person, not an item

- **q14:**
  - run `work turn q14`;
  - offer the 2.0 form of lines 19 and 23-26;
  - resolve the rest after b1;
  - add line 4 to b1.
- **The rulings:** all nine `plan-N-rulings.md` (about 27 question rulings and about 100 finding fixes), marked "revisit". The ones with most reach: plan-1 P10, P4, P8, P5; plan-4 Q1; plan-5 Q3; plan-7 Q1; plan-8 Q3; plan-9 Q1, Q2.
- **Call 16:** `## Relations` rows that use a bare preposition (gate-r2-done.md).
- **Rating b1-b4:** value, urgency and size are empty; and whether i59's agent half goes into b3.
- **Cleanup:**
  - 44 leftover worktrees under `.claude/worktrees/`, one of them (`agent-a91965f110ce351d6`) locked;
  - about 100 local branches;
  - `gfr/fix-wip`, an unverified WIP commit.
