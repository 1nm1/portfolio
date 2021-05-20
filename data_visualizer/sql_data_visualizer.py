import time
import pandas as pd
import numpy as np
from datetime import datetime
import base64
import json
import yfinance as yf
from dateutil.relativedelta import relativedelta
import datetime as dt

import seaborn as sns
import sys

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import plotly.express as px
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from formats import *
import warnings
warnings.simplefilter("ignore")

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG],suppress_callback_exceptions=True)

content = html.Div(id="page-content", style=content_style_1)

sidebar = html.Div([
                html.H4("Data Viz 3000"),
                html.Hr(style={'background-color':'white'}),
                html.P(
                    "Visualize any database data!"),
                html.P(
                    "Application developed by Nathan Meek. v0.1"),
                dbc.Nav(
                    [
                        dbc.NavLink("Data Viz", href="/dv", active="exact"),
                        dbc.NavLink("Settings", href="/st", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            style=sidebar_style_1,
        )

dv_page = html.Div([
            dbc.Navbar([
                html.H5("Table: "),
                dcc.Dropdown(
                    id='dropdown-table',
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montreal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value='NYC'
                    ),
                html.H5("Column: "),
                dcc.Dropdown(
                    id='dropdown-column',
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montreal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value='NYC'
                    ),
                dbc.Spinner(
                    html.Div(id="loading-stock",
                                style={'color':'white',
                                    'font-size':'18px'}),
                    color="white"
                    ),
                ],
                style=nav_bar_style_1),
            ])
st_page = html.Div([html.H3("Settings page")])

app.layout = html.Div([
                dcc.Store(
                    id='stock_data'),
                dcc.Store(
                    id='stock_data_60d'),
                dcc.Store(
                    id='info_store'), 
                dcc.Store(
                    id='recommend_store'),
                dcc.Location(id="url"), 
                html.H6(".",
                    id='text_system_message',
                    style=text_system_message_style),
                sidebar, 
                content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    # print(pathname)
    if pathname == "/":
        return dv_page
    if pathname == "/dv":
        return dv_page
    elif pathname == "/st":
        return st_page
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ]
    )



if __name__ == '__main__':
    app.run_server(debug=True,)
