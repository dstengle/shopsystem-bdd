---
name: shaping-items
description: Use when a brainstorming with the person settles work to do, in a repository with a codified spec (spec/index.md with `language: codified-1`), before any design document or plan is written. Also use when the person describes behaviour they want built here, or when `work ready` refuses an item's lines.
---

# Shaping Items

## Overview

A brainstorming ends in shaped items whose requirement lines pass the readiness bar, not in a long design document. The session writes the lines and readies the items; the person may skim the lines in the backlog and in the pull request. Do not ask the person to approve the lines: nothing waits on their reading.

An item's lines stay on the item (its `## Requirements`) until its batch merges; `spec/` is not written. `work ready` checks them on a copy of `spec/`: every line parses in the context's grammar, `model logic` finds no L0 nor an L1 naming them, `features generate` writes their scenarios, and every request line of the item is settled.

Scripts: `<this skill's base directory>/../../scripts/`. For larger work a design record is still written, beside the items, never in place of them.

In this repository this skill wins over superpowers:brainstorming's ending: when both fire, the brainstorming ends here, in items with lines, not in "write the design doc" and a plan. A design record may sit beside the items.

No command rewords or removes an item's line yet: `work line` only adds one. A line is reworded by editing its `- [r<n>]` bullet in the item's `## Requirements` (same id) and committing the item, or the item is withdrawn and shaped again.

## Process

1. **Write the item.** `python3 <scripts>/work idea "<title>"`, then `python3 <scripts>/work shape <b> --note "<the context to work from>"`. Until `work` keeps quotes (brainstorming r3), cite the person's words in the note with the date: `The person, 2026-11-04: "<their words>"`.
2. **Write each behaviour as a line**, the way raising-a-request's steps 1-5 say: find the words with `python3 <scripts>/model lexicon`, check the line with `python3 <scripts>/model parse "<line>"`, and reword from a refusal. A missing word is a term, never a synonym: write it with `python3 <scripts>/work line <b> --into <capability> --term "- **<term>** (<category>): <one sentence>."`. A term written so is on the item only, so `model parse` still refuses a line that uses it; the readiness bar (step 4) checks that line, with the item's terms laid in. Then `python3 <scripts>/work line <b> --into <capability> "<line>"`; a line of the same scenario as the one before joins its group with `--in g<n>`, and a new group takes `--group "<title>"`.
3. **Rate it.** `python3 <scripts>/work rate <b> --value <v> --urgency <u> --size <s>`, with the reason for each in a note (`work shape`'s note, or the item's `## Notes`).
4. **Ready it.** `python3 <scripts>/work ready <b>`. On a refusal, reword the lines it names from its reasons (a parse refusal's `parsed up to:` and nearest words, a logic finding's clash, a group with no scenario), by editing their bullets in the item's `## Requirements` as the Overview says (running `work line` again adds a second line beside the bad one), and run it again. A warning (an L3) does not refuse; read it, and reword when the line is wrong.
5. **Tell the person afterwards** which items are ready and what their lines say, in the backlog's words: `python3 <scripts>/work backlog` and `python3 <scripts>/work show <b>`.

## Red Flags

| Seen | Fix |
|---|---|
| A design document written in place of items | The brainstorming ends in items with lines (step 1-4); a design record only beside them |
| Asking the person to approve the lines before `work ready` | The bar is the check; tell the person afterwards (step 5) |
| A line bent onto a nearby word because the right one is missing | A term bullet with `work line --term` (step 2) |
| `spec/` edited to hold the item's lines | The lines live on the item until its batch merges; `work line` writes them there |
| An item left `shaped` after a refusal | Reword from the reasons and run `work ready` again |
| `work line` run again to fix a refused line | It adds a line; edit the bullet in `## Requirements` instead |
| Two lines with the same trigger and condition | One line, `shall A and B` |
