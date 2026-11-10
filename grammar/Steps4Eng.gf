-- English of the step grammar 4: a step is in the present tense; `inst` and `intro` are the opers the generated
-- ContextStepsEng names an instance and brings one in with, `holds` the one it gives an instance its example data with.
concrete Steps4Eng of Steps4 = BaseEng ** open SyntaxEng, (R = ResEng), Prelude in {
  lincat
    Step, Name, Quoted = {s : Str} ;
  oper
    -- "the stage s1": an instance of a kind, named after its noun
    inst : N -> Str -> NP = \n, x -> actor ("the" ++ n.s ! R.Sg ! R.Nom ++ x) ;
    -- "a stage s1": a Given that brings one in
    intro : N -> Str -> {s : Str} = \n, x -> {s = (mkUtt (mkNP a_Det (mkCN n))).s ++ x} ;
    -- "the feature file f1 holds": example data, its block after ":" or its one value after it
    holds : N -> Str -> Str -> {s : Str} = \n, x, v -> {s = "the" ++ n.s ! R.Sg ! R.Nom ++ x ++ "holds" ++ v} ;
  lin
    NameLit s = s ;
    QuotedLit s = s ;
    SCond c = {s = c.s} ;
    STrig t = {s = t.s} ;
}
