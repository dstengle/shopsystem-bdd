"""The suite's commands run as `shop` runs them (b631): the old command names print a notice on stderr that `shop`
replaces them (adapter_cli_respond's `notice`), and the tests that read stderr allow it by running every command with the mark `shop`
sets, until the scenarios and the CLI adapter contract say `shop` (b633). tests/scripts/test_old_names.py clears the
mark to see the notice."""
import os

os.environ["SHOPSYSTEM_BY_SHOP"] = "1"
