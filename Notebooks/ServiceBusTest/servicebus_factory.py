from azure.servicebus import ServiceBusClient

CONNECTION_STR = 'Endpoint=sb://sb-tradingtest.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=oEGc4wn7YRpYMLdEeqqfu/S/4Zq96CMHe+ASbAPsQT8='
class ServiceBusFactory:
    @staticmethod
    def get_client():
    # Create a Service Bus client using the connection string
        servicebus_client = ServiceBusClient.from_connection_string( conn_str=CONNECTION_STR)
        return servicebus_client