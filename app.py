import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
import flask
import os

# We start a Flask server
server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

# Dash then creates the app on the server
app = dash.Dash('app', server=server)

# This is a Python wrapper for generating HTML code.
app.layout = html.Div([
    html.H1('My better stock ticker title'),  # make a big header at the top
    dcc.Dropdown(  # dash-core-components has a Dropdown template
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Chipotle', 'value': 'CPE'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],
        value='COKE'  # the default value when you open the app
    ),
    dcc.Graph(id='my-graph'),  # ... as well as a graph template that takes a
                              # dictionary created by update_graph()

    # added a Date Picker Range from dash core components
    # more options here https://plot.ly/dash/dash-core-components/datepickerrange
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=dt(2001, 1, 1),
        end_date=dt.now()
    )
], className="container")

# this is a Python decorator. It feeds update_graph() into app.callback().
# It fetches the value from my-dropdown and feeds it into update_graph() as
# selected_dropdown_value.
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value'),
                                             Input('date-picker-range', 'start_date'),  # added more inputs
                                             Input('date-picker-range', 'end_date')])
def update_graph(selected_dropdown_value, start_date, end_date):
    df = web.DataReader(
        selected_dropdown_value, data_source='google',
        start=start_date, end=end_date)

    price_data = {
            'x': df.index,
            'y': df.Close,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }

    # return a dictionary which is fed to my-graph
    return {
        'data': [price_data],  # list of data dictionaries
        'layout': {  # legend would go here
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            },
            'title': 'Fig Title',
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'Price'}
        }
    }

# starts a webserver when running python app.py
if __name__ == '__main__':
    app.run_server()
