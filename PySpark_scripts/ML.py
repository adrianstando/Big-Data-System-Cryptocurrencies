# ./bin/pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 --conf spark.cassandra.auth.username=cassandra --conf spark.cassandra.auth.password=cassandra
#
# open cassandra
# cqlsh 10.0.0.40 -u cassandra -p cassandra
#
# in cassandra
# CREATE KEYSPACE test4
# WITH replication = {
#   'class': 'SimpleStrategy',
#   'replication_factor': 1
# };
#
# USE test4;
#
# CREATE TABLE ratespredictions (
#   start_window TIMESTAMP,
#   end_window TIMESTAMP,
#   currency TEXT,
#   prediction_arf DOUBLE,
#   rolling_rmse_arf DOUBLE,
#   prediction_lr DOUBLE,
#   rolling_rmse_lr DOUBLE,
#   real_previous_value DOUBLE,
#   prediction_previous_value_lr DOUBLE,
#   prediction_previous_value_arf DOUBLE,
#   PRIMARY KEY (end_window, currency)
# ) WITH default_time_to_live = 604800;
#
# default_time_to_live = 1 week
#


# pip install pandas PyArrow numpy requests


from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType, DoubleType, LongType, IntegerType
from pyspark.sql import functions as F
from pyspark.sql.functions import split, window, current_timestamp, date_format
from pyspark.sql.functions import col, collect_list, concat_ws, udf

spark = SparkSession.builder \
    .appName("KafkaReadAndWrite") \
    .getOrCreate()

spark.conf.set("spark.sql.streaming.statefulOperator.checkCorrectness.enabled", "false")

schema_rates = StructType() \
    .add("id", StringType()) \
    .add("symbol", StringType()) \
    .add("changePercent24Hr", StringType()) \
    .add("supply", StringType()) \
    .add("priceUsd", StringType()) \
    .add("timestamp", LongType())

schema_predict = StructType() \
    .add("prediction_arf", DoubleType()) \
    .add("rolling_rmse_arf", DoubleType()) \
    .add("prediction_lr", DoubleType()) \
    .add("rolling_rmse_lr", DoubleType()) \
    .add("real_previous_value", DoubleType()) \
    .add("prediction_previous_value_lr", DoubleType()) \
    .add("prediction_previous_value_arf", DoubleType())

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
filtered_df = modified_df.filter((col("symbol") == "BTC") | (col("symbol") == "ETH") | (col("symbol") == "DOGE"))
filtered_df = filtered_df.withWatermark("current_timestamp", "10 seconds")

df_with_window = filtered_df.withWatermark("current_timestamp", "15 seconds") \
    .groupBy(window(filtered_df.current_timestamp, "110 seconds", "10 seconds"), col("symbol"))

x = df_with_window.agg(collect_list('priceUsd').alias('data'))


# def myFunc(data_list, currency):
#     print(len(data_list), data_list)
#     return (0.0, 0.0, 0.0, 0.0)


def myFunc(data_list, currency):
    import requests
    api_url = "http://10.0.0.50:80/predict"
    payload = {
        "lag_values": data_list,
        "crypto_name": currency
    }
    response = requests.get(api_url, params=payload)
    if response.status_code == 200:
        response_json = response.json()
        return (
            response_json["prediction_arf"],
            response_json["rolling_rmse_arf"],
            response_json["prediction_lr"],
            response_json["rolling_rmse_lr"],
            response_json["real_previous_value"],
            response_json["prediction_previous_value_lr"],
            response_json["prediction_previous_value_arf"]
        )
    else:
        return (0, 0, 0, 0)


myUdf = udf(myFunc, schema_predict)

x1 = x.withColumn('data_predict', myUdf('data', 'symbol'))

out = x1.select(
    col("window.start").alias("start_window"),
    col("window.end").alias("end_window"),
    col("symbol").alias("currency"),
    col("data_predict.*")
)

# query = (out.selectExpr("*")
#          .writeStream.outputMode("Append").option("truncate", "false").format("console").start())
# query.awaitTermination()

cassandra_host = "10.0.0.40"
cassandra_port = "9042"
cassandra_keyspace = "test4"
cassandra_table = "ratespredictions"

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
