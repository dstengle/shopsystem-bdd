# shopsystem-bdd
Claude Code plugin for the shopsystem harness: a behaviour-driven workflow
that replaces test-driven development with a single spec of capability
files, Gherkin feature files paired with them as the contract, thin vertical
slicing, and one human gate on the spec's Behaviour lines.

Skills: `integrating-a-proposal`, `formulating-features`,
`slicing-into-increments`, `bdd-red-green`, `migrating-to-capabilities`.
Agents: `capability-writer`, `feature-formulator`, `bdd-implementer`,
`bdd-task-reviewer`, `bdd-branch-reviewer`, `architecture-reviewer`.
Format: `docs/capability-format.md`.
Design: `docs/superpowers/specs/2026-09-22-bdd-workflow-design.md`, and
`docs/superpowers/specs/2026-09-29-capability-spec-design.md` for 0.8.0.
Test logs: `docs/superpowers/testing/`.

## Requires

The [superpowers](https://github.com/obra/superpowers) plugin, 6.4.0 or
later, declared as the dependency `superpowers@claude-plugins-official` in
`.claude-plugin/plugin.json` (the marketplace suffix is required: a bare name
is resolved against this plugin's own marketplace and reported missing, and
the object form of a dependency rejects a suffixed name, so it is a string). Claude Code
refuses to load this plugin when superpowers is not installed (a
`dependency-unsatisfied` load error). As of Claude Code on 2026-09-22 version
constraints on dependencies are not enforced, so the minimum version here is
documentation. The skills assume the rest of
the superpowers pipeline around them:

- `superpowers:brainstorming` produces an approved note, a proposal that
  `integrating-a-proposal` merges into `spec/`; `formulating-features` reads
  `spec/`, never the note.
- `slicing-into-increments` invokes `superpowers:writing-plans` to turn
  slices into tasks.
- `superpowers:executing-plans` or `superpowers:subagent-driven-development`
  runs those tasks, with `bdd-red-green` firing where they would otherwise
  fire `superpowers:test-driven-development`. formulating-features, slicing and bdd-red-green state that
  they supersede test-driven-development when both apply.

## Models

The `feature-formulator` agent pins `model: opus`, so formulation runs on
Opus whatever the session runs on; verified by the subagent turns in a
Sonnet session. A skill's own turns run on the session's model: a `model:`
field in SKILL.md did not change a session's model when the skill was
invoked by the model rather than by a slash command, so the skills carry
none. Launch a headless formulation, slicing, or planning session with
`--model opus` and an execution session with `--model sonnet`;
subagent-driven-development puts implementers on Sonnet and reviewers on
Opus by its own rules, and `bdd-red-green` pins nothing.

## Install

```
claude plugin marketplace add dstengle/shopsystem-bdd
claude plugin install shopsystem-bdd@shopsystem-bdd
```

While developing, `claude --plugin-dir <path to this checkout>` loads the
working copy instead.

## Sized to the change (0.9.0)

0.9.0 makes the workflow's cost follow the size and risk of a change. Measured on shopsystem-kb, about half of a batch's agent time went to running the full pipeline around one-line changes, re-reviewing small tasks, and a two-minute suite run many times a slice.

- **A small-change path.** At most two Behaviour lines in existing capabilities, no contract change, nothing unknown: the controller writes the lines and their scenarios itself, from the spec alone. The gate on the lines stays. Anything larger takes the full path (`integrating-a-proposal`, `formulating-features`).
- **Review by risk.** Each planned task carries `Review:` and `Model:` lines. Concurrency, the published contract, data integrity and moving stored data get a per-task review on Opus; everything else, refactors and small slices included, is reviewed once at the batch's end and implemented on Sonnet (`slicing-into-increments`).
- **Findings triaged.** Correctness and data loss are fixed now; hardening goes to the plan's backlog with its reproduction, and is cut only when the person asks or it bites; polish is fixed when cheap (`slicing-into-increments`, both reviewers).
- **A line every call must keep is one scenario per reason,** with one representative call; a table-driven test checks every call goes through the boundary (`formulating-features`).
- **The architecture review folds into the branch review,** which now checks shape against `CLAUDE.md` and coupling every batch. `architecture-reviewer` runs only on request.
- **A short living plan.** A batch's green slices and log move to `docs/superpowers/plans/archive/` when its branch review is done.
- **A fast suite.** `bdd-red-green` runs the slice's marker during red-green and the whole suite once per slice, and asks for a parallel suite (`pytest-xdist`) that drives commands in-process.

## One spec per context; the gate is on Behaviour lines

From 0.8.0 a bounded context has one spec: `spec/index.md`, the decision ledger `spec/decisions.md`, and `spec/capabilities/<name>.md`, each capability formulated as `features/<name>.feature`. The format is `docs/capability-format.md`.

- A brainstorming note is a proposal. `integrating-a-proposal` has the `capability-writer` agent (read-only, blind to the code) merge it into `spec/`, and stops at the one human gate: the added, changed and removed Behaviour lines and the questions the note left open. It never starts a second spec.
- `formulating-features` writes one scenario per approved line and needs no second approval. A line with two readings gets no scenario; its question goes to the person and the answer back through integration. This replaces 0.6.0's settled/deciding sort.
- Slicing cuts stack slices from the bounds in `spec/index.md`; its `QUESTION FOR THE SPEC:` lines end in a capability line or a ledger entry.
- `migrating-to-capabilities` moves a repository with notes and approved features onto `spec/`: capabilities grouped by behaviour, not by the old files; scenarios moved verbatim; test bindings follow the step definitions, which are never edited; the suite, the passing tests and every slice-tag count equal before and after. On a copy of shopsystem-kb: 171 scenarios from 16 features into 20 capabilities, 265 passed before and after, all 89 slice-tag counts equal.

A consuming repository's `CLAUDE.md` can say: "Brainstorming reads `spec/` first. Its note proposes changes to `spec/`, which integrating-a-proposal merges; it never starts a second spec."

## Plans carry no code; approval is for decisions

From 0.6.0 the planner plans and the implementer implements. `slicing-into-increments` hands writing-plans a constraint: no code blocks, file contents or diffs in the plan; each task says which scenarios go green, why they are red today, where the change lands by the project's `CLAUDE.md`, what the spec left open and how it was decided, which steps and fixtures to reuse, and the verification commands with counts taken from the tags. Nothing is built in a scratch copy first and no plan is replayed. Under `bdd-red-green` the implementer writes the code after the red run; a task that carries code is not pasted.

When execution runs under `superpowers:subagent-driven-development`, say so in the prompt: implementers work from intent under `bdd-red-green` and hand back on its stop conditions; task reviewers run the suite and every check themselves, and "cannot verify" fails the review rather than passing it; main is pushed when the batch is green and reviewed.

0.6.0's settled/deciding sort of scenarios is replaced in 0.8.0 by the gate on Behaviour lines (above). The principle stands: the person approves decisions, not transcription.

## Agents: rules held by tools, not by asking

From 0.7.0 the plugin gives each role in the workflow an agent whose tools are exactly the role's. A controller running `superpowers:subagent-driven-development` dispatches these types instead of `general-purpose`.

| agent | tools | model | for |
|---|---|---|---|
| `shopsystem-bdd:capability-writer` | Read, Glob, Grep | opus | integrating a note into `spec/`, and a repository's first `spec/`, blind to the code |
| `shopsystem-bdd:feature-formulator` | Read, Glob, Grep | opus | writing feature files from the spec, blind to the code |
| `shopsystem-bdd:bdd-implementer` | Read, Edit, Write, Glob, Grep, Bash, Skill | sonnet | one task of a no-code plan, `bdd-red-green` preloaded |
| `shopsystem-bdd:bdd-task-reviewer` | Read, Glob, Grep, Bash | opus | a task's review, and the scoped re-review of a fix round |
| `shopsystem-bdd:bdd-branch-reviewer` | Read, Glob, Grep, Bash | opus | the whole-branch review at the end of a batch, shape and coupling included |
| `shopsystem-bdd:architecture-reviewer` | Read, Glob, Grep, Bash, Write | opus | an architecture review when the person asks for one (the branch review checks shape and coupling every batch from 0.9.0) |

What the tools make structural:
- **No agent can start another.** None has the Agent tool, so an implementer cannot spawn helpers or its own reviewer, and a reviewer cannot ask for a second opinion.
- **The reviewers cannot edit the code they judge.** They have no Edit tool. The architecture reviewer's one Write is for its report file.
- **The implementer always has `bdd-red-green` in its context.** It is loaded through the `skills` field.

What stays a request:
- **Bash is still available.** Reviewers need it to run the suite, so "no commit, no push, no tag" is still asked, not enforced.
- **Command restrictions don't carry over from a plugin.** A plugin agent's `hooks` and `permissionMode` are ignored, and a tool entry with a specifier such as `Bash(git push *)` removes Bash altogether.
- **The fuller guarantee needs repository settings.** It is `permissions.deny` in the repository's `.claude/settings.json`, which binds the controller too, so the controller's own push must then run where those rules do not apply.

`model` is a default: a dispatch that names a model overrides it, as the controller does for the final review on the most capable model.

