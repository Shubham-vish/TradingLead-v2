import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
import os
from opencensus.trace import config_integration
from  opencensus.ext.azure.log_exporter  import  AzureEventHandler
config_integration.trace_integrations(['logging'])

class LoggerFactory:
    _trace_logger_instance = None
    _event_logger_instance = None

    @staticmethod
    def get_trace_logger():
        connection_string = os.environ["APPINSIGHTS_ConnectionString"]
        if LoggerFactory._trace_logger_instance is None:
            logger = logging.getLogger("traceLogger")
            logger.addHandler(AzureLogHandler(connection_string=connection_string))
            LoggerFactory._trace_logger_instance = logger
        return LoggerFactory._trace_logger_instance

    @staticmethod
    def get_event_logger():
        connection_string = os.environ["APPINSIGHTS_ConnectionString"]
        if LoggerFactory._event_logger_instance is None:
            logger = logging.getLogger("eventLogger")
            logger.addHandler(AzureEventHandler(connection_string=connection_string))
            LoggerFactory._event_logger_instance = logger
        return LoggerFactory._event_logger_instance
