-- English of the step grammar. A step is in the present tense; its keyword (Given, When, Then) is not part of it.
concrete StepsEng of Steps = ReqEng ** {
  lincat Step, Name = Str ;
  lin
    NameLit s = s.s ;
    SAtom a = a ;
    SFeat f = f ;
    STrig t = t ;
    SPrints s l = s ++ "prints" ++ l.s ;
    SPrintsNot s l = s ++ "does" ++ "not" ++ "print" ++ l.s ;
    SExitsOk s = s ++ "exits" ++ "successfully" ;
    SExitsErr s x = s ++ "exits" ++ "with" ++ "an" ++ "error" ++ "naming" ++ x.s ;
    SChangesNothing s = s ++ "changes" ++ "nothing" ;
}
