# A history of demand forecasting methods

> **A derived reading.** Each claim links its primary source or textbook section. Where
> this page and a source disagree, the source wins.

How forecasting methods for item-level retail demand developed, one era at a time.

*Assumes: the forecast task in the [protocol](protocol.md#the-task).*

---

## 1. Classical local methods (1957 to 2011)

Each series gets its own model, fitted only to its own history.

Notation used throughout this era:

- $y_t$: sales on day $t$
- $\hat{y}_{t+h|t}$: the forecast for day $t+h$ made with data up to day $t$
- $h$: the horizon, how many days ahead

### Exponential smoothing

The forecast is a weighted average of past sales, with weights that shrink geometrically
with age ([FPP3 §8.1](https://otexts.com/fpp3/exponential-smoothing.html#sec-ses)). Simple exponential smoothing
tracks one quantity, the level:

$$\ell_t = \alpha y_t + (1-\alpha)\ell_{t-1}, \qquad \hat{y}_{t+h|t} = \ell_t$$

- $\ell_t$: the level, the estimate of typical sales after seeing day $t$
- $\alpha \in [0,1]$: the smoothing parameter
    - Near 1, the level follows real changes quickly and also chases noise; near 0, the
      reverse.
    - It is fitted by minimising one-step-ahead squared errors on the history.
- Expanding the recursion gives day $t-k$ the weight $\alpha(1-\alpha)^k$.

Holt (1957) added a smoothed trend and Winters (1960) a smoothed seasonal term; Brown
(1959) wrote the level-only method up for inventory control
([FPP3 ch. 8](https://otexts.com/fpp3/exponential-smoothing.html);
[Holt, reprinted 2004](https://doi.org/10.1016/j.ijforecast.2003.09.015);
[Winters](https://doi.org/10.1287/mnsc.6.3.324)). The additive Holt-Winters method
([FPP3 §8.3](https://otexts.com/fpp3/exponential-smoothing.html#sec-holt-winters)):

$$\ell_t = \alpha(y_t - s_{t-m}) + (1-\alpha)(\ell_{t-1} + b_{t-1})$$

$$b_t = \beta(\ell_t - \ell_{t-1}) + (1-\beta)b_{t-1}$$

$$s_t = \gamma(y_t - \ell_{t-1} - b_{t-1}) + (1-\gamma)s_{t-m}$$

$$\hat{y}_{t+h|t} = \ell_t + h b_t + s_{t+h-m(k+1)}$$

- $b_t$: the trend, the estimated change in the level per day
- $s_t$: the seasonal term for day $t$'s position in the cycle, how far that position
  sells above or below the level
- $m$: the cycle length, 7 for a weekly pattern; $s_{t-m}$ is the same position one cycle
  earlier
- $\beta, \gamma \in [0,1]$: smoothing parameters for the trend and the season (FPP3
  writes $\beta^{*}$ for the trend's)
- $k$: the integer part of $(h-1)/m$, so the forecast uses the latest estimate for each
  position

### ETS: exponential smoothing as a statistical model

[Hyndman et al. (2002)](https://doi.org/10.1016/S0169-2070(01)00110-8) added an explicit
error term. Error, Trend and Seasonal (ETS) are each none, additive or multiplicative; the
trend can also be damped. Simple exponential smoothing becomes ETS(A,N,N), additive error
with no trend and no season ([FPP3 §8.5](https://otexts.com/fpp3/exponential-smoothing.html#sec-ets)):

$$y_t = \ell_{t-1} + \varepsilon_t, \qquad \ell_t = \ell_{t-1} + \alpha\varepsilon_t, \qquad \varepsilon_t \sim \mathrm{N}(0, \sigma^2)$$

- $\varepsilon_t$: the error on day $t$, independent from day to day
- $\sigma$: the standard deviation of the errors, estimated from the history

The model gives two things the recursions lack:

- a likelihood, so parameters and the model form are chosen automatically
- a forecast distribution, Normal with centre $\ell_t$ and variance
  ([FPP3 §8.7](https://otexts.com/fpp3/exponential-smoothing.html#sec-ets-forecasting))

$$\sigma_h^2 = \sigma^2\left[1 + \alpha^2(h-1)\right]$$

Any quantile can be read from that distribution, including the order quantile in the
[protocol](protocol.md#the-decision). The variance grows with $h$ because each future
error moves the level by an unknown $\alpha\varepsilon$.

### Intermittent demand

Many retail series are mostly zeros. Plain smoothing drops after every zero run and jumps
after every sale.

[Croston (1972)](https://doi.org/10.2307/3007885) smooths two series separately
([FPP3 §13.2](https://otexts.com/fpp3/practical.html#sec-counts)):

$$\hat{q}_{i+1} = \alpha_q q_i + (1-\alpha_q)\hat{q}_i, \qquad \hat{a}_{i+1} = \alpha_a a_i + (1-\alpha_a)\hat{a}_i, \qquad \hat{y} = \frac{\hat{q}}{\hat{a}}$$

- $q_i$: the size of the $i$-th non-zero sale
- $a_i$: the number of days between sale $i-1$ and sale $i$
- $\alpha_q, \alpha_a$: smoothing parameters for sizes and intervals
- $\hat{y}$: an estimate of mean demand per day, the same for every horizon

Three known problems:

- It is biased upward ([Syntetos & Boylan, 2001](https://otexts.com/fpp3/practical.html#sec-counts)).
  The Syntetos-Boylan Approximation (SBA) multiplies the forecast by $1-\alpha_a/2$
  ([Syntetos & Boylan, 2005](https://doi.org/10.1016/j.ijforecast.2004.10.001)).
- It has no underlying statistical model, so no prediction intervals
  ([FPP3 §13.2](https://otexts.com/fpp3/practical.html#sec-counts)).
- It updates only on days with a sale, so an item that stops selling keeps its old
  forecast.

[TSB (Teunter, Syntetos & Babai, 2011)](https://doi.org/10.1016/j.ejor.2011.05.018)
smooths the probability of a sale every day instead:

$$\hat{p}_t = \beta o_t + (1-\beta)\hat{p}_{t-1}, \qquad \hat{y}_{t+h|t} = \hat{p}_t \hat{z}_t$$

- $o_t$: 1 if day $t$ had a sale, otherwise 0
- $\hat{p}_t$: the smoothed probability of a sale on a given day
- $\hat{z}_t$: the smoothed sale size, updated with $\alpha$ only on days with a sale
- $\beta$: the smoothing parameter for the probability

After $n$ days without a sale, $\hat{p}$ has shrunk by the factor $(1-\beta)^n$, so the
forecast decays toward zero.

### What the era leaves open

- ARIMA, the other classical family, models correlation between past values
  ([FPP3 ch. 9](https://otexts.com/fpp3/arima.html)). The M5 statistical benchmarks are
  exponential smoothing ([protocol](protocol.md#reproductions)).
- A local model learns a pattern such as a weekday effect separately for every series, from
  that series alone. A new or sparse item has too little history to learn it.
- A global model fits one function to all series, each divided by its own scale computed
  before the forecast origin. Global models can match the accuracy of local ones even on
  dissimilar series ([Montero-Manso & Hyndman, 2021](https://doi.org/10.1016/j.ijforecast.2021.03.004)).
  Era 2 begins there.
