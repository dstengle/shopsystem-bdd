-- The base grammar of the controlled language 4 (the CNL 4 design, call 1; I7a): the hand-written core of a line,
-- tied to no kind and no pack. A line is its preconditions (While, Where), a trigger (When, If) or none, and its
-- responses; conditions and responses are coordinated; a polarity is one argument (PPos, PNeg); determiners are one
-- category. Everything typed by a kind, an actor, an attribute or a verb's frame is generated over it, per context,
-- by scripts/spec_rgl.py as the module Context, which extends Base; the English is the RGL's (BaseEng).
abstract Base = {
  flags startcat = Req ;
  cat Req ; Pre ; Cond ; Conds ; Trig ; Resp ; Resps ; Pol ; Det ; Code ; Bound ; Many ;
  fun
    Ubiq : Pre -> Resps -> Req ;               -- R.
    When : Pre -> Trig -> Resps -> Req ;       -- When T, R.
    If : Pre -> Trig -> Resps -> Req ;         -- If T, then R.
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
    DetA, DetThe, DetEvery, DetPl, DetThePl, DetNo : Det ;   -- a, the, every, (bare plural), the (plural), no
    CodeLit : String -> Code ;                 -- `spec/index.md`
    -- counts (call 4; I15): "at least two", "exactly one" ... before a noun; "one" alone is exactly one
    DetCount : Bound -> Many -> Det ;
    DetOne : Det ;
    AtLeast, AtMost, Exactly, MoreThan, FewerThan : Bound ;
    Many1, Many2, Many3, Many4, Many5, Many6, Many7, Many8, Many9, Many10 : Many ;
}
