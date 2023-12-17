import os
import sys

#Below code is for testing
sys.path.append(os.path.abspath(os.path.join('../..')))

from Notebooks.setupConfig import setup_config
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
        Constants.SERVICE : Constants.access_token_generator_service,
        Constants.operation_id : operation_id,
    }

fyer_users_json = kv_service.get_secret("FyerUserDetails")
telemetry.info(fyer_users_json, tel_props)
fyer_users = json.loads(fyer_users_json)

fyers_details_json = kv_service.get_secret(fyer_users[0]['KvSecretName'])
fyers_details = json.loads(fyers_details_json)

fyerService = FyersService(fyers_details)


import pandas as pd
from datetime import datetime, timedelta, date


def historical_bydate(symbol,sd,ed, interval = 1):
    data = {"symbol":symbol, "resolution":"1","date_format":"1","range_from":str(sd),"range_to":str(ed),"cont_flag":"1"}
    nx = fyerService.history(data)
    cols = ['datetime','open','high','low','close','volume']
    df = pd.DataFrame.from_dict(nx['candles'])
    df.columns = cols
    df['datetime'] = pd.to_datetime(df['datetime'],unit = "s")
    df['datetime'] = df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
    df['datetime'] = df['datetime'].dt.tz_localize(None)
    df = df.set_index('datetime')
    return df

# sd  = date(2017,7,3)
# # sd = datetime.now()
# dat = sd.strftime("%Y-%m-%d")
# dat1 = (sd - timedelta(days=50)).strftime("%Y-%m-%d")
# data = {"symbol":"NSE:SBIN-EQ","resolution":"1","date_format":"1","range_from":dat1,"range_to":dat,"cont_flag":"1"}
# x = fyerService.history(data)
# df = pd.DataFrame.from_dict(x['candles'])
# cols = ['datetime','open','high','low','close','volume']
# df.columns = cols
# df['datetime'] = pd.to_datetime(df['datetime'],unit = "s")
# df['datetime'] = df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
# df['datetime'] = df['datetime'].dt.tz_localize(None)
# df = df.set_index('datetime')
    


# tickers=["NSE:NIFTYBANK-INDEX", "NSE:NIFTY50-INDEX", "NSE:SBIN-EQ"]
tickers= Tickers.nifty_50_stocks

for ticker in tickers[1:]:
    print(ticker)
    df = pd.DataFrame()
    sd = date(2017,7,3)
    enddate = datetime.now().date()

    n = abs((sd - enddate).days)
    ab = None
    while ab == None: 
        sd = (enddate - timedelta(days= n ))
        ed = (sd + timedelta(days= 99 if n >100 else n)).strftime("%Y-%m-%d")
        sd = sd.strftime("%Y-%m-%d")
        dx = historical_bydate(ticker, sd, ed)
        df = pd.concat([df, dx])
        n = n - 100 if n > 100 else n - n 
        print(n)
        if n == 0 : 
            ab = "done"
    ticker = ticker.replace(":","_")
    location = f"../Data/Nifty50/{ticker}.csv"
    df.to_csv(rf"{location}")
    print(location)
