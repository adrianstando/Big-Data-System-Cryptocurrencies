# Big-Data-System-Cryptocurrencies

This repository contains results of the project during Big Data Analytics course at 2nd semester of Master's Degree Studies in the field of Data Science at Warsaw University of Technology (WUT). Our developer team consists of 4 students: Maciej Pawlikowski, Hubert Ruczyński, Bartosz Siński, and Adrian Stańdo.

The aim of the project is to deploy an end-to-end solution based on the Big Data analytics platforms.

## Technological stack

In order to enable truely dsitributed computing our solution is heavily based on deploying each service in separate docker containers. With the usage of Tailscale, we designed a network that where the containers can communicate with each other. We aggregated various containers into separate subgroups, which share the same subnet. Such groups are described by the `COMPOSE_*`, where exists a `docker-compose.yaml` file which starts all containers described in the directory.

For now, our solution involves the following components:

* Docker,
* Tailscale,
* Portainer,
* Apache Hadoop 3.2.1 (namenode 2.0.0, java 8),
* Apache NiFi 1.23.2,
* Apache Kafka 3.4,
* Apache Spark 3.0.0,
* Apache HBase 1.2.6,
* Apache Hive 2.3.2. (metastore-postgresql 2.3.0)

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

### Stopping containers

In order to stop all containers running on a singular machine execute:

```
./stop.sh
```

### Tailscale and Portainer

To gain a remote access to the services, you have to download Tailscale (https://tailscale.com/download/), create an account there, and log in with whe same account on multiple devices which will be present in our Tailscale network. It assures, that you are able to connect (ping), all containers in the big-data-net.

Additionally, to remotely access the console of all containers you should use the Portainer, which is a web UI that allows you to access all the containers remotely. Firstly, you have to run it on the machine where the project is hosted, and set username and password. Later, Portainer will only ask you to log inwith provided data.

Portainer service link: http://10.0.0.34:9000

## Access

In order to get to services via internet explorers use following links (locally or globally):

Namenode: http://localhost:9870 or http://10.0.0.2:9870

Datanode: http://localhost:9864/datanode.html or http://10.0.0.3:9864/datanode.html

Resourcemanager: http://localhost:8088/cluster or http://10.0.0.4:8088/cluster

Nodemanager: http://localhost:8042/node or http://10.0.0.5:8042/node

NIFI: http://localhost:8080/nifi/ or http://10.0.0.6:8080/nifi/

Spark Master: http://localhost:9090 or http://10.0.0.20:8080

Spark Worker 1: http://10.0.0.21:8081

Spark Worker 2: http://10.0.0.22:8081

Jupyter with PySpark: http://10.0.0.23:8888

Portainer: http://10.0.0.34:9000 (login: admin password: BigData123BigData123)

## Containers

If we provide one port it means that we have assigned the same port on localhost, e.g. 9870 equals 9870:9870. If we are mapping different ports, then we provide info like this (9001:9000). If single container exposes more ports, then we provide them after keyword `or`.

* big-data-net:              10.0.0.0/16
* hdfs-namenode:             10.0.0.2:9870 or 8020 or (9001:9000 - Spark)
* hdfs-datanode:             10.0.0.3:9864
* hdfs-resourcemanager:      10.0.0.4:8088
* hdfs-nodemanager:          10.0.0.5:8042
* nifi:                      10.0.0.6:8080
* tailscale_nifi:            10.0.0.7
* news-scrapper:             10.0.0.8:(8012:80)
* kafka0:                    10.0.0.10:(9094:9092)
* kafka1:                    10.0.0.11:(9095:9092)
* spark-master:              10.0.0.20:(9090:8080) or 7077
* spark-worker-1:            10.0.0.21
* jupyter:                   10.0.0.23:8888
* jupyter_notebook:          10.0.0.24:(8889:8888)
* hive-server:               10.0.0.30:10000
* hive-metastore             10.0.0.31:9083
* hive-metastore-postgresql: 10.0.0.32
* hbase:                     10.0.0.33:16000 or 16010 or 16020 or 16030 or 2888 or 3888 or 2181
* portainer:                 10.0.0.34:9000

## Additional data

The `templates` file includes a NiFi templates used in our project. If you want to run it, copy the template to your NiFi. Probably you will additionally have to enable lots of services in the NiFi by hand, as we cannot do it automatically.

## Development stories

In the `Encountered issues.md` file you can read about the problems which occured during the project development, and get the insights into this process.

# Not applicable anymore

## Filling the route table

Execute the following command to configure all ip-routes between different subnets, while all services are running.

```
./start_network.sh
```

The script above walks through each `COMPOSE_*` directory, then gets into each container, where it updates the `apt-get`, and then installs the `iproute2` package. After this set up it creates the connections between the container and all other subnets, via the tailscale network.

If it it doesn't work properly, or if you use the distributed version you can run a legacy version in each `COMPOSE_*` directory.

```
./network.sh
```