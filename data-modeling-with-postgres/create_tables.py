import psycopg2
from sql_queries import create_table_queries, drop_table_queries
from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData
import configparser
import os

config = configparser.ConfigParser()

current_dir = os.path.abspath(".")

full_path = os.path.join(current_dir, "config/.env")

config.read(full_path, encoding="utf-8")

CONNECTION_SPARKIFYDB = config["DB"]["CONNECTION_SPARKIFYDB"]
CONNECTION_STUDENTDB = config["DB"]["CONNECTION_STUDENTDB"]
CONNECTION_STRING_SPARKIFYDB = config["DB"]["CONNECTION_STRING_SPARKIFYDB"]


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """

    # connect to default database
    conn = psycopg2.connect(CONNECTION_STUDENTDB)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect(CONNECTION_SPARKIFYDB)
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def generator_erd():
    """
    Generate the ER diagram using sqlalchemy_schemadisplay.

    Returns: The png image with the database schema in assets file.
    """
    graph = create_schema_graph(metadata=MetaData(CONNECTION_STRING_SPARKIFYDB))
    return graph.write_png("./assets/sparkifydb_erd.png")


def main():
    """
    - Drops (if exists) and Creates the sparkify database.

    - Establishes connection with the sparkify database and gets
    cursor to it.

    - Drops all the tables.

    - Creates all tables needed.

    - Finally, closes the connection.
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)
    generator_erd()

    conn.close()


if __name__ == "__main__":
    main()
