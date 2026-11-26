"""What the upgrade step "the controlled language 4" cannot reword, read off the rewritten spec (the CNL 4 design, I29):
`notes(copy, said)` over a copy of `spec/` the step's rewrites are laid on and its lines (file, id, text), by file and
id: each line grammar 4 refuses, with the refusal's reason ("the" with no antecedent and a negated indefinite in a
While clause told apart); each condition (adjective) and the lines using it, which grammar 4 reads no definition of;
each line holding example data (spec_example); each long-form refusal ("exit with an error naming") that "refuse the
command and name" says shorter; each relation row of no cardinality on of, for, with, on or in, which the old check
read as one; each term an imported pack defines too (v_t16). A spec grammar 4 cannot be built of is said in one note."""
import re

import spec_example
import spec_language
import spec_lexicon
import spec_logic_vocab
import spec_packs

NAME = "the controlled language 4"
LONG = "exit with an error naming"


def _note(rel, ident, what):
    return "%s: %s %s %s" % (NAME, rel, ident, what)


def refused(why):
    """What a refusal of grammar 4 says of a line, in the words of the report."""
    if "has no antecedent" in why:
        return 'says "the" with no antecedent: %s' % why
    if "the While clause says \"does not" in why:
        return "says a negated indefinite in a While clause: %s" % why
    return "no longer parses: %s" % why


def parses(copy, said):
    try:
        why = [(rel, i, spec_language.parse(copy, text).refusal) for rel, i, text in said]
        return [_note(rel, i, refused(r)) for rel, i, r in why if r]
    except Exception as error:      # noqa: BLE001 -- a vocabulary GF cannot compile: said, the upgrade goes on
        return ["%s: grammar 4 could not be built of this spec, so no line was parsed: %s" % (NAME, error)]


def uses(text, word):
    return re.search(r"(?<![\w`-])%s(?![\w`-])" % re.escape(word), text) is not None


def conditions(lexicon, said):
    out = []
    for t in lexicon.of("condition"):
        users = ["%s %s" % (rel, i) for rel, i, text in said if uses(text, t.term)]
        out.append("%s: %s %s is a condition (adjective) grammar 4 reads no definition of; say it with a structure in "
                   "each line using it: %s" % (NAME, t.where, t.term, ", ".join(users) or "none"))
    return out


def examples(lexicon, said):
    known = spec_example.constants(lexicon)
    out = []
    for rel, i, text in said:
        found = spec_example.parameters(text, known)
        if found:
            out.append(_note(rel, i, "holds example data: %s; give it in its group's given block" % ", ".join(
                "`%s`" % w for w in found)))
    return out


def long_refusals(said):
    return [_note(rel, i, 'says "%s": "refuse the command and name" says it shorter' % LONG)
            for rel, i, text in said if LONG in text]


def rows(lexicon):
    return ["%s: %s the row %s | %s | %s has no cardinality, which the old check read as one: write `one` where one "
            "is meant" % (NAME, r.where, r.k1, r.word, r.k2) for r in lexicon.rows
            if not r.cardinality.strip() and r.word.strip().lower() in spec_logic_vocab.PREPOSITIONS]


def redefined(copy, lexicon):
    return ["%s: v_t16 %s, %s: the pack %s defines it too; mark the entry Redefines: %s"
            % (NAME, term, where, ", ".join(packs), ", ".join(packs))
            for (where, term), packs in sorted(spec_packs.unmarked(copy, lexicon).items())]


def notes(copy, said):
    lexicon = spec_lexicon.read(copy)
    return (parses(copy, said) + conditions(lexicon, said) + examples(lexicon, said) + long_refusals(said)
            + rows(lexicon) + redefined(copy, lexicon))
