from azure.cosmos import CosmosClient
from Repository.KeyVault.keyvault_service import KeyVaultService

class CosmosDbFactory:
    _cosmos_client = None

    @staticmethod
    def get_cosmos_client():
        if CosmosDbFactory._cosmos_client is None:
            kv_service = KeyVaultService()
            url = kv_service.get_secret("CosmosDbUrl").value
            key = kv_service.get_secret("CosmosDbKey").value
            CosmosDbFactory._cosmos_client = CosmosClient(url, credential=key)
        return CosmosDbFactory._cosmos_client
