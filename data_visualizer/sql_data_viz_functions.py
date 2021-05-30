import sqlalchemy as sa


def connect_to_db(server, database, user, password):
    from sqlalchemy import create_engine

    db_string = f"postgres://{user}:{password}@{server}:15813/{database}"

    engine = sa.create_engine(db_string)

    return engine
