from .servicebus_factory import ServiceBusFactory
from azure.servicebus import ServiceBusMessage

class ServiceBusService:
    def __init__(self):
        self.client = ServiceBusFactory.get_client()

   
    
    def send_to_queue(self, message,queue_name):
        sender =  self.client.get_queue_sender(queue_name)
        service_bus_message = ServiceBusMessage(message)
        sender.send_messages(service_bus_message)
    
    def send_to_topic(self, message,topic_name):
        sender =  self.client.get_topic_sender(topic_name)
        service_bus_message = ServiceBusMessage(message)
        sender.send_messages(service_bus_message)
        
        
    def peek_from_subcription(self, topic_name, subscription_name, count:int =1):
        receiver = self.client.get_subscription_receiver(topic_name, subscription_name)
        messages = receiver.peek_messages(max_message_count = count)
        return messages

        
