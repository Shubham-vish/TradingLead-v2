import uuid
import logging
from azure.cosmos import exceptions

class AlertsRepository:
    def __init__(self, cosmos_service, container_name):
        self.container = cosmos_service.get_container(container_name)

    def fetch_user_alerts(self, user_id):
        logging.info(f"Fetching alerts for user ID: {user_id}")
        query = "SELECT * FROM c WHERE c.userId = @userId"
        parameters = [{'name': '@userId', 'value': user_id}]
        try:
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True))
            return items[0]['alerts'] if items else None
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error fetching alerts: {e}")
            return None

    def create_user_alert(self, user_id, alert_data):
        logging.info(f"Creating alert for user ID: {user_id}")
        new_alert = {
            "id": str(uuid.uuid4()),
            "userId": user_id,
            "alerts": [alert_data]  # Assuming alert_data is a dictionary with alert details
        }
        try:
            self.container.create_item(new_alert)
            return new_alert
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error creating alert: {e}")
            return None

    def update_user_alert(self, user_id, alert_data):
        logging.info(f"Updating alert for user ID: {user_id}")
        query = "SELECT * FROM c WHERE c.userId = @userId"
        parameters = [{'name': '@userId', 'value': user_id}]
        try:
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True))
            
            if items:
                existing_entry = items[0]
                existing_entry['alerts'].append(alert_data)
                self.container.replace_item(item=existing_entry['id'], body=existing_entry)
                return existing_entry
            else:
                return self.create_user_alert(user_id, alert_data)
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error updating alert: {e}")
            return None

    def delete_user_alert(self, user_id):
        logging.info(f"Deleting alerts for user ID: {user_id}")
        query = "SELECT * FROM c WHERE c.userId = @userId"
        parameters = [{'name': '@userId', 'value': user_id}]
        try:
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True))
            if items:
                self.container.delete_item(item=items[0], partition_key=user_id)
                return True
            return False
        except exceptions.CosmosHttpResponseError as e:
            logging.error(f"Error deleting alert: {e}")
            return False
