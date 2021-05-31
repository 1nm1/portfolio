import sqlalchemy as sa
from sqlalchemy.sql import text


def connect_to_db(server, database, user, password):
    global engine
    if (server is None) or (server == ""):
        server = 'localhost'
        database = 'data_viz_demo'
        user = 'data_viz_user'
        password = 'data_viz_pw_1!'

    db_string = f"postgres://{user}:{password}@{server}:5432/{database}"
    print(f"\t[MSG] Connecting to DB\n\t{db_string}")

    engine = sa.create_engine(db_string)


def extract_tables(server, database, user, password):
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


def extract_columns(table):
    col_q = text("""
            SELECT *
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
