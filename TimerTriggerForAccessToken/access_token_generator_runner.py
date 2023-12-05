from SharedCode.Repository.AccessToken.access_token import get_fyers_access_token
import json
import time
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.Cache.redis_cache_service import RedisCacheService
from SharedCode.Utils.constants import Constants
import concurrent.futures


kv_service = KeyVaultService()
telemetry = LoggerService()
redis_cache_service = RedisCacheService()

def fetch_and_store_token(user, tel_props):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            fyers_details_json = kv_service.get_secret(user['KvSecretName'])
            fyers_details = json.loads(fyers_details_json)
            username = fyers_details[Constants.fyers_username]

            tel_props.update( {
                Constants.username : username,
                Constants.client_id : fyers_details[Constants.client_id],
                Constants.contact_number : fyers_details[Constants.contact_number],
            })
            redis_key = f"{username}-token"
            access_token = get_fyers_access_token(fyers_details, tel_props)
            redis_cache_service.set_value(redis_key, access_token)
            fetched_token = redis_cache_service.get_value(redis_key)
            
            telemetry.info(f"Token stored for {username}, {fetched_token}", tel_props)
            return {"user": user, "fetched_token": fetched_token}

        except Exception as e:
            telemetry.exception(f"Error in fetching access token attempt no. {attempt}.\nError: {e}", tel_props)
            time.sleep(10)
            continue
    message = f"Max retries in main function. Error in fetching access token. for user {username}"
    telemetry.exception(message, tel_props)
    raise Exception(message)

def access_token_generator_runner(tel_props):
    fyer_users_json = kv_service.get_secret("FyerUserDetails")
    telemetry.info(fyer_users_json, tel_props)
    fyer_users = json.loads(fyer_users_json)
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_and_store_token, user, tel_props) for user in fyer_users]
        for future in concurrent.futures.as_completed(futures):
            try:
                # If your fetch_and_store_token function returns any result, you can retrieve it here
                result = future.result()
                results.append(result)
                user_info = result["user"]
                token = result["fetched_token"]
                # Log the success or result if necessary
                tel_props.update({"UserId": json.dumps(user_info),
                    "Token": token
                })
                telemetry.info(f"Task completed successfully: {result}", tel_props)
            except Exception as e:
                # Handle any exceptions that were raised during the task execution
                telemetry.exception(f"Task resulted in an exception: {e}", tel_props)
                
    return results