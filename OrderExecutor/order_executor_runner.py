import azure.functions as func
from SharedCode.Models.Order.order_message import OrderMessage, OrderConstants
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
import json
from SharedCode.Repository.Fyers.fyers_service import FyersService
from dataclasses import asdict

telemetry = LoggerService()
kv_service = KeyVaultService()



telemetry = LoggerService()
kv_service = KeyVaultService()


def place_margin_order(order_message:OrderMessage, tel_props):
    tel_props = tel_props.copy()
    telemetry.info(f"Executing market order: {order_message}", tel_props)
    fyers_service = FyersService.from_kv_secret_name(order_message.kv_secret_name, kv_service)
    
    
def place_cnc_order(order_message:OrderMessage, tel_props):
    tel_props = tel_props.copy()
    telemetry.info(f"Executing cnc order: {order_message}", tel_props)
    fyers_service = FyersService.from_kv_secret_name(order_message.kv_secret_name, kv_service)
    
def place_stoploss_order(order_message:OrderMessage, tel_props):
    tel_props = tel_props.copy()
    telemetry.info(f"Executing stoploss order: {order_message}", tel_props)
    fyers_service = FyersService.from_kv_secret_name(order_message.kv_secret_name, kv_service)
    # user_stoplosses =  asdict(order_message.orders)
    fyers_service.set_stop_losses(order_message.orders, tel_props)
    
    
def order_executor_runner(order_message:OrderMessage, tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"message":order_message, "user_id":order_message.user_id, "order_message":asdict(order_message)} )
    telemetry.info(f"Executing order: {order_message}", tel_props)    
    
    if order_message.order_type == OrderConstants.order_type_stoploss:
        place_stoploss_order(order_message, tel_props)
    
    elif order_message.order_type == OrderConstants.order_type_margin:
        place_margin_order(order_message, tel_props)
        
    elif order_message.order_type == OrderConstants.order_type_cnc:
        place_cnc_order(order_message, tel_props)
    
    