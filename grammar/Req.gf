-- The requirement grammar: one EARS statement, its responses and verb phrases joined by `and` (design-r2 §4.1).
-- Words and typed slots come from the generated Lex and Typed modules (a context's glossary); this module holds the
-- forms and the slots tied to no kind. A core fun is added only for a construct that recurs in at least two
-- capabilities (design §9.5), with a corpus line.
abstract Req = Typed ** {
  flags startcat = Req ;
  cat VPs ; VPor ; Resps ;
  fun
    -- the six EARS forms, clauses in a fixed order
    Ubiq : Resps -> Req ;                         -- R.
    When : Trig -> Resps -> Req ;                 -- When T, R.
    While : Cond -> Resps -> Req ;                -- While C, R.
    Where : Feat -> Resps -> Req ;                -- Where F, R.
    IfThen : Trig -> Resps -> Req ;               -- If T, then R.
    WhileWhen : Cond -> Trig -> Resps -> Req ;    -- While C, when T, R.
    WhereWhen : Feat -> Trig -> Resps -> Req ;    -- Where F, when T, R.
    WhereWhile : Feat -> Cond -> Resps -> Req ;   -- Where F, while C, R.
    WhileIf : Cond -> Trig -> Resps -> Req ;      -- While C, if T, then R.
    WhereIf : Feat -> Trig -> Resps -> Req ;      -- Where F, if T, then R.
    Shall : Subj -> VPs -> Resp ;               -- `work run` shall A, B and C
    ShallNot : Subj -> VPor -> Resp ;           -- `work run` shall not A or B (neither)
    OneVP : VP -> VPs ;
    AndVP : VP -> VPs -> VPs ;                   -- A and B / A, B and C
    OneVPor : VP -> VPor ;
    OrVP : VP -> VPor -> VPor ;                  -- A or B
    OneResp : Resp -> Resps ;
    AndResp : Resp -> Resps -> Resps ;           -- R1, and R2: responses whose subjects differ
    ActorSubj : Actor -> Subj ;
    NPSubj : NP -> Subj ;
    -- triggers and conditions tied to no kind
    Runs : Subj -> Cmd -> Trig ;                 -- the person runs `work start`
    RunsOn : Subj -> Cmd -> NP -> Trig ;         -- the person runs `work start` on an initiative that is ...
    IsRun : Cmd -> Trig ;                        -- `tools size` is run
    -- a verb's trigger, "a session writes a file", is a fun of its frame (spec_typed_verbs: e_write__Happens), and
    -- with a recipient after "to", "a session gives a brief to a stage", e_give__HappensTo
    CondOne : Atom -> Cond ;
    CondAnd : Atom -> Cond -> Cond ;             -- A and B
    CondOr : Atom -> Cond -> Cond ;              -- A or B
    Holds : NP -> Resource -> Atom ;             -- a session holds the spec lock
    HoldsA : NP -> Resource -> Atom ;            -- a stage holds a worker slot
    IsFree : Resource -> Atom ;                  -- the spec lock is free
    FeatGiven : Code -> Feat ;                   -- `--json` is given
    FeatAtom : Atom -> Feat ;
    -- verb phrases tied to no kind
    -- a verb's phrase, "write a file", is a fun of its frame (spec_typed_verbs: e_write__Do, __DoI, __DoTo)
    Print : NPs -> VP ;                          -- print X, Y and Z
    ExitOk : VP ;                                -- exit successfully
    ExitErr : NP -> VP ;                         -- exit with an error naming X
    ChangeNothing : VP ;                         -- change nothing
    Hold : Resource -> VP ;                      -- hold the spec lock
    HoldA : Resource -> VP ;                     -- hold a worker slot
    HoldAtMost : Count -> Resource -> VP ;       -- hold at most `workers` worker slots at a time
    -- noun phrases tied to no kind
    CodeNP : Code -> NP ;
    QuotedNP : Quoted -> NP ;
    QuotedFor : Quoted -> NP -> NP ;             -- "turns" for the logged stage: a figure given for one thing
    Only : NP -> NP ;                            -- only a brief
    OneNP : NP -> NPs ;
    MoreNP : NP -> NPs -> NPs ;
    CodeLit : String -> Code ;
    CmdCode : Code -> Cmd ;
    CmdActor : Actor -> Cmd ;                    -- runs `work run`: an actor named as the command it is
    QuotedLit : String -> Quoted ;
    CountNum : Int -> Count ;
    CountCode : Code -> Count ;
}
