import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.stock_chart import StockChart
import types
telemetry = LoggerService()
stock_chart = StockChart()


def plot_chart_runner(params,  tel_props) -> func.HttpResponse:

    tel_props.update({"params": params, "action":"plot_chart"})
    telemetry.info(f'Received parameters: {params}', tel_props)

    try:
        fig =  stock_chart.generate_chart(**params, tel_props=tel_props)
        html_string = fig.to_html(full_html=False)
        return func.HttpResponse(body=html_string, mimetype='text/html')
    except Exception as e:
        telemetry.exception(f'An error occurred: {str(e)}.', tel_props)
        return func.HttpResponse("An error occurred", status_code=500)