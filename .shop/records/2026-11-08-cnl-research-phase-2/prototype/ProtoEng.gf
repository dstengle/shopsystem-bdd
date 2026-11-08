concrete ProtoEng of Proto = LexEng ** open SyntaxEng, ParadigmsEng, (E = ExtraEng), (R = ResEng), ParamX, Prelude in {
  lincat Req, Resp = {s : Str} ; Cond = S ; Resps, ActList = {s : Str ; m : Bool} ; ActItem = {s : Str} ;
    Cmd, Code, Quoted = {s : Str} ;
  oper
    utt : NP -> Str = \x -> (mkUtt x).s ;
    raw : Str -> NP = \s -> lin NP {s = \\_ => s ; a = R.agrP3 R.Sg} ;
    comma : Bool -> Str = \m -> case m of {False => "and" ; True => ","} ;
  lin
    Ubiq r = {s = r.s ++ "."} ;
    When t r = {s = "when" ++ t.s ++ "," ++ r.s ++ "."} ;
    IfThen t r = {s = "if" ++ t.s ++ "," ++ "then" ++ r.s ++ "."} ;
    While c r = {s = "while" ++ c.s ++ "," ++ r.s ++ "."} ;
    WhileWhen c t r = {s = "while" ++ c.s ++ "," ++ "when" ++ t.s ++ "," ++ r.s ++ "."} ;
    WhileIf c t r = {s = "while" ++ c.s ++ "," ++ "if" ++ t.s ++ "," ++ "then" ++ r.s ++ "."} ;
    PPos = positivePol ; PNeg = E.UncNeg ;
    CondP p a = mkS p a ;
    CondAnd a b = mkS and_Conj a b ;
    Runs x c = mkS (mkCl x (mkV2 (mkV "run" "runs" "ran" "run" "running")) (raw c.s)) ;
    RunsOn x c o = mkS (mkCl x (mkVP (mkVP (mkV2 (mkV "run" "runs" "ran" "run" "running")) (raw c.s)) (SyntaxEng.mkAdv on_Prep o))) ;
    RunsWith x c o = mkS (mkCl x (mkVP (mkVP (mkV2 (mkV "run" "runs" "ran" "run" "running")) (raw c.s)) (SyntaxEng.mkAdv with_Prep o))) ;
    Shall x l = {s = utt x ++ "shall" ++ l.s} ;
    OneResp r = {s = r.s ; m = False} ;
    AndResp r l = {s = r.s ++ "," ++ "and" ++ l.s ; m = True} ;
    ActP p v = {s = p.s ++ R.infVP R.VVAux v False Simul p.p (R.agrP3 R.Sg)} ;
    OneAct a = {s = a.s ; m = False} ;
    AndAct a l = {s = a.s ++ comma l.m ++ l.s ; m = True} ;
    ExitOk = mkVP (mkVP (mkV "exit")) (ParadigmsEng.mkAdv "successfully") ;
    ExitErr x = mkVP (mkVP (mkV "exit")) (ParadigmsEng.mkAdv ("with an error naming" ++ utt x)) ;
    Nothing = nothing_NP ;
    CodeNP c = raw c.s ;
    QuotedNP q = raw q.s ;
    CmdCode c = c ;
    CmdActor a = {s = utt a} ;
    CodeLit s = s ;
    QuotedLit s = s ;
}
