import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../..")))

from Prototyping.setupConfig import setup_config

setup_config()

# Above code is for testing

import pandas as pd

from SharedCode.Repository.BlobService.blob_service import BlobService
from SharedCode.Utils.constants import Constants
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.tikers import Tickers
from SharedCode.Repository.Fyers.fyers_service import FyersService
from SharedCode.Repository.CosmosDB.strategy_repository import StrategyRepository
from SharedCode.Models.Strategy.strategy import Strategy, StrategyUser
from SharedCode.Repository.CosmosDB.user_repository import UserRepository

from dataclasses import asdict
from dacite import from_dict

kv_service = KeyVaultService()
blob_service = BlobService()
telemetry = LoggerService()

operation_id = "RandomOperationId"


tel_props = {
    Constants.SERVICE: Constants.fetch_store_history_data_service,
    Constants.operation_id: operation_id,
}


user_repo = UserRepository()
strategy_repo = StrategyRepository()

strategy = strategy_repo.get_strategy("KernelRegressionStrategy", telemetry, tel_props)


user = user_repo.get_user("1db30ee5-e01a-421f-9f60-bb72ffe31add", telemetry, tel_props)

strategy_name = strategy.strategy_name
ticker = "NSE:NIFTY50-INDEX"
quantity = 50
curr_quantity = 0
product_type = "MARGIN"
strategy_user = StrategyUser.from_user(user=user, ticker= ticker,trade_ticker= ticker,quantity= quantity, curr_quantity= curr_quantity, product_type=product_type)

strategy_repo.add_user_to_strategy(strategy_name, strategy_user, telemetry, tel_props)


ticker = "NSE:ADANIPORTS-EQ"
product_type = "CNC"
quantity = 10
strategy_user = StrategyUser.from_user(user=user, ticker= ticker,trade_ticker= ticker,quantity= quantity, curr_quantity= curr_quantity,, product_type=product_type)
strategy_repo.add_user_to_strategy(strategy_name, strategy_user, telemetry, tel_props)

