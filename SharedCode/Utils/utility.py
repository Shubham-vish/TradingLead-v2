class FunctionUtils:
    @staticmethod
    def get_operation_id(context):
        traceparent = context.trace_context.Traceparent
        try:
            operation_id = f"{traceparent}".split('-')[1]
        except IndexError:
            operation_id = 'default_id'
        return operation_id

    # Add other utility methods here as needed
