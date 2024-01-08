# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join("../../..")))
sys.path.append(os.path.abspath(os.path.join("..")))
from Prototyping.setupConfig import setup_config

setup_config()
# Above lines are only for local notebook testing. Not to be used in production.

import pandas as pd
from datetime import datetime, timedelta
import requests
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService

import pandas as pd
from datetime import datetime, timedelta
import requests
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, Stoploss
from dacite import from_dict
from dataclasses import asdict
from SharedCode.Repository.CosmosDB.user_repository import UserRepository
from SharedCode.Models.user import User
from SharedCode.Models.Order.order_message import OrderMessage
user_repo = UserRepository()
telemetry = LoggerService()
operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

stoploss_repo = StoplossesRepository()
user_repo = UserRepository()

all_stoplosses = stoploss_repo.get_all_stoplosses(telemetry, tel_props)


user_stoplosses = all_stoplosses[0]

user = user_repo.get_user(user_stoplosses.user_id, telemetry, tel_props)
order_message = OrderMessage.from_stoplosses(user_stoplosses.stop_losses, user)

# 

import azure.functions as func
from SharedCode.Models.Order.order_message import OrderMessage, OrderSide
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


def place_orders(order_message:OrderMessage, tel_props):
    tel_props = tel_props.copy()
    telemetry.info(f"Executing market order: {order_message}", tel_props)
    fyers_service = FyersService.from_kv_secret_name(order_message.kv_secret_name, kv_service)
    fyers_service.place_orders(order_message.orders, tel_props)
    
    
def place_stoploss_order(order_message:OrderMessage, tel_props):
    tel_props = tel_props.copy()
    telemetry.info(f"Executing stoploss order: {order_message}", tel_props)
    fyers_service = FyersService.from_kv_secret_name(order_message.kv_secret_name, kv_service)
    fyers_service.set_stop_losses(order_message.orders, tel_props)
    telemetry.info(f"Executed stoploss orders for: {order_message}", tel_props)
    
    
def order_executor_runner(order_message:OrderMessage, tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"message":order_message, "user_id":order_message.user_id, "order_message":asdict(order_message)} )
    telemetry.info(f"Executing order: {order_message}", tel_props)    
    
    if order_message.order_side == OrderSide.buy_stoploss.value:
        place_stoploss_order(order_message, tel_props)
    
    elif order_message.order_side == OrderSide.buy.value:
        place_orders(order_message, tel_props)
        
    elif order_message.order_side == OrderSide.sell.value:
        place_orders(order_message, tel_props)
    else:
        telemetry.info(f"Order side not supported: {order_message}", tel_props)
    