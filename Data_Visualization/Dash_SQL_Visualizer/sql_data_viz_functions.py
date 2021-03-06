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
    db_string = f"postgres://{user}:{password}@{server}:5432/{database}"
    print(f"\t[MSG] Connecting to DB\n\t{db_string}")

    engine = sa.create_engine(db_string)
    engine.execute('SELECT 1')
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
    try:
        connect_to_db(server, database, user, password)

    except Exception as ex:
        print("\t[ERR] DB Connection Failed")
        print(f"\t{ex.args}")
        return [None, 'failure', ex.args]

    table_q = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
    try:
        print(f"\t[MSG] Extracting tables from {database}")
        tables = engine.execute(table_q).fetchall()
        available_tables = [table[0] for table in tables]
        print("\t[MSG] Table Extraction Successful")
        return [available_tables, 'success', None]

    except Exception as ex:
        print("\t[ERR] Table Extraction Failed")
        print(f"\t{ex.args}")
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
        print(f"\t[MSG] Querying columns from {table}")
        columns = engine.execute(col_q, x=table).fetchall()
        available_cols = [col[0] for col in columns]
        print("\t[MSG] Column Query Successful")
        return [available_cols, 'success', None]

    except Exception as ex:
        print("\t[ERR] Column Query Failed")
        print(f"\t{ex.args}")
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
        print(f"\t[MSG] Querying data from '{table}.{column}'")
        data = pd.read_sql(
                table,
                engine,
                columns=[column])
        print("\t[MSG] Data Query Successful")
        return [data, 'success', None]

    except Exception as ex:
        print("\t[ERR] Data Query Failed")
        print(f"\t{ex.args}")
        return [None, 'failure', ex.args]
