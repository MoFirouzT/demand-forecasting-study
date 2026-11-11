# Evaluation protocol

What every result in this study is measured against: the forecasting task, the backtest,
the demand classes, the metrics, and the bars for "better". The evaluation code in
`dfstudy.evaluation` must agree with this document.

*Assumes: the [glossary](glossary.md).*

---

## The task

- Forecast daily unit sales for each item in each store of the M5 data, 28 days ahead.
- The forecast feeds one decision: how many units to stock for each item, store and day.
- A study on another dataset (H&M, FreshRetailNet-50K, synthetic data) states its own
  granularity and horizon in its spec.

## The decision

- Each morning, for each item and store, order up to a target stock level S. The order is S
  minus the units left from the previous day, or zero if that is negative.
- S is the q-quantile of that day's demand forecast, rounded up to an integer.
- q = c_u / (c_u + h), where c_u is the cost of one unit of lost demand and h the cost of
  holding one unit overnight.
- Demand above the stock on hand is lost. Unsold units stay for the next day.
- Lead time is zero. Stock is zero before the first day of each test window.
- Order cost over a window: c_u times the lost units plus h times the units held overnight,
  summed over its days.
- The data carries no costs, so q is swept over 0.5, 0.8, 0.9, 0.95 and 0.99, which is
  c_u : h of 1, 4, 9, 19 and 99.
- The rule above applies to M5. A study on perishable goods (FreshRetailNet-50K) states in
  its spec whether leftovers are discarded, in which case order cost reduces to pinball loss
  at q.

## The backtest

- Full M5: reported origins at days 1885, 1913 and 1941, each followed by a 28-day test
  window. The last window is M5's final window.
- Tuning origins at days 1829 and 1857. Every choice about a method (hyperparameters,
  features, which variant) is made on these alone.
- One-store subset: reported origins at days 1829, 1857, 1885, 1913 and 1941; tuning origins
  at 1773 and 1801.
- Every model, scale and demand-class label is fitted on data up to its origin only.

## Demand classes

- Each series gets one class per origin, from its sales between its first sale and the
  origin ([Syntetos, Boylan & Croston, 2005](https://doi.org/10.1057/palgrave.jors.2601841)).
- ADI = days in that span / days with a sale.
- CV² = (σ_z / μ_z)², where z is a day's sales on days with a sale, and σ_z divides by
  their count.
- Smooth: ADI < 1.32 and CV² < 0.49. Erratic: ADI < 1.32 and CV² ≥ 0.49.
  Intermittent: ADI ≥ 1.32 and CV² < 0.49. Lumpy: ADI ≥ 1.32 and CV² ≥ 0.49.
- A series with no sale before the origin is classed "no history" and reported apart.

## Metrics

Every metric is computed per series and origin, then reported overall and per demand class.

Point forecast (the mean):

- WRMSSE, as in M5, overall only. RMSSE per series = √(mean squared error over the window /
  mean squared one-step naive difference from first sale to origin).
- Per class: RMSSE averaged over the class's series, weighted by dollar sales in the 28 days
  before the origin.
- Bias = Σŷ / Σy − 1 over the series and days in the group.
- WAPE = Σ|y − ŷ| / Σy, as a secondary figure. WAPE is lowest for the median, not the mean.

Quantiles:

- Pinball loss at each q of the decision sweep, divided per series by the mean absolute
  one-step naive difference from first sale to origin
  ([M5 uncertainty competition](https://doi.org/10.1016/j.ijforecast.2021.10.009)).
  Series count equally.
- CRPS ≈ (2/99) Σ L_q over q = 0.01, …, 0.99, scaled the same way
  ([Gneiting & Raftery, 2007](https://doi.org/10.1198/016214506000001437)).
- Coverage at each q: the share of item-days with y ≤ ŷ^(q). On count data a correct
  q-quantile covers at least q.
- Every method outputs a mean and the 99 quantiles.

Decision:

- Order cost and fill rate (units sold / units demanded) from the order simulation.
- One day, leftovers discarded: q = c_u / (c_u + c_o), where c_o is the cost of one unsold
  unit, and (c_u + c_o)·L_q(y, S) = c_u(y − S)⁺ + c_o(S − y)⁺, where (x)⁺ = max(x, 0). The
  day's order cost is pinball loss at q, scaled.

A series whose scale is zero is left out of the scaled metrics, and the count left out is
reported.

## The questions

1. On full M5, how do pretrained models that take covariates (Chronos-2, TiRex-2) compare
   with a competition-grade LightGBM, by WRMSSE, pinball loss and order cost, with bias
   reported separately for intermittent items?
2. How much better than the rule-of-thumb heuristics is each method, per demand class?
3. Do methods rank the same by accuracy as by order cost?

## Reproductions

A reproduction scores a published method on the window its published score comes from:
M5's final 28 days (days 1942 to 1969), with the official WRMSSE weights. Kaggle's files stop
at day 1941; the final window's sales and the weights come from Nixtla's mirror of the
released M5 data (`scripts/download_data.py`).

- Seasonal naive and exponential smoothing: WRMSSE within 2% of M5's published benchmark
  scores.
- LightGBM counts as competition-grade when its WRMSSE is at most 0.576, the 50th-place M5
  score. For scale: the winner scored 0.520 and the best benchmark (bottom-up exponential
  smoothing, ES_bu) 0.671.
- A reproduction that misses its tolerance is a bug to find before any comparison uses that
  method.

## Bars for "better"

- Method A beats method B on a measure when the 95% bootstrap interval of their difference
  excludes zero. Resampling is by series, 1,000 draws, over all series and origins.
- An interval that includes zero is a tie, reported as one.
- Accuracy and order cost rank methods differently when the best method by WRMSSE is not
  the best by order cost and their order-cost difference passes the bar above.
- Each bar applies only to the pairs named in a study's spec before it runs. The intervals
  are not corrected for multiple comparisons.
