-- The step grammar of the controlled language 4 (the CNL 4 design, section 9; I14a): one Gherkin step over the base
-- grammar, its keyword not part of it. A Given or a Then of a state is a condition of Base (`SCond`), a When its
-- trigger (`STrig`); an instance is named after its noun ("the stage s1"), a Given brings one in ("a stage s1"),
-- and a Then of an act says it in the present ("`work` exits with an error naming `work start`"); example data is a
-- named instance that holds a block ("the feature file `a.feature` holds:") or one value, a code or a quoted string
-- (`Quoted`: "the tracked file `v` holds "3.0.0""). The funs typed by a
-- kind or a frame are generated per context over Context by scripts/spec_rgl_steps.py, as the module ContextSteps.
abstract Steps4 = Base ** {
  cat Step ; Name ; Quoted ;
  fun
    NameLit : String -> Name ;    -- s1
    QuotedLit : String -> Quoted ; -- "3.0.0" or `3.0.0`
    SCond : Cond -> Step ;        -- the stage s1 is `done`
    STrig : Trig -> Step ;        -- the person runs `work start`
}
