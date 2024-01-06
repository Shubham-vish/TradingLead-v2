# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join("../..")))
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
from SharedCode.Repository.CosmosDB.strategy_repository import StrategyRepository
from SharedCode.Models.user import User
from SharedCode.Models.Strategy.signal_message import SignalMessage
import json
user_repo = UserRepository()
telemetry = LoggerService()
strategy_repo = StrategyRepository()
strategy_name = "KernelRegressionStrategy"

operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}


strategy = strategy_repo.get_strategy(strategy_name, telemetry, tel_props)
strategy_user = strategy.strategy_users[1]

signal_message = SignalMessage.from_strategy_user(strategy_user, strategy.strategy_name, True, 100.0)
dict = asdict(signal_message)
dict
json.dumps(asdict(signal_message))
print(asdict(signal_message))


tel_props.update({"signal_message": asdict(signal_message)})
# tel_props.update({"signal_message2": json.dumps(asdict(signal_message))})
# telemetry.info(f"Signal message sent for user, ticker: {strategy_user.user_id}, {strategy_user.ticker} with signal: {True}", tel_props)
# Code to get the signal message
from SharedCode.Models.Strategy.signal_message import SignalMessage
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
import json
from SharedCode.Repository.Fyers.fyers_service import FyersService
from dataclasses import asdict
from SharedCode.Models.Fyers.fyers_constants import OrderType, OrderSide, ProductType
from SharedCode.Models.Order.order import Order


telemetry = LoggerService()
kv_service = KeyVaultService()


def place_order(signal_message:SignalMessage, tel_props):
    tel_props = tel_props.copy()
    telemetry.info(f"Executing market order: {signal_message}", tel_props)
    fyers_service = FyersService.from_kv_secret_name(signal_message.kv_secret_name, kv_service)
    
    
    
    order = Order.from_signal_message(signal_message)
    fyers_service.place_orders([order], tel_props)
    telemetry.info(f"Executed signal order: {signal_message}", tel_props)
    
    
def strategy_processor_runner(signal_message:SignalMessage, tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"message":signal_message, "user_id":signal_message.user_id, "signal_message":asdict(signal_message)} )
    telemetry.info(f"Processing Strategy signal: {signal_message}", tel_props)
    telemetry.info(f"Executing order: {signal_message}", tel_props)    
    
    if signal_message.signal == True:
        place_stoploss_order(signal_message, tel_props)
    
    elif signal_message.signal == False:
        place_orders(signal_message, tel_props)
    else:
        telemetry.info(f"Signal side not supported: {signal_message}", tel_props)
        telemetry.info(f"Order side not supported: {signal_message}", tel_props)
    
    
