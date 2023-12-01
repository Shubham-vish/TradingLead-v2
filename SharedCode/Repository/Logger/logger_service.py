from .logger_factory import LoggerFactory
from .appconfig import AppConfig

class LoggerService:
    def __init__(self):
        self.logger = LoggerFactory.get_trace_logger()
        self.event_logger = LoggerFactory.get_event_logger()
        self.global_properties = AppConfig().get_instance().get_properties()

    def info(self, message, properties=None):
        extra_properties = self._combine_properties(properties)
        self.logger.info(message, extra=extra_properties)
        
    def event(self, message, properties=None):
        extra_properties = self._combine_properties(properties)
        self.event_logger.info(message, extra=extra_properties)

    def warning(self, message, properties=None):
        extra_properties = self._combine_properties(properties)
        self.logger.warning(message, extra=extra_properties)

    def error(self, message, properties=None):
        extra_properties = self._combine_properties(properties)
        self.logger.error(message, extra=extra_properties)
    
    def exception(self, message, properties=None):
        extra_properties = self._combine_properties(properties)
        self.logger.exception(message, extra=extra_properties)

    def _combine_properties(self, properties):
        combined_properties = {**self.global_properties, **(properties or {})}
        props = {'custom_dimensions': combined_properties}
        props['operation_id'] = "ec5b8e658ea7c671da11b230a16d9c20"
        return props
