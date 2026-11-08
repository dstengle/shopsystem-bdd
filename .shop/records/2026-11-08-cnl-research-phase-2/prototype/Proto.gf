-- The hand-written core of the prototype: EARS forms, conditions with polarity, triggers tied to no kind,
-- responses as polarised verb phrases coordinated under one "shall", and literals. Everything typed comes from Lex.
abstract Proto = Lex ** {
  flags startcat = Req ;
  cat Req ; Cond ; Resp ; Resps ; ActItem ; ActList ; Cmd ; Code ; Quoted ;
  fun
    Ubiq : Resps -> Req ;                       -- R.
    When : Trig -> Resps -> Req ;               -- When T, R.
    IfThen : Trig -> Resps -> Req ;             -- If T, then R.
    While : Cond -> Resps -> Req ;              -- While C, R.
    WhileWhen : Cond -> Trig -> Resps -> Req ;  -- While C, when T, R.
    WhileIf : Cond -> Trig -> Resps -> Req ;    -- While C, if T, then R.
    PPos, PNeg : Pol ;
    CondP : Pol -> Atom -> Cond ;               -- a request is (not) `accepted`
    CondAnd : Cond -> Cond -> Cond ;            -- A and B
    Runs : agent_NP -> Cmd -> Trig ;            -- the person runs `work idea`
    RunsOn : agent_NP -> Cmd -> thing_NP -> Trig ;    -- ... on the request
    RunsWith : agent_NP -> Cmd -> thing_NP -> Trig ;  -- ... with no origin option
    Shall : agent_NP -> ActList -> Resp ;       -- `work` shall A, B and not C
    OneResp : Resp -> Resps ;
    AndResp : Resp -> Resps -> Resps ;          -- R1, and R2
    ActP : Pol -> agent_Act -> ActItem ;        -- (not) print the comment
    OneAct : ActItem -> ActList ;
    AndAct : ActItem -> ActList -> ActList ;    -- A and B / A, B and C
    ExitOk : agent_Act ;                        -- exit successfully
    ExitErr : thing_NP -> agent_Act ;           -- exit with an error naming X
    Nothing : thing_NP0 ;                       -- (change) nothing
    CodeNP : Code -> thing_NP0 ;                -- `spec/index.md`
    QuotedNP : Quoted -> text_NP0 ;             -- "wall time"
    CmdCode : Code -> Cmd ;                     -- `work sync`
    CmdActor : tool_NP0 -> Cmd ;                -- `trial-runner` (an actor named as the command it is)
    CodeLit : String -> Code ;
    QuotedLit : String -> Quoted ;
}
