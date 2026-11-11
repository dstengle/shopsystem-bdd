"""The constructs of grammar 4 (b240, quote-23): each a code, its label, its form, the grammar's functions it is made
of and an example line, from which `model constructs --write` (model_constructs) writes the construct catalogue
`grammar/constructs.md`. `funs` is a regular expression a function's whole name matches; `frame:<role>` names the
verb functions whose frame has that role (model_constructs.roles). `uses`, where given, is what the example's tree
must hold (a regular expression over the tree's text); else it must hold one of `funs`. WORDS and GLUE are the
families of functions that are words of a context or the joints of every line, not constructs."""

K, T = r"k_\w+", r"t_[a-z0-9_]+_\d+"
WORDS = r"%s_n|a_\w+|%s_v_\w+|Many\d+|Count_\d+|CodeLit" % (K, T)
GLUE = r"%s_(?:UseN|Det|One|Simple|Up_k_\w+|OneAct)|OneCond|OneResp|NoPre|PPos" % K
NEG = "PNeg"


def c(code, label, form, funs, example, uses=None):
    return {"code": code, "label": label, "form": form, "funs": funs, "example": example, "uses": uses}


CONSTRUCTS = [
    # the line
    c("when", "a line whose trigger is an event", "When <trigger>, <response>.", "When",
      "When a session ends a stage, `work` shall print the stage."),
    c("if-then", "a line of an unwanted event, which takes precedence over a line of another form on its trigger",
      "If <trigger>, then <response>.", "If",
      "If `work` refuses a command, then `work` shall exit with an error naming the command."),
    c("no-trigger", "a line of responses with no trigger", "<response>.", "Ubiq",
      "`work` shall not write a file."),
    c("always-never", "a line that holds at every moment", "<subject> always|never <verb> <object>.",
      r"Necessary|MAlways|MNever|%s_Nec" % K,
      "A session always follows a stage."),
    c("while", "a condition that holds while the trigger happens", "While <condition>, ...", "While",
      "While a stage is `open`, when a session ends the stage, `work` shall print the stage."),
    c("where", "a condition of the context the line is built into", "Where <condition>, [while <condition>,] ...",
      "Where|WhereWhile",
      "Where a stage is `open`, when a session writes a file, `work` shall print every file."),
    c("and-condition", "two conditions that both hold", "<condition> and <condition>", "AndCond",
      "While a stage is not `done` and sessions follow the stage, when a session ends the stage, `work` "
      "shall print the stage."),
    c("or-condition", "two conditions of which one holds, each a case of the line", "<condition> or <condition>",
      "OrCond",
      "While a stage is `open` or a stage is `done`, when the person runs `work start`, `work` shall exit "
      "successfully."),
    c("and-response", "two responses or two acts of one doer", "<response>, and <response>; <act> and <act>",
      r"AndResp|%s_AndAct" % K,
      "When a session ends a stage, `work` shall set the status of the stage to `done` and print the stage."),
    c("shall", "a response the doer is obliged to", "<doer> shall <act>", r"%s_Shall" % K,
      "When a session ends a stage, `work` shall write a file."),
    c("may", "a response the doer is permitted", "<doer> may <act>", r"%s_May" % K,
      "A session may write a file."),
    c("not-response", "a response that forbids its act", "<doer> shall not <act>", r"%s_Act_k_\w+|%s" % (K, NEG),
      "`work` shall not write a file.", r"_Act_k_\w+ PNeg"),
    # triggers and conditions
    c("event", "a trigger: an agent's act", "<subject> <action verb> ...", r"%s_Event" % K,
      "When a session writes a file, `work` shall print the file."),
    c("state-condition", "a condition: a state verb", "<subject> <state verb> ...", r"%s_Holds" % K,
      "While a session follows a stage, when the person runs `work start`, `work` shall print the stage."),
    c("not-condition", "a condition that does not hold", "<subject> does not <verb> ...; ... is not <value>",
      NEG,
      "While a stage is not `done`, when a session ends the stage, `work` shall print the stage.",
      r"_(?:Holds|Done|DoneSince|Is|IsOf|IsCode|IsCodeOf|Cmp|Within) PNeg"),
    c("done", "a condition of history: an act that has happened", "<subject> has <past participle> ...",
      r"%s_Done" % K,
      "While a session has ended a stage, when the person runs `work start`, `work` shall print the stage."),
    c("done-since", "a condition of history after a moment", "<subject> has <past participle> ... since <moment>",
      r"%s_DoneSince" % K,
      "While a session has written no file since `2026-01-01`, when the session ends a stage, `work` shall "
      "print the stage."),
    # a verb's frame
    c("object-role", "a verb's object, the kind right after the verb", "<subject> <verb> <object>", "frame:object",
      "When a session writes a file, `work` shall print the file."),
    c("to-role", "a verb's role after \"to\"", "<subject> <verb> [<object>] to <role>", "frame:to",
      "When the person runs `work start`, `work` shall give a file to a session."),
    c("oblique-role", "a verb's role after a preposition other than \"to\"",
      "<subject> <verb> ... <preposition> <role>",
      "frame:oblique",
      "When the person runs `work start` on a stage, `work` shall print the stage."),
    c("fixed-words", "fixed words of a verb's frame with no role after them", "<subject> <verb> <fixed words>",
      "frame:fixed",
      "When the person runs `work start`, `work` shall exit successfully."),
    # relative clauses
    c("rc-subject", "a relative clause whose subject is the noun", "<noun> that <verb> ...", r"%s_Rel_k_\w+" % K,
      "When a session ends a stage, `work` shall print every session that follows the stage."),
    c("rc-object", "a relative clause whose object is the noun", "<noun> that <subject> <verb>",
      r"%s_Obj_k_\w+|g_\w+|r\d+_\w+_Gap" % K,
      "When the person runs `work start`, `work` shall print every stage that a session follows."),
    c("rc-whose", "a relative clause on the noun's attribute", "<noun> whose <attribute> is <value>",
      r"%s_Whose_t_\w+" % K,
      "When the person runs `work start`, `work` shall print every stage whose status is `done`."),
    c("rc-whose-relation", "a relative clause on the noun's relation", "<noun> whose <noun2> <verb> ...",
      r"%s_Whose_r\d+_k_\w+" % K,
      "When the person runs `work start`, `work` shall print every session whose worktree holds a file."),
    c("not-relative", "a relative clause that does not hold", "<noun> that does not ...; <noun> whose ... is not",
      NEG,
      "When the person runs `work start` on a session, `work` shall print every stage that the session does "
      "not follow.", r"_(?:Rel_k_\w+|Obj_k_\w+|Whose_\w+) PNeg"),
    # noun phrases
    c("a-noun", "any one in a condition or a trigger, a new one in a response", "a <noun>", "DetA",
      "When a session ends a stage, `work` shall write a file."),
    c("the-noun", "the one the line gave before", "the <noun>", "DetThe",
      "When a session writes a file, `work` shall print the file."),
    c("every", "each one", "every <noun>", "DetEvery",
      "When the person runs `work start`, `work` shall print every stage."),
    c("bare-plural", "a noun in the plural with no determiner", "<nouns>", "DetPl",
      "When sessions write a file, `work` shall print the file."),
    c("the-plural", "the ones the line gave before", "the <nouns>", "DetThePl",
      "When sessions write a file, `work` shall print the sessions."),
    c("no-noun", "there is none", "no <noun>", "DetNo",
      "While no file exists, when the person runs `work start`, `work` shall exit successfully."),
    c("count", "a number of them, bounded", "at least|at most|exactly|more than|fewer than <number> <nouns>",
      r"DetCount|AtLeast|AtMost|Exactly|MoreThan|FewerThan",
      "When the person runs `work start`, `work` shall print at least two stages."),
    c("one", "exactly one", "one <noun>", "DetOne",
      "When the person runs `work start`, `work` shall print one stage."),
    c("same", "the one an earlier noun names", "the same <noun>", "DetSame",
      "While two sessions follow the same stage, when the person runs `work start`, `work` shall end the "
      "stage."),
    c("another", "one other than an earlier one", "another <noun>", "DetAnother",
      "When a session gives a file to another session, `work` shall print the file."),
    c("different", "one other than an earlier one", "a different <noun>", "DetDifferent",
      "When a session gives a file to a different session, `work` shall print the file."),
    c("two", "two distinct ones", "two <nouns>", "DetTwo",
      "When a session ends a stage, `work` shall write two files."),
    c("and-list", "noun phrases joined by \"and\"", "<np>, <np> and <np>",
      r"%s_And|%s_Two|%s_More" % (K, K, K),
      "When a session ends a stage, `work` shall print the status of the stage and the worktree of the "
      "session.", r"%s_And\b" % K),
    c("or-list", "noun phrases joined by \"or\"", "<np> or <np>", r"%s_Or" % K,
      "When the person runs `work start`, `work` shall print a file or a stage."),
    c("only", "nothing but these", "only <np>", r"%s_Only" % K,
      "A session shall change only files in its worktree."),
    c("its", "the noun's own, of the subject of its clause", "its <noun>", r"%s_Its|%s_Its" % (K, T),
      "When a session writes a file in its worktree, `work` shall print the file."),
    c("this", "the run's own thing", "this <noun>", r"%s_This" % K,
      "When the person runs this command, `work` shall print this command."),
    c("nothing", "no thing at all", "nothing", r"%s_Nothing" % K,
      "If `work` refuses a command, then `work` shall change nothing."),
    c("code", "a code as a thing", "`<code>`", r"%s_Code" % K,
      "`work` shall not change `spec/index.md`."),
    c("named", "a noun named by a code", "the <noun> `<code>`", r"%s_Named" % K,
      "While the `a` file exists, when the person runs `work start`, `work` shall print the file."),
    c("codes-list", "codes joined by \"and\" before a plural noun", "the `<code>` and `<code>` <nouns>",
      r"CodeTwo|CodeMore|%s_NamedAnd" % K,
      "When the person runs `work start` with the `--source` and `--thread` options, `work` shall exit "
      "successfully."),
    c("option-set-to", "an option with its argument", "the `<option>` option set to <thing>", r"%s_SetTo" % K,
      "When the person runs `work start` with the `--every` option set to `5`, `work` shall exit "
      "successfully."),
    # relations
    c("of-relation", "a noun of another by a relation row", "<noun> of|in <np>", r"r\d+_\w+_Mod",
      "When a session ends a stage, `work` shall print the worktree of the session."),
    c("compound", "a noun before another, by a relation row \"of\"", "<noun2> <noun>", r"r\d+_\w+_Cpd",
      "When a session writes a file, `work` shall print the session worktree."),
    c("has-relation", "a state: the other noun of a relation row \"of\"", "<np> has <np>", r"r\d+_\w+_Has",
      "While a session has a worktree, when the person runs `work start`, `work` shall print the worktree."),
    c("holds-relation", "a state: the other noun of a relation row \"in\"", "<np> holds <np>", r"r\d+_\w+_Holds",
      "While a worktree holds a file, when a session writes the file, `work` shall print the worktree."),
    # attributes
    c("attribute-of", "a thing's attribute", "the <attribute> of <np>; the <noun> <attribute>",
      r"%s_(?:Of_k_\w+|Cpd_k_\w+|Up)" % T,
      "When a session ends a stage, `work` shall print the status of the stage."),
    c("attribute-is", "an attribute's value, the full form, which any value takes", "the <attribute> of <np> is <value>",
      r"%s_IsOf" % T,
      "While the status of a stage is `open`, when a session ends the stage, `work` shall print the stage."),
    c("adjective-value", "an attribute's value in the short form, of a value its entry declares an adjective (`Values "
      "(adjective):`); a value declared a noun (`Values (noun):`) is refused in it, naming the full form (b257)",
      "<np> is <value>", r"%s_k_\w+_Is" % T,
      "While a stage is `open`, when a session ends the stage, `work` shall print the stage."),
    c("attribute-code", "an attribute's value given as a code no entry lists, a noun when the attribute declares its "
      "values' kinds", "the <attribute> of <np> is `<code>`",
      r"%s(?:_k_\w+)?_IsCode(?:Of)?" % T,
      "While the version of a file is `1.0.1`, when the person runs `work start`, `work` shall print the "
      "file."),
    c("set-attribute", "a doer gives an attribute a value", "set the <attribute> of <np> to <value>", r"%s_Set" % T,
      "When a session ends a stage, `work` shall set the status of the stage to `done`."),
    c("value-set", "one of a list of values, or none of them",
      "the <attribute> of <np> is one of <value> or <value>; is not <value> or <value> (after <np> alone, adjectives only)",
      r"%s(?:_k_\w+)?_Is(?:One|None)Of|%s_Vals(?:\d+|More)" % (T, T),
      "While the priority of a stage is one of `low` or `high`, when the person runs `work start`, `work` "
      "shall end the stage."),
    c("has-no-value", "an attribute with no value", "<np> has no <attribute>", r"%s_k_\w+_HasNo" % T,
      "While a stage has no priority, when the person runs `work start`, `work` shall print the stage."),
    c("ordered", "an ordered attribute's value compared", "the <attribute> of <np> is after|before <value>",
      r"%s_(?:Cmp|Between|PtCode|PtVal)|After|Before" % T,
      "While the priority of a stage is after `low`, when the person runs `work start`, `work` shall end "
      "the stage.", r"%s_(?:Cmp|Between)" % T),
    c("number-of", "a count as a value", "the number of <nouns> is at least <number>",
      r"Count_(?:Cmp|Code|Up|Op\w+)|%s_NumberOf" % K,
      "When a session ends a stage, `work` shall print the number of lines of the stage."),
    c("exists", "a thing there is", "<np> exists; no <noun> exists", "Exists_St",
      "While files exist, when the person runs `work start`, `work` shall exit successfully."),
    # time
    c("moment-compare", "a moment before or after another", "<moment> is after|before <moment>", "k_moment_Cmp",
      "While the deadline of a stage is after `2026-01-01`, when a session ends the stage, `work` shall "
      "print the stage."),
    c("within", "a moment within the last span", "<moment> is within the last <amount> <unit>",
      r"k_moment_Within|u_\w+_Span|AmountInt|A_\w+",
      "While a deadline of a stage is within the last 7 days, when the person runs `work start`, `work` "
      "shall print the stage.", "k_moment_Within"),
]
