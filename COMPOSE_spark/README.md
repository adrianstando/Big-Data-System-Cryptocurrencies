# README

## Spark

It is designed based on the article (https://medium.com/@mehmood9501/using-apache-spark-docker-containers-to-run-pyspark-programs-using-spark-submit-afd6da480e0f).

We have version 3.5.0
Scala: 2.12.18 OpenJDK 64-Bit Server VM, 17.0.9

### Test example

Execute the following commands while being in this folder:

```
docker cp -L your_program.py spark-master:/opt/bitnami/spark/anyfilename.py
docker-compose exec spark-master spark-submit --master spark://10.3.0.2:7077 anyfilename.py
```

### Check version

```
docker-compose exec spark-master spark-submit --version
```
## Jupyter Notebook

We use the Jupyter Notebook to develop the prototypes of the final solutions implemented in Apache Spark.

We've managed to force our Jupyter to enable the user to gain *sudo* rights, removed the necessity to provide a token or password while running the service (crucial, as after the restart we lost those information), and assigned a proper local volume for saving the files, present in Jupyter's *work* directory.

### How to use it

To access the notebook you have to get into following link http://127.0.0.1:8888/lab or http://10.0.0.23:8888/lab

### Bash commands

To check spark, and scala version, run the following command in COMPOSE_spark folder:

```
docker-compose exec spark-master spark-submit --version
```

