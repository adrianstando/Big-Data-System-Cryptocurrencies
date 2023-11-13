# Big-Data-System-Cryptocurrencies

This repository contains results of the project during Big Data Analytics course at WUT

## How to run the project?

### IMPORTANT

While running for the first time, the following steps had to be done:

1. In docker-compose.yaml comment volumes in hdfs-namenode and nifi (lines 15-17 and 90-92).

2. Run

    ```
    docker-compose --env-file stack.env up -d
    ```

3. When the contriners are running, run the following commands:

    ```
    docker cp hdfs-namenode:/hadoop/dfs/name ./hdfs/namenode
    docker cp hdfs-namenode:/etc/hadoop ./hdfs/namenode_etc
    docker cp nifi:/opt/nifi/nifi-current/conf ./nifi/nifi_data
    ```

4. Run

    ```
    docker-compose down
    ```

5. Uncomment lines which were commented in 1.

6. You can run now the containers normally, e.g. with:

    ```
    docker-compose --env-file stack.env up -d
    ```


### Runing next time

Each folder that start with `COMPOSE_*` contains `docker-compose.yaml` file to run different parts of the system. Study `README.md` files in each directory to see whether additional environment variables have to be set.

If the variables are set, you can run the following script to start all components:

```
./start.sh
```

In order to stop all containers, run:

```
./stop.sh
```
