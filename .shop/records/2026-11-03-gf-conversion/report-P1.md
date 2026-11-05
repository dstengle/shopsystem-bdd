---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p1
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P1, the grammar toolchain

Branch `gfc/P1`, commit f37d0ad0, off `gf-conversion`. Written by the layer 1 merge from the package's returned notes:
the harness refused the package's own write of this file.

## What was built

- `scripts/tools_grammar.py` (new, 180 lines): GF is downloaded with urllib (`file://` works for tests) into a
  mkdtemp beside the target, checked by sha256, unpacked with `dpkg-deb -x`, given a `bin/gf` wrapper
  (LD_LIBRARY_PATH = `usr/lib` plus the `*-ghc-*` dir), then renamed into place. A wrong digest leaves nothing
  behind. The pgf, clingo and telingo wheels go into `sys.executable`, never into `--python`. `gf_binary(environ)` is
  the one lookup of GF: `$SHOPSYSTEM_GF`, the install path, then a `gf` on PATH checked with `shutil.which`.
- `scripts/tools_env.py`: `RUFF_PIN` is now `PINS = {'ruff': '0.17.0'}`. `probe` prints a `grammar:` block after the
  python line (gf with its path, pgf, clingo, telingo, or `<tool> missing: <what stops>`) and exits 1 if one is
  missing. `probe --json` prints `{python, source, tools, grammar}`. `probe --log` is unchanged. `install` runs the
  analysis install, then always the grammar install, and on refusal prints `the grammar tools are not installed:
  <why>` and exits 1.
- `scripts/tools`, `tests/scripts/test_tools_grammar.py` (new), `tests/scripts/test_tools.py`,
  `tests/scenarios/analysis_tools_probe_steps.py`: an autouse fixture puts a stub GF 3.12 under a fresh
  XDG_DATA_HOME and unsets SHOPSYSTEM_GF, so scenarios never download; `tool_lines()` cuts off the grammar block.

## Checks

1. `pytest tests/scripts/test_tools_grammar.py tests/scripts/test_tools.py`: 19 passed, 1 skipped (an existing test
   that skips when nothing is missing). Covered: a download from a local `.deb` built with `dpkg-deb --build`, a
   wrong digest refused with nothing left behind, unsupported platforms refused naming `$SHOPSYSTEM_GF`, missing
   `dpkg-deb` refused, wheels at their pins (`--user` outside a venv), an externally managed interpreter refused
   naming `--python`, the gf lookup order, probe text and JSON.
2. `tools install && probe --json` grammar assert: PASS (gf 3.12.0, pgf 1.1, clingo 5.8.2, telingo 2.1.3).
3. `~/.local/share/shopsystem-bdd/gf-3.12/bin/gf --version` contains `version 3.12`: PASS.
4. A second install prints `gf 3.12 already installed` and no `downloaded`: PASS.
5. `tools size --limit 300` exits 0; the suite is at baseline; analysis-tools scenarios 65/65.

## Notes

- GF 3.12 is installed for real at `~/.local/share/shopsystem-bdd/gf-3.12`, so later layers can drop `SHOPSYSTEM_GF`.
- `tools check`: the only findings are RUF100 on `scripts/tools`' pre-existing `noqa: E402` lines, left as they were.
- Module-map row: `scripts/tools_grammar.py` | the grammar tools: GF 3.12 and the pinned pgf, clingo and telingo
  wheels, installed (`tools install`) and probed (`tools probe`'s grammar block, `--json`), and GF's lookup
  (`gf_binary`).
