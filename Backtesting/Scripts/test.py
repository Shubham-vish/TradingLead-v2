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
df.tail(20)
df.head()
fdf = utils.filter_last_n_days(df, 100)

# utils.are_dataframes_identical(
#     utils.resample_to_timeframe(fdf, "60T"),
#     utils.resample_to_timeframe(fdf, "1H"),
# )
sdf = utils.resample_to_timeframe(fdf, "30T")
sdf.head()
import mplfinance as mpf

mpf_style = mpf.make_mpf_style(base_mpf_style="yahoo")

# Plot the candlestick chart
mpf.plot(
    sdf.tail(30),
    type="candle",
    style=mpf_style,
    volume=True,
    title="30-Minute Candlestick Chart",
)

rsdf = sdf.iloc[::-1]
rsdf.head()
rsdf = rsdf.drop(['volume'], axis=1)
rsdf.head()

import math
# def kernel_regression(closedf, column_name, h, r, x_0):
#         curr_weight = 0
#         cum_weight = 0
#         yhat = 0

#         if column_name not in df.columns:
#             raise ValueError(f"Column '{column_name}' not found in DataFrame")

#         for i in range(0,2+x_0):
#             y = closedf[column_name].iloc[i]
#             print("y",y, " ",i)
#             # Handle cases where the index is out of range
#             # print("y",y, " ",i)
#             w = math.pow(1 + (math.pow(i, 2) / (math.pow(h, 2) * 2 * r)), -r)
#             curr_weight += y * w
#             cum_weight += w
#             # print("cur w",curr_weight)
#             # print("cu ww",cum_weight)

#             yhat=curr_weight / cum_weight
#             # Update the 'yhat' column in the DataFrame for the current index
#             closedf.at[i, 'yhat'] = yhat
#             # yhat_array.append(yhat)
#             # print("yhat ",yhat)
#         return closedf



# ydf = kernel_regression(rsdf.head(60), 8, 8, 25)

def kernel_regression(src, h, r, x_0):
        curr_weight = 0
        cum_weight = 0
        yhat = 0
        for i in range(0,2+x_0):
            y = src[i]
            # Handle cases where the index is out of range
            # print("y",y, " ",i)
            w = math.pow(1 + (math.pow(i, 2) / (math.pow(h, 2) * 2 * r)), -r)
            curr_weight += y * w
            cum_weight += w
            # print("cur w",curr_weight)
            # print("cu ww",cum_weight)

            yhat=curr_weight / cum_weight
            # print("yhat ",yhat)
        return yhat
    
def kernel_regression(cdf, start, h, r, x_0):
        curr_weight = 0
        cum_weight = 0
        yhat = 0
        for i in range(0,2+x_0):
            y = cdf.iloc[i+start]['close']
            # Handle cases where the index is out of range
            # print("y",y, " ",i)
            w = math.pow(1 + (math.pow(i, 2) / (math.pow(h, 2) * 2 * r)), -r)
            curr_weight += y * w
            cum_weight += w
            # print("cur w",curr_weight)
            # print("cu ww",cum_weight)

            yhat=curr_weight / cum_weight
            # print("yhat ",yhat)
        return round(yhat, 2)
window = 25
# yhatdf = kernel_regression(rsdf, 0, 8, 8, window)

# yhatdf

# shatdf = kernel_regression(rsdf, 1, 8, 8, window)

# shatdf

yhat_values = [None] * len(rsdf)
for i in range(len(rsdf) - window-1):
    yhat_values[i] = kernel_regression(rsdf, i, 8, 8, window)


rsdf['yhat'] = yhat_values
rsdf.head(25)
tdf = rsdf.iloc[1:]
tdf.head()

tyatdf = kernel_regression(tdf, 0, 8, 8, 25)
tyatdf
yhat = kernel_regression(closes, 8, 8, 25)
yhat