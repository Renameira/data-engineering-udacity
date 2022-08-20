from config import Settings
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
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

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
