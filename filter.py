import pandas as pd
import numpy as np


class Filter:
    def __init__(self, path: str):
        self.path = path
        self.df = pd.read_csv(path)
        self._set_df()
        self._clean_return()
        self._get_cummaxmin()
        return

    def _set_df(self, start_date: str = "2021-01-01", end_date="2024-01-01"):
        self.df["Date"] = pd.to_datetime(self.df["Date"])
        self.df = self.df.sort_values(["Date"]).reset_index()
        start_date = start_date
        end_date = end_date
        # Filter DataFrame
        self.filtered_df = self.df[
            (self.df["Date"] >= start_date) & (self.df["Date"] <= end_date)
        ]

    def _clean_return(self):
        quotes = np.array(self.filtered_df["Close/Last"])
        self.log_returns = np.log(quotes[1:] / quotes[:-1])
        quantile_sup = np.quantile(self.log_returns, 0.98)
        quantile_inf = np.quantile(self.log_returns, 0.01)
        self.log_returns_clean = self.log_returns[
            (self.log_returns < quantile_sup) & (self.log_returns > quantile_inf)
        ]
        # np.isinf(log_returns_clean).sum()

    def _get_cummaxmin(self):
        self.cummax = np.maximum.accumulate(self.log_returns_clean)
        self.cummin = np.minimum.accumulate(self.log_returns_clean)
