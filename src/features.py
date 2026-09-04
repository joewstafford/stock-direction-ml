import pandas as pd

RETURN_LAGS = (1,2,3,5,10)
VOL_WINDOWS = (5,10,20)
MA_WINDOWS = (5,10,20,50)

def check_input(close):
        #Makes sure close is an instance of a pandas series
        if not isinstance(close, pd.Series):
            raise TypeError(f"expected a Series, got {type(close).__name__}")
        #checks dates are increasing
        if not close.index.is_monotonic_increasing:
            raise ValueError("index must be sorted ascending or lags/rolling are meaningless")
        #checkes dates don't contain duplicates
        if close.index.has_duplicates:
            raise ValueError("index has duplicate dates")


#Individual daily returns at each lag. NOT CUMULATIVE RETURNS OVER WINDOW
# pct_change(periods=k) would give overlapping features (ret_10 contains ret_5),
# which makes the design matrix ill-conditioned and the coefficients meaningless.
def compute_lagged_returns(close, lags=RETURN_LAGS):
    daily = close.pct_change()
    returns = pd.DataFrame(index=close.index) 

    for lag in lags:
        #returns[f'ret_{lag}'] = df.pct_change(periods=lag)
        returns[f'ret_lag_{lag}'] = daily.shift(lag-1)

    #print("returns")
    return returns

def compute_rolling_volatility(close, windows=VOL_WINDOWS):
    #daily returns
    daily = close.pct_change()
    #rolling volatilities
    vols = pd.DataFrame(index=close.index) 

    for window in windows:
        vols[f'vol_{window}'] = daily.rolling(window=window).std()

    #print("rvs")
    return vols
    
#Compute moving average ratios
#Price is divided by own moving average (not average itself) giving raw MA levels 
def compute_moving_average_ratios(close, windows=MA_WINDOWS):
    ratios = pd.DataFrame(index=close.index)

    for window in windows:
        ratios[f'ma_ratio_{window}'] = close / close.rolling(window = window).mean()

    #print("mas")
    return ratios

def build_features(close,lags=RETURN_LAGS, vol_windows=VOL_WINDOWS, avg_windows=MA_WINDOWS, dropna=True ):
    check_input(close)
    lagged = compute_lagged_returns(close,lags)
    volatility = compute_rolling_volatility(close, vol_windows)
    average = compute_moving_average_ratios(close, avg_windows)
    features = pd.concat([close,lagged,volatility,average], axis=1)
    #print("result")
    return features.dropna() if dropna else features

#print(build_features(close))

if __name__ == "__main__":
    from data_pipeline import load_price_data

    close = load_price_data()["Close"].squeeze()
    #print(load_price_data().columns)
    features = build_features(close)
    print(features.shape)
    print(features.head())