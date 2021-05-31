
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.io as pio
import sql_data_viz_functions as dvfu
import sql_data_viz_formats as dvfo
import warnings
warnings.simplefilter("ignore")

pio.templates.default = "plotly_dark"

app = dash.Dash(
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True)

content = html.Div(id="page-content", style=dvfo.content_style_1)

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
            style=dvfo.sidebar_style_1,
        )

nav_bar = html.Div([
            dbc.Navbar([
                html.H5(
                    "Table: ",
                    style=dvfo.label_navbar_style_1),
                dcc.Dropdown(
                    id='dropdown-table',
                    options=[
                        {'label': '', 'value': ''}
                    ],
                    value='',
                    style=dvfo.dropdown_navbar_style_1
                    ),
                html.H5(
                    "Column: ",
                    style=dvfo.label_navbar_style_2),
                dcc.Dropdown(
                    id='dropdown-column',
                    optionHeight=30,
                    options=[
                        {'label': '', 'value': ''},
                    ],
                    value='',
                    style=dvfo.dropdown_navbar_style_1
                    ),
                dbc.Alert(
                    "Not Connected",
                    id='alert-db-connect',
                    color="danger",
                    style=dvfo.alert_settings_style_1)],
                style=dvfo.nav_bar_style_visible,
                color='dark'),
                ],
            id="navbar-table-col")

dv_page = html.Div([
            dbc.Spinner(
                html.Div([
                    dcc.Graph(id="graph-scatter"),
                    dcc.Graph(id="graph-histogram")
                ])
            )
    ])

st_page = html.Div([
            dbc.Form([
                dbc.FormGroup([
                    dbc.Label(
                        "Server",
                        html_for="input-server",
                        style=dvfo.formgroup_settings_label_style_1),
                    dbc.Input(
                        type="text",
                        id="input-server",
                        placeholder="Enter server location",
                        persistence=True,
                        persistence_type='session',
                        style=dvfo.formgroup_settings_input_style_1),
                    ],
                    row=True),
                dbc.FormGroup([
                    dbc.Label(
                        "Database",
                        html_for="input-db",
                        style=dvfo.formgroup_settings_label_style_1),
                    dbc.Input(
                        type="text",
                        id="input-db",
                        persistence=True,
                        persistence_type='session',
                        placeholder="Enter database",
                        style=dvfo.formgroup_settings_input_style_1),
                    ],
                    row=True),
                dbc.FormGroup([
                    dbc.Label(
                        "Database User",
                        html_for="input-user",
                        style=dvfo.formgroup_settings_label_style_1),
                    dbc.Input(
                        type="text",
                        id="input-user",
                        persistence=True,
                        persistence_type='session',
                        placeholder="Enter database user",
                        style=dvfo.formgroup_settings_input_style_1),
                    ],
                    row=True),
                dbc.FormGroup([
                    dbc.Label(
                        "User Password",
                        html_for="input-userpw",
                        style=dvfo.formgroup_settings_label_style_1),
                    dbc.Input(
                        type="password",
                        id="input-userpw",
                        persistence=True,
                        persistence_type='session',
                        placeholder="Enter user password",
                        style=dvfo.formgroup_settings_input_style_1),
                    ],
                    row=True),
                dbc.FormGroup([
                    dbc.Label(
                        "Reenter Password",
                        html_for="input-userpw2",
                        style=dvfo.formgroup_settings_label_style_1),
                    dbc.Input(
                        type="password",
                        id="input-userpw2",
                        persistence=True,
                        persistence_type='session',
                        placeholder="Reenter password",
                        style=dvfo.formgroup_settings_input_style_1),
                    ],
                    row=True),
                ],
                style=dvfo.formgroup_settings_style_1),
            html.Div([
                dbc.Button(
                    "Clear form",
                    id='button-st-clear',
                    color="secondary",
                    style=dvfo.button_settings_clear_form_style_1),
                dbc.Button(
                    "Disconnect",
                    id='button-db-disconnect',
                    color="secondary",
                    style=dvfo.button_settings_disconnect_style_1),
                dbc.Button(
                    "Connect",
                    id='button-db-connect',
                    color="primary",
                    style=dvfo.button_settings_connect_style_1),
                dbc.Alert(
                    "Not Connected",
                    id='alert-db-connect-st',
                    color="danger",
                    style=dvfo.alert_settings_style_1),
                ])
            ])

el_page = html.Div([
    html.H5("Application Event Log"),
    dcc.Textarea(
        id='textarea-event-log',)
    ])

app.layout = html.Div([
                nav_bar,
                dcc.Location(id="url"),
                dcc.Store(
                    id="db-info"),
                sidebar,
                content])


@app.callback(
    [Output("page-content", "children"),
     Output("navbar-table-col", "style")],
    [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return [dv_page, dvfo.nav_bar_style_visible]
    if pathname == "/dv":
        return [dv_page, dvfo.nav_bar_style_visible]
    elif pathname == "/st":
        return [st_page, dvfo.nav_bar_style_hidden]
    elif pathname == "/el":
        return [el_page, dvfo.nav_bar_style_hidden]
    return [dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ]), dvfo.nav_bar_style_hidden]


@app.callback(
    [Output("alert-db-connect", "children"),
     Output("alert-db-connect", "color"),
     Output("alert-db-connect-st", "children"),
     Output("alert-db-connect-st", "color"),
     Output("dropdown-table", "options"),
     Output("db-info", "data")],
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

    no_options = [{'label': '', 'value': ''}]
    if dis_time > con_time:
        return ['Disconnected', 'danger',
                'Disconnected', 'danger',
                no_options, None]

    if str(pw) != str(pw2):
        return ['ERROR', 'warning', 'ERROR', 'warning', no_options, None]

    conn_params = dvfu.extract_tables(server, db, user, pw)

    if conn_params[1] == 'success':
        options = [{'label': i, 'value': i} for i in conn_params[0]]
        data_db_info = {
            "server": server,
            "db": db,
            "user": user,
            "pw": pw
        }
        return ['Connected', 'success',
                'Connected', 'success',
                options, data_db_info]
    else:
        return ['ERROR', 'warning', 'ERROR', 'warning', no_options, None]


@app.callback(
    [Output("dropdown-column", "options")],
    [Input("dropdown-table", "value")],
    State("db-info", "data"))
def retrieve_columns(table, db_info):
    if (table is None) or (table == ""):
        raise PreventUpdate

    columns = dvfu.extract_columns(
                                table,
                                db_info['server'],
                                db_info['db'],
                                db_info['user'],
                                db_info['pw'])
    options = [{'label': i, 'value': i} for i in columns[0]]
    return [options]


@app.callback(
    [Output("graph-scatter", "figure"),
     Output("graph-histogram", "figure")],
    [Input("dropdown-column", "value"),
     Input("dropdown-table", "value")],
    State("db-info", "data"))
def retrieve_data(column, table, db_info):
    if (table is None):
        raise PreventUpdate

    if (column is None) or (column == ""):
        raise PreventUpdate

    data = dvfu.extract_data(
                            column,
                            table,
                            db_info['server'],
                            db_info['db'],
                            db_info['user'],
                            db_info['pw'])[0]
    if data is None:
        raise PreventUpdate

    fig1 = go.Figure(go.Scattergl(
            x=data.index,
            y=data[column],
            mode="markers"
        ))

    fig2 = go.Figure(data=[go.Histogram(
        x=data[column])
        ],)

    return [fig1, fig2]


if __name__ == '__main__':
    app.run_server(debug=True,)
