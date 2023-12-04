# Issues with containers:

* Used Tailscale for distributed computing which generated lots of issues (tens of hours spent by the whole team).

* We designed the first version of docker-compose for NiFi and HDFS - only one of us knew how it worked, and it worked properly only on 1 PC.

* We had issues with adding a volume to HDFS and NiFi, so we don't lose the data from both. We had to find a workaround by copying files from NiFi to local, and only then mounting the volume. A few hours lost.

* During the development an update to NiFi occured, they changed the requirements, and we had to mount the logs file to the volume additionally. Another hour lost.

* We had major issues with connecting Kafka to anything, after 5 hours we finally found out that it has to be in the same network as HDFS and Nifi.

* Only then did we realize that for the containers to see objects in different subnets we have to attach them to static IPs, so we had to design a whole network structure from scratch, write a bash script which starts it up, and so on.. another few hours.

* We had a problem with running Jupyter lab to develop the code, as it didn't see anything. It turned out that we had to configure route tables for all containers so they see themselves in various subnets.

* We couldn't do it so easily, as none of the services had the iproute2 package installed, and these were different distributions.. next hours lost.

* We had to write bash scripts for this purpose, even though none of us actually did this before. Lots of unknown errors occurred while we were developing a script that automatically generates proper route tables for each container so they can see each other.

* We wanted to use already created files for Kafka, so they contain topics, but it didn't work and caused Kafka to stop working. Half an hour lost. 

* In fact, we spend most of the time on configuring the networks, dockers, and so on, and so far we did very little of proper Big Data actions.