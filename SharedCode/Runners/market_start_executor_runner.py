from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Repository.CosmosDB.stoplosses_repository import StoplossesRepository
from SharedCode.Utils.constants import Constants
from SharedCode.Models.Order.user_stoplosses import UserStoplosses
from SharedCode.Repository.CosmosDB.user_repository import UserRepository
import concurrent.futures
import json
from SharedCode.Models.Order.order_message import OrderMessage
from SharedCode.Repository.ServiceBus.servicebus_service import ServiceBusService
from dataclasses import asdict

kv_service = KeyVaultService()
telemetry = LoggerService()
user_repository = UserRepository()
sb_service = ServiceBusService()

order_topic_name = kv_service.get_secret(Constants.ORDER_TOPIC_NAME)

    
def set_stoploss_for_user(user_stoplosses:UserStoplosses, tel_props):
    tel_props = tel_props.copy()
    tel_props.update({"action": "set_stoploss", "user_stoplosses": json.dumps(asdict(user_stoplosses)), "user_id": user_stoplosses.user_id})
    stoplosses = user_stoplosses.get_normal_stoplosses()
    
    if stoplosses is None or len(stoplosses) == 0:
        telemetry.info(f"No normal stoplosses found for user: {user_stoplosses.user_id}", tel_props)
        return True, user_stoplosses.user_id
    
    try:
        telemetry.info(f"Setting stoploss for {asdict(user_stoplosses)}", tel_props)
        user = user_repository.get_user(user_stoplosses.user_id, telemetry, tel_props)
        order_message = OrderMessage.from_stoplosses(stoplosses, user)
        order_msg_json = json.dumps(asdict(order_message))
        sb_service.send_to_topic(order_msg_json, order_topic_name)
        telemetry.info(f"Stoploss msg sent successfully: {order_msg_json}", tel_props)
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


def market_start_executer_runner(tel_props):
    return set_stoplosses_for_all_users(tel_props)
