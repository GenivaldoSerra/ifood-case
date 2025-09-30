# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS nyc_trip_record

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS nyc_trip_record.raw;
# MAGIC CREATE SCHEMA IF NOT EXISTS nyc_trip_record.refined;
# MAGIC CREATE SCHEMA IF NOT EXISTS nyc_trip_record.trusted;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS nyc_trip_record.raw.yellow_taxi
# MAGIC (
# MAGIC   VendorID BIGINT, -- INTEGER FUNCIONOU
# MAGIC   tpep_pickup_datetime TIMESTAMP,
# MAGIC   tpep_dropoff_datetime TIMESTAMP,
# MAGIC   passenger_count BIGINT, -- INTEGER NÃO FUNCIONOU
# MAGIC   trip_distance DOUBLE,
# MAGIC   RatecodeID BIGINT, -- INTEGER NÃO FUNCIONOU
# MAGIC   store_and_fwd_flag STRING,
# MAGIC   PULocationID BIGINT, -- INTEGER FUNCIONOU
# MAGIC   DOLocationID BIGINT, -- INTEGER FUNCIONOU
# MAGIC   payment_type BIGINT, 
# MAGIC   fare_amount DOUBLE,
# MAGIC   extra DOUBLE,
# MAGIC   mta_tax DOUBLE,
# MAGIC   tip_amount DOUBLE,
# MAGIC   tolls_amount DOUBLE,
# MAGIC   improvement_surcharge DOUBLE,
# MAGIC   total_amount DOUBLE,
# MAGIC   congestion_surcharge DOUBLE,
# MAGIC   airport_fee DOUBLE,
# MAGIC   cbd_congestion_fee DOUBLE,
# MAGIC   _rescued_data VARCHAR(200)
# MAGIC )
# MAGIC USING PARQUET
# MAGIC LOCATION 's3://nyc-trip-record-ifood/raw/yellow/'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS nyc_trip_record.raw.green_taxi
# MAGIC (
# MAGIC   VendorID BIGINT, -- INTEGER FUNCIONOU
# MAGIC   lpep_pickup_datetime TIMESTAMP,
# MAGIC   lpep_dropoff_datetime TIMESTAMP,
# MAGIC   store_and_fwd_flag STRING,
# MAGIC   RatecodeID BIGINT, -- INTEGER NÃO FUNCIONOU
# MAGIC   PULocationID BIGINT, -- INTEGER FUNCIONOU
# MAGIC   DOLocationID BIGINT, -- INTEGER FUNCIONOU
# MAGIC   passenger_count BIGINT, -- INTEGER NÃO FUNCIONOU
# MAGIC   trip_distance DOUBLE,
# MAGIC   fare_amount DOUBLE,
# MAGIC   extra DOUBLE,
# MAGIC   mta_tax DOUBLE,
# MAGIC   tip_amount DOUBLE,
# MAGIC   tolls_amount DOUBLE,
# MAGIC   ehail_flag DOUBLE,
# MAGIC   improvement_surcharge DOUBLE,
# MAGIC   total_amount DOUBLE,
# MAGIC   payment_type BIGINT,
# MAGIC   trip_type BIGINT,
# MAGIC   congestion_surcharge DOUBLE,
# MAGIC   cbd_congestion_fee DOUBLE,
# MAGIC   _rescued_data VARCHAR(200)
# MAGIC )
# MAGIC USING PARQUET
# MAGIC LOCATION 's3://nyc-trip-record-ifood/raw/green/'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS nyc_trip_record.raw.fhv
# MAGIC (
# MAGIC   dispatching_base_num STRING,
# MAGIC   pickup_datetime TIMESTAMP,
# MAGIC   dropOff_datetime TIMESTAMP,
# MAGIC   PULocationID BIGINT,
# MAGIC   DOLocationID BIGINT,
# MAGIC   SR_Flag BIGINT,
# MAGIC   Affiliated_base_number STRING,
# MAGIC   _rescued_data VARCHAR(200)
# MAGIC )
# MAGIC USING PARQUET
# MAGIC LOCATION 's3://nyc-trip-record-ifood/raw/fhv/'
# MAGIC COMMENT "For Hire Vehicles records"

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS nyc_trip_record.raw.fhvhv
# MAGIC (
# MAGIC   hvfhs_license_num STRING,
# MAGIC   dispatching_base_num STRING,
# MAGIC   originating_base_num STRING,
# MAGIC   request_datetime TIMESTAMP,
# MAGIC   on_scene_datetime TIMESTAMP,
# MAGIC   pickup_datetime TIMESTAMP,
# MAGIC   dropoff_datetime TIMESTAMP,
# MAGIC   PULocationID BIGINT,
# MAGIC   DOLocationID BIGINT,
# MAGIC   trip_miles DOUBLE,
# MAGIC   trip_time BIGINT,
# MAGIC   base_passenger_fare DOUBLE,
# MAGIC   tolls double,
# MAGIC   bcf DOUBLE,
# MAGIC   sales_tax DOUBLE,
# MAGIC   congestion_surcharge DOUBLE,
# MAGIC   airport_fee DOUBLE,
# MAGIC   tips DOUBLE,
# MAGIC   driver_pay DOUBLE,
# MAGIC   shared_request_flag STRING,
# MAGIC   shared_match_flag STRING,
# MAGIC   access_a_ride_flag STRING,
# MAGIC   wav_request_flag STRING,
# MAGIC   wav_match_flag STRING,
# MAGIC   cbd_congestion_fee DOUBLE,
# MAGIC   _rescued_data VARCHAR(200)
# MAGIC )
# MAGIC USING PARQUET
# MAGIC LOCATION 's3://nyc-trip-record-ifood/raw/fhvhv/'
# MAGIC COMMENT "High Volume For Hire Vehicles records"