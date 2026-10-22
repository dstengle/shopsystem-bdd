# shopsystem-bdd
Claude Code plugin for the shopsystem harness: a behaviour-driven workflow with one spec of capability files per
bounded context, Gherkin feature files paired with them as the contract, one human gate on the spec's Behaviour
lines, and delivery by work-items that a script, `work run`, pulls through research, plan, implementation and review.

Skills: `integrating-a-proposal`, `formulating-features`, `delivering-an-initiative`, `bdd-red-green`,
`checking-spec-consistency`, `migrating-to-capabilities`, `analyzing-a-batch`.
Agents: `capability-writer`, `feature-formulator`, `initiative-round`, `spec-checker`, `code-scout`, `bdd-planner`,
`bdd-implementer`, `bdd-task-reviewer`, `bdd-branch-reviewer`, `architecture-reviewer`, `trial-runner`.
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

The tests it runs load the plugin's own pytest plugin, `scripts/work_items.py` (`-p work_items`, the scripts
directory on `PYTHONPATH`): `--work-item <name>` for the work-item's scenarios, and `--whole-suite` for the suite
before a merge, where a failing scenario counts as expected while another work-item that is neither `green` nor
`withdrawn` accepts its requirement. Where pytest-xdist is installed, `-n auto` is added. A repository can name its
own commands in `.shop/delivery.toml` (`[tests]`, with `{work_item}` replaced by the name; its `suite` command needs
`--whole-suite` for expected red to work). `[allowed_tools]`, a list for a stage, replaces that stage's list
(`research`, `plan`, `implement`, `review`); a bare Write or Edit in it is still dropped. Git-ignore `.shop/scratch/`
and `.shop/worktrees/`.

Before you run it:

- The initiative branch needs a remote it can push to. `work run` checks the push before every worker starts and
  pushes after every commit it makes.
- Run `work run` with the same credentials as your `git push` (for example inside the credential wrapper you push
  with). Without them its push check fails and the work-item goes to `failed`.
- Commit `.shop/work/` first: `work run` refuses to start over uncommitted changes there.

A fault (a refused push, a git failure, a worker changing `.shop/work/`, a worker ending in an error or at its turn
limit, or with no readable result) moves the work-item to `failed` and the run exits with an error naming it. Fix the
cause, then `work retry <work-item>` brings it back to where its stage started. Workers write their result first, as
`PARTIAL`, and keep it current.

## Scripts

Python 3, in `scripts/`. `--help` is each one's contract; the plugin's own tests: `python3 -m pytest`.

- `scripts/model`: read a bounded context's spec, feature files, decisions, work and records as the facts of the
  design model's grammar (`facts`), check them with clingo (`check`), list the rules (`rules`), write the decisions
  index (`decisions`), and trace a requirement to why it exists (`why`).
- `scripts/features`: count, list, tag, move and verify-moved for feature files without the test runner;
  deprecate, retire and deprecated for scenarios kept while they still pass; bindings and rebind for the titles
  test modules bind.
- `scripts/work`: `add` drafts a work-item, `show` lists every work-item with its status (`--json`), `retry`
  returns a `failed` work-item, `withdraw` withdraws one, `run` delivers an initiative.
- `scripts/tools`: the project's analysis tools behind one interface: `probe`, `install`, `map`, `tests-of`,
  `untested`, `refs`, `check`, and `size`, the tracked Python files over a line limit.
- `scripts/migrate`: `migrate run --context <owner/product/context>` takes a repository from the old system to
  this layout in one run.
- `scripts/measure`: write an initiative's measurement from `work run`'s log, its sessions and git (`measure initiative`), print one as tables (`measure show`) and
  two side by side with their ratio (`measure compare`).

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
| `trial-runner` | Read, Glob, Grep, Bash, Write | sonnet | one trial of a plugin tool or `work run` on a target; writes only one measurement record |

Only `initiative-round` has the Agent tool. A plugin agent's `hooks` and `permissionMode` are ignored, so a role's
limits are its tools; under `work run` they are also its `--allowedTools`.

## 0.23.1: `--work-item` keeps tests that are not scenarios

- **`--work-item` keeps tests that are not scenarios** (supervision r55, r56): the option `work run` gives every
  worker's pytest now keeps a probe file or a script's test it collects, deselects only the scenarios the work-item
  does not accept, and refuses only a run that collected scenarios and none the work-item accepts. A researcher's
  probes run again, the cause of research stages ending at their turn limit since 0.22.0
  (`.shop/records/measurements/2026-10-22-research-at-the-limit.md`).
- **Still known**: work-item names repeat across initiatives, and `--work-item` takes the first initiative's
  work-item of a name; 0.24.0 gives work-items `w<n>` ids.

Upgrading a consuming repository from 0.23.0: a worker's `python3 -m pytest -q` under `--work-item` now also runs the
repository's tests that are not scenarios; nothing needs to change.

## 0.23.0: faults settled, query output as JSON, the session keeps the gate, measurement on v3

- **Faults settled** (the 0.22.0 review's deferred findings, decision 0057): a fault decides a work-item's status
  whatever its worker's outcome; a session that exits with an error or prints no JSON result is a fault;
  `work withdraw <work-item>`; `work retry` returns to the status `log.jsonl` gives before `failed`; the branch
  review's directory is kept under `.shop/work/<initiative>/runs/branch-review/<k>/`, committed, logged and pushed,
  and not run again while only its own commit is new; a run first pushes an initiative branch that is ahead of its
  remote; a run with a `failed` work-item exits with an error naming each fault. The glossary gains fault, remote and
  work-item branch.
- **Query commands answer in their output** (decision 0058, superseding 0055): `--json` prints a query's whole
  result as one JSON object for `features list`, `deprecated` and `bindings`, `model why` and `rules`, and
  `work show`; a query that finds nothing exits successfully (`features list`, `model why`). The `tools` query
  commands follow in a later release.
- **The session keeps the gate** (decision 0059): `initiative-round` gains a `gate` job and appends to the
  initiative's ledger; `delivering-an-initiative` sends fixes through `work run` and new scenario rows to the blind
  formulator; a new agent, `trial-runner`, runs one trial and writes a measurement record.
- **Measurement on v3** (decision 0060): `measure initiative <initiative>` measures an initiative's deliveries from
  `work run`'s log, the stages' sessions and git, with `--sessions` for the sessions around them; `measure show` and
  `measure compare` read the records. The old `measure batch` is removed; `analyzing-a-batch` follows.
- **Known**: a researcher under `work run` can end at its turn limit, because the `--work-item` option `work run`
  gives every worker's pytest refuses the researcher's probe files
  (`.shop/records/measurements/2026-10-22-research-at-the-limit.md`); work-item names repeat across initiatives.
  Both are next. Until then, deliver a work-item whose researcher fails by a direct `bdd-implementer`.

Upgrading a consuming repository from 0.22.0: scripts that read the exit of `features list` or `model why` on an
empty answer now see success (read the output, or use `--json`); records written by the old `measure batch` cannot be
read by `measure show` (measure an initiative instead); nothing else needs to change.

## 0.22.0: one requirement per scenario, faults, and the lessons of a blind formulation

- **One requirement per scenario** (decision 0054): a scenario names exactly one `@r<n>`; `model check` reports a
  scenario naming more (v_s2); `features tag` replaces the requirement tag. Steps are shared in code.
- **Exits in words** (decision 0055): a line and its scenario say a command exits successfully or with an error;
  exit codes live in a capability's Implementation section.
- **Faults** (decision 0056): `failed`, `work retry`, a push check before every worker and a push after every commit,
  worktrees removed on exit, a session ending in an error or at its turn limit is a fault, results start as
  `PARTIAL`, and expected red before a merge. `work add` and `work retry` commit what they change.
- **Small work-items**: `delivering-an-initiative` gives a work-item at most five requirements.
- **The spec's language**: a glossary in which each term has one meaning (run, delivery, stage directory, status,
  outcome, result, brief, input, template, transition, failed, ...), and five lessons in `docs/capability-format.md`
  that the spec-checker and the reviewers check (spec-consistency r22-r27, review r29-r30).
- **Records**: formulators' questions, reviews, run reports and gate verdicts kept under `.shop/records/`; bulky
  data (slim transcript exports) in a separate records repository, scanned by gitleaks before every push.

Upgrading a consuming repository from 0.21.0: give its initiative branches a pushable remote and run `work run` with
your push credentials; split any scenario that names two requirements (`model check` lists them under v_s2); reword
scenario steps that name exit codes as "exits successfully" or "exits with an error"; commit `.shop/work/` before each
`work run`.

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
