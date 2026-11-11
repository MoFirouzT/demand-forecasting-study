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
