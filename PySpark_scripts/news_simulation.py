# ./bin/pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0
import pyspark
import time
import shutil
from pyspark.sql.types import StructType, StringType, LongType
from pyspark.sql.functions import current_timestamp

# Settable parameters
time_between = 30 #time between article ingestion
number_of_iterations = 100 #how many times all articles from HDFS will be ingested into Kafka


# Spark session definition
spark = pyspark.sql.SparkSession.builder.appName("DataSimulatedFromHDFS").getOrCreate()

# Calculating number of files in HDFS folder
sc = spark.sparkContext
URI           = sc._gateway.jvm.java.net.URI
Path          = sc._gateway.jvm.org.apache.hadoop.fs.Path
FileSystem    = sc._gateway.jvm.org.apache.hadoop.fs.FileSystem
Configuration = sc._gateway.jvm.org.apache.hadoop.conf.Configuration

fs = FileSystem.get(URI("hdfs://namenode:9000"), Configuration())
status = fs.listStatus(Path('/master_dataset/news/news_io/'))

number_of_files = len(status)

# Method used to show estimated time news simulation will be running for 
def seconds_to_ddhhmmss(seconds):
    days, remainder = divmod(seconds, 86400)  
    hours, remainder = divmod(remainder, 3600)  
    minutes, seconds = divmod(remainder, 60)
    print("\n\n_________________________________________________________________")
    print(f"Maximum simulation time: {int(days):02d} days, {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
    print("_________________________________________________________________\n\n")

seconds_to_ddhhmmss(time_between * number_of_iterations * number_of_files)


# Schema of simulated data
schema = StructType()\
    .add("article_id",StringType())\
    .add("content",StringType())\
    .add("timestamp",LongType())

shutil.rmtree(f"checkpoint_rate_modified", ignore_errors=True)


# Main loop which reads files from HDFS and writes them one by one to Kafka with 30 seconds delay between each one of them. 
# After each file is processed spark starts process again untill reaching number_of_iterations limit.
i=30
while i<number_of_iterations:
    i+=1
    customer = spark.readStream.format("parquet").schema(schema).option("maxFilesPerTrigger",1).load("hdfs://namenode:9000/master_dataset/news/news_io")
    customer = customer.withColumn("current_timestamp", current_timestamp())
    query = customer.selectExpr("to_json(struct(*)) AS value").writeStream.format("kafka").outputMode("Append").trigger(processingTime=f"{time_between} seconds").option("kafka.bootstrap.servers", "10.0.0.10:9092").option("topic", "api_news").option("checkpointLocation", "checkpoint_rate_modified").start()
    query.awaitTermination(10)
    time.sleep(time_between * number_of_files)
    shutil.rmtree(f"checkpoint_rate_modified", ignore_errors=True)




