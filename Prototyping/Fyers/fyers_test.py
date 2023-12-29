import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../..")))
sys.path.append(os.path.abspath(os.path.join("..")))
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


from SharedCode.Models.Fyers.constants import OrderSide, OrderType, Response

from dataclasses import asdict
from dacite import from_dict
from SharedCode.Models.Fyers.holding import Holding
from SharedCode.Models.Fyers.holdings_response import HoldingsResponse, Holding

from SharedCode.Models.Fyers.orderbook_response import OrderBookResponse, OrderBook

operation_id = "RandomOperationId"

from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, Stoploss

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}
stoploss_repo = StoplossesRepository()
kv_service = KeyVaultService()
fyers_details = kv_service.get_fyers_user(0)
fyers_service = FyersService(fyers_details)
fyers_client = FyersClientFactory.get_fyers_client(fyers_details)
telemetry = LoggerService()

ticker_name = "NSE:ICICIBANK-EQ"
netpositison = fyers_service.get_positions(tel_props)
orders = fyers_service.get_order_book(tel_props)
holdingResponse = fyers_service.get_holdings(tel_props)
res = fyers_client.holdings()
holdingResponse.holdings
symbols = "NSE:ICICIBANK-EQ,NSE:NIFTY24JANFUT,NSE:BATAINDIA-EQ"

data = {"symbols": symbols}
quote_response = fyers_service.get_quote(data, tel_props)

quote_response.get_ticker_and_ltp()


asdict(quote_response)
orders.orderBook
orders.orderBook[0].side
for order in orders.orderBook:
    print(
        order.stopPrice,
        order.status,
        order.symbol,
        order.side,
        order.type,
        order.qty,
        order.filledQty,
        order.productType,
    )
#   6 NSE:INTELLECT-EQ - Working
#   6 NSE:INDHOTEL-EQ - Working
#   5 NSE:MPHASIS-EQ - Rejected
#   2 NSE:BATAINDIA-EQ - Filled
#   2 NSE:IEX-EQ - Filled
#   2 is Filled
#   6 is Working i.e active orders
# 1 is cancelled
# 5 is rejected
# 6 NSE:INTELLECT-EQ 1 1 1 0 CNC
# 6 NSE:INDHOTEL-EQ -1 1 1 0 INTRADAY
# 5 NSE:MPHASIS-EQ -1 1 3 0 CNC
# 2 NSE:BATAINDIA-EQ 1 2 3 3 CNC
# 2 NSE:IEX-EQ 1 2 2 2 CNC
# 2 NSE:TECHM-EQ 1 1 1 1 INTRADAY
# 2 NSE:ICICIBANK-EQ 1 2 1 1 CNC
# 2 NSE:NIFTY24JANFUT 1 2 50 50 MARGIN
# 5 NSE:ICICIBANK-EQ -1 3 50 0 CNC
# 5 NSE:ICICIBANK-EQ -1 3 50 0 CNC
# 5 NSE:ICICIBANK-EQ -1 3 50 0 CNC
# 2 NSE:ICICIBANK-EQ 1 2 3 3 CNC
# 5 NSE:ICICIBANK-EQ -1 3 50 0 CNC
# 5 NSE:ICICIBANK-EQ -1 3 50 0 CNC
# 5 NSE:ICICIBANK-EQ -1 3 50 0 CNC
# 5 NSE:ICICIBANK-EQ -1 3 5 0 CNC
# 5 NSE:ICICIBANK-EQ -1 3 5 0 CNC
# 5 NSE:ICICIBANK-EQ -1 3 5 0 CNC
# 6 NSE:ICICIBANK-EQ -1 3 1 0 CNC
# 6 NSE:NIFTY24JANFUT -1 3 50 0 MARGIN
# 1 NSE:NIFTY24JANFUT -1 3 50 0 MARGIN
# 6 NSE:ICICIBANK-EQ -1 3 2 0 CNC
# 5 NSE:ICICIBANK-EQ -1 3 2 0 CNC
# 5 NSE:ICICIBANK-EQ -1 3 2 0 CNC
# 5 NSE:ICICIBANK-EQ -1 3 2 0 CNC

ticker_name = "NSE:ICICIBANK-EQ"
ticker_name = "NSE:NIFTY24JANFUT"
ticker_name = "NSE:BATAINDIA-EQ"


OrderType.stoploss_limit.value
fyers_service.place_buy_market(ticker_name, 1, ProductType.CNC.value, tel_props)
res = fyers_client.orderbook()
response = from_dict(data_class=OrderBookResponse, data=res)

pos = fyers_service.get_positions(tel_props)
pos.get_positions_of_type(ProductType.MARGIN.value)


fyers_service.place_stoploss_for_buy_market_order(
    ticker_name=ticker_name,
    qty=1,
    stopprice=1000,
    product_type=ProductType.CNC.value,
    tel_props=tel_props,
)

userStoplosses = UserStoplosses(
    "1db30ee5-e01a-421f-9f60-bb72ffe31add",
    "1db30ee5-e01a-421f-9f60-bb72ffe31add",
    stop_losses=[],
)
stoploss_repo.update_user_stoplosses(userStoplosses, telemetry, tel_props)

userstoplosses = stoploss_repo.get_user_stoplosses(
    "1db30ee5-e01a-421f-9f60-bb72ffe31add", telemetry, tel_props
)

stoploss = Stoploss(
    "1db30ee5-e01a-421f-9f60-bb72ffe31add",
    "normal",
    ticker_name,
    1000.0,
    product_type="CNC",
    check_at="30t",
)
stoploss_repo.store_user_stoplosses(
    "1db30ee5-e01a-421f-9f60-bb72ffe31add", stoploss, telemetry, tel_props
)

all_stoplosses = stoploss_repo.get_all_stoplosses(telemetry, tel_props)
stoplosses = all_stoplosses[1].stop_losses
stoplosses = [stoploss]
fyers_service.set_stop_loss(userstoplosses.stop_losses[0], 1, tel_props)
fyers_service.set_stop_losses(userstoplosses.stop_losses, tel_props)

fyers_service.place_stoploss_for_buy_market_order(
    ticker_name=ticker_name,
    qty=2,
    stopprice=990,
    product_type=ProductType.CNC.value,
    tel_props=tel_props,
)


# -----------------
# ---------
# ---------
# ---------
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
fyers_service.place_buy_market(ticker_name, qty, ProductType.CNC.value, tel_props)

# Able to set stoploss for buy CNC order, once the stopprice is reached the order gets executed
# This doesnt get executed when there is no holding or active position for given quantity
fyers_service.place_stoploss_for_buy_market_order(
    ticker_name, qty, 121.7, ProductType.cnc, tel_props
)

fyers_client.funds()
fyers_client.holdings()


fyers_client.positions()
