# base

The base pack (b609, decisions 0129-0133): the kinds most bounded contexts name and none owns, so that no area of a
context's domain model declares them for the others. A bounded context imports it with `imports: [base, request]` in
the frontmatter of `spec/index.md` (`migrate init` writes it so); a word of its own spelled the same is marked
`Redefines: base.` In a context with a domain model, a kind of an imported pack is a declared object for the model: an
object may be a kind of it, and a relation, an attribute or a parameter may name it, as `has → file` (v_m8 names none).

## Glossary

- **text** (noun): what a person, a session or a tool writes, a file or a part of one written whole.
- **file** (noun): a file or a directory of the repository.
- **version** (noun): one release of a thing, written `<major>.<minor>.<patch>`.
- **repository** (noun): the version-controlled store a bounded context is kept in, with its working tree. Plural: repositories. This: the repository the request is made in.
- **bounded context** (noun): one repository's spec, with its index, capabilities and domain model. This: the bounded context the request is made in.
