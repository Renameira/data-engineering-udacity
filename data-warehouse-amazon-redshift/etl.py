from config import Settings
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            Settings.HOST,
            Settings.DB_NAME,
            Settings.DB_USER,
            Settings.DB_PASSWORD,
            Settings.DB_PORT,
        )
    )
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
