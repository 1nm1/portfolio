import sqlalchemy as sa


def connect_to_db(server='localhost',
                  database='data_viz_demo',
                  user='data_viz_user',
                  password='data_viz_pw_1!'):
    if server is None:
        server='localhost'
        database='data_viz_demo'
        user='data_viz_user'
        password='data_viz_pw_1!'

    db_string = f"postgres://{user}:{password}@{server}:5432/{database}"
    print(f"\t[MSG] Connecting to DB\n\t{db_string}")

    table_q = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
    try:
        engine = sa.create_engine(db_string)
        tables = engine.execute(table_q).fetchall()
        available_tables = [table[0] for table in tables]
        return [available_tables, 'success', None]

    except Exception as ex:
        print(ex.args)
        return [None, 'failure', ex.args]

