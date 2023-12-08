# README

## Spark

Spark version 3.0.0

### Previous:

Spark version 3.2.4
Scala version 2.12.15, OpenJDK 64-Bit Server VM, 11.0.21

Spark version 3.5.0
Scala version 2.12.18, OpenJDK 64-Bit Server VM, 17.0.9

### Test example

Copy from PC to spark-master:

```
docker cp -L your_program.py spark-master:spark/anyfilename.py
```

Get to folder spark and execute:

```
/spark/bin/spark-submit anyfilename.py
```

#### Legacy

```
docker cp -L your_program.py spark-master:/opt/bitnami/spark/anyfilename.py
docker-compose exec spark-master spark-submit --master spark://10.30.0.20:7077 anyfilename.py
```

### Check version

```
docker-compose exec spark-master spark-submit --version
```
## Jupyter Notebook - finally we dont use it

We use the Jupyter Notebook to develop the prototypes of the final solutions implemented in Apache Spark.

We've managed to force our Jupyter to enable the user to gain *sudo* rights, removed the necessity to provide a token or password while running the service (crucial, as after the restart we lost those information), and assigned a proper local volume for saving the files, present in Jupyter's *work* directory.

### How to use it

To access the notebook you have to get into following link http://127.0.0.1:8888/lab or http://10.0.0.23:8888/lab

### Bash commands

To check spark, and scala version, run the following command in COMPOSE_spark folder:

```
docker-compose exec spark-master spark-submit --version
```

