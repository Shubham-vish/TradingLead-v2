import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../..")))

from Prototyping.setupConfig import setup_config

setup_config()


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
from SharedCode.Repository.Fyers.fyers_service import FyersService
from SharedCode.Repository.Fyers.fyers_client_factory import FyersClientFactory

kv_service = KeyVaultService()
telemetry = LoggerService()

operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

fyers_details = kv_service.get_fyers_user(0)


fyers_client = FyersClientFactory.get_fyers_client(fyers_details)

fyers_service = FyersService(fyers_details)

ticker_name = "NSE:ICICIBANK-EQ"

# //Following code is able to execute Nifty fuy of 1 lot
ticker_name = "NSE:NIFTY24JANFUT"
qty = 50
productType = "MARGIN"
fyers_service.place_buy_market(ticker_name, qty, productType, tel_props)

# Able to set stoploss for Nifty future buy position, Once the stopprice is reached the order gets executed
# but if position is buy position is not there it will create a nakes sell position
fyers_service.execute_stop_loss_for_buy_market(
    ticker_name, qty, 21400, productType, tel_props
)


# //Able to exit all positions
fyers_service.exit_all_positions(tel_props)


ticker_name = "NSE:LEMONTREE-EQ"
qty = 1
productType = "CNC"
# Able to place buy order in CNC
fyers_service.place_buy_market(ticker_name, qty, productType, tel_props)

# Able to set stoploss for buy CNC order, once the stopprice is reached the order gets executed
# This doesnt get executed when there is no holding or active position for given quantity
fyers_service.execute_stop_loss_for_buy_market(
    ticker_name, qty, 121.7, productType, tel_props
)

fyers_client.positions()

currentprice = 21570
data = {
    "symbol": ticker_name,
    "qty": qty,
    "type": 3,
    "side": -1,
    "productType": productType,
    "stoploss": 0,
    "stopprice": 21480,
    "validity": "DAY",
    "disclosedQty": 0,
    "offlineOrder": False,
}

response = fyers_client.place_order(data=data)


qty = 50
productType = "MARGIN"
currentprice = 21575
# fired
data = {
    "symbol": ticker_name,
    "qty": qty,
    "type": 3,
    "side": 1,
    "productType": productType,
    "stoploss": 0,
    "stopprice": 21460,
    "validity": "DAY",
    "disclosedQty": 0,
    "offlineOrder": False,
}

response = fyers_client.place_order(data=data)


fyers_client.positions()
