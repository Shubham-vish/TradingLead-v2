# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join('../..')))

from Prototyping.setupConfig import setup_config
setup_config()
# Above lines are only for local notebook testing. Not to be used in production.
# from azure.servicebus import ServiceBusClient, ServiceBusMessage


from SharedCode.Repository.ServiceBus.servicebus_service import ServiceBusService
queue_name = "testingQueue"
topic_name = "testingTopic"
message = "hello Jaishree"

# #sender =  servicebus_client.get_queue_sender(queue_name)
# sender =  servicebus_client.get_topic_sender(topic_name)
# service_bus_message = ServiceBusMessage(message)
# sender.send_messages(service_bus_message)

Sb_service = ServiceBusService()
Sb_service.send_to_queue(message,queue_name)
Sb_service.send_to_topic(message,topic_name)


