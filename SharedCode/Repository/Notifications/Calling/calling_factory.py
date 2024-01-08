from twilio.rest import Client
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants


class CallingFactory:
    _client_instance = None
    @staticmethod
    def get_client():
    # Create a Service Bus client using the connection string
        if CallingFactory._client_instance is None:
             kv_service = KeyVaultService()
             account_sid = kv_service.get_secret(Constants.twilio_account_sid)
             auth_token = kv_service.get_secret(Constants.twilio_auth_token)
             CallingFactory._client_instance = Client(account_sid, auth_token)
        return CallingFactory._client_instance