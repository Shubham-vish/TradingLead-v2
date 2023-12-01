import os
from ...Utils.constants import Constants

class AppConfig:
    _instance = None
    properties = {
        Constants.APP: os.environ[Constants.telemetry_app],
        Constants.ENV: os.environ[Constants.telemetry_env],
        Constants.VERSION: os.environ[Constants.telemetry_version],
        Constants.SERVICE: os.environ[Constants.telemetry_service]
    }

    @staticmethod
    def get_instance():
        if AppConfig._instance is None:
            AppConfig._instance = AppConfig()
        return AppConfig._instance

    @classmethod
    def get_properties(cls):
        return cls.properties