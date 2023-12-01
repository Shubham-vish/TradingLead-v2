from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

class KeyVaultFactory:
    _client_instance = None

    @staticmethod
    def get_client():
        if KeyVaultFactory._client_instance is None:
            kv_uri = os.environ["KEY_VAULT_URI"]
            credential = DefaultAzureCredential()
            KeyVaultFactory._client_instance = SecretClient(vault_url=kv_uri, credential=credential)
        return KeyVaultFactory._client_instance
