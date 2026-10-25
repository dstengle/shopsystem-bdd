"""features/design-model-check.feature, bound to scripts/model: every scenario of the file, by `scenarios()`.

A Given builds the repository in `world` (see conftest); the When runs `model` once; the Then steps read what it
printed. The checks that read the findings as data (`check --json`) run it a second time, on demand.
The When steps are here; the Given and Then steps are in design_model_check_*.py, by what they are about.
"""
import sys

from pytest_bdd import parsers, scenarios, when

from .design_model_check_clingo import *
from .design_model_check_given import *
from .design_model_check_glossary import *
from .design_model_check_one_each import *
from .design_model_check_problems import *
from .design_model_check_requests import *
from .design_model_check_reading import *
from .design_model_check_records import *
from .design_model_check_then import *
from .design_model_check_trace import *

scenarios("design-model-check.feature")


# --- When ------------------------------------------------------------------------------------------------------

@when("`model check` is run")
def model_check(world, context):
    if "env" in context:  # r12: the interpreter that cannot import clingo, and no other on the PATH
        context["result"] = world.model("check", env=context["env"], timeout=60)
    else:
        context["result"] = world.model("check")


@when("`model check` is run without --json")
def model_check_plain(world, context):
    context["result"] = world.model("check")


@when(parsers.re(r"`model check` is run (?P<limit>with --limit \d+|with no --limit)"))
def model_check_limited(world, context, limit):
    args = [] if limit == "with no --limit" else ["--limit", limit.rsplit(" ", 1)[1]]
    context["result"] = world.model("check", *args)


@when("`model facts` is run")
def model_facts(world, context):
    context["result"] = world.model("facts", python=[sys.executable, "-I", "-S"])


@when(parsers.parse("`model why` is run for {ref}"))
def model_why(world, context, ref):
    if ref in ("that requirement", "it"):
        ref = context["ref"]
    context["result"] = world.model("why", ref)
