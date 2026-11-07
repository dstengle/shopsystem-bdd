---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools
title: Migration tools
narrator: a person or session migrating a repository to the final layout or upgrading it between plugin releases
group: service
language: codified-1
rests_on: [design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout, design-decision/references-are-ids, design-decision/capability-ids-are-context-scoped, design-decision/plugin-takes-the-dependencies-it-needs, design-decision/upgrades-between-plugin-releases, design-decision/work-items-named-by-ids, design-decision/answers-not-rulings, design-decision/the-ledger-is-tracked]
retired: [r22, r23]
unbuilt: [r25]
---

# Migration tools

## Purpose
`scripts/migrate` makes the mechanical changes that take a repository from the old system to the final layout
(design-decision/final-layout) in one `migrate run`, and the upgrades that take a repository on the final layout from
one plugin release to the next (design-decision/upgrades-between-plugin-releases). It is the only code in the plugin
that knows the old layout, and it decides nothing that needs judgment. The plugin's hooks run it to tell a session
what it needs to know at its start and before it is compacted.

## Terms
- **the SessionStart hook** (proper noun): the plugin's hook that runs `migrate status --hook` when a session starts, and
  gives the session what it prints.
- **the PreCompact hook** (proper noun): the plugin's hook that runs `migrate compacting` when a session is about to be
  compacted, and gives the session what it prints.
- **tracked file** (noun): a file committed in the repository `migrate` runs in.
- **untracked file** (noun): a file of the repository's working tree that git does not track, or a change not
  committed.
- **repository** (noun): the repository `migrate` runs in, with its working tree. Plural: repositories.
- **release** (attribute of repository): the plugin release `.shop/plugin-version` names, against the plugin's own: `0.23.1` before work-items were named by ids, `0.24.0` before `awaiting-answer` replaced `awaiting-ruling`, `0.29.0` before requirements were codified, `1.0.0` before the workflow was simplified, `own` the plugin's own release and `newer` a release newer than the plugin's. Values: `0.23.1`, `0.24.0`, `0.29.0`, `1.0.0`, `own`, `newer`.
- **codified** (adjective of capability): a capability whose file has `language: codified-1` in its frontmatter.
- **rewrite** (verb): `migrate` changes the text of a file in place. Forms: rewrites, rewritten. Frame: `migrate` rewrites file.
- **rename** (verb): `migrate` gives a file another name with git. Forms: renames, renamed. Frame: `migrate` renames file.
- **append** (verb): Forms: appends, appended. Frame: `migrate` appends file.
- **uncommitted** (adjective of untracked file): an untracked file whose text no commit holds.
- **unmigrated** (adjective of repository): a repository with a directory of the old layout at its root.
- **ledgered** (adjective of repository): a repository with the old system's ledger of decisions, `spec/decisions.md`.
- **superseding** (adjective of repository): a repository whose `spec/decisions.md` has an entry that supersedes another.
- **qualified** (adjective of repository): a repository whose `spec/decisions.md` has an entry that supersedes another in part.
- **numberless** (adjective of repository): a repository whose `spec/decisions.md` has an entry with no number.
- **idless** (adjective of repository): a repository with a capability that has a Behaviour line with no id.
- **conflicting** (adjective of repository): a repository with a file where `migrate run` would relocate another.
- **unversioned** (adjective of repository): a repository with `.shop/` and no `.shop/plugin-version`.
- **misversioned** (adjective of repository): a repository whose `.shop/plugin-version` holds no version.
- **behind** (adjective of repository): A repository is behind when the repository is `0.23.1`.
- **outdated** (adjective of repository): A repository is outdated when the repository is `0.24.0`.
- **uncodified** (adjective of repository): A repository is uncodified when the repository is `0.29.0` and a capability is not codified.
- **queued** (adjective of repository): A repository is queued when the repository is `1.0.0`.
- **current** (adjective of repository): A repository is current when the repository is `own`.
- **ahead** (adjective of repository): A repository is ahead when the repository is `newer`.
- **idle** (adjective of repository): A repository is idle when the repository is `own` and no initiative is open.
- **busy** (adjective of repository): a repository in which an initiative is open.
- **shopless** (adjective of repository): a repository without `.shop/`.

- **unframed** (adjective of repository): a repository whose `.shop/plugin-version` names a release after 1.0.0 and before 3.0.0.

## Behaviour

### [g1] `migrate run` relocates the old layout with git, rewrites what names it and gives each file the id of its kind
Restates: r1@0.29, r4@0.29, r5@0.29, r8@0.29, r9@0.29, r12@0.29, r14@0.29.
- [r1] While a repository is unmigrated, when the person runs `migrate run --context example.org/acme/shop`,
  `migrate` shall relocate `decisions/`, relocate `work/`, relocate `records/`, relocate `docs/superpowers/plans/`,
  relocate `docs/superpowers/specs/`, relocate `docs/superpowers/requests/`, relocate `adrs/`, rewrite
  `spec/index.md`, rewrite `README.md`, rewrite `spec/capabilities/thing.md` and rewrite `spec/decisions/0001-a.md`.

```given
the tracked file `decisions/0001-a.md` holds:
  ---
  id: decision/0001-a
  status: accepted
  ---
  # a
the tracked file `work/i1-cart/initiative.md` holds:
  ---
  id: initiative/i1-cart
  status: done
  ---
the tracked file `records/notes/one.md` holds:
  # one
  A note of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
  And a third line.
the tracked file `docs/superpowers/plans/2025-01-01-cart.md` holds:
  # The cart plan
  A plan of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
the tracked file `docs/superpowers/specs/2025-01-01-cart-design.md` holds:
  # The cart design
  A design note of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
the tracked file `docs/superpowers/requests/2025-01-02-pay.md` holds:
  # Pay
  A request of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
the tracked file `adrs/0001-use-git.md` holds:
  # Use git
  An ADR of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/shop
  title: shop
  ---
  # shop
the tracked file `README.md` holds:
  See [the note](records/notes/one.md) and work/i1-cart/initiative.md.
the tracked file `spec/capabilities/thing.md` holds:
  ---
  title: thing
  narrator: a client
  group: service
  rests_on: []
  retired: []
  ---
  # thing
  ## Purpose
  Something.
  ## Behaviour
  - [r1] **When** a, `thing` shall a.
```

### [g2] `migrate run` replaces a ledger with one decision file for each entry, removes it, and leaves no unresolved reference
Restates: r2@0.29, r6@0.29, r11@0.29, r16@0.29.
- [r2] While a repository is ledgered, when the person runs `migrate run --context example.org/acme/shop`, `migrate`
  shall relocate `spec/decisions.md`, rewrite `spec/decisions/index.md` and exit successfully.

```given
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/shop
  title: shop
  ---
  # shop
the tracked file `spec/decisions.md` holds:
  # Decisions
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
the tracked file `records/notes/one.md` holds:
  # one
  A note of the old system, long enough that git sees the rename after migrate adds an id.
  It has a second line.
```

### [g3] `migrate run` gives a decision file its entry's supersedes, and the entry it supersedes the status `superseded`
Restates: r2@0.29.
- [r3] While a repository is superseding, when the person runs `migrate run --context example.org/acme/shop`,
  `migrate` shall rewrite `spec/decisions/0007-a.md` and rewrite `spec/decisions/0008-b.md`.

```given
the tracked file `spec/decisions.md` holds:
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
  ## decision/0008-b
  We do b instead.
  date: 2025-03-02
  source: bob
  supersedes: decision/0007-a
  revisit_when: the cart grows
```

### [g4] `migrate run` writes a qualified supersedes as the decision's id alone, the qualifier going to `by`
Restates: r17@0.29.
- [r4] While a repository is qualified, when the person runs `migrate run --context example.org/acme/shop`,
  `migrate` shall rewrite `spec/decisions/0008-b.md`.

```given
the tracked file `spec/decisions.md` holds:
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
  ## decision/0008-b
  We do b.
  date: 2025-03-02
  source: bob
  supersedes: decision/0007-a (in part)
```

### [g5] `migrate run` numbers each ledger entry with no number from one above the ledger's highest
Restates: r13@0.29.
- [r5] While a repository is numberless, when the person runs `migrate run --context example.org/acme/shop`,
  `migrate` shall rewrite `spec/decisions/0008-b.md`.

```given
the tracked file `spec/decisions.md` holds:
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
  ## decision/b
  We do b.
  date: 2025-03-02
  source: bob
```

### [g6] `migrate run` numbers each Behaviour line with no id from one above the highest its capability has used
Restates: r10@0.29.
- [r6] While a repository is idless, when the person runs `migrate run --context example.org/acme/shop`, `migrate`
  shall rewrite `spec/capabilities/thing.md`.

```given
the tracked file `spec/capabilities/thing.md` holds:
  ---
  title: thing
  narrator: a client
  group: service
  rests_on: []
  retired: [r4]
  ---
  # thing
  ## Purpose
  Something.
  ## Behaviour
  - [r2] **When** a, `thing` shall a.
  - **When** b, `thing` shall b.
```

### [g7] `migrate run` that cannot make every change names it and changes no file
Restates: r7@0.29.
- [r7] While a repository is conflicting, if the person runs `migrate run --context example.org/acme/shop`, then
  `migrate` shall exit with an error naming `spec/decisions/0007-a.md` and change nothing.

```given
the tracked file `spec/decisions.md` holds:
  ## decision/0007-a
  We do a.
  date: 2025-03-01
  source: alice
the tracked file `decisions/0007-a.md` holds:
  ---
  id: decision/0007-a
  status: accepted
  ---
  # a, already there
```

### [g8] `migrate run` refuses a repository with uncommitted changes, naming them
Restates: r15@0.29.
- [r8] While an untracked file is uncommitted, if the person runs `migrate run --context example.org/acme/shop`,
  then `migrate` shall exit with an error naming the untracked file and change nothing.

```given
the tracked file `decisions/0001-a.md` holds "# a"
```

### [g9] `migrate upgrade` refuses a repository with uncommitted changes, naming them
Restates: r15@0.29.
- [r9] While an untracked file is uncommitted, if the person runs `migrate upgrade`, then `migrate` shall exit with
  an error naming the untracked file and change nothing.

```given
the tracked file `.shop/plugin-version` holds "0.23.1"
```

### [g10] `migrate status` prints both versions and each pending upgrade step
Restates: r18@0.29.
- [r10] While a repository is behind, when the person runs `migrate status`, `migrate` shall print "0.23.1",
  "0.24.0" and "work-items named by ids" and exit successfully.

```given
the tracked file `.shop/plugin-version` holds "0.23.1"
```

### [g11] a repository with `.shop/` and no `.shop/plugin-version` is on 0.23.1
Restates: r19@0.29.
- [r11] While a repository is unversioned, when the person runs `migrate status`, `migrate` shall print "0.23.1".

```given
the tracked file `.shop/records/.keep` holds "kept"
```

### [g12] `migrate status` refuses a `.shop/plugin-version` that holds no version, naming what it holds
Restates: r30@0.29.
- [r12] While a repository is misversioned, if the person runs `migrate status`, then `migrate` shall exit with an
  error naming "banana" and change nothing.

```given
the tracked file `.shop/plugin-version` holds "banana"
```

### [g13] `migrate upgrade` applies each pending step in one commit: work-items are named `w<n>` with their files and stage directories
Restates: r20@0.29, r25@0.29, r26@0.29.
- [r13] While the repository is behind, when the person runs `migrate upgrade`, `migrate` shall rewrite
  `.shop/plugin-version`, print "work-items named by ids" and "answers, not rulings", rename
  `.shop/work/i1/size-check.md`, rename `.shop/work/i1/runs/size-check/` and rewrite `.shop/work/i1/log.jsonl`.

```given
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `.shop/plugin-version` holds "0.23.1"
the tracked file `.shop/work/i1/size-check.md` holds:
  ---
  id: work-item/example.org/acme/shop/size-check
  kind: work-item
  status: drafted
  ---
  # size-check
the tracked file `.shop/work/i1/runs/size-check/1-research/notes.md` holds "Notes."
the tracked file `.shop/work/i1/log.jsonl` holds:
  {"time": "t", "work-item": "size-check", "event": "start"}
```

### [g14] `migrate upgrade` with no pending step says so and changes nothing
Restates: r27@0.29.
- [r14] While the repository is current, when the person runs `migrate upgrade`, `migrate` shall print "no upgrade
  step is pending" and change nothing.

```given
the tracked file `.shop/plugin-version` holds "2.4.0"
```

### [g15] the upgrade step after 0.24.0 renames `awaiting-ruling` to `awaiting-answer` and `## Rulings` to `## Answers`
Restates: r29@0.29.
- [r15] While the repository is outdated, when the person runs `migrate upgrade`, `migrate` shall rewrite
  `.shop/work/i1/w1.md`.

```given
the tracked file `.shop/plugin-version` holds "0.24.0"
the tracked file `.shop/work/i1/w1.md` holds:
  ---
  id: work-item/example.org/acme/shop/w1
  kind: work-item
  status: awaiting-ruling
  ---
  # w1
  ## Rulings
  - yes
```

### [g16] the upgrade step "codified requirements" writes `spec/restated.json`, scaffolds each uncodified capability, deletes deprecated scenarios and writes old references with their release
- [r16] While the repository is uncodified, when the person runs `migrate upgrade`, `migrate` shall print
  "spec/restated.json" and "spec/capabilities/cart.md", rewrite `spec/capabilities/cart.md`, rewrite
  `features/cart.feature` and rewrite `.shop/work/i1/w2.md`.

```given
the tracked file `.shop/plugin-version` holds "0.29.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `spec/capabilities/cart.md` holds:
  ---
  id: capability/example.org/acme/shop/cart
  title: Cart
  retired: []
  ---
  # Cart
  ## Behaviour
  - [r1] **When** the shopper applies a code, `cart` shall take ten percent off.
the tracked file `features/cart.feature` holds:
  Feature: Cart
    @r1 @deprecated
    Scenario: a code takes ten percent off (deprecated)
      Given a cart
the tracked file `.shop/work/i1/w2.md` holds:
  ---
  id: work-item/example.org/acme/shop/w2
  kind: work-item
  accepts: [cart#r1]
  ---
  # w2
```

### [g17] the SessionStart hook tells a session to offer a pending upgrade, and to run it only on the person's yes
Restates: r22@0.29.
- [r17] While a repository is behind, when the SessionStart hook runs `migrate status --hook`, `migrate` shall print
  "0.23.1", "work-items named by ids" and "only on the person's yes".

```given
the tracked file `.shop/plugin-version` holds "0.23.1"
```

### [g18] the SessionStart hook tells a session to tell the person to update the plugin
Restates: r23@0.29.
- [r18] While a repository is ahead, when the SessionStart hook runs `migrate status --hook`, `migrate` shall print
  "update the plugin".

```given
the tracked file `.shop/plugin-version` holds "9.0.0"
```

### [g19] the SessionStart hook tells a session nothing when nothing is pending and no initiative is open
Restates: r24@0.29.
- [r19] While a repository is idle, when the SessionStart hook runs `migrate status --hook`, `migrate` shall exit
  successfully, and `migrate` shall not print "migrate upgrade" or print "i1".

```given
the tracked file `.shop/plugin-version` holds "2.4.0"
the tracked file `.shop/work/i1/initiative.md` holds:
  ---
  id: initiative/example.org/acme/shop/i1
  kind: initiative
  status: done
  ---
  # i1
```

### [g20] the SessionStart hook tells a session nothing in a repository without `.shop/`
Restates: r28@0.29.
- [r20] While a repository is shopless, when the SessionStart hook runs `migrate status --hook`, `migrate` shall exit
  successfully.

```given
the tracked file `README.md` holds "No shop here."
```

### [g21] the SessionStart hook tells a session that `.shop/plugin-version` holds no version
Restates: r31@0.29.
- [r21] While a repository is misversioned, when the SessionStart hook runs `migrate status --hook`, `migrate` shall
  print "holds no version" and "banana".

```given
the tracked file `.shop/plugin-version` holds "banana"
```

### [g24] the upgrade step "the workflow simplified" freezes `.shop/work/`, moves the live requests to `.shop/requests/` and writes the decisions index
- [r24] While the repository is queued, when the person runs `migrate upgrade`, `migrate` shall write
  `.shop/work/FROZEN.md`, rename `.shop/work/requests/q2.md`, rewrite `spec/decisions/index.md` and print "the
  workflow simplified", "i1" and "q1".

```given
the tracked file `.shop/plugin-version` holds "1.0.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  ---
  # shop
the tracked file `spec/decisions/0001-one.md` holds:
  ---
  id: design-decision/example.org/acme/shop/one
  summary: One decision.
  status: accepted
  tier: judgement
  ---
  # One
  ## Decision
  One.
the tracked file `spec/decisions/index.md` holds:
  # Decisions
  Written by hand, with no tier.
the tracked file `.shop/work/i1/initiative.md` holds:
  ---
  id: initiative/example.org/acme/shop/i1
  kind: initiative
  title: A cart
  status: started
  ---
  # i1
the tracked file `.shop/work/requests/q1.md` holds:
  ---
  id: request/example.org/acme/shop/q1
  kind: request
  asker: internal
  status: open
  turn: upstream
  ---
  # An intention
the tracked file `.shop/work/requests/q2.md` holds:
  ---
  id: request/example.org/acme/shop/q2
  kind: request
  asker: bounded-context/example.org/acme/web
  status: open
  turn: upstream
  ---
  # A peer's request
```

### [g25] the upgrade step "verb frames" relabels each term with its part of speech and names each verb with no frame
- [r25] While the repository is unframed, when the person runs `migrate upgrade`, `migrate` shall rewrite `spec/index.md` and print "verb frames" and "v_t11".

```given
the tracked file `.shop/plugin-version` holds "2.4.0"
the tracked file `spec/index.md` holds:
  ---
  id: bounded-context/example.org/acme/shop
  title: shop
  language: codified-1
  ---
  # shop
  ## Glossary
  - **cart** (kind): the goods a shopper picks.
  - **shopper** (kind): a person who buys.
  - **pick** (event): a shopper puts goods in a cart. Forms: picks, picked.
```

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
- The 1.0.0 step "codified requirements" (`migrate_upgrade_codified.py`): when `spec/restated.json` is missing, it
  writes it from the live `[r<n>]` lines of each capability without `language: codified-1`, keyed `<cap>#r<n>` with the
  line's text (a table row's lead sentence and cells) and line number. Each such capability's Behaviour becomes one
  `### [g<n>]` group for each old line with `Restates: r<n>@0.29.` and the old text as an HTML comment, no requirement
  bullets and no marker; its `retired:` becomes `[]` and it gains `## Dropped`. A codified capability is left as it
  is. Every scenario tagged `@deprecated` in `features/` is deleted (a docstring's lines are text). Every
  `<cap>#r<n>` (bare, or `capability/[<context path>/]<cap>`) of a tracked file under `.shop/work/` becomes
  `<cap>#r<n>@0.29`, a range id by id: in every file when the step writes `spec/restated.json`, else in the lines a
  file had at the commit that added `spec/restated.json`. It prints, and the commit message lists, what is left for
  a session to write: each scaffolded capability, and the glossary of an index without `language: codified-1`.
- The 2.0.0 step "the workflow simplified" (`migrate_upgrade_simplified.py`): when `.shop/work/` exists, it writes
  `.shop/work/FROZEN.md`, which says that the queue of plugin 1.x is frozen and where items, batches and live requests
  are. Each request of `.shop/work/requests/` that is not closed (`open`, `awaiting-asker`, `awaiting-upstream`,
  `accepted`) and whose asker is neither `internal` nor this context is moved to `.shop/requests/` with `git mv`, its
  name and id unchanged; a destination that exists is a change it cannot make. When `spec/decisions/` exists, it
  rewrites `spec/decisions/index.md` as `model decisions` writes it. Nothing is deleted, and nothing else under
  `.shop/work/` changes. It prints, and the commit message lists, each initiative neither `done` nor `abandoned`, each
  capability- or glossary-proposal never applied, each internal request not closed, and each request moved. In the
  same upgrade as the 1.0.0 step, the 1.0.0 step's "left for a session to write" of a proposal under `.shop/work/` is
  dropped: the queue is frozen, and the 2.0.0 step's note names the proposal.
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
- r3@0.29: the `@holding` tag is the old system's, and `migrate run` deprecated a held scenario through `features deprecate`, which is removed: the generator owns the feature files (the GF conversion's design §15), and the 1.0.0 upgrade deletes deprecated scenarios
- r32@0.29: retired with migration-tools#r22 in 2.0.0 (the-old-workflow-retired).
- r33@0.29: retired with migration-tools#r23 in 2.0.0 (the-old-workflow-retired).
- r34@0.29: retired with migration-tools#r23 in 2.0.0 (the-old-workflow-retired).
