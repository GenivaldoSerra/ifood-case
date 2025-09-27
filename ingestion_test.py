import boto3
import requests

access_point_alias = 'access-point-g8hczuzn15jr7dy1jikwq5zbo94iause2a-s3alias'
client = boto3.client(
    "s3",
    aws_access_key_id="<my_access_key>",
    aws_secret_access_key="<my_secret_key>",
    region_name="us-east-1"  # ajuste a região se precisar
)

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet"

print(f"Baixando arquivo: {url}")

# faz o download
response = requests.get(url)
response.raise_for_status()

key = "yellow_tripdata_2025-01.parquet"

client.put_object(Bucket=access_point_alias, Key=key, Body=response.content)

print(f"Arquivo salvo em yellow_tripdata_2025-01.parquet")
