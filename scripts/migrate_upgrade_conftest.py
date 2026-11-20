"""The scenario conftest of an upgrade (b423, upgrades#r36, #r37), planned on every upgrade from a release before the
plugin's, tied to no release so that it holds whatever release a context was founded at: a scenario conftest that is
still the old scenario conftest form (the text `migrate init` wrote before 0.41.0, which does not load `work_items`)
rewritten to the scenario conftest form (migrate_init's `CONFTEST_TEXT`); one of neither form, edited by hand, left as
it is and named for a session to load `work_items` in by hand; one of the current form, or none, left alone."""
from migrate_upgrade_ids import Changes

# the scenario conftest `migrate init` wrote before 0.41.0, verbatim (4ba23b38b~:scripts/migrate_init.py)
OLD = '''"""The generated features' scenarios: one `test_<capability>.py` a capability binds its feature's steps."""
'''


def plan(root):
    # imported here: migrate_init imports migrate_upgrade, which imports this module
    from migrate_init import CONFTEST, CONFTEST_TEXT
    changes = Changes()
    changes.notes = []
    path = root / CONFTEST
    if not path.is_file():
        return changes
    text = path.read_text()
    if text.strip() == OLD.strip():
        changes.texts[CONFTEST] = CONFTEST_TEXT
        changes.notes.append("%s: rewritten to the scenario conftest form, which loads work_items" % CONFTEST)
    elif text.strip() != CONFTEST_TEXT.strip():
        changes.notes.append(
            "%s: of neither the old scenario conftest form nor the scenario conftest form, left as it is: load "
            "work_items in it by hand (config.pluginmanager.import_plugin(\"work_items\") in pytest_configure)"
            % CONFTEST)
    return changes
