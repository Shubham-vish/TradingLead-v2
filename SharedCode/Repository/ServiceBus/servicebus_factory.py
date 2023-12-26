from azure.servicebus import ServiceBusClient
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants


class ServiceBusFactory:
    _client_instance = None
    @staticmethod
    def get_client():
    # Create a Service Bus client using the connection string
        if ServiceBusFactory._client_instance is None:
             kv_service = KeyVaultService()
             servicebus_conn_str = kv_service.get_secret(Constants.service_bus_connection_string)
             ServiceBusFactory._client_instance = ServiceBusClient.from_connection_string( conn_str=servicebus_conn_str)
        return ServiceBusFactory._client_instance

        