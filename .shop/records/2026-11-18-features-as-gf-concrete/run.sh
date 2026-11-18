#!/bin/sh
# The spike of the record features-as-gf-concrete: a toy logical form turned into a toy scenario by `def` rules.
# Run from this folder with GF 3.12 on PATH (or $GF) and the pgf 1.1 wheel installed.
GF=${GF:-gf}
$GF -make --quiet LfEng.gf || exit 1
T='toScen (Rule (Cons (Done (Stage Z)) Nil) Runs (Cons (Writes (File Z)) Nil))'
echo "1. gf shell, pt -compute then linearise:"
echo "pt -compute ($T) | l" | $GF --run Lf.pgf
echo "2. a def with no equation for its argument is left as it is, with no error:"
echo 'pt -compute (givens (Cons (Writes (File Z)) Nil))' | $GF --run Lf.pgf
echo "3. pgf 1.1 (the C runtime's Python binding), PGF.compute of the same tree:"
python3 -c "import pgf,sys; g=pgf.readPGF('Lf.pgf'); print(g.compute(pgf.readExpr(sys.argv[1])))" "$T"
echo "   exit $?"
