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
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, Stoploss
from dacite import from_dict
from dataclasses import asdict
from SharedCode.Repository.CosmosDB.user_repository import UserRepository
from SharedCode.Models.user import User
user_repo = UserRepository()
telemetry = LoggerService()
operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

stoploss_repo = StoplossesRepository()
user_repo = UserRepository()


stoploss_repo.get_all_stoplosses(telemetry, tel_props)

stoploss1 = Stoploss("dfdasdf", "AAPL",price= 160.0, qty=3, type="normal", product_type="CNC", check_at="30t")

stoploss2 = Stoploss("dfasddf", "AAPL",price= 150.0, qty=3, type="normal", product_type="CNC", check_at="30t")

stoploss3 = Stoploss("dfdasdf", "AAPL",price= 150.0, qty=3, type="normal", product_type="CNC", check_at="clsoing")

# from_dict(data_class=Stoploss, data= asdict(stoploss1))
stoplosses = [stoploss1, stoploss2, stoploss3]
user_id = "1db30ee5-e01a-421f-9f60-bb72ffe31add"
user_stoplosses = UserStoplosses(user_id, user_id, stop_losses=stoplosses)

user = user_repo.get_user(user_id, telemetry, tel_props)

stoploss_repo.store_user_stoplosses(user.id, stoploss1, telemetry, tel_props)


for stop in stoplosses:
    stoploss_repo.store_user_stoplosses(user.id, stop, telemetry, tel_props)

next((sl for sl in stoplosses if sl.id == stoploss.id), None)

stopnew = from_dict(data_class=Stoploss, data= asdict( stoploss))
stopnew.id = "sdfsddfdsdfsdf"
            
            
userStopLosses = stoploss_repo.get_user_stoplosses(user.id, telemetry, tel_props)

stoploss_repo.delete_user_stoploss(user.id, "sdfsd", telemetry, tel_props)

user_stoplosses = UserStoplosses(user.id,user.id, stoplosses)
user_stoplosses.to_dict()

asdict(user_stoplosses)
stoploss_model.check_at = "closing"
stoploss_model.id = "asdasdfdfsd"
stoploss_repo.store_user_stoplosses("2db30ee5-e01a-421f-9f60-bb72ffe31add", stoploss_model, telemetry, tel_props)

stoploss_repo.delete_user_stoploss("2db30ee5-e01a-421f-9f60-bb72ffe31add", stoploss_model.id, telemetry, tel_props)
stoploss2.id = "asdfasdf"
stoploss_repo.store_user_stoplosses(user.user_id, stoploss2, telemetry, tel_props)
stoploss_repo.delete_user_stoploss(user.user_id, stoploss_model.id, telemetry, tel_props)
stoploss_repo.delete_user_stoploss(user.user_id, stoploss2.id, telemetry, tel_props)
s = stoploss_repo.get_stoplosses_by_user("testuserr")
response = stoploss_repo.get_stoplosses_by_user("testuser")

user_stoplosses = UserStoplosses.from_dict(response)
import json
json_string = json.dumps(response)
dic = json.loads(json_string)

dic[0]
user_stoplosses = UserStoplosses.from_dict(json_string[0])
tel_props.update({"number_of_days": 32423})

