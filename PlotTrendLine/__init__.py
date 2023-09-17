from functools import lru_cache
import logging
import plotly.graph_objs as go
import numpy as np
import yfinance as yf
from flask import Flask, jsonify, Response
import azure.functions as func
import time

app = Flask(__name__)
app.app_context().push()

@lru_cache(maxsize=32)
def generate_chart(date1, date2, ticker, chart_type, point):
    max_retries = 3
    retry_delay = 0.5  # in seconds
    
    for attempt in range(1, max_retries + 1):
        try:
            hist = yf.download(ticker, period="1y")
            df = hist.loc[(hist.index == date1) | (hist.index == date2)]

            if chart_type == 'scatter':
                fig = go.Figure(data=go.Scatter(x=hist.index, y=hist['Close'], mode='lines'))
            else:
                fig = go.Figure(data=[go.Candlestick(x=hist.index,
                                                    open=hist['Open'], high=hist['High'],
                                                    low=hist['Low'], close=hist['Close'])
                                      ])

            if date1 and date2:
                x = [hist.index.get_loc(date1), hist.index.get_loc(date2)]
                y = df[point].tolist()
                slope, intercept = np.polyfit(x, y, 1)
                logging.info(f'Calculated slope={slope}, intercept={intercept}')

                x_val_index = hist.index.get_loc(hist.index[-1])
                y_val = slope * x_val_index + intercept

                fig.add_trace(go.Scatter(
                    x=df.index, y=df[point], mode='markers', marker=dict(size=10)))

                fig.add_shape(type="line",
                              x0=date1, y0=slope * x[0] + intercept,
                              x1=hist.index[-1], y1=y_val,
                              line=dict(color='red', width=3))

            html_string = fig.to_html(full_html=False)
            return html_string
        
        except Exception as e:
            logging.error(f'An error occurred: {str(e)}. Attempt {attempt} of {max_retries}.')
            if attempt < max_retries:
                logging.info(f'Retrying in {retry_delay * 1000} milliseconds...')
                time.sleep(retry_delay)
            else:
                logging.error('Max retries reached. Exiting.')
                raise e  # Re-raise the exception to handle it upstream

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    date1 = req.params.get('date1')
    date2 = req.params.get('date2')
    ticker = req.params.get('ticker')
    chart_type = req.params.get('chart_type')
    point = req.params.get('point')

    logging.info(f'Received parameters: date1={date1}, date2={date2}, ticker={ticker}, chart_type={chart_type}, point={point}')

    if not point:
        point = 'Close'
    if not ticker:
        ticker = 'AAPL'

    try:
        html_string = generate_chart(date1, date2, ticker, chart_type, point)
        return func.HttpResponse(body=html_string, mimetype='text/html')
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}.')
        return func.HttpResponse("An error occurred", status_code=500)
