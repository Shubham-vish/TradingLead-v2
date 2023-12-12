# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from Notebooks.setupConfig import setup_config
setup_config()
# Above lines are only for local notebook testing. Not to be used in production.

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
from FetchAndStoreParticipantsData.fetch_store_participants_data_runner import fetch_store_data_for_n_days, delete_all_data

number_of_days = int(os.environ[Constants.number_of_days_to_fetch_participation_data])

operation_id = "RandomOperationId"

tel_props = {
        Constants.SERVICE : Constants.access_token_generator_service,
        Constants.operation_id : operation_id,
    }


tel_props.update({"number_of_days": number_of_days})

fetch_store_data_for_n_days(number_of_days, tel_props)
delete_all_data(tel_props)