'''
DAG Information
This DAG extracts Geomagnetic Storm data from NASA using the following API

https://api.nasa.gov/DONKI/GST

More information on it can be found here:
https://ccmc.gsfc.nasa.gov/tools/DONKI/

The data comes as a nested json which is exploded and inserted into a local postgres database

author: Nathan Meek, 2022
'''

from airflow import DAG
from airflow.models import Variable
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
#  from airflow.providers.postgres.hooks.postgres import PostgresHook

from datetime import datetime
from datetime import timedelta
import json
import psycopg2
import pandas as pd
from pandas import json_normalize
from psycopg2.extras import execute_values

# region User Inputs
DAG_ID = 'nasa_donki_data'
date2 = datetime.today().strftime('%Y-%m-%d')
date1 = (datetime.today() - timedelta(days=120)).strftime('%Y-%m-%d')
api_key = 'cTTebdwioe2NbYZnkIqW9326h8HkjiLMS5gIRwW3'
# endregion

# region User Defined Functions


def build_pg_conn():
    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user=Variable.get("local_postgres_user"),
        password=Variable.get("local_postgres_pw"))
    return conn


def insert_to_pg(conn, df, table):
    # Mapping columns to database columns
    df = df.rename(columns={
        "gstID": "GSTID",
        "startTime": "StartTime",
        "observedTime": "KpObservedTime",
        "kpIndex": "KpIndex",
        "source": "KpSource",
        "activityID": "LinkedEventsActivityId",
        "link": "Link",
    })

    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))

    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()

    try:
        execute_values(cursor, query, tuples)
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"[!! ERROR !!]: {error}")
        conn.rollback()
        cursor.close()
        raise ValueError(f"[!! ERROR !!]: {error}")

    print("the dataframe is inserted")
    cursor.close()


def _process_data(ti):
    def open_nested_rows(df, cols):
        # This function explodes nested json so it will come into the database as individual rows
        for col in cols:
            df = df.explode(col).reset_index(drop=True)
            df = df.merge(pd.json_normalize(
                df[col]), left_index=True, right_index=True).drop(col, axis=1)
        return df

    print('[!USER!] Starting Process Data')
    donki_data = ti.xcom_pull(task_ids='extract_data')
    if donki_data:

        data = json.loads(donki_data)
        df = json_normalize(data)
        df = open_nested_rows(df, ['allKpIndex', 'linkedEvents'])

        # Can also save locally to worker as well
        # df.to_csv('/tmp/donki/processed_data.csv', index=None, header=False)

        return df.to_json(orient='records')
    else:
        print('[!USER!] No data returned')
        return None


def _store_data(ti):
    # Another way to load this data would be to do a COPY command on a csv file
    # using the PostgresHook

    donki_data = ti.xcom_pull(task_ids='process_data')

    if donki_data:
        data = pd.read_json(donki_data)
        conn = build_pg_conn()
        insert_to_pg(conn, data, "geomagnetic_storm")
# endregion


with DAG(
    DAG_ID,
    start_date=datetime(2022, 7, 9),
    schedule_interval='@daily',
        catchup=False) as dag:

    create_pg_table = PostgresOperator(
        task_id='create_pg_table',
        postgres_conn_id='postgres_local',
        sql='''
            CREATE TABLE IF NOT EXISTS geomagnetic_storm (
                GSTID TEXT NOT NULL,
                StartTime TIMESTAMP,
                KpObservedTime TIMESTAMP,
                KpIndex INT, 
                KpSource TEXT,
                LinkedEventsActivityId TEXT,
                Link TEXT NOT NULL
            );
        ''')

    # region Defined Operators / Tasks
    extract_data = SimpleHttpOperator(
        task_id='extract_data',
        http_conn_id='nasa_donki_api',
        endpoint=f'?startDate={date1}&endDate={date2}&api_key={api_key}',
        method='GET',
        log_response=True
    )

    process_data = PythonOperator(
        task_id='process_data',
        python_callable=_process_data
    )

    store_data = PythonOperator(
        task_id='store_data',
        python_callable=_store_data
    )

    # endregion

    # Dependencies
    create_pg_table >> extract_data >> process_data >> store_data
