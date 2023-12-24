# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join("../../..")))

from Prototyping.setupConfig import setup_config

setup_config()
# 

from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.constants import Constants
from SharedCode.Repository.CosmosDB.user_repository import UserRepository
from MarketStartExecutor.market_start_executor_runner import market_start_executor_runner, set_stoploss, set_stoplosses_for_users

kv_service = KeyVaultService()
telemetry = LoggerService()
user_repository = UserRepository()

operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}


market_start_executor_runner(tel_props)