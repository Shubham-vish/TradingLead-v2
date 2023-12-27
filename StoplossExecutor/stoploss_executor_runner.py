from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
from SharedCode.Utils.constants import Constants
from SharedCode.Models.Order.user_stoplosses import UserStoplosses
from SharedCode.Repository.CosmosDB.user_repository import UserRepository
import concurrent.futures
import json
from SharedCode.Models.Order.order_message import OrderMessage
from SharedCode.Repository.ServiceBus.servicebus_service import ServiceBusService
from dataclasses import asdict
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, Stoploss
from SharedCode.Models.user import User
from SharedCode.Repository.Fyers.fyers_service import FyersService
from SharedCode.Models.Fyers.holdings_response import HoldingsResponse
from SharedCode.Models.Fyers.net_positions_response import NetPositionResponse
from SharedCode.Models.Fyers.quote_response import QuoteResponse, TickerLtp
from typing import List

kv_service = KeyVaultService()
telemetry = LoggerService()
user_repository = UserRepository()
sb_service = ServiceBusService()

operation_id = "RandomOperationId"
order_topic_name = kv_service.get_secret(Constants.ORDER_TOPIC_NAME)


def check_and_execute_stoploss(stoploss:Stoploss, fyers_service:FyersService, user:User, curr_qty:int, ltp:float, tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"action": "check_and_execute_stoploss", "stoploss": json.dumps(asdict(stoploss)), "user_id": user.id})
    
    is_ltp_greater = ltp > stoploss.price
    if is_ltp_greater and curr_qty < stoploss.qty:
        telemetry.info(f"Buy Triggered for ticker: {stoploss.ticker} as ltp: {ltp} is greater than stoploss price: {stoploss.price} and cur_qty: {curr_qty} is less than stoploss qty: {stoploss.qty}", tel_props)
        fyers_service.place_buy_market(stoploss.ticker, stoploss.qty - curr_qty, stoploss.product_type, tel_props)
    elif not is_ltp_greater and curr_qty > 0:
        telemetry.info(f"Sell triggered for ticker: {stoploss.ticker} as ltp: {ltp} is less than stoploss price: {stoploss.price} and cur_qty: {curr_qty} is more than 0", tel_props)
        fyers_service.place_sell_market(stoploss.ticker, curr_qty, stoploss.product_type, tel_props)
    else:
        telemetry.info(f"Stoploss Sell/Buy not triggered for ticker: {stoploss.ticker} as ltp: {ltp} is greater than stoploss price: {stoploss.price} and cur_qty: {curr_qty} is greater than stoploss qty: {stoploss.qty}", tel_props)
    

def execute_stoploss_for_user(user_stoplosses:UserStoplosses, tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"action": "execute_stoploss_for_user", "user_stoplosses": json.dumps(asdict(user_stoplosses)), "user_id": user_stoplosses.user_id})
    stoplosses = user_stoplosses.get_30t_line_stoplosses()
    
    if stoplosses is None or len(stoplosses) == 0:
        telemetry.info(f"No get_30t_line_stoplosses stoplosses found for user: {user_stoplosses.user_id}", tel_props)
        return True, user_stoplosses.user_id
    
    try:
        telemetry.info(f"Checking stoploss trigger for user: {user_stoplosses.id} : stoplosses: {asdict(stoplosses)}", tel_props)
        
        user = user_repository.get_user(user_stoplosses.user_id, telemetry, tel_props)
        
        fyers_service = FyersService.from_kv_secret_name(user.kv_secret_name, kv_service)        
        exceptions = []
        
        holdings = fyers_service.get_holdings(tel_props)
        positions = fyers_service.get_positions(tel_props)
        quote_req = user_stoplosses.get_quote_dict()
        quote_response = fyers_service.get_quote(quote_req, tel_props)
        ticker_and_ltp = quote_response.get_ticker_and_ltp()
        
        for stoploss in stoplosses:
            try:
                ltp = next((item for item in ticker_and_ltp if item.ticker == stoploss.ticker), None)
                curr_qty = holdings.get_quantity(stoploss.ticker) + positions.get_quantity(stoploss.ticker)
                check_and_execute_stoploss(stoploss, fyers_service, user,curr_qty, ltp, tel_props)
            except Exception as e:
                telemetry.exception(f"Error occurred while checking stoploss trigger for user: {user_stoplosses.id} : stoploss: {asdict(stoploss)}", tel_props)
                exceptions.append((e, asdict(stoploss)))
        telemetry.info(f"Stoploss set successfully for {asdict(user_stoplosses)}", tel_props)
        
        if len(exceptions) > 0:
            tel_props = tel_props.copy()
            tel_props.update({"exceptions": exceptions})
            telemetry.error(f"Stoploss set successfully for {asdict(user_stoplosses)} but with exceptions: {exceptions}", tel_props)
            raise Exception(exceptions)
        
        return True, user_stoplosses.user_id
    except Exception as e:
        msg = f"An error occurred while setting stoploss for {asdict(user_stoplosses)}: {e}"
        telemetry.exception(msg, tel_props)
        return False, user_stoplosses.user_id
    
    
def execute_stoplosses_for_all_users(tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"action": "execute_stoplosses_for_all_users"})
    stoploss_repo = StoplossesRepository()
    users_stoplosses = stoploss_repo.get_all_stoplosses(telemetry, tel_props)
    
    if (not users_stoplosses) or (len(users_stoplosses) == 0):
        telemetry.info("No stoplosses found", tel_props)
        return
    
    telemetry.info(f"execute_stoplosses_for_all_users started with userStoplosses count: {len(users_stoplosses)}", tel_props)
    results = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(execute_stoploss_for_user, users_stoplosses, tel_props)
        futures = [executor.submit(execute_stoploss_for_user, user_stoplosses, tel_props) for user_stoplosses in users_stoplosses]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                if result:
                    success, user_id = result
                    if success:
                        telemetry.info(f"Stoploss execute successfully for user ID: {user_id}", tel_props)
                    else:
                        telemetry.info(f"Failed to execute stoploss for user ID: {user_id}", tel_props)
                else:
                    telemetry.error(f"Task failed: {result}", tel_props)
            except Exception as e:
                telemetry.exception(f"Task resulted in an exception: {e}", tel_props)
                raise e
        
    telemetry.info("execute_stoplosses_for_all_users completed", tel_props)
    return results


def stoploss_executor_runner(tel_props):
    execute_stoplosses_for_all_users(tel_props)
    telemetry.info("stoploss_executor_runner completed", tel_props)