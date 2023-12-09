#!/bin/bash

# Get the current parent directory
parent_directory=$(pwd)


COMPOSE_folders=("COMPOSE_nifi-hdfs" "COMPOSE_kafka-cluster" "COMPOSE_spark" "COMPOSE_hbase-hive")

echo ${COMPOSE_folders[*]}

for directory in ${COMPOSE_folders[*]}; do
    # Remove trailing slash to get the directory name
    dir_name="${directory%/}"

    # Change to the current directory
    cd "$dir_name"

    # Run docker-compose up
    docker-compose --env-file stack.env up -d

    # Change back to the parent directory
    cd "$parent_directory"
done
