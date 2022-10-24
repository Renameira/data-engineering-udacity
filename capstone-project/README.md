# Capstone Project

## Overview
The purpose of the data engineering capstone project is to give you a chance to combine what you've learned throughout the program. This project will be an important part of your portfolio that will help you achieve your data engineering-related career goals. In this project, you can choose to complete the project provided for you, or define the scope and data for a project of your own design. Either way, you'll be expected to go through the same steps outlined below.

#### Describe and Gather Data 

- **I94 Immigration Data**: This data comes from the US National Tourism and Trade Office;
- **World Temperature Data**: Este conjunto de dados veio do Kaggle. E há informações sobre a média de temperatura de países e cidades;
- **U.S. City Demographic Data**: This dataset presents information on the city's population, such as median age, number of population 
separated by gender, number of people born abroad, among others.

## Data model
<br>


## Dimension Tables:


### **dim_immigration_person**

|COLUMN		|  TYPE	| DESCRIPTION |
|---		|  ---		| 		---				|            
|cic_id			|  int 	|		CIC id			|            
|citizen_country|		int	| Citizen Country 				|            	
|residence_country		|  int	| 	Residence country			|            
|birth_year		|  int		| Birthday year  					|             
|gender		|  varchar(1)		| Gener of person				|            
|ins_num		|  varchar		|	Ins num			|            


### **dim_immigration_airline**

|COLUMN	|  TYPE  	|DESCRIPTION |
| --- | -- | --- |
|cic_id		|  int	|CIC id  |
|airline		|  varchar		| Airline code  |
|admin_num			|  float 	| Admin number |
|flight_number		|  varchar	| Flight number |
|visa_type		|  varchar		| Visa code| 


### **dim_country_code**

|COLUMN | TYPE |DESCRIPTION |
| --- | --- | --- | 
|code 		|  int		| Country code | 
|country			|  varchar 	|  Country name |


### **city_code**

|COLUMN | TYPE |DESCRIPTION |
| --- | --- | --- |
|code 		|  varchar		| City code|
|city			|  varchar 	| City name |

### **state_code**

|COLUMN | TYPE |DESCRIPTION |
| --- | --- | --- |
|code 		|  varchar		| State code |
|state			|  varchar 	| State name |



### **dim_temperature**

| COLUMN  		| TYPE  	| DESCRIPTION | 
|	---			|	---		| --- |
|measurement_date	|  timestamp  | Measured date|
|average_temp		|  float	| Average of temperature |
|average_temperature_uncertainty | float | Temperature measurement uncertainty|
|city			|  varchar 	| Measured City | 
|country		|  varchar	| Measured Country |
|latitude		|  varchar	| Latitude |
|longitude		|  varchar	| Longitude |
|measuremnt_year		|  int	| Measured year |
|measuremnt_month		|  int		| Measuared month |


### **dim_demographics**

|COLUMN | TYPE | DESCRIPTION | 
| --- | --- | --- |
|city		|  varchar		| City |
|state			|  varchar 	| Full state name |
|median_age		|  float	| Median age |
|male_population		|  float	| Total male population |
|female_population		|  float		| Total female population |
|total_population		|  float		| Total of population | 
|number_veterans		|  float		| Total of veterans |
|foreign_born	|  int  	| Total of foreign born |
|average_household_size		|  float	| Average household size |
|cod_state		|  varchar		| State code|
|race			|  varchar 	| Race of population |
|count		|  bigint	| Total of population |



### **dim_demographics**

|COLUMN | TYPE | DESCRIPTION | 
| --- | --- | --- |
|city		|  varchar		| City |
|state			|  varchar 	| Full state name |
|median_age		|  float	| Median age |
|male_population		|  float	| Total male population |
|female_population		|  float		| Total female population |
|total_population		|  float		| Total of population | 
|number_veterans		|  float		| Total of veterans |
|foreign_born	|  int  	| Total of foreign born |
|average_household_size		|  float	| Average household size |
|cod_state		|  varchar		| State code|
|race			|  varchar 	| Race of population |
|count		|  bigint	| Total of population |
| r | float| |


## Fact Table:


### **fact_immigration**


| COLUMN  		| TYPE  	|DESCRIPTION | 
|	---			|	---		| --- |
|cic_id	|  int  	| CIC id |
|year		|  int	| Year | 
|month		|  int		 | Month |
|city_code  |  int | City code
|cod_port			|  varchar 	| Port code | 
|cod_state		|  varchar	| State code |
|arrival_date		|  timestamp	| Arrival date | 
|departure_date	|  timestamp		| Departure date |
|mode		|  int		| Mode code |
|visa		|  int		| Visa code |
|country	|  varchar  	| Country |


<p>

## Project structure

``` tree
capstone-project
├── DataDictionary.md
├── Makefile
├── README.md
├── config
├── data
│   ├── GlobalTemperature.zip
│   ├── I94_SAS_Labels_Descriptions.sas
│   ├── immigration_data_sample.csv
│   ├── sas_data.zip
│   └── us-cities-demographics.csv
├── requirements.txt
└── src
    ├── Capstone.ipynb
    ├── data_quality.ipynb
    └── etl.py
```

## Python File:

1. etl.py

    1. Connect to the data source;
    2. Process the data with Spark;

2. Data_quality.ipynb

Used to validate the data and confirm the process performed in etl.py

3. capstone.ipynb

It was used to explore the data and perform data modeling.


## How to run scripts
<br>

First of all, initialize a virtual environment with project dependency, using the script bellow.

``` bash 
cd capstone-project
make install && source venv/bin/activate
```

Then set the `.env` in config file (if you have problem there is `.env.example` for help you):

and if are ok, you execute:

``` bash
python3 etl.py
```

