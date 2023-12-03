#!/bin/bash

# Get the current parent directory
parent_directory=$(pwd)

COMPOSE_folders=("COMPOSE_hbase-hive" "COMPOSE_spark" "COMPOSE_kafka-cluster" "COMPOSE_nifi-hdfs")

echo ${COMPOSE_folders[*]}

for directory in ${COMPOSE_folders[*]}; do
    # Remove trailing slash to get the directory name
    dir_name="${directory%/}"

    # Change to the current directory
    cd "$dir_name"

    # Stop and remove containers defined in docker-compose.yml
    docker-compose down

    # Change back to the parent directory
    cd "$parent_directory"
done

