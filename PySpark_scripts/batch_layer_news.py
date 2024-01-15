from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.types import StructType, StringType, LongType
from pyspark.sql.functions import col, to_timestamp
from pyspark.sql import functions as F

# Spark session definition
spark = SparkSession.builder \
    .appName("YourAppName") \
    .enableHiveSupport() \
    .getOrCreate()

# Schema of article data
booksSchema = StructType()\
    .add("article_id",StringType())\
    .add("content",StringType())\
    .add("timestamp",LongType())
    


# Loading data from HDFS
folder = "/2024-01-13"
articles=spark.read.parquet(f"hdfs://namenode:9000/master_dataset/news/news_io{folder}")

### Bitcoin

# Adding temporary flags of articles containing words like BTC or bitcoin
articles = articles.withColumn("BTC", articles.content.contains('BTC'))
articles = articles.withColumn("Bitcoin", articles.content.contains('Bitcoin'))

# Combining above flags into singular flag which represents if article mentions bitcoin
articles = articles.withColumn("final_bitcoin", F.when((articles.BTC=="true") | (articles.Bitcoin == "true" ), 'true'))

### Ethereum

# Adding temporary flags of articles containing words like ETH or ethereum
articles = articles.withColumn("ETH", articles.content.contains('ETH'))
articles = articles.withColumn("Ethereum", articles.content.contains('Ethereum'))

# Combining above flags into singular flag which represents if article mentions ethereum
articles = articles.withColumn("final_ethereum", F.when((articles.ETH=="true") | (articles.Ethereum == "true" ), 'true'))

### Dogecoin

# Adding temporary flags of articles containing words like DOGE or Dogecoin
articles = articles.withColumn("DOGE", articles.content.contains('DOGE'))
articles = articles.withColumn("Dogecoin", articles.content.contains('Dogecoin'))

# Combining above flags into singular flag which represents if article mentions bitcoin
articles = articles.withColumn("final_dogecoin", F.when((articles.DOGE=="true") | (articles.Dogecoin == "true" ), 'true'))



# Filtering out articles that don't mention bitcoin
articles = articles.filter(col("Final_bitcoin") == "true")
articles = articles.withColumn("time_stamp", to_timestamp(col("timestamp").cast('double') / 1000))
articles = articles.select(col("article_id"),col("content"),col("time_stamp"), col("final_bitcoin"), col("final_ethereum"), col("final_dogecoin"))

# Writing data to hive table
articles.write.mode('append').option("delimiter", "\;-_-;").format('hive').saveAsTable('cryptonews')
articles.show()