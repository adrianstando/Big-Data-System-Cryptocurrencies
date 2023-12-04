#!/bin/bash
# Get the current parent directory
parent_directory=$(pwd)

COMPOSE_folders=("COMPOSE_nifi-hdfs" "COMPOSE_kafka-cluster" "COMPOSE_spark" "COMPOSE_hbase-hive")

echo ${COMPOSE_folders[*]}

install_apt() {
	container_name=$1
	tailscale_ip=$2
	subnet_address=$3
	echo "step 1"
	docker exec -it -u 0 "$container_name" sh -c "apt-get update -y"
	echo "step 2"
	docker exec -it -u 0 "$container_name" sh -c "apt-get install iproute2 -y"
}

add_route() {
	container_name=$1
	tailscale_ip=$2
	subnet_address=$3
	echo $container_name
	echo $tailscale_ip
	echo $subnet_address
	echo "step 3"
	docker exec -it -u 0 "$container_name" sh -c "ip route add $subnet_address via $tailscale_ip"
	echo "step 4"
	docker exec -it -u 0 "$container_name" sh -c "ip route add 100.64.0.0/20 via $tailscale_ip"
}

for directory in ${COMPOSE_folders[*]}; do
	# Remove trailing slash to get the directory name
	dir_name="${directory%/}"
	# Change to the current directory
	cd "$dir_name"
	# Extract container names from docker-compose file, excluding those starting with "tailscale"
	containers=$(docker-compose config --services | grep -v '^tailscale')
	tailscale_container=$(docker-compose config --services | grep '^tailscale')
	tailscale_container_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$tailscale_container")
	subnet_addresses=("10.0.0.0/16" "10.1.0.0/16" "10.2.0.0/16" "10.3.0.0/16" "10.4.0.0/16" "10.5.0.0/16" "10.6.0.0/16" "10.7.0.0/16")
	
	echo ${subnet_addresses[*]}
	echo ${containers}

	# Loop through each container and add route
	for container in $containers; do
		install_apt "$container" "$tailscale_container_ip" "$subnet"
		for subnet in ${subnet_addresses[*]}; do
			add_route "$container" "$tailscale_container_ip" "$subnet"
		done
	done
    # Change back to the parent directory
    cd "$parent_directory"
done

