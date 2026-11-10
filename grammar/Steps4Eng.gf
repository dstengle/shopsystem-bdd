-- English of the step grammar 4: a step is in the present tense; `inst` and `intro` are the opers the generated
-- ContextStepsEng names an instance and brings one in with.
concrete Steps4Eng of Steps4 = BaseEng ** open SyntaxEng, (R = ResEng), Prelude in {
  lincat
    Step, Name = {s : Str} ;
  oper
    -- "the stage s1": an instance of a kind, named after its noun
    inst : N -> Str -> NP = \n, x -> actor ("the" ++ n.s ! R.Sg ! R.Nom ++ x) ;
    -- "a stage s1": a Given that brings one in
    intro : N -> Str -> {s : Str} = \n, x -> {s = (mkUtt (mkNP a_Det (mkCN n))).s ++ x} ;
  lin
    NameLit s = s ;
    SCond c = {s = c.s} ;
    STrig t = {s = t.s} ;
}
