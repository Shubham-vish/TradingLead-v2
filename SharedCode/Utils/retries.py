from SharedCode.Utils.utility import FunctionUtils
import time
from functools import wraps
from SharedCode.Repository.Logger.logger_service import LoggerService
# Retry decorator

telemetry = LoggerService()

def retry_decorator_with_tel_props(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tel_props = kwargs['tel_props']
            retries = 0
            while retries < max_retries:
                try:
                    telemetry.info(f"Starting '{func.__name__}' with args: {args}, kwargs: {kwargs}", tel_props)
                    result = func(*args, **kwargs)
                    telemetry.info(f"Successful execution of '{func.__name__}'", tel_props)
                    
                    return result
                except Exception as e:
                    telemetry.exception_retriable(f"Error in '{func.__name__}': {e}, retrying {retries + 1}/{max_retries}", tel_props)
                    retries += 1
                    time.sleep(delay)
            raise Exception(f"Max retries exceeded for function {func.__name__}")
        return wrapper
    return decorator