---
name: shaping-items
description: Use when a brainstorming with the person settles work to do, in a repository with a codified spec (spec/index.md with `language: codified-2`, the controlled language 4), before any design document or plan is written. Also use when the person describes behaviour they want built here, when a delivered line must change, or when `work ready` refuses an item's lines.
---

# Shaping Items

## Overview

A brainstorming ends in shaped items whose requirement lines pass the readiness bar, not in a long design document. The session writes the lines and readies the items; the person may skim the lines in the backlog and in the pull request. Do not ask the person to approve the lines: nothing waits on their reading.

An item's lines stay on the item (its `## Requirements`) until its batch merges; `spec/` is not written. `work ready` checks them on a copy of `spec/`: every line parses to one meaning in the context's grammar 4 (its capability's terms and the item's laid in), `model logic` finds no L0 nor an L1 naming them, `features generate` writes their scenarios, and every request line of the item is settled.

Scripts: `<this skill's base directory>/../../scripts/`. For larger work a design record is still written, beside the items, never in place of them. A design-decision it settles is written with `work decision` (`--help` gives its fields), and `model forms` names the command for any other file.

In this repository this skill wins over superpowers:brainstorming's ending: when both fire, the brainstorming ends here, in items with lines, not in "write the design doc" and a plan. A design record may sit beside the items.

No command rewords or removes an item's own line: `work line` only adds one. Such a line is reworded by editing its `- [r<n>]` bullet in the item's `## Requirements` (same id) and committing the item, or the item is withdrawn and shaped again. A line already in `spec/` is never edited in place: a changed one is a new line that retires it, `python3 <scripts>/work line <b> --retires <capability>#r<n> "<the new line>"` (it goes into that capability, its new id into `unbuilt:` and the old id under `retired:` when the batch lays it; a universal condition: `--universal "<statement>" --retires universal#U<n>`). A line that parses unchanged and means the same keeps its id. `work line <b> --recodify <capability>` is only for a capability whose file still says `language: codified-1` (`model check` refuses it, naming `migrate upgrade`, which switches every file).

- A bug in what a delivered item built: `python3 <scripts>/measure defect <item> --says "<the fault and how to reproduce it>"` first, then shape its fix as an item.

## Process

1. **Write the item.** `python3 <scripts>/work idea "<title>"`. For each thing the person said that the item rests on, run `python3 <scripts>/work quote "<their words, exactly as they wrote them>"`. It prints `quote-<n> "…"`; on a refusal, copy the words again from their message, or give `--session <id>` for an earlier session: its id is the name of its transcript, `<id>.jsonl`, in the project's directory under `~/.claude/projects/` (newest last by `ls -tr`), or give that file with `--transcript <path>`. Then `python3 <scripts>/work shape <b> --note "<the context to work from>, the person's words in quote-<n>"`.
2. **Write each behaviour as a line**, the way raising-a-request's steps 1-5 and its "Writing a line in 4.0" say: plain words in sentence structure (no coined adjective for a state), states in While and behaviour in When or If, the agent explicit, a command's option in the trigger, a refusal as "shall refuse the command and name X", example data in the given block, a format as an artifact the line conforms to, a construct or a check named by its code. Find the words with `python3 <scripts>/model lexicon`, check the line with `python3 <scripts>/model parse "<line>"`, read what it means with `python3 <scripts>/model parse --form "<line>"` (and `python3 <scripts>/model explain <capability>#r<n>` for a line it retires or sits beside), and reword from a refusal. A missing word is a term, never a synonym: write it with `python3 <scripts>/work line <b> --into <capability> --term "- **<term>** (<part of speech>): <one sentence>."`, the part of speech one of `noun`, `proper noun`, `adjective of <kind>` (defined by a sentence of the grammar), `attribute of <kind>`, `verb, action`, `verb, state` (with its `Frame:` lines) or `artifact`, and `Redefines: <pack>.` when a pack the context imports has the word. Write all the item's terms (and relation rows) first, then its lines: a term written so is on the item only, so `model parse` still refuses a line that uses it, and the readiness bar (step 4) checks that line with the item's terms laid in; each change to the terms recompiles the grammar there, which takes minutes, so the terms go in at once, before the bar first runs (step 4). Then `python3 <scripts>/work line <b> --into <capability> "<line>"`; a line of the same scenario as the one before joins its group with `--in g<n>`, and a new group takes `--group "<title>"`. The other spec pieces a line needs go on the item the same way, never into `spec/`: a relation row with `--into <capability> --relation "| <from> | <word> | <to> | <cardinality> |"`, a group's example data, the sample values a line's parameters take, with `--into <capability> --given g<n> "<given block>"` (one of the item's own groups), a universal condition with `--universal "<statement>"` and an upstream with `--upstream "bounded-context/<path>: <text>, github: <owner>/<name>"`.
3. **Rate it.** `python3 <scripts>/work rate <b> --value <v> --urgency <u> --size <s>`, with the reason for each in a note (`work shape`'s note, or the item's `## Notes`).
4. **Ready it.** `python3 <scripts>/work ready <b>`. On a refusal, reword the lines it names from its reasons (a parse refusal's `parsed up to:`, nearest words and `may follow`, a refusal naming an unbound "the", a verb's frame or two readings, a logic finding's clash, a group with no scenario), by editing their bullets in the item's `## Requirements` as the Overview says (running `work line` again adds a second line beside the bad one), and run it again. A warning (an L3) does not refuse; read it, and reword when the line is wrong.
5. **Tell the person afterwards** which items are ready and what their lines say, in the backlog's words: `python3 <scripts>/work backlog` and `python3 <scripts>/work show <b>`.
6. **Build it.** With an item `ready` and no batch open, start building-a-batch without asking the person: readying an item is the decision to build it.

## Red Flags

| Seen | Fix |
|---|---|
| A design document written in place of items | The brainstorming ends in items with lines (step 1-4); a design record only beside them |
| Asking the person to approve the lines before `work ready` | The bar is the check; tell the person afterwards (step 5) |
| A line bent onto a nearby word because the right one is missing | A term bullet with `work line --term` (step 2) |
| `spec/` edited to hold the item's lines | The lines live on the item until its batch merges; `work line` writes them there |
| An item left `shaped` after a refusal | Reword from the reasons and run `work ready` again |
| Asking the person whether to ready or batch an item | Ready it (step 4) and build it (step 6) |
| `work line` run again to fix a refused line | It adds a line; edit the bullet in `## Requirements` instead |
| Two lines with the same trigger and condition | One line, `shall A and B` |
| A new adjective for a state | The structure that holds it, in the lexicon's words (raising-a-request, Writing a line in 4.0) |
| `Where `--x` is given`, or a long refusal | The option in the trigger; `shall refuse the command and name X` |
| A sample value in a line | The group's given block, `work line --given` |
| A delivered line's text edited in `spec/` or on the item | `work line --retires <capability>#r<n>`: a new id, the old one retired |
| A term added between two `work ready` runs | Every term first, then the lines and one `work ready` |
| `model parse --capability` | Gone: `model parse` reads grammar 4 from `spec/index.md` |
| The person's words pasted into a note with no quote | `work quote` keeps the turns around them; cite quote-<n> (step 1) |
