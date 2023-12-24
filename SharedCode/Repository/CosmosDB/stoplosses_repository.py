from azure.cosmos import PartitionKey
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Models.UserStoplosses import UserStoplosses

class StoplossesRepository:
    def __init__(self, cosmos_service: CosmosDbService, container_name):
        self.container = cosmos_service.get_container(container_name)

    def create_stoploss(self, stoploss):
        self.container.create_item(stoploss)

    def get_stoplosses_by_user(self, user_id):
        query = f"SELECT * FROM c WHERE c.UserId = '{user_id}'"
        result = self.container.query_items(query, enable_cross_partition_query=True)
        return list(result)

    def update_stoploss(self, stoploss):
        self.container.upsert_item(stoploss)

    def delete_stoploss(self, stoploss_id):
        self.container.delete_item(stoploss_id, PartitionKey(stoploss_id))

    def store_user_stoplosses(self, user_stoplosses:UserStoplosses, telemetry: LoggerService, tel_props):
        user_id = user_stoplosses.user_id
        existing_stoplosses = self.get_stoplosses_by_user(user_id)
        if existing_stoplosses:
            telemetry.info(f"User {user_id} already has stoplosses. Updating stoplosses.", tel_props)
            for stoploss in user_stoplosses.stop_losses:
                stoploss_id = f"{user_id}_{stoploss.ticker}"
                existing_stoploss = next((s for s in existing_stoplosses if s["id"] == stoploss_id), None)
                if existing_stoploss:
                    existing_stoploss["price"] = stoploss.price
                    existing_stoploss["trendStart"] = stoploss.trend_start
                    existing_stoploss["trendEnd"] = stoploss.trend_end
                    self.update_stoploss(existing_stoploss)
                else:
                    stoploss_dict = {
                        "id": stoploss_id,
                        "UserId": user_id,
                        "Ticker": stoploss.ticker,
                        "Price": stoploss.price,
                        "TrendStart": stoploss.trend_start,
                        "TrendEnd": stoploss.trend_end
                    }
                    self.create_stoploss(stoploss_dict)
        else:
            telemetry.info(f"User {user_id} does not have any stoplosses. Creating stoplosses.", tel_props)
            for stoploss in user_stoplosses.stop_losses:
                stoploss_dict = {
                    "id": f"{user_id}_{stoploss.ticker}",
                    "UserId": user_id,
                    "Ticker": stoploss.ticker,
                    "Price": stoploss.price,
                    "TrendStart": stoploss.trend_start,
                    "TrendEnd": stoploss.trend_end
                }
                self.create_stoploss(stoploss_dict)
