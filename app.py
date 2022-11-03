from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import main
from main import *

app = Dash(__name__)

# TODO: Create drop down menu associated with these variables.
# Test values
ticker = 'USDGBP=X'
time_range = '1mo'
interval = '60m'
level_strength = 2

# Create the data that will be used for the graph on first load.
df = pd.DataFrame(data=main.fetch_ticker(ticker, time_range, interval))
support_df = main.is_support(df, level_strength)
resistance_df = main.is_resistance(df, level_strength)
levels = main.create_level_coords(df)

def update_graph_data():

    return


def redraw_graph():
    return


# Plot the main graph
fig = go.Figure(
    data=[go.Candlestick(
        name='Candle',
        x=df['Datetime'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
    )]
)

# Remove non trading times
fig.update_xaxes(
    rangebreaks=[
        dict(bounds=['sat',  'mon']),
        dict(bounds=[16, 9.5], pattern='hour')
    ]
)

# Remove rangeslider
fig.update_layout(
    title='GBP : USD Exchange Rate Performance',
    xaxis=dict(
        title='Date',
        rangeslider=dict(
            visible=False
        )
    ),
    yaxis=dict(
        title='Exchange Rate',
    )
)

# Plot Support levels onto the main graph
fig.add_trace(
    go.Scatter(
        mode='markers',
        marker_symbol='triangle-up',
        x=levels['Support X'],
        y=levels['Support Y'],
        name='Support',
        marker=dict(
            color='Blue',
            size=15,
        )
    )
)

# Plot Resistance levels onto the main graph
fig.add_trace(
    go.Scatter(
        mode='markers',
        marker_symbol='triangle-down',
        x=levels['Resistance X'],
        y=levels['Resistance Y'],
        name='Resistance',
        marker=dict(
            color='Purple',
            size=15,
        )
    )
)

# Layout options
app.layout = html.Div(children=[
    html.H1(children='Stock Picker - Support and Resistance Level Identifier'),

    # Dropdown box: Time Period Selection
    html.Div(children='''
        Select time period to evaluate:
    '''),
    html.Div([
        dcc.Dropdown(
            options={
                '1 Day': '1d',
                '1 Week': '1wk',
                '2 Weeks': '2wk',
                '1 Month': '1mo',
                '3 Months': '3mo',
                '6 Months': '6mo',
                '1 Year': '1y',
                '2 Years': '2y',
                '3 Years': '3y',
                '5 Years': '5y',
                '10 Years': '10y',
            },
            value='2wk',
            id='dd-time-period'
        ),
        html.Div(id='dd-time-period-container')
    ],
        style={'width': '10%'}
    ),

    # Dropdown box: Time Period Selection
    html.Div(children='''
    Select Interval to show:
    '''),
    html.Div([
        dcc.Dropdown(
            options={
                '5 Mins': '5m',
                '15 Mins': '15m',
                '30 Mins': '30m',
                '1 Hour': '60m',
                '1.5 Hours': '90m',
                '1 Day': '1d',
                '2 Days': '2d',
                '5 Days': '5d',
                '1 Week': '1wk',
                '2 Weeks': '2wk',
                '1 Month': '1mo',
            },
            value='60m',
            id='dd-interval'
        ),
        html.Div(id='dd-interval-container')
    ],
        style={'width': '10%'}
    ),

    # Main graph
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
])

# Callback options

# Time period updater
@app.callback(
    Output('dd-time-period-container', 'children'),
    Output('dd-interval-container', 'children'),
    Input('dd-time-period', 'value'),
    Input('dd-interval', 'value'),
)


def update_output(value):
    time_range == value
    update_graph_data()
    redraw_graph()
    return


if __name__ == '__main__':
    app.run_server(debug=True)
