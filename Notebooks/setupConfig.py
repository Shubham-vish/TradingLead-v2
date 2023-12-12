import azure.functions as func
import os
import json
import sys

def setup_config():
    module_path = os.path.abspath(os.path.join('..'))
    if module_path not in sys.path:
        sys.path.append(module_path)
    config = {
    "IsEncrypted": False,
    "Values": {
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "pythonPath": "C:\\Users\\Shubham Vishwakarma\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe",
        "APPINSIGHTS_INSTRUMENTATIONKEY": "f0cd5280-7f75-4c2e-9e92-93bc75b8a8c4",
        "APPINSIGHTS_ConnectionString": "InstrumentationKey=f0cd5280-7f75-4c2e-9e92-93bc75b8a8c4",
        "KEY_VAULT_URI": "https://kv-tradinglead.vault.azure.net/",
        "TelemetryPropApp": "TradingLead - Backend Function App",
        "TelemetryPropEnv": "local",
        "TelemetryPropVersion": "1.0.0",
        "TelemetryPropService": "TradingLead - General Service",
        "SCHEDULE_CRON_FOR_ACCESS_TOKEN_GENERATOR": "0 * * * * *",
        "SCHEDULE_CRON_FOR_PARTICIPATION_DATA_STORE": "0 */10 * * * *",
        "NumberOfDataParticipationDataToBeFetched": "20"
    },
    "Host": {
        "CORS": "http://localhost:3000",
        "CORSCredentials": True
    }
    }


    module_path = os.path.abspath(os.path.join('..'))
    if module_path not in sys.path:
        sys.path.append(module_path)


    # Set the environment variables
    for key, value in config['Values'].items():
        os.environ[key] = value

    # Verify the environment variables are set
    for key in config['Values'].keys():
        print(f'{key}: {os.getenv(key)}')
