import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../../..")))

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
import pandas as pd
from datetime import datetime, date
from SharedCode.Repository.BlobService.blob_service import BlobService

kv_service = KeyVaultService()
blob_service = BlobService()

operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

fyers_details = kv_service.get_fyers_user(0)
fyerService = FyersService(fyers_details)


tickers = Tickers.nifty_50_stocks
# df = fyerService.fetch_deep_history(tickers[0], date(2017, 7, 3), datetime.now().date(), tel_props)
tickers = tickers[:1]
for ticker in tickers:
    print(ticker)
    df = pd.DataFrame()
    sd = date(2017, 7, 3)
    enddate = datetime.now().date()

    fyerService.fetch_deep_history(ticker, sd, enddate, resolution="1", tel_props=tel_props)
    ticker = ticker.replace(":", "_")
    # location = f"../Data/Nifty50/{ticker}.csv"
    # df.to_csv(rf"{location}")
    blob_name = f"{Constants.DIR_NIFTY_50}/{ticker}.csv"
    result = blob_service.create_blob(df, Constants.STOCK_HISTORY_CONTAINER, blob_name)
    print(result)
    # print(location)

# tickers = Tickers.nifty_50_stocks
# cdf = blob_service.get_ticker_history(tickers[0])
# cdf.head()
