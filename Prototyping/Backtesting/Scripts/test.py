import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../..")))

from Prototyping.setupConfig import setup_config

setup_config()

# Above code is for testing

import pandas as pd

from SharedCode.Repository.BlobService.blob_service import BlobService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.tikers import Tickers
from SharedCode.Utils.utility import FunctionUtils as utils

blob_service = BlobService()
ticker = Tickers.nifty_50_stocks[6]
df = blob_service.get_ticker_history(ticker)
df = utils.filter_last_n_days(df, 100)

# utils.are_dataframes_identical(
#     utils.resample_to_timeframe(fdf, "60T"),
#     utils.resample_to_timeframe(fdf, "1H"),
# )
df = utils.resample_to_timeframe(df, "30T")
df.head()

df = df.iloc[::-1]
df.head()

import math


def kernel_regression(cdf, start, h, r, x_0):
    curr_weight = 0
    cum_weight = 0
    yhat = 0
    for i in range(0, 2 + x_0):
        y = cdf.iloc[i + start]["close"]
        # Handle cases where the index is out of range
        # print("y",y, " ",i)
        w = math.pow(1 + (math.pow(i, 2) / (math.pow(h, 2) * 2 * r)), -r)
        curr_weight += y * w
        cum_weight += w
        # print("cur w",curr_weight)
        # print("cu ww",cum_weight)

        yhat = curr_weight / cum_weight
        # print("yhat ",yhat)
    return round(yhat, 2)


window = 25
yhat_values = [None] * len(df)
for i in range(len(df) - window - 1):
    yhat_values[i] = kernel_regression(df, i, 8, 8, window)


df["yhat"] = yhat_values

df["prev-yhat"] = df["yhat"].shift(-1)

df.head(25)
import numpy as np

df["pyhat"] = np.where(df["yhat"] >= df["prev-yhat"], df["yhat"], np.nan)
df["nyhat"] = np.where(df["yhat"] < df["prev-yhat"], df["yhat"], np.nan)
df.head(200)

# For plotting
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# add subplot properties when initializing fig variable
fig = make_subplots(
    rows=4,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.01,
    row_heights=[0.9, 0.3, 0.2, 0.2],
)

fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
    )
)

# df.head()

# Colours for the Bar chart
colors = [
    "#FF0000" if row["open"] - row["close"] > 0 else "#00FF00"
    for index, row in df.iterrows()
]
fig.add_trace(
    go.Bar(
        x=df.index,
        y=df["volume"],
        marker_color=colors,
    ),
    row=2,
    col=1,
)


fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["pyhat"],
        opacity=0.7,
        line=dict(color="green", width=2),
        name="MA 5",
    )
)


fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["nyhat"],
        opacity=0.7,
        line=dict(color="red", width=2),
        name="MA 5",
    )
)

fig.update_xaxes(
    rangeselector=dict(
        buttons=list(
            [
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(step="all"),
            ]
        )
    )
)

fig.update_layout(
    height=600,
    width=1200,
    xaxis_rangeslider_visible=False,
    xaxis_rangebreaks=[
        dict(bounds=["sat", "mon"]),
        dict(bounds=[15.15, 9.25], pattern="hour"),
    ],
)


fig.update_yaxes(title_text="Price", row=1, col=1)
fig.update_yaxes(title_text="Volume", row=2, col=1)

fig.show()


# df['MA20'] = df['close'].rolling(window=20).mean()
# df['MA5'] = df['close'].rolling(window=5).mean()
