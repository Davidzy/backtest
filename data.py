from abc import ABCMeta, abstractmethod
import datetime
import os, os.path

import numpy as np
import pandas as pd

from event import MarketEvent

class DataHandler(object):
    """
    DataHandler is an abstract base class providing an interface for
    all subsequent (inherited) data handlers (both live and historic).
    The goal of a (derived) DataHandler object is to output a generated
    set of bars (OHLCVI) for each symbol requested.
    This will replicate how a live strategy would function as current
    market data would be sent "down the pipe". Thus a historic and live
    system will be treated identically by the rest of the backtesting suite.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_bar(self, symbol):
        """
        :return: returns the last bar updated.
        """
        raise NotImplementedError("Should implement get_latest_bar()")

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """
        :return: returns the last N bar updated.
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def get_latest_bar_datetime(self, symbol):
        """
        :return: Returns a Python datetime object for the last bar.
        """
        raise NotImplementedError("Should implement get_latest_bar_datetime()")

    @abstractmethod
    def get_latest_bar_value(self, symbol, val_type):
        """
        :return: Returns one of the Open, High, Low, Close, Volume or OI from
            the last bar.
        """
        raise NotImplementedError("Should implement get_latest_bar_value()")

    @abstractmethod
    def get_latest_bar_values(self, symbol, val_type, N=1):
        """
        :return: Returns hte last N bar values from the latest_symbol list, or
            the last bar.
        """
        raise NotImplementedError("Should implement get_latest_bar_values()")

    @abstractmethod
    def update_bars(self):
        """
        :return: Returns the latest bars to the bars_queue for each symbol in a
            tuple OHLCVI format: (datetime, open, high, low, close, volume,
            open interest).
        """
        raise NotImplementedError("Should implement update_bars()")


class HistoricCSVDataHandler(DataHandler):
    """
    HistoricCSVDataHandler is designed to read CSV files for each requested
    symbol from disk and provide an interface to obtain the "latest" bar in
    a manner identical to a live trading interface.
    """
    def __init__(self, events, csv_dir, symbol_list):
        """

        :param events:
        :param csv_dir:
        :param symbol_list:
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True

        self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        """

        :return:
        """
        comb_index = None
        for s in self.symbol_list:
            # Load the CSV
            self.symbol_data[s] = pd.read_csv(
                os.path.join(self.csv_dir, "{fname}.csv".format(fname=symbol)),
                parse_dates = True,
                header=0,
                index_col=0,
                names=['datetime', 'open', 'high', 'low', 'close', 'volume',
                       'adj_close']
            ).sort()

            if comb_index is None:
                comb_index = self.symbol_data[s].index
            else:
                comb_index.union(self.symbol_data[s].index)

            self.latest_symbol_data[s] = []

        for s in self.symbol_list:
            self.symbol_data[s] = self.symbol_data[s].\
                reindex(index=comb_index, method='pad').iterrows()