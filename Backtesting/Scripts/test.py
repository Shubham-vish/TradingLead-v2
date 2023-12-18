import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../..")))

from Notebooks.setupConfig import setup_config

setup_config()

# Above code is for testing

import pandas as pd

from SharedCode.Repository.BlobService.blob_service import BlobService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.tikers import Tickers
from SharedCode.Utils.utility import FunctionUtils as utils

blob_service = BlobService()

df = blob_service.get_ticker_history(Tickers.nifty_50_stocks[0])

df.head()
fdf = utils.filter_last_n_days(df, 20)

fdf.head()

utils.are_dataframes_identical(
    utils.resample_to_timeframe(fdf, "60T"),
    utils.resample_to_timeframe(fdf, "1H"),
)
sdf = utils.resample_to_timeframe(fdf, "1D")
sdf.head(20)

import mplfinance as mpf

mpf_style = mpf.make_mpf_style(base_mpf_style="yahoo")

# Plot the candlestick chart
mpf.plot(
    sdf.head(30),
    type="candle",
    style=mpf_style,
    volume=True,
    title="30-Minute Candlestick Chart",
)
# fdf.to_csv("../test.csv")
