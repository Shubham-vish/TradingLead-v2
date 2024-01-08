import os
import sys

# Below code is for testing
sys.path.append(os.path.abspath(os.path.join("../..")))
sys.path.append(os.path.abspath(os.path.join("..")))
from Prototyping.setupConfig import setup_config
import uuid
setup_config()

#
import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
import types
from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
from SharedCode.Utils.constants import Constants
import json
from SharedCode.Models.Order.user_stoplosses import Stoploss
from SharedCode.Runners.alerts_runner import process_get_request, process_post_request, process_delete_request, alerts_runner

from dacite import from_dict
from dataclasses import asdict

telemetry = LoggerService()
stoploss_repo = StoplossesRepository()
application_json = "application/json"

#

operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

user_stoplosses = stoploss_repo.get_all_stoplosses(telemetry, tel_props)
stoploss = user_stoplosses[0].stop_losses[0]

asdict(stoploss)
stoploss.ticker = "MSFT"

for stoploss in user_stoplosses[0].stop_losses:
    stoploss.id = str(uuid.uuid4())

stoploss_repo.update_user_stoplosses(user_stoplosses[0], telemetry=telemetry, tel_props=tel_props)
stoploss_repo.store_user_stoplosses(user_stoplosses[0].user_id, stoploss, telemetry, tel_props)

#  
# 

user_id = user_stoplosses[0].user_id
response = process_get_request(user_stoplosses[0].user_id, tel_props)
response.get_body().decode("utf-8")

req = func.HttpRequest(url = "google.com", method="POST", body=json.dumps({"ticker": "NSE:BATAINDIA-EQ","price":1400 , "stock_name": "Microsoft", "type":"line", "is_alert":False, "is_stoploss":False}), route_params={"user_id": user_id})

response = process_post_request(req, user_id, tel_props)
res_body = response.get_body().decode("utf-8")

json_body = json.loads(res_body)

stoploss_id = json_body.get("alert").get("id")
req = func.HttpRequest(url = "google.com", method="DELETE", body=json.dumps({"stoploss_id":"63c90eef-cc3e-471e-a0ac-a8640e87c755"}), route_params={"user_id": user_id})

response = process_delete_request(req, user_id, tel_props)

response = alerts_runner(req, tel_props)
response.get_body().decode("utf-8")