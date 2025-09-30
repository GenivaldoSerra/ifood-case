# Databricks notebook source
# MAGIC %md
# MAGIC ## Escopo da camada:
# MAGIC * Selecionar colunas necessárias:
# MAGIC   * **Yellow_Taxi**
# MAGIC     * **VendorID**,
# MAGIC     * **passenger_count**, 
# MAGIC     * **total_amount**,
# MAGIC     * **tpep_pickup_datetime** 
# MAGIC     * **tpep_dropoff_datetime**
# MAGIC   * **Green_Taxi**
# MAGIC     * **VendorID**,
# MAGIC     * **passenger_count**, 
# MAGIC     * **total_amount**,
# MAGIC     * **lpep_pickup_datetime** 
# MAGIC     * **lpep_dropoff_datetime**
# MAGIC * Deduplicar seu conteúdo

# COMMAND ----------

# MAGIC %sql 
# MAGIC CREATE TABLE IF NOT EXISTS nyc_trip_record.refined.yellow_taxi
# MAGIC USING DELTA
# MAGIC LOCATION 's3://nyc-trip-record-ifood/refined/yellow/'

# COMMAND ----------

# MAGIC %sql 
# MAGIC CREATE TABLE IF NOT EXISTS nyc_trip_record.refined.green_taxi
# MAGIC USING DELTA
# MAGIC LOCATION 's3://nyc-trip-record-ifood/refined/green/'

# COMMAND ----------

# MAGIC %sql 
# MAGIC CREATE TABLE IF NOT EXISTS nyc_trip_record.refined.fhv
# MAGIC USING DELTA
# MAGIC LOCATION 's3://nyc-trip-record-ifood/refined/fhv/'

# COMMAND ----------

# MAGIC %sql 
# MAGIC CREATE TABLE IF NOT EXISTS nyc_trip_record.refined.fhvhv
# MAGIC USING DELTA
# MAGIC LOCATION 's3://nyc-trip-record-ifood/refined/fhvhv/'

# COMMAND ----------

yellow_taxi_refined_columns = [
    "VendorID",
    "passenger_count",
    "total_amount",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]

yellow_taxi_primary_keys = [
    "VendorID", 
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

(
    spark.table("nyc_trip_record.raw.yellow_taxi")
    .select(
        yellow_taxi_refined_columns
    )
    .dropDuplicates(yellow_taxi_primary_keys)
    .write.saveAsTable(
        mode="overwrite",
        format="delta",
        name="nyc_trip_record.refined.yellow_taxi"
    )
)

# COMMAND ----------

green_taxi_refined_columns = [
    "VendorID",
    "passenger_count",
    "total_amount",
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
]

green_taxi_primary_keys = [
    "VendorID", 
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]

(
    spark.table("nyc_trip_record.raw.green_taxi")
    .select(
        green_taxi_refined_columns
    )
    .dropDuplicates(green_taxi_primary_keys)
    .write.saveAsTable(
        mode="overwrite",
        format="delta",
        name="nyc_trip_record.refined.green_taxi"
    )
)