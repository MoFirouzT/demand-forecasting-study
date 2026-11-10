# Conventions

House rules for this repository: how shared quantities are named and expressed, and
how committed documentation is written.

*Assumes: the operating contract in [CLAUDE.md](../CLAUDE.md).*

---

## 1. Domain conventions

<!-- Project-specific. Sign conventions, units, time zones, naming, configuration,
     logging. Whatever a reader must hold in their head to read the canonical doc
     without being misled. Delete this comment once filled in. -->

## 2. Writing charter (documentation quality)

The rules that keep the docs clear and consistent. The ones marked **lint** are
enforced by `scripts/lint_docs.py` in CI; the rest are review judgment. A line that
must break a per-line check, for instance to quote a banned word, can end with a
`<!-- lint-ok -->` comment, used sparingly.

This charter is this project's, not a standard. Delete what does not apply here and add
what does; what is not negotiable is that the charter exists, that a subset of it is
machine-checked, and that it says which.

### Clarity outranks brevity

When the two conflict, clarity wins. A rewrite aims first at the message a reader who has
seen none of the surrounding work can take on one pass, and only then compresses it.
Never the reverse: text compressed first and clarified afterwards keeps whatever the
compression broke, because the author can still read their own meaning into it.

Brevity is what is left after clarity, not a budget clarity is spent from. A short
sentence that has to be asked about was not brief; it was incomplete, and the question it
provokes costs more than the words it saved.

The failures are specific, and all of them look tight on the page:

| Symptom | Example | What it costs |
| --- | --- | --- |
| An idiom standing in for a causal chain | "the missing routes are what rung 2 turns on" | The reader has to guess the mechanism |
| A pronoun pointing at a list or a section | "what the archive shows of **this**" | Resolves to nothing specific |
| A compressed noun naming a combination without its parts | "what is less common is **the join**" | Joining what to what |
| A verb used in a guessed sense | "§7 **costs** the alternative" | Reads as a noun first, then has to be re-parsed |
| A deictic with no nearby referent | "it is a kill criterion **there**" | "There" was two clauses ago |

**Test before shipping a sentence:** could a reader who has not seen the conversation that
produced it parse it on one read? If not, the sentence is not finished, however short.

### Word choice

**Use the most common word that is exactly as precise.** A less common word must earn
its place by carrying meaning the common one lacks. If it only sounds more considered,
it is costing the reader and buying nothing. This repo is read by people who did not
write it, including readers whose first language is not English.

Substitutions this project has actually made, kept as a worked example. The table is a
record, not a checklist: the rule is the test.

| Instead of | Write |
| --- | --- |
| | |

**lint: no coined `-able` or `-ability` words.** The commonest failure of the rule, and
the check uses the system word list. If English has no such adjective, write the verb
phrase instead: not *unimplementable* but *cannot be implemented*. <!-- lint-ok --> A real word the list
genuinely lacks goes in `REAL_ADJECTIVES`.

**Borrow a term, do not coin one.** When this project needs a name for a concept, take
the existing term from the field and pin its local meaning in the [glossary](glossary.md).
Repurposed common words need pinning most: they look like plain English and are not.

**Exempt: terms of art.** A word naming a code identifier, a symbol from the canonical
document, or a rule ID is used verbatim every time and never softened into a synonym.
The [glossary](glossary.md) is the sanctioned list; anything outside it can be
simplified.

**Prose about code must be checkable, or not written.** A sentence asserting a fact
about the code is not executable, so nothing fails when the code moves underneath it
and the claim rots invisibly. `scripts/lint_docs.py` therefore binds the checkable
subset: a spec marked `Implemented` must have no unrecorded box and must carry its
`Decisions` section; `Depends on:` IDs must name real specs and form an acyclic graph;
`file.md#anchor` links must resolve to a real heading; specs must carry no instruction
that was already carried out; and math must render on GitHub. The rule generalizes:
**if a doc claim about code cannot be checked mechanically, either make it checkable
or leave it out.** Counts, module paths restated from memory, and prose duplicating a
table are the usual offenders.

**Math renders through GitHub's Markdown first.** GitHub treats a backslash before
ASCII punctuation as a Markdown escape and drops the backslash before MathJax runs, so
spacing control symbols render as literal punctuation inside formulas. Control words
(`\quad`, `\sum`) are unaffected. Spacing is cosmetic: delete it rather than reach for
a workaround. Inline math must not start or end with a space, which can stop GitHub
parsing the span as math at all.

### Structure

1. **One source per claim.** A document is either a **source**, which owns the claims
   it makes, or a **derived reading**, which owns nothing, says so in a stamp at the
   top, and links the source behind every load-bearing sentence. A source never
   restates another source. A derived reading may restate anything, because the stamp
   says which copy wins. Decisions go in `docs/decisions/` (why); work orders and
   module docs describe what.
2. **Every canonical section follows the same fixed skeleton**, ending in a worked
   example tied to a golden oracle. The worked example is mandatory: it is how a stuck
   reader self-debugs by recomputing.
3. **Justify, do not assert.** Each non-obvious step earns its why; theory claims are
   pinned to a verified chapter, never cited from memory.
4. **Lead with the correctness trap.** State the failure mode before the mechanics.
5. **lint: every canonical doc opens with a purpose line and an `*Assumes:*` line.**
   Name what the doc takes as given and link there. Point to prerequisites; do not gate
   on the reader's background. A closing footer naming where the document's reasoning
   lives is good practice on top of this, not instead of it.
6. **No cold jargon.** Define or link any term or symbol at first use.
7. **If it is spatial, draw it.** One small SVG beats a dense paragraph.
8. **lint: a section says what is true now, never how it got that way.** When a decision
   changes a section, rewrite it as though it had always read that way and put the
   reasoning in `docs/decisions/`. Do not annotate it in place beside the old reading.
   Retrospective phrasing belongs to the decision record and nowhere else;
   `scripts/lint_docs.py` holds the list and gates it everywhere but there.

   Rewriting is where clarity outranks brevity most sharply: the aim is the message, and
   the compression comes after. A section rewritten short and unclear has to be rewritten
   again.

   Rewriting is where clarity outranks brevity most sharply: aim at the message, compress
   afterwards. A section rewritten short and unclear has to be rewritten again.

   **A substantial edit is a rewrite, not an annotation.** Compacting an annotated
   section keeps every kind of content already in it and only makes it denser. Rewriting
   starts from what the section is *for* and drops whatever serves something else. Two
   triggers, either sufficient: a section grows by more than about half while being
   edited, or an edit adds a sentence narrating what the document said before.

   The cost of getting this wrong is not one clumsy paragraph. Each annotation is
   defensible by itself, so nothing stops the next one, and the document accretes its own
   edit history until a reader has to reconstruct the current design from a changelog.

   Exempt, because they state current status rather than history: marking a section as
   describing unbuilt work, and CLAUDE.md's Overrides section, where a silently deleted
   rule is indistinguishable from a forgotten one.

### Prose mechanics

8. **lint: no em dashes.** Banned outright in committed docs, enforced per line. Use a
   colon, semicolon, comma, period, or parentheses, and vary the device so the prose
   does not settle into one substitute. A project with an archive it never rewrites
   should decline this rather than carry a rule it breaks everywhere.
9. **lint: one load-bearing claim per sentence; files stay under the line cap.** Push
   qualifiers into the next sentence rather than nesting three asides. Split a file
   that outgrows the cap: agents read whole files, and a file that has to be split is
   usually two subjects. A file that grows by design goes in `LINE_CAP_EXEMPT`.
10. **No filler or tics.** Skip "it is worth noting" and "in essence", do not reach for
    a rule-of-three list every time, do not hedge. Plain words over flourish.
11. **lint: no self-positioning language in committed files.** The gated
    words are listed in `scripts/lint_docs.py`; strategy stays in the gitignored
    `planning/` log.
12. **lint: no bare release names in committed files.** Which releases exist, which one
    may end the project, and which is dropped first are decisions about the project
    rather than engineering in it, so they stay in `planning/` with the rest of the
    strategy. A committed file names the gate or the spec it means. Phase IDs are not
    release names and stay legal: `R2.1` passes, a bare `R2` does not. <!-- lint-ok -->
13. **Reader confusion is data.** When someone trips on a passage, capture the fix as a
    glossary gotcha or an FAQ entry, not a one-off reply.
14. **Anti-patterns are explicit:** say what not to do. Agents and readers both follow
    that well.
