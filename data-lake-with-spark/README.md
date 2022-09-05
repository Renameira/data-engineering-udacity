# Project: Data Lake with Spark

## Introduction
Introduction
A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. This will allow their analytics team to continue finding insights in what songs their users are listening to.

You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## How to run scripts
<br>

First of all, initialize a virtual environment with project dependency, using the script bellow.
Then set the `.env` in config file (if you have some problem, there is `.env.example` for support):

``` bash 
cd data-modeling-with-postgres
make install && source venv/bin/activate
```

In order to start extracting data from source data and inserting the data into the target data, run this python script.
``` bash
python3 src/etl.py
```

## Python File

### etl.py

The way we perform an etl is generally the same (extract, transform and load), the big tip of the project is represented in the use of Spark, using the pyspark library, in order to, in addition to extracting and loading, use the main concepts of the tool , that is, map, shuffle and reduce. With this we conclude that for large volume of data we need robust tools like spark to manage data processing.

about the script:

**process_song_data**:

1. extract data from a bucket(S3) that has the sound information;
2. we extracted some columns to enrich the information of the sounds;
3. we write the sound data in the destination bucket in a specific folder for the subject;
4. we extracted some columns to enrich the information of the artists;
5. we write the artist data in the destination bucket in a specific folder for the subject;

**process_song_data**
1. we extract some columns to enrich user's information;
2. we write the user data in the destination bucket in a specific folder for the subject;
3. we extract some columns to enrich the weather information;
4. we write the time data in the destination bucket in a specific folder for the subject;
5. we extracted some columns to enrich the songsplays information;
6. we write the songplay data in the destination bucket in a specific folder for the subject;


## Project Structure

``` tree
data-lake-with-spark
├── Makefile
├── README.md
├── config
│	└── .env.example
├── docker
│	└── docker-compose.yml
├── requirements.txt
└── src
	└──etl.py
```
