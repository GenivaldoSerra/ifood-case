# Databricks notebook source

# COMMAND ----------

green_taxi_refined_columns = [
    "VendorID",
    "passenger_count",
    "total_amount",
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
]

green_malformed_path = "s3://nyc-trip-record-ifood/staging/green_tripdata_2023-01.parquet"
green_refined_schema = spark.table("nyc_trip_record.refined.green_taxi").schema
green_target_schema = {field.name: field.dataType.simpleString() for field in green_refined_schema}

green_taxi_primary_keys = [
    "VendorID", 
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]

# Build select expressions with explicit casts
green_select_exprs = [
    f"CAST({col} AS {green_target_schema[col]}) AS {col}"
    for col in green_taxi_refined_columns
]

green_malformed_load = (
    spark.read
    .parquet(green_malformed_path)
    .selectExpr(*green_select_exprs)
    .dropDuplicates(green_taxi_primary_keys)
    .write.saveAsTable(
        mode="append",
        format="delta",
        name="nyc_trip_record.refined.green_taxi"
    )
)

# green_malformed_load.display()

# COMMAND ----------

yellow_taxi_refined_columns = [
    "VendorID",
    "passenger_count",
    "total_amount",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]

yellow_malformed_path = "s3://nyc-trip-record-ifood/staging/yellow_tripdata_2023-01.parquet"
yellow_refined_schema = spark.table("nyc_trip_record.refined.yellow_taxi").schema
yellow_target_schema = {field.name: field.dataType.simpleString() for field in yellow_refined_schema}

yellow_taxi_primary_keys = [
    "VendorID", 
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

yellow_select_exprs = [
    f"CAST({col} AS {yellow_target_schema[col]}) AS {col}"
    for col in yellow_taxi_refined_columns
]

yellow_malformed_load = (
    spark.read
    .parquet(yellow_malformed_path)
    .selectExpr(*yellow_select_exprs)
    .dropDuplicates(yellow_taxi_primary_keys)
    .write.saveAsTable(
        mode="append",
        format="delta",
        name="nyc_trip_record.refined.yellow_taxi"
    )
)