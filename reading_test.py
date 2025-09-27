from pyspark.sql import SparkSession
from pyspark import SparkConf

conf = SparkConf() \
    .set("spark.hadoop.fs.s3a.access.key", "<my_access_key>") \
    .set("spark.hadoop.fs.s3a.secret.key", "<my_secret_key>") \
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .set("spark.hadoop.fs.s3a.path.style.access", "true") \
    .set("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .set("spark.hadoop.fs.s3a.connection.timeout", "60000") \
    .set("spark.hadoop.fs.s3a.connection.establish.timeout", "60000") \
    .set("spark.hadoop.fs.s3a.connection.request.timeout", "60000") \
    .set("spark.hadoop.fs.s3a.attempts.maximum", "3") \
    .set("spark.hadoop.fs.s3a.paging.maximum", "1000")



spark = SparkSession.builder.config(conf=conf).getOrCreate()

# spark = SparkSession.builder.config(conf=conf).getOrCreate()

# conf.set("spark.hadoop.fs.s3a.access.key", "<my_access_key>")
# conf.set("spark.hadoop.fs.s3a.secret.key", "<my_secret_key>")

s3_path = "s3a://teste-calili/yellow_tripdata_2025-01.parquet"
df = spark.read.parquet(s3_path)

# If you have partitioned data and want to read a specific partition
# df = spark.read.parquet("s3a://your-bucket-name/path/to/your/parquet_data/partition_col=value/")

df.show()

