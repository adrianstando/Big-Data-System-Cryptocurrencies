# PySpark Scripts

This directory contains the most important PySpark/Python scripts used in the project.
* batch_layer_news.py      - Transferring data about articles (3 cryptocurrenicies: BTC, ETH, DOGE) from HDFS to Hive as a part of batch processing.
* batch_layer_rates_old.py - Transferring data about cryptocurrencies values (BTC, ETH, DOGE) from HDFS to Hive as a part of batch processing.
* kafka_simulated_data.py  - Simulates article flow from kafka to kafka.
* kafka_to_kafka.py        - Joining two streams (currency rates, and sentiment).
* kafka_to_sentiment.py    - Calculates sentiment on streamlined scrapped news.
* ML.py                    - Creates ML models (Adaptive Random Forest, and Linear Regression) which make predictions, and puts them in Cassandra.
* news_simulation.py       - Simulation of the news stream in a real-time manner, which is much faster than original stream. It reads files from HDFS, and writesthem to KAfka one by one with 30 seconds of delay.
* rates_sentiment_join.py  - Joining the streams for cryptocurrencies exchange rates with the results of sentiment analysis.
* sentiment_analysis.py    - Calculation of the sentiment on stream news data (new version).
* test_raw_in_hdfs         - Testing if new data is saved to HDFS.
* test_streaming_news.py   - Testing the preprocessing for news by prints in the terminal.
* test_streaming_rate.py   - Testing the preprocessing for currency rates by prints in the terminal.

## ML.py

The most important script in our project. It uses the scrapped data to perform the real-time predictions. To run it you have to follow this instruction:

```
./bin/pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 --conf spark.cassandra.auth.username=cassandra --conf spark.cassandra.auth.password=cassandra
#open cassandra
#cqlsh 10.0.0.40 -u cassandra -p cassandra

# in cassandra
CREATE KEYSPACE test4
WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};

USE test4;

CREATE TABLE ratespredictions (
  start_window TIMESTAMP,
  end_window TIMESTAMP,
  currency TEXT,
  prediction_arf DOUBLE,
  rolling_rmse_arf DOUBLE,
  prediction_lr DOUBLE,
  rolling_rmse_lr DOUBLE,
  real_previous_value DOUBLE,
  prediction_previous_value_lr DOUBLE,
  prediction_previous_value_arf DOUBLE,
  PRIMARY KEY (end_window, currency)
) WITH default_time_to_live = 604800;

default_time_to_live = 1 week


pip install pandas PyArrow numpy requests
```