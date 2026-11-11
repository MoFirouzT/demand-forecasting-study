# Spec: Evaluation harness

**Status:** Draft
**Release:** none  **Depends on:** none

## Objective

Score any method's forecasts on M5-shaped arrays as `docs/protocol.md` defines: backtest
windows, demand classes, accuracy metrics, the order simulation and bootstrap intervals.

## Canonical reference

`docs/protocol.md`: The decision, The backtest, Demand classes, Metrics, Bars for "better".

## Governing reference

- WRMSSE and its scale: [M5 accuracy competition](https://doi.org/10.1016/j.ijforecast.2021.11.013).
- Scaled pinball loss: [M5 uncertainty competition](https://doi.org/10.1016/j.ijforecast.2021.10.009).
- Demand classes: [Syntetos, Boylan & Croston, 2005](https://doi.org/10.1057/palgrave.jors.2601841).
- CRPS as twice the integral of pinball loss over q: [Gneiting & Raftery, 2007](https://doi.org/10.1198/016214506000001437).

## Design sketch

Arrays are indexed by series (rows) and day (columns). Column `j` is M5 day `j + 1`, so an
origin at day `t` gives:

- history: `sales[:, :t]`, days 1 to t
- actual: `sales[:, t:t + 28]`, days t + 1 to t + 28

Every function that fits something to the data (class, scale, weight) receives the history
only. The harness does the slicing, so no caller can pass it the test window by mistake.

"From first sale" means from the first day with a sale up to the origin, per series. The
demand class, the RMSSE scale and the pinball scale all use that span.

The order simulation, per series, with stock zero before the first day:

- S_t = ⌈forecast q-quantile for day t⌉
- order_t = max(S_t − stock_t, 0); on hand = stock_t + order_t
- sold_t = min(y_t, on hand); lost_t = y_t − sold_t
- held_t = on hand − sold_t, which is stock_{t+1}
- cost = c_u · Σ lost_t + h · Σ held_t, with h = 1 and c_u = q / (1 − q)
- fill rate = Σ sold / Σ y over the group

The last day's leftovers count as held overnight.

## Parameters / configuration

Constants in `dfstudy.evaluation.backtest`:

- `HORIZON = 28`
- full M5: reported origins `(1885, 1913, 1941)`, tuning origins `(1829, 1857)`
- one-store subset: reported origins `(1829, 1857, 1885, 1913, 1941)`, tuning origins
  `(1773, 1801)`

Constants in `dfstudy.types` and `dfstudy.evaluation.metrics`:

- quantile levels: 0.01, 0.02, …, 0.99 (99 levels)
- decision sweep: q in (0.5, 0.8, 0.9, 0.95, 0.99)
- WRMSSE weight window: the 28 days before the origin
- class cut-offs: ADI 1.32, CV² 0.49
- bootstrap: 1,000 draws, 95% interval, seed set by the caller

## Interfaces

`dfstudy.types` (imported by both `dfstudy.models` and `dfstudy.evaluation`):

```python
QUANTILE_LEVELS: np.ndarray  # shape (99,), 0.01 to 0.99

@dataclass(frozen=True)
class Forecast:
    mean: np.ndarray       # (n_series, horizon)
    quantiles: np.ndarray  # (n_series, horizon, 99); raises if not non-decreasing in q
```

`dfstudy.evaluation`:

```python
# backtest.py
def split(sales: np.ndarray, origin: int, horizon: int = HORIZON) -> tuple[np.ndarray, np.ndarray]

# classes.py
def adi_cv2(history: np.ndarray) -> tuple[np.ndarray, np.ndarray]     # per series; NaN with no sale
def demand_class(history: np.ndarray) -> np.ndarray                   # str labels per series

# metrics.py
def rmsse(history, actual, mean) -> np.ndarray                        # per series; NaN if scale is 0
def wrmsse(history, actual, mean, revenue_history, hierarchy: pd.DataFrame,
           levels: Sequence[tuple[str, ...]] = M5_LEVELS) -> float
def bias(actual, mean) -> float
def wape(actual, mean) -> float
def pinball(actual, quantile_forecast, q: float) -> np.ndarray        # per series, unscaled
def scaled_pinball(history, actual, quantile_forecast, q) -> np.ndarray
def crps(history, actual, quantiles) -> np.ndarray                    # per series, scaled
def coverage(actual, quantile_forecast) -> float

# decision.py
@dataclass(frozen=True)
class OrderResult:
    sold: np.ndarray; lost: np.ndarray; held: np.ndarray  # (n_series, horizon)
def simulate_orders(actual, quantile_forecast) -> OrderResult
def order_cost(result: OrderResult, q: float) -> np.ndarray           # per series, in units of h
def fill_rate(result: OrderResult) -> float

# bootstrap.py
def bootstrap_difference(stat_a: Callable[[np.ndarray], float],
                         stat_b: Callable[[np.ndarray], float],
                         n_series: int, n_draws: int = 1000,
                         seed: int = 0) -> tuple[float, float]
```

- `revenue_history` is units times sell price, same shape as the history; `wrmsse` uses its
  last 28 columns.
- `hierarchy` has one row per series with columns `item_id`, `dept_id`, `cat_id`,
  `store_id`, `state_id`. `M5_LEVELS` lists M5's 12 levels as tuples of those columns;
  the empty tuple is the total.
- A `stat` takes an array of drawn series indices and returns the measure over those
  series. Both methods get the same draws.

## Layering

- `dfstudy.types` imports neither `dfstudy.models` nor `dfstudy.evaluation`.
- The independence contract between `dfstudy.models` and `dfstudy.evaluation` is
  unchanged.

## Build tasks

Each is one increment, reviewed before the next.

- [ ] Add `numpy` and `pandas` to the dependencies.
- [ ] `dfstudy.types`: `QUANTILE_LEVELS`, `Forecast`.
- [ ] `backtest.py`: constants, `split`.
- [ ] `classes.py`: `adi_cv2`, `demand_class`.
- [ ] `metrics.py`, point part: the two scales, `rmsse`, `wrmsse`, `bias`, `wape`.
- [ ] `metrics.py`, quantile part: `pinball`, `scaled_pinball`, `crps`, `coverage`.
- [ ] `decision.py`: `simulate_orders`, `order_cost`, `fill_rate`.
- [ ] `bootstrap.py`: `bootstrap_difference`.

## Golden oracles

| # | inputs | expected output | why this case |
|---|--------|-----------------|---------------|
| 1 | `0,0,5,0,0,0,5,0,0,5` | ADI 8/3, CV² 0, intermittent | equal sizes, sparse sales |
| 2 | `0,0,1,0,0,0,12,0,0,2` | ADI 8/3, CV² 0.9867, lumpy | sizes vary, sparse sales |
| 3 | `2,9,0,1,8,2,0,10,1,7` | ADI 1.25, CV² 0.52, erratic | μ_z counts sale days only (40/8) |
| 4 | `0,0,0,5,5,0,5,5` | ADI 1.25, CV² 0, smooth | leading zeros dropped; with them ADI = 2, intermittent |
| 5 | `0,0,0,0` | no history | no sale before the origin |
| 6 | sales 2 × 40, origin 6 | history columns 0–5 (days 1–6), actual columns 6–33 (days 7–34) | the day-to-column mapping |
| 7 | history `1,3,2,4`, actual `3,3`, mean `2,4` | RMSSE √(1/3) = 0.5774 | scale = mean squared step, 3 |
| 8 | history `0,0,1,3,2,4`, same actual and mean | RMSSE 0.5774 | the 0 → 1 step before the first sale is not in the scale |
| 9 | series a as #7; b: history `2,2,4,4`, actual `4,6`, mean `4,4`; revenue a 10/day, b 30/day; levels: bottom and total | bottom 0.25·0.5774 + 0.75·1.2247 = 1.0629; total 0.5774; WRMSSE 0.8201 | weights within a level, equal weight across levels, means add up the hierarchy |
| 10 | actual `0,0,0,3,0,0,1,0,0,0`; mean all 0, then all 0.4 | bias −1 and 0; WAPE 1.0 and 1.6 | the zero forecast wins on WAPE and fails on bias |
| 11 | y = 5, forecast 3, q = 0.9; y = 3, forecast 5, q = 0.9 | pinball 1.8; 0.2 | the two slopes |
| 12 | history `1,3,2,4`, actual `3,3`, 0.9-quantile `2,4` | scaled pinball 0.5 / (5/3) = 0.3 | the absolute scale |
| 13 | y = 5, all 99 quantiles 3, scale 1; and y = 3, all 5 | CRPS 2 in both | a point forecast's CRPS is its absolute error |
| 14 | actual `0,0,0,1,3`, quantile `0,0,1,1,1` | coverage 0.8 | ties count as covered |
| 15 | actual `2,6,1`, quantile `5,5,5` | held 3,0,4; lost 0,1,0; fill rate 8/9; cost at q = 0.9 is 9·1 + 7 = 16 | carry-over, a stockout, last-night holding |
| 16 | actual `1,1`, quantile `5,2` | order on day 2 is 0; held 4,3 | S below stock orders nothing |
| 17 | quantile `4.2`, `4.0` | S = 5, 4 | rounding up, and an integer stays itself |
| 18 | history `0,0,5,5,5` | scale 0; left out of scaled metrics; count 1 | zero-scale series |

## Property tests

- Leakage: changing any value at or after the origin changes no class label, no scale and
  no WRMSSE weight.
- A perfect mean forecast has RMSSE 0 for every series with a positive scale, and WRMSSE 0.
- For q = c_u / (c_u + c_o): (c_u + c_o) · pinball = c_u(y − S)⁺ + c_o(S − y)⁺.
- CRPS of a forecast whose 99 quantiles are equal is the scaled absolute error.
- Multiplying a series by a positive integer leaves its class unchanged.
- Order simulation: sold + lost = y; sold, lost and held are non-negative; fill rate is in
  [0, 1].
- Raising S on every day never lowers the fill rate.
- `Forecast` rejects quantiles that decrease in q.
- Bootstrap: a method against itself gives (0, 0); swapping the two methods negates the
  interval.

## Bar for better (set before running)

n/a: this unit compares no methods.

## Acceptance gate

*Blocks:* every experiment and the M5 EDA.

- [ ] All golden tests pass.
- [ ] All property tests pass.
- [ ] `uv run lint-imports` passes.
- [ ] `bootstrap_difference` with 1,000 draws on random 30,490 × 28 arrays, for a
  per-series mean, runs in under one minute on the laptop.

## Out of scope

- Loading M5 (its own spec, with the EDA).
- How a method that gives one number produces 99 quantiles (plan days 4–5).
- Reproduction checks against published scores.
- Quantile metrics at aggregate levels of the hierarchy.
- Plots and result tables.

## Decisions

- Data shape inside the harness. **Resolved:** NumPy arrays, series × days, plus a pandas
  table for the hierarchy; the maths stays vectorised and simple (2026-11-11).
- Where the forecast type lives. **Resolved:** `dfstudy.types`, imported by both sides,
  so the independence contract holds (2026-11-11).
- M5 loading in this unit. **Resolved:** no; golden tests run on hand-made arrays, and
  loading gets its own spec with the EDA (2026-11-11).
- Order cost scaling. *Proposed:* unscaled, summed in units of h, since it stands for
  money and a fast item's lost sales do cost more.
- WRMSSE bootstrap. *Proposed:* resample bottom series and recompute all 12 levels per
  draw, as the protocol's "by series" says; if that is too slow on full M5, revisit here
  before any WRMSSE comparison.
- Rounding S. *Proposed:* `ceil(x − 1e-9)`, so a quantile stored as 4.0000000001 gives 4.
