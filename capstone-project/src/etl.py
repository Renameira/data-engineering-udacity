import configparser
import os
import logging
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import DateType
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.functions import col, lit, year, month, upper, to_date, udf


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# AWS configuration
config = configparser.ConfigParser()
config.read("config/.env", encoding="utf-8-sig")

os.environ["AWS_ACCESS_KEY_ID"] = config["AWS"]["AWS_ACCESS_KEY_ID"]
os.environ["AWS_SECRET_ACCESS_KEY"] = config["AWS"]["AWS_SECRET_ACCESS_KEY"]
SOURCE_S3_BUCKET = config["S3"]["SOURCE_S3_BUCKET"]
DEST_S3_BUCKET = config["S3"]["DEST_S3_BUCKET"]


# data processing functions
def create_spark_session():

    logging.info("Creating spark session")

    spark = (
        SparkSession.builder.config(
            "spark.jars.packages", "saurfang:spark-sas7bdat:2.0.0-s_2.11"
        )
        .enableHiveSupport()
        .getOrCreate()
    )
    logging.info("Created spark session")
    return spark


def _sas_to_date(date):
    if date is not None:
        return pd.to_timedelta(date, unit="D") + pd.Timestamp("1960-1-1")


def _transform_columns(table, new_columns):
    for original, new in zip(table.columns, new_columns):
        table = table.withColumnRenamed(original, new)
    return table


def process_immigration_data_fact(spark, input_data, output_data):
    """
    This process performs a reading of data immigration of the sources and performs the
    insertions of fact data in the storage(S3).

    Args:
        spark {object}: SparkSession
        input_data {object}: data source
        output_data {object}: data target

    Returns:
        None
    """

    logging.info("processing immigration")

    df_immigration = os.path.join(input_data, "sas_data")
    df = spark.read.parquet(df_immigration)

    logging.info("Start processing fact_immigration")

    df_fact_immigration = (
        df.select(
            "cicid",
            "i94yr",
            "i94mon",
            "i94port",
            "i94addr",
            "arrdate",
            "depdate",
            "i94mode",
            "i94visa",
        )
        .distinct()
        .withColumn("immigration_id", monotonically_increasing_id())
    )

    new_columns = [
        "cic_id",
        "year",
        "month",
        "city_code",
        "state_code",
        "arrive_date",
        "departure_date",
        "mode",
        "visa",
    ]

    df_fact_immigration = _transform_columns(df_fact_immigration, new_columns)

    df_fact_immigration = df_fact_immigration.withColumn(
        "arrive_date", udf(_sas_to_date, DateType())(col("arrive_date"))
    )
    df_fact_immigration = df_fact_immigration.withColumn(
        "departure_date", udf(_sas_to_date, DateType())(col("departure_date"))
    )

    df_fact_immigration = df_fact_immigration.withColumn(
        "country", lit("United States")
    )

    df_fact_immigration.write.mode("overwrite").partitionBy(
        "year", "month", "state_code"
    ).parquet(path=f"{output_data}/fact_immigration")


def process_immigration_data_dim(spark, input_data, output_data):
    """
    This process performs a reading of data immigration of the sources and performs the
    insertions of dimension data in the storage(S3).

    Args:
        spark {object}: SparkSession
        input_data {object}: data source
        output_data {object}: data target

    Returns:
        None
    """

    logging.info("processing immigration dimension")

    immi_data = os.path.join(input_data, "sas_data")
    df = spark.read.parquet(immi_data)

    logging.info("Start processing dimension immigration person")

    df_dim_immigration_person = (
        df.select("cicid", "i94cit", "i94res", "biryear", "gender", "insnum")
        .distinct()
        .withColumn("immi_person_id", monotonically_increasing_id())
    )

    new_columns = [
        "cic_id",
        "citizen_country",
        "residence_country",
        "birth_year",
        "gender",
        "ins_num",
    ]
    df_dim_immigration_person = _transform_columns(
        df_dim_immigration_person, new_columns
    )

    df_dim_immigration_person.write.mode("overwrite").parquet(
        path=f"{output_data}/dim_immigration_person"
    )

    logging.info("Start processing dimension immigration airline")

    df_dim_immigration_airline = (
        df.select("cicid", "airline", "admnum", "fltno", "visatype")
        .distinct()
        .withColumn("immigration_airline_id", monotonically_increasing_id())
    )

    new_columns = ["cic_id", "airline", "admin_num", "flight_number", "visa_type"]
    df_dim_immigration_airline = _transform_columns(
        df_dim_immigration_airline, new_columns
    )

    df_dim_immigration_airline.write.mode("overwrite").parquet(
        path=f"{output_data}/dim_immigration_airline"
    )


def _read_SAS_i94(input_data: str):
    label_file = os.path.join(input_data, "I94_SAS_Labels_Descriptions.SAS")
    print(label_file)
    with open(label_file) as f:
        data = f.readlines()
    return data


def process_label_descriptions_country(spark, input_data, output_data):
    """Prepare the auxiliar country_code table"
    Arguments:
        spark {object}: SparkSession object
        input_data {object}: Source S3 endpoint
        output_data {object}: Target S3 endpoint
    Returns:
        None
    """

    logging.info("Start processing SAS label descriptions to country")
    contents = _read_SAS_i94(input_data)

    country_code = {}
    for countries in contents[10:298]:
        pair = countries.split("=")
        code, country = pair[0].strip(), pair[1].strip().strip("'")
        country_code[code] = country
    spark.createDataFrame(country_code.items(), ["code", "country"]).write.mode(
        "overwrite"
    ).parquet(path=f"{output_data}/country_code")


def process_label_descriptions_city(spark, input_data, output_data):
    """Prepare the auxiliar city_code table
    Arguments:
        spark {object}: SparkSession object
        input_data {object}: Source S3 endpoint
        output_data {object}: Target S3 endpoint
    Returns:
        None
    """

    logging.info("Start processing SAS label descriptions to city")
    contents = _read_SAS_i94(input_data)

    city_code = {}
    for cities in contents[303:962]:
        pair = cities.split("=")
        code, city = pair[0].strip("\t").strip().strip("'"), pair[1].strip(
            "\t"
        ).strip().strip("''")
        city_code[code] = city
    spark.createDataFrame(city_code.items(), ["code", "city"]).write.mode(
        "overwrite"
    ).parquet(path=f"{output_data}/city_code")


def process_label_descriptions_state(spark, input_data, output_data):
    """Prepare the auxiliar country_state city_code"
    Arguments:
        spark {object}: SparkSession object
        input_data {object}: Source S3 endpoint
        output_data {object}: Target S3 endpoint
    Returns:
        None
    """

    logging.info("Start processing SAS label descriptions to state")
    contents = _read_SAS_i94(input_data)

    state_code = {}
    for states in contents[982:1036]:
        pair = states.split("=")
        code, state = pair[0].strip("\t").strip("'"), pair[1].strip().strip("'")
        state_code[code] = state
    spark.createDataFrame(state_code.items(), ["code", "state"]).write.mode(
        "overwrite"
    ).parquet(path=f"{output_data}/state_code")


def process_temperature_data(spark, input_data, output_data):
    """Process temperature data to use like dimension table.
    Arguments:
        spark {object}: SparkSession object
        input_data {object}: Source S3 endpoint
        output_data {object}: Target S3 endpoint
    Returns:
        None
    """

    logging.info("Start processing temperature data")

    temperature_file = os.path.join(
        input_data, "Globaltemperature/GlobalLandTemperaturesByCity.csv"
    )
    df_temperature = spark.read.csv(temperature_file, header=True)

    df_temperature = df_temperature.where(df_temperature["Country"] == "United States")
    df_dim_temperature = df_temperature.select(
        [
            "dt",
            "AverageTemperature",
            "AverageTemperatureUncertainty",
            "City",
            "Country",
            "Latitude",
            "Longitude",
        ]
    ).distinct()

    new_columns = [
        "date",
        "avg_temp",
        "avg_temp_uncertnty",
        "city",
        "country",
        "latitude",
        "longitude",
    ]
    df_dim_temperature = _transform_columns(df_dim_temperature, new_columns)

    df_dim_temperature = df_dim_temperature.withColumn("date", to_date(col("date")))
    df_dim_temperature = df_dim_temperature.withColumn(
        "year", year(df_dim_temperature["date"])
    )
    df_dim_temperature = df_dim_temperature.withColumn(
        "month", month(df_dim_temperature["date"])
    )

    df_dim_temperature.write.mode("overwrite").parquet(
        path=f"{output_data}/dim_temperature"
    )


def process_demographic_data(spark, input_data, output_data):
    """process that extracts information from the demographic dimension
    Arguments:
        spark {object}: SparkSession object
        input_data {object}: Source S3 endpoint
        output_data {object}: Target S3 endpoint
    Returns:
        None
    """

    logging.info("Start processing dim_demog_populaiton")

    df_demographics = os.path.join(input_data, "us-cities-demographics.csv")
    df = (
        spark.read.format("csv")
        .options(header=True, delimiter=";")
        .load(df_demographics)
    )

    df_dim_demographics = (
        df.select(
            [
                "City",
                "State",
                "Median Age",
                "Male Population",
                "Female Population",
                "Total Population",
                "Number of Veterans",
                "Foreign-born",
                "Average Household Size",
                "State Code",
                "Race",
                "Count",
            ]
        )
        .distinct()
        .withColumn("demog_pop_id", monotonically_increasing_id())
    )

    new_columns = [
        "city",
        "state",
        "median_age",
        "male_population",
        "female_population",
        "total_population",
        "number_veterans",
        "foreign_born",
        "average_household_size",
        "cod_state",
        "race",
        "count",
    ]
    df_dim_demographics = _transform_columns(df_dim_demographics, new_columns)

    df_dim_demographics.write.mode("overwrite").parquet(
        path=f"{output_data}/dim_demographics"
    )


def main():
    spark = create_spark_session()
    input_data = SOURCE_S3_BUCKET
    output_data = DEST_S3_BUCKET

    process_immigration_data_fact(spark, input_data, output_data)
    process_immigration_data_dim(spark, input_data, output_data)
    process_label_descriptions_country(spark, input_data, output_data)
    process_label_descriptions_city(spark, input_data, output_data)
    process_label_descriptions_state(spark, input_data, output_data)
    process_temperature_data(spark, input_data, output_data)
    process_demographic_data(spark, input_data, output_data)
    logging.info("The data was processed correctly")


if __name__ == "__main__":
    main()
