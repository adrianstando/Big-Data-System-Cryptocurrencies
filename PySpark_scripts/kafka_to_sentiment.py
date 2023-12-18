# jak odpalic sparka
# ./bin/pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.johnsnowlabs.nlp:spark-nlp_2.12:5.2.0

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType, DoubleType, LongType, ArrayType
from pyspark.sql import functions as F
from pyspark.sql.functions import col
from pyspark.sql.functions import split, window, current_timestamp, date_format
import pyspark.sql.types as T
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline
from statistics import mode 

spark = SparkSession.builder \
    .appName("KafkaReadAndWrite") \
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
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema_rates).alias("data")) \
    .select("data.*")\
    
modified_df = news_df.withColumn("BTC", news_df.content.contains('BTC'))
modified_df = modified_df.withColumn("bitcoin", news_df.content.contains('bitcoin'))
modified_df = modified_df.withColumn("Bitcoin", news_df.content.contains('Bitcoin'))

modified_df = modified_df.withColumn("ETH", news_df.content.contains('ETH'))
modified_df = modified_df.withColumn("Etherium", news_df.content.contains('Ethereum'))
modified_df = modified_df.withColumn("ether", news_df.content.contains('ether'))

modified_df = modified_df.withColumn("Final_bitcoin", F.when((modified_df.BTC=="true") | (modified_df.Bitcoin == "true" ), 'true'))
modified_df = modified_df.withColumn("Final_etherum", F.when((modified_df.ether=="true") | (modified_df.Etherium == "true" ) | (modified_df.ETH == "true" ), 'true'))

filtered_df = modified_df.filter(col("Final_bitcoin") == "true")

pipeline = PretrainedPipeline("analyze_sentiment", lang="en")

filtered_df = filtered_df.select('article_id',col('content').alias('text'),'timestamp')        

result_df = pipeline.transform(filtered_df).select('article_id', 'text', 'timestamp','sentiment.result')

temp = (result_df.withColumn("Dist",F.array_distinct("result"))
              .withColumn("Counts",F.expr("""transform(Dist,x->
                           aggregate(result,0,(acc,y)-> IF (y=x, acc+1,acc))
                                      )"""))
              .withColumn("Map",F.arrays_zip("Dist","Counts")
              )).drop("Dist","Counts")
out = temp.withColumn("Output_column",
                    F.expr("""element_at(array_sort(Map,(first,second)->
         CASE WHEN first['Counts']>second['Counts'] THEN -1 ELSE 1 END),1)['Dist']"""))

out_df = out.select('article_id','text','timestamp',col('Output_column').alias('sentiment'))

query = out_df.selectExpr("*") \
    .writeStream.outputMode("append").format("console").start()
query.awaitTermination()

