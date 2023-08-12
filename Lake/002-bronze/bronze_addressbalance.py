# Databricks notebook source
# MAGIC %md
# MAGIC #Ingestão da tabela address balance na camada bronze

# COMMAND ----------

# DBTITLE 1,Imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import date


# COMMAND ----------

# DBTITLE 1,Ingestão bronze
blob_folder = "dbfs:/mnt/criptoscamstorage/landing/walletexplorer/*_address_balance.json"
data_atual = date.today()

df = spark.read.json(blob_folder)

df = df.withColumn("data_carga",lit(data_atual))

df.write.format("delta")\
        .mode("append")\
        .partitionBy("data_carga")\
        .option("path","dbfs:/mnt/criptoscamstorage/bronze/addressbalance/")\
        .saveAsTable('bronze.addressbalance')

    
