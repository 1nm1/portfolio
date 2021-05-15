# region Import Libraries
from fastquant import get_crypto_data
from fastquant import backtest
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import sys
import general_script_functions as gsf
# endregion


def data_api(pair, start_date, end_date, time_resolution):
    '''
    Summary:
    ----------
    Retrieves crypto data via Binance API

    Params:
    ----------
    pair : str
        crypto pair to retrieve (i.e. BTC/USDT)
    start_date : str
        starting date in dataset (YYYY-MM-DD)
    end_date : str
        ending date in dataset (YYYY-MM-DD)
    time_resolution : str
        resolution in data set (1h, 1d, 1w)

    Outputs:
    ----------
    crypto : dataframe
        financial data in OHLCV form
    '''
    crypto = get_crypto_data(
        pair,
        start_date,
        end_date,
        time_resolution=time_resolution)

    return crypto


@gsf.func_perform_time
def fetch_data(pair, start_date, end_date, time_resolution):
    '''
    Summary:
    ----------
    Manages the data retrievel from Binance API.
    Due to API limitation, this function continues to collect data
    if the required dataset is larger than 500 data points (does this by
    checking if end date equals the requested end date)

    Params:
    ----------
    pair : str
        crypto pair to retrieve (i.e. BTC/USDT)
    start_date : str
        starting date in dataset (YYYY-MM-DD)
    end_date : str
        ending date in dataset (YYYY-MM-DD)
    time_resolution : str
        resolution in data set (1h, 1d, 1w)

    Outputs:
    ----------
    crypto : dataframe
        financial data in OHLCV form
    '''
    print("\n=== Fetching Data ===")
    print(f"""\tAsset / Pair: {pair}\n\tStart Date:
         {start_date}\n\tEnd Date: {end_date}\n\t
         Resolution: {time_resolution}""")

    # Retrieve initial set of data
    df_main = data_api(pair, start_date, end_date, time_resolution)

    # Check if end date matches requested end date
    end_date_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
    df_end_date = df_main.iloc[[-1]].index.date[0]

    # If dates don't match, collect additional data
    if end_date_date != df_end_date:
        data_trigger = True
        while data_trigger is True:
            df = data_api(
                pair,
                df_end_date.strftime('%Y-%m-%d'),
                end_date,
                time_resolution)
            df_end_date = df.iloc[[-1]].index.date[0]
            df_main = pd.concat([df_main, df])
            print(f"""\tCurrent date captured: {df_end_date}
                 | There are {(end_date_date-df_end_date).days}
                  days remaining""")
            if int((end_date_date-df_end_date).days) < 1:
                data_trigger = False

    print("\n=== Data Successfully Retrieved ===")

    return df_main


@gsf.func_perform_time
def df_trans_calcs(df):
    '''
    Summary:
    ----------
    Performs transformations and calculations on dataframe

    Params:
    ----------
    df : pandas dataframe
        financial data in OHLCV format

    Outputs:
    ----------
    df : pandas dataframe
        resulting dataframe after transformations and calculations
    '''
    periods = 10
    df['close pert change'] = df['close'].pct_change(periods=periods) * 100
    df['close delta'] = df['close'].diff(periods=periods)
    df['vol pert change'] = df['volume'].pct_change(periods=periods) * 100
    df['vol delta'] = df['volume'].diff(periods=periods)
    df['close pert change ewm'] = df['close pert change'].ewm(span=20).mean()
    df['vol pert change ewm'] = df['vol pert change'].ewm(span=20).mean()
    return df


@gsf.func_perform_time
def plot_data(df, pair, start_date, end_date, time_resolution):
    '''
    Summary:
    ----------
    Plots data

    Params:
    ----------
    df : dataframe
        financial data in OHLCV form
    pair : str
        crypto pair to retrieve (i.e. BTC/USDT)
    start_date : str
        starting date in dataset (YYYY-MM-DD)
    end_date : str
        ending date in dataset (YYYY-MM-DD)
    time_resolution : str
        resolution in data set (1h, 1d, 1w)

    Outputs:
    ----------
    none
    '''
    # Create figure object
    fig = make_subplots(
            rows=1,
            cols=2,
            specs=[[{"secondary_y": True}, {"secondary_y": True}]])

    # Create dictionary with figure params
    fig_dict = {
        'fig1':
            {
                'name': 'Volume', 'x': df.index, 'y': df['volume'],
                'mode': 'lines', 'opacity': 0.75,
                'line': dict(color='darkgreen', width=1),
                'secondary_y': True, 'row': 1, 'col': 1
            },
        'fig2':
            {
                'name': 'Close', 'x': df.index, 'y': df['close'],
                'mode': 'lines', 'opacity': 1.0,
                'line': dict(color='darkblue', width=2),
                'secondary_y': False, 'row': 1, 'col': 1
            },
        'fig3':
            {
                'name': 'Volume % Change EWM', 'x': df.index,
                'y': df['vol pert change ewm'], 'mode': 'lines',
                'opacity': 0.75, 'line': dict(color='darkgreen', width=1),
                'secondary_y': True, 'row': 1, 'col': 2
            },
        'fig4':
            {
                'name': 'Close % Change EWM', 'x': df.index,
                'y': df['close pert change ewm'], 'mode': 'lines',
                'opacity': 1.0, 'line': dict(color='darkblue', width=2),
                'secondary_y': False, 'row': 1, 'col': 2
            },
        }

    # Create figures for each figure in fig_dict
    for fig_ in fig_dict:
        figure = fig_dict[fig_]
        fig.add_trace(
            go.Scattergl(
                name=figure['name'],
                x=figure['x'],
                y=figure['y'],
                mode=figure['mode'],
                opacity=figure['opacity'],
                line=figure['line']
                ),
            secondary_y=figure['secondary_y'],
            row=figure['row'],
            col=figure['col']
            )

    fig.update_layout(title_text=f"""{pair}, {time_resolution}
          |  {start_date} --> {end_date}""")
    fig.show()


@gsf.func_perform_time
def backtest_data_gdsr(df):
    '''
    Summary:
    ----------
    Open json trading strategy file, test strategies through fastquant backtest

    Params:
    ----------
    df : dataframe with financial data

    Outputs:
    ----------
    none
    '''

    json_file_path = os.path.join(sys.path[0], 'bt_strats_params.json')

    with open(json_file_path, encoding='utf-8', errors='ignore') as json_data:
        strat_dict = json.load(json_data, strict=False)

    for strat in strat_dict['strats']:
        bt = backtest(
            "multi",
            df,
            strats=strat,
            plot=True)
        print(bt)


if __name__ == "__main__":
    gsf.clear_terminal()

    # User Inputs
    pair = "ETH/USDT"
    start_date = "2021-03-10"
    end_date = "2021-05-15"
    time_resolution = "15m"  # 15m 30m 1h 1d 1w

    # Retrieve financial data
    df = fetch_data(pair, start_date, end_date, time_resolution)

    # Performs additional transformations
    df = df_trans_calcs(df)

    # Plot data
    plot_data(df, pair, start_date, end_date, time_resolution)

    # Test trading strategies
    test_strat = False
    if test_strat is True:
        backtest_data_gdsr(df)
