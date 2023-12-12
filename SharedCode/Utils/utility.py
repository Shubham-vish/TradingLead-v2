from datetime import datetime, timedelta

class FunctionUtils:
    @staticmethod
    def get_operation_id(context):
        traceparent = context.trace_context.Traceparent
        try:
            operation_id = f"{traceparent}".split('-')[1]
        except IndexError:
            operation_id = 'default_id'
        return operation_id

    @staticmethod
    def get_ist_time(time=None):
        utc_time = time if time is not None else datetime.utcnow()
        # IST is UTC + 5 hours 30 minutes
        ist_time = utc_time + timedelta(hours=5, minutes=30)
        return ist_time
    # Add other utility methods here as needed
