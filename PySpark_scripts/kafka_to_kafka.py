# spark/bin/pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 
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
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema_rates).alias("data")) \
    .select("data.*")\
    
crypto_coins = ["BTC", "bitcoin", "Bitcoin", "ETH", "Ethereum", "ether"]
for coin in crypto_coins:
    news_df = news_df.withColumn(coin, col("content").contains(coin))

news_df = news_df.withColumn("Final_bitcoin", F.when((news_df.BTC=="true") | (news_df.Bitcoin == "true" ), 'true'))
news_df = news_df.withColumn("Final_etherum", F.when((news_df.ether=="true") | (news_df.Ethereum == "true" ) | (news_df.ETH == "true" ), 'true'))

news_df = news_df.filter(col("Final_bitcoin") == "true")

news_df = news_df.withColumn("sentiment_test", news_df.timestamp/3)
news_df = news_df.withColumn("current_time", current_timestamp())  #+ expr("INTERVAL 5 minutes")

news_df = news_df.withWatermark("current_time", "4 minutes").groupBy(window("current_time", "5 minutes")).agg(F.avg("sentiment_test").alias("avg_sentiment"))


# Left outer join with time range conditions
df_joined = df_with_window.join(
  news_df,
 "window",
  "leftOuter" )

query = df_joined.selectExpr("*") \
    .writeStream.outputMode("Append").option("truncate", "false").format("console").start()
query.awaitTermination()

# update
# append
# news_df.selectExpr("*").writeStream.outputMode("append").option("truncate", "false").format("console").start().awaitTermination()
# df_with_window.selectExpr("*").writeStream.outputMode("update").format("console").start().awaitTermination()
# query = df_with_window.selectExpr("to_json(struct(*)) AS value") \
#     .writeStream \
#     .format("kafka") \
#     .outputMode("complete")\
#     .option("kafka.bootstrap.servers", "10.0.0.10:9092") \
#     .option("topic", "topic_modified") \
#     .option("checkpointLocation", "checkpoint_rate_modified") \
#     .start()

# query.awaitTermination()

# df_with_window.selectExpr("*").writeStream.outputMode("append").option("truncate", "false").format("console").start().awaitTermination()
