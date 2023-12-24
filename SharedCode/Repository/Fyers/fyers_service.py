from typing import List

from .fyers_client_factory import FyersClientFactory
from ..Logger.logger_service import LoggerService
from .Models.fyers_constants import (
    ProductType,
    OrderSide,
    OrderType,
    Response,
)

from .Models.NetPositionResponse import (
    NetPositionResponse,
    NetPosition,
)
import pandas as pd
from datetime import timedelta
telemetry = LoggerService()


class FyersService:
    def __init__(self, client_details):
        self.fyers_client = FyersClientFactory.get_fyers_client(client_details)
        
    
    def place_buy_market(
        self, ticker_name: str, qty: int, product_type: str, tel_props={}
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

        tel_props.update(
            {
                "ticker_name": ticker_name,
                "qty": qty,
                "product_type": product_type,
                "order_type": "market",
                "side": "buy",
                "action": "place_buy_market_order",
            }
        )

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
            return response
        except Exception as e:
            telemetry.exception(f"Error in placing buy market: {data} : {e}", tel_props)
            raise e

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
        tel_props.update(
            {
                "ticker_name": ticker_name,
                "qty": qty,
                "product_type": product_type,
                "order_type": "stoploss",
                "side": "buy",
                "action": "place_stoploss_for_buy_market_order",
            }
        )

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
            return respnose
        except Exception as e:
            telemetry.exception(f"Error in placing stoploss: {data} : {e}", tel_props)
            raise

    def exit_positions(self, position_ids: List[str], tel_props):
        tel_props.update({"position_ids": position_ids})
        try:
            if not position_ids:
                raise ValueError("No position IDs provided")

            data = {"id": position_ids}
            response = self.fyers_client.exit_positions(data=data)
            telemetry.info(
                f"Exiting positions response for {data}: {response}", tel_props
            )
            return response
        except Exception as e:
            telemetry.exception(f"Error in exiting positions: {e}", tel_props)
            raise

    def exit_all_positions(self, tel_props):
        tel_props.update({"position_ids": "all", "action": "exit_all_positions"})
        try:
            data = {}
            response = self.fyers_client.exit_positions(data)
            telemetry.log(f"Exiting all positions response: {response}", tel_props)
            return response
        except Exception as e:
            telemetry.exception(f"Error in exiting positions: {e}", tel_props)
            raise e

    def get_positions(self, tel_props):
        tel_props.update({"action": "get_positions"})
        try:
            res = self.fyers_client.positions()
            telemetry.info(f"Returning positions response: {res}", tel_props)
            response = NetPositionResponse.from_dict(res)

            if response.s == Response.OK:
                return response
            else:
                telemetry.exception(f"Invalid Response: {res}", tel_props)
                return None
        except Exception as e:
            telemetry.exception(f"Error in exiting positions: {e}", tel_props)
            raise e

    def history(self, ticker, range_from, range_to, resolution, tel_props):
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