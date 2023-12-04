# README

## Spark

It is designed based on the article (https://medium.com/@mehmood9501/using-apache-spark-docker-containers-to-run-pyspark-programs-using-spark-submit-afd6da480e0f).

### Test example

Execute the following command:

```
docker cp -L your_program.py compose_spark-spark-master-1:/opt/bitnami/spark/anyfilename.py
```

Execute the following command:

```
docker logs compose_spark-spark-master-1
```

Find something like Starting Spark master at: *spark://172.X.0.2:7077*

```
docker-compose exec spark-master spark-submit --master spark://172.X.0.2:7077 anyfilename.py
```
## Jupyter Notebook

We use the Jupyter Notebook to develop the prototypes of the final solutions implemented in Apache Spark.

We've managed to force our Jupyter to enable the user to gain *sudo* rights, removed the necessity to provide a token or password while running the service (crucial, as after the restart we lost those information), and assigned a proper local volume for saving the files, present in Jupyter's *work* directory.

### How to use it

To access the notebook you have to get into following link http://127.0.0.1:8888/lab or http://10.3.0.6:8888/lab



