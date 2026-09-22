# shopsystem-bdd
Claude Code plugin for the shopsystem harness: a behaviour-driven workflow
that replaces test-driven development with Gherkin feature files as the
contract, thin vertical slicing, and one human gate at feature approval.

Skills: `formulating-features`, `slicing-into-increments`, `bdd-red-green`.
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

## Install

```
claude plugin marketplace add dstengle/shopsystem-bdd
claude plugin install shopsystem-bdd@shopsystem-bdd
```

While developing, `claude --plugin-dir <path to this checkout>` loads the
working copy instead.
