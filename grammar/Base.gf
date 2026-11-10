-- The base grammar of the controlled language 4 (the CNL 4 design, call 1; I7a): the hand-written core of a line,
-- tied to no kind and no pack. A line is its preconditions (While, Where), a trigger (When, If) or none, and its
-- responses; conditions and responses are coordinated; a polarity is one argument (PPos, PNeg); determiners are one
-- category. Everything typed by a kind, an actor, an attribute or a verb's frame is generated over it, per context,
-- by scripts/spec_rgl.py as the module Context, which extends Base; the English is the RGL's (BaseEng). Modality
-- (I17): "shall" and "may" are a response's (a doer's `Shall`, `May`); "always" and "never" a line of no trigger
-- over one clause (`Necessary`, its clause a subject's `Nec`).
abstract Base = {
  flags startcat = Req ;
  cat Req ; Pre ; Cond ; Conds ; Trig ; Resp ; Resps ; Pol ; Det ; Code ; Mod ; Nec ;
  fun
    Ubiq : Pre -> Resps -> Req ;               -- R.
    When : Pre -> Trig -> Resps -> Req ;       -- When T, R.
    If : Pre -> Trig -> Resps -> Req ;         -- If T, then R.
    Necessary : Pre -> Nec -> Req ;           -- A session always follows a stage.
    NoPre : Pre ;
    While : Conds -> Pre ;                     -- While C, ...
    Where : Conds -> Pre ;                     -- Where F, ...
    WhereWhile : Conds -> Conds -> Pre ;       -- Where F, while C, ...
    OneCond : Cond -> Conds ;
    AndCond : Cond -> Conds -> Conds ;         -- A and B
    OrCond : Cond -> Conds -> Conds ;          -- A or B
    OneResp : Resp -> Resps ;
    AndResp : Resp -> Resps -> Resps ;         -- R1, and R2
    PPos, PNeg : Pol ;
    MAlways, MNever : Mod ;                    -- always, never
    DetA, DetThe, DetEvery, DetPl, DetThePl, DetNo : Det ;   -- a, the, every, (bare plural), the (plural), no
    CodeLit : String -> Code ;                 -- `spec/index.md`
}
