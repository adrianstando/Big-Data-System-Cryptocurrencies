import pyspark
print(pyspark.version)
spark = pyspark.sql.SparkSession.builder.appName("Testing").getOrCreate()

data = [("J",2),("A",3)]
columns = ["1","2"]
df = spark.createDataFrame(data, columns)
print(df)
df.write.format("csv").save("hdfs://10.0.0.2:9870/tmp/df.csv")
import sys
sys.exit()