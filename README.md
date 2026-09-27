# shopsystem-bdd
Claude Code plugin for the shopsystem harness: a behaviour-driven workflow
that replaces test-driven development with Gherkin feature files as the
contract, thin vertical slicing, and one human gate at feature approval.

Skills: `formulating-features`, `slicing-into-increments`, `bdd-red-green`.
Agents: `feature-formulator`, `bdd-implementer`, `bdd-task-reviewer`,
`bdd-branch-reviewer`, `architecture-reviewer`.
Design: `docs/superpowers/specs/2026-09-22-bdd-workflow-design.md`.
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
documentation. The three skills assume the rest of
the superpowers pipeline around them:

- `superpowers:brainstorming` produces the approved spec that
  `formulating-features` reads.
- `slicing-into-increments` invokes `superpowers:writing-plans` to turn
  slices into tasks.
- `superpowers:executing-plans` or `superpowers:subagent-driven-development`
  runs those tasks, with `bdd-red-green` firing where they would otherwise
  fire `superpowers:test-driven-development`. All three skills state that
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

## Plans carry no code; approval is for decisions

From 0.6.0 the planner plans and the implementer implements. `slicing-into-increments` hands writing-plans a constraint: no code blocks, file contents or diffs in the plan; each task says which scenarios go green, why they are red today, where the change lands by the project's `CLAUDE.md`, what the spec left open and how it was decided, which steps and fixtures to reuse, and the verification commands with counts taken from the tags. Nothing is built in a scratch copy first and no plan is replayed. Under `bdd-red-green` the implementer writes the code after the red run; a task that carries code is not pasted.

When execution runs under `superpowers:subagent-driven-development`, say so in the prompt: implementers work from intent under `bdd-red-green` and hand back on its stop conditions; task reviewers run the suite and every check themselves, and "cannot verify" fails the review rather than passing it; main is pushed when the batch is green and reviewed.

`formulating-features` sorts each scenario as *settled*, when the spec sentence it cites admits one reading, or *deciding*, when it fixes something the spec leaves open or picks one of two readings. Only deciding scenarios wait for the person's approval; settled ones go straight to slicing. The person approves decisions, not transcription.

## Agents: rules held by tools, not by asking

From 0.7.0 the plugin gives each role in the workflow an agent whose tools are exactly the role's. A controller running `superpowers:subagent-driven-development` dispatches these types instead of `general-purpose`.

| agent | tools | model | for |
|---|---|---|---|
| `shopsystem-bdd:feature-formulator` | Read, Glob, Grep | opus | writing feature files from the spec, blind to the code |
| `shopsystem-bdd:bdd-implementer` | Read, Edit, Write, Glob, Grep, Bash, Skill | sonnet | one task of a no-code plan, `bdd-red-green` preloaded |
| `shopsystem-bdd:bdd-task-reviewer` | Read, Glob, Grep, Bash | opus | a task's review, and the scoped re-review of a fix round |
| `shopsystem-bdd:bdd-branch-reviewer` | Read, Glob, Grep, Bash | opus | the whole-branch review at the end of a batch |
| `shopsystem-bdd:architecture-reviewer` | Read, Glob, Grep, Bash, Write | opus | the review cut after every six slices, coupling included |

What the tools make structural:
- **No agent can start another.** None has the Agent tool, so an implementer cannot spawn helpers or its own reviewer, and a reviewer cannot ask for a second opinion.
- **The reviewers cannot edit the code they judge.** They have no Edit tool. The architecture reviewer's one Write is for its report file.
- **The implementer always has `bdd-red-green` in its context.** It is loaded through the `skills` field.

What stays a request:
- **Bash is still available.** Reviewers need it to run the suite, so "no commit, no push, no tag" is still asked, not enforced.
- **Command restrictions don't carry over from a plugin.** A plugin agent's `hooks` and `permissionMode` are ignored, and a tool entry with a specifier such as `Bash(git push *)` removes Bash altogether.
- **The fuller guarantee needs repository settings.** It is `permissions.deny` in the repository's `.claude/settings.json`, which binds the controller too, so the controller's own push must then run where those rules do not apply.

`model` is a default: a dispatch that names a model overrides it, as the controller does for the final review on the most capable model.

