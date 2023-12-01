import datetime
import azure.functions as func
from SharedCode.Repository.AccessToken.access_token import get_fyers_access_token
import json
import time
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.Cache.redis_cache_service import RedisCacheService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils


kv_service = KeyVaultService()

telemetry = LoggerService()


def main(mytimer: func.TimerRequest, context: func.Context) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    operation_id = FunctionUtils.get_operation_id(context)
    tel_props = {
        Constants.SERVICE : Constants.access_token_generator_service,
        Constants.operation_id : operation_id,
    }
    
    redis_cache_service = RedisCacheService()
    
    telemetry.event("Trigger fired with operation id: " + operation_id, tel_props)
    
    if mytimer.past_due:
        telemetry.info('The timer is past due!', tel_props)
    
    fyers_details_json = kv_service.get_secret("ShubhamFyersDetails")
    fyers_details = json.loads(fyers_details_json)
    username = fyers_details[Constants.fyers_username]
    
    tel_props.update( {
        Constants.username : fyers_details[Constants.fyers_username],
        Constants.client_id : fyers_details[Constants.client_id],
        Constants.contact_number : fyers_details[Constants.contact_number],
        Constants.operation_id : operation_id,
    })

    telemetry.event(f'Python timer trigger function ran at {utc_timestamp}', tel_props)
    telemetry.event(f"Fetching access token for {username}", tel_props)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            access_token = get_fyers_access_token(fyers_details, tel_props)
            redis_cache_service.set_value(username, access_token)
            fetched_token = redis_cache_service.get_value(username)
            telemetry.info(fetched_token, tel_props)
            return
        except Exception as e:
            telemetry.exception(f"Error in fetching access token attempt no. {attempt}.\nError: {e}", tel_props)
            time.sleep(10)
            continue
        
    message = f"Max retries in main function. Error in fetching access token.\nError: {e}"
    telemetry.exception(message, tel_props)
    raise Exception(message)
    
    