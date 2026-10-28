---
name: writing-requirements
description: Use when writing or rewording a requirement line, whether a request's line for `work request`, a Behaviour line the capability-writer drafts, or a line an answer asks for, in a repository with spec/ capability files with [r<n>] ids. Also use when a line has two responses, when choosing between When, If, While and Where, when a word is not in the glossary, or when a new line touches what an existing line already does.
---

# Writing Requirements

## Overview

A line that leaves something to infer comes back as a question at the gate. Each such question costs the person a
round trip, and often another `integrate` and `gate` round. In i39–i43, 24 of 42 gate questions came from the wording of
a line: 13 from existing lines, 8 from requests and 3 from undefined terms. Only 6 were decisions. Write the line so the
gate has only decisions left.

The format is `docs/capability-format.md` ("Writing the behaviour section"). The terms are the glossary in
`spec/index.md`. `model check` holds the strict form (`v_e1`, `v_e2`), and `work request` refuses a line not in it. This
skill covers what that check cannot see.

**A request line proposes. The upstream owns the wording.** Write the behaviour you need. Do not write where it is
stored or how it travels, and do not fight for a phrasing.

## One line

1. **Choose the keyword by what starts the behaviour**, not by the wording of your note:

   | Starts it | Keyword | Example |
   |---|---|---|
   | a command, an input, an event | `When` | When `work run` starts a branch review, … |
   | a refusal or a fault | `If …, then` | If a worker ends without a result file …, then … |
   | a period during which it holds | `While` | While a request … is not `delivered`, … |
   | an option or configuration | `Where` | Where `--by-file` is given, … |
   | nothing: always true | none | The branch reviewer shall … |

   Combine the keywords in this order: Where, While, then one When or If.

   "Where the branch reviewer finds…" is an event, so it takes **When** (q23 line 5).

2. **One trigger, one `shall`, one response.** "…set the proposal `drafted`, its earlier drafts kept…" is two responses
   (q18 line 4, q19 line 3). Write them as two lines with the same trigger. Conditions that share one response join in
   one line: `If A or B, then …`. The general failure trailer "exit with an error, say why, and change nothing" is one
   response.

3. **Every noun that matters is a glossary term, used in its glossary sense.** Run
   `grep -n '^- \*\*' spec/index.md` and read the entries you use. If a word is missing:
   - a request names it in a line of its own as a proposed term ("**message**: …"), or uses the term the glossary has;
   - the writer drafts the entry and raises it as a question with the entry it would write.

   These words were asked about: "message" (q14), "belongs to" a work-item (q23 line 2), "run" as a noun (r155), and
   "capability-proposal", "drafts" and "change list" (used, never defined).

4. **No implementation detail.** Exits are in words: "exits successfully" or "exits with an error", never an exit code
   (design-decision/exits-are-successful-or-errors). A carrier, a port, a file format, a field, a column, the words of
   a message: all go to the Implementation section, or to the upstream. "exit code" (q23 line 1), "carrier … behind one
   port, with a file … and an issue on … GitHub" (q14 line 2) and "the fields of the contract's form" (q14 line 22)
   each drew a question.

5. **The response is something the narrator observes:** a value, a file at a path, a status, a refusal and the reason
   it names.

## Against the lines that exist

Before you write, read the capability's Behaviour section for every line with the **same system and the same subject**.
For a round, that means every line on that kind of round.

1. **A catch-all trigger catches your line too.** "When a round of the kind `apply` … ends having applied its drafts"
   (r144–r146) and "ends without giving a question" (r83) fire for every new outcome of that round. Before a line adds
   an outcome ("applies nothing because…", "formulates nothing because…"), check every "ends" line of that kind.
   Then do one of:
   - **name** the existing line and say which wins in your note;
   - **retire** it and add a replacement whose trigger excludes your case.

   Missing this cost i40's dropped question, q19 and all of i41 (r80/r71/r114), and the i42 questions on
   r144–r146 and r83.

2. **A closed list goes out of date.** A ubiquitous line that lists what counts as something (r132: a stage's output)
   needs your new case added. Retire it and add the longer list.

3. **Widening is replacing.** A line that does what an existing or retired line does, for more cases, names that line
   and retires it. q22 line 3 widened r140 without naming it, and the gate had to ask (#10). q19 named r80 and r71 and
   was not asked.

4. **A prohibition binds every line of its system.** "The branch reviewer shall run nothing" (r32) conflicts with every
   reviewer line that presupposes a run: wall time (r7), a check it "cannot verify" (r6), "its reproduction" (r12). Name
   each, and say how it holds now.

5. **Never edit a line in place.** A changed line gets a **new id**. The old id goes to `retired`. No line overrides
   another (the person, `.shop/work/i39/ledger.md:83-84`).

   **Note:** `docs/capability-format.md:162`, `agents/capability-writer.md:22` and the "keeps its id" sentences in other
   skills still say a changed line keeps its id. Until they change, follow the person's rule and name the conflict.

In a request, put the ids in its text: "replaces supervision r140 (retired)", "r83 stands; this line is its exception",
"narrows review r12".

## Red flags

| You wrote | What the gate asked | Write instead | Check that sees it |
|---|---|---|---|
| **Where** the reviewer finds… (q23 line 5) | "Should Where become When?" | **When** a branch review finds… | `where_event` (ASP p1) |
| …shall set the proposal `drafted`, its earlier drafts kept… (q18 line 4) | "Split into two lines?" | Two lines, one trigger | two responses (p2; Haiku: `responses`) |
| …each one's command, **exit code** and output (q23 line 1) | "Exit code or how it exited?" | …how it exited… | implementation lexicon |
| …keep the **carrier** behind one **port**… (q14 line 2) | "Where is this kept?" | Leave storage to the upstream | implementation lexicon, novel word |
| a request **or a message** (q14 lines 18, 20, 22) | "What is a message?" | A glossary term, or a proposed entry | Haiku: `undefined_terms` |
| the work-item it **belongs to** (q23 line 2) | "When does a commit belong to a work-item?" | A term: **work-item's commits** | Haiku: `undefined_terms` |
| When an `apply` round gives … (q22 line 3), r140 unnamed | "Retire r140?" | "…replaces r140 (retired)" | widens (ASP c3) |
| A new round outcome, with r144–r146 or r83 left "ends…" | "Does a partial apply count as having applied?" | Retire and replace the catch-all, or name the exception | catch-all (ASP c2), conflict (c1) |
| A new outcome, r132's list unchanged (q19, q22) | "What is this round's output?" | Retire r132 and add the longer list | Haiku: closed list |
| The branch reviewer shall run nothing (q23 line 4) | r7, r6, r12 each asked | Name r6, r7 and r12 and say how each holds | presupposes (ASP c4) |
| A changed line keeping its id (i39 requests r3) | "Changed or replaced?" | New id, old one retired | — |
| "one set of commands (raise, take in, …) and one lifecycle" (q14 line 1) | asked twice | One line for each command | two responses (p2) |

## Before you hand it on

- The keyword fits what starts the behaviour.
- The line has one `shall` and one response.
- Every noun is a term in its glossary sense, or a proposed entry comes with it.
- There are no codes, fields, carriers or formats.
- Every existing line with the same system and subject was read. Each one this line narrows, widens, conflicts with,
  falls inside or retires is named by id.
- `model check` shows no new `v_e1` or `v_e2`.
