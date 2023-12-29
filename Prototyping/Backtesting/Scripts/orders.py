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

kv_service = KeyVaultService()

operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

fyers_details = kv_service.get_fyers_user(0)

fyers_client = FyersClientFactory.get_fyers_client(fyers_details)

fyers_service = FyersService(fyers_details)

ticker_name = "NSE:ICICIBANK-EQ"
pos_json = fyers_client.positions()


positions = fyers_service.get_positions(tel_props)

positions.net_positions
positions.get_positions_of_type(ProductType.MARGIN.value)

# netposition_response = NetPositionResponse.from_dict(pos_json)

# for position in netposition_response.net_positions:
#     print(position.product_type)
# //Following code is able to execute Nifty fuy of 1 lot
ticker_name = "NSE:NIFTY24JANFUT"
qty = 50
fyers_service.place_buy_market(ticker_name, qty, ProductType.MARGIN.value, tel_props)

# Able to set stoploss for Nifty future buy position, Once the stopprice is reached the order gets executed
# but if position is buy position is not there it will create a nakes sell position
fyers_service.place_stoploss_for_buy_market_order(
    ticker_name, qty, 21400, ProductType.MARGIN.value, tel_props
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
