import azure.functions as func
from SharedCode.Models.Order.order_message import OrderMessage, OrderSide
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
import json
from SharedCode.Repository.Fyers.fyers_service import FyersService
from dataclasses import asdict
from SharedCode.Models.Strategy.signal_message import SignalMessage
from SharedCode.Repository.CosmosDB.strategy_repository import StrategyRepository

telemetry = LoggerService()
kv_service = KeyVaultService()
strategy_repo = StrategyRepository()


def place_order(signal_message:SignalMessage, tel_props):
    tel_props = tel_props.copy()
    telemetry.info(f"Executing market order: {signal_message}", tel_props)
    
    
    
def strategy_processor_runner(signal_message:SignalMessage, tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"message":signal_message, "user_id":signal_message.user_id, "signal_message":asdict(signal_message)} )
    telemetry.info(f"Processing Strategy signal: {signal_message}", tel_props)
    
    if signal_message.to_do_something():
        if signal_message.to_buy():
            telemetry.info(f"Executing market buy: {signal_message}", tel_props)
            fyers_service = FyersService.from_kv_secret_name(signal_message.kv_secret_name, kv_service)
            fyers_service.place_buy_market(signal_message.trade_ticker, signal_message.quantity, signal_message.product_type, tel_props)
            telemetry.info(f"Executed market buy: {signal_message}", tel_props)
        elif signal_message.to_sell():
            telemetry.info(f"Executing market sell: {signal_message}", tel_props)
            fyers_service = FyersService.from_kv_secret_name(signal_message.kv_secret_name, kv_service)
            fyers_service.place_sell_market(signal_message.trade_ticker, signal_message.quantity, signal_message.product_type, tel_props)
            telemetry.info(f"Executed market sell: {signal_message}", tel_props)
        else:
            telemetry.exception(f"Signal side not supported: {signal_message}", tel_props)
            return
        
        strategy_repo.strategy_executed_for_user(signal_message)
    else:
        telemetry.info(f"Nothing to do for signal: {signal_message}", tel_props)
    
    
    