# README

## Spark

It is designed based on the article (https://medium.com/@mehmood9501/using-apache-spark-docker-containers-to-run-pyspark-programs-using-spark-submit-afd6da480e0f).

**WARNING** This time we have to run it via following command, as we have no stack.env file: docker-compose up -d

### Test example

docker cp -L your_program.py compose_spark-spark-master-1:/opt/bitnami/spark/anyfilename.py

Execute:
docker logs spark_spark-master-1
Find sth like Starting Spark master at *spark://172.21.0.2:7077*

docker-compose exec compose_spark-spark-master-1 spark-submit --master spark://172.21.0.2:7077 anyfilename.py

**WARNING** Unfortunatelly it didn't work for me. I cannot execute the job, no idea why.