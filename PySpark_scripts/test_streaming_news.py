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



news_df.selectExpr("*").writeStream.outputMode("append").option("truncate", "false").format("console").start().awaitTermination()
