import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def insert_record(cur: object, df: object, insert_query: str, fields: list):
    """Insert object data records in database.

    Args:
        cur: Cursor of database`s connect.
        df: dataframe in question
        insert_query: query that insert data in specific table.
        fields: main columns added to the table

    Returns:
        None
    """
    record = df[fields].values[0].tolist()
    cur.execute(insert_query, record)


def insert_dataframe(cur: object, df: object, insert_query: str):
    """Insert object data of dataframe in database.

    Args:
        cur: Cursor of database`s connect.
        df: dataframe in question
        insert_query: query that insert data in specific table.
    Returns:
        None
    """
    for i, row in df.iterrows():
        cur.execute(insert_query, list(row))


def process_song_file(cur, filepath):
    """This process performs a reading of the data in a specific path and performs the
    insertions of data in the user and artist tables.

    Args:
        cur: Cursor of database`s connect.
        filepath: the specific path to read of data

    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    insert_record(
        cur,
        df,
        song_table_insert,
        ["song_id", "title", "artist_id", "year", "duration"],
    )

    # insert artist record
    insert_record(
        cur,
        df,
        artist_table_insert,
        [
            "artist_id",
            "artist_name",
            "artist_location",
            "artist_latitude",
            "artist_longitude",
        ],
    )


def process_log_file(cur, filepath):
    """This process performs a reading of the data in a specific path and performs the
    insertions of data in the time, user and songplay tables.

    Args:
        cur: Cursor of database`s connect.
        filepath: the specific path to read of data

    Returns:
        None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df["ts"], unit="ms")

    # insert time data records
    time_data = (
        df["ts"],
        t.dt.hour,
        t.dt.day,
        t.dt.isocalendar().week,
        t.dt.month,
        t.dt.year,
        t.dt.weekday,
    )
    column_labels = ("start_time", "hour", "day", "week", "month", "year", "weekday")
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))

    insert_dataframe(
        cur,
        time_df,
        time_table_insert,
    )

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    insert_dataframe(
        cur,
        user_df,
        user_table_insert,
    )

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            row.ts,
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent,
        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Get all files matching extension from directory,
    get total number of files found,
    iterate over files and process.

    Args:
        cur: Cursor of database`s connect.
        conn: conector of database`s connect
        filepath: the specific path to read of data
        func: function that will extract, transform and load the data into the database.

    Returns:
        None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print("{} files found in {}".format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print("{}/{} files processed.".format(i, num_files))


def main():
    """Connection through lib psycopg2, run process data to process_song_file 
    and run process data to process_log_file.

    Returns:
        None
    """
    try:
        conn = psycopg2.connect(
            "host=127.0.0.1 dbname=sparkifydb user=student password=student"
        )
        cur = conn.cursor()

        process_data(cur, conn, filepath="data/song_data", func=process_song_file)
        process_data(cur, conn, filepath="data/log_data", func=process_log_file)

        conn.close()
    except ValueError as error:
        print(error)
        conn.close()


if __name__ == "__main__":
    main()
