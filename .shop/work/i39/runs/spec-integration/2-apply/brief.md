# apply of spec-integration

Capability-proposal: .shop/work/i39/spec-integration.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Drafts path: .shop/work/i39/runs/i39/1-integrate/drafts/round-1/
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-2-apply
Branch: round/spec-integration-2-apply
Answers the person gave, each with the question it answers:
- Question: spec-integration r44 (new line): "[r44] **Where** `spec/index.md` names an upstream bounded-context, **when** a round of the kind `integrate` drafts a line that needs what the upstream does not yet give, `initiative-round` shall give in its result the lines of a request into that upstream, in the upstream's terms." (request q14, line 23). The line says `spec/index.md` names an upstream but not how. Readings: (a) no further line; how the index names an upstream is Implementation only (recommended: the line already fixes the behaviour and the lines of q14 do not ask for a format); (b) a field: the frontmatter of `spec/index.md` lists `upstreams: [bounded-context/<context path>, ...]` (Implementation), and the index gains an "Upstreams" section. Answer (a) gives the line as drafted; answer (b) gives the line as drafted plus that Implementation entry and index section.
  Answer: 2026-10-27: r44: Reading (a), how spec/index.md names an upstream is Implementation only. Also folded in: a requirement line, a numbered table row included, is never edited in place; a change adds a replacement with a new id and retires the original.

Read (paths in your worktree):
- .shop/work/i39/spec-integration.md
- .shop/work/i39/runs/spec-integration/1-gate
- .shop/work/i39/runs/i39/1-integrate/drafts/round-1/

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-2-apply/.shop/scratch/2-apply
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/spec-integration-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
