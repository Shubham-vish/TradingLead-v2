# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join("../../..")))

from Prototyping.setupConfig import setup_config

setup_config()
# Above lines are only for local notebook testing. Not to be used in production.

import pandas as pd
from datetime import datetime, timedelta
import requests
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join("../../..")))

from Prototyping.setupConfig import setup_config

setup_config()
# Above lines are only for local notebook testing. Not to be used in production.

import pandas as pd
from datetime import datetime, timedelta
import requests
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
from SharedCode.Models.user_stoplosses import UserStoplosses, Stoploss

telemetry = LoggerService()
operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

stoploss_repo = StoplossesRepository()

stoplosses = [
    Stoploss("dfasdf", "normal", "AAPL", 150.0),
    Stoploss("sdsfd", "line", "GOOG", 2000.0),
    Stoploss("sdfsd", "trend", "MSFT", 300.0, "2022-01-10", "2022-01-20")
]

stoploss = Stoploss("dfasdf", "normal", "AAPL", 150.0, check_at="30t")

stoploss.price = 200.0
stoploss_repo.store_user_stoplosses("testuser", stoploss, telemetry, tel_props)

userStopLosses = stoploss_repo.get_user_stoplosses("testuser", telemetry, tel_props)

UserStoplosses.from_dict(userStopLosses)
stoploss_repo.delete_user_stoploss("testuser", "sdfsd", telemetry, tel_props)

user_stoplosses = UserStoplosses("testuser", "fyers_username", stoplosses)
user_stoplosses.to_dict()

stoploss_repo.store_user_stoplosses(user_stoplosses, telemetry, tel_props)
s = stoploss_repo.get_stoplosses_by_user("testuserr")
response = stoploss_repo.get_stoplosses_by_user("testuser")

user_stoplosses = UserStoplosses.from_dict(response)
import json
json_string = json.dumps(response)
dic = json.loads(json_string)

dic[0]
user_stoplosses = UserStoplosses.from_dict(json_string[0])
tel_props.update({"number_of_days": 32423})

