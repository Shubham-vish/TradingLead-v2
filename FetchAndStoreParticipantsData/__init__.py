import datetime
import azure.functions as func
from FetchAndStoreParticipantsData.fetch_store_participants_data_runner import fetch_store_data_for_n_days
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Repository.Logger.logger_service import LoggerService
import os


number_of_days = int(os.environ[Constants.number_of_days_to_fetch_participation_data])

telemetry = LoggerService()

def main(mytimer: func.TimerRequest , context: func.Context) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()


    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.fetch_store_participants_data_service,
        Constants.operation_id : operation_id,
        number_of_days : number_of_days
    }
    
    if mytimer.past_due:
        telemetry.info('The timer is past due!', tel_props)
    
    telemetry.info(f'Python timer trigger function FetchStoreParticipantsData started at {utc_timestamp}', tel_props)    
    
    fetch_store_data_for_n_days(number_of_days, tel_props)
    
    telemetry.info(f'Python timer trigger function FetchStoreParticipantsData ran at {utc_timestamp} Completed', tel_props)

