import datetime
import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from .fetch_store_stock_history_data_runner import fetch_store_history_data_runner
telemetry = LoggerService()


def main(mytimer: func.TimerRequest, context: func.Context) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.fetch_store_history_data_service,
        Constants.operation_id : operation_id,
    }
    
    
    telemetry.info(f'Python timer trigger function started at {utc_timestamp}', tel_props)
    
    if mytimer.past_due:
        telemetry.info('The timer is past due!', tel_props)

    fetch_store_history_data_runner(tel_props)
    
    utc_timestamp = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).isoformat()
    telemetry.info(f'Python timer trigger function FetchStoreHidstoryData completed at {utc_timestamp}', tel_props)
