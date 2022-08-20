# Project: Data Warehouse

## Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights into what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Project Description
In this project, you'll apply what you've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, you will need to load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

## Data model
<br>


### Fact table

### Dimension table





## Project structure

``` tree
data-warehouse-amazon-redshift
├── Makefile
├── README.md
├── __pycache__
├── config
│   └── .env.example
├── config.py
├── create_tables.py
├── etl.py
├── requirements.txt
├── sql_queries.py
├── terraform
│	├── main.tf
│	└── variable.tf   
└── venv
```

## Python File:
	
1. sql_queries.py:

    Contains all the queries needed to delete and create databases and tables, 
in addition to inserting the available data


2. create_tables.py

    1. connect to the sparkify database;  
    2. drop table if exists;
    3. create table;
    4. Close connect to the database. 

3. etl.py

    1. Connect to the database;
    2. 





    2. Process song files;
        1. Insert song data in songs table; 
        2. Insert artist data in artists table; 
    3. Process log files;
        1. Insert the date and time in unix format on time table, with this we can extract information such as day, month and year, hour, week of the year, week;
        2. Insert user info in users table;
        3. Insert songpplay records in songplays table; 
    4. Close connect to the database.

## How to run scripts
<br>

First of all, initialize a virtual environment with project dependency, using the script bellow.

``` bash 
cd data-warehouse-amazon-redshift
make install && source venv/bin/activate
```

Then set the `.env` in config file (if you have problem there is `.env.example` for help you):

<p>
Then, create the readshift cluster using o terraform, run the code bellow in your terminal:
``` bash
terraform plan
```

and if are ok, you execute:

``` bash
terraform apply
```

Run python script that consist in connecting with sparkify database and create tables of data model:
``` bash
python3 create_tables.py
```

In order to start extracting data from s3 and inserting the data into the data warehouse(redshift), run this python script.

``` bash
python3 etl.py
```

