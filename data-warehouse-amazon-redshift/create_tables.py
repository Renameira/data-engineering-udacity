from config import Settings
import psycopg2
from sql_queries import create_table_queries, drop_table_queries
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/debug-create-table.log"),
        logging.StreamHandler(),
    ],
)


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        logging.info(f"{query}")
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        logging.info(f"{query}")
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

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()
    logging.info(f"tables created")


if __name__ == "__main__":
    main()
