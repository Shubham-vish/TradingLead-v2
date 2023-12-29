from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants


class BlobServiceFactory:
    _blobservice_client = None

    @staticmethod
    def get_blob_service_client():
        if BlobServiceFactory._blobservice_client is None:
            kv_service = KeyVaultService()
            connect_str = kv_service.get_secret(Constants.STORAGE_CONNECTION_STRING)
            BlobServiceFactory._blobservice_client = (
                BlobServiceClient.from_connection_string(connect_str)
            )
        return BlobServiceFactory._blobservice_client
