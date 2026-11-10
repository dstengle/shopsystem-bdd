# spec

The spec pack (b240, quote-23): the few words for talking about a spec. A bounded context imports it with
`imports: [cli, spec]` in the frontmatter of `spec/index.md`; a word of its own spelled the same is marked
`Redefines: spec.` A line about the language names a construct by its code in the construct catalogue ("a
requirement that uses `rc-object`"), and a line about a check names a rule by its code in the rule catalogue ("a
term that violates `v_t11`"), never by a coined word.

## Glossary

- **requirement** (noun): a line of a capability, named `<capability>#r<n>`.
- **construct** (noun): a sentence structure of the controlled language, named by its code in the construct catalogue `grammar/constructs.md`.
- **rule** (noun): a check a spec is held to, named by its code in the rule catalogue `grammar/rules.md`.
- **use** (verb, state): a requirement is said with a construct. Forms: uses, used. Frame: requirement uses construct.
- **violate** (verb, state): a thing breaks a rule. Forms: violates, violated. Frame: thing violates rule.
