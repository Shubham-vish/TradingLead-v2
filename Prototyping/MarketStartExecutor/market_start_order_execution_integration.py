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
from SharedCode.Runners.market_start_executor_runner import market_start_executer_runner
import json
from SharedCode.Repository.ServiceBus.servicebus_factory import ServiceBusFactory
from dacite import from_dict
from SharedCode.Runners.order_executor_runner import order_executor_runner
from SharedCode.Runners.access_token_generator_runner import access_token_generator_runner
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


results = market_start_executer_runner(tel_props)

user2 = user_repository.get_user("2db30ee5-e01a-421f-9f60-bb72ffe31add", telemetry, tel_props)

sb_service = ServiceBusService()
sb_client = ServiceBusFactory.get_client()
sb_receiver = sb_client.get_subscription_receiver("orders", "executor")

msgs = sb_service.peek_from_subcription("orders", "executor", 1)
msg = msgs[0]


dict = json.loads(str(msg))
order_message = from_dict(OrderMessage, dict)


order_executor_runner(order_message, tel_props)
access_token_generator_runner(tel_props)

from SharedCode.Utils.utility import FunctionUtils

key = FunctionUtils.get_key_for_user_access_token("XS42465")
from SharedCode.Repository.Cache.redis_cache_service import RedisCacheService

redis_service = RedisCacheService()

token = redis_service.get_decoded_value(key)

from SharedCode.Repository.Fyers.fyers_service import FyersService
fyer_service = FyersService.from_kv_secret_name("XS42465", kv_service)

fyers_deails = kv_service.get_fyers_user(0)
fyer_service = FyersService(fyers_deails)
fyer_service.get_order_book(tel_props)