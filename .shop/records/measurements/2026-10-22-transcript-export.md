---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-22-transcript-export
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
---

# Transcript export, through 0.21.0

The slim export of this repository's Claude Code transcripts through 0.21.0 (217 transcripts: 9 sessions and their
subagents; 13 MB of JSONL text: per entry time, type, session, agent, model, token usage, the tools called and the
text, no tool inputs or outputs) is in https://github.com/dstengle/shopsystem-records, path
`transcripts/2026-10-shopsystem-bdd-0.21.0/`, commit f31120e. Made by that repository's `tools/export_transcripts.py`;
checked by gitleaks 8.21.2 (no leaks) and for email addresses (only the author's and noreply) before the push.
For i12's measurement. The raw transcripts (168 MB) stay under ~/.claude/projects/ until Claude Code removes them.

## Through 0.22.0

The second export, a full snapshot through 0.22.0 (230 transcripts: the 9 sessions of the main project directory
and their subagents, plus the two `.shop/worktrees/*-research` directories that `work run` workers ran in), is in
the same repository at `transcripts/2026-10-shopsystem-bdd-0.22.0/`, commit fce2939. Files unchanged since the
0.21.0 export share their git blobs. Checked by the pre-push hook (gitleaks: no leaks; email check) before the push.
The session that delivers 0.23.0 (0a7907e0) is not in it.
