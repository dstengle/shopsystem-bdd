-- English of the requirement grammar. A sentence's first word is lower case here: spec_grammar.tokenise lowers it
-- and spec_grammar.linearise raises it again.
concrete ReqEng of Req = TypedEng ** {
  lin
    Ubiq r = r ++ "." ;
    When t r = "when" ++ t ++ "," ++ r ++ "." ;
    While c r = "while" ++ c ++ "," ++ r ++ "." ;
    Where f r = "where" ++ f ++ "," ++ r ++ "." ;
    IfThen t r = "if" ++ t ++ "," ++ "then" ++ r ++ "." ;
    WhileWhen c t r = "while" ++ c ++ "," ++ "when" ++ t ++ "," ++ r ++ "." ;
    WhereWhen f t r = "where" ++ f ++ "," ++ "when" ++ t ++ "," ++ r ++ "." ;
    WhereWhile f c r = "where" ++ f ++ "," ++ "while" ++ c ++ "," ++ r ++ "." ;
    WhileIf c t r = "while" ++ c ++ "," ++ "if" ++ t ++ "," ++ "then" ++ r ++ "." ;
    WhereIf f t r = "where" ++ f ++ "," ++ "if" ++ t ++ "," ++ "then" ++ r ++ "." ;
    Shall s v = s ++ "shall" ++ v ;
    ShallNot s v = s ++ "shall" ++ "not" ++ v ;
    ActorSubj a = a ;
    NPSubj x = x.s ;
    Runs s c = s ++ "runs" ++ c ;
    RunsOn s c x = s ++ "runs" ++ c ++ "on" ++ x.s ;
    IsRun c = c ++ "is" ++ "run" ;
    Happens s e x = s ++ e.s3 ++ x.s ;
    HappensI s e = s ++ e.s3 ;
    Undergoes x e = x.s ++ be x ++ e.part ;
    CondOne a = a ;
    CondAnd a c = a ++ "and" ++ c ;
    Holds x r = x.s ++ (case x.n of {Sg => "holds" ; Pl => "hold"}) ++ "the" ++ r.s ! Sg ;
    HoldsA x r = x.s ++ (case x.n of {Sg => "holds" ; Pl => "hold"}) ++ art ++ r.s ! Sg ;
    IsFree r = "the" ++ r.s ! Sg ++ "is" ++ "free" ;
    FeatGiven c = c ++ "is" ++ "given" ;
    FeatAtom a = a ;
    Do e x = e.inf ++ x.s ;
    DoTo e x y = e.inf ++ x.s ++ y.s ;
    Print l = "print" ++ l.s ;
    ExitOk = "exit" ++ "successfully" ;
    ExitErr x = "exit" ++ "with" ++ "an" ++ "error" ++ "naming" ++ x.s ;
    RefuseErr x = "exit" ++ "with" ++ "an" ++ "error" ++ "naming" ++ x.s ++ "and" ++ "change" ++ "nothing" ;
    CommitPush x = "commit" ++ x.s ++ "and" ++ "push" ++ "the" ++ "commit" ;
    ChangeNothing = "change" ++ "nothing" ;
    Hold r = "hold" ++ "the" ++ r.s ! Sg ;
    HoldA r = "hold" ++ art ++ r.s ! Sg ;
    HoldAtMost c r = "hold" ++ "at" ++ "most" ++ c ++ r.s ! Pl ++ "at" ++ "a" ++ "time" ;
    CodeNP c = np c ;
    QuotedNP q = np q ;
    Only x = {s = "only" ++ x.s ; p = Full ; n = x.n} ;
    OneNP x = {s = x.s ; m = One} ;
    MoreNP x l = {s = x.s ++ (case l.m of {One => "and" ; More => ","}) ++ l.s ; m = More} ;
    CodeLit s = s.s ;
    CmdCode c = c ;
    CmdActor a = a ;
    QuotedLit s = s.s ;
    CountNum i = i.s ;
    CountCode c = c ;
}
