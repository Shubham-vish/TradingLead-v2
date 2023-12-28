import pandas as pd
from datetime import datetime, timedelta
import requests
from SharedCode.Repository.KeyVault.keyvault_service import KeyVaultService
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Repository.Cache.redis_cache_service import RedisCacheService
from SharedCode.Repository.CosmosDB.participants_data_repository import ParticipantsDataCosmosRepository
from SharedCode.Repository.CosmosDB.CosmosUtils.cosmos_db_service import CosmosDbService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils

kv_service = KeyVaultService()
telemetry = LoggerService()
redis_cache_service = RedisCacheService()

database_id = kv_service.get_secret(Constants.DATABASE_ID)
participants_data_container = kv_service.get_secret(Constants.PARTICIPANTS_DATA_CONTAINER)
cosmos_db_service = CosmosDbService(database_id)
participants_data_cosmos_repo = ParticipantsDataCosmosRepository(cosmos_db_service, participants_data_container)


def is_weekday(date):
    return date.weekday() < 5  # 0 is Monday, 6 is Sunday

# Function to generate URL for a given date
def create_url_for_date(date: datetime) -> str:
    base_url = 'https://archives.nseindia.com/content/nsccl/fao_participant_oi_'
    date_str = date.strftime('%d%m%Y')  # Format the date as DDMMYYYY
    return f"{base_url}{date_str}.csv"

def is_data_available(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return False

def store_data_for_day(date: datetime, tel_props):
    if is_weekday(date):
        url = create_url_for_date(date)
        if is_data_available(url):
            try:
                df = pd.read_csv(url, header=1)
                participants_data_cosmos_repo.store_data_for_day(date, df, telemetry, tel_props)
                telemetry.info(f"Data for {date.strftime('%d-%m-%Y')}:")
                telemetry.info(df.head())
            except pd.errors.EmptyDataError:
                telemetry.info(f"No data available for {date.strftime('%d-%m-%Y')}.")
            except Exception as e:
                telemetry.info(f"An error occurred while fetching data for {date.strftime('%d-%m-%Y')}: {e}")
        else:
            telemetry.info(f"Data not available. Check why not available on this date: {date.strftime('%d-%m-%Y')}")
    else:
        telemetry.info(f"{date.strftime('%d-%m-%Y')} is not a weekday.")
    
def fetch_store_data_for_n_days(n: int, tel_props):
    check_date = datetime.now()
    for _ in range(n):
        store_data_for_day(check_date, tel_props)
        check_date -= timedelta(days=1)
        
def delete_all_data(tel_props):
    participants_data_cosmos_repo.delete_all_data(telemetry, tel_props)

operation_id = "RandomOperationId"

tel_props = {
        Constants.SERVICE : Constants.access_token_generator_service,
        Constants.operation_id : operation_id,
    }

# fetch_store_data_for_n_days(100, tel_props)