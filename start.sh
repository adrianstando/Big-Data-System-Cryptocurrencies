#!/bin/bash

# Loop through each subdirectory starting with the prefix 'COMPOSE_'
for directory in COMPOSE_*/; do
    # Remove trailing slash to get the directory name
    dir_name="${directory%/}"

    # Change to the current directory
    cd "$dir_name"

    # Run docker-compose up
    docker-compose --env-file stack.env up -d

    # Change back to the parent directory
    cd "$parent_directory"
done

