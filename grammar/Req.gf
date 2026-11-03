-- The requirement grammar: one EARS statement, one `shall`. Words and typed slots come from the generated Lex and
-- Typed modules (a context's glossary); this module holds the forms and the slots tied to no kind. A core fun is
-- added only for a construct that recurs in at least two capabilities (design §9.5), with a corpus line.
abstract Req = Typed ** {
  flags startcat = Req ;
  fun
    -- the six EARS forms, clauses in a fixed order
    Ubiq : Resp -> Req ;                         -- R.
    When : Trig -> Resp -> Req ;                 -- When T, R.
    While : Cond -> Resp -> Req ;                -- While C, R.
    Where : Feat -> Resp -> Req ;                -- Where F, R.
    IfThen : Trig -> Resp -> Req ;               -- If T, then R.
    WhileWhen : Cond -> Trig -> Resp -> Req ;    -- While C, when T, R.
    WhereWhen : Feat -> Trig -> Resp -> Req ;    -- Where F, when T, R.
    WhereWhile : Feat -> Cond -> Resp -> Req ;   -- Where F, while C, R.
    WhileIf : Cond -> Trig -> Resp -> Req ;      -- While C, if T, then R.
    WhereIf : Feat -> Trig -> Resp -> Req ;      -- Where F, if T, then R.
    Shall, ShallNot : Subj -> VP -> Resp ;
    ActorSubj : Actor -> Subj ;
    NPSubj : NP -> Subj ;
    -- triggers and conditions tied to no kind
    Runs : Subj -> Cmd -> Trig ;                 -- the person runs `work start`
    RunsOn : Subj -> Cmd -> NP -> Trig ;         -- the person runs `work start` on an initiative that is ...
    IsRun : Cmd -> Trig ;                        -- `tools size` is run
    Happens : Subj -> Event -> NP -> Trig ;      -- a session ends a stage
    HappensI : Subj -> Event -> Trig ;           -- research ends
    Undergoes : NP -> Event -> Trig ;            -- a command is refused
    CondOne : Atom -> Cond ;
    CondAnd : Atom -> Cond -> Cond ;             -- A and B
    Holds : NP -> Resource -> Atom ;             -- a session holds the spec lock
    HoldsA : NP -> Resource -> Atom ;            -- a stage holds a worker slot
    IsFree : Resource -> Atom ;                  -- the spec lock is free
    FeatGiven : Code -> Feat ;                   -- `--json` is given
    FeatAtom : Atom -> Feat ;
    -- verb phrases tied to no kind
    Do : Event -> NP -> VP ;                     -- start the stage
    DoTo : Event -> NP -> NP -> VP ;             -- give the stage only a brief
    Print : NPs -> VP ;                          -- print X, Y and Z
    ExitOk : VP ;                                -- exit successfully
    ExitErr : NP -> VP ;                         -- exit with an error naming X
    RefuseErr : NP -> VP ;                       -- exit with an error naming X and change nothing
    CommitPush : NP -> VP ;                      -- commit X and push the commit
    ChangeNothing : VP ;                         -- change nothing
    Hold : Resource -> VP ;                      -- hold the spec lock
    HoldA : Resource -> VP ;                     -- hold a worker slot
    HoldAtMost : Count -> Resource -> VP ;       -- hold at most `workers` worker slots at a time
    -- noun phrases tied to no kind
    CodeNP : Code -> NP ;
    QuotedNP : Quoted -> NP ;
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
