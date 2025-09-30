# Databricks notebook source
# MAGIC %md
# MAGIC * Escopo da camada:
# MAGIC   * Modelagem dimensional (Star Schema)
# MAGIC     ```sql
# MAGIC     nyc_trip_record.trusted.fact_trip
# MAGIC     (
# MAGIC       fact_id STRING,
# MAGIC       vendor_id STRING,
# MAGIC       trip_time_id STRING,
# MAGIC       passenger_count LONG,
# MAGIC       total_amount DOUBLE
# MAGIC     );
# MAGIC     ```
# MAGIC
# MAGIC     ```sql
# MAGIC     nyc_trip_record.trusted.dim_trip_time
# MAGIC     (
# MAGIC       trip_time_id STRING,
# MAGIC       pickup_datetime TIMESTAMP,
# MAGIC       pickup_month INTEGER,
# MAGIC       pickup_hour INTEGER,
# MAGIC       dropoff_datetime TIMESTAMP,
# MAGIC       dropoff_month INTEGER,
# MAGIC       dropoff_hour INTEGER
# MAGIC     )
# MAGIC     ```
# MAGIC
# MAGIC     ```sql
# MAGIC     nyc_trip_record.trusted.dim_vendor
# MAGIC     (
# MAGIC       vendor_id STRING,
# MAGIC       vendor_code BIGINT,
# MAGIC       vendor_name STRING,
# MAGIC       car_type STRING
# MAGIC     )
# MAGIC     ``````
# MAGIC

# COMMAND ----------

from pyspark.sql import functions as F

green_taxi_vendor_id = {
    1: "Creative Mobile Technologies, LLC",
    2: "Curb Mobility, LLC",
    6: "Myle Technologies Inc"
}

yellow_taxi_columns_to_rename = {
        "VendorID": "vendor_code",
        "lpep_pickup_datetime": "pickup_datetime",
        "lpep_dropoff_datetime": "dropoff_datetime"
    }

green_taxi_new_columns = {
        "car_type": F.lit("green_taxi"),
        "vendor_name": F.when(F.col("vendor_code") == 1, green_taxi_vendor_id[1])
        .when(F.col("vendor_code") == 2, green_taxi_vendor_id[2])
        .when(F.col("vendor_code") == 6, green_taxi_vendor_id[6])
        .otherwise("Unknown")
    }

green_taxy_df = (
    spark.table("nyc_trip_record.refined.green_taxi")
    .withColumnsRenamed(yellow_taxi_columns_to_rename)
    .withColumns(green_taxi_new_columns)
)

# COMMAND ----------

yellow_taxi_vendor_id = {
    1: "Creative Mobile Technologies, LLC",
    2: "Curb Mobility, LLC",
    6: "Myle Technologies Inc",
    7: "Helix"
}

yellow_taxi_columns_to_rename = {
    "VendorID": "vendor_code",
    "tpep_pickup_datetime": "pickup_datetime",
    "tpep_dropoff_datetime": "dropoff_datetime"
}

yellow_taxi_new_columns = {
    "car_type": F.lit("yellow_taxi"),
    "vendor_name": F.when(F.col("vendor_code") == 1, yellow_taxi_vendor_id[1])
    .when(F.col("vendor_code") == 2, yellow_taxi_vendor_id[2])
    .when(F.col("vendor_code") == 6, yellow_taxi_vendor_id[6])
    .when(F.col("vendor_code") == 7, yellow_taxi_vendor_id[7])
    .otherwise("Unknown")
}

yellow_taxy_df = (
    spark.table("nyc_trip_record.refined.yellow_taxi")
    .withColumnsRenamed(yellow_taxi_columns_to_rename)
    .withColumns(yellow_taxi_new_columns)
)

# COMMAND ----------

sha_num_bits = 256

model_columns = {
    "pickup_month": F.month("pickup_datetime"),
    "pickup_hour": F.hour("pickup_datetime"),
    "dropoff_month": F.month("dropoff_datetime"),
    "dropoff_hour": F.hour("dropoff_datetime"),
    "vendor_id": F.sha2(
        col=F.concat(
            F.col("vendor_code").cast("string"), 
            F.col("vendor_name"), 
            F.col("car_type")
        ),
        numBits=sha_num_bits
    ),
    "trip_time_id": F.sha2(
        col=F.concat(
            F.col("pickup_datetime").cast("string"),
            F.col("dropoff_datetime").cast("string")
        ), 
        numBits=sha_num_bits
    ),
    "fact_id": F.sha2(
        col=F.concat(
            F.col("vendor_id").cast("string"),
            F.col("pickup_datetime").cast("string"),
            F.col("dropoff_datetime").cast("string"),
            F.col("total_amount").cast("string"),
            F.col("passenger_count").cast("string")
        ), 
        numBits=sha_num_bits
    )
}

trusted_trips = (
    green_taxy_df.unionByName(yellow_taxy_df)
    .withColumns(model_columns)
)

# COMMAND ----------

(
    trusted_trips.select(
        "vendor_id",
        "vendor_code",
        "vendor_name", 
        "car_type"
    )
    .distinct()
    .write.saveAsTable(
        mode="overwrite",
        format="delta",
        name="nyc_trip_record.trusted.dim_vendor"
    )
)

# COMMAND ----------

(
    trusted_trips.select(
        "trip_time_id",
        "pickup_datetime",
        "pickup_month",
        "pickup_hour",
        "dropoff_datetime",
        "dropoff_month",
        "dropoff_hour"
    )
    .distinct()
    .write.saveAsTable(
        mode="overwrite",
        format="delta",
        name="nyc_trip_record.trusted.dim_trip_time"
    )
)

# COMMAND ----------

(
    trusted_trips.select(
        "fact_id",
        "vendor_id",
        "trip_time_id",
        "passenger_count",
        "total_amount"
    )
    .write.saveAsTable(
        mode="append",
        format="delta",
        name="nyc_trip_record.trusted.fact_trip"
    )
)