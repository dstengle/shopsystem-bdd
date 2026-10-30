# requests, round 1: reply

## Coverage

| id | line | scenario |
|---|---|---|
| r59 | "**If** a line given to `work request` names an implementation detail or uses a word that is neither a term of the upstream's glossary nor a word of a Behaviour line under the upstream's `spec/capabilities/`, **then** `work request` shall refuse, naming the word and why it is refused, and change nothing." | none: the line admits two readings (see Questions), so it is returned as a question |

No other line was touched. No scenario was drafted, so there is no feature draft this round.

## Questions

1. r59: "names an implementation detail". Neither the line nor the Glossary says what an implementation detail is, or how `work request` can tell one.
   - Reading A: a line names an implementation detail when it uses a word or phrase that appears in an `## Implementation, may change` section of the upstream's `spec/capabilities/` (for example `.shop/work/requests/q<n>.md` or the frontmatter field `delegation`), and no Behaviour line uses it.
   - Reading B: a line names an implementation detail when it names how something is built (a file path, a module, a frontmatter field, a data format), whether or not any section of the upstream's spec names it. `work request` judges this itself.
2. r59: "a word of a Behaviour line". It does not say whether a different form of the word counts.
   - Reading A: the word has to appear exactly as written in some Behaviour line, so "raises" is refused when Behaviour lines have only "raise" and "raised".
   - Reading B: any form of a word that appears in a Behaviour line is allowed (raise, raises, raised, raising), and capital letters do not matter ("When" and "when").
3. r59: "a term of the upstream's glossary". It does not say whether a word listed after `Not:` in a Glossary entry is a term of the glossary.
   - Reading A: only the entry's term is a glossary term. A `Not:` word is allowed only if some Behaviour line uses it.
   - Reading B: a `Not:` word is refused even if some Behaviour line uses it, because the glossary rules it out.

## Cases no line mentions

- Tokens that are not plain words: commands and options in backticks (`work request`, `--thread`), ids (q7, ctx-a, thing#r3), numbers and dates. Are they words the check reads, and if so, which ones are allowed?
- A request whose purpose is to propose a new term. Under r59 its line can never be raised, because the word is in no Behaviour line and in no glossary entry yet.
- A term that a glossary-proposal of the upstream adds but that is not yet approved: is it a term of the upstream's glossary?
- Words that appear only in retired lines, Purpose, Not yet or Implementation, may change, and in no Behaviour line.
- A line that is not in strict form (r2) and also uses a refused word: which refusal `work request` gives, or whether it gives both.
- A line with several refused words: whether `work request` names all of them or only the first.
- Where the asker reads the upstream's glossary and Behaviour lines from, given that r28 says the asker has no checkout of the upstream's repository.

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/requests-7-formulate/.shop/scratch/7-formulate/drafts/round-1/requests.reply.md (this reply; there is no feature draft)
