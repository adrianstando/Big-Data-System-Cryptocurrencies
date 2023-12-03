# README

## Spark

It is designed based on the article (https://medium.com/@mehmood9501/using-apache-spark-docker-containers-to-run-pyspark-programs-using-spark-submit-afd6da480e0f).

**WARNING** This time we have to run it via following command, as we have no stack.env file: docker-compose up -d

### Test example

```
docker cp -L your_program.py compose_spark-spark-master-1:/opt/bitnami/spark/anyfilename.py
```

*Execute:*

```
docker logs compose_spark-spark-master-1
```

Find sth like Starting Spark master at: *spark://172.X.0.2:7077*

```
docker-compose exec spark-master spark-submit --master spark://172.X.0.2:7077 anyfilename.py
```
## Jupyter Notebook

**WANING** Remember to save file locally, because for now we don't have a volume assigned to jupyter.

To access the notebook you have to get into following link http://127.0.0.1:8888/?token=TOKEN, and swap TOKEN with the value provided below.

After running in the following command in COMPOSE_spark directory: 

```
docker-compose --env-file stack.env up -d
```

Run the following code and find something like this *http://127.0.0.1:8888/lab?token=060dc836b804c2e5688bab72664df43a9f66e1571737a5b8* where X in token=X is your TOKEN.

```
docker logs --tail 2000 --follow --timestamps pyspark
```


