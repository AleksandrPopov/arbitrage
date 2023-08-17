import sqlite3 as db


def set_pair(table: str, pair_list: list):
    with db.connect('db.db') as database:
        cursor = database.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS  {table} (couples TEXT UNIQUE)")
        cursor.executemany(f"INSERT INTO {table} VALUES (?) ON CONFLICT DO NOTHING", zip(pair_list))
        database.commit()


def get_pair(table: str):
    with db.connect('db.db') as database:
        cursor = database.cursor()
        couples = []
        for item in cursor.execute(f"SELECT * FROM {table}").fetchall():
            couples.append(item[0])
        return couples
