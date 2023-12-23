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
ticker = Tickers.nifty_50_stocks[1]
df = blob_service.get_ticker_history(ticker)
df = utils.filter_last_n_days(df, 100)
timeframe = "30T"
df = utils.resample_to_timeframe(df, timeframe)

df = df.iloc[::-1]
df.head()

from SharedCode.Strategies.ml import KernelRegressionStrategy
strategy = KernelRegressionStrategy()
df = strategy.get_yhat1_with_signals(df, "close")

df.head(200)


from SharedCode.Utils.stock_chart import StockChart

StockChart.plot(df, ticker, timeframe)


# 
# 
# 
# For plotting
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# add subplot properties when initializing fig variable
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.01,
    row_heights=[0.9, 0.3],
    
)

fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
    ), row=1, col=1
)

fig.add_trace(
    go.Bar(
        x=df.index,
        y=df["volume"],
    ),
    row=2,
    col=1,
)

fig.update_xaxes(
    rangeselector=dict(
        buttons=list(
            [
                dict(count=7, label="7D", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(step="all"),
            ]
        )
    ), row=1, col=1
)
fig.update_layout(
    title_text=f"{ticker} | {timeframe}",
    height=600,
    width=900,
    xaxis_rangeslider_visible=False,
    xaxis_rangebreaks=[
        dict(bounds=["sat", "mon"]),
        dict(bounds=[15.15, 9.25], pattern="hour"),
    ],
)
fig.show()