# The board: items ranked and prepared apart from the building of work (design, 2026-10-30)

A design from a discovery conversation between the person and a session on 2026-10-30, held in place of answering the
eight questions of initiative i57 (request q31, "A backlog of ideas and a log of temporary rules"). It replaces q31's
backlog lines; q31's log of temporary rules is out of it (see Non-goals).

## Intent and the why

Today the only place a thought can go is a request, and a request is work: raised, it sits in the queue that `work run`
executes. The person, 2026-10-30: "I don't want everything to immediately become work. It makes it seem like everything
is set up and there is just a queue to go through. Some things are just ideas for improvements. Others may be bugs that
may or may not be relevant and even well-formed work should be able to be prioritized. The mix of items in different
states of readiness can be taken care of separately from the execution of work."

A second cost: the shaping of a request (the `integrate`, gate, `apply` and `formulate` rounds) happens inside `work run`
today, so its questions interrupt delivery. i48 stopped three times in one day on spec questions (r189, then w238's
missing r190) while the person wanted it to build. The person would "prefer if any of the questions were taken care of
in a dedicated session rather than interrupting the work. It doesn't have to literally be in session, it can still be a
background task so as to keep up the flow."

So: a **board** that holds every item in its stage of readiness, ranked, with the preparing of items kept apart from
their building, and `work run` building only items that are fully formed.

## Goals

1. **Items before work.** An idea, an observation or a suspected bug a session or the person notices goes on the board,
   not into the build queue. Adding an item commits to nothing.
2. **Stages.** Each item is in one of five stages:
   - **Backlog**: raw; may be one line.
   - **Discovered**: has the context to be worked from without the person: a design note from a discovery conversation
     like this one, or a bug write-up.
   - **Groomed**: shaped. Its spec lines and scenarios are written and the shaping rounds have no question left open.
   - **Doing**: being built by `work run`.
   - **Done**.
3. **Ranking by WSJF.** Each item carries three ratings, each low, medium or high: **value** (what it is worth done),
   **urgency** (how much waiting costs) and **size** (how much work). Order is cost of delay over size
   (Weighted Shortest Job First). The person: "A good framework would be the cost of delay vs effort." Low/medium/high is
   the person's chosen starting scale.
4. **Bugs rated the same way.** A bug item says, in plain words, what goes wrong and how badly (risk) and how often it
   is likely to happen (likelihood); these feed its value and urgency. The person: "In order to prioritize a bug I need to
   know what the risk and likelihood is."
5. **The session guesses, the person corrects.** A session that adds an item gives its first ratings and, for each, its
   reasons. The person corrects ratings and reasons.
6. **Dependencies.** An item may name items it depends on. An item is never picked, for grooming or for building, while
   an item it depends on is not Done. The person: "There should be priority and dependency together, which will drive the
   actual order of grooming and building."
7. **Backlog → Discovered is recommended, not automatic.** The session recommends that an item has enough context to
   leave Backlog, by a ruleset that starts small and that the person refines over time. The person: "the session can
   recommend and we can refine a ruleset over time." A one-liner usually needs a discovery conversation with the person,
   which writes the item's note.
8. **Discovered → Groomed runs on its own.** A background task takes the top-ranked unblocked Discovered item and runs
   the shaping rounds on it. Questions those rounds cannot settle are left on the item for the person's next sitting;
   they do not stop any build. The item is Groomed when no question is left.
9. **Groomed → Doing runs on its own.** `work run` takes the top-ranked unblocked Groomed item by itself and builds it.
   The person: "work run takes the top unblocked item automatically."
10. **The board as tables in the Claude session, the least effort first.** The person: "the easiest path with tables in
    the claude session and minimize the effort." A command prints the board as a table per stage, items in rank order,
    each row with its kind (bug, idea, request), its three ratings with the session's reasons, its blockers and its open
    questions. The person grooms in the session: the session shows the table, the person corrects ratings, moves items
    and talks an item through, and the session writes each change with the board's commands.
11. **Requests from other repositories skip the board.** A request whose asker is another bounded context or the product
    level goes straight to Doing through intake, as today. The person: "requests from other repos should go straight to
    doing." The board holds this context's own items.

## Non-goals

- **The log of temporary rules** (q31 lines 6-9 and i57's migration-tools r35-r36): a separate idea that "doesn't fit
  well into the above framework" (the person). It goes on the board as its own Backlog item.
- **Removing every question from building.** Some questions only show when code is written (w238's "the spec has no line
  for this"). The aim is fewer; a question during building goes back to the board and does not hold the run.
- **A finer scale than low/medium/high**, for now.
- **A browser board with a session beside it, and a TUI.** The person preferred them in the mockups (a browser board
  first, a TUI as the terminal view) but chose the least effort for now. Each is a Backlog item of its own.

## Anti-goals

- **A board that is just the queue again**: if adding an item drafts work, starts rounds, or puts it in front of
  `work run` without passing Discovered and Groomed, the design has failed.
- **Questions interrupting a build** that grooming could have asked.
- **Ratings without reasons**: the person corrects reasoning, not bare labels.

## Constraints

- Everything the plugin keeps is kept in the repository (q31 line 10; the repository's way throughout).
- Work enters the bounded context only as a request (glossary, **request**). An item reaches the shaping rounds by
  becoming a request; the board is where items wait before and while that happens.
- Spec lines are never edited, only retired and replaced.
- The repository's 300-line limit on Python files and its module map (CLAUDE.md) hold for whatever is built.

## Decided in the conversation

The five stages and what moves an item between them; WSJF with low/medium/high value, urgency and size; risk and
likelihood for bugs; the session's first guess with reasons; dependencies blocking both grooming and building; the
tables in the Claude session as the only view for now; requests from other repositories straight to Doing; the
temporary-rules log out of scope; the scoring: L=1, M=2, H=3, cost of delay = value + urgency, score = cost of delay /
size, ties to the item added first.

## The session's calls (not agreed by the person)

- The board is stored in the repository, in `.shop/`.
- One item becomes one request, raised when the background grooming task takes it from Discovered; the request's lines
  are drafted from the item's note.
- A groomed item's spec lines and scenarios land on main as today's formulate rounds land them; its scenarios are
  expected failures until built.
- A bug item whose spec line already exists is groomed to a failing scenario of its own, so it reaches Groomed the same
  way.
- `work run` keeps its pool of initiatives side by side, filled from Groomed in rank order. A question raised while an
  item is in Doing stays on the item's row; its other work-items go on.
- A session's size guess may draw on what `measure` recorded for similar finished initiatives.
- An existing observation of `.shop/records/observations.md` that no request or initiative names (what `work list`
  prints today, requests r64) becomes a Backlog item.

## Left to the builder

The board's file format; the commands that print and change the board; how the background grooming task is started and
paced; the first ruleset for Discovered; how i57, i48's w238 and q44 move onto the board.
