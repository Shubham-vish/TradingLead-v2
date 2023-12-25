import uuid
from azure.cosmos import PartitionKey
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Models.user import User
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Utils.constants import Constants
from dataclasses import asdict
from dacite import from_dict

class UserRepository:
    def __init__(self):
        kv_service = KeyVaultService()
        self.database_id = kv_service.get_secret(Constants.DATABASE_ID)
        self.users_container_name = kv_service.get_secret(Constants.USERS_CONTAINER_NAME)
        self.cosmos_db_service = CosmosDbService(self.database_id)
        self.container = self.cosmos_db_service.get_container(self.users_container_name)

    def create_user(self, user: User, telemetry: LoggerService, tel_props):
        tel_props = tel_props.copy()
        tel_props.update({Constants.USER_ID: user.user_id, "action": "create_user"})
        telemetry.info(f"Creating user: {user}", tel_props)
        try:
            self.container.create_item(asdict(user))
            telemetry.info(f"User created: {user}", tel_props)
        except Exception as e:
            msg = f"Error occurred while creating user: user_id, name: {user.user_id}, {user.name} {str(e)}"
            telemetry.exception(msg, tel_props)
            raise e

    def get_user(self, user_id, telemetry: LoggerService, tel_props) -> User:
        query = "SELECT * FROM c WHERE c.user_id = @user_id"
        parameters = [{"name": "@user_id", "value": user_id}]
        tel_props = tel_props.copy()
        tel_props.update({Constants.COSMOS_QUERY: query, "action": "get_user"})
        try:
            result = self.container.query_items(query, parameters=parameters, enable_cross_partition_query=True)
            users = list(result)
            
            if len(users) == 0:
                telemetry.info(f"No user found for user_id: {user_id}", tel_props)
                return None
            
            if len(users) > 1:
                telemetry.exception(f"Multiple users found for user_id: {user_id}", tel_props)
            
            telemetry.info(f"User fetched: {users}", tel_props)
            return from_dict(data_class=User, data= users[0])
        except Exception as e:
            telemetry.exception(f"Error occurred while fetching user: {str(e)}", tel_props)
            raise e

    def update_user(self, user: User, telemetry: LoggerService, tel_props):
        tel_props = tel_props.copy()
        tel_props.update({Constants.USER_ID: user.user_id, "action": "update_user"})
        telemetry.info(f"Updating user: {user}", tel_props)
        try:
            self.container.upsert_item(asdict(user))
            telemetry.info(f"User updated: {user}", tel_props)
        except Exception as e:
            msg = f"Error occurred while updating user: user_id, name: {user.user_id}, {user.name} {str(e)}"
            telemetry.exception(msg, tel_props)
            raise e

    def delete_user(self, user_id, telemetry: LoggerService, tel_props):
        tel_props = tel_props.copy()
        telemetry.info(f"Deleting user: {user_id}", tel_props)
        try:
            self.container.delete_item(user_id, partition_key=user_id)
            telemetry.info(f"User deleted: {user_id}", tel_props)
        except Exception as e:
            msg = f"Error occurred while deleting user: user_id: {user_id} {str(e)}"
            telemetry.exception(msg, tel_props)
            raise e

    def store_user(self, user: User, telemetry: LoggerService, tel_props):
        tel_props = tel_props.copy()
        tel_props.update({Constants.USER_ID: user.user_id, "action": "store_user"})
        
        telemetry.info(f"Storing user: {user}", tel_props)
        existing_user = self.get_user(user.user_id, telemetry, tel_props)
        try:
            if existing_user:
                telemetry.info(f"User {user.user_id} already exists. Updating user.", tel_props)
                self.update_user(user, telemetry, tel_props)
            else:
                telemetry.info(f"User {user.user_id} does not exist. Creating user.", tel_props)
                self.create_user(user, telemetry, tel_props)
        except Exception as e:
            msg = f"Error occurred while storing user: user_id, name: {user.user_id}, {user.name} {str(e)}"
            telemetry.exception(msg)
            raise e
        