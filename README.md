# Big-Data-System-Cryptocurrencies

This repository contains results of the project during Big Data Analytics course at 2nd semester of Master's Degree Studies in the field of Data Science at Warsaw University of Technology (WUT). Our developer team consists of 4 students: Maciej Pawlikowski, Hubert Ruczyński, Bartosz Siński, and Adrian Stańdo.

The aim of the project is to deploy an end-to-end solution based on the Big Data analytics platforms.

## Technological stack

In order to enable truely dsitributed computing our solution is heavily based on deploying each service in separate docker containers. With the usage of Tailscale, we designed a network that where the containers can communicate with each other. We aggregated various containers into separate subgroups, which share the same subnet. Such groups are described by the `COMPOSE_*`, where exists a `docker-compose.yaml` file which starts all containers described in the directory.

For now, our solution involves the following components:

* Docker,
* Tailscale,
* Apache Hadoop,
* Apache NiFi,
* Apache Kafka,
* Apache Spark,
* Apache HBase,
* Apache Hive.

## How to run the project?

### Prerequisites

You need Docker (Linux) or Docker-Desktop (Windows) installed.

You need WSL on Windows.

You need Tailscale (Linux) or Tailscale add-in (Windows) installed.

You need proper tokens to the APIs mentioned somewhere in the main folders READMEs.

### First-time set-up

Each folder that start with `COMPOSE_*` contains `docker-compose.yaml` file to run different parts of the system. Study `README.md` files in each directory to see whether additional environment variables have to be set.

### Starting containers

If the variables are set, you can run the following script to start all components on a singular machine:

```
./start.sh
```

### Filling the route table

Execute the following command to configure all ip-routes between different subnets, while all services are running.

```
./start_network.sh
```

The script above walks through each `COMPOSE_*` directory, then gets into each container, where it updates the `apt-get`, and then installs the `iproute2` package. After this set up it creates the connections between the container and all other subnets, via the tailscale network.

If it it doesn't work properly, or if you use the distributed version you can run a legacy version in each `COMPOSE_*` directory.

```
./network.sh
```

#### Stopping containers

In order to stop all containers running on a singular machine execute:

```
./stop.sh
```

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

## Additional data

The `templates` file includes a nifi templates used in our project.