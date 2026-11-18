-- a toy logical form and a toy scenario, with a transfer by def rules
abstract Lf = {
  flags startcat = Scenario ;
  cat Ref ; Atom ; Atoms ; Step ; Steps ; Scenario ; Nat ;
  data
    Z : Nat ; S : Nat -> Nat ;
    Stage, File : Nat -> Ref ;            -- referent of a kind, numbered
    Done : Ref -> Atom ;                  -- status(x) = done
    Writes : Ref -> Atom ;                -- work writes x
    Runs : Atom ;                         -- the person runs `work start`
    Nil : Atoms ; Cons : Atom -> Atoms -> Atoms ;
    Rule : Atoms -> Atom -> Atoms -> Scenario ;   -- while ; when ; response  (the LF)
    -- the scenario side
    GivenA : Ref -> Step ; GivenC : Atom -> Step ; When : Atom -> Step ; Then : Atom -> Step ;
    SNil : Steps ; SCons : Step -> Steps -> Steps ;
    Scen : Steps -> Scenario ;
  fun
    -- transfer
    toScen : Scenario -> Scenario ;
    givens : Atoms -> Steps ; thens : Atoms -> Steps -> Steps ; app : Steps -> Steps -> Steps ;
  def
    toScen (Rule w t r) = Scen (app (givens w) (SCons (When t) (thens r SNil))) ;
    givens Nil = SNil ;
    givens (Cons (Done x) as) = SCons (GivenA x) (SCons (GivenC (Done x)) (givens as)) ;
    thens Nil k = k ;
    thens (Cons a as) k = SCons (Then a) (thens as k) ;
    app SNil ys = ys ;
    app (SCons x xs) ys = SCons x (app xs ys) ;
}
