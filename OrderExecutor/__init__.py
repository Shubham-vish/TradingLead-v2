import azure.functions as func
from SharedCode.Models.Order.order_message import StoplossMessage
from SharedCode.Repository.Fyers.fyers_service import FyersService
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
import json

telemetry = LoggerService()
kv_service = KeyVaultService()

def main(message: func.ServiceBusMessage, context: func.Context):
    # Log the Service Bus Message as plaintext
    
    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.stoploss_executor_service,
        Constants.operation_id : operation_id,
    }
    
    telemetry.info(f"StopLoss Executor ServiceBus trigger function processing message: {message}", tel_props)

    message_content_type = message.content_type
    
    message_body = message.get_body().decode("utf-8")
    json_message = json.loads(message_body)
    
    tel_props.update({"message":json_message})
    stoploss_message = StoplossMessage(**json_message)
    
    telemetry.info(f"StopLoss Executor ServiceBus parsed message properly: {json_message}", tel_props)
    
    fyers_details_json = kv_service.get_secret(stoploss_message.kv_secret_name)
    fyers_details = json.loads(fyers_details_json)
    
    fyers_service = FyersService(fyers_details)
    
    fyers_service.set_stop_losses([stoploss_message.stoploss], telemetry)
    
    telemetry.info(f"StopLoss Executor ServiceBus trigger function processed message: {message}", tel_props)