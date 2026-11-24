"""Each scripts/ module put in one group: an area of spec/model/, the language toolchain, plumbing or a CLI entry.

The groups follow the capabilities' handlers and CLAUDE.md's module map. `language` is the controlled language's
toolchain (grammar 4, its logical form, the logic and entailment checks, the step grammar and the scenario writer);
`specification` is the rest of the specification area (the domain model, vocabulary, spec reading, `spec` checks,
decisions, records, contracts); `plumbing` is what every command shares; `cli` the entry scripts.
"""

EXPLICIT = {
    # language toolchain
    "features_generate": "language", "features_generate4": "language", "features_vocab4": "language",
    "features_vocab4_request": "language", "model_constructs": "language", "model_constructs_table": "language",
    "model_rules": "language", "model_catalogue": "language", "model_catalogue_entries": "language",
    "model_catalogue_write": "language", "model_explain": "language", "spec_corpus_write": "language",
    # specification (not the language)
    "spec_read": "specification", "spec_read_given": "specification", "spec_context": "specification",
    "spec_moves": "specification", "spec_unbuilt": "specification", "spec_preview": "specification",
    "spec_vocabulary": "specification", "spec_vocabulary_terms": "specification",
    "contract_form": "specification", "adapter_annotate": "specification", "adapter_cli_check": "specification",
    "adapter_tables": "specification", "decision_write": "specification", "decision_amend": "specification",
    "record_write": "specification", "record_design": "specification", "observation_write": "specification",
    "model_requests": "specification", "model_work": "specification",
    # tracking
    "intake_moves": "tracking", "readiness_bar": "tracking", "readiness_before": "tracking",
    "shop_ids": "tracking", "shop_frozen": "tracking", "directive": "tracking", "directive_cli": "tracking",
    # execution
    "delivery_settings": "execution", "work_items": "execution",
    # measurement
    "transcripts": "measurement",
    # plumbing
    "shop_files": "plumbing", "shop_refused": "plumbing", "toml_edit": "plumbing", "domain_envelope": "plumbing",
    "adapter_cli": "plumbing", "adapter_cli_respond": "plumbing", "adapter_cli_probe": "plumbing",
    "store_git": "plumbing", "model_parse": "plumbing", "spec_held": "language",
    # entry scripts
    "work": "cli", "spec": "cli", "model": "cli", "measure": "cli", "tools": "cli", "features": "cli",
    "migrate": "cli",
}

PREFIX = [
    ("spec_", "language"), ("domain_model", "specification"), ("model_", "specification"),
    ("backlog_", "tracking"), ("request_", "tracking"), ("conversation_", "tracking"),
    ("batch_", "execution"), ("measure_", "measurement"), ("tools_", "analysis"), ("features_", "analysis"),
    ("migrate_", "upgrades"),
]


def group(module):
    if module in EXPLICIT:
        return EXPLICIT[module]
    for prefix, g in PREFIX:
        if module.startswith(prefix):
            return g
    return "unplaced"
