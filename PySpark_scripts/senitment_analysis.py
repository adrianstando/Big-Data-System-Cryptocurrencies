# at first
# pip install sparknlp
# later run pyspark:
# ./bin/pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.johnsnowlabs.nlp:spark-nlp_2.12:5.2.0

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType, LongType
from pyspark.sql import functions as F
from pyspark.sql.functions import col
from pyspark.sql.functions import window, current_timestamp
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline
from pyspark.sql.functions import col, avg

# Spark session definition
spark = SparkSession.builder \
    .appName("KafkaReadAndWrite") \
    .getOrCreate()

# Schema of incoming stream
schema = StructType()\
    .add("article_id",StringType())\
    .add("content",StringType())\
    .add("timestamp",LongType())
    
    
# Loading scrapped_news from kafka
news_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "10.0.0.10:9092") \
    .option("subscribe", "api_news") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")\
    
# Adding temporary flags of articles containing words like BTC or bitcoin
modified_df = news_df.withColumn("BTC", news_df.content.contains('BTC'))
modified_df = modified_df.withColumn("Bitcoin", news_df.content.contains('Bitcoin'))

# Combining above flags into singular flag which represents if article mentions bitcoin
modified_df = modified_df.withColumn("Final_bitcoin", F.when((modified_df.BTC=="true") | (modified_df.Bitcoin == "true" ), 'true'))

# Filtering out articles that don't mention bitcoin
filtered_df = modified_df.filter(col("Final_bitcoin") == "true")
filtered_df = filtered_df.select('article_id',col('content').alias('text'),'timestamp')        

# Sentiment calculation
pipeline = PretrainedPipeline("analyze_sentiment", lang="en")
result_df = pipeline.transform(filtered_df).select('article_id', 'text', 'timestamp','sentiment.result')
result_df = result_df.withColumn("result", F.expr("""transform(result,x-> CASE WHEN x == 'positive' THEN 1 ELSE 0 END)"""))
result_df = result_df.withColumn('size', F.size('result')).withColumn('sentiment', F.expr('aggregate(result, 0L, (acc,x) -> acc+x, acc -> acc /size)'))
result_df = result_df.select('sentiment')

# Adding timestamp, watermark and time window
result_df = result_df.withColumn("news_time", current_timestamp()) 
grouped_df = result_df.withWatermark("news_time", "2 minutes").groupBy(window("news_time", "2 minutes")).agg(F.avg("sentiment").alias("avg_sentiment"))

# Writing stream to Kafka
query = grouped_df.selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "10.0.0.10:9092") \
    .option("topic", "sentiment") \
    .option("checkpointLocation", "checkpoint_sentiment") \
    .start()

query.awaitTermination()



