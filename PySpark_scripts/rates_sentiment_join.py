# ./bin/pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType
from pyspark.sql.functions import col
from pyspark.sql.functions import window, current_timestamp

### Currency rates

# Spark session definition
spark = SparkSession.builder \
    .appName("KafkaReadAndWrite")\
    .getOrCreate()
spark.conf.set("spark.sql.streaming.statefulOperator.checkCorrectness.enabled", "false")

# Schema of incoming stream of crypto currency rates
schema_rates = StructType() \
    .add("id", StringType()) \
    .add("symbol", StringType()) \
    .add("changePercent24Hr", StringType()) \
    .add("priceUsd", StringType())

# loading crypto_rates from kafka
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

# Converting priceUSD to double and filtering out currency rates other than bitcoin
modified_df = rates_df.withColumn("priceUsd", rates_df["priceUsd"].cast("double"))
filtered_df = modified_df.filter(col("symbol") == "BTC")

# Adding timestamp, watermark and time window
filtered_df = filtered_df.withColumn("currency_timestamp", current_timestamp())
filtered_df = filtered_df.withWatermark("currency_timestamp", "2 minutes")
df_with_window = filtered_df.withColumn("window", window(filtered_df.currency_timestamp, "2 minutes") )# - expr("INTERVAL 1 hours")




### Sentiment

# Schema of incoming stream of sentiment
schema_rates = StructType()\
    .add("window_org",StringType())\
    .add("avg_sentiment",StringType())
    
    
# Loading sentiment from kafka
sentiment_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "10.0.0.10:9092") \
    .option("subscribe", "sentiment") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema_rates).alias("data")) \
    .select("data.*")\

# Adding timestamp, watermark and time window
sentiment_df = sentiment_df.withColumn("sentiment_timestamp", current_timestamp())
sentiment_df  = sentiment_df .withWatermark("sentiment_timestamp", "2 minutes")
sentiment_df= sentiment_df.withColumn("window", window(sentiment_df.sentiment_timestamp, "2 minutes") )
sentiment_df = sentiment_df.select('window','avg_sentiment')




### Joining of the streams

df_joined = df_with_window.join(
  sentiment_df,
 "window",
  "leftOuter" )

# Writing resulting stream to Kafka
query = df_joined.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "10.0.0.10:9092") \
    .option("topic", "rates_sentiment_joined") \
    .option("checkpointLocation", "checkpoint_rates_sentiment") \
    .start()

query.awaitTermination()
