---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools
title: Migration tools
narrator: a person or session migrating a repository to the final layout or upgrading it between plugin releases
group: service
language: codified-2
rests_on: [design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout, design-decision/references-are-ids, design-decision/capability-ids-are-context-scoped, design-decision/plugin-takes-the-dependencies-it-needs, design-decision/upgrades-between-plugin-releases, design-decision/work-items-named-by-ids, design-decision/answers-not-rulings, design-decision/the-ledger-is-tracked]
retired: [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17, g18, g19, g20, g21, g24, g25, g29, g30, g40, g41, g45, g46, g57, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r29, r30, r40, r41, r45, r46, r57, g42, r42, g48, r48, g49, r49, g62, r62, g63, r63, g64, r64, g44, r44, g60, r60, g52, r52, g53, r53, g54, r54, g55, r55, g56, r56, g61, r61, g66, r66, g67, r67, g68, r68, g65, r65, g77, r77, g78, r78, g79, r79, g27, r27, g28, r28, g58, r58, g31, r31, g32, r32, g33, r33, g34, r34, g35, r35, g36, r36, g37, r37, g38, r38, g39, r39, g59, r59, g43, r43, g69, r69, g70, r70, g47, r47, g50, r50, g51, r51, g71, r71, g72, r72, g73, r73, g74, r74, g75, r75, g76, r76, g80, r80, g81, r81, g82, r82, g83, r83, g84, r84]
unbuilt: []
---

# Migration tools

## Purpose
`scripts/migrate` makes the mechanical changes that take a repository from the old system to the final layout
(design-decision/final-layout) in one `migrate run`, and the upgrades that take a repository on the final layout from
one plugin release to the next (design-decision/upgrades-between-plugin-releases). It is the only code in the plugin
that knows the old layout, and it decides nothing that needs judgment. The plugin's hooks run it to tell a session
what it needs to know at its start and before it is compacted.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

## Implementation, may change
- r17's `by`: the entry's source, then `; supersedes <id> <qualifier>`.
- Python 3 with the standard library; it relocates with `git mv`; `migrate run` does not commit, `migrate upgrade`
  does. Every change is computed first, then written. A relocation onto a file that exists is a change it cannot make.
- The destinations under `.shop/records/` (archive, measurements, decision-arguments) and the record ids are
  design-decision/final-layout's; a decision file is `spec/decisions/<nnnn>-<name>.md` with an id, summary, date
  and status, and `spec/decisions/index.md` as `model decisions` writes it.
- `.shop/plugin-version` is one line holding the version. The plugin's SessionStart hook runs `migrate status` to
  learn what it tells the session.

- The relocations, each with `git mv`: `decisions/` to `spec/decisions/`, `work/` to `.shop/work/`, each
  `records/<x>` to `.shop/records/<x>`, `docs/superpowers/plans/` to `.shop/records/archive/plans/`,
  `docs/superpowers/specs/` to `.shop/records/archive/design-notes/`, `docs/superpowers/requests/` to
  `.shop/records/archive/requests/` and `adrs/` to `.shop/records/decision-arguments/`. A relocated record with no
  `about` gets `about: bounded-context/<path>`.
- A ledger entry `## decision/<nnnn>-<slug>` becomes `spec/decisions/<nnnn>-<slug>.md`: its summary is the entry's
  first paragraph, its Decision the entry's whole text, its status `superseded` when another entry supersedes it and
  `accepted` otherwise, and its `date`, `by`, `supersedes` and `revisit_when` the entry's. An entry with no number is
  numbered in ledger order from one above the ledger's highest. The ledger is removed once it holds nothing but its
  entries and a title. `migrate run` adds every file it wrote or relocated to git and writes `spec/decisions/index.md`.
- Ids are `<kind>/<path>/<name>`, the name being the file's stem without a decision file's number: `capability`,
  `design-decision`, `initiative-archive` for a relocated plan or request, `decision-argument` for a relocated
  design note or ADR, and `measurement` for a relocated test log (`*-test-log.md`). Behaviour lines with no id are
  numbered in Behaviour order from one above the highest id the capability has used or retired.
- What `migrate run` relocates or renames is rewritten wherever a repository-relative path, a relative Markdown link
  or a frontmatter id names it, in every tracked text file.
- The 0.24.0 step "work-items named by ids" numbers work-items from 1 by their initiative's number and then their file
  name, renames each file to `w<n>.md` and `runs/<name>/` to `runs/w<n>/`, writes the id
  `work-item/<context path>/w<n>`, keeps or writes the heading, and rewrites the old name in `log.jsonl` and in every
  `blocked_by`, `depends_on` and `for`; free text in records is left as it is. The 0.25.0 step renames
  `awaiting-ruling` to `awaiting-answer` and `## Rulings` to `## Answers`.
- The 0.30.0 step "codified requirements" (`migrate_upgrade_codified.py`): when `spec/restated.json` is missing, it
  writes it from the live `[r<n>]` lines of each capability without `language: codified-1`, keyed `<cap>#r<n>` with the
  line's text (a table row's lead sentence and cells) and line number. Each such capability's Behaviour becomes one
  `### [g<n>]` group for each old line with `Restates: r<n>@0.29.` and the old text as an HTML comment, no requirement
  bullets and no marker; its `retired:` becomes `[]` and it gains `## Dropped`. A codified capability is left as it
  is. Every scenario tagged `@deprecated` in `features/` is deleted (a docstring's lines are text). Every
  `<cap>#r<n>` (bare, or `capability/[<context path>/]<cap>`) of a tracked file under `.shop/work/` becomes
  `<cap>#r<n>@0.29`, a range id by id: in every file when the step writes `spec/restated.json`, else in the lines a
  file had at the commit that added `spec/restated.json`. It prints, and the commit message lists, what is left for
  a session to write: each scaffolded capability, and the glossary of an index without `language: codified-1`.
- The 0.31.0 step "the workflow simplified" (`migrate_upgrade_simplified.py`): when `.shop/work/` exists, it writes
  `.shop/work/FROZEN.md`, which says that the queue of plugin 0.30 is frozen and where items, batches and live requests
  are. Each request of `.shop/work/requests/` that is not closed (`open`, `awaiting-asker`, `awaiting-upstream`,
  `accepted`) and whose asker is neither `internal` nor this context is moved to `.shop/requests/` with `git mv`, its
  name and id unchanged; a destination that exists is a change it cannot make. When `spec/decisions/` exists, it
  rewrites `spec/decisions/index.md` as `model decisions` writes it. Nothing is deleted, and nothing else under
  `.shop/work/` changes. It prints, and the commit message lists, each initiative neither `done` nor `abandoned`, each
  capability- or glossary-proposal never applied, each internal request not closed, and each request moved. In the
  same upgrade as the 0.30.0 step, the 0.30.0 step's "left for a session to write" of a proposal under `.shop/work/` is
  dropped: the queue is frozen, and the 0.31.0 step's note names the proposal.
- `migrate upgrade` refuses, before it plans any step, when git has no author or committer identity
  (`git var GIT_AUTHOR_IDENT`, `GIT_COMMITTER_IDENT`), naming `git config user.name` and `user.email`.
- `migrate status` and `migrate upgrade` refuse a `.shop/plugin-version` that holds no version, naming an empty file
  as empty and otherwise what it holds; the SessionStart hook tells the session the same.

## Not yet
- `migrate plan` (a living plan to work-items and observations), `--dry-run`, and product-level repositories (see
  skeleton-notes.md).
- Upgrade steps for releases before 0.24.0, a repository before it being taken as 0.23.1 and earlier upgrades having
  been by hand — trigger: a repository on a release before 0.23.1 needs an upgrade.

## Dropped
- r3@0.29: the `@holding` tag is the old system's, and `migrate run` deprecated a held scenario through `features deprecate`, which is removed: the generator owns the feature files (the GF conversion's design §15), and the 0.30.0 upgrade deletes deprecated scenarios
- r32@0.29: retired with migration-tools#r22 in 0.31.0 (the-old-workflow-retired).
- r33@0.29: retired with migration-tools#r23 in 0.31.0 (the-old-workflow-retired).
- r34@0.29: retired with migration-tools#r23 in 0.31.0 (the-old-workflow-retired).
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g27 | upgrades#g1 |
| r27 | upgrades#r1 |
| g28 | upgrades#g2 |
| r28 | upgrades#r2 |
| g58 | upgrades#g3 |
| r58 | upgrades#r3 |
| g31 | upgrades#g4 |
| r31 | upgrades#r4 |
| g32 | upgrades#g5 |
| r32 | upgrades#r5 |
| g33 | upgrades#g6 |
| r33 | upgrades#r6 |
| g34 | upgrades#g7 |
| r34 | upgrades#r7 |
| g35 | upgrades#g8 |
| r35 | upgrades#r8 |
| g36 | upgrades#g9 |
| r36 | upgrades#r9 |
| g37 | upgrades#g10 |
| r37 | upgrades#r10 |
| g38 | upgrades#g11 |
| r38 | upgrades#r11 |
| g39 | upgrades#g12 |
| r39 | upgrades#r12 |
| g59 | upgrades#g13 |
| r59 | upgrades#r13 |
| g43 | upgrades#g14 |
| r43 | upgrades#r14 |
| g69 | upgrades#g15 |
| r69 | upgrades#r15 |
| g70 | upgrades#g16 |
| r70 | upgrades#r16 |
| g47 | upgrades#g17 |
| r47 | upgrades#r17 |
| g50 | upgrades#g18 |
| r50 | upgrades#r18 |
| g51 | upgrades#g19 |
| r51 | upgrades#r19 |
| g71 | upgrades#g20 |
| r71 | upgrades#r20 |
| g72 | upgrades#g21 |
| r72 | upgrades#r21 |
| g73 | upgrades#g22 |
| r73 | upgrades#r22 |
| g74 | upgrades#g23 |
| r74 | upgrades#r23 |
| g75 | upgrades#g24 |
| r75 | upgrades#r24 |
| g76 | upgrades#g25 |
| r76 | upgrades#r25 |
| g80 | upgrades#g26 |
| r80 | upgrades#r26 |
| g81 | upgrades#g27 |
| r81 | upgrades#r27 |
| g82 | upgrades#g28 |
| r82 | upgrades#r28 |
| g83 | upgrades#g29 |
| r83 | upgrades#r29 |
| g84 | upgrades#g30 |
| r84 | upgrades#r30 |
