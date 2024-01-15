import pyspark

# Spark session definition
spark = pyspark.sql.SparkSession.builder.appName("DataSimulatedFromHDFS").getOrCreate()

date = "2024-01-14"
# Getting file paths in directory
sc = spark.sparkContext
URI           = sc._gateway.jvm.java.net.URI
Path          = sc._gateway.jvm.org.apache.hadoop.fs.Path
FileSystem    = sc._gateway.jvm.org.apache.hadoop.fs.FileSystem
Configuration = sc._gateway.jvm.org.apache.hadoop.conf.Configuration

fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(URI("hdfs://namenode:9000"), Configuration())
status = fs.listStatus(Path(f'/master_dataset/crypto_rates/{date}'))
paths = [file.getPath().toString() for file in status]

print(paths[-1:])