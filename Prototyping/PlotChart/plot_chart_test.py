# Following lines are only for local notebook testing. Not to be used in production.
import os
import sys

sys.path.append(os.path.abspath(os.path.join("../..")))
sys.path.append(os.path.abspath(os.path.join("..")))
from Prototyping.setupConfig import setup_config

setup_config()
# Above lines are only for local notebook testing. Not to be used in production.


import azure.functions as func
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.stock_chart import StockChart
from SharedCode.Utils.constants import Constants
import types
telemetry = LoggerService()
stock_chart = StockChart()

operation_id = "RandomOperationId"

tel_props = {
    Constants.SERVICE: Constants.access_token_generator_service,
    Constants.operation_id: operation_id,
}

params = {
    'trend_start': '2023-01-05',
    'trend_end': '2023-10-26',
    'ticker': 'AAPL',
    'chart_type': 'scatter',
    "avg_price": 170,
    "stop_price": 160
}

from azure.functions import HttpRequest
import IPython
req = HttpRequest(method="get", url="www.google.com", params=params, body = None, headers=None, route_params=None)

req.params
stock_chart.generate_chart(**params).show()
stock_chart.generate_chart(**req.params).show()


# 
def plot_chart(params,  tel_props) -> func.HttpResponse:

    tel_props.update({"params": params, "action":"plot_chart"})
    telemetry.info(f'Received parameters: {params}', tel_props)

    try:
        fig =  stock_chart.generate_chart(**params)
        html_string = fig.to_html(full_html=False)
        return func.HttpResponse(body=html_string, mimetype='text/html')
    except Exception as e:
        telemetry.exception(f'An error occurred: {str(e)}.', tel_props)
        return func.HttpResponse("An error occurred", status_code=500)
    
html_string = plot_chart(req.params, tel_props).get_body()

IPython.display.Image(html_string, width=700, height=600)

type(html_string)