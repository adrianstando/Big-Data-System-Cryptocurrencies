# PySpark Scripts

This directory contains the most important PySpark/Python scripts used in the project.

* ML.py                   - Creates a simple ML model which makes predictions, and puts them in Cassandra.
* kafka_simulated_data.py - Simulates article flow from kafka to kafka.
* kafka_to_kafka.py       - Joining two streams (currency rates, and sentiment).
* kafka_to_sentiment.py   - Calculates sentiment on streamlined scrapped news.
* test_streaming_news.py  - Testing the preprocessing for news by prints in the terminal.
* test_streaming_rate.py  - Testing the preprocessing for currency rates by prints in the terminal.