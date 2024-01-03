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

    number_of_days_to_fetch_participation_data = (
        "NumberOfDataParticipationDataToBeFetched"
    )

    # Telemetry Service Names
    fetch_stock_info_service = "TickerListService"
    holdings_service = "HoldingsService"
    user_service = "UsersService"
    access_token_generator_service = "AccessTokenGeneratorService"
    fetch_store_participants_data_service = "FetchStoreParticipantsDataService"
    fetch_store_history_data_service = "FetchStoreHistoryDataService"
    market_start_executor_services = "MarketStartExecutorService"
    market_close_executor_services = "MarketCloseExecutorService"
    order_executor_service = "OrderExecutorService"
    stoploss_executor_service = "StopLossExecutorService"
    strategy_executor_service = "StrategyExecutorService"
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

    STORAGE_CONNECTION_STRING = "StorageConnectionString"
    STOCK_HISTORY_CONTAINER = "stock-history-data"
    DIR_NIFTY_50 = "nifty50-stocks"

    ### Cosmos DB Constants ###
    COSMOS_DB_URL = "CosmosDbUrl"
    COSMOS_DB_KEY = "CosmosDbKey"
    HOLDINGS_CONTAINER_NAME = "CosmosHoldingsContainer"
    PARTICIPANTS_DATA_CONTAINER = "CosmosParticipantsDataContainer"
    ALERTS_CONTAINER_NAME = "CosmosAlertsContainer"
    STOPLOSS_CONTAINER_NAME = "StoplossContainerName"
    STRATEGY_CONTAINER_NAME = "StrategyContainerName"
    USERS_CONTAINER_NAME = "UsersContainerName"
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

    communication_service_endpoint = "CommunicationServiceEndpoint"


    color_green = "#00FF00"
    color_red = "#FF0000"
    color_black = "#000000"
    color_white = "#FFFFFF"
    color_blue = "#0000FF"
    color_yellow = "#FFFF00"
    color_pink = "#FFC0CB"
    
    
    timeframe_30t = "30T"
    timeframe_hourly = "1H"
    timeframe_daily = "1D"
    timeframe_weekly = "1W"
    timeframe_monthly = "1M"
    
    USER_ID = "user_id"
    STOPLOSS_ID = "stoploss_id" 
    
    kv_secret_name = "kv_secret_name"
    fyers_user_name = "fyers_user_name"
    
    
    service_bus_connection_string = "ServiceBusConnectionString"
    ORDER_TOPIC_NAME = "OrderTopicName"