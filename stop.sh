#!/bin/bash

# Get the current parent directory
parent_directory=$(pwd)

# Loop through each subdirectory starting with the prefix 'COMPOSE_'
for directory in COMPOSE_*/; do
    # Remove trailing slash to get the directory name
    dir_name="${directory%/}"

    # Change to the current directory
    cd "$dir_name"

    # Stop and remove containers defined in docker-compose.yml
    docker-compose down

    # Change back to the parent directory
    cd "$parent_directory"
done

