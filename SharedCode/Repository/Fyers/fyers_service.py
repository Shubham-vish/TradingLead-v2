from datetime import datetime, timedelta
from .fyers_client_factory import FyersClientFactory

from ..Logger.logger_service import LoggerService
telemetry = LoggerService()

class FyersService:

    def __init__(self, client_details):
        self.fyers_client = FyersClientFactory.get_fyers_client(client_details)

    def history(self, data=None):
        if data is None:
            data = {
                "symbol":"NSE:ICICIBANK-EQ",
                "resolution":"60",
                "date_format":"1",
                "range_from":"2023-10-10",
                "range_to":"2023-12-30",
                "cont_flag":"1"
            }
        return self.fyers_client.history(data)

    def get_close_data(self, ticker_name, tf="60",tel_props={}):
        try:
            range_to = datetime.now() + timedelta(days = 2)
            range_from = datetime.now() + timedelta(days = -4)

            range_from = range_from.strftime('%Y-%m-%d')
            range_to = range_to.strftime('%Y-%m-%d')

            data = {
                "symbol":ticker_name,
                "resolution":tf,
                "date_format":"1",
                "range_from":range_from,
                "range_to":range_to,
                "cont_flag":"1"
            }

            response = self.fyers_client.history(data=data)
            print("Api response :",response["s"])
            candles = response["candles"]
            close_prices = [candle[-2] for candle in candles]
            stoploss = response["candles"][-1][-3]
            return close_prices
        except Exception as e:
            telemetry.warning(f"Error in fetching history data {data}.\nError: {e}", properties=tel_props)

    def execute_trade(self, client_id, token, trade_data):
        # Get the client from the factory
        # client = self.client_factory.create_client(client_id, token)

        # Placeholder for actual trade execution logic
        # For example, using client to place an order
        # response = client.place_order(trade_data)
        # return response

        # For demonstration, just printing a message
        print(f"Executing trade for client {client_id} with data: {trade_data}")

    def cancel_trade(self, client_id, token, trade_id):
        # Get the client from the factory
        # client = self.client_factory.create_client(client_id, token)

        # Placeholder for actual trade cancellation logic
        # For example, using client to cancel an order
        # response = client.cancel_order(trade_id)
        # return response

        # For demonstration, just printing a message
        print(f"Cancelling trade {trade_id} for client {client_id}")

# # Example usage:
# # Initialize the client factory
# client_factory = FyersClientFactory()

# # Create an instance of FyersService
# fyers_service = FyersService(client_factory)

# # Example client and trade data
# client_id = "user123"
# token = "token_abc"
# trade_data = {"symbol": "NSE:RELIANCE", "quantity": 10, "type": "BUY"}

# # Execute a trade
# fyers_service.execute_trade(client_id, token, trade_data)

# # Cancel a trade
# trade_id = "trade123"
# fyers_service.cancel_trade(client_id, token, trade_id)
