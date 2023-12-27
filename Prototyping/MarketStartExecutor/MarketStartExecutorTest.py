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
from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
from SharedCode.Utils.constants import Constants
import concurrent.futures
from dataclasses import asdict
from SharedCode.Models.Order.user_stoplosses import UserStoplosses, Stoploss
from SharedCode.Models.user import User
import json
from SharedCode.Repository.Fyers.fyers_service import FyersService
from SharedCode.Models.Order.order_message import OrderMessage, OrderConstants
from SharedCode.Repository.ServiceBus.servicebus_service import ServiceBusService
from dataclasses import asdict
from MarketStartExecutor.market_start_executor_runner import market_start_executer_runner

kv_service = KeyVaultService()
telemetry = LoggerService()
user_repository = UserRepository()
service_bus_repo = ServiceBusService()


operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}



stoploss_repo = StoplossesRepository()
users_stoplosses = stoploss_repo.get_all_stoplosses(telemetry, tel_props)

userStoplosses = users_stoplosses[0]
user = user_repository.get_user(userStoplosses.user_id, telemetry, tel_props)


order_message =  OrderMessage.from_stoplosses(users_stoplosses[0].stop_losses, user)
order_message.id = "sdfsdf"

# service_bus_repo.send_to_topic("sdfs", "orders")
# service_bus_repo.send_to_topic(json.dumps(asdict(order_message)), "orders")

results = market_start_executer_runner(tel_props)

user2 = user_repository.get_user("2db30ee5-e01a-421f-9f60-bb72ffe31add", telemetry, tel_props)
from SharedCode.Repository.ServiceBus.servicebus_factory import ServiceBusFactory
import json
sb_client = ServiceBusFactory.get_client()
sb_receiver = sb_client.get_subscription_receiver("orders", "executor")
msg = sb_receiver.peek_messages()
# Use message_body as needed

# def set_stoploss(user_stoplosses:UserStoplosses, tel_props):
#     # user_stoplosses = users_stoplosses[0]
#     tel_props = tel_props.copy()
#     tel_props.update({"action": "set_stoploss"})
#     try:
#         telemetry.info(f"Setting stoploss for {user_stoplosses}", tel_props)
#         user = user_repository.get_user(user_stoplosses.user_id, telemetry, tel_props)
#         print(user)
#         user_model = User.from_dict(user)
#         tel_props.update({"user":json.dumps(user_model.to_dict()) })
        
#         telemetry.info(f"User found for userId: {user_stoplosses.user_id}", tel_props)
        
#         if user_model.kv_secret_name is None:
#             telemetry.exception(f"User {user_stoplosses.user_id} does not have fyers details", tel_props)
#             return
#         fyers_details_json = kv_service.get_secret(user_model.kv_secret_name)
#         fyers_details = json.loads(fyers_details_json)
#         fyers_service = FyersService(fyers_details)
#         stoplosses_to_set = user_stoplosses.get_normal_stoplosses()
#         return fyers_service.set_stop_losses(stoplosses_to_set, tel_props)
#     except Exception as e:
#         print(f"An error occurred while setting stoploss for {user_stoplosses}: {e}")
#         telemetry.exception(f"An error occurred while setting stoploss for {user_stoplosses}: {e}", tel_props)

# def set_stoplosses_for_users(tel_props):
#     tel_props = tel_props.copy()
#     stoploss_repo = StoplossesRepository()
#     users_stoplosses = stoploss_repo.get_all_stoplosses(telemetry, tel_props)
    
#     tel_props.update({"action": "set_stoplosses"})
    
#     if not users_stoplosses:
#         telemetry.info("No stoplosses found", tel_props)
#         return
#     len(users_stoplosses)
#     telemetry.info(f"set_stoplosses started with userStoplosses count: {len(users_stoplosses)}", tel_props)
    
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(set_stoploss, users_stoplosses, tel_props)
#         futures = [executor.submit(set_stoploss, user_stoplosses, tel_props) for user_stoplosses in users_stoplosses]
#         results = []
#         for future in concurrent.futures.as_completed(futures):
#             try:
#                 # If your fetch_and_store_token function returns any result, you can retrieve it here
#                 result = future.result()
#                 results.append(result)
#                 telemetry.info(f"Task completed successfully: {result}", tel_props)
#             except Exception as e:
#                 # Handle any exceptions that were raised during the task execution
#                 telemetry.exception(f"Task resulted in an exception: {e}", tel_props)
                
        
#     telemetry.info("set_stoplosses completed", tel_props)


# def market_start_executor_runner(tel_props):
#     set_stoplosses_for_users(tel_props)