from functools import lru_cache
import plotly.graph_objs as go
import numpy as np
import yfinance as yf
from flask import Flask, jsonify, Response
import azure.functions as func
import time
from SharedCode.Repository.Logger.logger_service import LoggerService
from SharedCode.Utils.constants import Constants
from SharedCode.Utils.utility import FunctionUtils
from SharedCode.Runners.plot_chart_runner import plot_chart_runner

telemetry = LoggerService()

def main(req: func.HttpRequest,  context: func.Context ) -> func.HttpResponse:
    
    operation_id = FunctionUtils.get_operation_id(context)

    tel_props = {
        Constants.SERVICE : Constants.plot_chart_service,
        Constants.operation_id : operation_id,
    }
    
    telemetry.info('Plot Chart HTTP trigger function started.', tel_props)
    

    response =  plot_chart_runner(req.params, tel_props)
    
    tel_props.update({"response":response})
    telemetry.info('Plot Chart HTTP trigger function processed a request.', tel_props)

    return response