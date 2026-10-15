# Test log: agents for each role (0.7.0)

**Baseline.** Before 0.7.0, a controller dispatched `general-purpose` agents for implementers and reviewers, and each rule of the role was asked for in the dispatch prompt:
- no subagents;
- a review is read-only;
- load `bdd-red-green` first;
- no push, no tag.

In the shopsystem-knowledge and shopsystem-kb batches of 2026-09-27, the rules held because every dispatch repeated them, but nothing enforced them. A general-purpose agent has the Agent tool, Edit, Write and full Bash. One final reviewer sent a synthetic table to an external markdown API to check an escape, which no prompt had forbidden.

**Change.** Four agents added: `bdd-implementer`, `bdd-task-reviewer`, `bdd-branch-reviewer` and `architecture-reviewer`. Each has only its role's tools, and the standing rules are written into its body, the external-service rule among them. The slicing skill's step 6 names the architecture reviewer and its coupling lens.

**Verification.**
- `claude --plugin-dir <this checkout> plugin details shopsystem-bdd` lists all five agents parsed (inventory: `Agents (5)`).
- A headless Sonnet session with the working copy loaded dispatched three of the agents. Each was told to use no tool and to report its tools and the skills already in its context. The replies, verbatim:
  - bdd-implementer: `TOOLS: Read, Edit, Write, Bash, Skill` / `SKILLS: shopsystem-bdd:bdd-red-green`
  - bdd-task-reviewer: `TOOLS: Read, Bash` / `SKILLS: none`
  - architecture-reviewer: `TOOLS: Read, Bash, Write` / `SKILLS: none`

  No agent has the Agent tool. The implementer has `bdd-red-green` preloaded. The reviewers have no Edit. Glob and Grep do not appear in that harness for any session, the main one included, so their absence is the harness's, not the agents'. GREEN for the structural rules.

**Not verified by a run.** The rules that stay requests (no commit, push or tag through Bash) are unchanged from 0.6.0, and are held by the agents' bodies as they were by the dispatch prompts.
