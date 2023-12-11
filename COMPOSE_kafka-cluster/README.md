# Kafka

Kafka Version: 3.4

To run it on your machine you have to execute the following code in order to create topics:


```
docker exec -it kafka0 /bin/bash

kafka-topics.sh --create --bootstrap-server 10.0.0.10:9092 --topic api_news --partitions 2 --replication-factor 2

kafka-topics.sh --create --bootstrap-server 10.0.0.10:9092 --topic crypto_rates --partitions 2 --replication-factor 2

kafka-topics.sh --create --bootstrap-server 10.0.0.10:9092 --topic scraped_news --partitions 2 --replication-factor 2

exit
```
