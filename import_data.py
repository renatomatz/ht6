import os
import json
from datetime import datetime

import quandl
import pandas as pd
import pandas_datareader as web
import numpy as np

class Interface:

    _mem_file: str
    _API_KEY: int

    def __init__(self, mem_file=None, key=None):
        
        self._mem_file = mem_file
        self.set_key(key)

    def set_key(self, key):

        if ".txt" in key:

            with open(key) as f:
                self._API_KEY = f.readline().rstrip("\n")

        else:
            self._API_KEY = key

    def set_mem_file(self, new):
        
        self._mem_file = new

    def _ensure_api_enabled(f):

        def check(*args, **kwargs):
            
            if quandl.ApiConfig.api_key is None:

                args[0].enable()  # args[0] == self

            return f(*args, **kwargs)

        return check


class Equity(Interface):

    ticker: str
    inv_type: str
    market: str
    industry: str
    start: datetime
    end: datetime

    def __init__(self, name, inv_type="Equity", market=None, industry=None, 
                 start=None, end=None, mem_file=None, key=None):

        self.ticker = name
        self.inv_type = inv_type
        self.market = market
        self.industry = industry
        self.start = start
        self.end = end

        self.set_start(start)

        self.set_end(end)

        if not mem_file:
            mem_file = "data/" + self.ticker

        super().__init__(mem_file=mem_file, key=key)

    def enable(self):
        
        if self._API_KEY:
            quandl.ApiConfig.api_key = self._API_KEY
        else:
            ValueError("_API_KEY is not set, set it with self.set_key()")

    def set_start(self, new):

        if isinstance(new, str):
            new = pd.Timestamp(new)

        self.start = new

    def set_end(self, new):

        if isinstance(new, str):
            new = pd.Timestamp(new)

        self.end = new

    def set_market(self, new):
        self.market = new

    def set_industry(self, new):
        self.industry = new

    @Interface._ensure_api_enabled
    def get_dataset(self, name, columns=None, save_new=True, industry=False):
        
        if self._exists(name):

            data = pd.read_csv(self._make_path(name))
            data.set_index("None")
            # Imported index is normally labeled as "None" and saved as column

            for col in [c for c in data.columns if "date" in c]:
                # Dates are not automatically converted to <pd.Timestamp> objects
                # assumes <pd.Timestamp> columns have "date" in their names
                data[col] = data[col].map(lambda x: pd.Timestamp(x))

        else:

            data = quandl.get_table("SHARADAR/"+name, 
                                    paginate=True,
                                    ticker=self.ticker if not industry \
                                                else self.industry)

            if save_new:

                if not os.path.exists(self._mem_file):
                    os.mkdir(self._mem_file)

                data.to_csv(self._make_path(name))

        return data.loc[:, columns] if columns else data

    def update_dataset(self, name):
        """Update existing dataset or import it from Quandl given its name
        """
        quandl.get_table("SHARADAR/" + name, ticker=self.ticker) \
            .to_csv(self._make_path(name))

    def available_saved(self):
        """Return the saved datasets available
        """
        return [*os.listdir(self._mem_file)]

    def _exists(self, name):
        """Return whether a dataset exists
        """
        return os.path.exists(self._make_path(name))

    def _make_path(self, name):
        """Return a path (not necessarily there) to a .csv file with a given
        name
        """

        return self._mem_file + "/" + name + ".csv"

    def _filter_dates(self, data, start=None, end=None):
        """Filter data in accordance to the values set in <self.start> and
        <self.end> or no bound if none are set

        Assumes data is indexed by date at level 0
        """
        if not start:
            start = self.start

        if not end:
            end = self.end
         
        if start: 
            data = data[data.index > start]

        if end:
            data = data[data.index <= end]

        return data

    def _ts_index(self, data, date_col=None):
        """Return data with a time series index at <date_col>

        If <date_col> is None, use the first column in the dataset containing
        the word "date"
        """

        if not date_col:
            date_col = [c for c in data.columns if "date" in c]

        return data.set_index(date_col)

    @Interface._ensure_api_enabled
    def get_daily_prices(self):

        data = self.get_dataset("SEP", 
                                 columns=["ticker", "date", "close"])

        data = self._ts_index(data, date_col="date")

        data = self._filter_dates(data)

        data["price"] = data["close"]
        del data["close"]

        return data

    @Interface._ensure_api_enabled
    def get_fundamentals(self):

        data = self.get_dataset("SF1", 
                                columns=["calendardate", "ticker", "price", 
                                         "ev", "ebitda", "grossmargin", 
                                         "revenue", "fcf", "workingcapital"])

        data["ev/ebitda"] = data["ev"] / data["ebitda"]
        data["ev/sales"] = data["ev"] / data["revenue"]
        data["ev/fcf"] = data["ev"] / data["fcf"]
        data["nwc_percent_sales"] = (data["workingcapital"] / data["revenue"])*100

        data = self._ts_index(data, date_col="calendardate")

        data = self._filter_dates(data)

        return data

    @Interface._ensure_api_enabled
    def get_industry(self, set_new=True):
        """Get company industry based on its sic code

        As this method gathers all available data 
        """
        if self.industry and not set_new:
            return self.industry

        data = self.get_dataset("TICKERS")
        data = data[data.ticker == self.ticker][data.table == "SF1"]
        # guarantee there will be a single sic code available

        code = int(data["siccode"].iloc[0])
        # returns only the first industry code number
        return code // 1000 

class Custom(Interface):

    def __init__(self, inv_type=None, mem_file=None, key=None):

        self.inv_type = inv_type

        if not mem_file:
            mem_file = "data"

        super().__init__(mem_file, key)

    def get_dataset(self, name, source="yahoo", columns=None, date_col="Date"):
        """Get market data from Yahoo! finance using a <pandas.data_reader>

        name: market index name as available in Yahoo! finance
        """
        if name is None:
            return pd.DataFrame()

        path = self._mem_file+"/"+name+".csv"

        if os.path.exists(path):

            data = pd.read_csv(path)

            data[date_col] = data[date_col].map(lambda x: pd.Timestamp(x))

            data = data.set_index(date_col)

        else:
            
            data = web.DataReader(name,source)

            if not os.path.exists(self._mem_file):
                os.mkdir(self._mem_file)

            data.to_csv(path)
            # unlike Quandl tables, <DataReader> calls automatically index
            # data on dates, <Interface> calls are supposed to return data with
            # a standardized index, and optionally make them time series 

        return data.loc[:, columns] if columns else data

