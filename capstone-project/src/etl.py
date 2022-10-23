import configparser
import os
import logging
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import DateType
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.functions import col, lit, year, month, upper, to_date


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
    spark = (
        SparkSession.builder.config(
            "spark.jars.packages", "saurfang:spark-sas7bdat:2.0.0-s_2.11"
        )
        .enableHiveSupport()
        .getOrCreate()
    )
    return spark


def rename_columns(table, new_columns):
    for original, new in zip(table.columns, new_columns):
        table = table.withColumnRenamed(original, new)
    return table


def process_immigration_data(spark, input_data, output_data):
    """Process immigration data to get fact_immigration,
    dim_immi_personal and dim_immi_airline tables
        Arguments:
            spark {object}: SparkSession object
            input_data {object}: Source S3 endpoint
            output_data {object}: Target S3 endpoint
        Returns:
            None
    """

    logging.info("Start processing immigration")

    immi_data = os.path.join(
        input_data + "sas_data"
    )
    df = spark.read.parquet(immi_data)

    logging.info("Start processing fact_immigration")

    fact_immigration = (
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
    fact_immigration = rename_columns(fact_immigration, new_columns)

    fact_immigration = fact_immigration.withColumn("country", lit("United States"))

    fact_immigration.write.mode("overwrite").partitionBy("state_code").parquet(
        path=output_data + "fact_immigration"
    )

    logging.info("Start processing dim_immi_personal")

    dim_immi_personal = (
        df.select("cicid", "i94cit", "i94res", "biryear", "gender", "insnum")
        .distinct()
        .withColumn("immi_personal_id", monotonically_increasing_id())
    )


    new_columns = [
        "cic_id",
        "citizen_country",
        "residence_country",
        "birth_year",
        "gender",
        "ins_num",
    ]
    dim_immi_personal = rename_columns(dim_immi_personal, new_columns)


    dim_immi_personal.write.mode("overwrite").parquet(
        path=output_data + "dim_immi_personal"
    )

    logging.info("Start processing dim_immi_airline")

    dim_immi_airline = (
        df.select("cicid", "airline", "admnum", "fltno", "visatype")
        .distinct()
        .withColumn("immi_airline_id", monotonically_increasing_id())
    )


    new_columns = ["cic_id", "airline", "admin_num", "flight_number", "visa_type"]
    dim_immi_airline = rename_columns(dim_immi_airline, new_columns)


    dim_immi_airline.write.mode("overwrite").parquet(
        path=output_data + "dim_immi_airline"
    )


def process_label_descriptions(spark, input_data, output_data):
    """Parsing label desctiption file to get codes of country, city, state
    Arguments:
        spark {object}: SparkSession object
        input_data {object}: Source S3 endpoint
        output_data {object}: Target S3 endpoint
    Returns:
        None
    """

    logging.info("Start processing label descriptions")
    label_file = os.path.join(input_data + "I94_SAS_Labels_Descriptions.SAS")
    with open(label_file) as f:
        contents = f.readlines()

    country_code = {}
    for countries in contents[10:298]:
        pair = countries.split("=")
        code, country = pair[0].strip(), pair[1].strip().strip("'")
        country_code[code] = country
    spark.createDataFrame(country_code.items(), ["code", "country"]).write.mode(
        "overwrite"
    ).parquet(path=output_data + "country_code")

    city_code = {}
    for cities in contents[303:962]:
        pair = cities.split("=")
        code, city = pair[0].strip("\t").strip().strip("'"), pair[1].strip(
            "\t"
        ).strip().strip("''")
        city_code[code] = city
    spark.createDataFrame(city_code.items(), ["code", "city"]).write.mode(
        "overwrite"
    ).parquet(path=output_data + "city_code")

    state_code = {}
    for states in contents[982:1036]:
        pair = states.split("=")
        code, state = pair[0].strip("\t").strip("'"), pair[1].strip().strip("'")
        state_code[code] = state
    spark.createDataFrame(state_code.items(), ["code", "state"]).write.mode(
        "overwrite"
    ).parquet(path=output_data + "state_code")


def process_temperature_data(spark, input_data, output_data):
    """Process temperature data to get dim_temperature table
    Arguments:
        spark {object}: SparkSession object
        input_data {object}: Source S3 endpoint
        output_data {object}: Target S3 endpoint
    Returns:
        None
    """

    logging.info("Start processing dim_temperature")

    tempe_data = os.path.join(
        input_data + "Globaltemperature/GlobalLandTemperaturesByCity.csv"
    )
    df = spark.read.csv(tempe_data, header=True)

    df = df.where(df["Country"] == "United States")
    dim_temperature = df.select(
        ["dt", "AverageTemperature", "AverageTemperatureUncertainty", "City", "Country"]
    ).distinct()

    new_columns = ["dt", "avg_temp", "avg_temp_uncertnty", "city", "country"]
    dim_temperature = rename_columns(dim_temperature, new_columns)

    dim_temperature = dim_temperature.withColumn("dt", to_date(col("dt")))
    dim_temperature = dim_temperature.withColumn("year", year(dim_temperature["dt"]))
    dim_temperature = dim_temperature.withColumn("month", month(dim_temperature["dt"]))

    dim_temperature.write.mode("overwrite").parquet(
        path=output_data + "dim_temperature"
    )


def process_demography_data(spark, input_data, output_data):
    """Process demograpy data to get dim_demog_population
    and dim_demog_statistics table
       Arguments:
           spark {object}: SparkSession object
           input_data {object}: Source S3 endpoint
           output_data {object}: Target S3 endpoint
       Returns:
           None
    """

    logging.info("Start processing dim_demog_populaiton")
    
    demog_data = os.path.join(input_data + "us-cities-demographics.csv")
    df = spark.read.format("csv").options(header=True, delimiter=";").load(demog_data)

    dim_demog_population = (
        df.select(
            [
                "City",
                "State",
                "Male Population",
                "Female Population",
                "Number of Veterans",
                "Foreign-born",
                "Race",
            ]
        )
        .distinct()
        .withColumn("demog_pop_id", monotonically_increasing_id())
    )

    new_columns = [
        "city",
        "state",
        "male_population",
        "female_population",
        "num_vetarans",
        "foreign_born",
        "race",
    ]
    dim_demog_population = rename_columns(dim_demog_population, new_columns)

    dim_demog_population.write.mode("overwrite").parquet(
        path=output_data + "dim_demog_population"
    )

    logging.info("Start processing dim_demog_statistics")
    dim_demog_statistics = (
        df.select(["City", "State", "Median Age", "Average Household Size"])
        .distinct()
        .withColumn("demog_stat_id", monotonically_increasing_id())
    )

    new_columns = ["city", "state", "median_age", "avg_household_size"]
    dim_demog_statistics = rename_columns(dim_demog_statistics, new_columns)
    dim_demog_statistics = dim_demog_statistics.withColumn("city", upper(col("city")))
    dim_demog_statistics = dim_demog_statistics.withColumn("state", upper(col("state")))

    dim_demog_statistics.write.mode("overwrite").parquet(
        path=output_data + "dim_demog_statistics"
    )


def main():
    spark = create_spark_session()
    input_data = SOURCE_S3_BUCKET
    output_data = DEST_S3_BUCKET

    process_immigration_data(spark, input_data, output_data)
    process_label_descriptions(spark, input_data, output_data)
    process_temperature_data(spark, input_data, output_data)
    process_demography_data(spark, input_data, output_data)
    logging.info("Data processing completed")


if __name__ == "__main__":
    main()
