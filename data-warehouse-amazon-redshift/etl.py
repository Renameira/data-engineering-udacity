from config import Settings
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("logs/debug-etl.log"), logging.StreamHandler()],
)


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        logging.info(f"{query}")
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        logging.info(f"{query}")
        cur.execute(query)
        conn.commit()


def main():
    logging.info(f"Process inicialized")
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

    logging.info(f"ETL finished")


if __name__ == "__main__":
    main()
