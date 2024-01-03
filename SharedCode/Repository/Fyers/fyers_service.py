from typing import List

from .fyers_client_factory import FyersClientFactory
from ..Logger.logger_service import LoggerService

from SharedCode.Models.Fyers.fyers_constants import (
    ProductType,
    OrderSide,
    OrderType,
    Response,
)

from SharedCode.Models.Fyers.net_positions_response import (
    NetPositionResponse,
    NetPosition,
)

from SharedCode.Models.Fyers.holdings_response import HoldingsResponse, Holding
from SharedCode.Models.Fyers.orderbook_response import OrderBookResponse, OrderBook
from SharedCode.Models.Fyers.quote_response import QuoteResponse
from SharedCode.Models.Order.user_stoplosses import Stoploss
import pandas as pd
from datetime import timedelta
from SharedCode.Utils.constants import Constants
import json
from dacite import from_dict
from dataclasses import asdict
from SharedCode.Models.Order.order import Order
telemetry = LoggerService()


class FyersService:
    def __init__(self, client_details):
        self.fyers_client = FyersClientFactory.get_fyers_client(client_details)
        self.fyers_username = client_details[Constants.fyers_username]
        self.client_id = client_details[Constants.client_id]
        
    @staticmethod
    def from_kv_secret_name(kv_secret_name, kv_service):
        fyers_details_json = kv_service.get_secret(kv_secret_name)
        fyers_details = json.loads(fyers_details_json)
        return FyersService(fyers_details)
    
    
    def place_order(self, ticker_name: str, qty: int, product_type: str, side: OrderSide, tel_props):
        tel_props = tel_props.copy()
        side_str = "buy" if side == OrderSide.buy.value else "sell"    
        
        tel_props.update(
            {
                "side": side_str,
                "action": "place_order",
            }
        )
        
        for attempt in range(3):
            try:
                data = {
                    "symbol": ticker_name,
                    "qty": qty,
                    "type": OrderType.market.value,
                    "side": side,
                    "productType": product_type,
                    "stoploss": 0,
                    "stopprice": 0,
                    "validity": "DAY",
                    "disclosedQty": 0,
                    "offlineOrder": False,
                }
                response = self.fyers_client.place_order(data)
                telemetry.info(
                    f"Placing {side_str} market response for {data}: {response}", tel_props
                )
                
                if response["s"] == Response.OK:
                    telemetry.info(f"Placing {side_str} market response OK for {data}", tel_props)
                    return response
                else:
                    msg = f"Invalid Response while placing {side_str} market:{data} response:{response}"
                    telemetry.exception(msg, tel_props)
                    raise Exception(msg)
            except Exception as e:
                telemetry.exception(f"Error in placing {side_str} market, attempt: {attempt}, error: {e}", tel_props)
                continue
        msg = f"Max retries in placing {side_str} market, error"
        telemetry.exception(msg, tel_props)
        raise Exception(msg)
    
    def place_buy_market(
        self, ticker_name: str, qty: int, product_type: str, tel_props
    ):
        """
        # Able to place buy order in CNC
        # ticker_name = "NSE:LEMONTREE-EQ"
        # qty = 1
        # productType = "CNC"
        # fyers_service.place_buy_market(ticker_name, qty, productType, tel_props)


        # # Able to place buy order in Margin Nifty Fut Order for 1 lot

        # ticker_name = "NSE:NIFTY24JANFUT"
        # qty = 50
        # productType = "MARGIN"
        # fyers_service.place_buy_market(ticker_name, qty, productType, tel_props)
        """

        tel_props = tel_props.copy()
        tel_props.update(
            {
                "ticker_name": ticker_name,
                "qty": qty,
                "product_type": product_type,
                "order_type": "market",
                "side": "buy",
                "action": "place_buy_market_order",
                Constants.fyers_user_name: self.fyers_username,
                Constants.client_id: self.client_id,
            }
        )
        
        return self.place_order(ticker_name, qty, product_type, OrderSide.buy.value, tel_props)
    
    def place_sell_market(
        self, ticker_name: str, qty: int, product_type: str, tel_props
    ):
        tel_props = tel_props.copy()
        tel_props.update(
            {
                "ticker_name": ticker_name,
                "qty": qty,
                "product_type": product_type,
                "order_type": "market",
                "side": "sell",
                "action": "place_sell_market_order",
                Constants.fyers_user_name: self.fyers_username,
                Constants.client_id: self.client_id,
            }
        )
        
        return self.place_order(ticker_name, qty, product_type, OrderSide.sell.value, tel_props)
    
    def place_stoploss_for_buy_market_order(
        self,
        ticker_name: str,
        qty: int,
        stopprice: float,
        product_type: str,
        tel_props,
    ):
        # For CNC it will not place order for the quantity more than positions plus holding
        """_summary_
        # Able to set stoploss for Nifty future buy position, Once the stopprice is reached the order gets executed
        # but if position is buy position is not there it will create a nakes sell position


        ticker_name = "NSE:NIFTY24JANFUT"
        qty = 50
        productType = "MARGIN"
        fyers_service.execute_stop_loss_for_buy_market(ticker_name, qty, 21400, productType, tel_props)

        ticker_name = "NSE:LEMONTREE-EQ"
        qty = 1
        productType = "CNC"
        # Able to set stoploss for buy CNC order, once the stopprice is reached the order gets executed
        # This doesnt get executed when there is no holding or active position for given quantity
        fyers_service.execute_stop_loss_for_buy_market(ticker_name, qty, 121.7, productType, tel_props)
        """
        tel_props = tel_props.copy()
        tel_props.update(
            {
                "ticker_name": ticker_name,
                "qty": qty,
                "product_type": product_type,
                "order_type": "stoploss",
                "side": "buy",
                "action": "place_stoploss_for_buy_market_order",
                Constants.fyers_user_name: self.fyers_username,
                Constants.client_id: self.client_id,
            }
        )

        
        for attempt in range(3):
            try:
                data = {
                    "symbol": ticker_name,
                    "qty": qty,
                    "type": OrderType.stoploss_market.value,
                    "side": OrderSide.sell.value,
                    "productType": product_type,
                    "stoploss": 0,
                    "stopprice": stopprice,
                    "validity": "DAY",
                    "disclosedQty": 0,
                    "offlineOrder": False,
                }
                
                respnose = self.fyers_client.place_order(data=data)
                telemetry.info(
                    f"Placing stoploss response for {data}: {respnose}", tel_props
                )
                
                if respnose["s"] == Response.OK:
                    telemetry.info(f"Placing stoploss response OK for {data}", tel_props)
                    return respnose
                else:
                    msg = f"Invalid Response while placing stoploss:{data} response:{respnose}"
                    telemetry.exception(msg, tel_props)
                    raise Exception(msg)
            except Exception as e:
                telemetry.exception(f"Error in placing stoploss, attempt: {attempt}, data: {data}, error : {e}", tel_props)
                continue
        msg = f"Max retries in placing stoploss, data: {data}, error"
        telemetry.exception(msg, tel_props)
        raise Exception(msg)
    

    def exit_positions(self, position_ids: List[str], tel_props):
        tel_props = tel_props.copy()
        tel_props.update({"position_ids": position_ids, Constants.fyers_user_name: self.fyers_username,
                Constants.client_id: self.client_id})
    
        
        for attempt in range(3):
            try:
                if not position_ids:
                    raise ValueError("No position IDs provided")

                data = {"id": position_ids}
                response = self.fyers_client.exit_positions(data=data)
                telemetry.info(
                    f"Exiting positions response for {data}: {response}", tel_props
                )
                
                if response["s"] == Response.OK:
                    telemetry.info(f"Exiting positions response OK for {data}", tel_props)
                    return response
                else:
                    msg = f"Invalid Response while exiting positions:{data} response:{response}"
                    telemetry.exception(msg, tel_props)
                    raise Exception(msg)
            except Exception as e:
                telemetry.exception(f"Error in exiting positions, attempt: {attempt}, error: {e}", tel_props)
                continue
        msg = f"Max retries in exiting positions. Error in exiting positions"
        telemetry.exception(msg, tel_props)
        raise Exception(msg)

    def exit_all_positions(self, tel_props):
        tel_props = tel_props.copy()
        tel_props.update(
                {
                "position_ids": "all", 
                "action": "exit_all_positions", 
                Constants.fyers_user_name: self.fyers_username,
                Constants.client_id: self.client_id,
                } 
            )
        
        for attempt in range(3):
            try:
                data = {}
                response = self.fyers_client.exit_positions(data)
                telemetry.log(f"Exiting all positions response: {response}", tel_props)
                if response["s"] == Response.OK:
                    telemetry.info(f"Exiting all positions response OK", tel_props)
                    return response
                else :
                    msg = f"Invalid Response while exiting all positions: {response}"
                    telemetry.exception(msg, tel_props)
                    raise Exception(msg)
            except Exception as e:
                telemetry.exception(f"Error in exiting all positions, attempt: {attempt}, error: {e}", tel_props)
                continue
        msg = f"Max retries in exiting all positions. Error in exiting all positions"
        telemetry.exception(msg, tel_props)
        raise Exception(msg)
    
    
    def get_positions(self, tel_props)-> NetPositionResponse:
        tel_props = tel_props.copy()
        tel_props.update({"action": "get_positions", Constants.fyers_user_name: self.fyers_username,
                Constants.client_id: self.client_id})
        
        
        for attempt in range(3):
            try:
                res = self.fyers_client.positions()
                telemetry.info(f"Returning positions response: {res}", tel_props)
                response = NetPositionResponse.from_dict(res)

                if response.s == Response.OK:
                    return response
                else:
                    msg = f"Invalid Response while fetching positions: {res}"
                    telemetry.exception(msg, tel_props)
                    raise Exception(msg)
            except Exception as e:
                telemetry.exception(f"Error in getting positions, attempt: {attempt}, error: {e}", tel_props)
                continue
        msg = f"Max retries in getting positions. Error in getting positions"
        telemetry.exception(msg, tel_props)
        raise Exception(msg)


    def get_holdings(self, tel_props) -> HoldingsResponse:
        tel_props = tel_props.copy()
        tel_props.update({"action": "get_holdings", Constants.fyers_user_name: self.fyers_username,
                Constants.client_id: self.client_id,})
        
        for attempt in range(3):
            try:
                res = self.fyers_client.holdings()
                telemetry.info(f"Returning holdings response: {res}", tel_props)
                response = from_dict(data_class=HoldingsResponse, data=res)

                if response.s == Response.OK:
                    return response
                else:
                    msg = f"Invalid Response while fetchig holdings: {res}"
                    telemetry.exception(msg, tel_props)
                    raise Exception(msg)
            except Exception as e:
                telemetry.exception(f"Error in getting holdings, attempt: {attempt}, error: {e}", tel_props)
                continue
        msg = f"Max retries in getting holdings. Error in getting holdings"
        telemetry.exception(msg, tel_props)
        raise Exception(msg)
    
    
    def get_order_book(self, tel_props) -> OrderBookResponse:
        tel_props = tel_props.copy()
        tel_props.update({"action": "get_order_book", Constants.fyers_user_name: self.fyers_username,
                Constants.client_id: self.client_id,})
        
        for attempt in range(3):
            try:
                res = self.fyers_client.orderbook()
                telemetry.info(f"Returning Order Book response: {res}", tel_props)
                response = from_dict(data_class=OrderBookResponse, data=res)

                if response.s == Response.OK:
                    return response
                else:
                    msg = f"Invalid Response while getting orderbook: {res}"
                    telemetry.exception(msg, tel_props)
                    raise Exception(msg)
            except Exception as e:
                telemetry.exception(f"Error in getting Order Book, attempt: {attempt}, error: {e}", tel_props)
                continue
        msg = f"Max retries in getting Order Book. Error in getting Order Book"
        telemetry.exception(msg, tel_props)
        raise Exception(msg)
    
    def cancel_orders(self, order_ids: List[str], tel_props):
        tel_props = tel_props.copy()
        tel_props.update({"action": "cancel_orders", "order_ids": order_ids, Constants.fyers_user_name: self.fyers_username,
                Constants.client_id: self.client_id})
        
        
        for attempt in range(3):
            try:
                if not order_ids:
                    telemetry.exception(f"No order IDs provided", tel_props)
                    return None

                data = [{"id": order_id} for order_id in order_ids]
                response = self.fyers_client.cancel_basket_orders(data=data)
                telemetry.info(
                    f"Cancel orders response for {data}: {response}", tel_props
                )
                
                if response["s"] == Response.OK:
                    telemetry.info(f"Cancelled orders response OK for {data}", tel_props)
                    return response
                else:
                    msg = f"Invalid Response while cancelling orders:{data} response:{response}"
                    telemetry.exception(msg, tel_props)
                    raise Exception(msg)
            except Exception as e:
                telemetry.exception(f"Error in cancelling orders, attempt {attempt}, error: {e}", tel_props)
                continue
        msg = f"Max retries in cancelling orders. Error in cancelling orders"
        telemetry.exception(msg, tel_props)
        raise Exception(msg)
    
        
    def set_stop_loss(self, stoploss: Stoploss, qty, tel_props):
        tel_props = tel_props.copy()
        tel_props.update({"action": "setStoploss", "stoploss": asdict(stoploss), "qty": qty})
        telemetry.info(f"Processing stoploss: {stoploss.ticker}, {qty}", tel_props)
        response = self.place_stoploss_for_buy_market_order(
            stoploss.ticker,
            qty,
            stoploss.price,
            stoploss.product_type,
            tel_props,
        )
        
        return response
        
    
    
    def set_stop_losses(self, stoplosses: List[Stoploss], tel_props):
        
        tel_props = tel_props.copy()
        tel_props.update({"action": "setStoplosses", "stoplosses": [asdict(stoploss) for stoploss in stoplosses], Constants.fyers_user_name: self.fyers_username, Constants.client_id: self.client_id})
        
        telemetry.info(f"Processing stoplosses: {stoplosses}", tel_props)
        
        hldng_res = self.get_holdings(tel_props)
        pos_res = self.get_positions(tel_props)
        orderbook = self.get_order_book(tel_props)
        
        telemetry.info(f"Current holdings: {hldng_res}", tel_props)  
        telemetry.info(f"Current positions: {pos_res}", tel_props)
        telemetry.info(f"Current orderbook: {orderbook}", tel_props)
        exception_occurred = False
        
        for stoploss in stoplosses:
            
            try:
                telemetry.info(f"Processing stoploss: {stoploss}", tel_props)    
                
                qty_positions = pos_res.get_quantity(stoploss.ticker)
                qty_holdings = hldng_res.get_quantity(stoploss.ticker)
                
                qty = qty_positions + qty_holdings
                telemetry.info(f"Qty for {stoploss.ticker}: {qty}", tel_props)
                if not orderbook.is_same_stoploss_present(stoploss.ticker, qty):
                    cur_orders = orderbook.get_stoploss_orders_for_ticker(stoploss.ticker)
                    if cur_orders:
                        telemetry.info(f"Current orders already exist for {stoploss.ticker}, {qty}: {cur_orders}", tel_props)
                        self.cancel_orders([order.id for order in cur_orders], tel_props)
                        telemetry.info(f"Exited current orders for {stoploss.ticker}, {qty}: {cur_orders}", tel_props)
                    else:
                        telemetry.info(f"No current orders for {stoploss.ticker}, {qty}", tel_props)
                    
                    response = self.set_stop_loss(stoploss, qty, tel_props)
                    telemetry.info(f"Stoploss set for {stoploss}", tel_props)
                else:
                    telemetry.info(f"Stoploss already set for -> {stoploss.ticker}, {qty}", tel_props)
            except Exception as e:
                telemetry.exception(f"Error in getting qty: {stoploss}, {e}", tel_props)
                exception_occurred = True
                
    def place_orders(self, orders: List[Order], tel_props):
        
        tel_props = tel_props.copy()
        tel_props.update({"action": "place_orders", "orders": [asdict(order) for order in orders], Constants.fyers_user_name: self.fyers_username, Constants.client_id: self.client_id})
        telemetry.info(f"Processing orders: {orders}", tel_props)
        
        for order in orders:
            telemetry.info(f"Processing order: {order}", tel_props)    
            if(order.order_type == OrderType.market.value):
                if order.side == OrderSide.buy.value.value:
                    telemetry.info(f"Placing buy market order: {order}", tel_props)
                    self.place_buy_market(order.symbol, order.quantity, order.product_type, tel_props)
                elif order.side == OrderSide.sell.value.value:
                    telemetry.info(f"Placing sell market order: {order}", tel_props)
                    self.place_sell_market(order.symbol, order.quantity, order.product_type, tel_props)
                else:
                    telemetry.exception(f"Order side not supported: {order}", tel_props)
                    raise Exception(f"Order side not supported: {order}")
            else:
                telemetry.exception(f"Order type not supported: {order}", tel_props)
                raise Exception(f"Order type not supported: {order}")
            
            telemetry.info(f"Qty for {order.symbol}: {order.quantity}", tel_props)
            
            
    def is_stoploss_triggered(self, stoploss: Stoploss, hldng_res: HoldingsResponse,pos_res:NetPositionResponse , tel_props):
        
        tel_props = tel_props.copy()
        tel_props.update({"action": "is_stoploss_triggered", "stoploss": asdict(stoploss), Constants.fyers_user_name: self.fyers_username, Constants.client_id: self.client_id})
        
        telemetry.info(f"Checking stoploss trigger for {stoploss}", tel_props)
        
        qty_positions = pos_res.get_quantity(stoploss.ticker)
        qty_holdings = hldng_res.get_quantity(stoploss.ticker)
        
        qty = qty_positions + qty_holdings
        telemetry.info(f"Qty for {stoploss.ticker}: {qty}", tel_props)
        
        if qty == 0:
            telemetry.info(f"No qty for {stoploss.ticker}: {qty}", tel_props)
            return True
        
        if stoploss.is_triggered(qty):
            telemetry.info(f"Stoploss triggered for {stoploss}", tel_props)
            return True
        
        telemetry.info(f"Stoploss not triggered for {stoploss}", tel_props)
        return False
           
    # Apis to get History data
    # No retries implemented as of now
    # 
    
    def get_quote(self, quote_req, tel_props)-> QuoteResponse:
        tel_props = tel_props.copy()
        tel_props.update({"action": "get_quote", "quote_req": quote_req, Constants.fyers_user_name: self.fyers_username, Constants.client_id: self.client_id})
        
        telemetry.info(f"Fetching quote for {quote_req}", tel_props)
        for attempt in range(3):
            try:
                response = self.fyers_client.quotes(quote_req)
                
                telemetry.info(f"Fetched quote response for {quote_req}: {response}", tel_props)
                quote_res = from_dict(data_class=QuoteResponse, data=response)
                return quote_res
            except Exception as e:
                telemetry.exception(f"Error in fetching quote attempt: {attempt} for {quote_req}: {e}", tel_props)
                continue
        msg = f"Max retries in fetching quote for {quote_req}. Error in fetching quote"
        telemetry.exception(msg, tel_props)
        raise Exception(msg)

    def history(self, ticker, range_from, range_to, resolution, tel_props)->pd.DataFrame:
        tel_props = tel_props.copy()
        tel_props.update({"action": "history", "ticker": ticker, "range_from": range_from, "range_to": range_to, "resolution": resolution, Constants.fyers_user_name: self.fyers_username, Constants.client_id: self.client_id})
        telemetry.info(
            f"Fetching history for {ticker} from {range_from} to {range_to} with resolution {resolution}"
        )

        """_summary_
            # "range_from":"2023-10-10",
            # "range_to":"2023-12-30",
        """

        try:
            data = {
                "symbol": ticker,
                "resolution": resolution,
                "date_format": "1",
                "range_from": range_from,
                "range_to": range_to,
                "cont_flag": "1",
            }
            response = self.fyers_client.history(data)
            
            if response["s"] == Response.OK:
                telemetry.info(f"Fetched history response OK for {data}")
                
                cols = ["datetime", "open", "high", "low", "close", "volume"]
                df = pd.DataFrame.from_dict(response["candles"])
                df.columns = cols
                df["datetime"] = pd.to_datetime(df["datetime"], unit="s")
                df["datetime"] = df["datetime"].dt.tz_localize("utc").dt.tz_convert("Asia/Kolkata")
                df["datetime"] = df["datetime"].dt.tz_localize(None)
                df = df.set_index("datetime")
                df.drop_duplicates(inplace=True)
                return df
            else:
                telemetry.exception(f"Invalid Response: {response}", tel_props)
            return response
        except Exception as e:
            telemetry.exception(f"Error in fetching history: {e}")
            raise e

    def fetch_deep_history(self, ticker, range_from, range_to, resolution, tel_props)->pd.DataFrame:
        tel_props = tel_props.copy()
        tel_props.update({"action": "fetch_deep_history", "ticker": ticker, "range_from": range_from, "range_to": range_to, "resolution": resolution})
        
        telemetry.info(
            f"Fetching history for {ticker} from {range_from} to {range_to} with resolution {resolution}"
        , tel_props)
        
        df = pd.DataFrame()
        sd = range_from
        enddate = range_to

        n = abs((sd - enddate).days)
        ab = None
        while ab == None:
            sd = enddate - timedelta(days=n)
            ed = (sd + timedelta(days=99 if n > 100 else n)).strftime("%Y-%m-%d")
            sd = sd.strftime("%Y-%m-%d")
            dx = self.history(ticker, sd, ed, resolution, tel_props)
            df = pd.concat([df, dx])
            n = n - 100 if n > 100 else n - n
            telemetry.info(f"n : {n}", tel_props)
            if n == 0:
                ab = "done"
        return df