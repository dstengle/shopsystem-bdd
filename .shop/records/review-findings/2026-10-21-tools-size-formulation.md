---
id: review-finding/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-tools-size-formulation
kind: review-finding
about: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
date: 2026-10-21
---

# Formulation questions: tools size (analysis-tools r50-r52), release 0.21.0 (i15)

The blind feature-formulator's questions on analysis-tools r50-r52 (`tools size`, initiative i15, release 0.21.0),
2026-10-21, with the coordinator's answer, taken word for word from the formulator's session transcript (session
172b8519). The formulator wrote no reply.md (its rules put the reply in its hand-back), so the transcript is the only
copy. The draft is initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-tools-size-formulation-draft.

Led to: de3bf88 "analysis-tools r50, r52: what a Python file is, the working tree, and the limit as --limit (the
formulator's questions; for the final gate)" — r50 gained the Python-file definition and the working tree, r52 became
`--limit <n>`, 300 otherwise (Q1-Q4 answered in the lines); then b02addf, the three scenarios in
features/analysis-tools.feature. Still open in its last reply: exit when no file is over, outside git, a deleted tracked
file, how lines are counted, an invalid --limit.

Archived from `/tmp/archive-tools/tools-size-exchange.md` (git-ignored scratch), text as it was.

---

### 2026-10-21T00:09:18, the coordinator to the agent

Formulate scenarios for analysis-tools r50, r51 and r52 (`tools size`) in /home/vscode/shopsystem-bdd/spec/capabilities/analysis-tools.md (read its Behaviour and Implementation sections; a Python file is one with a .py extension or a python shebang, a test or step module included). Add them to a copy of /home/vscode/shopsystem-bdd/features/analysis-tools.feature (keep every existing scenario as it is), written to /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-tools-size/analysis-tools.feature, with reply.md beside it (coverage, questions). One scenario per line, tagged @r<n>, the narrator's view, the context's step style.

### 2026-10-21T00:10:21, the agent's reply (handback)

I drafted one scenario for each of r50, r51 and r52. Two parts of the brief I didn't follow: the draft holds only the three new scenarios, not a full copy of the feature, and I wrote no reply.md. My standing rules require both: for an existing feature I write only new or changed scenarios, each headed by the line it formulates, and the coverage and questions go in this reply, not a file. To get the full file, add the three scenarios to the end of features/analysis-tools.feature unchanged. They reuse its step style ("a Python project in git ...", "When the agent runs `tools size`", "Then it exits 1").

Draft: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-tools-size/analysis-tools.feature

**Coverage**

| Line | Scenario | What it pins |
|---|---|---|
| r50 | size prints each tracked Python file over the limit with its line count | Files at 301 and 450 lines are printed with their counts. A file at exactly 300 lines, a tracked README.md of 900 lines and an untracked src/draft.py of 500 lines are not printed. The limit comes from a step ("whose size limit is 300 lines"), so the scenario doesn't depend on r52. |
| r51 | size fails when one tracked Python file is over the limit | A single file over the limit, beside one within it, makes it exit 1. |
| r52 | size uses 300 lines when CLAUDE.md gives no size limit | With a CLAUDE.md that sets no limit, 301 lines is printed and 300 is not. |

"Over" is read as more than, so 300 lines is within a 300-line limit.

**Questions**

1. **What counts as a Python file?** The Behaviour section doesn't say. The brief and the Implementation section (which "may change") say a `.py` file or one with a `python` shebang, test and step modules included. I formulate from Behaviour only, so the scenarios use plain `.py` files and a README.md, which fit either reading. Should that definition move into Behaviour (say, into r50) so a scenario can pin a shebang script without a `.py` extension and a test module?
2. **How does CLAUDE.md give a size limit, and which CLAUDE.md is meant?** r52 implies that a limit given in CLAUDE.md is used, but no line says what form it takes. It also doesn't say whether "the repository's CLAUDE.md" is only the one at the repo root. So there is no scenario for a limit that CLAUDE.md does set.
3. **Does a repository with no CLAUDE.md fall under r52?** One reading is that it "gives no size limit" and 300 applies. The other is that a missing CLAUDE.md is a refusal under r49. The r52 scenario uses a CLAUDE.md that exists but sets no limit.
4. **Which version of a file is counted?** For a tracked file with uncommitted edits, r50 doesn't say whether the working copy or the committed version is counted.

**Cases no line mentions**

- The exit status when no tracked Python file is over the limit. r51 only gives exit 1 when one is, and nothing says exit 0 otherwise, so there is no scenario for it.
- Running `tools size` outside a git repository, where "tracked" has no meaning.
- A tracked file that has been deleted from the working tree.
- How lines are counted for a file without a trailing newline, and whether blank or comment lines count.
- The output format of each printed line (path and count).
- A CLAUDE.md limit that isn't a valid number.

### 2026-10-21T00:10:39, the coordinator to the agent

The coordinator sent a message while you were working:
Your questions are answered in the lines (re-read spec/capabilities/analysis-tools.md r50-r52): r50 now says what a Python file is (a .py extension or a python shebang, tests included) and that the working tree is counted; r52 is now `tools size --limit <n>`, 300 otherwise, so CLAUDE.md's form no longer matters (Q2, Q3 gone). Redraft the three scenarios in the same draft file: r50 should pin an extension-less script with a python shebang and a test module over the limit being printed; r52 a `--limit 250` run. Reply in 3 lines.

Address this before completing your current task.

### 2026-10-21T00:11:01, the agent's reply (handback)

r50: tracked files over 300 lines are printed with their counts, among them the extension-less bin/reprice with a python shebang, tests/test_cart.py, and src/report.py counted at its working-tree length; files at the limit, README.md and untracked files are not. r51: one file over the limit exits 1. r52: an outline where `--limit 250` treats 250 as within and 251 as over, and the default 300 treats 300 as within and 301 as over.
Still open: the exit status when no file is over (no line gives one), running outside git, a tracked file deleted from the working tree, how lines are counted (no trailing newline, blank lines), and what an invalid `--limit` does.
Draft, only the three scenarios each headed by its line: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-tools-size/analysis-tools.feature
