from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import main
from main import *

app = Dash(__name__)

# assume you have a "long-form" data frame
test_ticker = 'USDGBP=X'
test_time_range = '2wk'
test_interval = '60m'
test_strength = 2

df = pd.DataFrame(data=main.fetch_ticker(test_ticker, test_time_range, test_interval))
support_df = main.is_support(df, test_strength)
resistance_df = main.is_resistance(df, test_strength)
levels = main.create_level_coords(df)

fig = go.Figure(
    data=[go.Candlestick(
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
    title='GBP : USD Exchange Rate Performance - 2 Week, Hourly Candles',
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

# Plot Support levels.
fig.add_trace(
    go.Scatter(
        mode='markers',
        marker_symbol='triangle-up',
        x=levels['Support X'],
        y=levels['Support Y'],
        name='Support',
        marker=dict(
            color='Yellow',
            size=15,
        )
    )
)

# Plot Resistance levels.
fig.add_trace(
    go.Scatter(
        mode='markers',
        marker_symbol='triangle-down',
        x=levels['Resistance X'],
        y=levels['Resistance Y'],
        name='Resistance',
        marker=dict(
            color='MediumPurple',
            size=15,
        )
    )
)

# Layout options
app.layout = html.Div(children=[
    html.H1(children='Stock Picker - Support and Resistance Level Identifier'),

    html.Div(children='''
        Dash App - Joshua S Hammond.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
