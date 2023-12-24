import datetime
from fyers_apiv3 import fyersModel
from SharedCode.Repository.Cache.redis_cache_service import RedisCacheService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils

class FyersClientFactory:
    clients = {}
    expiry_duration = datetime.timedelta(hours=1)

    @staticmethod
    def get_fyers_client(user_fyers_details):

        client_id = user_fyers_details[Constants.client_id]
        current_time = datetime.datetime.now()

        if client_id in FyersClientFactory.clients:
            client, creation_time = FyersClientFactory.clients[client_id]
            if current_time - creation_time > FyersClientFactory.expiry_duration:
                # Client expired, create a new one
                client = FyersClientFactory._create_new_client(user_fyers_details)
                FyersClientFactory.clients[client_id] = (client, current_time)
        else:
            # Create new client
            client = FyersClientFactory._create_new_client(user_fyers_details)
            FyersClientFactory.clients[client_id] = (client, current_time)
        return client

    @staticmethod
    def _create_new_client(user_fyers_details):
        username = user_fyers_details[Constants.fyers_username]
        client_id = user_fyers_details[Constants.client_id]
        redis_key = FunctionUtils.get_key_for_user_access_token(username)
        redis_cache_service = RedisCacheService()
        access_token_for_user = redis_cache_service.get_decoded_value(redis_key)
        # Logic to create a new FyersModel instance
        return fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token_for_user, log_path="/tmp")

# Rest of the code remains the same
