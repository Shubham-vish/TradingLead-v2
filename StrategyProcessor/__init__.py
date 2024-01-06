import azure.functions as func
from SharedCode.Models.Strategy.signal_message import SignalMessage
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Runners.strategy_processor_runner import strategy_processor_runner
import json

telemetry = LoggerService()

def main(message: func.ServiceBusMessage, context: func.Context):
    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.strategy_processor_service,
        Constants.operation_id : operation_id,
    }
    
    telemetry.info(f"Strategt Processor ServiceBus trigger function processing message: {message}", tel_props)
    message_body = message.get_body().decode("utf-8")
    json_message = json.loads(message_body)
    
    tel_props.update({"message":json_message})
    signal_message = SignalMessage(**json_message)
    
    telemetry.info(f"Strategt Processor ServiceBus parsed message properly: {json_message}", tel_props)
    
    strategy_processor_runner(signal_message, tel_props)
    
    telemetry.info(f"Strategt Processor ServiceBus trigger function processed message: {message}", tel_props)
    
