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
