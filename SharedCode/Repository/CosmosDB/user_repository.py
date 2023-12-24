import uuid

from azure.cosmos import PartitionKey
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.Logger.logger_service import LoggerService

class UserRepository:
    def __init__(self, cosmos_service:CosmosDbService, container_name):
        self.container = cosmos_service.get_container(container_name)

    def create_user(self, user):
        user["id"] = str(uuid.uuid4())
        self.container.create_item(user)

    def get_user(self, user_id):
        
        query = f"SELECT * FROM c WHERE c.UserId = '{user_id}'"
        result = self.container.query_items(query, enable_cross_partition_query=True)
        return list(result)

    def update_user(self, user):
        self.container.upsert_item(user)

    def delete_user(self, user_id):
        self.container.delete_item(user_id, PartitionKey(user_id))

    def store_user(self, user_id, name, email, telemetry:LoggerService, tel_props):
        user = {
            "UserId": user_id,
            "name": name,
            "email": email
        }
        telemetry.info(f"Storing user: {user}", tel_props)
        existing_user = self.get_user(user_id)
        if existing_user:
            telemetry.info(f"User {user_id} already exists. Updating user.", tel_props)
            existing_user["name"] = name
            existing_user["email"] = email
            self.update_user(existing_user)
        else:
            telemetry.info(f"User {user_id} does not exist. Creating user.", tel_props)
            self.create_user(user)
        
    


# # Usage example
# endpoint = "your_cosmosdb_endpoint"
# key = "your_cosmosdb_key"
# database_name = "your_database_name"
# container_name = "your_container_name"

# repository = UserRepository(endpoint, key, database_name, container_name)

# # Create a user
# user = {
#     "id": "1",
#     "name": "John Doe",
#     "email": "john.doe@example.com"
# }
# repository.create_user(user)

# # Get a user
# user_id = "1"
# result = repository.get_user(user_id)
# print(result)

# # Update a user
# user["name"] = "Jane Doe"
# repository.update_user(user)

# # Delete a user
# repository.delete_user(user_id)
