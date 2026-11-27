---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-27-guided-tutorial-plugins-and-patterns
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-27
---

# Guided tutorial plugins and patterns

A web search (2026-11-27) for Claude Code plugins, skills or output styles, and analogues for other coding agents, that run an interactive guided tutorial checking each step's outcome; for b869 (quote-116). Plugin pages were read mostly as search snippets; quality and maintenance unchecked.

## Found

- No tool walks a user through a tool's own docs building a sample product with each step checked. Community onboarding skills exist, mostly for learning Claude Code itself; Anthropic ships no tutorial skill. Nothing for Cursor, Codex, Aider or Copilot beyond rules/instructions files.
- guide (github.com/orinachum/claude-code-guide): `/guide:onboard` walkthrough and a hook-tracked "game mode"; no step checks.
- claude-code-hero: lessons as numbered "level" skills. claude-code-tutor: Anki-based quizzes unlocking topics. cc-self-train: picks a project, checks the environment, scaffolds (page refused fetch). claude-code-workshop: hands-on workshop. code-tour, learning-guide: a codebase or design doc turned into a guided tour.

## Claude Code mechanisms

- Output styles: built-in Explanatory and Learning (`TODO(human)`), effective only after `/clear`, main conversation only.
- Skills with `disable-model-invocation: true`, run only when the user calls them; a slash command as the entry point (`/tutorial`, `/tutorial next`); a SessionStart hook announcing the current step, as this plugin already prints live state.

## Patterns worth borrowing

- Killercoda/Katacoda: a verify script per step gating the next, and a solution script per step.
- Rustlings: progress held in the files, a fixed order, `verify` and `list`.
- GitHub Skills: one numbered file per step, advanced by real events.
- vimtutor: a throwaway copy, one concept a step, restartable.
- Notebook-style assertions after each step that fail with a hint.

## Recommendation

A `/tutorial` skill the model does not start on its own, reading a step manifest beside the docs: each step its doc section, what the person says, a check command and its expected outcome. Progress in the sample product's folder (`.tutorial/state.json`), resumable and announced by the SessionStart hook. Per step: explain, let the person (or Claude, if asked) act, run the check, move on only when it passes, on failure show the difference and the doc anchor. Each step also has a solution; running every solution in order is the end-to-end test of b868 that keeps the tutorial and the docs in step. The Learning output style offered, not required.
