# Tokenized Gold Statistical Arbitrage

Analysing Statistical Arbitrage on Tokenized Gold Assets and Gold Futures and Comparing Results of these Arbitrage Strategies With Gold Returns


This project explores whether the spread between tokenized gold products and gold futures exhibit a statistically robust mean reverting relationship that can be traded profitably. 

The analysis focuses on the following assets PAXG, XAUT, COMEX Gold Futures and Micros (rolling front month contracts), and evaluates whether spread-based signals remain economically meaningful before and after accounting for beta adjustments and execution cost considerations.

## Pairwise Correlation & Cointegration Analysis

Correlation alone doesn't justify a pairs trade; two assets can move together without their spread ever reverting. So each pair is tested in two steps:

1. **Correlation** – a quick check of how closely the assets co-move.
2. **Engle-Granger cointegration test** – regresses one asset on the other and tests whether the residuals (the spread) are stationary.

The null hypothesis is that a pair has **no** stable long-run equilibrium. If the test rejects it at the 5% level ($p < 0.05$), the spread is treated as mean-reverting and the pair is considered tradeable.

The null hypothesis is that a pair has **no** stable long-run equilibrium. If the test rejects it at the 5% level ($p < 0.05$), the spread is treated as mean-reverting and the pair is considered tradeable.

![Correlation & Cointegratino Matrices](corr-coint-matrices_black.png)

Key result: All pairs aree highly correlated and cointegration is confirmed

## Normalised Spreads: Preliminary Analysis

Before formal testing, the spreads are plotted to check for mean reversion visually. Each spread is defined as:

$$\text{spread} = A - \beta B$$

where $\beta$ is the hedge ratio from regressing asset $A$ on asset $B$. The plot shows the raw spread, the beta-adjusted spread, and its z-score. Both spreads oscillate around a stable level, and the beta-adjusted spread shows larger deviations.

![Raw spread, beta-adjusted spread and z-score](spread_bspread_zscore_plot_white.png)

## Pairwise Stationarity Analysis

The ADF and KPSS tests check whether the visual mean reversion is statistically real. They test opposite null hypotheses: ADF assumes the spread is non-stationary (has a unit root), while KPSS assumes it is stationary. If ADF rejects its null and KPSS fails to reject, the spread is treated as stationary and tradeable with z-score signals. If ADF fails to reject and KPSS rejects, the spread is non-stationary and offers no reliable arbitrage signal. Mixed results, where both tests reject or neither does, are treated as inconclusive.

![ADF and KPSS results for each spread](stationarity_plots_white.png)

## Threshold Optimisation: Zeng & Lee (2014)

Rather than picking z-score entry and exit levels by hand, thresholds are derived from the spread's dynamics. Following Zeng & Lee (2014), the spread is modelled as an Ornstein-Uhlenbeck (OU) process, and the entry and exit levels are chosen to maximise expected return per unit time after transaction costs. The surface below shows how that objective varies across threshold choices, with the peak marking the optimal pair.

![Expected return per unit time across entry and exit thresholds](ou_threshold_optimisation_surface.png)

## Bid-Ask Spread & Slippage Modelling

The backtest currently assumes a flat 20 bps round-trip cost. Real execution costs vary with liquidity and market conditions, so costs are being modelled per trade in two parts: the bid-ask spread, and the extra slippage from trade size and volatility.

**Bid-ask spread: Corwin & Schultz (2012).** The spread is estimated from daily high and low prices, so no quote data is needed. The Abdi & Ranaldo (2017) estimator may replace it later as is more customary with the naive slippage model. For consecutive days $t$ and $t+1$:

$$\beta = \sum_{j=0}^{1}\left[\ln\frac{H_{t+j}}{L_{t+j}}\right]^2, \qquad \gamma = \left[\ln\frac{H_{t,t+1}}{L_{t,t+1}}\right]^2$$

$$\alpha = \frac{\sqrt{2\beta}-\sqrt{\beta}}{3-2\sqrt{2}} - \sqrt{\frac{\gamma}{3-2\sqrt{2}}}, \qquad S = \frac{2\left(e^{\alpha}-1\right)}{1+e^{\alpha}}$$

Here $H_{t,t+1}$ and $L_{t,t+1}$ are the high and low over both days combined. Negative estimates of $S$ are set to zero.

**Slippage.** The spread estimate is combined with current volatility and the participation rate $\pi = Q / \text{ADV}$, where $Q$ is the trade volume and ADV is average daily volume. The cost per side is:

$$c_t = \frac{S_t}{2} + \eta\,\sigma_t\sqrt{\pi_t}$$

The first term is the cost of crossing half the spread. The second is market impact, which grows with volatility $\sigma_t$ and with trade size relative to normal volume. The parameter $\eta$ scales the impact. The square-root form means doubling trade size raises impact by about 41% rather than 100%.


### Trade Dashboard

The dashboard breaks down every trade from the backtest: entries and exits, holding periods, and returns net of the assumed 20 bps round-trip cost.

![Trade-level returns, holding periods and cumulative P&L](detailed_trade_analysis_dashboard.png)

**Key results:** Over 4 years, 35 trades returned 48.3% with a Sharpe ratio of 2.40 and a maximum drawdown of 2.5%. Buy-and-hold gold returned more (87%) but with far higher risk: a Sharpe of 1.27 and a 30% drawdown. The strategy trades raw return for much smoother, market-neutral performance. Buy-and-hold figures exclude carry.

## Interpretation

These results are not proof of a reliable profit source. With only 35 trades, the Sharpe ratio is still just a noisy estimate.

## Future Work

**Back-adjusted futures data.** The futures series currently come from yfinance's continuous front-month contracts. These have price jumps at each roll date that can show up as false spread moves. The plan is to build the series by hand from one contract per year and apply Panama back-adjustment: at each roll, the price gap between the old and new contract is added to all earlier prices, which removes the jump while keeping price changes intact.

**Dynamic hedge ratio.** A Kalman filter will replace the rolling regression for estimating $\beta$, letting the hedge ratio update continuously as the relationship between the assets shifts.