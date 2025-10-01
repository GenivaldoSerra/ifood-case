# Databricks notebook source
# MAGIC %md
# MAGIC ## Qual a média de valor total (total\_amount) recebido em um mês considerando todos os yellow táxis da frota?
# MAGIC * **IMPORTANTE:** Conforme consulta abaixo da principal, foi verificado dados out of sample (Janeiro a Maio de 2023)
# MAGIC   * Assim foi adicionado filtro de mês e ano, atendendo demanda de negócio

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH monthly_total_amount AS (
# MAGIC   SELECT 
# MAGIC     SUM(FT.total_amount) AS monthly_total_amount
# MAGIC   FROM nyc_trip_record.trusted.fact_trip FT
# MAGIC   JOIN nyc_trip_record.trusted.dim_vendor DV
# MAGIC   ON FT.vendor_id = DV.vendor_id
# MAGIC   JOIN nyc_trip_record.trusted.dim_trip_time DT
# MAGIC   ON FT.trip_time_id = DT.trip_time_id
# MAGIC   WHERE 
# MAGIC     DV.car_type = "yellow_taxi"
# MAGIC     AND DT.dropoff_month < 6
# MAGIC     AND YEAR(DT.dropoff_datetime) = 2023
# MAGIC   GROUP BY DT.dropoff_month
# MAGIC )
# MAGIC
# MAGIC SELECT 
# MAGIC   CONCAT('R$ ', FORMAT_NUMBER(ROUND(AVG(monthly_total_amount), 2), 2)) AS avg_monthly_total_amount
# MAGIC FROM monthly_total_amount

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM nyc_trip_record.trusted.dim_trip_time
# MAGIC WHERE dropoff_month > 6
# MAGIC ORDER BY dropoff_datetime