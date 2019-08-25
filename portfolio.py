from typing import List, Dict

import pandas as pd
import numpy as np

from import_data import *

class Portfolio:
    """Class for a portfolio, containing composition and transaction history

    assets: Dict with interface:weight pairs. For simplicity, weights are 
    assumed to be constant

    history: Dataframe containing the date and ammount of deposit/removal
    from the portfolio

    returns: time-series dataframe containing portfolio returns through time
    """
    
    assets: Dict[int, Interface]
    history: pd.DataFrame
    returns: pd.DataFrame
    
    def __init__(self, assets, history):

        assert sum([*assets.keys()]) == 1
        assert isinstance([*assets.values()][0], Interface)

        self.assets = assets
        self.history = history
        self.returns = returns

    def add_transaction(self, time, ammount):
        if isinstance(time, str):
            time = pd.Timestamp(time)

        history.append(pd.DataFrame({"ammount":[ammount]}, index=[time]))

    def set_returns(self):
        rets = []

        for a, w in self.assets.items():
            rets.append(a.get_daily_prices().pct_change().iloc[1:] * w)

        self.returns = pd.concat(rets, join="outer").mean(axis=1).fillna(0)
        # mean of the returns of each axis

    def get_returns(self, latest_annualized=True, start=None, end=None):
        
        mean_rets = _filter_dates(self.returns, start, end) if start \
                                                            else self.returns

        mean_rets = mean_rets.resample("Y").mean()

        return mean_rets.iloc[0, 0] if latest_annualized else np.mean(mean_rets)

    def get_volatility(self, latest_annualized=True, start=None, end=None):

        sd_rets = _filter_dates(self.returns, start, end) if start \
                                                          else self.returns
        sd_rets = sd_rets.resample("Y").std()

        return sd_rets.iloc[0, 0] if latest_annualized else np.mean(sd_rets)

 
def _filter_dates(data, start, end):
    ret = data.copy()

    ret = data[data.index >= start]

    if self.end:
        ret = data[data.index <= end]

    return ret
