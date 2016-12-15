import datetime

import numpy as np
import pandas as pd
import statsmodels.api as sm

from strategy import Strategy
from event import SignalEvent
from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import Portfolio

"""
Strategy based on analysts' historical performance.
"""


class FollowStarAnalystStrategy(Strategy):
    """
    Follow the rank of star analysts' reports. Buy assets when the rank is buy
    or strong buy, and sell assets when the rank is sell and strong sell.
    A star analyst is that who has a good record in giving proper rank,
    predicting the price changes or trend more precisely than others.
    """
    def __init__(self, bars, events):
        self.bars = bars
        self.events = events
    pass