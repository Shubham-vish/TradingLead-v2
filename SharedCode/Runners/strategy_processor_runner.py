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

telemetry = LoggerService()
kv_service = KeyVaultService()



def place_order(signal_message:SignalMessage, tel_props):
    tel_props = tel_props.copy()
    telemetry.info(f"Executing market order: {signal_message}", tel_props)
    
    
    
def strategy_processor_runner(signal_message:SignalMessage, tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"message":signal_message, "user_id":signal_message.user_id, "signal_message":asdict(signal_message)} )
    telemetry.info(f"Processing Strategy signal: {signal_message}", tel_props)
    telemetry.info(f"Executing order: {signal_message}", tel_props)    
    
    if signal_message.signal == True:
        telemetry.info(f"Signal side buy: {signal_message}", tel_props)
    
    elif signal_message.signal == False:
        telemetry.info(f"Signal side sell: {signal_message}", tel_props)
    else:
        telemetry.info(f"Signal side not supported: {signal_message}", tel_props)
    
    
    