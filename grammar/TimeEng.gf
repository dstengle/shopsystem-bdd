-- The English of the base grammar's time words: an amount carries its number, so its unit agrees ("one day",
-- "7 days"); `dur` is the noun phrase of an amount and a unit, `cmp` "x is after y".
concrete TimeEng of Time = BaseEng ** open SyntaxEng, ParadigmsEng, (R = ResEng), ParamX, Prelude in {
  lincat
    Amount = {s : Str ; n : ParamX.Number} ;
    Order = {s : Str} ;
    Span = NP ;
  oper
    amount : Str -> ParamX.Number -> {s : Str ; n : ParamX.Number} = \s, n -> {s = s ; n = n} ;
    dur : {s : Str ; n : ParamX.Number} -> N -> NP = \a, u -> lin NP {s = \\_ => a.s ++ u.s ! a.n ! R.Nom ;
      a = R.agrP3 a.n} ;
  lin
    AmountInt i = amount i.s Pl ;
    A_one = amount "one" Sg ;
    A_two = amount "two" Pl ;
    A_three = amount "three" Pl ;
    A_four = amount "four" Pl ;
    A_five = amount "five" Pl ;
    A_six = amount "six" Pl ;
    A_seven = amount "seven" Pl ;
    A_eight = amount "eight" Pl ;
    A_nine = amount "nine" Pl ;
    A_ten = amount "ten" Pl ;
    A_eleven = amount "eleven" Pl ;
    A_twelve = amount "twelve" Pl ;
    After = {s = "after"} ;
    Before = {s = "before"} ;
}
