import sqlalchemy as sa
from sqlalchemy.sql import text
import pandas as pd


def connect_to_db(server, database, user, password):
    # region Function notes
    '''Summary:
    ----------
    Establishes the connection to the database

    Params:
    ----------
    server : str
        server address (i.e. 'localhost' or similar)
    database : str
        name of database
    user : str
        name of user
    password : str
        user password

    Outputs:
    ----------
    NA - declares create_engine variable, engine, globally'''
    # endregion
    global engine
    if (server is None) or (server == ""):
        server = 'localhost'
        database = 'data_viz_demo'
        user = 'data_viz_user'
        password = 'data_viz_pw_1!'

    db_string = f"postgres://{user}:{password}@{server}:5432/{database}"
    print(f"\t[MSG] Connecting to DB\n\t{db_string}")

    engine = sa.create_engine(db_string)
    print("\t[MSG] Connection Established")


def extract_tables(server, database, user, password):
    # region Function Notes
    '''Summary:
    ----------
    Extracts the list of tables on the provided database.

    Params:
    ----------
    server : str
        server address (i.e. 'localhost' or similar)
    database : str
        name of database
    user : str
        name of user
    password : str
        user password

    Outputs:
    ----------
    list
        available_tables : str
            list of tables available on the database
        success_or_failure : str
            str indicating success or failure of extraction
        ex.args : str
            error arguments if any'''
    # endregion
    connect_to_db(server, database, user, password)

    table_q = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
    try:
        tables = engine.execute(table_q).fetchall()
        available_tables = [table[0] for table in tables]
        return [available_tables, 'success', None]

    except Exception as ex:
        print(ex.args)
        return [None, 'failure', ex.args]


def extract_columns(table,  server, database, user, pw):
    # region Function Notes
    '''Summary:
    ----------
    Extracts the columns on the provided table\n
    Will re-establish database connection if lost

    Params:
    ----------
    table : str
        name of table
    server : str
        server address (i.e. 'localhost' or similar)
    database : str
        name of database
    user : str
        name of user
    password : str
        user password

    Outputs:
    ----------
    list
        available_cols : str
            list of columns available on the table
        success_or_failure : str
            str indicating success or failure of extraction
        ex.args : str
            error arguments if any'''
    # endregion
    if (engine is None):
        connect_to_db(server, database, user, pw)

    col_q = text("""
            SELECT column_name
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = :x;
            """)
    try:
        columns = engine.execute(col_q, x=table).fetchall()
        available_cols = [col[0] for col in columns]
        return [available_cols, 'success', None]

    except Exception as ex:
        print(ex.args)
        return [None, 'failure', ex.args]


def extract_data(column, table, server, database, user, pw):
    # region Function Notes
    '''Summary:
    ----------
    Extracts the data from the provided column and table\n
    Will re-establish database connection if lost

    Params:
    ----------
    column : str
        name of column
    table : str
        name of table
    server : str
        server address (i.e. 'localhost' or similar)
    database : str
        name of database
    user : str
        name of user
    password : str
        user password

    Outputs:
    ----------
    list
        data : dataframe
            dataframe of data from column & table
        success_or_failure : str
            str indicating success or failure of extraction
        ex.args : str
            error arguments if any'''
    # endregion
    if (engine is None):
        connect_to_db(server, database, user, pw)

    try:
        data = pd.read_sql(
                table,
                engine,
                columns=[column])

        return [data, 'success', None]

    except Exception as ex:
        print(ex.args)
        return [None, 'failure', ex.args]
