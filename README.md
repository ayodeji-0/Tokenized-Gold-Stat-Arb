# Tokenized Gold Statistical Arbitrage

Analysing Statistical Arbitrage on Tokenized Gold Assets and Gold Futures and Comparing Results of these Arbitrage Strategies With Gold Returns


This project explores whether tokenized gold products and gold futures exhibit statistically robust mean-reverting relationships that can be traded as a pairs or spread strategy. 

The analysis focuses on assets such as PAXG-USD, XAUT-USD, MGC=F and GC=F, and evaluates whether spread-based signals remain economically meaningful before and after accounting for beta adjustments and execution cost considerations.

## Pairwise Correlation & Cointegration Analysis

The empirical approach is built around the null hypothesis that the pairs do not share a stable long-run equilibrium. To evaluate this, pairwise correlations are computed, then Engle-Granger cointegration tests to the spread between each asset pair. If the residuals of the spread regression are stationary and the cointegration test rejects the null of no cointegration at conventional significance levels (for example, p < 0.05), that is evidence in favour of a mean-reverting relationship rather than mere contemporaneous co-movement. In other words, the strategy is not being justified by correlation alone; it requires the spread itself to behave like a statistically stable, reverting process.

![Correlation & Cointegratino Matrices](https://github.com/ayodeji-0/Tokenized-Gold-Stat-Arb/blob/main/corr-coint-matrices_black.png)

Key result: All pairs aree highly correlated and cointegration is confirmed

## Pairwise Stationarity Analysis

The project also applies ADF and KPSS tests to the spread series. ADF tests the null of a unit root (non-stationarity), while KPSS tests the null of stationarity. Taken together, these tests help distinguish between a temporary mispricing process and a genuinely stable spread relationship. If the ADF rejects non-stationarity and the KPSS fails to reject stationarity, the evidence is consistent with a mean-reverting spread that can be normalized with z-scores and traded systematically. Conversely, if both tests point away from stationarity, the spread may not offer a robust arbitrage signal.

![Stationarity Analysis Plots](https://github.com/ayodeji-0/Tokenized-Gold-Stat-Arb/blob/main/stationarity_plots_white.png)

# EDA, Normalised Spread analysis


### Correlation and cointegration

![Correlation / cointegration matrix](corr-coint-matrices_black.png)

![Correlation / cointegration matrix (white theme)](corr-coint-matrices_white.png)

### Spread and z-score analysis

![Spread and z-score plot](spread_bspread_zscore_plot.png)

![Spread and z-score plot (black theme)](spread_bspread_zscore_plot_black.png)

![Spread and z-score plot (white theme)](spread_bspread_zscore_plot_white.png)

### Stationarity and threshold diagnostics

![Stationarity analysis](stationarity_analysis.png)

![Stationarity test plot](stationarity_tests_plot.png)

![Threshold optimisation surface](ou_threshold_optimisation_surface.png)

### Trade dashboard

![Detailed trade analysis dashboard](detailed_trade_analysis_dashboard.png)

### Additional matrix summary

![Matrix summary](matrices_plot.png)

## Interpretation

The project does not treat the strategy as a guaranteed profit engine. Rather, it offers evidence that gold-linked products can share a mean-reverting spread relationship under certain conditions. The strongest takeaway is that the relationship is present enough to justify further testing with realistic execution assumptions, cost modelling, and out-of-sample validation.

This makes the repository a useful starting point for systematic relative-value work in tokenized gold, gold futures, and related commodity-linked assets.

## Notes

The charts in this folder are the visual outputs of the analysis. The notebooks in the same directory contain the underlying computation, and the CSV outputs provide trade-level detail for more granular review.



