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
from SharedCode.Utils.tikers import Tickers
from SharedCode.Repository.Fyers.fyers_service import FyersService
import pandas as pd
from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
from SharedCode.Utils.constants import Constants
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, Stoploss
from SharedCode.Repository.CosmosDB.user_repository import UserRepository

from SharedCode.Models.user import User
from dacite import from_dict
from dataclasses import asdict

kv_service = KeyVaultService()
telemetry = LoggerService()
user_repository = UserRepository()

telemetry = LoggerService()
operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

user = user_repository.get_user("1db30ee5-e01a-421f-9f60-bb72ffe31add", telemetry, tel_props)

user.fyers_user_name = "ZS42465"
# user = User(
#     user_id="1db30ee5-e01a-421f-9f60-bb72ffe31add",
#     fyers_user_name="XS42465",
#     kv_secret_name="ShubhamFyersDetails",
#     id="1db30ee5-e01a-421f-9f60-bb72ffe31add",
#     name="Shubham Vishwakarma",
#     email=""
# )
user2 = user_repository.get_user(user.user_id, telemetry, tel_props)

user.fyers_user_name = "XS42465"
user.kv_secret_name = "ShubhamFyersDetails"
user_repository.store_user(user, telemetry, tel_props)

user.fyers_user_name = ""
user.kv_secret_name = ""
user.user_id = "1db50ee5-e01a-421f-9f60-bb72ffe31add"
user_repository.store_user(user, telemetry, tel_props)