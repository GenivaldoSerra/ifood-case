# Databricks notebook source
import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product
import logging
import requests


LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_STYLE: str = '%'

logger = logging.getLogger(__name__)

logging.basicConfig(
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    style=LOG_STYLE,
    level=logging.INFO
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=dbutils.secrets.get(scope="nyc-trip-record", key="aws-access-key"),
    aws_secret_access_key=dbutils.secrets.get(scope="nyc-trip-record", key="aws-secret-key")
)

bucket_name = "nyc-trip-record-ifood"
valid_car_types = ["yellow", "green", "fhv", "fhvhv"]
car_type = valid_car_types if dbutils.widgets.get("car_type") == "all" else dbutils.widgets.get("car_type").split(",")
years = list(map(int, dbutils.widgets.get("years").split(",")))
months = list(map(int, dbutils.widgets.get("months").split("-")))

car_type_malformed_error_log = "Parâmetro car_type inválido ou não informado"
car_type_value_error_log = f"Valor de car_type inválido. Valores válidos: {valid_car_types}"
years_error_log = "Parâmetro years inválido ou não informado"
month_error_log = "Parâmetro months inválido ou não informado"

if not car_type or type(car_type[0]) != str:
    logger.error(car_type_malformed_error_log)
    raise Exception(car_type_malformed_error_log)
for taxi in car_type:
    if taxi not in valid_car_types:
        taxi_error_log = logger.error(car_type_value_error_log)
        raise Exception(car_type_value_error_log)
if not years or years[0] > years[-1]:
    logger.error(years_error_log)
    raise Exception(years_error_log)
if not months or months[0] > months[1]:
    logger.error(month_error_log)
    raise Exception(month_error_log)
months_adjusted = [("0"+ str(month)) if month < 10 else str(month) for month in range(months[0], months[1]+1)]
logger.info(f"Baixando arquivos para: {car_type}, {years}, {months_adjusted}")

url_tpl = "https://d37ci6vzurychx.cloudfront.net/trip-data/{CAR_TYPE}_tripdata_{YEAR}-{MONTH}.parquet"
key_tpl = "raw/{CAR_TYPE}/{YEAR}_{MONTH}.parquet"

def download_and_upload(taxi, year, month):
    url = url_tpl.format(CAR_TYPE=taxi, YEAR=year, MONTH=month)
    key = key_tpl.format(CAR_TYPE=taxi, YEAR=year, MONTH=month)

    if "2023_01.parquet" not in key:
        logger.info(f"Baixando: {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        logger.info(f"Salvando em: {key}")
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=response.content
        )
        return key

tasks = list(product(car_type, years, months_adjusted))

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(download_and_upload, *t) for t in tasks]
    for f in as_completed(futures):
        logger.info("Arquivo salvo em:", f.result())