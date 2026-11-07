-- The categories every requirement and step grammar shares. The generated Lex and Typed modules extend this one,
-- and Req (and Steps) extend Typed, so a typed slot can fill a core slot.
abstract Core = {
  cat
    Req ; Feat ; Cond ; Atom ; Trig ; Resp ; Subj ; VP ; NP ; NPs ; Code ; Cmd ; Quoted ; Count ;
    Actor ; Resource ;
}
