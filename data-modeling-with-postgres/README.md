# Project: Data Modeling with Postgres


<img src="./assets/postgresql-tutorial-homepage.svg" height="100" width="1000" >

## Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Project Description
In this project, you'll apply what you've learned on data modeling with Postgres and build an ETL pipeline using Python. To complete the project, you will need to define fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.

## Data model

 ### Fact Table
**Table songplays**

| COLUMN  		| TYPE  	| CONSTRAINT  	|
|	---			|	---		|	---			|	
|songplay_id	|  SERIAL  	|   PRIMARY KEY	| 
|start_time		|  bigint	|   NOT NULL	| 
|user_id		|  int		|   NOT NULL	| 
|level			|  varchar 	|   			| 
|song_id		|  varchar	|   			| 
|artist_id		|  varchar	|   			| 
|session_id		|  int		|   			| 
|location		|  text		|   			| 
|user_agent		|  text		|   			|

The column songplay_id is the primary key.

Followed by the query to insert the data in the table above:

``` sql 
INSERT INTO songplays (start_time, user_id, level,song_id, artist_id, session_id, location, user_agent)
VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
 ```

 ### Dimensions Tables
 
 **Table users**
 
| 	COLUMN  	| TYPE  		| CONSTRAINT  	|
|	---			|	---			|		---		|	
| user_id		| int  			|   PRIMARY KEY	| 
| first_name	|   varchar		|  				| 
| last_name		|   varchar		|  				| 
| gender		|   varchar(1) 	|   			| 
| level			|   varchar		|   			| 

 
Followed by the query to insert the data in the table above:
 
 ``` sql
 INSERT INTO users (user_id, first_name, last_name, gender, level) 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (user_id) 
        DO UPDATE
        SET first_name = EXCLUDED.first_name, last_name = EXCLUDED.last_name,
        gender = EXCLUDED.gender, level = EXCLUDED.level
```

**Table songs**

| 	COLUMN  	| TYPE  	| CONSTRAINT   	|
|	---			|	---		|	---			|	
|   song_id		| varchar  	|   PRIMARY KEY	| 
|   title		|   text	|  				| 
|   artist_id	|   varchar	|   			| 
|   year		|   int 	|   			| 
|   duration	|   numeric	|   			| 

Followed by the query to insert the data in the table above:
 
``` sql
INSERT INTO songs (song_id, title, artist_id, year, duration) 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (song_id) 
        DO UPDATE
        SET title = EXCLUDED.title, artist_id = EXCLUDED.artist_id,
        year = EXCLUDED.year, duration = EXCLUDED.duration 
```

**Table artists**

| COLUMN  		| 	TYPE  		| CONSTRAINT   	|
|	---			|	---			|	---			|	
|   artist_id	| 	varchar 	|   PRIMARY KEY	| 
|   name		|   varchar		|   			| 
|   location	|   text		|   			| 
|   latitude	|   decimal		|   			| 
|   longitude	|   decimal 	|   			| 


Followed by the query to insert the data in the table above:
 
``` sql
INSERT INTO artists (artist_id, name, location, latitude, longitude) 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (artist_id) 
        DO UPDATE
        SET name = EXCLUDED.name, location = EXCLUDED.location,
        latitude = EXCLUDED.latitude, longitude = EXCLUDED.longitude
```

**Table time**
 
| COLUMN  	| 	TYPE  	| CONSTRAINT   	|
|	---		|	---		|	---			|	
|start_time	| 	bigint  |  PRIMARY KEY	| 
|   hour	|   int		|   			| 
|   day		|   int		|   			| 
|   week	|   int		|   			| 
|   month	|   int		|   			| 
|   year	|   int		|   			| 
|   weekday	|   varchar	|   			| 

Followed by the query to insert the data in the table above:
 
``` sql
INSERT INTO time (start_time, hour, day, week, month, year, weekday) 
VALUES (%s, %s, %s, %s, %s, %s, %s) 
ON CONFLICT (start_time) 
DO NOTHING
```

## Project Architecture

``` tree
data-modeling-with-postgres
├── Makefile
├── README.md
├── __pycache__
├── assets
├── create_tables.py
├── data
├── docker-compose-postgres.yml
├── etl.ipynb
├── etl.py
├── requirements.txt
├── sql_queries.py
├── test.ipynb
└── venv
```

## Directory:
	
1. sql_queries.py:

    Contains all the queries needed to delete and create databases and tables, 
in addition to inserting and selecting the available data

2. etl.py

step by step:

    1. Connect to the database;
    2. Process song files;
        1. Insert song data in songs table; 
        2. Insert artist data in artists table; 
    3. Process log files;
        1. Insert the date and time in unix format on time table, with this we can extract information such as day, month and year, hour, week of the year, week;
        2. Insert user info in users table;
        3. Insert songpplay records in songplays table; 
    4. Close connect to the database.

### create_tables.py

step by step:

    1. connect to the studentdb database;
    2. drop sparkifydb database  
    3. connect to the sparkifydb database;
    4. create table;
    5. Close connect to the database. 


## How to run scripts

First of all, initialize a virtual environment with project dependency, using the script:

``` bash 
cd data-modeling-with-postgres
make install && source venv/bin/activate
```

Download docker image:
``` bash
docker pull postgres
```
Run script docker-compose in your terminal:

``` bash
docker-compose -f docker-compose-postgres.yml up -d 
```

Run python script that consist in create database and tables of data model:
``` bash
python3 create_tables.py
```
In order to start extracting data from files and inserting the data into the database, run this python script.
``` bash
python3 etl.py
```


