from .cosmos_db_factory import CosmosDbFactory

class CosmosDbService:
    def __init__(self, database_id):
        self.client = CosmosDbFactory.get_cosmos_client()
        self.database = self.client.get_database_client(database_id)

    def get_container(self, container_id):
        return self.database.get_container_client(container_id)
