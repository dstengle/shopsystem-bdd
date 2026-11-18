concrete LfEng of Lf = {
  lincat Ref, Atom, Step, Nat = Str ; Atoms, Steps, Scenario = Str ;
  lin
    Z = "1" ; S n = n ++ "+1" ;
    Stage n = "the stage s" ++ n ; File n = "the file f" ++ n ;
    Done x = x ++ "is `done`" ; Writes x = "`work` writes" ++ x ; Runs = "the person runs `work start`" ;
    Nil = "" ; Cons a as = a ++ ";" ++ as ;
    Rule w t r = "while" ++ w ++ "when" ++ t ++ "then" ++ r ;
    GivenA x = "Given a" ++ x ; GivenC a = "Given" ++ a ; When a = "When" ++ a ; Then a = "Then" ++ a ;
    SNil = "" ; SCons x xs = x ++ "&+ \n" ++ xs ;
    Scen s = s ;
    toScen s = s ; givens a = a ; thens a k = a ++ k ; app a b = a ++ b ;
}
