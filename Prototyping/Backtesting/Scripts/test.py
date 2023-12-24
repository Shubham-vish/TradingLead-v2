import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../../..")))

from Prototyping.setupConfig import setup_config

setup_config()

# Above code is for testing

import pandas as pd

from SharedCode.Repository.BlobService.blob_service import BlobService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.tikers import Tickers
from SharedCode.Utils.utility import FunctionUtils as utils

blob_service = BlobService()
ticker = Tickers.nifty_50_stocks[0]
df = blob_service.get_ticker_history(ticker)
df = utils.filter_last_n_days(df, 100)
timeframe = "30T"
df = utils.resample_to_timeframe(df, timeframe)
df.head()
df = df.iloc[::-1]

df.head()
df.tail(10)

# testing

from SharedCode.Strategies.ml import KernelRegressionStrategy
strategy = KernelRegressionStrategy()
df = strategy.get_yhat1_with_signals(df, "close")

from SharedCode.Utils.stock_chart import StockChart
StockChart.plot_chart_with_yhat(df, ticker, timeframe)