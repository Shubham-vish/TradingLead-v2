import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../..")))

from Prototyping.setupConfig import setup_config

setup_config()

# Above code is for testing

import pandas as pd

from SharedCode.Utils.constants import Constants
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Repository.Fyers.fyers_service import FyersService
import datetime
from SharedCode.Repository.CosmosDB.strategy_repository import StrategyRepository
from SharedCode.Strategies.ml import KernelRegressionStrategy
from SharedCode.Utils.stock_chart import StockChart
from SharedCode.Runners.strategy_kernel_regression_runner import strategy_kernel_regression_runner

from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.constants import Constants
from SharedCode.Repository.CosmosDB.user_repository import UserRepository
from SharedCode.Repository.ServiceBus.servicebus_service import ServiceBusService
from dataclasses import asdict
from SharedCode.Repository.CosmosDB.strategy_repository import StrategyRepository
import json
import concurrent.futures
from SharedCode.Repository.Fyers.fyers_service import FyersService
from SharedCode.Models.Strategy.strategy import Strategy, StrategyUser
from SharedCode.Strategies.ml import KernelRegressionStrategy
import datetime
from SharedCode.Models.Strategy.signal_message import SignalMessage

kv_service = KeyVaultService()
telemetry = LoggerService()
sb_service = ServiceBusService()
strategy_repo = StrategyRepository()


fyers_details = kv_service.get_fyers_user(0)
fyers_service = FyersService(fyers_details)
kernel_strategy = KernelRegressionStrategy()

strategy_name = "KernelRegressionStrategy"

operation_id = "RandomOperationId"

signal_topic_name = "signal-topic"

operation_id = "RandomOperationId"


tel_props = {
    Constants.SERVICE: Constants.fetch_store_history_data_service,
    Constants.operation_id: operation_id,
}

strategy = strategy_repo.get_strategy(strategy_name, telemetry, tel_props)
strategy_user = strategy.strategy_users[1]

from SharedCode.Utils.utility import FunctionUtils

FunctionUtils.set_trade_ticker_for_fyers_ticker("NSE:NIFTY50-INDEX", "MARGIN", "NSE:NIFTY24JANFUT")

df = fyers_service.history("NSE:NIFTY24JANFUT", "2021-01-01", "2022-01-01", "1D", tel_props)

df.head()
asdict(strategy_user)

strategy_kernel_regression_runner(tel_props)