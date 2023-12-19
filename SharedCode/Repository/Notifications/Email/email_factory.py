from azure.communication.email import EmailClient
from azure.identity import DefaultAzureCredential
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants

class EmailFactory:
    _client_instance = None

    @staticmethod
    def get_client():
        if EmailFactory._client_instance is None:
            kv_service = KeyVaultService()
            endpoint = kv_service.get_secret(Constants.communication_service_endpoint)
            credential = DefaultAzureCredential()
            EmailFactory._client_instance = EmailClient(endpoint=endpoint, credential=credential)

        return EmailFactory._client_instance
