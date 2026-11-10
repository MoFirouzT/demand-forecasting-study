# CLAUDE.md - operating contract for this repo

Built under spec-first discipline, one component at a time. Read this file, then
`docs/STATE.md`, at the start of every session.

The method is the `project-discipline` skill: the rules, the document tiers, the
component workflow, the decision-record bar, and the working preferences. It is not
repeated here. This file holds only what is specific to this project, and the skill's
rules apply in full except where `## Overrides` below says otherwise.

## 1. Evaluation discipline (highest priority)

- Evaluation is defined in `docs/protocol.md`, the single source of truth.
  NEVER change what it defines without (1) updating `docs/protocol.md` in the same
  change and (2) updating or adding a golden test.
- Before editing `dfstudy.evaluation`, restate the relevant clause from
  `docs/protocol.md` and the invariant it must satisfy.
- **The correctness trap:** information from after the forecast origin reaching a model, a feature, a demand-class label or a scaling factor (series scales, WRMSSE weights). It improves every score silently and invalidates every comparison.
- The gates are `tests/golden/` (golden) and `tests/property/` (property). A
  failing gate means the spec or the code is wrong: surface it, do not suppress it.

## 2. Where things live

- **Tier 0 - `planning/` (GITIGNORED, never commit):** the plan, unbuilt roadmaps, and
  private reasoning. Read it for context; never copy its framing into a committed file.
- **Tier 1:** `README.md`, `docs/architecture.md`, `docs/history.md`, `docs/models/` (one
  card per model). All derived readings: each opens with a stamp naming its sources.
- **Tier 2:** `docs/protocol.md`, `docs/glossary.md`, `docs/references.md`,
  `docs/decisions/`, `docs/studies/` (one chapter per study, numbered like its
  `experiments/` folder). Numbers in a study come only from `results/`.
- **Tier 3:** `docs/specs/<subject>.md`, one per component; `docs/specs/README.md` is the
  ledger.

**Governing rule:** job-search reasoning (why this study exists for a CV, application
targets) never appears in a committed file.

**Writing:** committed docs follow `docs/conventions.md`, which is this project's own
charter and says which of its rules are machine-checked. Read it before writing docs.

**A substantial edit is a rewrite, not an annotation.** When a change alters what a
section means, rewrite the whole section so it reads as though it had always said that,
and put the reasoning in `docs/decisions/`. Never leave the old reading in place beside
the new one. This applies to `planning/` as much as to committed docs, and
`scripts/lint_docs.py` checks the phrasing in both. Two triggers, either one enough:

- A section grows by more than about half while being edited. Rewrite it whole before
  moving on; later is a separate task nobody scheduled.
- An edit adds a sentence about what the document used to say. That sentence is the
  reasoning, and the reasoning goes to the decision record.

Rewriting means asking what the section is *for* and dropping whatever serves something
else, not making the same material denser.

**Clarity outranks brevity.** Aim first at the message a reader who has seen none of the
surrounding work can take on one pass, then compress it. Never compress first and clarify
after: the author can still read their own meaning into broken text, so the break
survives. A short sentence that has to be asked about was not brief, it was incomplete.

## 3. Layering

`dfstudy.evaluation` and `dfstudy.models` never import each other, so no model can reach the scoring or test-window code. Checked by import-linter (`[tool.importlinter]` in `pyproject.toml`).

## 4. Commands

- env: `uv sync` (add `--group docs` for the site)
- test: `uv run pytest`
- layering: `uv run lint-imports`
- site: `uv run --group docs mkdocs serve`

- docs: `uv run python scripts/lint_docs.py` (writing charter)

## 5. Overrides

Rules from the `project-discipline` skill that this project deliberately does not
follow, each with the reason. This section is the only supported way to turn one off:
a rule that is silently ignored looks identical to a rule that was forgotten.

- None yet.

## 6. Guardrails (known failure modes)

- Do not code against a remote API schema from memory. Fetch and print a real sample
  first, then write code against the actual shape.
- Do not over-build. The spec's "out of scope" section is binding.
- After any refactor of `dfstudy.evaluation`, re-run the golden tests: they catch silent
  changes to meaning.
- Sales are not demand: stockouts censor what was observed. Never treat a zero during a
  stockout as zero demand.
- New items have no history (cold start); a model scored only on established series says
  nothing about them.
- Forecasts at different hierarchy levels must add up; report accuracy at each level.
- Every feature is an as-of value: known at the forecast origin, not later.
- Score at the decision level (fill rate, order cost) as well as on accuracy.
- Reproduction checks (a model's score against its published score) are experiments, not
  gates. Golden and property tests cover the evaluation code and the features only.
