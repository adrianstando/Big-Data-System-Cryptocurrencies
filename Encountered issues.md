# Enocuntered issues log

## 11.11.23

* Used Tailscale for distributed computing which generated lots of issues (tens of hours spent by the whole team).

## 18.11.23

* We designed the first version of docker-compose for NiFi and HDFS - only one of us knew how it worked, and it worked properly only on 1 PC.

## 25.11.23

* We had issues with adding a volume to HDFS and NiFi, so we don't lose the data from both. We had to find a workaround by copying files from NiFi to local, and only then mounting the volume. A few hours lost.

## 01.12.23

* We had major issues with connecting Kafka to anything, after 5 hours we finally found out that it has to be in the same network as HDFS and Nifi.

## 02.12.23

* Only then did we realize that for the containers to see objects in different subnets we have to attach them to static IPs, so we had to design a whole network structure from scratch, write a bash script which starts it up, and so on.. another few hours.

## 03.12.23

* During the development an update to NiFi occured, they changed the requirements, and we had to mount the logs file to the volume additionally. Another hour lost.

* We had a problem with running Jupyter lab to develop the code, as it didn't see anything. It turned out that we had to configure route tables for all containers so they see themselves in various subnets.

* We couldn't do it so easily, as none of the services had the iproute2 package installed, and these were different distributions.. next hours lost.

* We had to write bash scripts for this purpose, even though none of us actually did this before. Lots of unknown errors occurred while we were developing a script that automatically generates proper route tables for each container so they can see each other.

* We wanted to use already created files for Kafka, so they contain topics, but it didn't work and caused Kafka to stop working. Half an hour lost.

* In fact, we spend most of the time on configuring the networks, dockers, and so on, and so far we did very little of proper Big Data actions.

## 07.12.23

* After next few hours lost in configuring the networks between various containers we decided to place all of them in the same network. From this time on, all resources are run on the Hubert's PC, as it has 32GB of RAM.

* We encountered multiple issues regarding the huge files in Kafka, when we couldn't push them to GitHub, thus we had to re-configure the .gitkeep file. On the way we messed up the commits, where some of them tried to push those huge files, and had to go back a bit in some cases.

* We had major issues with connecting a notebook inside the jupyter container to any dataseource (Kafka, NiFi). We thought that we have some issues with versions of Apache services, and that they are not compatible so we started digging.

* We found out that there isn't any official table which version of services are compatible. After an hour we finally found out seemingly compatible versions, but it didn't work and the pyspark told us that we sue 3.5 version, instead of 3.2 which was installed. At this point, it occured to us that on the jupyter notebook we connected to the Spark installed on the provided container, not our Spark.

* Finally, we found out compatible versions of Hadoop (3.2.1) and Spark (3.0.0), but we still were not able to connect any form of Python notebook to Spark.

* We decided to use Portainer, which enables direct access to containers consoles, and this way, people other than Hubert are able to run spark-submit of PySpark scripts to the container.

## 09.12.23

* We faced major issues while running Hive with our Hadoop, because of configuration files. After searching through the guides with setting up Hive with docker-compose we found out some variables that people set, and it came out that in the config for namenode we use port 9000, whereas for Hive we try to connect with port 8020. After the fix we can finally access Hive.

* During the changes for Hive to work, we introduced a major bug which made our Hadoop services unhealthy. We accidentally added unwanted SERVICE_PRECONDITION, which made the services unavailable.

* We faced a problem while connecting Spark to nodemanager, and it came out that we used wrong port for it 9870 instead of 9000.

* Another problems occured with connecting to Hive with PySpark, as by default it connected to spark-warehouse, and it seemed to not notice out Hive-metastore, even though we exlicitly pointed out where we want to connect. After 2 or 3 hours we finally found out that we had to copy hive-site.xml configuration file to Spark to enable connecting to proper Hive service. Learning on our mistakes, this time we configured hbase the same way upfront.

## 10.12.23

* We faced major issues with connecting to HBase from PySpark or Spark. We tried to find proper connectors in Maeven repository, or some automatic methods of determining those from GitHub. The abundance of terribly documented solutions makes it nearly impossible to find proper files. Circa 3 hours lost.

* Another approach to overcome these issues was installing Happybase on spark-master, however we run into the abundance of setup issues, which unabled us getting positive results. 1 hour lost.

* Finally, we switched to Cassandra, instead of HBase, which ended up being perfectly fit for connecting to Spark, and we didn't face any issues. Half an hour.

## 17.12.23

* While working with Spark (2 people running scripts) we killed Huberts PC and used all available RAM so he was not able restart processors and had to restart whole PC. The issues occur regularly, and are wasting lots of times.

* Due to multiple errors with installing python packages such as numpy on Spark container, we had to change from bde2020 image to bitami, which works on different operating system (Alpine -> Bitnami). Firstly we tried multiple approaches, including recommended `apk add python3-dev`, however it destroyed pip, and we were not able to install it again.

* Initially we intended to use a sentiment analysis model for whole texts, however it wieghted 0.5GB, which is too big for our containers, thus we decided to use smaller, one-sentence version, and aggregate the outcomes by assigning a mode of all sentences. It caused additional problems, as Spark 3.2 doesn't support this function, thus we had to design a workaround, which eventually worked out.

* We spent whole day on working with streams, with symbolic results. We managed to introduce a data preprocessing and reasonable aggregations, however we still cannot join two streams.

## 18.12.23

* 