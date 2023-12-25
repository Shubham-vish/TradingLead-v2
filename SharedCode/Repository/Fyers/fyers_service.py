from typing import List

from .fyers_client_factory import FyersClientFactory
from ..Logger.logger_service import LoggerService

from SharedCode.Models.fyers_constants import (
    ProductType,
    OrderSide,
    OrderType,
    Response,
)

from SharedCode.Models.net_positions_response import (
    NetPositionResponse,
    NetPosition,
)

from SharedCode.Models.holdings_response import HoldingsResponse, Holding
from SharedCode.Models.orderbook_response import OrderBookResponse, OrderBook
from SharedCode.Models.user_stoplosses import Stoploss
import pandas as pd
from datetime import timedelta
from SharedCode.Utils.constants import Constants
telemetry = LoggerService()


class FyersService:
    def __init__(self, client_details):
        self.fyers_client = FyersClientFactory.get_fyers_client(client_details)
        self.fyers_username = client_details[Constants.fyers_username]
        self.client_id = client_details[Constants.client_id]
        
    
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
        
        
        for attempt in range(3):
            try:
                data = {
                    "symbol": ticker_name,
                    "qty": qty,
                    "type": OrderType.market,
                    "side": OrderSide.buy,
                    "productType": product_type,
                    "stoploss": 0,
                    "stopprice": 0,
                    "validity": "DAY",
                    "disclosedQty": 0,
                    "offlineOrder": False,
                }
                response = self.fyers_client.place_order(data)
                telemetry.info(
                    f"Placing buy market response for {data}: {response}", tel_props
                )
                
                if response["s"] == Response.OK:
                    telemetry.info(f"Placing buy market response OK for {data}", tel_props)
                    return response
                else:
                    msg = f"Invalid Response while placing buy market:{data} response:{response}"
                    telemetry.exception(msg, tel_props)
                    raise Exception(msg)
            except Exception as e:
                telemetry.exception(f"Error in placing buy market, attempt: {attempt}, error: {e}", tel_props)
                continue
        msg = f"Max retries in placing buy market, error"
        telemetry.exception(msg, tel_props)
        raise Exception(msg)

    def place_stoploss_for_buy_market_order(
        self,
        ticker_name: str,
        qty: int,
        stopprice: float,
        product_type: str,
        tel_props,
    ):
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
                    "type": OrderType.stoploss_market,
                    "side": OrderSide.sell,
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
                response = HoldingsResponse(**res)

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
                response = OrderBookResponse.from_dict(res)

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
        tel_props.update({"action": "setStoploss", "stoploss": stoploss.to_dict(), "qty": qty})
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
        tel_props.update({"action": "setStoplosses", "stoplosses": [stoploss.to_dict() for stoploss in stoplosses], Constants.fyers_user_name: self.fyers_username, Constants.client_id: self.client_id})
        
        positions = self.get_positions(tel_props)
        telemetry.info(f"Positions: {positions}", tel_props)
        
        hldng_res = self.get_holdings(tel_props)
        pos_res = self.get_positions(tel_props)
        orderbook = self.get_order_book(tel_props)
        exception_occurred = False
        
        for stoploss in stoplosses:
            
            try:
                telemetry.info(f"Processing stoploss: {stoploss}", tel_props)    
                
                qty_positions = pos_res.get_qty(stoploss.ticker)
                qty_holdings = hldng_res.get_qty(stoploss.ticker)
                
                qty = qty_positions + qty_holdings
                
                if not orderbook.is_same_order_present(stoploss.ticker, qty):
                    cur_orders = orderbook.get_orders_for_ticker(stoploss.ticker)
                    telemetry.info(f"Current orders: {cur_orders}", tel_props)
                    if cur_orders:
                        self.cancel_orders([order.id for order in cur_orders], tel_props)
                        telemetry.info(f"Exited current orders: {cur_orders}", tel_props)
                    if self.set_stop_loss(stoploss, qty, tel_props):
                        telemetry.info(f"Stoploss set for {stoploss}", tel_props)
                    else:
                        exception_occurred = True
                        telemetry.info(f"Stoploss not set for -> {stoploss.ticker}, {qty}", tel_props)
                    
            except Exception as e:
                telemetry.exception(f"Error in getting qty: {stoploss}", tel_props)
                exception_occurred = True
                
        if exception_occurred:
            msg = f"Error in setting stoplosses"
            telemetry.exception(msg, tel_props)
            raise Exception(msg)
                
            
    # Apis to get History data
    # No retries implemented as of now
    # 
    def history(self, ticker, range_from, range_to, resolution, tel_props):
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
                return df
            else:
                telemetry.exception(f"Invalid Response: {response}", tel_props)
            return response
        except Exception as e:
            telemetry.exception(f"Error in fetching history: {e}")
            raise e

    def fetch_deep_history(self, ticker, range_from, range_to, resolution, tel_props):
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