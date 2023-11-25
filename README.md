# Big-Data-System-Cryptocurrencies

This repository contains results of the project during Big Data Analytics course at WUT

## How to run the project?

Each folder that start with `COMPOSE_*` contains `docker-compose.yaml` file to run different parts of the system. Study `README.md` files in each directory to see whether additional environment variables have to be set.

If the variables are set, you can run the following script to start all components:

```
./start.sh
```

In order to stop all containers, run:

```
./stop.sh
```

## Nifi-test branch

COMPOSE_kafka folder stores compose files for single kafka instance.
COMPOSE_kafka_cluster folder stores compose files for kafka cluster.
COMPOSE_kafka_zookeper folder stores compose files for kafka cluster with zookeper.

save_to_kafka.xml is a template for nifi flow that saves data to kafka topic. There are three publishKafka processors, each of them in different version to check if either of them works. 
