# Decision records

Decisions that are expensive to reverse, each the stable answer to "why is it like
this?". Cheaper to write once than to keep re-deriving, and they stop a future
contributor from quietly reverting a considered choice while improving the code.

*Assumes: the capability map in [architecture.md](../architecture.md).*

**This directory is curated.** Files are named by subject, with no numbering, so a
decision can be merged into a related one or retired without leaving a gap. What lives
here is what governs the code today, and a record that supersedes another names what it
replaced and why the old reading was wrong. Nothing is preserved in a state known to be
false.

History is not this directory's job: the build record is the
[ledger](../specs/README.md), and the reasoning trail for any delivery unit is in its
work order under Decisions. Measurements are different again: a study in
[`studies/`](../studies) is never rewritten and never retired, because evidence does not
expire. See the plugin's own record, *Records are curated; measurements are durable*.

---

## By capability

**&lt;capability&gt;**

- [&lt;decision&gt;](&lt;slug&gt;.md): one line saying what it decides and why it matters.

---

## Writing one

Create `<short-slug>.md` from the template below when a decision is locked, and add it
to the index above under its capability.

A decision earns a file here when reversing it would be expensive: it would invalidate
a gate, force a re-derivation, or change a published number. A conventional choice
with an obvious default does not, and neither does a refactor. If the reasoning fits
in a sentence, put that sentence where the code is instead.

**Status** is `Accepted`, `Superseded`, or `Rejected`. A rejected decision is kept only
when the rejection itself matters, that is, when someone would otherwise re-propose it.

**When a decision changes:** revise the file in place and date the change in the front
matter, or fold it into the record that supersedes it. Never leave two files
disagreeing about what governs the code.

## Template

```markdown
# <what was decided, as a statement>

**Status:** Accepted | Superseded | Rejected
**Date:** YYYY-MM-DD

## Context
The problem, the constraints, what was considered.

## Decision
The chosen approach, stated as concisely as possible.

## Consequences
What gets easier, what gets harder, and which check (CI, lint, a golden test)
enforces this mechanically.

## Failure mode
How this could go wrong in practice, and the signal that would reveal it.

## Alternatives considered
The other options and why they were rejected.
```

**Failure mode** is the section that is not standard practice, and it is the one worth
keeping: it forces a decision to name what would falsify it.
