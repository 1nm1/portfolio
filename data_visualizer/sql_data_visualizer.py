
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
import sql_data_viz_functions as sdvf
from formats import *
import warnings
warnings.simplefilter("ignore")

app = dash.Dash(
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True)

content = html.Div(id="page-content", style=content_style_1)

sidebar = html.Div([
                html.H4("Data Viz 3000"),
                html.Hr(style={'background-color': 'white'}),
                html.P(
                    "Visualize any database data!"),
                dbc.Nav(
                    [
                        dbc.NavLink("Data Viz", href="/dv", active="exact"),
                        dbc.NavLink("Settings", href="/st", active="exact"),
                        dbc.NavLink("Event Log", href="/el", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
                html.P(
                    "Application developed by Nathan Meek",
                    style={'position': 'absolute', 'bottom': '50px'}),
                html.P(
                    "Application version v0.1",
                    style={'position': 'absolute', 'bottom': '10px'}),
            ],
            style=sidebar_style_1,
        )

dv_page = html.Div([
            dbc.Navbar([
                html.H5("Table: ",
                    style=label_navbar_style_1),
                dcc.Dropdown(
                    id='dropdown-table',
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montreal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value='NYC'
                    ),
                html.H5("Column: ",
                    style=label_navbar_style_1),
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
                style=nav_bar_style_1,
                color='dark'),
            ])

st_page = html.Div([
            dbc.Form([
                dbc.FormGroup([
                    dbc.Label(
                        "Server",
                        html_for="input-server",
                        style=formgroup_settings_label_style_1),
                    dbc.Input(
                        type="text",
                        id="input-server",
                        placeholder="Enter server location",
                        style=formgroup_settings_input_style_1),
                    ],
                    row=True),
                dbc.FormGroup([
                    dbc.Label(
                        "Database", 
                        html_for="input-db",
                        style=formgroup_settings_label_style_1),
                    dbc.Input(
                        type="text", 
                        id="input-db", 
                        placeholder="Enter database",
                        style=formgroup_settings_input_style_1),
                    ],
                    row=True),
                dbc.FormGroup([
                    dbc.Label(
                        "Database User", 
                        html_for="input-user",
                        style=formgroup_settings_label_style_1),
                    dbc.Input(
                        type="text",
                        id="input-user",
                        placeholder="Enter database user",
                        style=formgroup_settings_input_style_1),
                    ],
                    row=True),
                dbc.FormGroup([
                    dbc.Label(
                        "User Password", 
                        html_for="input-userpw",
                        style=formgroup_settings_label_style_1),
                    dbc.Input(
                        type="password",
                        id="input-userpw",
                        placeholder="Enter user password",
                        style=formgroup_settings_input_style_1),
                    ],
                    row=True),
                dbc.FormGroup([
                    dbc.Label(
                        "Reenter Password",
                        html_for="input-userpw2",
                        style=formgroup_settings_label_style_1),
                    dbc.Input(
                        type="password",
                        id="input-userpw2",
                        placeholder="Reenter password",
                        style=formgroup_settings_input_style_1),
                    ],
                    row=True),
                ],
                style=formgroup_settings_style_1),
            html.Div([
                dbc.Button(
                    "Clear form",
                    id='button-st-clear',
                    color="secondary",
                    style=button_settings_clear_form_style_1),
                dbc.Button(
                    "Disconnect",
                    id='button-db-disconnect',
                    color="secondary",
                    style=button_settings_disconnect_style_1),
                dbc.Button(
                    "Connect",
                    id='button-db-connect',
                    color="primary",
                    style=button_settings_connect_style_1),                
                dbc.Alert(
                    "Not Connected",
                    id='alert-db-connect',
                    color="danger",
                    style=alert_settings_style_1),
                ])
            ])

el_page = html.Div([
    html.H5("Application Event Log"),
    dcc.Textarea(
        id='textarea-event-log',)
])

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
                sidebar,
                content])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def render_page_content(pathname):
    # print(pathname)
    if pathname == "/":
        return dv_page
    if pathname == "/dv":
        return dv_page
    elif pathname == "/st":
        return st_page
    elif pathname == "/el":
        return el_page
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ]
    )


@app.callback(
    [Output("alert-db-connect", "children"),
     Output("alert-db-connect", "color")],
    [Input("button-db-connect", "n_clicks"),
     Input("button-db-connect", "n_clicks_timestamp"),
     Input("button-db-disconnect", "n_clicks_timestamp")],
    [State("input-server", "value"),
     State("input-db", "value"),
     State("input-user", "value"),
     State("input-userpw", "value"),
     State("input-userpw2", "value")])
def connect_to_db(con_clicks, con_time, dis_time, server, db, user, pw, pw2):
    if con_clicks is None:
        raise PreventUpdate

    if dis_time is None:
        dis_time = 0

    if dis_time > con_time:
        return ['Disconnected', 'danger']

    if str(pw) != str(pw2):
        return ['ERROR', 'warning']

    conn_params = sdvf.connect_to_db(server, db, user, pw)
    print(conn_params)
    if conn_params[1] == 'success':
        return ['Connected', 'success']
    else:
        return ['ERROR', 'warning']


if __name__ == '__main__':
    app.run_server(debug=True,)
