# Helper function Bid-Ask Spread Estimator - Corwin Schultz (2012)
# *todo make class out of spread estimator
'''
S = 2 * (exp(alpha) - 1) / (1 + exp(alpha))
Where:
alpha = (sqrt(2 * beta) - sqrt(beta)) / k - sqrt(gamma / k)
beta = (log(H_2d / L_2d))^2
gamma = (log(H / L))^2
k = 3 - 2 * sqrt(2) ≈ 0.1715728752538099

S is the estimated bid-ask spread
H is the high price
L is the low price
'''

def cs_spread_estimator(df: pd.DataFrame, k: float = 3 - 2 * np.sqrt(2), abs: bool = False, bps: bool = False, pips: bool = False, target: tuple[bool, float] = (False, 20.0)) -> pd.Series:

    df = df[['High', 'Low']].dropna()
    df = df[(df['High'] > 0) & (df['Low'] > 0)]

    high = df['High']
    low = df['Low']

    # 2-day high/low
    high_2d = pd.concat([high, high.shift(1)], axis=1).max(axis=1)
    low_2d = pd.concat([low, low.shift(1)], axis=1).min(axis=1)

    beta = (np.log(high_2d / low_2d))**2
    gamma = (np.log(high / low))**2

    # align
    valid = beta.notna() & gamma.notna()
    beta = beta[valid]
    gamma = gamma[valid]

    alpha = (
        (np.sqrt(2 * beta) - np.sqrt(beta)) / k
        - np.sqrt(gamma / k)
    )

    alpha = np.maximum(alpha, 0)

    spread = 2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha))

    # conversions
    if abs:
        avg = (high + low) / 2
        spread = spread * avg

    if bps:
        spread = spread * 10000

    if pips:
        avg = ((high + low) / 2).loc[spread.index]
        spread = (spread * avg) / 0.01
    if  target[0]:
        avg = ((high + low) / 2).loc[spread.index]
        spread = (spread * avg) / target[1]
    # else return as a percentage of the mid price
    # lag to avoid lookahead bias
    return spread.shift(1).dropna()

spread_cs_abs = cs_spread_estimator(data_weekdays['XAUT-USD'], abs=True)
spread_cs_bps = cs_spread_estimator(data_weekdays['XAUT-USD'], bps=True)
spread_cs_pips = cs_spread_estimator(data_weekdays['XAUT-USD'], pips=True)




# def CorwinSchultzSpread(df: pd.DataFrame,
#                         absolute: bool = False,
#                         bps: bool = False,
#                         pips: bool = False,
#                         pip_size: Optional[float] = 0.01,
#                         target: tuple[bool, float] = (False, 20.0),
#                         clip_sigma: Optional[float] = None) -> pd.Series:
#     if int(bool(absolute)) + int(bool(bps)) + int(bool(pips)) + int(bool(target[0])) > 1:
#         raise ValueError("Only one of `absolute`, `bps`, `pips` or `target` may be active")
#     k = 3 - 2 * np.sqrt(2)

#     df_used = df[['High', 'Low']].dropna().copy()
#     df_used = df_used[(df_used['High'] > 0) & (df_used['Low'] > 0)]

#     high = df_used['High']
#     low = df_used['Low']

#     # single-day log range; optionally guard against wick outliers
#     log_hl = np.log(high / low)
#     if clip_sigma is not None:
#         med = log_hl.rolling(20, min_periods=5).median()
#         mad = (log_hl - med).abs().rolling(20, min_periods=5).median()
#         upper = med + clip_sigma * 1.4826 * mad          # robust sigma
#         log_hl = log_hl.clip(upper=upper)

#     # beta  = sum of the two SINGLE-day squared log-ranges   (fixed)
#     beta = log_hl ** 2 + log_hl.shift(1) ** 2

#     # gamma = the TWO-day squared log-range                   (fixed)
#     high_2d = pd.concat([high, high.shift(1)], axis=1).max(axis=1)
#     low_2d = pd.concat([low, low.shift(1)], axis=1).min(axis=1)
#     gamma = (np.log(high_2d / low_2d)) ** 2

#     valid = beta.notna() & gamma.notna()
#     beta = beta[valid]
#     gamma = gamma[valid]

#     sqrt_beta = np.sqrt(beta)
#     sqrt_2beta = np.sqrt(2 * beta)
#     alpha = (sqrt_2beta - sqrt_beta) / k - np.sqrt(gamma / k)

#     # signed spread as a fraction of mid — DO NOT floor per-day here
#     spread_frac = 2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha))
#     mid = ((high + low) / 2).reindex(spread_frac.index)

#     if absolute:
#         result = spread_frac * mid
#     elif bps:
#         result = spread_frac * 10000.0
#     elif pips:
#         result = (spread_frac * mid) / pip_size
#     elif target[0]:
#             target_mean_bps = float(target[1])
#             floor_bps       = float(target[2]) if len(target) > 2 else 0.25 * target_mean_bps
#             tgt_frac, floor_frac = target_mean_bps/1e4, floor_bps/1e4

#             shape = spread_frac.rolling(20, min_periods=5).mean()   # signed, de-noised
#             shape = shape - shape.min() + 1e-9                      # shift so min ~ 0  (NO clip)
#             m = shape.mean()
#             shape = shape / m if (np.isfinite(m) and m > 0) else shape*0 + 1   # mean -> 1

#             result = floor_frac + (tgt_frac - floor_frac) * shape   # min = floor, mean = tgt
#     else:
#         result = spread_frac

#     return result.shift(1).dropna()

# spread_cs_abs    = CorwinSchultzSpread(data_weekdays['XAUT-USD'], absolute=True)
# spread_cs_bps    = CorwinSchultzSpread(data_weekdays['XAUT-USD'], bps=True)
# spread_cs_pips   = CorwinSchultzSpread(data_weekdays['XAUT-USD'], pips=True, pip_size=0.01)
# spread_cs_target = CorwinSchultzSpread(data_weekdays['XAUT-USD'], target=(True, 20.0))


# function to compute spread with optional rolling beta adjustment
def compute_spread(data, asset1, asset2, beta=True, rolling_window=window, min_periods=20, debug=True):
    """
    Compute spread between two assets with optional rolling beta adjustment
    
    Args:
        data: Dictionary of dataframes with price data
        asset1, asset2: Asset names
        beta: Whether to apply beta adjustment
        rolling_window: Rolling window for beta estimation (default 60 days)
        min_periods: Minimum periods required for beta calculation
        debug: Whether to print debug information
    """
    # Get data for the two specific assets
    df1 = data[asset1].copy()
    df2 = data[asset2].copy()
    
    # Find common dates between these two assets only
    common_dates = set(df1.index).intersection(set(df2.index))
    
    # Align both dataframes to common dates
    df1_aligned = df1.loc[df1.index.isin(common_dates)].sort_index()
    df2_aligned = df2.loc[df2.index.isin(common_dates)].sort_index()
    
    if beta:
        # Calculate rolling beta
        rolling_betas = []
        
        for i in range(len(df1_aligned)):
            if i < min_periods - 1:
                rolling_betas.append(np.nan)
            else:
                # Define the rolling window
                start_idx = max(0, i - rolling_window + 1)
                end_idx = i + 1
                
                # Get the window data
                y_window = df1_aligned['Close'].iloc[start_idx:end_idx]
                x_window = df2_aligned['Close'].iloc[start_idx:end_idx]
                
                # Skip if insufficient data
                if len(y_window) < min_periods:
                    rolling_betas.append(np.nan)
                    continue
                
                try:
                    # OLS regression: y = alpha + beta * x
                    model = OLS(y_window, add_constant(x_window)).fit()
                    beta_est = model.params.iloc[1]
                    rolling_betas.append(beta_est)
                except:
                    rolling_betas.append(np.nan)
        
        # Convert to pandas series
        beta_series = pd.Series(rolling_betas, index=df1_aligned.index)
        
        # Calculate spread using rolling beta: asset1 - beta(t) * asset2
        spread = df1_aligned['Close'] - beta_series * df2_aligned['Close']
        
        if debug:
            valid_betas = beta_series.dropna()
            print(f"Rolling Beta for {asset1}-{asset2} (window={rolling_window})")
            print(f"  Mean: {valid_betas.mean():.4f}")
            print(f"  Std: {valid_betas.std():.4f}")
            print(f"  Min: {valid_betas.min():.4f}")
            print(f"  Max: {valid_betas.max():.4f}")
            print(f"  Valid observations: {len(valid_betas)}/{len(beta_series)}")
        
        spread.name = f'{asset1}_{asset2}_spread_rolling_beta_{rolling_window}d'
    else:
        spread = df1_aligned['Close'] - df2_aligned['Close']
        # spread.name = f'{asset1}_{asset2}_spread'
        spread.name = f'spread'
    
    if beta:
        return spread, beta_series
    return spread, pd.Series(1.0, index=spread.index, name='beta')