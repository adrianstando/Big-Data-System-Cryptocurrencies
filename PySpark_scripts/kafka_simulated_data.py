# spark/bin/pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType, DoubleType, LongType
from pyspark.sql import functions as F
from pyspark.sql.functions import col, sum, expr, avg
from pyspark.sql.functions import split, window, current_timestamp, date_format
import pyspark.sql.types as T
from pyspark.sql.functions import from_unixtime
import time

spark = SparkSession.builder \
    .appName("KafkaReadAndWrite")\
    .getOrCreate()



schema_rates = StructType()\
    .add("article_id",StringType())\
    .add("content",StringType())\
    .add("timestamp",LongType())
    
    
# scraped_news
news_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "10.0.0.10:9092") \
    .option("subscribe", "api_news") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema_rates).alias("data")) \
    .select("data.*")\
    
time.sleep(60)
# update
# append
# news_df.selectExpr("*").writeStream.outputMode("append").option("truncate", "false").format("console").start().awaitTermination()
# df_with_window.selectExpr("*").writeStream.outputMode("update").format("console").start().awaitTermination()
query = news_df.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .outputMode("Append")\
    .option("kafka.bootstrap.servers", "10.0.0.10:9092") \
    .option("topic", "api_news") \
    .option("checkpointLocation", "checkpoint_rate_modified") \
    .start()

query.awaitTermination()

# df_with_window.selectExpr("*").writeStream.outputMode("append").option("truncate", "false").format("console").start().awaitTermination()
