# shopsystem-bdd
Claude Code plugin for the shopsystem harness: a behaviour-driven workflow with one spec of capability files per
bounded context, Gherkin feature files paired with them as the contract, one human gate on the spec's Behaviour
lines, and delivery by work-items that a script, `work run`, pulls through research, plan, implementation and review.

Skills: `integrating-a-proposal`, `formulating-features`, `delivering-an-initiative`, `bdd-red-green`,
`checking-spec-consistency`, `migrating-to-capabilities`, `analyzing-a-batch`.
Agents: `capability-writer`, `feature-formulator`, `initiative-round`, `spec-checker`, `code-scout`, `bdd-planner`,
`bdd-implementer`, `bdd-task-reviewer`, `bdd-branch-reviewer`, `architecture-reviewer`.
Format: `docs/capability-format.md`. The design model it keeps: `docs/design-model/` (version 3).
This repository's own spec: `spec/index.md`; check it with `python3 scripts/model check`.

## Requires

The plugin depends on no other plugin. It needs, in the consuming repository's Python:

- clingo, for `model check` (`python3 -m pip install clingo`);
- pytest and pytest-bdd, for the scenarios;
- pytest-xdist, optional, to run the tests in parallel (`pytest.ini`'s `addopts = -n auto`; `-n 0` runs them in one
  process). `work run` runs the tests with `-n auto` where it is installed.

`work run` also needs the `claude` CLI on the PATH (or `$SHOPSYSTEM_WORK_CLAUDE`).

## Install

```
claude plugin marketplace add dstengle/shopsystem-bdd
claude plugin install shopsystem-bdd@shopsystem-bdd
```

While developing, `claude --plugin-dir <path to this checkout>` loads the working copy instead.

## The layout

A consuming repository keeps (design-decision/final-layout):

- `spec/`: `index.md` (the bounded context: purpose, constraints, composition, glossary), `capabilities/<name>.md`,
  and `decisions/`, one file a decision with its index `decisions/index.md`, written by `model decisions`;
- `features/<name>.feature`, one a capability, the file of its own name;
- `.shop/work/<initiative>/`: the initiative, its proposals and its work-items, and `runs/`, what `work run`'s
  workers left;
- `.shop/records/`: observations, measurements, review findings, decision arguments and the archive;
- `.shop/delivery.toml`, `work run`'s settings, optional;
- `.shop/scratch/` and `.shop/worktrees/`, drafts, notes and the implementers' worktrees, both git-ignored.

## The workflow

- **A proposal becomes lines.** `integrating-a-proposal` has the `capability-writer` (blind to the code) merge an
  approved note into `spec/` and stops at the one gate: the added, changed and removed Behaviour lines with their
  ids, glossary entries and decisions. Nothing is written to `spec/` before the person's yes.
- **Lines are EARS.** Every Behaviour line is one EARS requirement with "shall", in one of its patterns (`When`,
  `While`, `If … then`, `Where`, or none), one response, one sentence, with a stable id `[r<n>]`
  (design-decision/behaviour-lines-are-ears). `model check` reports a line that is not (`v_e1`, `v_e2`).
- **Lines become scenarios.** `formulating-features` has the `feature-formulator` (blind to the code) write one
  scenario a line, tagged `@r<n>`, with no second approval. A scenario that passes today and whose line changes is
  kept, tagged `@deprecated`, until the work-item that turns its replacement green retires it.
- **Scenarios are delivered.** `delivering-an-initiative` drafts the initiative's work-items from the spec alone
  (`work add`), commits them and starts `work run <initiative>`. `work run` takes each work-item through its stages,
  one fresh `claude -p` worker a stage: `code-scout` researches, `bdd-planner` plans (intent, never code),
  `bdd-implementer` implements red-green under `bdd-red-green` in its own worktree, and `bdd-task-reviewer`
  reviews. It writes every status itself, merges a branch only when the work-item's scenarios and the whole suite
  pass on it, and ends printing each work-item's status and each question for the person. Exit 0: every work-item
  green; 3: a question awaits the person; 1: it stopped, saying why.
- **The spec checks itself.** `checking-spec-consistency` and the `spec-checker` judge lines against scenarios and
  against the glossary; `model check` checks the whole repository against the design model.

## `work run`

Each worker runs with `--permission-mode acceptEdits`, the plugin's directory as `--plugin-dir`, and
`--allowedTools` set for its stage: no bare Write or Edit (a worker's writes stay in the worktree it starts in), and
Bash only for `python3 -m pytest`, the plugin's scripts by path and the git commands the stage needs. Nothing runs
with permissions bypassed.

The tests it runs are `python3 -m pytest -q --work-item <name>` for the work-item and `python3 -m pytest -q` for the
suite. `--work-item` is a pytest option that selects the scenarios tagged with a requirement the work-item accepts;
a repository whose pytest has none names its own commands in `.shop/delivery.toml`:

```
[tests]
work_item = "python3 -m pytest -q"
suite = "python3 -m pytest -q"
```

`{work_item}` in `work_item` is replaced by the work-item's name. `[allowed_tools]`, a list for a stage, replaces
that stage's list (`research`, `plan`, `implement`, `review`); a bare Write or Edit in it is
still dropped. Git-ignore `.shop/scratch/` and `.shop/worktrees/`.

## Scripts

Python 3, in `scripts/`. `--help` is each one's contract; the plugin's own tests: `python3 -m pytest`.

- `scripts/model`: read a bounded context's spec, feature files, decisions, work and records as the facts of the
  design model's grammar (`facts`), check them with clingo (`check`), list the rules (`rules`), write the decisions
  index (`decisions`), and trace a requirement to why it exists (`why`).
- `scripts/features`: count, list, tag, move and verify-moved for feature files without the test runner;
  deprecate, retire and deprecated for scenarios kept while they still pass; bindings and rebind for the titles
  test modules bind.
- `scripts/work`: `add` drafts a work-item, `show` lists every work-item with its status, `run` delivers an
  initiative.
- `scripts/tools`: the project's analysis tools behind one interface: `probe`, `install`, `map`, `tests-of`,
  `untested`, `refs`, `check`, and `size`, the tracked Python files over a line limit.
- `scripts/migrate`: `migrate run --context <owner/product/context>` takes a repository from the old system to
  this layout in one run.
- `scripts/measure`: write, show and compare a batch's facts from the session transcripts and git.

## Agents: rules enforced by tools

| agent | tools | model | for |
|---|---|---|---|
| `capability-writer` | Read, Glob, Grep, Write | opus | integrating a note into `spec/`, and a repository's first `spec/`, blind to the code; writes only drafts |
| `feature-formulator` | Read, Glob, Grep, Write | opus | writing feature files from the spec, blind to the code; writes only drafts |
| `initiative-round` | Read, Glob, Grep, Bash, Write, Edit, Agent | sonnet | one round of spec work for the session that keeps the gate; dispatches only the two agents above |
| `spec-checker` | Read, Glob, Grep, Write | sonnet | judging a spec against itself, blind to the code; writes only its findings file |
| `code-scout` | Read, Glob, Grep, Bash, Write | haiku | a work-item's research for `work run`: why its scenarios are red, its file set, the tests it may break |
| `bdd-planner` | Read, Glob, Grep, Write | opus | a work-item's plan for `work run`, from the research notes, intent and never code |
| `bdd-implementer` | Read, Edit, Write, Glob, Grep, Bash, Skill | sonnet | a work-item, red-green under `bdd-red-green`, in its worktree and branch |
| `bdd-task-reviewer` | Read, Glob, Grep, Bash, Write | opus | a done work-item's review for `work run`; changes nothing |
| `bdd-branch-reviewer` | Read, Glob, Grep, Bash, Write | opus | an initiative's branch review, from its base, over every work-item; changes nothing |
| `architecture-reviewer` | Read, Glob, Grep, Bash, Write | opus | an architecture review when the person asks for one |

Only `initiative-round` has the Agent tool. A plugin agent's `hooks` and `permissionMode` are ignored, so a role's
limits are its tools; under `work run` they are also its `--allowedTools`.

## 0.21.0: the final layout and delivery by `work run`

What changes for a consuming repository:

- **The layout.** `spec/` (with `decisions/` one file a decision, where 0.20.0 had the ledger
  `spec/decisions.md`), `features/`, and `.shop/` for work, records, scratch and worktrees. `docs/superpowers/`
  and top-level `decisions/`, `work/` and `records/` are gone; `model` reads only the new layout.
- **Delivery is v3.** Slicing, slice plans, lanes and steps, `scripts/plan` and the `slicing-into-increments` skill
  are removed, and so is the dependency on superpowers (design-decision/superpowers-not-a-dependency).
  An initiative's work-items are drafted by `delivering-an-initiative` and delivered by `work run`.
- **EARS.** Behaviour lines are EARS requirements with "shall"; `model check` reports any that is not.
- **`migrate run`** makes every mechanical change of the move in one run, or none: moves, decision files from the
  ledger, ids, `@holding` scenarios to `@deprecated`, rewritten references.
- **pytest-bdd and xdist.** The plugin's scenarios run as pytest-bdd step definitions, every scenario bound
  exactly once (`features bindings --unbound`), in parallel under pytest-xdist.
- **`tools size`.** Tracked Python files stay at 300 lines or fewer; `tools size --limit 300` lists those over it,
  and the reviewers run it.

To upgrade: install 0.21.0, `python3 -m pip install clingo pytest pytest-bdd` (and pytest-xdist), and from a clean
checkout with nothing in progress ask Claude to migrate the repository: the `migrating-to-capabilities` skill runs
`migrate run`, re-pairs what needs judgment, and stops at its one gate. Then git-ignore `.shop/scratch/` and
`.shop/worktrees/`, and give pytest a `--work-item` option or set `[tests]` in `.shop/delivery.toml` before the first
`work run`. Earlier releases' notes are in git's history of this file.
