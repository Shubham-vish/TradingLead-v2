from azure.cosmos import CosmosClient
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants
class CosmosDbFactory:
    _cosmos_client = None

    @staticmethod
    def get_cosmos_client():
        if CosmosDbFactory._cosmos_client is None:
            kv_service = KeyVaultService()
            url = kv_service.get_secret(Constants.COSMOS_DB_URL )
            key = kv_service.get_secret(Constants.COSMOS_DB_KEY)
            CosmosDbFactory._cosmos_client = CosmosClient(url, credential=key)
        return CosmosDbFactory._cosmos_client
