"""The live spec's `model logic`, solved once per session (once per xdist worker) for every test that asks for it
(design-r3 §7): `live_logic` is `spec_solve.run` of this repository, its findings. A test that uses it is marked
`@pytest.mark.live_logic`, so `-m "not live_logic"` leaves out every test that solves the live spec.

`EXPECTED` is {finding text: why} of the live findings that are known and open; the tests pass over them. It starts
empty, and the work that finds a live clash (plan-r3 S11) adds it here with its reason."""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
EXPECTED: dict[str, str] = {}


@pytest.fixture(scope="session")
def live_logic():
    import spec_solve
    toolchain.require()
    return spec_solve.run(REPO)


@pytest.fixture(scope="session")
def live_expected():
    """`EXPECTED`, for a test module, which cannot import this conftest by name."""
    return EXPECTED
