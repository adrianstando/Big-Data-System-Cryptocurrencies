# This is a crucial branch. It contains only the most important things. It was developed for the supervisor of the subject.

# Big-Data-System-Cryptocurrencies

This repository contains results of the project during Big Data Analytics course at 2nd semester of Master's Degree Studies in the field of Data Science at Warsaw University of Technology (WUT). Our developer team consists of 4 students: Maciej Pawlikowski, Hubert Ruczyński, Bartosz Siński, and Adrian Stańdo.

TL;DR - The aim of the project is to deploy an end-to-end solution based on the Big Data analytics platforms.

The goal of this project is to create a system that enables its users to investigate the influence of the latest news articles on the exchange rates of cryptocurrencies. Our tool scraps current exchange rates and recent news regarding cryptocurrencies in order to perform a sentiment analysis of those messages. Extracted features are provided to the time-series, online, predictive model that will present estimated exchange rates of selected cryptocurrencies based on recent data. The archival data is also maintained to analyze past trends and article occurrences. The end users are able to track current exchange rates, our predictions, and current evaluation scores for our models, as well as analyze past data.

## Technological stack

In order to enable truely dsitributed computing our solution is heavily based on deploying each service in separate docker containers. With the usage of Tailscale, we designed a network that where the containers can communicate with each other. We aggregated various containers into separate subgroups, which share the same subnet. Such groups are described by the `COMPOSE_*`, where exists a `docker-compose.yaml` file which starts all containers described in the directory.

For now, our solution involves the following components:

* Docker,
* Tailscale,
* Portainer,
* Apache Hadoop 3.2.1 (namenode 2.0.0, java 8),
* Apache NiFi 1.23.2,
* Apache Kafka 3.4,
* Apache Spark 3.2.0 (bitnami, Debian Linux) (bde2020, commented version, 3.0.0 (Alpine Linux)),
* Apache HBase 2.2.6 (previously 1.2.6),
* Apache Hive 2.3.2 (metastore-postgresql 2.3.0),
* Apache Cassandra 4.0.11,
* Power BI Desktop with ODBC drivers for Cassandra, and Hive from CData (30-day trial).

## How to run the project?

### Prerequisites

You need Docker (Linux) or Docker-Desktop (Windows) installed.

You need WSL on Windows.

You need at least 16GB (prefferably 24GB) of unused RAM memory for the sytem.

You need a strong CPU (at least: 11th Gen Intel(R) Core(TM) i7-11700KF @3.60GHz).

You need around 50GB of free disk space for images, and data.

You need Tailscale (Linux) or Tailscale add-in (Windows) installed.

You need proper tokens to the APIs mentioned somewhere in the main folders READMEs.

You need Power BI Desktop with ODBC Drivers for Cassandra, and Hive (e.g. from CData): https://www.cdata.com/drivers/cassandra/download/odbc/ , https://www.cdata.com/drivers/hive/download/odbc/. During the installation/connection to the data sources you have to provide logins and passwords, which for Cassandra are: cassandra, cassandra, whereas for Hive: hive, hive.

### First-time set-up

Each folder that start with `COMPOSE_*` contains `docker-compose.yaml` file to run different parts of the system. Study `README.md` files in each directory to see whether additional environment variables have to be set.

#### Legacy
Additionally you have to configure hive, during the first runs.

```
docker cp hive-server:/opt/hive/conf/hive-site.xml .
docker cp ./hive-site.xml spark-master-test:/spark/conf/
docker cp ./hive-site.xml spark-master-test:/opt/bitnami/spark/conf/
rm ./hive-site.xml
```

Not required anymore, as we implemented it in start.sh script.

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

## Containers

If we provide one port it means that we have assigned the same port on localhost, e.g. 9870 equals 9870:9870. If we are mapping different ports, then we provide info like this (9001:9000). If single container exposes more ports, then we provide them after keyword `or`. If after the name you can see `^` indicator, it means that the containers are commented out/unavailable in final solution.

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
* spark-master^:             10.0.0.20:(9090:8080) or 7077
* spark-worker-1^:           10.0.0.21:8081
* jupyter^:                  10.0.0.23:8888
* jupyter_notebook^:         10.0.0.24:(8889:8888)
* spark-master-test:         10.0.0.25:(8082:8080) or (7078:7077)
* spark-worker-test:         10.0.0.26:(8083:8081)
* hive-server:               10.0.0.30:10000
* hive-metastore             10.0.0.31:9083
* hive-metastore-postgresql: 10.0.0.32
* hbase^:                    10.0.0.33:16000 or 16010 or 16020 or 16030 or 2888 or 3888 or 2181 or 9091:9090
* portainer:                 10.0.0.34:9000
* cassandra:                 10.0.0.40:7000 or 9042
* predictor:                 10:0.0.50:(8013:80)

## Web-Access

In order to get to services via internet explorers use following links (locally or globally):

Namenode: http://localhost:9870 or http://10.0.0.2:9870

Datanode: http://localhost:9864/datanode.html or http://10.0.0.3:9864/datanode.html

Resourcemanager: http://localhost:8088/cluster or http://10.0.0.4:8088/cluster

Nodemanager: http://localhost:8042/node or http://10.0.0.5:8042/node

NIFI: http://localhost:8080/nifi/ or http://10.0.0.6:8080/nifi/

Spark Master^: http://localhost:9090 or http://10.0.0.20:8080

Spark Worker 1^: http://10.0.0.21:8081

Spark Master Test: http://localhost:8082 or http://10.0.0.25:8080

Spark Worker Test: http://10.0.0.26:8081

Jupyter with PySpark^: http://10.0.0.23:8888

Portainer: http://10.0.0.34:9000 (login: admin password: BigData123BigData123)

## Additional data

The `templates` file includes NiFi templates used in our project. If you want to run it, copy the template to your NiFi. Probably you will additionally have to enable lots of services in the NiFi by hand, as we cannot do it automatically.

## Development stories

In the `Encountered issues.md` file you can read about the problems which occured during the project development, and get the insights into this process.

## Project architecture

The diagram below present the logical architecture of our project.

![diagram_MS4_project_architecture_final](https://github.com/adrianstando/Big-Data-System-Cryptocurrencies/assets/56126542/c1645440-b881-4d12-9397-886173e6a8fa)


## Exemplary results

In this section we include exemplary views from the final dashboards presenting the outcomes, prepared in Power BI.

![Dashboard_MS4_Batch_Views](https://github.com/adrianstando/Big-Data-System-Cryptocurrencies/assets/56126542/ba1d34c1-2f66-4884-bef0-9f87a74c3bae)
![Dashboard_MS4_Real_Time_Views_2](https://github.com/adrianstando/Big-Data-System-Cryptocurrencies/assets/56126542/56d8fb7b-78de-480b-b5e3-4bceb531eb4a)
![Dashboard_MS4_Dummy_predictor](https://github.com/adrianstando/Big-Data-System-Cryptocurrencies/assets/56126542/c8242c42-a5c1-45b7-a36a-deb5b5986484)


# GitHub Structure

* The COMPOSE files refer to particular docker container groups.
* Pictures presents the diagrams, screenshots, and plots created during the project.
* PowerBI contains things for this software.
* Project_Deliverables has various deliverables in forms of reports and presentations mostly
* PySpark_scripts gather all scripts used in the project.
* templates contains NiFi templates.
* Videos present short videos that present how the dashboard look-like.

# Not applicable anymore

This section provides additional information about the solutions, which were eventually discarded during the project development process.

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

## HBase

Eventually, we resigned from using HBase, and decided to use cassanda, but you can try you luck with executing following commands, and maybe it will work.

```
docker cp hbase:/opt/hbase-2.2.6/lib/hbase-client-2.2.6.jar .
docker cp ./hbase-client-2.2.6.jar spark-master:/spark/conf/
rm ./hbase-client-2.2.6.jar

docker cp hbase:/opt/hbase-2.2.6/conf/hbase-site.xml .
docker cp ./hbase-site.xml spark-master:/spark/conf/
rm ./hbase-site.xml
```

### Old hbase

```
docker cp hbase:/opt/hbase-1.2.6/lib/hbase-client-1.2.6.jar .
docker cp ./hbase-client-1.2.6.jar spark-master:/spark/conf/
rm ./hbase-client-1.2.6.jar

docker cp hbase:/etc/hbase-1.2.6/hbase-site.xml .
docker cp ./hbase-site.xml spark-master:/spark/conf/
rm ./hbase-site.xml
```
