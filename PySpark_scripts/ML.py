# ./bin/pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 --conf spark.cassandra.auth.username=cassandra --conf spark.cassandra.auth.password=cassandra
#
# open cassandra
# cqlsh 10.0.0.40 -u cassandra -p cassandra
#
# in cassandra
# CREATE KEYSPACE example_keyspace
# WITH replication = {
#   'class': 'SimpleStrategy',
#   'replication_factor': 1
# };
#
# USE example_keyspace;
#
# CREATE TABLE rates_predictions_2 (
#   start_window TIMESTAMP,
#   end_window TIMESTAMP,
#   currency TEXT,
#   predict DOUBLE,
#   PRIMARY KEY ((start_window, end_window, currency))
#) WITH default_time_to_live = 7200;
#
# default_time_to_live = 2 hours
#


# pip install pandas PyArrow numpy scikit-learn


from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType, DoubleType, LongType, IntegerType
from pyspark.sql import functions as F
from pyspark.sql.functions import col, sum, expr, avg
from pyspark.sql.functions import split, window, current_timestamp, date_format
import pyspark.sql.types as T
from pyspark.sql.functions import from_unixtime
from pyspark.sql.functions import lag
from pyspark.sql.functions import col, collect_list, concat_ws, udf

spark = SparkSession.builder \
    .appName("KafkaReadAndWrite")\
    .getOrCreate()

spark.conf.set("spark.sql.streaming.statefulOperator.checkCorrectness.enabled", "false")

schema_rates = StructType() \
    .add("id", StringType()) \
    .add("symbol", StringType()) \
    .add("changePercent24Hr", StringType()) \
    .add("supply", StringType()) \
    .add("priceUsd", StringType()) \
    .add("timestamp", LongType())

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
modified_df = modified_df.withColumn("priceUsd_modified", F.col("priceUsd") * 2)
modified_df = modified_df.withColumn("current_timestamp", current_timestamp())
filtered_df = modified_df.withWatermark("current_timestamp", "10 seconds")

df_with_window = filtered_df.withWatermark("current_timestamp", "15 seconds") \
    .groupBy(window(filtered_df.current_timestamp, "60 seconds","10 seconds"), col("symbol"))

x = df_with_window.agg(collect_list('priceUsd').alias('data'))

def myFunc(data_list):
    import numpy as np
    from sklearn.linear_model import LinearRegression
    y_values = data_list
    X_values = np.arange(1, len(y_values) + 1).reshape(-1, 1)
    model = LinearRegression()
    model.fit(X_values, y_values)
    return float(model.predict([[len(y_values) + 1]])[0])

myUdf = udf(myFunc, DoubleType())

x1 = x.withColumn('data', myUdf('data'))

out = x1.select(
    col("window.start").alias("start_window"),
    col("window.end").alias("end_window"),
    col("symbol").alias("currency"),
    col("data").alias("predict")
)


#query = out.selectExpr("*") \
#    .writeStream.outputMode("Append").option("truncate", "false").format("console").start()
#query.awaitTermination()

cassandra_host = "10.0.0.40"
cassandra_port = "9042"
cassandra_keyspace = "example_keyspace"
cassandra_table = "rates_predictions_2"

cassandra_query = out \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(lambda df, epoch_id: df.write \
                  .format("org.apache.spark.sql.cassandra") \
                  .mode("append") \
                  .option("keyspace", cassandra_keyspace) \
                  .option("table", cassandra_table) \
                  .option("spark.cassandra.connection.host", cassandra_host) \
                  .option("spark.cassandra.connection.port", cassandra_port) \
                  .save()) \
    .start()




# 1. retention_period on Cassandra
# 2. folders in hdfs
# 3. batch processing to hive -> timestamp, data_source, sentiment
# 4. sentiment from kafka to hdfs
# 5. stream joining
