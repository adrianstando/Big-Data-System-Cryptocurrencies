# Big-Data-System-Cryptocurrencies

This repository contains results of the project during Big Data Analytics course at WUT

## Access

In order to get to services via internet explorers use following links (locally or globally):

Namenode: http://localhost:9870 or http://10.0.0.2:9870
Datanode: http://localhost:9864/datanode.html or http://10.0.0.3:9864/datanode.html
Resourcemanager: http://localhost:8088/cluster or http://10.0.0.4:8088/cluster
Nodemanager: http://localhost:8042/node or http://10.0.0.5:8042/node
NIFI: http://localhost:8080/nifi/ or http://10.0.0.6:8080/nifi/
Spark Master: http://localhost:9090 or http://10.3.0.2:8080
Spark Worker 1: http://10.3.0.3:8081
Spark Worker 2: http://10.3.0.4:8081
Jupyter with PySpark: http://10.3.0.6:8888

## How to run the project?

### First-time set-up

Each folder that start with `COMPOSE_*` contains `docker-compose.yaml` file to run different parts of the system. Study `README.md` files in each directory to see whether additional environment variables have to be set.

### Starting containers

If the variables are set, you can run the following script to start all components:

```
./start.sh
```

## Filling the IP-route

Execute the following command to configure all ip-routes between different subnets.

```
./start_network.sh
```

If it it doesn't work properly you can run a legacy version in each COMPOSE_ file

```
./network.sh
```

### Stopping containers

In order to stop all containers, run:

```
./stop.sh
```
