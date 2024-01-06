# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join("../..")))

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
from SharedCode.Models.Order.order_message import OrderMessage
from SharedCode.Repository.ServiceBus.servicebus_service import ServiceBusService
from dataclasses import asdict
# from SharedCode.Runners.market_start_executor_runner import market_start_executer_runner

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

# results = market_start_executer_runner(tel_props)
sb_service = ServiceBusService()


def set_stoploss_for_user(user_stoplosses:UserStoplosses, tel_props):
    user_stoplosses = users_stoplosses[0]
    tel_props = tel_props.copy()
    tel_props.update({"action": "set_stoploss", "user_stoplosses": json.dumps(asdict(user_stoplosses)), "user_id": user_stoplosses.user_id})
    stoplosses = user_stoplosses.get_normal_stoplosses()
    
    if stoplosses is None or len(stoplosses) == 0:
        telemetry.info(f"No normal stoplosses found for user: {user_stoplosses.user_id}", tel_props)
        return True, user_stoplosses.user_id
    try:
        telemetry.info(f"Setting stoploss for user: {user_stoplosses.id} {stoplosses}", tel_props)
        user = user_repository.get_user(user_stoplosses.user_id, telemetry, tel_props)
        order_message = OrderMessage.from_stoplosses(stoplosses, user)
        sb_service.send_to_topic(json.dumps(asdict(order_message)), "orders")
        telemetry.info(f"Stoploss set successfully for {asdict(user_stoplosses)}", tel_props)
        return True, user_stoplosses.user_id
    except Exception as e:
        msg = f"An error occurred while setting stoploss for {asdict(user_stoplosses)}: {e}"
        telemetry.exception(msg, tel_props)
        return False, user_stoplosses.user_id

def set_stoplosses_for_all_users(tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"action": "set_stoplosses_for_users"})
    stoploss_repo = StoplossesRepository()
    users_stoplosses = stoploss_repo.get_all_stoplosses(telemetry, tel_props)
    
    if (not users_stoplosses) or (len(users_stoplosses) == 0):
        telemetry.info("No stoplosses found", tel_props)
        return
    
    telemetry.info(f"set_stoplosses started with userStoplosses count: {len(users_stoplosses)}", tel_props)
    results = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(set_stoploss_for_user, users_stoplosses, tel_props)
        futures = [executor.submit(set_stoploss_for_user, user_stoplosses, tel_props) for user_stoplosses in users_stoplosses]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                if result:
                    success, user_id = result
                    if success:
                        telemetry.info(f"Stoploss set successfully for user ID: {user_id}", tel_props)
                    else:
                        telemetry.info(f"Failed to set stoploss for user ID: {user_id}", tel_props)
                else:
                    telemetry.error(f"Task failed: {result}", tel_props)
            except Exception as e:
                telemetry.exception(f"Task resulted in an exception: {e}", tel_props)
                raise e
        
    telemetry.info("set_stoplosses_for_all_users completed", tel_props)
    return results


def runner(tel_props):
    return set_stoplosses_for_all_users(tel_props)

runner(tel_props)



# 



user2 = user_repository.get_user("2db30ee5-e01a-421f-9f60-bb72ffe31add", telemetry, tel_props)
from SharedCode.Repository.ServiceBus.servicebus_factory import ServiceBusFactory
import json
import json
import json
from dacite import from_dict
sb_client = ServiceBusFactory.get_client()
sb_receiver = sb_client.get_subscription_receiver("orders", "executor")
msg = sb_receiver.peek_messages()

dict = json.loads(str(msg[0]))
order_message = from_dict(OrderMessage, dict)

asdict(msg[0].message)
