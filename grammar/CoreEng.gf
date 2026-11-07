-- English of the shared categories, and the opers the generated TypedEng uses. There is no RGL: records carry
-- agreement only where English needs it (number of a noun phrase).
concrete CoreEng of Core = {
  param
    Number = Sg | Pl ;
    Pron = Full | It ;
    Many = One | More ;
  lincat
    Req, Feat, Cond, Atom, Trig, Resp, Subj, VP, Code, Cmd, Quoted, Count, Actor = Str ;
    NP = NPr ;
    NPs = {s : Str ; m : Many} ;
    Resource = {s : Number => Str} ;
  oper
    NPr : Type = {s : Str ; p : Pron ; n : Number} ;
    CN : Type = {s : Number => Str} ;
    Vs : Type = {s : Str ; m : Many} ;
    art : Str = pre { "a" ; "an" / strs { "a" ; "e" ; "i" ; "o" ; "u" ; "`a" ; "`e" ; "`i" ; "`o" ; "`u" } } ;
    mkCN : Str -> Str -> CN = \sg, pl -> {s = table {Sg => sg ; Pl => pl}} ;
    mkRes : Str -> Str -> {s : Number => Str} = \sg, pl -> {s = table {Sg => sg ; Pl => pl}} ;
    np : Str -> NPr = \s -> {s = s ; p = Full ; n = Sg} ;
    det : Str -> CN -> NPr = \d, cn -> np (d ++ cn.s ! Sg) ;
    detA : CN -> NPr = \cn -> np (art ++ cn.s ! Sg) ;
    plural : CN -> NPr = \cn -> {s = cn.s ! Pl ; p = Full ; n = Pl} ;
    itNP : NPr = {s = "it" ; p = It ; n = Sg} ;
    be : NPr -> Str = \x -> case x.n of {Sg => "is" ; Pl => "are"} ;
    post : CN -> (Number => Str) -> CN = \cn, rest -> {s = \\n => cn.s ! n ++ rest ! n} ;
    thatBe : Str -> (Number => Str) = \rest -> table {Sg => "that" ++ "is" ++ rest ; Pl => "that" ++ "are" ++ rest} ;
    whose : Str -> Str -> (Number => Str) = \attr, rest -> \\_ => "whose" ++ attr ++ "is" ++ rest ;
    same : Str -> (Number => Str) = \rest -> \\_ => rest ;
    verbal : Str -> Str -> NPr -> (Number => Str) = \s3, inf, o -> table {Sg => "that" ++ s3 ++ o.s ; Pl => "that" ++ inf ++ o.s} ;
    attrOf : Str -> NPr -> NPr = \attr, x -> np (case x.p of {It => "its" ++ attr ; Full => "the" ++ attr ++ "of" ++ x.s}) ;
    oneV : Str -> Vs = \v -> {s = v ; m = One} ;
    moreV : Str -> Vs -> Vs = \v, l -> {s = v ++ (case l.m of {One => "or" ; More => ","}) ++ l.s ; m = More} ;
}
