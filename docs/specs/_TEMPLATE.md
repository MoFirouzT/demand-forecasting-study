# Spec &lt;ID&gt;: &lt;Title&gt;

**Status:** Draft | Approved | Implemented
**Release:** &lt;label, or none&gt;  **Depends on:** &lt;prior unit IDs, or none&gt;

## Objective
&lt;one sentence: what this unit delivers&gt;

## Motivation
&lt;optional; include when the unit is not obviously needed, or when it closes a loop
an earlier one left open. State the question, not the solution.&gt;

## Canonical reference
&lt;which section(s) of the source-of-truth document this implements, or "n/a, nothing
new"&gt;

## Governing reference
&lt;optional; the published source this unit's theory rests on, recorded in
`references.md`. Standard technique needs none, and saying so explicitly beats
inventing one. Never cite from memory: verify edition and section first.&gt;

## Design sketch
&lt;optional; the construction in house notation, for a unit whose shape is not
obvious from the objective&gt;

## Parameters / configuration
&lt;concrete values for this unit and where they are configured&gt;

## Interfaces
&lt;function signatures, request/response schema, data schema; omit if none&gt;

## Layering
&lt;optional; which contracts this unit touches&gt;

## Build tasks
- [ ] &lt;task&gt;

## Golden oracles
| # | inputs | expected output | why this case |
|---|--------|-----------------|---------------|
| 1 | &lt;…&gt; | &lt;…&gt; | &lt;what it pins down&gt; |

## Property tests
- &lt;invariant&gt;

## Bar for better (set before running)
&lt;for a comparison: the measure, the two sides, and what counts as better, e.g. "the
bootstrap interval of the WRMSSE difference excludes zero". For a reproduction: the
published score and the tolerance. A result that misses the bar is recorded as a null,
never re-scored against a new bar.&gt;

## Acceptance gate

*Blocks:* &lt;what this gate blocks&gt;. Every box must pass.

- [ ] &lt;condition&gt;

Record a box only against evidence, with the measured value beside it. A box has
three states: `- [x]` ran and passed, `- [!]` ran and did not pass (or was conditional
on something that did not happen), and `- [ ]` no record either way. A spec whose
**Status** is `Implemented` may carry no `- [ ]`; `scripts/lint_docs.py` enforces that,
because "we meant to tick it" and "it passed" are indistinguishable six weeks later. A
`- [!]` must say what happened on the line, so a gate that says no is recorded as a
result rather than leaving a finished unit with no way to mark it.

## Measured results
&lt;optional; what this unit actually found, when the finding is the point. The
one-line version goes in the ledger row.&gt;

## Out of scope
- &lt;item&gt;

## Decisions

Local design, interface, and build decisions only. Roadmap and positioning
questions stay in the gitignored `planning/` log, never here.

Pose each with a proposed answer, then resolve it in place at review, keeping the
proposal so the section becomes the decision trail rather than a list of questions
answered elsewhere. This is where a later reader is sent for why, so it is the one
section that must not be trimmed on the way to green.

Promote a decision to a record in `docs/decisions/` only when it is cross-cutting and
expensive to reverse, and leave a pointer here.

- &lt;question&gt; *Proposed:* &lt;recommendation&gt;.
- &lt;question&gt; **Resolved:** &lt;decision + rationale&gt; (YYYY-MM-DD).
