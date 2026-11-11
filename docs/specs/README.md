# Work orders and the ledger

Each component of this project was built from a frozen work order in this directory:
scope, interfaces, and the test contract, reviewed before any code was written. This
file indexes them and records what each one concluded.

*Assumes: the capability map in [architecture.md](../architecture.md); the workflow in
[CLAUDE.md](../../CLAUDE.md) §3.*

---

## The unit and the label

The unit of work here is the **component**. Delivery labels, if this project uses them,
record the order things were built and are not architecture; reader-facing documents
name capabilities instead.

Filenames name their subject, so a capability delivered over several units has one work
order, and a capability whose later units answered a different question has several.

| Capability | Work orders | Labels | Packages |
| --- | --- | --- | --- |
| | | | |

## In flight

Approved-but-unbuilt and draft work orders are listed separately because they carry no
ledger row: a row records what was found, and an unbuilt unit has found nothing.

| Work order | Label | Status | What it proposes |
| --- | --- | --- | --- |
| [evaluation-harness](evaluation-harness.md) | none | Draft | Score forecasts as the protocol defines: backtest, demand classes, metrics, order simulation, bootstrap |

---

## The ledger

One row per component, oldest first. Dates are the implementing commit's date. The
**finding** column is the point: what it established, including when the answer was
"no". This ledger is the project's history, which is why the decision records do not
have to be.

| Component | Date | Capability | What changed | Finding |
| --- | --- | --- | --- | --- |
| | | | | |

---

## Where the detail lives

This ledger is deliberately one line each. Every unit's design detail, its
resolved decision trail, and what it ruled out are in its own spec, under
**Decisions**, which is where a reader should go for the reasoning.

## Adding one

1. Copy [`_TEMPLATE.md`](_TEMPLATE.md); fill scope, interfaces, and the test contract.
   Add it to **In flight** above, which is where a spec lives until it is green.
2. Human review and approval, before any implementation.
3. Write the golden and property tests first, failing.
4. Implement to green.
5. Move the work order from **In flight** to a ledger row, and update
   [STATE.md](../STATE.md).

Resolve each open question in place, keeping the proposal, so the section becomes the
decision trail rather than a list of questions that were answered elsewhere.
