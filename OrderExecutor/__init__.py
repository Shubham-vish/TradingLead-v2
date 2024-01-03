import azure.functions as func
from SharedCode.Models.Order.order_message import OrderMessage
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Runners.order_executor_runner import order_executor_runner
import json

telemetry = LoggerService()
kv_service = KeyVaultService()

def main(message: func.ServiceBusMessage, context: func.Context):
    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.order_executor_service,
        Constants.operation_id : operation_id,
    }
    
    telemetry.info(f"StopLoss Executor ServiceBus trigger function processing message: {message}", tel_props)
    message_body = message.get_body().decode("utf-8")
    json_message = json.loads(message_body)
    
    tel_props.update({"message":json_message})
    order_message = OrderMessage(**json_message)
    
    telemetry.info(f"StopLoss Executor ServiceBus parsed message properly: {json_message}", tel_props)
    
    order_executor_runner(order_message, tel_props)
    
    telemetry.info(f"StopLoss Executor ServiceBus trigger function processed message: {message}", tel_props)
    
