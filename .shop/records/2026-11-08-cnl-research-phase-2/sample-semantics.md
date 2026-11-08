# What the 27 sample lines mean: today, under a formal reading, and how each should be verified (b112, phase 2)

## 0. What was done

For each of the 27 lines in the phase 2 sample (`scratchpad/b112/sample.md`: 24 capability lines and U4, U7, U11):

1. **Today's facts**: read from the code on main, not by hand: `spec_context.load('.')` (`scripts/spec_context.py`)
   gives `ctx.facts[id]`, the output of `spec_facts.translate` on the parsed tree, and `ctx.domain` (the `prose/1`,
   `dalt/dlit` and `fun/1` facts). Script: `scratchpad/b112/semantics/facts.py`, output `facts.out` beside it. Which
   predicates `grammar/check.lp` reads was counted with grep (`every/2`, `only/3`, `ocond`, `onot`: 0 uses).
2. **A DRS / first-order reading** as ACE would give it (Fuchs, Kaljurand & Kuhn 2008; Fuchs & Kaljurand 2006,
   "Logical Background"): an indefinite in a condition is universally quantified over the whole conditional (the
   donkey reading); "the" must find an accessible antecedent; "no" and "not" open a negation box whose referents are
   inaccessible outside it; "every" is a universal box wherever it stands; "only" is a universal with restrictor and
   scope swapped. ACE has no "while"/"when" templates: I read EARS's While/When/If as a conditional box whose
   antecedent holds at time T and whose consequent is obliged at T+1 (the reading `design-r3 §9` states: G(T → X R),
   G(C → R)).
3. **An event-calculus reading** after Hall et al. 2021 (EARS into event calculus in s(CASP), arXiv 2109.04634) and
   PENG-ASP's temporal extension (Schwitter 2019, read in abstract only, as phase 1 did): `While C` = `HoldsAt(C,T)`,
   `When/If E` = `Happens(E,T)`, a state-changing response = `Initiates/Terminates(E,F,T)` and inertia carries every
   other fluent to T+1; an output (print, exit, an error message) = `Happens(out,T+1)`. "change nothing" = no fluent of
   the repository is initiated or terminated by E. Notation: `H(f,T)` HoldsAt, `E(e,T)` Happens, `I(e,f,T)` Initiates,
   `Tm(e,f,T)` Terminates. I write EC only where it says something the FOL does not (state change, time, inertia).
4. The current scenario (the one tagged `@<id>` in `features/<cap>.feature`), judged good / fair / weak / none.

Facts are shown without their first argument (the requirement id). `v<n>` is a role (one generic instance), `a_*` an
actor constant, `k_*` a kind, `c_*` a condition, `t_*` an attribute, `r_*` a relation, `e_*` a verb.

Of the 15 conditions the sample uses, **3 are defined** (read into facts: `idle`, `current`, commit's `uncited`) and
**12 are prose** (`prose(c)`: unreadable, unparsed, originless, tasked, tracking, unframed, uncommitted, misversioned,
nested, sweeping, frameless, prepositioned). The right sense of each homonym was picked in every case (e.g.
`c_unparsed` is the request line's, `c_unparsed_2` the requirement's; `c_uncommitted` the untracked file's).

### Verdict scale

- **same**: today's facts carry what the formal reading carries (a prose condition is then just a one-place
  predicate in both).
- **loses detail**: the facts are a weaker or vaguer reading; nothing the line asserts is turned into something else,
  but a relation, a binding, a quantifier or a variable is lost (including a coined adjective hiding a relation the
  writer meant).
- **different meaning**: the facts, or the line read literally, assert something other than the writer meant, or
  drop the assertion.

---

## 1. The lines

### 1.1 requests#r33

> While a comment is unreadable, when a session runs `work sync`, `work` shall print the comment, and `work` shall not
> write the comment. *(unreadable: a comment whose block of fields does not parse; prose)*

**Today.** `form(while_when)`, `role(v1,k_comment)`, `ccond(v1,c_unreadable,pos)`, `role(v2,k_session)`,
`trig(ran,"`work sync`",v2,none)`, `resp(1,pos,print,a_work,v1)`, `resp(2,neg,e_write,a_work,v1)`. In English: for
any comment that has the opaque property *unreadable* and any session that runs the string `` `work sync` ``, `work`
prints that comment and does not write it. `check.lp` reports L6 against r32, r52, r53 because the clash rests on the
prose condition.

**DRS / FOL.** ∀c∀s [comment(c) ∧ unreadable(c) ∧ session(s) ∧ run(s,`work sync`) → print(work,c) ∧ ¬write(work,c)];
with the definition expanded: unreadable(c) ≡ ∃b (block_of_fields(b) ∧ of(b,c) ∧ ¬parses(b)), or in the owner's
rewrite ¬conforms(c, comment_schema).
**EC.** H(unreadable(c),T) ∧ E(run(s,sync),T) → E(print(work,c),T+1) ∧ ¬I(run(s,sync), recorded(c), T).
"shall not write" is a frame statement: the event initiates no `recorded(c)`.

**Differences.** The comment is not anchored to the sync: the formal reading quantifies over every unreadable comment
anywhere, where the writer means a comment on an issue the sync reads. The condition is opaque (a relation to a
block of fields and a parse, i.e. conformance to a schema). **Loses detail.**

**Pattern / route.** Next-step effect rule (State-driven + event-driven EARS). Route: scenario. Scenario: *Given a
comment c1 / And the comment c1 is unreadable / When the session s1 runs `work sync` / Then `work` prints the comment
c1 / And `work` does not write the comment c1*. **Good**, but the meaning of *unreadable* is only in the handler
(`requests_handlers_issues.py`), and `s1` is never introduced.

### 1.2 requests#r38

> While a request line is unparsed, if a session runs `work outcome accepted` on the request line, then `work` shall
> exit with an error naming the request line and change nothing. *(unparsed: a request line that does not parse in
> its upstream's requirement grammar; prose)*

**Today.** `form(while_if)`, `role(v1,k_request_line)`, `ccond(v1,c_unparsed,pos)`, `role(v2,k_session)`,
`trig(ran,"`work outcome accepted`",v2,v1)`, `resp(1,pos,exit_error,a_work,v1)`, `resp(2,pos,change_nothing,a_work,none)`.
The trigger's object is bound to the request line: the link is kept.

**DRS / FOL.** ∀l∀s [request_line(l) ∧ unparsed(l) ∧ session(s) ∧ run_on(s,`work outcome accepted`,l) →
∃e (error(e) ∧ names(e,l) ∧ exit(work,e)) ∧ nochange(work)]. Definition: unparsed(l) ≡ ∃q∃u∃g (request(q) ∧
in(l,q) ∧ upstream_of(u,q) ∧ grammar_of(g,u) ∧ ¬parses(l,g)).
**EC.** H(unparsed(l),T) ∧ E(run(s,outcome,l),T) → E(exit_error(work,l),T+1) ∧ ∀f (H(f,T+1) ↔ H(f,T)).

**Differences.** Condition opaque: the chain line → request → upstream → grammar and the parse are lost. **Loses
detail.**

**Pattern / route.** Effect rule (unwanted behaviour, If). Scenario: *Given a request line r1 / And the request line r1
is unparsed / When the session s1 runs `work outcome accepted` on the request line r1 / Then `work` exits with an error
naming the request line r1 / And `work` changes nothing*. **Good.** "change nothing" is entailed by U11 (§2).

### 1.3 requests#r6

> While a command is originless, if the person runs `work request`, then `work` shall exit with an error naming an
> origin and change nothing. *(originless: a command that gives none of `--source`, `--thread` and `--raised-for`;
> prose)*

**Today.** `form(while_if)`, `role(v1,k_command)`, `ccond(v1,c_originless,pos)`,
`trig(ran,"`work request`",a_the_person,none)`, `role(v2,k_origin)`, `resp(1,pos,exit_error,a_work,v2)`,
`resp(2,pos,change_nothing,a_work,none)`. Two unconnected things: *some* originless command, and a run of the string
`` `work request` ``. The error names a fresh origin `v2`.

**DRS / FOL.** ∀c [command(c) ∧ originless(c) ∧ run(person,`work request`) → ∃o (origin(o) ∧ ∃e (error(e) ∧ names(e,o)
∧ exit(work,e))) ∧ nochange(work)]. What the writer means: ∀c [command(c) ∧ run(person,c) ∧ name(c,`work request`) ∧
¬∃p (option(p) ∧ gives(c,p) ∧ p ∈ {--source, --thread, --raised-for}) → ∃e (error(e) ∧ mentions(e, "origin") ∧
exit(work,e)) ∧ nochange(work)].

**Differences.** (a) The originless command is not the command run (the glossary's *command* is "one run of a tool
with its arguments", so the run *is* the command, but the line does not say so). (b) "naming an origin" introduces
an origin that, by the condition, does not exist: the word is used about the concept (the error says an origin is
needed), not about a thing. (c) The definition hides the command's options. **Different meaning.**

**Pattern / route.** Effect rule (If). Scenario: *Given a command c1 / And the command c1 is originless / When the
person runs `work request` / Then `work` exits with an error naming the origin o1 / And `work` changes nothing*.
**Weak**: `c1` is not the command run except by the handler's convention; `o1` is never introduced and cannot exist.
"change nothing" entailed by U11.

### 1.4 requests#r24

> If the person runs `work resolve` on a request that is not `accepted`, then `work` shall exit with an error naming
> the status of the request and change nothing.

**Today.** `form(if)`, `role(v1,k_request)`, `cond(v1,t_status_7,v_accepted_2,neg)`,
`trig(ran,"`work resolve`",a_the_person,v1)`, `resp(1,pos,exit_error,a_work,value(t_status_7,v1))`,
`resp(2,pos,change_nothing,a_work,none)`.

**DRS / FOL.** ∀q [request(q) ∧ ¬status(q,accepted) ∧ run_on(person,`work resolve`,q) → ∃e (error(e) ∧
names(e,status_of(q)) ∧ exit(work,e)) ∧ nochange(work)]. The negation is on an attribute value of a bound referent,
so its scope is unproblematic.
**EC.** ¬H(status(q,accepted),T) ∧ E(run(person,resolve,q),T) → E(exit_error(work,status_of(q)),T+1) ∧ no
I/Tm by the event.

**Differences.** None of substance. **Same.**

**Pattern / route.** Effect rule (If). Scenario: *Given a request q1 / And the request q1 is not `accepted` / When the
person runs `work resolve` on the request q1 / Then `work` exits with an error naming the status of the request q1 /
And `work` changes nothing*. **Good.** "change nothing" entailed by U11.

### 1.5 batches#r8

> While a batch is `building` and every task of the batch is `done`, when the person runs `work batch review` on the
> batch, `work` shall publish a pull request of the batch and set the status of the batch to `in-review`.

**Today.** `form(while_when)`, `role(v1,k_batch)`, `cond(v1,t_status,v_building,pos)`, `uall(u1,k_task)`,
`urel(r_task_of_batch,u1,v1)`, `ucond(u1,t_status_8,v_done_3,pos)`, `trig(ran,"`work batch review`",a_the_person,v1)`,
`role(v2,k_pull_request)`, `orel(r_pull_request_of_batch,v2,v1)`, `resp(1,pos,e_publish,a_work,v2)`,
`set(2,v1,t_status,v_in_review)`, `resp(2,pos,set(t_status,v_in_review),a_work,v1)`. `check.lp` reads `uall/urel/ucond`
(the universal in a condition subject is supported).

**DRS / FOL.** ∀b [batch(b) ∧ status(b,building) ∧ ∀t (task(t) ∧ of(t,b) → status(t,done)) ∧
run_on(person,`work batch review`,b) → ∃p (pull_request(p) ∧ of(p,b) ∧ publish(work,p)) ∧ set(work,b,status,in-review)].
**EC.** H(status(b,building),T) ∧ ∀t (H(of(t,b),T) → H(status(t,done),T)) ∧ E(review(person,b),T) →
I(review, exists(p) ∧ of(p,b), T) ∧ Tm(review, status(b,building), T) ∧ I(review, status(b,in-review), T).
It is also a transition rule of the batch lifecycle (building → in-review), checkable by L3.

**Differences.** None in the facts. **Same.**

**Pattern / route.** Effect rule + lifecycle transition. Scenario: *Given a batch b1 that is `building` / When the
person runs `work batch review` on the batch b1 / Then `work` publishes the pull request p1 / And the pull request p1
is of the batch b1 / And the batch b1 is `in-review`*. **Weak**: the universal precondition gives no Given at all (no
task, no contrast with a task that is not `done`), so the scenario tests a weaker rule (any building batch is
published). U4 entails that the status change is committed and pushed (§2).

### 1.6 batches#r13

> While a commit of an item in a batch is uncited, if the person runs `work batch review` on the batch, then `work`
> shall exit with an error naming the commit and change nothing. *(uncited: a commit is uncited when the commit cites
> no item; defined)*

**Today.** `form(while_if)`, roles commit v1, item v2, batch v3, `crel(r_item_in_batch,v2,v3,pos)`,
`crel(r_commit_of_item,v1,v2,pos)`, `ccond(v1,c_uncited,pos)`, `rnone(r_commit_cites_item,v1,kind(k_item))` (the
definition expanded), `trig(ran,"`work batch review`",a_the_person,v3)`, `resp(1,pos,exit_error,a_work,v1)`,
`resp(2,pos,change_nothing,a_work,none)`.

**DRS / FOL.** ∀c∀i∀b [commit(c) ∧ item(i) ∧ batch(b) ∧ in(i,b) ∧ of(c,i) ∧ ¬∃j (item(j) ∧ cites(c,j)) ∧
run_on(person,`work batch review`,b) → ∃e (error(e) ∧ names(e,c) ∧ exit(work,e)) ∧ nochange(work)]. The `rnone` is the
correct ¬∃ (wide negation), as ACE gives "cites no item".

**Differences.** None. **Same.** (A relative clause "a commit that cites no item" would make the adjective
unnecessary.)

**Pattern / route.** Effect rule (If). Scenario: *Given an item i1 / And a batch b1 / And the item i1 is in the batch b1
/ And a commit c1 / And the commit c1 is of the item i1 / And the commit c1 is uncited / When … / Then `work` exits
with an error naming the commit c1 / And `work` changes nothing*. **Good.** "change nothing" entailed by U11.

### 1.7 batches#r17

> While an item that is `in-batch` proposes a requirement, when a batch parks the item, `work` shall remove the
> requirement.

**Today.** `form(while_when)`, `role(v1,k_item)`, `cond(v1,t_status_6,v_in_batch,pos)`, `role(v2,k_requirement)`,
`crel(r_item_proposes_requirement,v1,v2,pos)`, `role(v3,k_batch)`, `trig(does,e_park,v3,v1)`,
`resp(1,pos,e_remove,a_work,v2)`.

**DRS / FOL.** ∀i∀r∀b [item(i) ∧ status(i,in-batch) ∧ requirement(r) ∧ proposes(i,r) ∧ batch(b) ∧ park(b,i) →
remove(work,r)]. Meant: ∀i∀r∀b [… ∧ in(i,b) ∧ park(person,i) → remove_from(work, r, spec_of(branch_of(b)))].
**EC.** E(park(b,i),T) → Tm(park, in(r, spec(branch(b))), T): the requirement is taken out of the batch branch's spec,
not destroyed.

**Differences.** (a) The batch is not linked to the item (`in(i,b)` missing). (b) A batch is the agent of "parks":
the real agent is the person running `work batch park`. (c) "remove" has no place: the requirement leaves the batch
branch's `spec/`, it is not deleted from the item. **Loses detail.**

**Pattern / route.** Effect rule. Scenario: *Given an item i1 that is `in-batch` / And a requirement r1 / And the item
i1 proposes the requirement r1 / When the batch b1 parks the item i1 / Then `work` removes the requirement r1*.
**Fair**: the handler decides where "removed" is checked; `b1` is never introduced.

### 1.8 batches#r16

> When the person merges the pull request of a batch, `work` shall remove every review folder of the batch.

**Today.** `form(when)`, `role(v1,k_pull_request)`, `the(v1)`, `role(v2,k_batch)`,
`crel(r_pull_request_of_batch,v1,v2,pos)`, `trig(does,e_merge,a_the_person,v1)`, `role(v3,k_review_folder)`,
`every(v3)`, `crel(r_review_folder_of_batch,v3,v2,pos)`, `resp(1,pos,e_remove,a_work,v3)`.

**DRS / FOL.** ∀b∀p [batch(b) ∧ pull_request(p) ∧ of(p,b) ∧ merge(person,p) → ∀f (review_folder(f) ∧ of(f,b) →
remove(work,f))]. "the pull request of a batch" is a functional definite (one pull request per batch), unique
*relative to b*, not globally.
**EC.** The trigger is outside the system (a merge on GitHub); `work` observes it when `work batch merged` runs:
E(merge(person,p),T1) ∧ E(run(person,`work batch merged`,b),T2) ∧ T1 < T2 → ∀f (of(f,b) → Tm(…, exists(f), T2)).

**Differences.** (a) `the(v1)` makes the pull request the only one of its kind in the check (`check.lp:73-96` forces
every pull-request role of a paired line onto it) instead of the batch's own. (b) `every(v3)` is not read by
`check.lp` (0 uses); the generic instance happens to give a universal-like reading for a positive response, but the
scenario shows one folder and no contrast. (c) The response is to an external event observed later. **Loses detail.**

**Pattern / route.** Bounded response (after the merge, by the next `work batch merged`). Scenario: *Given a pull
request p1 / And a batch b1 / And the pull request p1 is of the batch b1 / And a review folder r1 / And the review
folder r1 is of the batch b1 / When the person merges the pull request p1 / Then `work` removes the review folder r1*.
**Weak**: one folder, no folder of another batch kept, and the When names an act the tool does not observe.

### 1.9 backlog#r20

> While a repository is tasked, if the person runs `work idea`, then `work` shall exit with an error naming the task
> and change nothing. *(tasked: a repository whose branch checked out is the branch of a task; prose)*

**Today.** `form(while_if)`, `role(v1,k_repository)`, `ccond(v1,c_tasked,pos)`,
`trig(ran,"`work idea`",a_the_person,none)`, `role(v2,k_task)`, `the(v2)`, `resp(1,pos,exit_error,a_work,v2)`,
`resp(2,pos,change_nothing,a_work,none)`.

**DRS / FOL.** As written, "the task" has no antecedent: ACE would refuse it, or (with a lexicon-declared unique
task) read it as the one task. Meant: ∀r∀t [repository(r) ∧ current_repo(r) ∧ task(t) ∧ checked_out(r) = branch_of(t)
∧ run_in(person,`work idea`,r) → ∃e (error(e) ∧ names(e,t) ∧ exit(work,e)) ∧ nochange(work)].

**Differences.** (a) The task's antecedent exists only inside the prose definition of *tasked*: the adjective hides
the referent the response names; the check reads it as the unique task. (b) "a repository" is not tied to the
repository the command runs in. **Loses detail** (near "different": with two tasks the facts force them to be one).

**Pattern / route.** Effect rule (If). Scenario: *Given a repository r1 / And the repository r1 is tasked / When the
person runs `work idea` / Then `work` exits with an error naming the task t1 / And `work` changes nothing*. **Fair**:
`t1` is never introduced; its link to `r1` lives in the handler. "change nothing" entailed by U11. With r21 it shows a
hidden priority (§2).

### 1.10 backlog#r21

> While a repository is tracking, when the person runs `work idea`, `work` shall write an item that is `idea`, commit
> the item and keep the upstream branch. *(tracking: a repository whose branch checked out has an upstream branch of
> another name; prose)*

**Today.** `form(while_when)`, `role(v1,k_repository)`, `ccond(v1,c_tracking,pos)`,
`trig(ran,"`work idea`",a_the_person,none)`, `role(v2,k_item)`, `oattr(v2,t_status_6,v_idea)`,
`resp(1,pos,e_write,a_work,v2)`, `resp(2,pos,e_commit,a_work,v2)`, `role(v3,k_upstream_branch)`, `the(v3)`,
`resp(3,pos,e_keep,a_work,v3)`.

**DRS / FOL.** ∀r [repository(r) ∧ ∃b∃u (checked_out(r,b) ∧ upstream_of(u,b) ∧ name(u) ≠ name(b)) ∧
run_in(person,`work idea`,r) → ∃i (item(i) ∧ status(i,idea) ∧ write(work,i) ∧ commit(work,i)) ∧ keep(work,u)] — with
`u` bound from inside the definition, which a DRS can only do if the definition is part of the line.
**EC.** I(idea, exists(i) ∧ status(i,idea), T) ∧ I(idea, committed(i), T) ∧ ¬Tm(idea, upstream_of(u,b), T). "keep" is a
frame statement (inertia already gives it unless some effect terminates it), i.e. a prohibition, not an action.

**Differences.** (a) "the upstream branch" is bound inside the prose definition; read as the unique upstream branch.
(b) The definition hides a comparison of names. (c) "keep" reads as a positive event `e_keep`; it is the negation of
an effect. **Loses detail.**

**Pattern / route.** Effect rule. Scenario: *… When the person runs `work idea` / Then `work` writes the item i1 / And
the item i1 is `idea` / And `work` commits the item i1 / And `work` keeps the upstream branch u1*. **Fair** (`u1` never
introduced). "commit the item" is entailed by U4 if writing a new item `idea` is a transition (§2).

### 1.11 migration-tools#r19

> While a repository is idle, when the SessionStart hook runs `migrate status --hook`, `migrate` shall exit
> successfully, and `migrate` shall not print "migrate upgrade" or print "i1". *(idle: the repository is `own` and no
> initiative is open; defined)*

**Today.** `form(while_when)`, `role(v1,k_repository)`, `ccond(v1,c_idle,pos)`, `cond(v1,t_release,v_own_2,pos)`,
`cnone(k_initiative,c_open)`, `trig(ran,"`migrate status --hook`",a_the_sessionstart_hook,none)`,
`resp(1,pos,exit_ok,a_migrate,none)`, `resp(2,neg,print,a_migrate,"migrate upgrade")`, `resp(3,neg,print,a_migrate,"i1")`.
The defined condition is expanded; "shall not print A or print B" is correctly ¬A ∧ ¬B.

**DRS / FOL.** ∀r [repository(r) ∧ release(r,own) ∧ ¬∃n (initiative(n) ∧ open(n)) ∧ run(hook,`migrate status --hook`)
→ exit_ok(migrate) ∧ ¬print(migrate,"migrate upgrade") ∧ ¬print(migrate,"i1")]. Meant for the last conjunct:
∀n (initiative(n) → ¬print(migrate, id_of(n))).

**Differences.** "i1" is the example's initiative id (from the group's given block), a constant in the formal
reading: the line forbids printing that string only, not any initiative's id. **Loses detail** (example data in a
literal).

**Pattern / route.** Effect rule. Scenario (with example data `.shop/plugin-version` "3.0.1" and a closed `i1`):
**Good** for the example; the general rule is untested.

### 1.12 migration-tools#r14

> While the repository is current, when the person runs `migrate upgrade`, `migrate` shall print "no upgrade step is
> pending" and change nothing. *(current: the repository is `own`; defined)*

**Today.** `form(while_when)`, `role(v1,k_repository)`, `the(v1)`, `ccond(v1,c_current,pos)`,
`cond(v1,t_release,v_own_2,pos)`, `trig(ran,"`migrate upgrade`",a_the_person,none)`,
`resp(1,pos,print,a_migrate,"no upgrade step is pending")`, `resp(2,pos,change_nothing,a_migrate,none)`.

**DRS / FOL.** release(here,own) ∧ run(person,`migrate upgrade`) → print(migrate,"no upgrade step is pending") ∧
nochange(migrate). "the repository" is deictic: the glossary defines *repository* as "the repository `migrate` runs
in", so uniqueness is right here.

**Differences.** None of substance. **Same.** (The L6 finding r14/r25 comes from r25's prose condition.)

**Pattern / route.** Effect rule. Scenario: **Good**. "change nothing" is **not** entailed by U11: nothing is refused.

### 1.13 migration-tools#r25

> While the repository is unframed, when the person runs `migrate upgrade`, `migrate` shall rewrite `spec/index.md` and
> print "verb frames" and "v_t11". *(unframed: `.shop/plugin-version` names a release after 1.0.0 and before 3.0.0;
> prose)*

**Today.** `role(v1,k_repository)`, `the(v1)`, `ccond(v1,c_unframed,pos)`, `trig(ran,"`migrate upgrade`",a_the_person,none)`,
`resp(1,pos,e_rewrite,a_migrate,"`spec/index.md`")`, two `print` responses.

**DRS / FOL.** ∀v [version_in(here,v) ∧ 1.0.0 < v < 3.0.0 ∧ run(person,`migrate upgrade`) → rewrite(migrate,`spec/index.md`)
∧ print(migrate,"verb frames") ∧ print(migrate,"v_t11")].
**EC.** I(upgrade, frames_labelled(spec_index), T) — the rewrite is a state change, not an output.

**Differences.** The condition hides an order comparison on versions. Because it is prose, `check.lp` cannot see
that *unframed* and *current* (`own`, the plugin's own release) are disjoint, and reports L6 for r14/r25. **Loses
detail.**

**Pattern / route.** Effect rule. Scenario: **Good** (example data "2.4.0").

### 1.14 migration-tools#r8

> While an untracked file is uncommitted, if the person runs `migrate run --context example.org/acme/shop`, then
> `migrate` shall exit with an error naming the untracked file and change nothing. *(uncommitted: an untracked file
> whose text no commit holds; prose)*

**Today.** `form(while_if)`, `role(v1,k_untracked_file)`, `ccond(v1,c_uncommitted,pos)`,
`trig(ran,"`migrate run --context example.org/acme/shop`",a_the_person,none)`, `resp(1,pos,exit_error,a_migrate,v1)`,
`resp(2,pos,change_nothing,a_migrate,none)`.

**DRS / FOL.** ∀f [untracked_file(f) ∧ ¬∃c (commit(c) ∧ holds(c,text_of(f))) ∧ run(person,`migrate run --context
example.org/acme/shop`) → ∃e (error(e) ∧ names(e,f) ∧ exit(migrate,e)) ∧ nochange(migrate)]. Meant: ∀x (context(x) →
…run(person, migrate run --context x)…), and the file in the repository the command runs in.

**Differences.** (a) The context argument is example data fixed in the code: the rule is stated for one context id.
(b) The file is not tied to the repository. (c) The definition hides a negated relation (no commit holds its text).
**Loses detail.**

**Pattern / route.** Effect rule (If). Scenario: **Good** for the example. "change nothing" entailed by U11.

### 1.15 migration-tools#r21

> While a repository is misversioned, when the SessionStart hook runs `migrate status --hook`, `migrate` shall print
> "holds no version" and "banana". *(misversioned: `.shop/plugin-version` holds no version; prose)*

**Today.** `role(v1,k_repository)`, `ccond(v1,c_misversioned,pos)`, `trig(ran,"`migrate status --hook`",
a_the_sessionstart_hook,none)`, `resp(1,pos,print,a_migrate,"holds no version")`, `resp(2,pos,print,a_migrate,"banana")`.

**DRS / FOL.** As written: ∀r [repository(r) ∧ misversioned(r) ∧ run(hook,…) → print(migrate,"holds no version") ∧
print(migrate,"banana")]. Meant: ∀r∀x [… ∧ text_of(plugin_version_file(r)) = x ∧ ¬version(x) → print(migrate,"holds
no version") ∧ print(migrate,x)].

**Differences.** "banana" is the example's file content; read formally it is a constant, so the line requires
printing "banana" in every misversioned repository, which is false for a file holding anything else. **Different
meaning.**

**Pattern / route.** Effect rule. Scenario (Given `.shop/plugin-version` holds "banana"): **Good** for the example;
the requirement itself is right only through the given block.

### 1.16 feature-file-tools#r3

> While the feature file `features/notes.feature` is nested, when the person runs `features list --tag slice-9`,
> `features` shall exit successfully, and `features` shall not print the feature file `features/notes.feature`.
> *(nested: a feature file with a docstring whose text has a tag and a `Scenario:` line; prose)*

**Today.** `role(v1,k_feature_file)`, `named(v1,"`features/notes.feature`")`, `ccond(v1,c_nested,pos)`,
`trig(ran,"`features list --tag slice-9`",a_the_person,none)`, `resp(1,pos,exit_ok,a_features,none)`,
`role(v2,k_feature_file)`, `named(v2,…same…)`, `resp(2,neg,print,a_features,v2)` (`named` makes v1 and v2 one thing).

**DRS / FOL.** As written: nested(notes) ∧ run(person,`features list --tag slice-9`) → exit_ok ∧ ¬print(notes). Meant:
∀f∀g [feature_file(f) ∧ ∃d (docstring(d) ∧ in(d,f) ∧ has_tag(text(d),g) ∧ has_scenario_line(text(d))) ∧ ¬∃s
(scenario(s) ∧ in(s,f) ∧ tagged(s,g)) ∧ run(person, features list --tag g) → exit_ok ∧ ¬print(f)].

**Differences.** The essential link (the tag in the docstring is the tag asked for, and the file has no real scenario
with it) lives only in the example data: `slice-9` in the code and `notes.feature` as a constant. **Loses detail.**

**Pattern / route.** Effect rule. Scenario: *Given the feature file `features/notes.feature` is nested / When … /
Then `features` exits successfully / And `features` does not print `features/notes.feature`*. **Good** for the example.

### 1.17 feature-file-tools#r14

> While the test module `tests/test_cart.py` is sweeping, when the person runs `features bindings --unbound`,
> `features` shall exit successfully. *(sweeping: a test module that binds every scenario of a feature file with one
> `scenarios(...)` call; prose)*

**Today.** `role(v1,k_test_module)`, `named(v1,"`tests/test_cart.py`")`, `ccond(v1,c_sweeping,pos)`,
`trig(ran,"`features bindings --unbound`",a_the_person,none)`, `resp(1,pos,exit_ok,a_features,none)`.

**DRS / FOL.** sweeping(test_cart) ∧ run(…) → exit_ok(features). Meant: ∀m∀f [test_module(m) ∧ feature_file(f) ∧
calls_scenarios(m,f) ∧ run(person,`features bindings --unbound`) → ∀s (scenario(s) ∧ in(s,f) → ¬reports_unbound(features,s))].

**Differences.** The point (each scenario of the file counts as bound) is in the group title and the adjective; the
Then says only "exit successfully", which `--unbound` would do whether or not it lists the cart scenarios. **Loses
detail.**

**Pattern / route.** Effect rule. Scenario: exit code only. **Weak.**

### 1.18 trials#r1

> When a session runs `trial-runner` on a trial, `trial-runner` shall start the trial.

**Today.** `form(when)`, `role(v1,k_session)`, `role(v2,k_trial)`, `trig(ran,a_trial_runner,v1,v2)` (the actor
constant as the command), `resp(1,pos,e_start,a_trial_runner,v2)`.

**DRS / FOL.** ∀s∀t [session(s) ∧ trial(t) ∧ run_on(s,trial-runner,t) → start(trial-runner,t)].
**EC.** E(dispatch(s,tr,t),T) → I(…, running(t), T).

**Differences.** None in the facts. **Same** — though near tautological (running the agent on a trial is starting it).

**Pattern / route.** Effect rule of an agent. Route: judgement (design-decision); a guarantees capability gets no
feature, so no scenario.

### 1.19 trials#r2

> `trial-runner` shall read only a target.

**Today.** `form(ubiq)`, `role(v1,k_target)`, `only(1,k_target)`. **Nothing else**: `respond()` (`spec_facts.py:209-213`)
emits `only` and returns before `resp`, so the verb *read* and the actor disappear; `check.lp` has no rule on `only/3`.
The facts say only "there is a target".

**DRS / FOL.** ∀x [read(trial-runner,x) → ∃g (target(g) ∧ (x = g ∨ part_of(x,g)))] — "only" as a universal with
restrictor and scope swapped (ACE does not have "only" on objects; this is the standard reading).
**EC.** ∀T∀x: E(read(tr,x),T) → within(x, target). A constraint on every event, not a response.

**Differences.** The assertion is lost entirely. **Different meaning.**

**Pattern / route.** State (action) invariant; Dwyer *absence, globally* (no read outside the target). Route: runtime
monitor over the agent's transcript (paths of Read/Glob/Grep/Bash calls), or judgement. No scenario.

### 1.20 trials#r4

> When `trial-runner` ends a trial, `trial-runner` shall write a measurement and name the target.

**Today.** `form(when)`, `role(v1,k_trial)`, `trig(does,e_end,a_trial_runner,v1)`, `role(v2,k_measurement)`,
`resp(1,pos,e_write,a_trial_runner,v2)`, `role(v3,k_target)`, `the(v3)`, `resp(2,pos,e_name,a_trial_runner,v3)`.

**DRS / FOL.** ∀t [trial(t) ∧ end(trial-runner,t) → ∃m (measurement(m) ∧ of(m,t) ∧ write(trial-runner,m) ∧
names(m, target_of(t)))].
**EC.** Better as precedence: E(end(tr,t),T) → ∃T' ≤ T E(write(tr,m),T') ∧ of(m,t). In past-time LTL:
G(end → O write).

**Differences.** (a) "the target" has no antecedent: read as the unique target, where the trial's own target is
meant (`target_of(t)`, a relation the vocabulary lacks). (b) The naming is put on the agent's act, not inside the
measurement (the glossary's *name* has "a message or a file names a thing"). (c) The measurement is not tied to the
trial. **Loses detail.**

**Pattern / route.** Precedence (the trial ends only after its measurement is written). Route: a check after each trial
(the measurement record exists and names the target), or judgement. No scenario.

### 1.21 design-model-check#r60

> If the person runs `model check` on a term that is frameless, then `model` shall exit with an error naming the term.
> *(frameless, adjective of term: a verb whose glossary entry does not name the kinds of its subject and object, nor
> say that it takes no object; prose)*

**Today.** `form(if)`, `role(v1,k_term)`, `ccond(v1,c_frameless,pos)`, `trig(ran,"`model check`",a_the_person,v1)`,
`resp(1,pos,exit_error,a_model,v1)`.

**DRS / FOL.** ∀t [term(t) ∧ verb(t) ∧ ¬∃f (frame(f) ∧ of(f,entry(t))) ∧ run_on(person,`model check`,t) →
∃e (error(e) ∧ names(e,t) ∧ exit(model,e))].

**Differences.** The definition is of a different kind (a verb) than the adjective's (a term), and hides the
relation entry → frame. **Loses detail.**

**Pattern / route.** Effect rule (If). Scenario: **Good**. No "change nothing", but U11 gives it (§2).

### 1.22 design-model-check#r69

> When the person runs `model parse` on a requirement that is prepositioned, `model` shall exit successfully.
> *(prepositioned: a requirement with a prepositional verb followed by its preposition and its object; prose)*

**Today.** `form(when)`, `role(v1,k_requirement)`, `ccond(v1,c_prepositioned,pos)`,
`trig(ran,"`model parse`",a_the_person,v1)`, `resp(1,pos,exit_ok,a_model,none)`.

**DRS / FOL.** ∀r [requirement(r) ∧ prepositioned(r) ∧ run_on(person,`model parse`,r) → exit_ok(model)]. Meant: →
∃tr (tree(tr) ∧ parse_of(tr,r) ∧ print(model,tr)), i.e. parses(r, grammar).

**Differences.** The property is syntactic (a pattern in the text) and the response is a proxy (exit code for
"parses"). **Loses detail.**

**Pattern / route.** Effect rule. Scenario: exit code only. **Weak.**

### 1.23 conversation#r2

> When the UserPromptSubmit hook runs `work quote --hook`, `work` shall keep the session.

**Today.** `form(when)`, `trig(ran,"`work quote --hook`",a_the_userpromptsubmit_hook,none)`, `role(v1,k_session)`,
`the(v1)`, `resp(1,pos,e_keep,a_work,v1)`.

**DRS / FOL.** "the session" has no antecedent. Meant: ∀s [session(s) ∧ prompt_of(s) triggers hook ∧ run(hook,`work
quote --hook`) → store(work, id_of(s), git_dir) ∧ store(work, transcript_of(s), git_dir)] (the handler checks exactly
this, plus a clean `git status`).
**EC.** I(quote_hook, kept(s), T).

**Differences.** (a) The glossary's *keep* (role-boundaries.md) is "a session leaves a thing as it was": under that
reading the line says `work` does not change the session, not that it records it. (b) `the(v1)`: the unique session,
where the one whose prompt fired the hook is meant. **Different meaning.**

**Pattern / route.** Effect rule. Scenario: *When the UserPromptSubmit hook runs `work quote --hook` / Then `work`
keeps the session s1*. **Weak**: no Given introduces `s1`; the meaning is all in `keeps_session`
(`conversation_handlers.py:149-158`).

### 1.24 telemetry#r1

> When the person runs `measure batch` on a batch that is `merged`, `measure` shall write a measurement of the batch,
> include "wall time", include "session time", include "tokens" and include "cost by role".

**Today.** `role(v1,k_batch)`, `cond(v1,t_status,v_merged,pos)`, `trig(ran,"`measure batch`",a_the_person,v1)`,
`role(v2,k_measurement)`, `orel(r_measurement_of_batch,v2,v1)`, `resp(1,pos,e_write,a_measure,v2)`, then four
`resp(i,pos,e_include,a_measure,"<string>")`.

**DRS / FOL.** ∀b [batch(b) ∧ status(b,merged) ∧ run_on(person,`measure batch`,b) → ∃m (measurement(m) ∧ of(m,b) ∧
write(measure,m) ∧ includes(m,"wall time") ∧ …)].

**Differences.** "include" has the tool as subject; what includes the figures is the measurement. The four facts are
not about `v2`. **Loses detail.**

**Pattern / route.** Effect rule. Scenario: *… Then `measure` writes the measurement m1 / And the measurement m1 is of
the batch b1 / And `measure` includes "wall time" …*. **Fair** (the handler reads the record).

### 1.25 universal#U4

> `work` shall commit every transition and push the commit.

**Today.** `form(ubiq)`, `role(v1,k_transition)`, `every(v1)`, `resp(1,pos,e_commit,a_work,v1)`, `role(v2,k_commit)`,
`the(v2)`, `resp(2,pos,e_push,a_work,v2)`. `check.lp` ignores `every/2` and reads an untriggered positive event as an
obligation in every state: L5 twice ("U4 obliges `work` to commit a transition in every state").

**DRS / FOL.** ∀x [transition(x) → ∃c (commit(c) ∧ records(c,x) ∧ make(work,c) ∧ push(work,c))]. "the commit" is an
anaphor to the commit implied by the verb "commit" (verb-to-noun anaphora, which ACE does not resolve either).
**EC.** E(transition(x),T) → ∃T'≥T E(commit(work,c),T') ∧ ∃T''≥T' E(push(work,c),T''), bounded by the end of the
command that made the transition.

**Differences.** Read as "commit in every state", with "the commit" the one commit of the world. The writer means a
response: every transition is followed, before the command exits, by its commit and that commit's push. **Different
meaning.**

**Pattern / route.** Bounded response (Dwyer *response, globally*, bounded by command exit); the owner's "transition
rule" ("the server checks every request"). Route: check after each scenario — `vocab.py:101-124` checks "a run's
commit on the branch is on its remote" (commit ⇒ push); the first half (transition ⇒ commit) is not checked.

### 1.26 universal#U7

> A worker shall change only files in its worktree.

**Today.** `form(ubiq)`, `role(v1,k_worker)`, `role(v2,k_file)`, `every(v2)`, `role(v3,k_worktree)`, `the(v3)`,
`crel(r_file_in_worktree,v2,v3,pos)`, `resp(1,pos,e_change,v1,v2)`. `unwrap()` (`spec_facts_np.py:27-30`) strips the
`Only`, the plural becomes `every`, and since the `only` test in `objects()` looks only at `An`/`One`, no `only` fact is
emitted. "its" becomes `the`: the one worktree, unrelated to the worker. L5 ("in every state").

**DRS / FOL.** ∀w∀f [worker(w) ∧ file(f) ∧ change(w,f) → ∃t (worktree(t) ∧ of(t,w) ∧ in(f,t))].
**EC.** ∀T: E(change(w,f),T) → H(in(f, worktree_of(w)),T).

**Differences.** The facts say "a worker changes every file in the worktree" — an obligation to change everything,
where the line restricts what may be changed. The possessive's link to the worker is lost. **Different meaning.**

**Pattern / route.** Action invariant, Dwyer *absence, globally* (no change outside the worktree). Route: runtime
monitor (the worker's writes, from its transcript or the file system) or a check after each task (the task's diff
touches only its worktree); git worktrees make it largely structural. Not checked today. (*worker* is a retired
workflow's term: universal.md keeps U7 until a line on a batch's task subagent is written.)

### 1.27 universal#U11

> If a tool refuses a command, then the tool shall exit with an error naming the reason and change nothing.

**Today.** `form(if)`, `role(v1,k_tool)`, `role(v2,k_command)`, `trig(does,e_refuse,v1,v2)`, `role(v3,k_reason)`,
`the(v3)`, `resp(1,pos,exit_error,v1,v3)`, `resp(2,pos,change_nothing,v1,none)`.

**DRS / FOL.** ∀t∀c [tool(t) ∧ command(c) ∧ refuse(t,c) → ∃r (reason(r) ∧ of(r,refusal(t,c)) ∧ ∃e (error(e) ∧
names(e,r) ∧ exit(t,e))) ∧ nochange(t)].
**EC.** E(refuse(t,c),T) → E(exit_error(t,r),T+1) ∧ ∀f (H(f,T+1) ↔ H(f,T)).

**Differences.** (a) "the reason" is read as the one reason of the world, not the reason of this refusal. (b) The
trigger is the event `e_refuse`; every line's trigger is a command string, and `check.lp` pairs only coinciding
triggers, so U11 never meets a line in the check. (c) "refuse" has no observable definition; the test check equates
it with a non-zero exit. **Loses detail.**

**Pattern / route.** Effect rule over every command. Route: check after each scenario — `vocab.py:126-127`: non-zero
exit ⇒ no file changed.

---

## 2. Entailment: which lines and Thens follow from others

| Then / line | Entailed by | Bridge needed | Scenario Then removable? |
|---|---|---|---|
| "change nothing" in requests r38, r6, r24; batches r13; backlog r20; migration-tools r8 (6 Thens) | U11 | **refuse(t,c) ↔ exit_error(t,…)**: U11 says refuse → exit error ∧ change nothing; the lines state exit error ∧ change nothing, so U11 entails their second conjunct only if every error exit is a refusal. The after-scenario check already assumes exactly that (non-zero exit ⇒ nothing changed). | Yes: the U11 check after every scenario tests it already, more strongly (on the whole file tree). |
| "change nothing" missing in design-model-check r60 | U11 (same bridge) | as above | Nothing to remove; U11 supplies it. |
| "change nothing" in migration-tools r14 | — | not a refusal (success path) | No. |
| "exit with an error naming X" (7 lines) | U11 gives "naming *a* reason"; the line adds which reason | — | No: the line's own content. With the bridge, each such line is "if C, the tool refuses the command, the reason naming X". |
| batches r8: the status change is committed and pushed (unstated) | U4 | a status change is a *transition* (glossary: "one change of a node's status, written by `work`") | Covered by the U4 check (push half). |
| backlog r21 "commit the item" | U4 | writing a new item with status `idea` counts as a transition (unclear in the glossary) | Only if the bridge is settled. "keep the upstream branch" is not entailed (U4 says push, not where to). |
| batches r16 removal committed and pushed (unstated) | U4 only if removing folders is a transition — it is not a status change | — | — |
| migration-tools r19 vs r14 | idle ⊂ current (idle = own ∧ no open initiative; current = own) | — | No entailment: different triggers. |
| migration-tools r14 vs r25 | disjoint states (own vs 1.0.0 < v < 3.0.0) | an order on versions | Today L6 because unframed is prose. |
| backlog r20 vs r21 | both on `work idea`; tasked ∧ tracking can both hold (a task branch with an upstream of another name) | — | In FOL the pair is **inconsistent** (exit error ∧ change nothing vs write ∧ commit). `check.lp` never pairs them because an `If` line is an exception to a non-`If` one (`check.lp:57-61`): a hidden default/priority that a DRS→FOL translation would have to make explicit. |
| trials r2, U7 | no relation (trial-runner is a *dispatch*, not a *worker*) | — | — |

So the owner's idea holds for the sample, with one bridge axiom: **6 of the 27 lines carry a Then (change nothing)
that U11 entails**, and the scenario's step for it is redundant with the after-scenario check. The entailment cannot be
computed today: the check has no notion of entailment, U11's trigger never meets a command string, and "refuse" has no
definition in observable terms. A DRS-like form with the bridge `refuse ↔ exit_error` as a background axiom would make
it a one-line query.

---

## 3. Summary

### 3.1 Verdicts

| Verdict | n | Lines |
|---|---|---|
| same | 5 | requests r24; batches r8, r13; migration-tools r14; trials r1 |
| loses detail | 16 | requests r33, r38; batches r17, r16; backlog r20, r21; migration-tools r19, r25, r8; feature-file-tools r3, r14; trials r4; design-model-check r60, r69; telemetry r1; U11 |
| different meaning | 6 | requests r6; migration-tools r21; trials r2; conversation r2; U4; U7 |

Two of the five "same" lines are same only for the logic: batches r8's scenario drops its universal precondition.

### 3.2 Patterns

| Pattern | n | Lines |
|---|---|---|
| Next-step effect rule (When/If → response at the next state) | 22 | all service lines but batches r16; trials r1; U11 (batches r8 is also a lifecycle transition) |
| Bounded response | 2 | batches r16 (after an external merge, by the next `work batch merged`); U4 (every transition committed and pushed before the command exits) |
| Precedence (only after) | 1 | trials r4 (a trial ends only after its measurement is written) |
| State / action invariant (absence, globally) | 2 | trials r2; U7 |
| Unbounded liveness | 0 | — |

No sample line is true liveness. The three ubiquitous lines with a verb (trials r2, U4, U7) are two invariants and
one bounded response; today's check reads all three as "does it in every state" (U4, U7: L5) or drops them (r2).

### 3.3 Routes

| Route | n | Lines |
|---|---|---|
| Scenario | 21 | the 21 service lines (scenario today: 11 good, 4 fair, 6 weak) |
| Check after each run (scenario or trial) | 3 | U11 (exists), U4 (exists, push half only), trials r4 (record check after a trial) |
| Runtime monitor | 2 | trials r2 (paths read), U7 (files changed) |
| Judgement (design-decision) | 1 | trials r1 |
| Static check | 0 | — |

Weak scenarios: requests r6 (unconnected command, an origin that cannot exist), batches r8 (no tasks), batches r16
(one folder, an unobserved trigger), feature-file-tools r14 and design-model-check r69 (exit code only), conversation
r2 (session never introduced). The Thens that U11 entails (six) are tested twice.

### 3.4 The five most important semantic faults

1. **`only` is lost or reversed.** trials r2: the verb and actor disappear, the facts say only "there is a target".
   U7: `Only` is stripped by `unwrap()`, the plural becomes `every`, and the facts oblige a worker to change every file
   in the worktree — the opposite of a restriction. `check.lp` has no rule for `only/3` anyway.
2. **A ubiquitous line with a verb is read as "does it in every state", and `every` on an object is ignored.** U4
   (L5 twice), U7 (L5), and batches r16's "every review folder" read as one instance by the check and as one folder in
   the scenario. The real patterns (bounded response, absence invariant) have no representation.
3. **"the" with no antecedent means "the only one in the world".** backlog r20 "the task" and r21 "the upstream
   branch" (antecedent inside a prose definition), trials r4 "the target" (the trial's), U4 "the commit" (the verb's
   object), U11 "the reason" (this refusal's), conversation r2 "the session" (the prompt's), batches r16 "the pull
   request of a batch" (functional, unique per batch). Seven of 27 lines. `check.lp` then forces every same-kind role
   of a paired line onto that one thing.
4. **Unanchored referents: the state's subject is not the thing the trigger acts in or on.** requests r6 (the
   originless command is not the command run, and "naming an origin" introduces an origin that cannot exist), r33 (any
   unreadable comment, not one the sync reads), backlog r20/r21, migration-tools r19/r21/r8 ("a repository", "an
   untracked file" not tied to the repository of the run), batches r17 (batch not linked to the item; a batch as the
   agent of "parks"). The language has no indexical for "the repository / command / session of this run".
5. **Example data stands in for variables, and coined adjectives stand in for relations.** migration-tools r21
   ("banana": a false requirement read literally), r19 ("i1"), r8 (the context argument), feature-file-tools r3
   (`slice-9`, `notes.feature`), r14 (`test_cart.py`). And 12 of the 15 conditions are prose, hiding: a schema
   conformance (unreadable), a parse in a grammar (unparsed, prepositioned), a command's options (originless), a branch
   relation (tasked, tracking, with the very referents the response names), a version order (unframed — the cause of
   the r14/r25 L6), a negated relation (uncommitted, misversioned), a frame relation of a different kind (frameless).

Also seen: verb-sense drift (conversation r2's "keep" means store; the glossary's means leave unchanged); "keep" and
"change nothing" are frame statements read as events; a response's container lost (telemetry r1 "include", trials r4
"name" are put on the tool, not the record); the `If` form's priority (backlog r20 over r21) is a default rule that
first-order logic does not have.

### 3.5 What a DRS-like intermediate form needs to cover the 27

**Referents.** Discourse referents with a kind; constants for actors and named codes; **parameters** for example data
(a variable with a sample value from the given block, so "banana", "i1", `slice-9` are bound to the scenario, not
constants of the rule); **indexical referents** for the run's own repository, command and session (`here`, `this
command`, `this session`), introduced by every trigger.

**Atomic conditions (the minimal predicate set).**

| Predicate | Covers |
|---|---|
| `kind(x,K)` with sub-kinds | every noun |
| `attr(x,A,v)` with an optional order on values | status, release; unframed's version range (r25) |
| `rel(R,x,y)` with cardinality; `fn(R,y)` for "the R of y" | of, in, proposes, cites, upstream of, target of |
| `event(e, Verb, agent, object[, recipient])` | park, merge, refuse, read, change, publish, remove, start, end |
| `run(e, agent, command, args)` with args as referents (`option(p)`, `gives(e,p)`) | every trigger; originless (r6); the context argument (r8) |
| `out(e, Kind, x)` for print / exit ok / exit error, `names(msg,x)`, `includes(record,x)` with its container | the fixed responses; telemetry r1, trials r4 |
| `conforms(x, artifact)` / `parses(x, grammar)` | unreadable, unparsed, prepositioned (owner's schema reading) |
| `defined(C)` as a sub-DRS (its definition box), opaque only when declared external | the 12 prose conditions |
| `initiates/terminates(e,f)`, `nochange(e, scope)`, `keeps(e,f)` (= ¬terminates) | write, remove, set, commit; change nothing; keep |

**Boxes.**

- **Conditional box** (While / When / If ⇒ shall) with a time index: antecedent at T (While = holds, When/If =
  happens), consequent at T+1; antecedent referents universally quantified and accessible in the consequent; inertia
  for every fluent not initiated or terminated.
- **Negation box** with scope over its referents ("no K", "does not V a K" = ¬∃), so "a" under "not" is narrow.
- **Universal box** in any position (every, plurals) and an **only box** (∀x (V(a,x) → restrictor(x))).
- **Disjunction box** (today's case split).
- **Modal operator** on a box: obligation (shall), prohibition (shall not), necessity (invariant: always / never),
  permission (may); and a **priority tag** for the If-form exception.
- **Temporal operators**: next (T+1), a past-time "once / only after" history fluent (precedence, trials r4), and a
  bounded "before the command exits" (U4, batches r16). No unbounded future operator is needed for this sample.
- **Definite resolution rules**: "the" binds to an accessible referent, else to the image of a functional relation
  ("the pull request of the batch"), else to an indexical declared in the glossary ("the repository"), else it is
  refused — never "the only one in the world".

With these, every line in the sample has a formula with truth conditions; the clash check, the Gherkin generator and an
entailment check (U11's "change nothing") can all read the same form.

## Sources

- Fuchs, N. E., Kaljurand, K., Kuhn, T. (2008). Attempto Controlled English for Knowledge Representation. *Reasoning
  Web*, LNCS 5224. Fuchs, N. E., Kaljurand, K. (2006). ACE: Language, Tools and Applications — Logical Background
  (course notes). (As cited in phase 1's `logic-cnls.md`; I relied on that report's summary of the DRS and its
  interpretation rules, not on a fresh reading.)
- Kamp, H., Reyle, U. (1993). *From Discourse to Logic*. Kluwer. (DRS accessibility and donkey sentences; standard
  reference, not re-read for this report.)
- Guy, S., Schwitter, R. (2017). The PENG^ASP system. *Language Resources and Evaluation*; Schwitter, R. (2019).
  Augmenting an Answer Set Based Controlled Natural Language with Temporal Expressions. *PRICAI 2019* (abstract only).
- Hall, B., et al. (2021). Knowledge-assisted reasoning of model-augmented system requirements with event calculus
  and goal-directed answer set programming. HCVS 2021, https://arxiv.org/abs/2109.04634 (via phase 1's
  `requirement-cnls.md` §3).
- Dwyer, M. B., Avrunin, G. S., Corbett, J. C. (1999). Patterns in property specifications for finite-state
  verification. *ICSE 1999*.
- This repository on main: `scripts/spec_context.py`, `scripts/spec_facts.py` (`respond`, `objects`),
  `scripts/spec_facts_np.py` (`unwrap`), `grammar/check.lp`, `tests/scenarios/vocab.py` (`unpushed`, `u_problems`),
  `tests/scenarios/conversation_handlers.py:149-158`, `features/*.feature`, `spec/index.md`, `spec/universal.md`,
  `spec/capabilities/*.md`. Facts dump: `scratchpad/b112/semantics/facts.py` and `facts.out`.
