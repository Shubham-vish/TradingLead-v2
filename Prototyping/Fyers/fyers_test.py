import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../../..")))

from Prototyping.setupConfig import setup_config

setup_config()

#
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
from SharedCode.Models.net_positions_response import (
    NetPositionResponse,
    NetPosition,
)

from SharedCode.Models.fyers_constants import (
    ProductType,
    OrderSide,
    OrderType,
)

kv_service = KeyVaultService()

operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

fyers_details = kv_service.get_fyers_user(1)

fyers_service = FyersService(fyers_details)

ticker_name = "NSE:ICICIBANK-EQ"


from SharedCode.Models.dataclass_from_dict import dataclass_from_dict
from dataclasses import asdict
from SharedCode.Models.holdings_response import HoldingsResponse, Holding


fyers_client = FyersClientFactory.get_fyers_client(fyers_details)

from SharedCode.Models.holding import Holding

holdings = fyers_client.holdings()
from dacite import from_dict

data = {
    'costPrice': 100.0,
    'id': 1,
    'symbol': 'XYZ',
    'quantity': 10,
    'segment': 2,
    'pl': 50.0,
    'ltp': 150.0,
    'marketVal': 1000.0,
    'holdingType': 'TypeA'
}

Holding(**data)
holding_instance = from_dict(data_class=Holding, data=data)

hres = from_dict(data_class=HoldingsResponse, data=holdings)
type(holdings)

HoldingsResponse.from_dict(holdings)
holdings = fyers_service.get_holdings(tel_props)

netpositison = fyers_service.get_positions(tel_props)
pos = from_dict(data_class=NetPositionResponse, data=netpositison)
holdings.get_quantity("NSE:GAIL-EQ")

type(holdings)


ss = dataclass_from_dict(HoldingsResponse, asdict(holdings))

type(holdings.holdings[0])
for holding in holdings.holdings:
    print(type(holding))
    
    
fyers_client.orderbook()
holdings.get_quantity("NSE:GAIL-EQ")
from SharedCode.Models.holdings_response import HoldingsResponse, Holding
hold_model = HoldingsResponse.from_dict(holdings)
hold_model.get_quantity("NSE:GAIL-EQ")
positions = fyers_service.get_positions(tel_props)
positions.get_quantity("NSE:GAIL-EQ")
positions.net_positions
positions.get_positions_of_type(ProductType.margin)

ticker_name = "NSE:NIFTY24JANFUT"
qty = 50
fyers_service.place_buy_market(ticker_name, qty, ProductType.margin, tel_props)

# Able to set stoploss for Nifty future buy position, Once the stopprice is reached the order gets executed
# but if position is buy position is not there it will create a nakes sell position
fyers_service.place_stoploss_for_buy_market_order(
    ticker_name, qty, 21400, ProductType.margin, tel_props
)


# //Able to exit all positions
fyers_service.exit_all_positions(tel_props)


ticker_name = "NSE:LEMONTREE-EQ"
qty = 1
# Able to place buy order in CNC
fyers_service.place_buy_market(ticker_name, qty, ProductType.cnc, tel_props)

# Able to set stoploss for buy CNC order, once the stopprice is reached the order gets executed
# This doesnt get executed when there is no holding or active position for given quantity
fyers_service.place_stoploss_for_buy_market_order(
    ticker_name, qty, 121.7, ProductType.cnc, tel_props
)

fyers_client.funds()
fyers_client.holdings()


fyers_client.positions()


#
