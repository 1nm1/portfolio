toast_param_color = '#73a8ff'

buttongroup_color = '#4a4a4a'

buttongroup_button_color = '#445669'

input_ticker_style = {'width':'200px', 'margin-right':'20px','font-size':'18px'}

button_search_style = {'width':'120px','font-size':'18px','margin-right':'40px'}

text_system_message_style = {'position': 'absolute', 'right': '20px', 'top': '10px', 'font-size':'12px','color':'#454545','width':'auto'}

tabs_style = {'margin':'10px', 'margin-bottom':'20px'}

tab_style = {}

toast_company_info_style_1 = {'width':'90%','min-width':'90%','font-size':'20px', 'margin':'10px'}

toast_company_info_style_2 = {'width':'800px', 'min-width':'800px','font-size':'20px', 'margin-left':'10px','display': 'inline-block', 'vertical-align':'top'}

toast_cell_large_style_1 = {'font-size':'20px', 'text-align':'right'}

toast_cell_large_style_2 = {'font-size':'20px', 'text-align':'left', 'color':toast_param_color}

toast_cell_small_style_1 = {'font-size':'16px', 'text-align':'left'}

toast_cell_small_style_2 = {'font-size':'16px', 'text-align':'left', 'color':toast_param_color, }

toast_col_label_style_1 = {'max-width':'100px'}

toast_col_label_style_2 = {'max-width':'140px', 'width':'140px'}

toast_col_param_style_1 = {'padding-left':'0px'}

graph_style_1 = {'width':'90%','min-width':'80%','margin-left':'auto','margin-right':'auto', 'margin-top':'20px', 'color':'blue'}

graph_style_2 = {'min-width':'45%','margin-left':'2.5%', 'margin-right':'2.5%', 'margin-top':'20px','display': 'inline-block'}

dash_table_style_1 ={'marginLeft': 'auto', 'marginRight': 'auto', 'max-width':'650px'}

dash_table_header_style_1 = {'backgroundColor': '#292929','fontWeight': 'bold','textAlign': 'center','font-family':'arial','font-size':'14px'}

dash_table_cell_style_1 = {'padding': '5px','backgroundColor': '#4d4d4d','fontWeight': 'bold','textAlign': 'center','font-family':'arial','font-size':'12px'}

dash_table_condform_1 = [
        {'if': {
                'filter_query': '{Action} = "up"',
                'column_id': 'Action'
            },
            'backgroundColor': 'green',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{Action} = "down"',
                'column_id': 'Action'
            },
            'backgroundColor': '#854545',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{Action} = "main"',
                'column_id': 'Action'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{Action} = "init"',
                'column_id': 'Action'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{Action} = "reit"',
                'column_id': 'Action'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "In-Line"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Sector Perform"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Neutral"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Hold"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Peer Perform"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Perform"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Equal-Weight"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Market Perform"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#484585',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Underweight"',
                'column_id': 'To Grade'
            },
            'backgroundColor': 'green',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Outperform"',
                'column_id': 'To Grade'
            },
            'backgroundColor': 'green',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Market Outperform"',
                'column_id': 'To Grade'
            },
            'backgroundColor': 'green',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Buy"',
                'column_id': 'To Grade'
            },
            'backgroundColor': 'green',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Overweight"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#854545',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Negative"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#854545',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Underperform"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#854545',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Sell"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#854545',
            'color': 'white'
        },
        {'if': {
                'filter_query': '{To Grade} = "Sector Underperform"',
                'column_id': 'To Grade'
            },
            'backgroundColor': '#854545',
            'color': 'white'
        },
        
        ]

buttongroup_button_style_1 = {'margin':'20px 20px 0px 30px','width':'280px','font-size':'24px','background-color':buttongroup_button_color}

buttongroup_style_1 = {'width':'320px', 'height':'300px','display':'grid'}

jumbotron_style_1 = {'padding':'20px 20px 10px 20px', 'margin':'0px 0px 10px 0px'}

image_style_1 = {'position':'absolute','left': '30px', 'bottom': '10px', 'width':'225px'}

nav_bar_style_1={'height': '70px', 'margin':'10px'}

sidebar_style_1={
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "300px",
    "padding": "2rem 1rem",
    "background-color": "#212121",}

content_style_1 = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "1rem 1rem",}

