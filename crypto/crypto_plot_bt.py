from fastquant import get_crypto_data
from fastquant import backtest
import pandas as pd
import datetime as dt
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import sys

def data_api(pair, start_date,end_date, time_resolution):
    crypto = get_crypto_data(
        pair,
        start_date,
        end_date,
        time_resolution=time_resolution)
    crypto['price change'] = crypto['close'] - crypto['open']
    
    return crypto


def fetch_data(pair, start_date,end_date, time_resolution):
    start = time.time()
    print("\n=== Fetching Data ===")
    print(f"\tAsset / Pair: {pair}\n\tStart Date: {start_date}\n\tEnd Date: {end_date}\n\tResolution: {time_resolution}")

    df_main = data_api(pair, start_date,end_date, time_resolution)

    end_date_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
    df_end_date = df_main.iloc[[-1]].index.date[0]
        
    if end_date_date != df_end_date:
        data_trigger = True
        while data_trigger == True:        
            df = data_api(
                pair, 
                df_end_date.strftime('%Y-%m-%d'),
                end_date, 
                time_resolution)
            df_end_date = df.iloc[[-1]].index.date[0]
            df_main = pd.concat([df_main, df])
            print(f"\tCurrent date captured: {df_end_date} | There are {(end_date_date-df_end_date).days} days remaining")
            if int((end_date_date-df_end_date).days) < 1:
                data_trigger = False

    end = time.time()
    print(f"\n=== Data Successfully Retrieved ===\nData Extraction Time: {round(end-start,2)}s")
    
    return df_main


def plot_data(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scattergl(
            name="Volume",
            x = df.index,
            y = df['volume'],
            mode='lines',
            opacity=0.5,
            line=dict(color='grey', width=1)
            ),
            secondary_y=True,
        )

    fig.add_trace(
        go.Scattergl(
            name="Close",
            x = df.index,
            y = df['close'],
            mode='lines+markers',
            opacity=1.0,
            line=dict(color='darkblue', width=2),
            marker=dict(
                size=6,
                )
            ),
            secondary_y=False,
        )

    fig.show()


def backtest_data_gdsr(df):
    '''
    Open json trading strategy file, test strategies

    Params:
    df : dataframe will financial data

    Outputs:
    None, prints to terminal
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
    # User Inputs
    pair = "LSK/USDT"
    start_date = "2021-03-10"
    end_date = "2021-05-14"
    time_resolution = "15m" #15m 30m 1h 1d 1w
    df = fetch_data(pair, start_date, end_date, time_resolution)
    plot_data(df)
    
    test_strat = True
    if test_strat == True:
        backtest_data_gdsr(df)
        
    
    