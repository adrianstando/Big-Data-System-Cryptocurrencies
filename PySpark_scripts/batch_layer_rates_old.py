from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

# Spark session definition
spark = SparkSession.builder \
    .appName("YourAppName") \
    .enableHiveSupport() \
    .getOrCreate()

# Getting file paths in directory
sc = spark.sparkContext
URI           = sc._gateway.jvm.java.net.URI
Path          = sc._gateway.jvm.org.apache.hadoop.fs.Path
FileSystem    = sc._gateway.jvm.org.apache.hadoop.fs.FileSystem
Configuration = sc._gateway.jvm.org.apache.hadoop.conf.Configuration

path = '/path/to/files/'
from py4j.java_gateway import java_import

fs = spark._jvm.org.apache.hadoop.fs.FileSystem.get(URI("hdfs://namenode:9000"), Configuration())
status = fs.listStatus(Path('/master_dataset/crypto_rates/'))
paths = [file.getPath().toString() for file in status if file.getPath().toString()[-4:]=="avro"]



# Loading data from HDFS
rates=spark.read.format("avro").load(paths[3000:])

# Filtering interesting cryptocurrencies
rates = rates.filter(col("symbol").isin(["BTC", "ETH", "DOGE"]))

# Casting timestamp to timestamp
rates = rates.na.fill(0)
rates = rates.withColumn("time_stamp", to_timestamp(col("timestamp").cast('double') / 1000))
rates = rates.withColumn("rateusd", col("priceUsd").cast('double') )
# Choice of columns
rates = rates.select(col("id"),col("symbol"),col("rateusd"), col("time_stamp"))

# Writing data to hive table
rates.write.mode('append').option("delimiter", "\;-_-;").format('hive').saveAsTable('cryptorates')
rates.show()