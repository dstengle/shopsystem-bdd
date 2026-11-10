-- The time words of the base grammar 4 (the CNL 4 design, section 4.4; I16), tied to no kind: an amount (a number
-- in digits, or one to twelve in words), the order of two moments (after, before), and newest and oldest. What they
-- say of a kind (a moment compared, a duration of a unit, "the newest K", the perfect as history) is generated over
-- them (a Span is a duration said: an amount and a unit) by scripts/spec_rgl_time.py into the module Context, which extends this one.
abstract Time = Base ** {
  cat Amount ; Order ; Sup ; Span ;
  fun
    AmountInt : Int -> Amount ;                 -- 7
    A_one, A_two, A_three, A_four, A_five, A_six, A_seven, A_eight, A_nine, A_ten, A_eleven, A_twelve : Amount ;
    After, Before : Order ;
    Newest, Oldest : Sup ;
}
