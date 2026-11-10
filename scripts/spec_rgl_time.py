"""The time constructs of grammar 4 (the CNL 4 design, section 4.4, call 9; I16), generated into the module `Context`
over the base grammar's time words (`grammar/Time.gf`): what they say of a context's kinds and verbs, and the
refusal of a number where a duration is due with no unit after it.

The perfect of an action verb is a state, the history of that action (call 3): for each subject kind S of an action
frame, `S_Done : Pol -> S_Arg -> S_V -> Cond`, "a session has ended a stage", "sessions have not written a file".
Every kind K has "the newest K" and "the oldest K" (`K_Sup : Sup -> K_CN -> K_NP0`). With the time pack imported
(the kind `moment`): each unit U, a kind of `unit`, gives a duration said, `u_<U>_Span : Amount -> Span`, "7 days";
a moment is compared, `k_moment_Cmp : Pol -> k_moment_NP -> Order -> k_moment_Arg -> Cond`, "a deadline of a stage
is after `2026-01-01`", or put within the last span before now, `k_moment_Within : Pol -> k_moment_NP -> Span ->
Cond`; and a history is since a moment, `S_DoneSince : Pol -> S_Arg -> S_V -> k_moment_Arg -> Cond`.
"""
import spec_rgl

MOMENT, UNIT = "moment", "unit"
NUMBERS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve")
PERFECT = "mkS presentTense anteriorAnt p (mkCl x %s)"


def units(vocab):
    """The units of the time pack and of the context: the kinds under `unit`, `unit` itself left out."""
    return [k for k in vocab.kinds if k != UNIT and UNIT in vocab.ancestors(k)]


def actions(vocab):
    """The subject kinds of the action frames, in order."""
    return list(dict.fromkeys(s for v in vocab.verbs if v.aspect == "action" for s, _ in v.frames))


def constructs(w, vocab):
    """Every time construct of `vocab` written to `w` (a spec_rgl.Writer)."""
    for k in vocab.kinds:
        K = spec_rgl.kid(k)
        w.fun(K + "_Sup", "Sup -> %s_CN -> %s_NP0" % (K, K), "sup s cn", "s cn")
    timed = MOMENT in vocab.kinds
    M = spec_rgl.kid(MOMENT)
    for s in actions(vocab):
        S = spec_rgl.kid(s)
        w.fun(S + "_Done", "Pol -> %s_Arg -> %s_V -> Cond" % (S, S), PERFECT % "v", "p x v")
        if timed:
            w.fun(S + "_DoneSince", "Pol -> %s_Arg -> %s_V -> %s_Arg -> Cond" % (S, S, M),
                  PERFECT % '(mkVP v (SyntaxEng.mkAdv (mkPrep "since") m))', "p x v m")
    if not timed:
        return
    for u in units(vocab):
        w.fun("u_%s_Span" % spec_rgl.slug(u), "Amount -> Span", "dur a (%s)" % spec_rgl.noun(*vocab.nouns[u]), "a")
    w.fun(M + "_Cmp", "Pol -> %s_NP -> Order -> %s_Arg -> Cond" % (M, M),
          "mkS p (mkCl x (mkVP (SyntaxEng.mkAdv (mkPrep o.s) y)))", "p x o y")
    w.fun(M + "_Within", "Pol -> %s_NP -> Span -> Cond" % M,
          "mkS p (mkCl x (mkVP (SyntaxEng.mkAdv (mkPrep %s) d)))" % spec_rgl.s("within the last"), "p x d")


def unitless(vocab, tokens, at):
    """The refusal of a number where a duration is due with no unit after it (grammar 4 stopped at token `at`, after
    "within the last" and a number), or None."""
    if at is None or at < 4 or MOMENT not in vocab.kinds or [t.lower() for t in tokens[at - 4:at - 1]] != [
            "within", "the", "last"]:
        return None
    number = tokens[at - 1]
    if not (number.isdigit() or number.lower() in NUMBERS):
        return None
    return ("refused: the number %s is a duration and takes a unit of the time pack after it: %s"
            % (number, ", ".join(units(vocab))))
