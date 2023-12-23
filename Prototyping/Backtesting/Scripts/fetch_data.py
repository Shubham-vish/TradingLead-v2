import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../..")))

from Prototyping.setupConfig import setup_config

setup_config()

# Above code is for testing

from SharedCode.Repository.AccessToken.access_token import get_fyers_access_token
import json
import time
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.Cache.redis_cache_service import RedisCacheService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.tikers import Tickers
from SharedCode.Repository.Fyers.fyers_client_factory import FyersClientFactory
from SharedCode.Repository.Fyers.fyers_service import FyersService

kv_service = KeyVaultService()
telemetry = LoggerService()
redis_cache_service = RedisCacheService()

operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

fyer_users_json = kv_service.get_secret("FyerUserDetails")
telemetry.info(fyer_users_json, tel_props)
fyer_users = json.loads(fyer_users_json)

fyers_details_json = kv_service.get_secret(fyer_users[0]["KvSecretName"])
fyers_details = json.loads(fyers_details_json)

fyerService = FyersService(fyers_details)


import pandas as pd
from datetime import datetime, timedelta, date


def historical_bydate(symbol, sd, ed, resolution="1"):
    nx = fyerService.history(symbol, str(sd), str(ed),resolution)
    cols = ["datetime", "open", "high", "low", "close", "volume"]
    df = pd.DataFrame.from_dict(nx["candles"])
    df.columns = cols
    df["datetime"] = pd.to_datetime(df["datetime"], unit="s")
    df["datetime"] = df["datetime"].dt.tz_localize("utc").dt.tz_convert("Asia/Kolkata")
    df["datetime"] = df["datetime"].dt.tz_localize(None)
    df = df.set_index("datetime")
    return df


tickers = Tickers.nifty_50_stocks

from SharedCode.Repository.BlobService.blob_service import BlobService

blob_service = BlobService()

for ticker in tickers:
    print(ticker)
    df = pd.DataFrame()
    sd = date(2017, 7, 3)
    enddate = datetime.now().date()

    n = abs((sd - enddate).days)
    ab = None
    while ab == None:
        sd = enddate - timedelta(days=n)
        ed = (sd + timedelta(days=99 if n > 100 else n)).strftime("%Y-%m-%d")
        sd = sd.strftime("%Y-%m-%d")
        dx = historical_bydate(ticker, sd, ed)
        df = pd.concat([df, dx])
        n = n - 100 if n > 100 else n - n
        print(n)
        if n == 0:
            ab = "done"
    ticker = ticker.replace(":", "_")
    # location = f"../Data/Nifty50/{ticker}.csv"
    # df.to_csv(rf"{location}")
    blob_name = f"{Constants.DIR_NIFTY_50}/{ticker}.csv"
    result = blob_service.create_blob(df, Constants.STOCK_HISTORY_CONTAINER, blob_name)
    print(result)
    # print(location)

tickers = Tickers.nifty_50_stocks
cdf = blob_service.get_ticker_history(tickers[0])
cdf.head()
