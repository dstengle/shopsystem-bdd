-- The English of the base grammar, over GF's RGL: agreement, negation and "a"/"an" are the RGL's. Overridden
-- defaults (call 1): "does not" (ExtraEng's uncontracted negation), not "doesn't"; no comma after a While clause but
-- the one before what follows it. `actor`, `named`, `act` and `acts` are the opers the generated ContextEng uses.
concrete BaseEng of Base = open SyntaxEng, ParadigmsEng, (E = ExtraEng), (R = ResEng), ParamX, Prelude in {
  lincat
    Req, Pre, Resp, Code = {s : Str} ;
    Resps = {s : Str} ;
    Cond, Trig = S ;
    Conds = {s : Str} ;
    Pol = SyntaxEng.Pol ;
    Det = SyntaxEng.Det ;
  oper
    -- a noun phrase spelled as written: an actor's name, a code; singular
    actor : Str -> NP = \s -> lin NP {s = \\_ => s ; a = R.agrP3 R.Sg} ;
    -- a thing named by a code before its noun: "the `--json` option"
    named : Str -> CN -> NP = \c, cn -> actor ("the" ++ c ++ cn.s ! R.Sg ! R.Nom) ;
    -- a verb phrase after "shall", with its polarity: "write a file", "not write a file"
    act : SyntaxEng.Pol -> VP -> Str = \p, v -> p.s ++ R.infVP R.VVAux v False Simul p.p (R.agrP3 R.Sg) ;
    Acts : Type = {s : Str ; m : Bool} ;
    oneAct : Str -> Acts = \a -> {s = a ; m = False} ;
    andAct : Str -> Acts -> Acts = \a, l -> {s = a ++ (case l.m of {False => "and" ; True => ","}) ++ l.s ; m = True} ;
    shall : NP -> Acts -> {s : Str} = \x, l -> {s = (mkUtt x).s ++ "shall" ++ l.s} ;
  lin
    Ubiq p r = {s = p.s ++ r.s ++ "."} ;
    When p t r = {s = p.s ++ "when" ++ t.s ++ "," ++ r.s ++ "."} ;
    If p t r = {s = p.s ++ "if" ++ t.s ++ "," ++ "then" ++ r.s ++ "."} ;
    NoPre = {s = []} ;
    While c = {s = "while" ++ c.s ++ ","} ;
    Where c = {s = "where" ++ c.s ++ ","} ;
    WhereWhile f c = {s = "where" ++ f.s ++ "," ++ "while" ++ c.s ++ ","} ;
    OneCond c = {s = c.s} ;
    AndCond c l = {s = c.s ++ "and" ++ l.s} ;
    OrCond c l = {s = c.s ++ "or" ++ l.s} ;
    OneResp r = r ;
    AndResp r l = {s = r.s ++ "," ++ "and" ++ l.s} ;
    PPos = positivePol ;
    PNeg = E.UncNeg ;
    DetA = a_Det ;
    DetThe = the_Det ;
    DetEvery = every_Det ;
    DetPl = aPl_Det ;
    DetThePl = thePl_Det ;
    DetNo = mkDet no_Quant ;
    CodeLit s = s ;
}
