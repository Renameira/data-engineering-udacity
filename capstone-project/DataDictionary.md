# **Data Dictionary Dimension Tables**

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




