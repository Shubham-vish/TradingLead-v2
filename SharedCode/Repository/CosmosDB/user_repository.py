import uuid
from azure.cosmos import PartitionKey
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Models.user import User
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants
from dataclasses import asdict

class UserRepository:
    def __init__(self):
        kv_service = KeyVaultService()
        self.database_id = kv_service.get_secret(Constants.DATABASE_ID)
        self.users_container_name = kv_service.get_secret(Constants.USERS_CONTAINER_NAME)
        self.cosmos_db_service = CosmosDbService(self.database_id)
        self.container = self.cosmos_db_service.get_container(self.users_container_name)

    def create_user(self, user: User):
        doc = asdict(user)
        self.container.create_item(doc)

    def get_user(self, user_id, telemetry: LoggerService, tel_props):
        query = "SELECT * FROM c WHERE c.user_id = @user_id"
        parameters = [{"name": "@user_id", "value": user_id}]
        
        try:
            result = self.container.query_items(query, parameters=parameters, enable_cross_partition_query=True)
            users = list(result)
            
            if len(users) == 0:
                telemetry.info(f"No user found for user_id: {user_id}", tel_props)
                return None
            
            if len(users) > 1:
                telemetry.exception(f"Multiple users found for user_id: {user_id}", tel_props)
            
            telemetry.info(f"User fetched: {users}", tel_props)
            return users[0]
        except Exception as e:
            telemetry.exception(f"Error occurred while fetching user: {str(e)}", tel_props)
            return None

    def update_user(self, user: User):
        try:
            self.container.upsert_item(user)
        except Exception as e:
            print(f"Error occurred while updating user: {str(e)}")

    def delete_user(self, user_id):
        try:
            self.container.delete_item(user_id, PartitionKey(user_id))
        except Exception as e:
            print(f"Error occurred while deleting user: {str(e)}")

    def store_user(self, user: User, telemetry: LoggerService, tel_props):
        telemetry.info(f"Storing user: {user}", tel_props)
        existing_user = self.get_user(user.user_id, telemetry, tel_props)
        
        if existing_user:
            telemetry.info(f"User {user.user_id} already exists. Updating user.", tel_props)
            existing_user.update(user)
            self.update_user(existing_user)
        else:
            telemetry.info(f"User {user.user_id} does not exist. Creating user.", tel_props)
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
