# The spec corpus

The acceptance test of grammar 4 (b240): every live line of this repository's spec in the new language, under its id,
with the reading it is meant to have. One file a capability, `<capability>.md`, and `universal.md` for
`spec/universal.md`'s conditions.

A file holds a heading `# <capability>: ...`, then a section a line:

````
## r103
Retires: r45. From: b153 r89. Audit: distortion, fixed by section 5 ("not close the issue of the request").

```reading
If the person runs `work reply` on a request that this bounded context received, then `work` shall refuse the command and name the request.
shall [x1: agent the person (constant), ...]
  if [...]
    ...
  response
    ...
```
````

- The heading is the line's id (`r<n>`, or `U<n>` in `universal.md`).
- The line under it is the trace: the id the line retires, the item line it reuses, the audit's verdict and what
  fixed it (`Retires: r45. From: b153 r89. Audit: ...`), or `Known limit: #<n>` with the construct of
  `grammar/language.md`'s "What the language cannot say yet" it waits on. A line kept from the old spec says `Kept.`
- The block is the line, word for word as the capability file has it, then its logical form as `model parse --form`
  prints it. The form is the **intended** reading: written from the old line's meaning, the audit's row and the
  item's notes, never copied from the parser unread. Where the parser prints a form already, read it against the old
  line atom by atom, and write it down only when it agrees.

`tests/scripts/test_corpus_spec.py` checks every block:

1. the line parses in grammar 4 to one meaning, and its form is the block's;
2. the form translates to `model logic`'s facts and, for a "shall" line, to `features generate`'s steps, with no
   refusal;
3. for each file whose marker is `language: codified-2`, the corpus file has a block for every live id and for no
   other, each block's line the file's line word for word (a file still codified-1 needs no corpus file);
4. the line's tree linearises back to the line.

## Adding a block

1. Write the line and its intended form under the line's new id, with its trace.
2. Run `python3 -m pytest -q tests/scripts/test_corpus_spec.py`: it fails (check 3 names a block of no live line,
   and check 1 a form that grammar 4 does not give yet).
3. Lay the line into its capability file (the old id into `retired:`) and build what check 1 or 2 still names, until
   the test passes.
