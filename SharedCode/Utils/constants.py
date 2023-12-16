class Constants:
    # Telemetry property keys
    APP = "App"
    ENV = "Env"
    VERSION = "Version"
    SERVICE = "Service"
    
    # Telemetry property constants (for environment variables)
    telemetry_app = "TelemetryPropApp"
    telemetry_env = "TelemetryPropEnv"
    telemetry_version = "TelemetryPropVersion"
    telemetry_service = "TelemetryPropService"
    
    number_of_days_to_fetch_participation_data = "NumberOfDataParticipationDataToBeFetched"
    
    # Telemetry Service Names
    fetch_stock_info_service = "TickerListService"
    holdings_service = "HoldingsService"
    access_token_generator_service = "AccessTokenGeneratorService"
    strategy_executor_service = "StrategyExecutorService"
    fetch_store_participants_data_service = "FetchStoreParticipantsDataService"
    
    # telemetry custom dimensions keys
    username = "username"
    contact_number = "contact_number"
    operation_id = "operation_id"

    ### KeyVault Constants ###
    fyers_username = "FyersUserName"
    client_id = "ClientId"
    contact_number = "ContactNumber"
    fyers_totp_secret_key = "FyersTotpSecretKey"
    fyers_pin = "FyersPin"
    secret_key = "SecretKey"
    redirect_uri = "RedirectUri"
    
    ### Cosmos DB Constants ###
    COSMOS_DB_URL = "CosmosDbUrl"
    COSMOS_DB_KEY = "CosmosDbKey"
    HOLDINGS_CONTAINER_NAME = "CosmosHoldingsContainer"
    PARTICIPANTS_DATA_CONTAINER = "CosmosParticipantsDataContainer"
    ALERTS_CONTAINER_NAME = "CosmosAlertsContainer"
    DATABASE_ID = "CosmosDbDatabaseId"
    
    ### HTTP Constants
    HTTP_GET = "GET"
    HTTP_POST = "POST"
    HTTP_DELETE = "DELETE"
    REQUEST_METHOD = "request_method"
    REQUEST_BODY = "request_body"
    RESPONSE_BODY = "response_body"
    REQUEST_PARAM_USER_ID = "userId"
    
    COSMOS_QUERY = "CosmosQuery"
    COSMOS_PARAMS = "CosmosParams"

    CACHE_KEY = "CacheKey"