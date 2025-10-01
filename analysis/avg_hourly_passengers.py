# Databricks notebook source
# MAGIC %md
# MAGIC ## Qual a média de passageiros (passenger\_count) por cada hora do dia que pegaram táxi no mês de maio considerando todos os táxis da frota?

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH hourly_passengers_count AS (
# MAGIC   SELECT
# MAGIC     DT.dropoff_hour AS dropoff_hour,
# MAGIC     SUM(FT.passenger_count) AS hourly_passengers_count
# MAGIC   FROM nyc_trip_record.trusted.fact_trip FT
# MAGIC   JOIN nyc_trip_record.trusted.dim_trip_time DT
# MAGIC   ON FT.trip_time_id = DT.trip_time_id
# MAGIC   WHERE DT.dropoff_month = 5
# MAGIC   GROUP BY DT.dropoff_hour
# MAGIC )
# MAGIC
# MAGIC SELECT 
# MAGIC   dropoff_hour,
# MAGIC   FORMAT_NUMBER(
# MAGIC     FLOOR(AVG(hourly_passengers_count)), 
# MAGIC     0
# MAGIC   ) AS avg_hourly_passengers_count
# MAGIC FROM hourly_passengers_count
# MAGIC GROUP BY dropoff_hour
# MAGIC ORDER BY dropoff_hour

# COMMAND ----------

