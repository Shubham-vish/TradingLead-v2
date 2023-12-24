# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join('../..')))

from Notebooks.setupConfig import setup_config
setup_config()
# Above lines are only for local notebook testing. Not to be used in production.
# from azure.servicebus import ServiceBusClient, ServiceBusMessage

# CONNECTION_STR = 'Endpoint=sb://sb-tradingtest.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=oEGc4wn7YRpYMLdEeqqfu/S/4Zq96CMHe+ASbAPsQT8='

# servicebus_client = ServiceBusClient.from_connection_string( conn_str=CONNECTION_STR)

from .servicebus_service import ServiceBusService
queue_name = "testingQueue"
topic_name = "testingTopic"
message = "hello"

# #sender =  servicebus_client.get_queue_sender(queue_name)
# sender =  servicebus_client.get_topic_sender(topic_name)
# service_bus_message = ServiceBusMessage(message)
# sender.send_messages(service_bus_message)

Sb_service = ServiceBusService()
Sb_service.send_to_queue(message,queue_name)
Sb_service.send_to_topic(message,topic_name)


