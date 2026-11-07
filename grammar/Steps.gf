-- The step grammar (design §14.1): one Gherkin step, the linearisation of one step function. It extends Req, so a
-- step speaks the requirement grammar's atoms, triggers and noun phrases. The generated StepsTyped module (written
-- by scripts/features_vocab.py from the lexicon) adds, for each kind, the instance mention ("the initiative i1")
-- and the Given templates. Every instance is named with its kind word. The same text can be a Given and a Then
-- (an atom), or a When and a Then (an event): the step's keyword decides which template it is.
abstract Steps = Req ** {
  flags startcat = Step ;
  cat Step ; Name ;
  fun
    NameLit : String -> Name ;                     -- i1, or a code `spec/index.md`
    SAtom : Atom -> Step ;                         -- the initiative i1 is `started` / the session s1 holds the spec lock
    SFeat : Feat -> Step ;                         -- `--json` is given
    STrig : Trig -> Step ;                         -- the person runs `work start` on the initiative i1
    SDoes : Subj -> Event -> NP -> Step ;          -- `work run` takes the initiative i1
    SDoesNot : Subj -> Event -> NP -> Step ;       -- `work run` does not take the initiative i3
    SDoesTo : Subj -> Event -> NP -> NP -> Step ;  -- `work run` gives only a brief to the stage s1
    SDoesI : Subj -> Event -> Step ;               -- `work` stops
    SDoesINot : Subj -> Event -> Step ;            -- `work` does not stop
    SPrints : Subj -> NPs -> Step ;                -- `work` prints the work-item w1
    SPrintsNot : Subj -> NPs -> Step ;             -- `work` does not print the work-item w2
    SExitsOk : Subj -> Step ;                      -- `work` exits successfully
    SExitsErr : Subj -> NP -> Step ;               -- `work` exits with an error naming the reason
    SChangesNothing : Subj -> Step ;               -- `work` changes nothing
}
