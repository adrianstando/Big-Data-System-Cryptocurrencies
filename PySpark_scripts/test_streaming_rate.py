from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType, LongType
from pyspark.sql import functions as F
from pyspark.sql.functions import col, expr
from pyspark.sql.functions import window, current_timestamp



spark = SparkSession.builder \
    .appName("KafkaReadAndWrite")\
    .getOrCreate()
spark.conf.set("spark.sql.streaming.statefulOperator.checkCorrectness.enabled", "false")
schema_rates = StructType() \
    .add("id", StringType()) \
    .add("symbol", StringType()) \
    .add("changePercent24Hr", StringType()) \
    .add("priceUsd", StringType())

rates_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "10.0.0.10:9092") \
    .option("subscribe", "crypto_rates") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema_rates).alias("data")) \
    .select("data.*")

modified_df = rates_df.withColumn("priceUsd", rates_df["priceUsd"].cast("double"))
# modified_df = modified_df.withColumn("priceUsd_modified", F.col("priceUsd") * 2)
modified_df = modified_df.withColumn("current_timestamp", current_timestamp())
filtered_df = modified_df.filter(col("symbol") == "BTC")
filtered_df = filtered_df.withWatermark("current_timestamp", "6 minutes")
df_with_window = filtered_df.withColumn("window", window(filtered_df.current_timestamp, "5 minutes") )# - expr("INTERVAL 1 hours")

df_with_window.selectExpr("*").writeStream.outputMode("append").option("truncate", "false").format("console").start().awaitTermination()